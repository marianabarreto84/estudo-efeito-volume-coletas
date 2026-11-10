#!/usr/bin/env python3
"""RB3 — a ESCADA do recorte: quanto mais posts, quanta interseção a mais.

Complementa `rb3_recorte_artigo.py`, que mede as duas pontas. Este levanta os
degraus intermediários, para responder à pergunta da Mariana (29/set/2026):
*coletar mais posts do que os top-100 pega mais interseção entre usuários?*

O artigo olhou os **top 100 submissions** de julho/2013 de cada subreddit e ~200
comentários de cada um. O nosso instantâneo tem **todos** os posts do mesmo mês
nos mesmos 13 subreddits. A escada solta um eixo de cada vez:

    top-100 x 200  ->  top-100 x todos  ->  todas submissões x 200  ->  tudo

e mede, em cada degrau, as DUAS leituras de "participar de mais de uma
comunidade" que o artigo mistura:

  (a) QUALIFICADO — ter >=20 arestas de saída dentro da rede de cada subreddit.
      É o que o artigo de fato conta ("279 unique users ... who had more than 20
      outgoing edges ... seven appeared in more than one subreddit community").
  (b) PRESENTE — ter postado ali. É como o artigo ENUNCIA o achado no §5.3
      ("only seven of our 279 unique users, or around 3%, were identified in
      multiple communities") e na pergunta do §1 ("whether users participate in
      multiple communities at all").

A população fica FIXA nos participantes que o recorte do artigo identifica, para
que o único eixo que varia seja o quanto se coletou.

Uso: python analise/rb3_escada_recorte.py
Requer o snapshot (não versionado); rodar na cópia de dados, em Documents/dissertacao/.
"""
import sqlite3, os, sys, json
from collections import defaultdict

from rb3_recorte_artigo import (DB, carrega, recorte, qualificados,
                                N_SUBS, N_COMS, LIMIAR, TUDO)

SAIDA = os.path.join(os.path.dirname(__file__), "..", "data", "repl",
                     "buntain2013", "rb3_escada_recorte.json")

DEGRAUS = [
    (N_SUBS, N_COMS, "top-100 x 200 (o do artigo)"),
    (N_SUBS, TUDO,   "top-100 x todos os comentarios"),
    (TUDO,   N_COMS, "TODAS as submissoes x 200"),
    (TUDO,   TUDO,   "universo (tudo)"),
]


def main():
    if not os.path.exists(DB):
        sys.exit(f"snapshot nao encontrado: {DB}")
    cx = sqlite3.connect(DB)
    subs, coms, autor_por_id, presenca_universo = carrega(cx)

    n_subs_total = sum(len(v) for v in subs.values())
    n_subs_recorte = sum(len(v[:N_SUBS]) for v in subs.values())

    # populacao FIXA: os participantes que o desenho do artigo identifica
    saida0, _ = recorte(subs, coms, autor_por_id, N_SUBS, N_COMS)
    pop = sorted(qualificados(saida0))
    n = len(pop)

    print("ARTIGO (§4.1): 279 usuarios com >20 arestas de saida em 10 de 13 subreddits;")
    print("               7 deles 'appeared in more than one subreddit community' = 2,5%\n")
    print(f"posts no recorte do artigo: {n_subs_recorte:,} de {n_subs_total:,} "
          f"({n_subs_total/n_subs_recorte:.0f}x mais no instantaneo)\n")
    print(f"populacao fixa: {n} participantes (artigo: 279)\n")
    print(f"{'degrau':<34} {'posts':>8} {'qualif.>1':>11} {'presente>1':>12}")
    print("-" * 68)

    linhas = []
    for ns, nc, rot in DEGRAUS:
        s, presenca = recorte(subs, coms, autor_por_id, ns, nc)
        q = qualificados(s)
        n_posts = sum(len(v[:ns]) for v in subs.values())
        qm = sum(1 for au in pop if len(q.get(au, ())) > 1)
        pm = sum(1 for au in pop if len(presenca.get(au, ())) > 1)
        print(f"{rot:<34} {n_posts:>8,} {qm:>5} = {100*qm/n:>4.1f}% {pm:>5} = {100*pm/n:>4.1f}%")
        linhas.append({"degrau": rot, "posts": n_posts,
                       "qualificado_em_mais_de_1": {"n": qm, "pct": round(100*qm/n, 1)},
                       "presente_em_mais_de_1": {"n": pm, "pct": round(100*pm/n, 1)}})

    # conferencia: o ultimo degrau tem de bater com a presenca no universo
    cc = sum(1 for au in pop if len(presenca_universo[au]) > 1)
    print(f"\nconferencia — presenca no universo por fora da escada: {cc} = {100*cc/n:.1f}%")

    with open(SAIDA, "w", encoding="utf-8") as fh:
        json.dump({"populacao_fixa": n, "artigo": {"participantes": 279, "multi": 7,
                                                   "pct": 2.5},
                   "posts_no_recorte": n_subs_recorte, "posts_no_universo": n_subs_total,
                   "escada": linhas, "conferencia_presenca_universo": cc}, fh,
                  ensure_ascii=False, indent=1)
    print(f"\njson: {os.path.abspath(SAIDA)}")


if __name__ == "__main__":
    main()
