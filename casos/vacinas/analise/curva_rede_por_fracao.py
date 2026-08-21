"""
Fase 3 / eixo A — curva A(volume) da REDE: AV1 por fracao de N.

A pergunta (do plano, Fase 3): "AV1 converge a que fracao?"
Simula ter coletado MENOS: sorteia uma fracao f da coleta (originais E eventos de
RT), reconstroi o grafo, roda Louvain, atribui lado pela regra do AV1 e mede.

O que se mede em cada ponto
---------------------------
  - razao pro/anti dos posts  <- a quantidade de que AV1b depende
  - cobertura (pro+anti)/total
  - modularidade e n de comunidades
  - NMI contra a particao do corpus cheio (nos em comum) — estabilidade estrutural

Decisoes registradas
--------------------
  - Sorteia originais e RTs na MESMA fracao: e o analogo honesto de "o estudo
    coletou f vezes menos", nao de "perdeu so retweets".
  - Lado por maioria das 599 sementes publicadas, min. 1 semente (mesma regra de
    `atribui_lado_comunidades.py`); comunidade sem semente -> nao identificada.
  - Base de posts: AMPLA (todos os originais sorteados + RTs sorteados). A base
    "convencao do paper" nao se aplica aqui, porque o ponto e a curva, e a razao
    pro/anti — a quantidade que interessa — e invariante a base (ver FASE2 §AV1).
  - Louvain com seed = 1000 + replica, para as replicas diferirem de fato.

⚠ COBERTURA DE REPLICAS ABAIXO DO PROTOCOLO
   O protocolo da dissertacao pede >= 30 replicas bootstrap por ponto. Aqui rodam
   5 replicas ate f=0,25, 3 em f=0,50/0,75 e 1 em f=1,0 (o corpus cheio, onde nao ha
   sorteio — so a variacao do Louvain). Motivo: cada replica exige um Louvain sobre
   ate 3,3 M arestas. As bandas reportadas sao min-max das replicas, NAO IC bootstrap,
   e estao declaradas como tal no doc de resultados. Aumentar para 30 e trabalho de
   maquina, nao de metodo.

Saidas: stdout + data/repl/vacinas2022/curva_rede.json
Uso: PYTHONIOENCODING=utf-8 python -u analise/curva_rede_por_fracao.py
"""
import array
import collections
import json
import pathlib
import random
import sqlite3
import time

import igraph as ig
import openpyxl

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
SUPL = RAIZ / "data/repl/vacinas2022/suplementar_rotulos.xlsx"
OUT_JSON = RAIZ / "data/repl/vacinas2022/curva_rede.json"

REPLICAS = {0.01: 5, 0.025: 5, 0.05: 5, 0.10: 5, 0.25: 5,
            0.50: 3, 0.75: 3, 1.0: 1}
FRACOES = tuple(sorted(REPLICAS))


def log(msg):
    print(msg, flush=True)


def norm(a):
    return a.strip().lstrip("@").lower() if a else None


