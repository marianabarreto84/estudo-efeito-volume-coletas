"""
Fase 3 / eixo A — AV4b: o topo da distribuicao de RTs e dominado pelos anti?

A afirmacao do alvo (§3-4): "o top-10 e dominado pelos anti — 9 dos 10 tweets
mais retuitados". E a peca que sustenta a leitura 'o lado anti ficou com a
atencao'. O AV4 ja replicado mediu a CONCENTRACAO (top-10 = 15,7% dos RTs);
a COMPOSICAO desse topo (quantos sao pro, quantos anti) nunca foi medida.

Mede-se tres coisas:
  (A) COMPOSICAO DO TOPO — entre os k tweets mais retuitados, quantos de cada
      lado. Testa a frase '9 dos 10' ao pe da letra e ve ate onde ela vale.
  (B) DESPROPORCAO — fatia de RTs de cada lado dividida pela fatia de tweets.
      R > 1 = o lado captura atencao acima do seu peso em volume. E a mesma
      convencao adotada no caso meta-ads (DECISOES_CB2.md), de proposito:
      as duas linhas da tabela mestre precisam ser comparaveis.
  (C) POR FAIXA — a composicao ao longo da distribuicao, para ver se o topo e
      qualitativamente diferente do resto ou se e so o fim de um gradiente.

Tambem por AUTOR, porque a frase do artigo mistura 'top-10 autores' (a
concentracao) com 'tweets mais retuitados' (a composicao).

Dados
-----
  - RTs por tweet: coluna `retweets` dos originais (a que reproduziu o AV4).
  - Lado por tweet: rotulos do eixo B (`e1_lim10_pt_p4`, esquema BINARIO do
    artigo, k 0,759). Sensibilidade com `p6` (tres classes).
  - Cobertura: rotulos existem para tweets pt com >10 RT (29.978). O topo da
    distribuicao esta inteiro dentro dessa faixa, entao (A) e (B) nao sofrem
    censura; (C) so vale de 10 RT para cima.

Uso: PYTHONIOENCODING=utf-8 python -u analise/av4_topo_por_lado.py
Saidas: stdout + data/repl/vacinas2022/av4_topo_por_lado.json
"""
import collections
import csv
import json
import pathlib
import sqlite3
import time

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
ROT = RAIZ / "data/repl/vacinas2022/rotulos_llm"
OUT_JSON = RAIZ / "data/repl/vacinas2022/av4_topo_por_lado.json"

TOPOS = (10, 20, 50, 100, 500, 1000)
FAIXAS = [(100000, None), (10000, 100000), (5000, 10000), (1000, 5000),
          (500, 1000), (100, 500), (50, 100), (10, 50)]
ESQUEMAS = {"p4": "e1_lim10_pt_p4", "p6": "e1_lim10_pt_p6"}


def log(m):
    print(m, flush=True)


