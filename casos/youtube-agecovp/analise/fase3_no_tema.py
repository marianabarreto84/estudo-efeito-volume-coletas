"""
Fase 3 (corrigida) — o efeito do filtro **entre os vídeos que estão no tema**.

Por que esta versao existe
--------------------------
A [Fase 3 parcial](../data/repl/agecovp2020/FASE3_efeito_filtro.md) mostrou que o
conjunto descartado pelo filtro traz conteudo genuinamente fora do tema (Sport,
Baseball). Comparar os dois lados sem isolar isso mede RUIDO, nao vies — e derrubou
a predicao P4 por um motivo espurio.

Aqui a comparacao e refeita **so entre videos que passam no teste de tema**
(`core.regras.no_tema`, validado em 99,9% do corpus do artigo). A pergunta fica:

    entre videos que SAO sobre idosos na pandemia, o filtro do artigo
    seleciona um subconjunto diferente do que descarta?

Se sim, o filtro enviesa. Se nao, ele so limpa ruido — e a critica cai.

Uso: PYTHONIOENCODING=utf-8 python -u analise/fase3_no_tema.py
Saida: stdout + data/repl/agecovp2020/fase3_no_tema.json
"""
import collections
import csv
import json
import pathlib
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.regras import no_tema, eh_ugc, LIMIAR_INSCRITOS

csv.field_size_limit(10 ** 8)
D = pathlib.Path("data/repl/agecovp2020")
G = D / "gabarito_zenodo"
OUT = D / "fase3_no_tema.json"


def log(m):
    print(m, flush=True)


def le(nome):
    with open(G / nome, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def cats(r):
    out = []
    for x in (r.get("TopicCategories") or "").split(","):
        x = x.strip().strip("[]'\" ")
        if x:
            out.append(x.split("/")[-1])
    return out


def main():
    cx = sqlite3.connect(D / "snapshot_agecovp.sqlite")
    cx.row_factory = sqlite3.Row
    vids = [dict(r) for r in cx.execute(
        "SELECT video_id, channel_id, channel_title, published_at, title, description,"
        " passa_filtro FROM videos")]
    feitos = cx.execute("SELECT COUNT(*) FROM log_busca WHERE done=1").fetchone()[0]
    cx.close()

    for v in vids:
        v["no_tema"] = no_tema(v["title"], v["description"])

    n = len(vids)
    tema = [v for v in vids if v["no_tema"]]
    fora = [v for v in vids if not v["no_tema"]]
    log("coleta parcial: %d de 85 combinacoes | %d videos" % (feitos, n))
    log("  no tema:  %5d (%.1f%%)" % (len(tema), 100 * len(tema) / n))
    log("  fora:     %5d (%.1f%%)" % (len(fora), 100 * len(fora) / n))

    # ---- 1. o filtro descarta quanto, DENTRO do tema? ----
    t_passa = [v for v in tema if v["passa_filtro"]]
    t_barra = [v for v in tema if not v["passa_filtro"]]
    f_passa = [v for v in fora if v["passa_filtro"]]
    log("\n== 1. o que o filtro faz, separado por tema ==")
    log("  %-22s %8s %8s %9s" % ("", "passa", "descarta", "descarte"))
    log("  %-22s %8d %8d %8.1f%%" % ("NO TEMA", len(t_passa), len(t_barra),
                                     100 * len(t_barra) / len(tema) if tema else 0))
    log("  %-22s %8d %8d %8.1f%%" % ("fora do tema", len(f_passa), len(fora) - len(f_passa),
                                     100 * (len(fora) - len(f_passa)) / len(fora) if fora else 0))
    log("\n  -> dos %d videos descartados pelo filtro, **%d (%.1f%%) ESTAO no tema**"
        % (len(t_barra) + (len(fora) - len(f_passa)), len(t_barra),
           100 * len(t_barra) / (len(t_barra) + len(fora) - len(f_passa))))
    log("     (o resto e ruido que o filtro remove com razao)")

    res = {"combinacoes": feitos, "n": n, "no_tema": len(tema), "fora_tema": len(fora),
           "descartados_no_tema": len(t_barra),
           "descartados_fora_tema": len(fora) - len(f_passa)}

    # ---- 2. dentro do tema: os dois lados sao diferentes? ----
    ch = {r["Channel_id"]: r for r in le("channels.csv")}

    def perfil(grupo, rotulo):
        cat = collections.Counter()
        ugc = inst = 0
        casados = 0
        for v in grupo:
            r = ch.get(v["channel_id"])
            if not r:
                continue
            casados += 1
            cs = cats(r)
            if cs:
                cat[cs[0]] += 1
            if eh_ugc(r.get("Title"), r.get("Subscriptions"), LIMIAR_INSCRITOS):
                ugc += 1
            else:
                inst += 1
        tot = ugc + inst
        return {"n_casados": casados, "ugc_pct": round(100 * ugc / tot, 1) if tot else None,
                "categorias": {k: round(100 * v / sum(cat.values()), 1)
                               for k, v in cat.most_common(6)} if cat else {}}

    pa = perfil(t_passa, "passa")
    ba = perfil(t_barra, "descartado")
    log("\n== 2. DENTRO do tema, os dois lados diferem? ==")
    log("  canais reconhecidos: %d (passa) / %d (descartado)" % (pa["n_casados"], ba["n_casados"]))
    if pa["ugc_pct"] is not None and ba["ugc_pct"] is not None:
        log("\n  UGC (regra declarada: marcador de imprensa ou >=%s inscritos)"
            % "{:,}".format(LIMIAR_INSCRITOS))
        log("    passam o filtro : %.1f%% UGC" % pa["ugc_pct"])
        log("    DESCARTADOS     : %.1f%% UGC" % ba["ugc_pct"])
        d = ba["ugc_pct"] - pa["ugc_pct"]
        log("    -> diferenca: **%+.1f p.p.**  | P1 (o filtro remove UGC): %s"
            % (d, "CONFIRMA" if d > 0 else "NAO confirma"))
        res["UGC"] = {"passa": pa["ugc_pct"], "descartado": ba["ugc_pct"], "delta_pp": round(d, 1)}
    log("\n  categorias de canal (1a categoria):")
    todas = sorted(set(pa["categorias"]) | set(ba["categorias"]),
                   key=lambda k: -(pa["categorias"].get(k, 0) + ba["categorias"].get(k, 0)))
    log("    %-24s %8s %11s %8s" % ("categoria", "passa", "descartado", "delta"))
    for k in todas[:8]:
        p, b = pa["categorias"].get(k, 0), ba["categorias"].get(k, 0)
        log("    %-24s %7.1f%% %10.1f%% %+7.1f" % (k, p, b, b - p))
    res["categorias"] = {"passa": pa["categorias"], "descartado": ba["categorias"]}

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    log("\nescrito em %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