def main():
    t0 = time.time()
    db = sqlite3.connect(SNAP)
    cur = db.cursor()

    # ---------- 1. sementes ----------
    log("== 1. Sementes publicadas ==")
    lado_semente = {}
    for r in list(openpyxl.load_workbook(SUPL, read_only=True, data_only=True)
                  ["Authors"].iter_rows(values_only=True))[1:]:
        pro, anti, autor = r[0], r[1], r[2]
        a = norm(autor)
        if not a:
            continue
        if pro == 1 and anti != 1:
            lado_semente[a] = "pro"
        elif anti == 1 and pro != 1:
            lado_semente[a] = "anti"
    log(f"   {len(lado_semente)} sementes com lado")

    # ---------- 2. carga em memoria (ids inteiros) ----------
    log("== 2. Carregando arestas e originais ==")
    ids, nomes = {}, []

    def idx(a):
        a = norm(a)
        if a not in ids:
            ids[a] = len(nomes)
            nomes.append(a)
        return ids[a]

    src, dst = array.array("i"), array.array("i")
    for a, b in cur.execute("SELECT autor, autor_original FROM rt_arestas "
                            "WHERE autor IS NOT NULL AND autor_original IS NOT NULL"):
        src.append(idx(a))
        dst.append(idx(b))
    log(f"   {len(src):,} eventos de RT")

    orig = array.array("i")
    for (a,) in cur.execute("SELECT autor FROM originais WHERE autor IS NOT NULL"):
        orig.append(idx(a))
    log(f"   {len(orig):,} originais · {len(nomes):,} autores distintos")

    # particao do corpus cheio (referencia para o NMI)
    com_cheio = {}
    for a, c in cur.execute("SELECT autor, comunidade FROM comunidades_autores"):
        a = norm(a)
        if a in ids:
            com_cheio[ids[a]] = c
    log(f"   particao de referencia: {len(com_cheio):,} autores")
    db.close()

    sementes_id = {ids[a]: lado for a, lado in lado_semente.items() if a in ids}
    log(f"   {len(sementes_id)}/{len(lado_semente)} sementes localizadas nos ids")

    # ---------- 3. a curva ----------
    log("== 3. Curva A(volume) ==")
    log(f"   {'fracao':>7} {'rep':>4} {'arestas':>10} {'mod':>6} {'n_com':>7} "
        f"{'razao':>7} {'cobert':>8} {'NMI':>6} {'s':>5}")
    pontos = []
    for f in FRACOES:
        reps = []
        for r in range(REPLICAS[f]):
            t = time.time()
            rnd = random.Random(1000 + r)

            # --- sorteio da coleta ---
            if f >= 1.0:
                sel_e = range(len(src))
                orig_sel = orig
            else:
                sel_e = [i for i in range(len(src)) if rnd.random() < f]
                orig_sel = [o for o in orig if rnd.random() < f]

            pares = collections.Counter()
            for i in sel_e:
                u, v = src[i], dst[i]
                pares[(u, v) if u < v else (v, u)] += 1

            posts = collections.Counter()
            for i in sel_e:
                posts[src[i]] += 1
            for o in orig_sel:
                posts[o] += 1
            total = sum(posts.values())

            # --- grafo + Louvain ---
            locais = sorted({u for u, _ in pares} | {v for _, v in pares})
            pos = {n: k for k, n in enumerate(locais)}
            g = ig.Graph(n=len(locais),
                         edges=[(pos[u], pos[v]) for u, v in pares],
                         edge_attrs={"weight": list(pares.values())},
                         directed=False)
            random.seed(1000 + r)
            ig.set_random_number_generator(random)
            part = g.community_multilevel(weights="weight")
            memb = {locais[k]: c for k, c in enumerate(part.membership)}

            # --- lado por comunidade ---
            votos = collections.defaultdict(collections.Counter)
            for a, lado in sementes_id.items():
                c = memb.get(a)
                if c is not None:
                    votos[c][lado] += 1
            lado_com = {}
            for c, v in votos.items():
                o = v.most_common()
                if len(o) > 1 and o[0][1] == o[1][1]:
                    continue
                lado_com[c] = o[0][0]

            agg = collections.Counter()
            for a, n in posts.items():
                agg[lado_com.get(memb.get(a), "nao_ident")] += n
            pro, anti = agg["pro"], agg["anti"]
            razao = pro / anti if anti else None
            cobert = 100 * (pro + anti) / total if total else 0

            # --- NMI contra o corpus cheio (nos em comum) ---
            comuns = [a for a in memb if a in com_cheio]
            nmi = ig.compare_communities([memb[a] for a in comuns],
                                         [com_cheio[a] for a in comuns],
                                         method="nmi") if comuns else None

            reps.append({"replica": r, "arestas": g.ecount(), "nos": g.vcount(),
                         "posts": total, "modularidade": round(part.modularity, 4),
                         "n_comunidades": len(part),
                         "razao_pro_anti": round(razao, 3) if razao else None,
                         "cobertura_pct": round(cobert, 1),
                         "nmi_vs_cheio": round(nmi, 4) if nmi else None,
                         "com_com_lado": len(lado_com)})
            log(f"   {f:>7.3f} {r:>4} {g.ecount():>10,} "
                f"{part.modularity:>6.3f} {len(part):>7,} "
                f"{(razao or 0):>7.2f} {cobert:>7.1f}% {(nmi or 0):>6.3f} "
                f"{time.time()-t:>5.0f}")

        razoes = [x["razao_pro_anti"] for x in reps if x["razao_pro_anti"]]
        coberts = [x["cobertura_pct"] for x in reps]
        nmis = [x["nmi_vs_cheio"] for x in reps if x["nmi_vs_cheio"]]
        pontos.append({
            "fracao": f, "n_replicas": len(reps),
            "posts_medio": round(sum(x["posts"] for x in reps) / len(reps)),
            "razao_pro_anti": {"min": min(razoes), "max": max(razoes),
                               "media": round(sum(razoes) / len(razoes), 3)},
            "cobertura_pct": {"min": min(coberts), "max": max(coberts),
                              "media": round(sum(coberts) / len(coberts), 1)},
            "nmi_vs_cheio": {"min": min(nmis), "max": max(nmis),
                             "media": round(sum(nmis) / len(nmis), 4)} if nmis else None,
            "replicas": reps,
        })

    # ---------- 4. resumo ----------
    log("== 4. Resumo da curva ==")
    log(f"   {'fracao':>7} {'posts':>11} {'razao (min-max)':>20} "
        f"{'cobertura':>12} {'NMI':>8}")
    for p in pontos:
        rz = p["razao_pro_anti"]
        cb = p["cobertura_pct"]
        nm = p["nmi_vs_cheio"]
        log(f"   {p['fracao']:>7.3f} {p['posts_medio']:>11,} "
            f"{rz['media']:>8.2f} ({rz['min']:.2f}-{rz['max']:.2f}) "
            f"{cb['media']:>10.1f}% {(nm['media'] if nm else 0):>8.3f}")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/curva_rede_por_fracao.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "aviso_replicas": ("5 replicas ate f=0,25; 3 em 0,50/0,75; 1 em 1,0. "
                           "ABAIXO das >=30 do protocolo (custo de Louvain). "
                           "Bandas sao min-max, nao IC bootstrap."),
        "regra_lado": "maioria das 599 sementes publicadas, min. 1",
        "pontos": pontos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {(time.time()-t0)/60:.1f} min -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