def carrega_rotulos(pasta):
    d = {}
    with open(ROT / pasta / "rotulos.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d[r["ID"]] = r["stance"]
    return d


def main():
    t0 = time.time()

    db = sqlite3.connect(SNAP)
    linhas_db = db.execute(
        "SELECT twitter_id, autor, retweets FROM originais "
        "WHERE idioma='pt' AND retweets IS NOT NULL").fetchall()
    db.close()
    rts = {str(i): n for i, _, n in linhas_db}
    autor_de = {str(i): a for i, a, _ in linhas_db}
    log(f"{len(rts):,} tweets pt com contagem de RT no snapshot")

    resultado = {}
    for esq, pasta in ESQUEMAS.items():
        rot = carrega_rotulos(pasta)
        # so os tweets rotulados, ordenados por RT desc
        seq = sorted(((rts[t], t, lado) for t, lado in rot.items() if t in rts),
                     reverse=True)
        log(f"\n{'='*66}\n== Esquema {esq} — {len(seq):,} tweets rotulados com RT ==")

        # ---- (A) composicao do topo ----
        log("\n-- (A) composicao dos k tweets mais retuitados --")
        log(f"   {'k':>6} {'pro':>6} {'anti':>6} {'nenhum':>7} {'%anti':>7} {'RT min':>9}")
        topo = []
        for k in TOPOS:
            c = collections.Counter(l for _, _, l in seq[:k])
            decididos = c["pro"] + c["anti"]
            pct_anti = 100 * c["anti"] / decididos if decididos else float("nan")
            topo.append({"k": k, "pro": c["pro"], "anti": c["anti"],
                         "nenhum": c["nenhum"], "pct_anti_entre_decididos":
                         round(pct_anti, 1), "rt_minimo": seq[k - 1][0]})
            log(f"   {k:>6} {c['pro']:>6} {c['anti']:>6} {c['nenhum']:>7} "
                f"{pct_anti:>6.1f}% {seq[k-1][0]:>9,}")

        # os 10 mais retuitados, um a um (e a frase literal do artigo)
        log("\n   os 10 mais retuitados, na ordem:")
        for pos, (n, tid, lado) in enumerate(seq[:10], 1):
            log(f"     {pos:>2}. {n:>8,} RT  [{lado:>6}]  @{autor_de.get(tid,'?')}")

        # ---- (B) desproporcao: fatia de RTs / fatia de tweets ----
        log("\n-- (B) desproporcao (fatia de RTs / fatia de tweets) --")
        n_lado = collections.Counter(l for _, _, l in seq)
        rt_lado = collections.Counter()
        for n, _, lado in seq:
            rt_lado[lado] += n
        tot_n, tot_rt = len(seq), sum(rt_lado.values())
        desprop = {}
        log(f"   {'lado':>8} {'tweets':>8} {'%tw':>7} {'RTs':>12} {'%RT':>7} {'R':>6}")
        for lado in ("pro", "anti", "nenhum"):
            if not n_lado[lado]:
                continue
            f_tw, f_rt = n_lado[lado] / tot_n, rt_lado[lado] / tot_rt
            R = f_rt / f_tw
            desprop[lado] = {"tweets": n_lado[lado], "frac_tweets": round(f_tw, 4),
                             "rts": rt_lado[lado], "frac_rts": round(f_rt, 4),
                             "R": round(R, 3)}
            log(f"   {lado:>8} {n_lado[lado]:>8,} {100*f_tw:>6.1f}% "
                f"{rt_lado[lado]:>12,} {100*f_rt:>6.1f}% {R:>6.2f}")

        # ---- (C) composicao por faixa de RT ----
        log("\n-- (C) composicao por faixa de RT --")
        log(f"   {'faixa':>16} {'n':>7} {'%pro':>7} {'%anti':>7} {'%nenhum':>8} {'razao':>7}")
        faixas = []
        for lo, hi in FAIXAS:
            sub = [l for n, _, l in seq if n >= lo and (hi is None or n < hi)]
            if not sub:
                continue
            c = collections.Counter(sub)
            tot = len(sub)
            razao = c["pro"] / c["anti"] if c["anti"] else float("inf")
            rot_faixa = f"{lo:,}+" if hi is None else f"{lo:,}-{hi:,}"
            faixas.append({"faixa": rot_faixa, "n": tot, "pro": c["pro"],
                           "anti": c["anti"], "nenhum": c["nenhum"],
                           "razao_pro_anti": round(razao, 3)})
            log(f"   {rot_faixa:>16} {tot:>7,} {100*c['pro']/tot:>6.1f}% "
                f"{100*c['anti']/tot:>6.1f}% {100*c['nenhum']/tot:>7.1f}% {razao:>7.2f}")

        # ---- (D) por autor: o top-10 de autores do AV4 ----
        rt_autor = collections.Counter()
        lados_autor = collections.defaultdict(collections.Counter)
        for n, tid, lado in seq:
            a = autor_de.get(tid)
            if a:
                rt_autor[a] += n
                lados_autor[a][lado] += 1
        top_autores = rt_autor.most_common(10)
        log("\n-- (D) os 10 autores com mais RTs (o top-10 do AV4) --")
        autores = []
        for pos, (a, n) in enumerate(top_autores, 1):
            c = lados_autor[a]
            dominante = max(("pro", "anti", "nenhum"), key=lambda l: c[l])
            autores.append({"pos": pos, "autor": a, "rts": n,
                            "lado_dominante": dominante, "pro": c["pro"],
                            "anti": c["anti"], "nenhum": c["nenhum"]})
            log(f"     {pos:>2}. {n:>9,} RT  [{dominante:>6}]  @{a}  "
                f"(pro {c['pro']} / anti {c['anti']} / nenhum {c['nenhum']})")
        c_top = collections.Counter(x["lado_dominante"] for x in autores)
        log(f"   composicao do top-10 de autores: pro {c_top['pro']} / "
            f"anti {c_top['anti']} / nenhum {c_top['nenhum']}")

        resultado[esq] = {"topo": topo, "desproporcao": desprop,
                          "por_faixa": faixas, "top10_autores": autores,
                          "top10_autores_composicao": dict(c_top)}

    OUT_JSON.write_text(json.dumps({
        "script": "analise/av4_topo_por_lado.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "fonte_rts": "coluna `retweets` dos originais (pt)",
        "fonte_lado": "rotulos do eixo B (E1, >10 RT, pt)",
        "afirmacao_alvo": "top-10 dominado pelos anti (9 dos 10 mais retuitados)",
        "por_esquema": resultado,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
