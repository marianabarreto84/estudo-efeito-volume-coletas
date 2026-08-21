"""
Fase 2 / eixo A — Replica o ponto original da rede: modularidade sobre o grafo
de retweets do snapshot (busca 178), como o paper fez no Gephi (Louvain).

Checa:
  AV1 — duas comunidades dominantes, cada uma ~2/5 dos posts; juntas ~78%.
  AV4 — top-10 autores mais retuitados concentram ~15,7% de todos os RTs.

Decisões registradas (ver FASE2 doc):
  - Grafo NIVEL-AUTOR (retuitador -> autor_original), pois tweet_referenciado_id
    veio nulo na re-coleta; e o que a modularidade do paper agrupa sao usuarios.
  - Sem filtro de idioma (o paper rodou a rede no corpus todo — Tabela 1).
  - Arestas agregadas com peso = numero de RTs entre o par; grafo nao-direcionado
    (a modularidade classica do Gephi ignora direcao).
  - Louvain do igraph (community_multilevel), RNG do python com seed fixa;
    3 replicas (seeds 42/43/44) + NMI par-a-par para estabilidade.
  - "Posts" de um autor = originais dele + RTs feitos por ele (posts totais =
    6.554.705, como a Tabela 1 do paper, que fala em tweets AND retweets).

Saidas:
  - stdout (numeros com contexto);
  - data/repl/vacinas2022/fase2_rede.json (numeros-chave, rastreabilidade);
  - tabela `comunidades_autores` no snapshot (autor, comunidade da run seed 42)
    para reuso no eixo B.

Uso: PYTHONIOENCODING=utf-8 python -u analise/rede_modularidade.py
"""
import json
import pathlib
import random
import sqlite3
import sys
import time

import igraph as ig

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
OUT_JSON = RAIZ / "data/repl/vacinas2022/fase2_rede.json"

SEEDS = (42, 43, 44)
TOTAL_POSTS_ESPERADO = 6_554_705


def log(msg):
    print(msg, flush=True)


