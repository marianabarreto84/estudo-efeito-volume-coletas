"""
Fase 3 (caso AGECovP) — o efeito do filtro de palavra-chave. PARCIAL e OFFLINE.

O que se mede
-------------
O artigo mantem so os videos em que a palavra-chave da busca reaparece no titulo ou
na descricao. Nossa coleta guarda TUDO e marca o filtro numa coluna
(`passa_filtro`), entao os dois lados da comparacao saem do mesmo snapshot.

Tres perguntas, todas respondiveis sem gastar cota:

  Q1  Quanto o filtro descarta? (o artigo: 52,1% na busca; 99,0% nos sugeridos)
  Q2  Os videos que o filtro descarta sao DIFERENTES dos que ele mantem?
      Medido pelo cruzamento com `channels.csv` do gabarito, que traz a categoria
      de cada canal — testa a predicao P4 (a fatia "Society", dos canais
      institucionais, cai quando se solta o filtro).
  Q3  Nossa reconstrucao alcanca o corpus do artigo? Medido pela sobreposicao de
      video_id com `videos.csv` do gabarito, separada por lado do filtro. Se os
      videos que PASSAM o filtro sobrepoem muito mais, a reconstrucao e fiel e a
      diferenca observada e do filtro, nao do procedimento.

⚠ PARCIAL: roda sobre as combinacoes de busca ja coletadas (a cota do dia acabou
antes das 85). Os percentuais sao estaveis, as contagens absolutas nao.

Uso: PYTHONIOENCODING=utf-8 python -u analise/fase3_efeito_filtro.py
Saida: stdout + data/repl/agecovp2020/fase3_efeito_filtro.json
"""
import collections
import csv
import json
import pathlib
import sqlite3
import sys

csv.field_size_limit(10 ** 8)

D = pathlib.Path("data/repl/agecovp2020")
DB = D / "snapshot_agecovp.sqlite"
G = D / "gabarito_zenodo"
OUT = D / "fase3_efeito_filtro.json"


def log(m):
    print(m, flush=True)


def le_csv(nome):
    with open(G / nome, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def cats(r):
    t = r.get("TopicCategories") or ""
    out = []
    for x in t.split(","):
        x = x.strip().strip("[]'\" ")
        if x:
            out.append(x.split("/")[-1])
    return out


def main():
    cx = sqlite3.connect(DB)
    cx.row_factory = sqlite3.Row
    vids = [dict(r) for r in cx.execute(
        "SELECT video_id, channel_id, channel_title, published_at, passa_filtro FROM videos")]
    feitos = cx.execute("SELECT COUNT(*) FROM log_busca WHERE done=1").fetchone()[0]
    cx.close()
    n = len(vids)
    passa = [v for v in vids if v["passa_filtro"]]
    barra = [v for v in vids if not v["passa_filtro"]]
    res = {"combinacoes_concluidas": feitos, "de": 85, "n_videos": n}

    # ---- Q1 ----
    log("== Q1: quanto o filtro descarta? (parcial: %d de 85 combinacoes)" % feitos)
    log("  coletados        %5d" % n)
    log("  passam o filtro  %5d  (%.1f%%)" % (len(passa), 100 * len(passa) / n))
    log("  DESCARTADOS      %5d  (**%.1f%%**)  | o artigo declara 52,1%% na busca"
        % (len(barra), 100 * len(barra) / n))
    res["Q1"] = {"passa": len(passa), "descarta": len(barra),
                 "pct_descartado": round(100 * len(barra) / n, 1), "alvo_artigo": 52.1}

    # ---- Q2: composicao por categoria de canal (join com o gabarito) ----
    ch = {r["Channel_id"]: r for r in le_csv("channels.csv")}
    log("\n== Q2: os descartados sao diferentes? (categoria do canal, via gabarito)")

    def perfil(grupo):
        c = collections.Counter()
        casados = 0
        for v in grupo:
            r = ch.get(v["channel_id"])
            if not r:
                continue
            cs = cats(r)
            if cs:
                casados += 1
                c[cs[0]] += 1        # 1a categoria: a convencao que replica (Fase 2 §1)
        tot = sum(c.values())
        return casados, {k: round(100 * v / tot, 1) for k, v in c.most_common(6)} if tot else {}

    cp, dp = perfil(passa)
    cb, db = perfil(barra)
    log("  canais reconhecidos no gabarito: %d dos que passam, %d dos descartados" % (cp, cb))
    if cp and cb:
        log("  %-26s %10s %12s %8s" % ("categoria", "passa", "descartado", "delta"))
        for k in sorted(set(dp) | set(db), key=lambda x: -(dp.get(x, 0) + db.get(x, 0))):
            log("  %-26s %9.1f%% %11.1f%% %+7.1f" % (k, dp.get(k, 0), db.get(k, 0),
                                                     db.get(k, 0) - dp.get(k, 0)))
        soc = db.get("Society", 0) - dp.get("Society", 0)
        log("\n  -> P4 (a fatia 'Society' cai ao soltar o filtro): %s  (delta %+.1f p.p.)"
            % ("CONFIRMA" if soc < 0 else "NAO confirma", soc))
    else:
        log("  (poucos canais em comum para comparar)")
    res["Q2"] = {"perfil_passa": dp, "perfil_descartado": db,
                 "canais_casados_passa": cp, "canais_casados_descartado": cb}

    # ---- Q3: sobreposicao com o corpus do artigo ----
    ids_art = {r[list(r)[0]] for r in le_csv("videos.csv")}   # 1a coluna = Video_id (com BOM)
    log("\n== Q3: nossa reconstrucao alcanca o corpus do artigo? (%d videos no gabarito)"
        % len(ids_art))
    for nome, grupo in (("passam o filtro", passa), ("descartados", barra)):
        inter = sum(1 for v in grupo if v["video_id"] in ids_art)
        log("  %-18s %5d videos | %4d tambem no artigo (%.1f%%)"
            % (nome, len(grupo), inter, 100 * inter / len(grupo) if grupo else 0))
        res.setdefault("Q3", {})[nome] = {"n": len(grupo), "no_artigo": inter,
                                          "pct": round(100 * inter / len(grupo), 1) if grupo else 0}
    tot_inter = sum(1 for v in vids if v["video_id"] in ids_art)
    log("  total: %d dos nossos %d estao no corpus do artigo (%.1f%%)"
        % (tot_inter, n, 100 * tot_inter / n))
    log("  e cobrimos %.1f%% do corpus dele" % (100 * tot_inter / len(ids_art)))
    res["Q3"]["total_intersecao"] = tot_inter
    res["Q3"]["cobertura_do_artigo_pct"] = round(100 * tot_inter / len(ids_art), 1)

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    log("\nescrito em %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
