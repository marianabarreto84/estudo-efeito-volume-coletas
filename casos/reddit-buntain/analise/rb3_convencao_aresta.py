#!/usr/bin/env python3
"""RB3 — a convenção do limiar: aresta distinta x resposta contada.

Conferência independente de `rb3_escada_recorte.py`, escrita em 29/set/2026 antes
de o número ir para um slide. O artigo (§3.1) diz:

    "the directed edges between these nodes in E corresponded to comment replies
     directed from author to recipient. Edges in G were WEIGHTED BY THE NUMBER OF
     RESPONSES between the two users."

Logo uma ARESTA é um par (autor -> destinatário) distinto, e o número de respostas
é o PESO dela. "more than 20 outgoing edges" (§4.1) deve então significar >20
destinatários distintos, não >20 respostas.

`rb3_recorte_artigo.py` soma respostas. Este script mede as duas convenções, e os
dois limiares (>=20 e >20), para saber se o achado depende disso.

Uso: python analise/rb3_convencao_aresta.py
Requer o snapshot; rodar na cópia de dados, em Documents/dissertacao/.
"""
import sqlite3, os, sys, json
from collections import defaultdict

DB = os.path.join(os.path.dirname(__file__), "..", "data", "repl", "buntain2013",
                  "snapshot_buntain.sqlite")
SAIDA = os.path.join(os.path.dirname(__file__), "..", "data", "repl",
                     "buntain2013", "rb3_convencao_aresta.json")
BOTS = {"[deleted]", "AutoModerator", None, ""}
TUDO = 10 ** 9


def constroi(cx, n_subs, n_coms):
    """-> destinos[(autor, sr)] = {destinatario: n_respostas}"""
    subs = defaultdict(list)
    for sid, sr, au, sc in cx.execute(
            "SELECT id, subreddit, author, score FROM submissions"):
        subs[sr].append((sc or 0, sid, au))
    coms, autor = defaultdict(list), {}
    for cid, au, lid, par, sc in cx.execute(
            "SELECT id, author, link_id, parent_id, score FROM comments"):
        autor[cid] = au
        coms[(lid or "").split("_")[-1]].append((sc or 0, cid, au, par or ""))

    destinos = defaultdict(lambda: defaultdict(int))
    for sr, lst in subs.items():
        lst.sort(key=lambda t: -t[0])
        for _sc, sid, au_sub in lst[:n_subs]:
            cl = sorted(coms.get(sid, []), key=lambda t: -t[0])[:n_coms]
            ids = {c[1] for c in cl}
            for _s, _cid, au, par in cl:
                if au in BOTS:
                    continue
                pid = par.split("_")[-1]
                pai = au_sub if (par.startswith("t3_") or pid == sid) else (
                    autor.get(pid) if pid in ids else None)
                if pai is None or pai in BOTS or pai == au:
                    continue
                destinos[(au, sr)][pai] += 1
    return destinos


def qualifica(destinos, modo, limiar, estrito):
    """modo: 'arestas' (destinatarios distintos) ou 'respostas' (soma dos pesos)."""
    q = defaultdict(set)
    for (au, sr), d in destinos.items():
        g = len(d) if modo == "arestas" else sum(d.values())
        if (g > limiar) if estrito else (g >= limiar):
            q[au].add(sr)
    return q


def main():
    if not os.path.exists(DB):
        sys.exit(f"snapshot nao encontrado: {DB}")
    cx = sqlite3.connect(DB)

    print("ARTIGO: 279 participantes em 10 de 13 subreddits; 7 em >1 = 2,5%\n")
    print("== o RECORTE do artigo (top-100 x 200), pelas 4 convencoes ==")
    print(f"{'convencao':<34} {'particip.':>10} {'subs':>6} {'em >1':>14}")
    print("-" * 68)

    rec = constroi(cx, 100, 200)
    uni = constroi(cx, TUDO, TUDO)
    linhas = []
    for modo in ("arestas", "respostas"):
        for limiar, estrito in ((20, True), (20, False)):
            q = qualifica(rec, modo, limiar, estrito)
            pop = sorted(q)
            n = len(pop)
            vivos = len({s for ss in q.values() for s in ss})
            m = sum(1 for au in pop if len(q[au]) > 1)
            rot = f"{modo}, {'>' if estrito else '>='}{limiar}"
            print(f"{rot:<34} {n:>10} {vivos:>6} {m:>5} = {100*m/n if n else 0:>5.1f}%")

            # mesma populacao, universo, mesmo criterio
            qu = qualifica(uni, modo, limiar, estrito)
            mu = sum(1 for au in pop if len(qu.get(au, ())) > 1)
            linhas.append({"convencao": rot, "participantes": n, "subreddits": vivos,
                           "multi_recorte": m, "pct_recorte": round(100*m/n, 1) if n else 0,
                           "multi_universo_mesma_pop": mu,
                           "pct_universo_mesma_pop": round(100*mu/n, 1) if n else 0})

    print("\n== a ESCADA: mesma populacao, mesmo criterio, tudo coletado ==")
    print(f"{'convencao':<34} {'recorte':>12} {'universo':>12} {'fator':>7}")
    print("-" * 68)
    for L in linhas:
        f = (L["pct_universo_mesma_pop"] / L["pct_recorte"]) if L["pct_recorte"] else float("inf")
        print(f"{L['convencao']:<34} {L['pct_recorte']:>11.1f}% "
              f"{L['pct_universo_mesma_pop']:>11.1f}% {f:>6.0f}x")

    with open(SAIDA, "w", encoding="utf-8") as fh:
        json.dump({"artigo": {"participantes": 279, "subreddits": 10, "multi": 7,
                              "pct": 2.5}, "convencoes": linhas}, fh,
                  ensure_ascii=False, indent=1)
    print(f"\njson: {os.path.abspath(SAIDA)}")


if __name__ == "__main__":
    main()
