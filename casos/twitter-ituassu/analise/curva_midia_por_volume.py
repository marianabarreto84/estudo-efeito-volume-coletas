"""
Fase 3 (eixo midia) — curva A(volume): a conclusao converge a que volume?

O que se mede
-------------
Subamostras ALEATORIAS de tamanho n crescente do universo, com B replicas cada, e
a distribuicao de:
  - RTMV%  (retweet cujo 1o link e MV) sobre a janela 19-25/out, n_max = 32.193
           -> e a quantidade de H1 ("RTMV > 50%"), linha 2 da tabela mestre;
  - P(MV | ha midia)  sobre o universo pleno, n_max = 140.909
           -> e a quantidade da dominancia MV:MH, linha 1 da tabela mestre.

As duas perguntas que a curva responde
--------------------------------------
  (1) A que n a estimativa estabiliza? (banda de 95% estreita o bastante)
  (2) O 48,3% que o artigo obteve com n=700 cabe na banda de n=700? Se NAO cabe,
      a divergencia do artigo NAO e erro amostral — e VIES do esquema (100/dia nos
      horarios de pico). Essa distincao e o ponto: separa "coletou pouco" de
      "coletou torto", que a tabela mestre hoje nao separa.
  (3) A partir de que n a banda exclui 50%? — isto e, com que volume ALEATORIO ja
      daria para refutar H1. Resposta operacional, nao so diagnostico.

Decisoes registradas
--------------------
  - Classe recomputada pelo caminho CANONICO (1o link efetivo: campo `links`; se
    vazio, 1a URL do texto + cache de expansao). A coluna `classe_midia` gravada no
    snapshot e PRE-correcao de jul/2026 (MV 50.040 la, 66.370 no canonico) e NAO e
    usada.
  - Subamostragem SEM reposicao (analogo honesto de "coletar menos"), nao bootstrap
    com reposicao.
  - B = 300 replicas por ponto (o protocolo pede >= 30).

Uso: PYTHONIOENCODING=utf-8 python -u analise/curva_midia_por_volume.py
Saidas: stdout + data/repl/compos2014/curva_midia.json
"""
import json
import pathlib
import random
import sqlite3
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.resolve_midia import carrega_cache, classe_do_primeiro_link
from core.extrai_links import links_efetivos

D = pathlib.Path("data/repl/compos2014")
OUT_JSON = D / "curva_midia.json"
CACHE = carrega_cache(D / "expand_cache.sqlite")

B = 300
TAMANHOS = (100, 200, 350, 700, 1400, 2800, 5600, 11200, 22400)
PAPER_RTMV = 48.3          # amostra 100/dia por pico, n=700
PAPER_MV_DOM = 83.4        # P(MV | ha midia) no universo (valor canonico)


def log(m):
    print(m, flush=True)


def cls(links_json, texto):
    c, _ = classe_do_primeiro_link(links_efetivos(links_json, texto), CACHE)
    return c


def banda(vals):
    v = sorted(vals)
    n = len(v)
    return {"media": round(sum(v) / n, 2),
            "p2_5": round(v[int(0.025 * n)], 2),
            "p97_5": round(v[min(n - 1, int(0.975 * n))], 2)}


def curva(flags, n_max, rotulo, alvo_pct, denom_flags=None, poder_vs=None):
    """flags: lista de 0/1 (evento). denom_flags: se dado, so contam onde ==1.
    poder_vs: se dado (ex. 0.5), reporta o PODER — a fracao de replicas em que um
    teste unicaudal rejeitaria H0: p = poder_vs em favor de p < poder_vs (z<-1,645).
    E a pergunta operacional certa: nao "a banda exclui 50%?", e sim "com esse n,
    qual a chance de o pesquisador CONCLUIR corretamente?"."""
    log(f"\n== {rotulo} (n_max = {n_max:,}) ==")
    cab = f"   {'n':>7} {'media':>8} {'IC95 (p2,5-p97,5)':>22} {'largura':>9}"
    if poder_vs:
        cab += f" {'poder':>7}"
    log(cab)
    pontos = []
    idx = list(range(len(flags)))
    for n in list(TAMANHOS) + [n_max]:
        if n > n_max:
            continue
        reps, rejeicoes = [], 0
        nrep = B if n < n_max else 1
        for b in range(nrep):
            rnd = random.Random(10_000 + b)
            sel = rnd.sample(idx, n) if n < n_max else idx
            if denom_flags is None:
                k, d = sum(flags[i] for i in sel), n
            else:
                k = sum(flags[i] for i in sel)
                d = sum(denom_flags[i] for i in sel)
            if not d:
                continue
            reps.append(100 * k / d)
            if poder_vs:
                p0 = poder_vs
                z = (k / d - p0) / ((p0 * (1 - p0) / d) ** 0.5)
                if z < -1.645:          # unicaudal: p < p0
                    rejeicoes += 1
        bd = banda(reps)
        larg = round(bd["p97_5"] - bd["p2_5"], 2)
        pt = {"n": n, **bd, "largura_ic": larg, "n_replicas": len(reps)}
        linha = (f"   {n:>7,} {bd['media']:>7.2f}% "
                 f"{bd['p2_5']:>10.2f}–{bd['p97_5']:<10.2f} {larg:>8.2f}")
        if poder_vs:
            pt["poder_pct"] = round(100 * rejeicoes / len(reps), 1)
            linha += f" {pt['poder_pct']:>6.1f}%"
        pontos.append(pt)
        log(linha)
    return pontos


