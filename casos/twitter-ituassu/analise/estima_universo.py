# -*- coding: utf-8 -*-
"""Estimativa CORRIGIDA das proporcoes de stance no universo, e a curva (§6).

O rotulador reprovou o criterio do §4 (kappa 0,604 < 0,70) e continua reprovado.
Este script nao o reabilita: usa-o como instrumento de ESTIMATIVA AGREGADA,
corrigindo o vies pela matriz de confusao medida nos 210.

  M[i][j] = P(rotulo automatico = j | rotulo humano = i)      (estimada nos 210)
  q       = proporcoes que o rotulador produz na amostra do universo
  q = M^T p   ->   p = (M^T)^-1 q      projetada no simplex quando cai fora

Incerteza por bootstrap propagando as DUAS fontes: a matriz (reamostra os 210,
estratificado por classe humana) e a amostra do universo. O intervalo sai mais
largo que o ingenuo, e e esse o ponto -- o preco do ruido aparece, nao some.

Tudo declarado em PRE_REGISTRO_stance.md §6.3 e §6.4 ANTES de rodar.

Uso:  PYTHONUTF8=1 python analise/estima_universo.py
"""
import csv
import io
import json
import pathlib
import random

import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[1]
STANCE = RAIZ / "data" / "repl" / "compos2014" / "stance"
GOLD = STANCE / "gold_stance_teste_MARIANA.csv"
LLM210 = STANCE / "prerotulagem_teste_LLM.csv"
UNIV = STANCE / "rotulos_universo_LLM.csv"
AMOSTRA = STANCE / "amostra_universo_stance.json"
SAIDA_MD = STANCE / "RESULTADOS_stance_universo.md"
SAIDA_JSON = STANCE / "curva_stance_universo.json"

CLASSES = ["EA", "ED", "NDA"]
B = 2000                     # reamostragens do bootstrap
PONTOS = [100, 200, 500, 1000, 2000, 5000]
SORTEIOS_POR_PONTO = 200
TOL_PP = 3.0                 # criterio de convergencia: +-3 p.p. (§6.4)
SEED = 20260909


