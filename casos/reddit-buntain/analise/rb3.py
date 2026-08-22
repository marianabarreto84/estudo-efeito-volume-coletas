#!/usr/bin/env python3
"""RB3 — participação multi-comunidade (caso Buntain).

Afirmação do alvo (Buntain & Golbeck 2014, §5.3): apenas **~3%** dos usuários
(7 de 279) participam de mais de uma comunidade. Aqui medimos a mesma coisa no
**universo** (todos os usuários que postaram/comentaram nos 13 subreddits em
jul/2013, sem o corte de grau nem o top-100/top-200 do paper).

Predição pré-registrada: os ~3% **sobem muito** — a sub-coleta escondia a atividade
cruzada por construção. Determinístico; não precisa de gabarito humano.

Uso: python analise/rb3.py

Grava tambem `data/repl/buntain2013/curva_rb3.json`, consumido pela figura
da curva por limiar em escrita/dissertacao/figuras/gerar_figuras.py.
"""
import sqlite3, os, sys, json
from collections import defaultdict

DB = os.path.join(os.path.dirname(__file__), "..", "data", "repl", "buntain2013",
                  "snapshot_buntain.sqlite")
BOTS = {"[deleted]", "AutoModerator", None, ""}
SAIDA = os.path.join(os.path.dirname(__file__), "..", "data", "repl",
                     "buntain2013", "curva_rb3.json")
LIMIARES = (1, 2, 5, 10, 20, 50)


def author_subs(cx):
    """author -> set de subreddits (dos 13) onde tem submission OU comentário."""
    d = defaultdict(set)
    for tbl in ("submissions", "comments"):
        for a, s in cx.execute(f"SELECT author, subreddit FROM {tbl}"):
            if a in BOTS:
                continue
            d[a].add(s)
    return d


def author_activity(cx):
    """author -> nº total de mensagens (submissions+comentários)."""
    act = defaultdict(int)
    for tbl in ("submissions", "comments"):
        for (a,) in cx.execute(f"SELECT author FROM {tbl}"):
            if a not in BOTS:
                act[a] += 1
    return act


def main():
    if not os.path.exists(DB):
        sys.exit(f"snapshot ainda não existe: {DB} — rode pipeline/collect.py antes")
    cx = sqlite3.connect(DB)
    subs_by_author = author_subs(cx)
    act = author_activity(cx)

    n_users = len(subs_by_author)
    multi = sum(1 for a, ss in subs_by_author.items() if len(ss) > 1)
    print(f"== RB3 · universo (todos os usuários, sem corte) ==")
    print(f"usuários únicos (não-bot): {n_users:,}")
    print(f"em >1 dos 13 subreddits:   {multi:,}  ({100*multi/n_users:.1f}%)")
    print(f"  [alvo do paper: 3% — 7 de 279]")

    # sensibilidade ao limiar de atividade (o paper cortava usuários pouco ativos)
    print(f"\n== RB3 por limiar de atividade (≥k mensagens) ==")
    print(f"{'k':>4} {'usuários':>10} {'multi':>8} {'% multi':>8}")
    curva = []
    for k in LIMIARES:
        elig = [a for a in subs_by_author if act[a] >= k]
        if not elig:
            continue
        m = sum(1 for a in elig if len(subs_by_author[a]) > 1)
        print(f"{k:>4} {len(elig):>10,} {m:>8,} {100*m/len(elig):>7.1f}%")
        curva.append({"k": k, "usuarios": len(elig), "multi": m,
                      "pct_multi": round(100 * m / len(elig), 2)})

    # distribuição do nº de subreddits por usuário
    print(f"\n== nº de subreddits por usuário ==")
    dist = defaultdict(int)
    for ss in subs_by_author.values():
        dist[len(ss)] += 1
    for k in sorted(dist):
        print(f"  {k} subreddit(s): {dist[k]:,}")

    with open(SAIDA, "w", encoding="utf-8") as fh:
        json.dump({
            "fonte": "snapshot_buntain.sqlite (43.479 submissions + 1.015.247 "
                     "comentários, 13 subreddits, jul/2013)",
            "paper": {"usuarios": 279, "multi": 7, "pct_multi": 3.0},
            "curva_por_limiar": curva,
            "subreddits_por_usuario": {str(k): dist[k] for k in sorted(dist)},
        }, fh, ensure_ascii=False, indent=1)
    print(f"\njson: {os.path.abspath(SAIDA)}")


if __name__ == "__main__":
    main()
