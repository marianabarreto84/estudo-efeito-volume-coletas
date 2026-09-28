#!/usr/bin/env python3
"""RB3 — reconstrução do RECORTE do artigo sobre o snapshot completo.

Complementa `rb3.py`. Enquanto aquele mede o universo, este responde à pergunta
inversa (levantada pela Mariana em 25/set/2026): aplicando ao nosso dado o mesmo
desenho de coleta do artigo — top-100 submissões por subreddit, ~200 comentários
de cada, grafo dirigido POR subreddit, corte de >=20 arestas de saída —, a fração
multi-comunidade volta aos ~3% publicados?

Isso separa o efeito do RECORTE do efeito de dado/método diferente, que a
comparação da Tabela `tab:reddit-rb3` deixa confundidos.

Detalhe que fixa a leitura do corte: o artigo termina com 279 usuários em 10 dos
13 subreddits, tendo descartado 3 "por não ter usuário acima do limiar" — o que
só é possível se o corte for avaliado DENTRO de cada rede, e não globalmente.

Uso: python analise/rb3_recorte_artigo.py
Requer o snapshot (não versionado); rodar na cópia de dados, em Documents/dissertacao/.
"""
import sqlite3, os, sys, json
from collections import defaultdict

DB = os.path.join(os.path.dirname(__file__), "..", "data", "repl", "buntain2013",
                  "snapshot_buntain.sqlite")
SAIDA = os.path.join(os.path.dirname(__file__), "..", "data", "repl",
                     "buntain2013", "rb3_recorte_artigo.json")
BOTS = {"[deleted]", "AutoModerator", None, ""}
N_SUBS, N_COMS, LIMIAR = 100, 200, 20
TUDO = 10 ** 9


def carrega(cx):
    subs = defaultdict(list)
    for sid, sr, au, sc in cx.execute(
            "SELECT id, subreddit, author, score FROM submissions"):
        subs[sr].append((sc or 0, sid, au))
    coms, autor_por_id, presenca_universo = defaultdict(list), {}, defaultdict(set)
    for cid, sr, au, cu, par, lid, sc in cx.execute(
            "SELECT id, subreddit, author, created_utc, parent_id, link_id, score "
            "FROM comments"):
        autor_por_id[cid] = au
        coms[(lid or "").split("_")[-1]].append((sc or 0, cu or 0, cid, au, par or ""))
        if au not in BOTS:
            presenca_universo[au].add(sr)
    for sr, lst in subs.items():
        for sc, sid, au in lst:
            if au not in BOTS:
                presenca_universo[au].add(sr)
    return subs, coms, autor_por_id, presenca_universo


def recorte(subs, coms, autor_por_id, n_subs=N_SUBS, n_coms=N_COMS):
    """Aplica o desenho do artigo. -> (saida[(autor,sr)], presenca_no_recorte)."""
    saida, presenca = defaultdict(int), defaultdict(set)
    for sr, lst in subs.items():
        lst.sort(key=lambda t: -t[0])
        for _sc, sid, au_sub in lst[:n_subs]:
            cl = sorted(coms.get(sid, []), key=lambda t: -t[0])[:n_coms]
            ids = {c[2] for c in cl}
            if au_sub not in BOTS:
                presenca[au_sub].add(sr)
            for _s, _c, _cid, au, par in cl:
                if au in BOTS:
                    continue
                presenca[au].add(sr)
                pid = par.split("_")[-1]
                pai = au_sub if (par.startswith("t3_") or pid == sid) else (
                    autor_por_id.get(pid) if pid in ids else None)
                if pai is None or pai in BOTS or pai == au:
                    continue
                saida[(au, sr)] += 1          # aresta de saída de quem responde
    return saida, presenca


def qualificados(saida, limiar=LIMIAR):
    q = defaultdict(set)
    for (au, sr), g in saida.items():
        if g >= limiar:
            q[au].add(sr)
    return q


def main():
    if not os.path.exists(DB):
        sys.exit(f"snapshot não encontrado: {DB}")
    cx = sqlite3.connect(DB)
    subs, coms, autor_por_id, presenca_universo = carrega(cx)

    saida, presenca_rec = recorte(subs, coms, autor_por_id)
    qual = qualificados(saida)
    pop = sorted(qual)
    n = len(pop)
    vivos = len({s for ss in qual.values() for s in ss})

    print("ARTIGO: 279 participantes em 10 de 13 subreddits; 7 em >1 = 2,5% (~3%)\n")
    print(f"== reconstrução do recorte (top-{N_SUBS} x {N_COMS}, saída >={LIMIAR} por rede) ==")
    print(f"  participantes:                {n:>6,}   (artigo: 279)")
    print(f"  subreddits com alguém acima:  {vivos:>6}   (artigo: 10 de 13)")

    a = sum(1 for au in pop if len(qual[au]) > 1)
    b = sum(1 for au in pop if len(presenca_rec[au]) > 1)
    c = sum(1 for au in pop if len(presenca_universo[au]) > 1)
    print(f"\n== MESMA população, três modos de enxergá-la ==")
    print(f"  qualificado em >1 rede (o que o artigo conta): {a:>5} = {100*a/n:>5.1f}%")
    print(f"  presente em >1 subreddit, dentro do recorte:   {b:>5} = {100*b/n:>5.1f}%")
    print(f"  presente em >1 subreddit, no universo:         {c:>5} = {100*c/n:>5.1f}%")

    dist = defaultdict(int)
    for au in pop:
        dist[len(presenca_universo[au])] += 1
    print(f"\n  subreddits por participante, no universo:")
    for k in sorted(dist):
        print(f"    {k}: {dist[k]}")

    print(f"\n== soltando o recorte, corte do artigo fixo ==")
    abertura = []
    for ns, nc, rot in ((N_SUBS, N_COMS, "artigo: top-100 x 200"),
                        (N_SUBS, TUDO, "top-100 x todos coment."),
                        (TUDO, N_COMS, "todas submissões x 200"),
                        (TUDO, TUDO, "universo (tudo)")):
        s, _p = recorte(subs, coms, autor_por_id, ns, nc)
        q = qualificados(s)
        nn = len(q)
        mm = sum(1 for ss in q.values() if len(ss) > 1)
        pp = (100 * mm / nn) if nn else 0.0
        print(f"  {rot:<24} {nn:>7,} particip., {mm:>5,} multi = {pp:>5.1f}%")
        abertura.append({"recorte": rot, "participantes": nn, "multi": mm, "pct": round(pp, 2)})

    with open(SAIDA, "w", encoding="utf-8") as fh:
        json.dump({
            "fonte": "snapshot_buntain.sqlite (43.479 submissões + 1.015.247 "
                     "comentários, 13 subreddits, jul/2013)",
            "artigo": {"participantes": 279, "subreddits": 10, "multi": 7,
                       "pct_multi": 2.5},
            "reconstrucao_do_recorte": {
                "participantes": n, "subreddits_vivos": vivos,
                "qualificado_em_mais_de_uma_rede": {"n": a, "pct": round(100*a/n, 2)},
                "presente_em_mais_de_um_sub_no_recorte": {"n": b, "pct": round(100*b/n, 2)},
                "presente_em_mais_de_um_sub_no_universo": {"n": c, "pct": round(100*c/n, 2)},
                "subreddits_por_participante_no_universo": {str(k): dist[k] for k in sorted(dist)},
            },
            "abertura_do_recorte_com_corte_do_artigo": abertura,
        }, fh, ensure_ascii=False, indent=1)
    print(f"\njson: {os.path.abspath(SAIDA)}")


if __name__ == "__main__":
    main()