def proj_simplex(v):
    """Projecao euclidiana no simplex de probabilidade."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    theta = (css[rho] - 1.0) / (rho + 1.0)
    return np.maximum(v - theta, 0.0)


def matriz_confusao(pares):
    """M[i][j] = P(llm=j | humano=i), linhas normalizadas."""
    M = np.zeros((3, 3))
    for h, l in pares:
        M[CLASSES.index(h), CLASSES.index(l)] += 1
    linhas = M.sum(axis=1, keepdims=True)
    linhas[linhas == 0] = 1.0
    return M / linhas


def corrige(M, q):
    try:
        p = np.linalg.solve(M.T, q)
    except np.linalg.LinAlgError:
        p = np.linalg.lstsq(M.T, q, rcond=None)[0]
    return proj_simplex(p) if (p.min() < 0 or abs(p.sum() - 1) > 1e-9) else p


def prop(rotulos):
    n = len(rotulos)
    return np.array([sum(1 for r in rotulos if r == c) / n for c in CLASSES])


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)

    with io.open(GOLD, encoding="utf-8-sig", newline="") as fh:
        gold = list(csv.DictReader(fh))
    with io.open(LLM210, encoding="utf-8-sig", newline="") as fh:
        llm = {r["id_tweet"]: r for r in csv.DictReader(fh)}
    pares = [(r["stance"], llm[r["id_tweet"]]["stance"]) for r in gold]

    with io.open(UNIV, encoding="utf-8-sig", newline="") as fh:
        univ = list(csv.DictReader(fh))
    doc = json.loads(AMOSTRA.read_text(encoding="utf-8"))
    rot_univ = [r["stance"] for r in univ]
    assert len(rot_univ) == doc["n_total"], (len(rot_univ), doc["n_total"])

    M = matriz_confusao(pares)
    q = prop(rot_univ)
    p = corrige(M, q)

    # ---------- bootstrap: matriz + amostra ----------
    por_classe = {c: [pr for pr in pares if pr[0] == c] for c in CLASSES}
    idx = np.arange(len(rot_univ))
    amostras = []
    for _ in range(B):
        rep = []
        for c in CLASSES:                       # estratificado por classe humana
            v = por_classe[c]
            if v:
                rep += [v[rng.randrange(len(v))] for _ in range(len(v))]
        Mb = matriz_confusao(rep)
        sel = nprng.choice(idx, size=len(idx), replace=True)
        qb = prop([rot_univ[i] for i in sel])
        amostras.append(corrige(Mb, qb))
    amostras = np.array(amostras)
    ic = np.percentile(amostras, [2.5, 97.5], axis=0)

    res = {
        "amostra": {"n": doc["n_total"], "sha": doc["sha256_12_dos_ids"],
                    "populacao": doc["populacao"]["n_populacao"],
                    "textos_distintos": doc["grupos_de_texto"]},
        "matriz_confusao": {CLASSES[i]: {CLASSES[j]: float(M[i, j]) for j in range(3)}
                            for i in range(3)},
        "bruto": {c: float(q[k]) for k, c in enumerate(CLASSES)},
        "corrigido": {c: float(p[k]) for k, c in enumerate(CLASSES)},
        "ic95_corrigido": {c: [float(ic[0, k]), float(ic[1, k])]
                           for k, c in enumerate(CLASSES)},
    }

    # ---------- curva ----------
    curva = []
    for n in PONTOS:
        pontos = []
        for _ in range(SORTEIOS_POR_PONTO):
            sel = nprng.choice(idx, size=min(n, len(idx)), replace=False)
            pontos.append(corrige(M, prop([rot_univ[i] for i in sel])))
        pontos = np.array(pontos)
        curva.append({
            "n": n,
            "media": {c: float(pontos[:, k].mean()) for k, c in enumerate(CLASSES)},
            "ic95": {c: [float(np.percentile(pontos[:, k], 2.5)),
                         float(np.percentile(pontos[:, k], 97.5))]
                     for k, c in enumerate(CLASSES)},
        })
    res["curva"] = curva

    # convergencia (§6.4): IC95 inteiro dentro de +-3 p.p. do valor em n=5000
    alvo = {c: curva[-1]["media"][c] for c in CLASSES}
    conv = {}
    for c in CLASSES:
        conv[c] = None
        for ponto in curva:
            lo, hi = ponto["ic95"][c]
            if (abs(lo - alvo[c]) * 100 <= TOL_PP) and (abs(hi - alvo[c]) * 100 <= TOL_PP):
                conv[c] = ponto["n"]
                break
    res["convergencia_n"] = conv
    res["criterio_convergencia"] = "IC95 inteiro a menos de %.0f p.p. do valor em n=5000" % TOL_PP

    # razao EA/ED, que e a forma da afirmacao do artigo
    r_art = 226 / 284.0        # artigo 2015: EA 226, ED 284 (entre os cidadaos)
    razao_boot = amostras[:, 0] / np.maximum(amostras[:, 1], 1e-12)
    res["razao_EA_ED"] = {
        "corrigida": float(p[0] / p[1]) if p[1] > 0 else None,
        "ic95": [float(np.percentile(razao_boot, 2.5)),
                 float(np.percentile(razao_boot, 97.5))],
        "artigo_2015": r_art,
    }

    SAIDA_JSON.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    f = lambda x: "%.1f%%" % (100 * x)
    L = ["# *Stance* no universo — estimativa corrigida pela matriz de confusão", "",
         "> Desenho registrado em `PRE_REGISTRO_stance.md` §6, **antes** de sortear e de",
         "> rotular. O rotulador **continua reprovado** no critério do §4 (κ 0,604 < 0,70);",
         "> aqui ele é usado como instrumento de **estimativa agregada**, com o viés",
         "> corrigido, e não como instrumento de rótulo individual.", "",
         "## 1. Amostra", "",
         "| item | valor |", "|---|---|",
         "| população | %s tweets (19–25/out/2014) |" % f"{res['amostra']['populacao']:,}".replace(",", "."),
         "| amostra | %s itens em %s textos distintos |"
         % (f"{res['amostra']['n']:,}".replace(",", "."),
            f"{res['amostra']['textos_distintos']:,}".replace(",", ".")),
         "| `sha256(ids)[:12]` | `%s` |" % res["amostra"]["sha"],
         "", "## 2. Proporções", "",
         "| classe | bruto (rotulador) | **corrigido** | IC95% |",
         "|---|---:|---:|---:|"]
    for c in CLASSES:
        lo, hi = res["ic95_corrigido"][c]
        L.append("| %s | %s | **%s** | [%s; %s] |"
                 % (c, f(res["bruto"][c]), f(res["corrigido"][c]), f(lo), f(hi)))
    L += ["", "## 3. Curva `A(volume)`", "",
          "Estimativa corrigida em subamostras crescentes, %d sorteios por ponto." % SORTEIOS_POR_PONTO,
          "", "| n | EA | ED | NDA |", "|---:|---:|---:|---:|"]
    for ponto in curva:
        L.append("| %s | %s | %s | %s |"
                 % (f"{ponto['n']:,}".replace(",", "."),
                    f(ponto["media"]["EA"]), f(ponto["media"]["ED"]), f(ponto["media"]["NDA"])))
    L += ["", "**Convergência** (%s):" % res["criterio_convergencia"], ""]
    for c in CLASSES:
        L.append("- %s: %s" % (c, ("n = %s" % f"{conv[c]:,}".replace(",", "."))
                               if conv[c] else "não convergiu dentro da amostra"))
    L += ["", "## 4. A afirmação do artigo", "",
          "O artigo de 2015 reporta, entre os 666 cidadãos: ED 284 (42,6%) contra EA 226",
          "(33,9%%) — razão EA/ED = **%.2f**, isto é, **ED > EA**." % r_art, "",
          "Aqui a razão EA/ED corrigida é **%.2f** (IC95%% [%.2f; %.2f])."
          % (res["razao_EA_ED"]["corrigida"], *res["razao_EA_ED"]["ic95"]), ""]
    SAIDA_MD.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print("\ngravados:\n  %s\n  %s" % (SAIDA_MD, SAIDA_JSON))


if __name__ == "__main__":
    main()
