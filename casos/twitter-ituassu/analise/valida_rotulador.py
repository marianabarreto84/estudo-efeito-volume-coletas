# -*- coding: utf-8 -*-
"""Valida o rotulador automatico de *stance* contra o gabarito humano (kappa).

Mede uma vez so, sobre o teste cego de 210, com o prompt ja congelado -- e o
que o PRE_REGISTRO_stance.md §4 definiu ANTES de qualquer medida:

  criterio 1: kappa de Cohen (3 classes EA/ED/NDA) >= 0,70
  criterio 2: acuracia do portao `cidadao` >= 0,90
  criterio 3: reportar SEMPRE em conjunto, sem escolher o melhor --
              kappa com duplicatas e sem; em todos os itens e restrito a
              confianca >= 2; e o teto (reteste humano).

Nao escolhe recorte: imprime todos e deixa o pior a vista.

Uso:  python analise/valida_rotulador.py
"""
import argparse
import csv
import io
import json
import math
import pathlib
import re
import unicodedata
from collections import Counter, OrderedDict

RAIZ = pathlib.Path(__file__).resolve().parents[1]
STANCE = RAIZ / "data" / "repl" / "compos2014" / "stance"
GOLD = STANCE / "gold_stance_teste_MARIANA.csv"
LLM = STANCE / "prerotulagem_teste_LLM.csv"
SAIDA_MD = STANCE / "RESULTADOS_stance_validacao.md"
SAIDA_JSON = STANCE / "validacao_stance.json"

ACEITE_KAPPA = 0.70
ACEITE_PORTAO = 0.90
CLASSES = ["EA", "ED", "NDA"]


def norm_texto(t):
    t = (t or "").lower()
    t = re.sub(r"^rt @[a-z0-9_]+:\s*", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip()


def kappa_cohen(a, b):
    """Kappa de Cohen para duas listas pareadas de rotulos."""
    n = len(a)
    if n == 0:
        return None
    cls = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cls)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def ic95_prop(k, n):
    """Wilson."""
    if n == 0:
        return (None, None)
    p, z = k / n, 1.959964
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def matriz(ouro, prev, classes=CLASSES):
    m = OrderedDict((o, OrderedDict((p, 0) for p in classes)) for o in classes)
    for o, p in zip(ouro, prev):
        if o in m and p in m[o]:
            m[o][p] += 1
    return m


def carrega():
    with io.open(GOLD, encoding="utf-8-sig", newline="") as fh:
        gold = list(csv.DictReader(fh))
    if not LLM.exists():
        raise SystemExit(
            "[erro] %s nao existe.\n"
            "       Rode antes: python analise/rotula_stance.py" % LLM)
    with io.open(LLM, encoding="utf-8-sig", newline="") as fh:
        llm = {r["id_tweet"]: r for r in csv.DictReader(fh)}
    faltam = [r["n"] for r in gold if r["id_tweet"] not in llm]
    if faltam:
        raise SystemExit("[erro] o rotulador nao cobriu %d itens: %s"
                         % (len(faltam), faltam[:10]))
    return gold, llm