def main():
    t0 = time.time()
    con = sqlite3.connect(D / "snapshot_hashtag.sqlite")
    con.row_factory = sqlite3.Row

    log("== Carregando e classificando (caminho canonico) ==")
    linhas = con.execute("SELECT links, texto, status_retweet, data_brt "
                         "FROM tweets").fetchall()
    con.close()
    classes, rt, janela = [], [], []
    for r in linhas:
        classes.append(cls(r["links"], r["texto"]))
        rt.append(1 if r["status_retweet"] else 0)
        janela.append(1 if "2014-10-19" <= r["data_brt"][:10] <= "2014-10-25" else 0)
    from collections import Counter
    dist = Counter(classes)
    log(f"   {len(classes):,} tweets · distribuicao: "
        + " · ".join(f"{k} {v:,}" for k, v in dist.most_common()))
    log("   (confere com RESULTADOS_analise_midia_MV_MH.md §1: MV 66.370, NDA 37.921,"
        " nao_resolvido 18.480, MH 13.233, indefinido 4.905)")

    # ---------- curva 1: RTMV na janela ----------
    jan = [i for i in range(len(classes)) if janela[i]]
    rtmv = [1 if (rt[i] and classes[i] == "MV") else 0 for i in jan]
    p1 = curva(rtmv, len(jan), "RTMV% — janela 19-25/out (H1)", PAPER_RTMV,
               poder_vs=0.5)

    # ---------- curva 2: P(MV | ha midia) no universo pleno ----------
    hamidia = [1 if c in ("MV", "MH") else 0 for c in classes]
    ehmv = [1 if c == "MV" else 0 for c in classes]
    p2 = curva(ehmv, len(classes), "P(MV | ha midia) — universo pleno",
               PAPER_MV_DOM, denom_flags=hamidia)

    # ---------- leitura ----------
    log("\n== Leitura ==")
    n700 = next(p for p in p1 if p["n"] == 700)
    log(f"   (2) Em n=700 ALEATORIO, RTMV cai em {n700['p2_5']:.1f}–{n700['p97_5']:.1f}%.")
    dentro = n700["p2_5"] <= PAPER_RTMV <= n700["p97_5"]
    log(f"       O {PAPER_RTMV}% do artigo {'CABE' if dentro else 'NAO CABE'} nessa banda"
        f" -> a divergencia e {'erro amostral' if dentro else 'VIES DO ESQUEMA'}.")

    p80 = next((p for p in p1 if p.get("poder_pct", 0) >= 80), None)
    p95 = next((p for p in p1 if p.get("poder_pct", 0) >= 95), None)
    log("   (3) PODER de refutar H1 com amostra ALEATORIA (teste unicaudal, a=0,05):")
    for p in p1:
        if p["n"] <= 2800:
            log(f"       n={p['n']:>5,} -> {p['poder_pct']:>5.1f}%")
    if p80:
        log(f"       80% de poder em n = {p80['n']:,}"
            + (f" · 95% em n = {p95['n']:,}" if p95 else ""))
    est = next((p for p in p1 if p["largura_ic"] < 5), None)
    if est:
        log(f"   (1) Banda < 5 p.p. a partir de n = {est['n']:,}.")

    n700b = next(p for p in p2 if p["n"] == 700)
    log(f"   Dominancia MV: em n=700 aleatorio, {n700b['p2_5']:.1f}–{n700b['p97_5']:.1f}%"
        f" (universo {PAPER_MV_DOM}%) — converge cedo.")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/curva_midia_por_volume.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "B_replicas": B,
        "metodo": "subamostragem sem reposicao; classe pelo 1o link efetivo",
        "distribuicao_classes": dict(dist),
        "curva_rtmv_janela": p1,
        "curva_mv_dominancia": p2,
        "paper": {"rtmv_amostra_700": PAPER_RTMV, "mv_dominancia": PAPER_MV_DOM},
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