def main():
    t0 = time.time()
    db = sqlite3.connect(SNAP)
    cur = db.cursor()

    # ---------- 1. arestas agregadas (retuitador -> autor_original) ----------
    log("== 1. Agregando arestas de RT (par retuitador -> autor original) ==")
    arestas = cur.execute("""
        SELECT autor, autor_original, count(*) AS w
        FROM rt_arestas
        WHERE autor IS NOT NULL AND autor_original IS NOT NULL
        GROUP BY 1, 2;""").fetchall()
    log(f"   {len(arestas):,} pares distintos (de 4.507.889 RTs)")

    # ---------- 2. posts por autor (originais + RTs feitos) ----------
    log("== 2. Posts por autor (originais + RTs feitos) ==")
    posts = {}
    for autor, n in cur.execute("SELECT autor, count(*) FROM originais GROUP BY 1"):
        posts[autor] = posts.get(autor, 0) + n
    for autor, n in cur.execute("SELECT autor, count(*) FROM rt_arestas GROUP BY 1"):
        posts[autor] = posts.get(autor, 0) + n
    total_posts = sum(posts.values())
    log(f"   {len(posts):,} autores; {total_posts:,} posts "
        f"(esperado {TOTAL_POSTS_ESPERADO:,})")

    # ---------- 3. grafo ----------
    log("== 3. Montando grafo nao-direcionado ponderado ==")
    nomes = sorted({a for a, b, w in arestas} | {b for a, b, w in arestas})
    idx = {n: i for i, n in enumerate(nomes)}
    g = ig.Graph(
        n=len(nomes),
        edges=[(idx[a], idx[b]) for a, b, w in arestas],
        edge_attrs={"weight": [w for a, b, w in arestas]},
        directed=False,
    )
    g.simplify(combine_edges={"weight": "sum"})  # colapsa A<->B
    log(f"   {g.vcount():,} nos, {g.ecount():,} arestas (apos simplify)")

    # ---------- 4. Louvain com seeds fixas ----------
    log("== 4. Louvain (igraph community_multilevel), 3 seeds ==")
    particoes = {}
    for seed in SEEDS:
        random.seed(seed)
        ig.set_random_number_generator(random)
        t = time.time()
        part = g.community_multilevel(weights="weight")
        particoes[seed] = part
        log(f"   seed {seed}: {len(part)} comunidades, "
            f"modularidade={part.modularity:.4f} ({time.time()-t:.0f}s)")

    log("   Estabilidade (NMI par-a-par):")
    nmis = {}
    for i, s1 in enumerate(SEEDS):
        for s2 in SEEDS[i + 1:]:
            nmi = ig.compare_communities(particoes[s1], particoes[s2], method="nmi")
            nmis[f"{s1}x{s2}"] = round(nmi, 4)
            log(f"     seed {s1} x seed {s2}: NMI={nmi:.4f}")

    # ---------- 5. AV1 — cobertura das 2 maiores comunidades (por POSTS) ----------
    log("== 5. AV1 — tamanho das comunidades (referencia da run: seed 42) ==")
    part = particoes[42]
    membro = {nomes[v]: c for v, c in enumerate(part.membership)}
    posts_com = {}
    for autor, n in posts.items():
        c = membro.get(autor)          # autores sem aresta de RT ficam fora do grafo
        posts_com[c] = posts_com.get(c, 0) + n
    fora = posts_com.pop(None, 0)

    rank = sorted(posts_com.items(), key=lambda kv: -kv[1])
    log(f"   posts de autores fora do grafo (sem RT dado/recebido): {fora:,} "
        f"({100*fora/total_posts:.1f}%)")
    top5 = []
    for c, n in rank[:5]:
        pct = 100 * n / total_posts
        n_autores = sum(1 for v in part.membership if v == c)
        top5.append({"comunidade": c, "posts": n, "pct_posts": round(pct, 1),
                     "autores": n_autores})
        log(f"   com {c:>5}: {n:>10,} posts ({pct:5.1f}%)  {n_autores:,} autores")
    cob2 = 100 * (rank[0][1] + rank[1][1]) / total_posts
    log(f"   >>> AV1: 2 maiores juntas = {cob2:.1f}% dos posts "
        f"(paper: ~2/5 + ~2/5 = 78%)")

    # ---------- 6. AV4 — concentracao do top-10 ----------
    log("== 6. AV4 — top-10 autores mais retuitados ==")
    top_rt = cur.execute("""
        SELECT autor_original, count(*) AS rts
        FROM rt_arestas GROUP BY 1 ORDER BY 2 DESC LIMIT 10;""").fetchall()
    total_rts = cur.execute("SELECT count(*) FROM rt_arestas").fetchone()[0]
    soma10 = sum(r for _, r in top_rt)
    log(f"   total de RTs no periodo: {total_rts:,}")
    top10 = []
    for autor, rts in top_rt:
        c = membro.get(autor)
        top10.append({"autor": autor, "rts_recebidos": rts, "comunidade": c})
        log(f"   {autor:<22} {rts:>9,} RTs  com={c}")
    pct10 = 100 * soma10 / total_rts
    log(f"   >>> AV4: top-10 = {pct10:.1f}% de todos os RTs (paper: 15,7%)")

    # ---------- 7. persistencia ----------
    log("== 7. Gravando comunidades_autores no snapshot + JSON ==")
    cur.execute("DROP TABLE IF EXISTS comunidades_autores")
    cur.execute("""CREATE TABLE comunidades_autores (
                       autor TEXT PRIMARY KEY, comunidade INTEGER)""")
    cur.executemany("INSERT OR REPLACE INTO comunidades_autores VALUES (?, ?)",
                    [(nomes[v], c) for v, c in enumerate(part.membership)])
    db.commit()

    resultado = {
        "script": "analise/rede_modularidade.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "grafo": {"nos": g.vcount(), "arestas": g.ecount(),
                  "pares_rt": len(arestas)},
        "posts": {"total": total_posts, "fora_do_grafo": fora},
        "louvain": {
            "seeds": list(SEEDS),
            "n_comunidades": {s: len(p) for s, p in particoes.items()},
            "modularidade": {s: round(p.modularity, 4) for s, p in particoes.items()},
            "nmi": nmis,
        },
        "AV1": {"top5_comunidades_por_posts": top5,
                "cobertura_2_maiores_pct": round(cob2, 1),
                "paper": "duas comunidades ~2/5 cada; juntas 78%"},
        "AV4": {"top10": top10, "total_rts": total_rts,
                "pct_top10": round(pct10, 1), "paper": "15,7%"},
    }
    OUT_JSON.write_text(json.dumps(resultado, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    db.close()
    log(f"\n✅ Fase 2 / eixo A concluida em {(time.time()-t0)/60:.1f} min "
        f"→ {OUT_JSON.name}")


if __name__ == "__main__":
    main()