def recorte(gold, llm, filtro=None, dedup=False):
    """Devolve (ouro, previsto) do stance sob um filtro e/ou deduplicado."""
    linhas = [r for r in gold if (filtro is None or filtro(r))]
    if dedup:
        vistos, unicas = set(), []
        for r in linhas:
            k = norm_texto(r["texto"])
            if k in vistos:
                continue
            vistos.add(k)
            unicas.append(r)
        linhas = unicas
    return ([r["stance"] for r in linhas],
            [llm[r["id_tweet"]]["stance"] for r in linhas])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args()
    gold, llm = carrega()
    res = {}

    # ---------- stance, nos quatro recortes pre-registrados ----------
    recortes = [
        ("todos", None, False),
        ("sem duplicatas", None, True),
        ("confianca >= 2", lambda r: r["confianca"] in ("2", "3"), False),
        ("confianca >= 2, sem dup.", lambda r: r["confianca"] in ("2", "3"), True),
    ]
    res["stance"] = {}
    for nome, filtro, dedup in recortes:
        o, p = recorte(gold, llm, filtro, dedup)
        ac = sum(1 for x, y in zip(o, p) if x == y) / len(o) if o else None
        res["stance"][nome] = {"n": len(o), "kappa": kappa_cohen(o, p), "acuracia": ac}

    # ---------- portao cidadao ----------
    og = [r["cidadao"] for r in gold]
    pg = [llm[r["id_tweet"]]["cidadao"] for r in gold]
    ac_todos = sum(1 for x, y in zip(og, pg) if x == y) / len(og)
    lo, hi = ic95_prop(sum(1 for x, y in zip(og, pg) if x == y), len(og))
    idx = [k for k, r in enumerate(gold) if r["cidadao"] != "?"]
    ac_sem = (sum(1 for k in idx if og[k] == pg[k]) / len(idx)) if idx else None
    res["portao"] = {
        "n": len(og), "acuracia": ac_todos, "ic95": [lo, hi],
        "kappa": kappa_cohen(og, pg),
        "acuracia_sem_interrogacao": ac_sem, "n_sem_interrogacao": len(idx),
    }

    # ---------- matriz de confusao e divergencias ----------
    o, p = recorte(gold, llm)
    res["matriz"] = {a: dict(b) for a, b in matriz(o, p).items()}
    div = [{"n": r["n"], "id": r["id_tweet"], "ouro": r["stance"],
            "llm": llm[r["id_tweet"]]["stance"], "conf": r["confianca"],
            "nda_tipo": r.get("nda_tipo", ""), "texto": r["texto"][:150]}
           for r in gold if r["stance"] != llm[r["id_tweet"]]["stance"]]
    res["n_divergencias"] = len(div)
    res["divergencias"] = div
    # polo: EA lido como ED ou vice-versa (o erro grave)
    res["divergencias_de_polo"] = sum(
        1 for d in div if {d["ouro"], d["llm"]} == {"EA", "ED"})

    res["distribuicoes"] = {
        "ouro": dict(Counter(r["stance"] for r in gold)),
        "llm": dict(Counter(llm[r["id_tweet"]]["stance"] for r in gold)),
    }
    k = res["stance"]["todos"]["kappa"]
    res["aceite"] = {
        "kappa_stance": {"medido": k, "minimo": ACEITE_KAPPA, "passa": k >= ACEITE_KAPPA},
        "acuracia_portao": {"medido": ac_todos, "minimo": ACEITE_PORTAO,
                            "passa": ac_todos >= ACEITE_PORTAO},
    }

    SAIDA_JSON.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------- relatorio ----------
    f = lambda x: "—" if x is None else ("%.3f" % x)
    L = ["# Validação do rotulador de *stance* — teste cego (210)", "",
         "> Medida **única**, sobre o teste cego, com o prompt congelado.",
         "> Critérios escritos em `PRE_REGISTRO_stance.md` §4, **antes** de medir.", "",
         "## 1. Critérios de aceite", "",
         "| critério | medido | mínimo | passa? |", "|---|---:|---:|:--:|",
         "| κ de Cohen (stance, 3 classes) | %s | %.2f | %s |"
         % (f(k), ACEITE_KAPPA, "✅" if k >= ACEITE_KAPPA else "❌"),
         "| acurácia do portão `cidadao` | %s | %.2f | %s |"
         % (f(ac_todos), ACEITE_PORTAO, "✅" if ac_todos >= ACEITE_PORTAO else "❌"),
         "", "## 2. κ do stance nos quatro recortes", "",
         "Reportados **em conjunto**, como o pré-registro exige.", "",
         "| recorte | n | κ | acurácia |", "|---|---:|---:|---:|"]
    for nome, _, _ in recortes:
        d = res["stance"][nome]
        L.append("| %s | %d | %s | %s |" % (nome, d["n"], f(d["kappa"]), f(d["acuracia"])))
    L += ["", "## 3. Portão `cidadao`", "",
          "| base | n | acurácia | κ |", "|---|---:|---:|---:|",
          "| todos os itens | %d | %s | %s |" % (len(og), f(ac_todos), f(res["portao"]["kappa"])),
          "| excluindo os `?` do gabarito | %d | %s | — |" % (len(idx), f(ac_sem)),
          "",
          "⚠ O pré-registro §4.2 pedia a acurácia em **duas bases** — todos os itens e",
          "só os decidíveis pelo CSV congelado —, porque o codebook permite à anotadora",
          "abrir o perfil vivo e o rotulador não tem esse acesso. **A segunda base não é",
          "computável**: a rotulagem não registrou em quais itens o perfil foi consultado.",
          "A linha dos `?` acima é o que mais se aproxima, e não substitui. Fica como",
          "limitação declarada, e como lição de instrumento: a consulta deveria ter sido",
          "marcada em `notas`.",
          "", "## 4. Matriz de confusão (linhas = gabarito, colunas = rotulador)", "",
          "| | " + " | ".join(CLASSES) + " |", "|---|" + "---|" * len(CLASSES)]
    for a in CLASSES:
        L.append("| **%s** | " % a + " | ".join(str(res["matriz"][a][b]) for b in CLASSES) + " |")
    L += ["",
          "Divergências: **%d** de 210. Divergências de **polo** (EA lido como ED, ou o "
          "contrário): **%d**." % (len(div), res["divergencias_de_polo"]),
          "", "## 5. Distribuições", "",
          "| classe | gabarito | rotulador |", "|---|---:|---:|"]
    for c in CLASSES:
        L.append("| %s | %d | %d |" % (c, res["distribuicoes"]["ouro"].get(c, 0),
                                       res["distribuicoes"]["llm"].get(c, 0)))
    L += ["", "## 6. Teto da tarefa", "",
          "O reteste intracodificador (40 itens, ≥ 7 dias depois) **ainda não foi feito**.",
          "Sem ele não há teto medido, e o κ acima não tem contra o que ser relativizado.",
          "No caso vacinas o teto foi 0,746.", ""]
    SAIDA_MD.write_text("\n".join(L), encoding="utf-8")

    print("\n".join(L[:34]))
    print("\ngravados:\n  %s\n  %s" % (SAIDA_MD, SAIDA_JSON))


if __name__ == "__main__":
    main()
