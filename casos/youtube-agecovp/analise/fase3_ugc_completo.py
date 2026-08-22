"""
Fase 3 (definitiva) — P1 medido sobre TODOS os canais, e nao so os do gabarito.

Por que esta versao existe
--------------------------
`fase3_no_tema.py` respondia "o filtro do artigo remove conteudo de usuario?"
cruzando os nossos canais com o `channels.csv` dos autores. Um canal so esta nesse
CSV se sobreviveu ao filtro DELES — logo o lado descartado era representado por uma
minoria nao aleatoria, e a estimativa oscilava com o tamanho da coleta:

    coleta parcial (50/85):  +7,9 p.p.  (P1 confirma)
    coleta completa (85/85): -3,2 p.p.  (P1 nao confirma)

Aqui a mesma pergunta e refeita sobre `canais`, a tabela que `pipeline/coleta_canais.py`
preencheu pela API para os 2.165 canais do instantaneo — cobertura de 100% nos dois
lados do filtro. O script reporta as duas bases lado a lado, com IC de 95%, para que a
diferenca entre elas seja ela propria um resultado.

Uso: PYTHONIOENCODING=utf-8 python -u analise/fase3_ugc_completo.py
Saida: stdout + data/repl/agecovp2020/fase3_ugc_completo.json
"""
import collections
import csv
import json
import math
import pathlib
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.regras import no_tema, eh_ugc, LIMIAR_INSCRITOS

csv.field_size_limit(10 ** 8)
D = pathlib.Path("data/repl/agecovp2020")
G = D / "gabarito_zenodo"
OUT = D / "fase3_ugc_completo.json"
Z = 1.959964


def log(m):
    print(m, flush=True)


def ic_diferenca(k1, n1, k2, n2):
    """IC95% de (p2 - p1), Wald (n grande nos dois lados)."""
    p1, p2 = k1 / n1, k2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p2 - p1
    return 100 * d, 100 * (d - Z * se), 100 * (d + Z * se)


def primeira_cat(s):
    for x in (s or "").split(","):
        x = x.strip().strip("[]\"' ")
        if x:
            return x.split("/")[-1]
    return None


def main():
    cx = sqlite3.connect(D / "snapshot_agecovp.sqlite")
    cx.row_factory = sqlite3.Row
    vids = [dict(r) for r in cx.execute(
        "SELECT video_id, channel_id, title, description, passa_filtro FROM videos")]
    canais = {r["channel_id"]: dict(r) for r in cx.execute("SELECT * FROM canais")}
    feitos = cx.execute("SELECT COUNT(*) FROM log_busca WHERE done=1").fetchone()[0]
    cx.close()

    tema = [v for v in vids if no_tema(v["title"], v["description"])]
    passa = [v for v in tema if v["passa_filtro"]]
    barra = [v for v in tema if not v["passa_filtro"]]
    log("combinacoes: %d/85 | videos %d | no tema %d (passa %d, descartados %d)"
        % (feitos, len(vids), len(tema), len(passa), len(barra)))

    # --- base A: gabarito dos autores (o que a versao anterior usava) ---
    gab = {}
    with open(G / "channels.csv", encoding="utf-8", errors="replace", newline="") as f:
        for r in csv.DictReader(f):
            gab[r["Channel_id"]] = r

    def conta_gab(grupo):
        u = t = 0
        for v in grupo:
            r = gab.get(v["channel_id"])
            if not r:
                continue
            t += 1
            u += 1 if eh_ugc(r.get("Title"), r.get("Subscriptions")) else 0
        return u, t

    # --- base B: API, todos os canais ---
    def conta_api(grupo, limiar=LIMIAR_INSCRITOS):
        u = t = 0
        for v in grupo:
            r = canais.get(v["channel_id"])
            if not r:
                continue
            t += 1
            u += 1 if eh_ugc(r.get("title"), r.get("inscritos"), limiar) else 0
        return u, t

    res = {"combinacoes": feitos, "n_videos": len(vids), "n_tema": len(tema),
           "limiar_inscritos": LIMIAR_INSCRITOS}
    log("")
    log("== P1: o filtro descarta conteudo de usuario? (videos NO TEMA) ==")
    log("  %-24s %13s %13s %11s %-20s"
        % ("base de canais", "passa", "descarta", "delta p.p.", "IC95% do delta"))
    for nome, fn in (("gabarito dos autores", conta_gab), ("API (todos os canais)", conta_api)):
        up, tp = fn(passa)
        ub, tb = fn(barra)
        if not (tp and tb):
            continue
        d, lo, hi = ic_diferenca(up, tp, ub, tb)
        sig = "  <- significativo" if not (lo <= 0 <= hi) else ""
        log("  %-24s %5.1f%% (%4d) %5.1f%% (%4d) %+10.1f  [%+.1f, %+.1f]%s"
            % (nome, 100 * up / tp, tp, 100 * ub / tb, tb, d, lo, hi, sig))
        res[nome] = {"passa_pct": round(100 * up / tp, 1), "n_passa": tp,
                     "descartado_pct": round(100 * ub / tb, 1), "n_descartado": tb,
                     "delta_pp": round(d, 1), "ic95": [round(lo, 1), round(hi, 1)],
                     "significativo": not (lo <= 0 <= hi)}

    # --- cobertura: a origem do vies ---
    cob_p = sum(1 for v in passa if v["channel_id"] in gab) / len(passa)
    cob_b = sum(1 for v in barra if v["channel_id"] in gab) / len(barra)
    log("")
    log("== por que as duas bases divergem: cobertura do gabarito ==")
    log("  videos que PASSAM o filtro    : %.1f%% tem canal no gabarito" % (100 * cob_p))
    log("  videos DESCARTADOS pelo filtro: %.1f%% tem canal no gabarito" % (100 * cob_b))
    log("  -> o gabarito representa os dois lados de forma desigual (razao %.2fx)"
        % (cob_p / cob_b if cob_b else float("nan")))
    res["cobertura_gabarito"] = {"passa": round(100 * cob_p, 1),
                                 "descartado": round(100 * cob_b, 1)}

    # --- sensibilidade ao limiar (a regra e declarada, nao calibrada) ---
    log("")
    log("== sensibilidade: o sinal depende do limiar de inscritos? ==")
    log("  %-12s %10s %10s %11s %-20s"
        % ("limiar", "passa", "descarta", "delta p.p.", "IC95%"))
    sens = {}
    for lim in (1000, 5000, 10000, 50000, 100000):
        up, tp = conta_api(passa, lim)
        ub, tb = conta_api(barra, lim)
        d, lo, hi = ic_diferenca(up, tp, ub, tb)
        log("  %-12s %9.1f%% %9.1f%% %+10.1f  [%+.1f, %+.1f]"
            % ("{:,}".format(lim), 100 * up / tp, 100 * ub / tb, d, lo, hi))
        sens[lim] = {"delta_pp": round(d, 1), "ic95": [round(lo, 1), round(hi, 1)]}
    res["sensibilidade_limiar"] = sens

    # --- inscritos medianos, que nao dependem de limiar nenhum ---
    def mediana(grupo):
        xs = sorted(canais[v["channel_id"]]["inscritos"] for v in grupo
                    if v["channel_id"] in canais
                    and canais[v["channel_id"]]["inscritos"] is not None)
        return xs[len(xs) // 2] if xs else None
    mp, mb = mediana(passa), mediana(barra)
    log("")
    log("== sem limiar nenhum: inscritos medianos do canal ==")
    log("  passam o filtro : %s" % "{:,}".format(mp))
    log("  DESCARTADOS     : %s" % "{:,}".format(mb))
    res["inscritos_mediana"] = {"passa": mp, "descartado": mb}

    # --- onde o efeito de selecao REALMENTE esta ---
    # P1 pergunta pelo filtro de palavra-chave. Medido acima, ele nao explica a
    # composicao do corpus. Esta secao pergunta pelo funil INTEIRO: entre os videos
    # no tema que as mesmas buscas devolvem, os que acabaram no corpus publicado sao
    # diferentes dos que nao acabaram?
    dentro = [v for v in tema if v["channel_id"] in gab]
    fora_c = [v for v in tema if v["channel_id"] not in gab]

    def perfil_api(grupo):
        u = t = 0
        ins = []
        for v in grupo:
            r = canais.get(v["channel_id"])
            if not r:
                continue
            t += 1
            u += 1 if eh_ugc(r.get("title"), r.get("inscritos")) else 0
            if r.get("inscritos") is not None:
                ins.append(r["inscritos"])
        ins.sort()
        return u, t, (ins[len(ins) // 2] if ins else None)

    ud, td, md = perfil_api(dentro)
    uf, tf, mf = perfil_api(fora_c)
    d, lo, hi = ic_diferenca(ud, td, uf, tf)
    log("")
    log("== o funil INTEIRO: quem entrou no corpus publicado x quem nao entrou ==")
    log("  %-34s %8s %8s %14s" % ("", "UGC", "n", "inscr. mediano"))
    log("  %-34s %7.1f%% %8d %14s"
        % ("canal ESTA no corpus do artigo", 100 * ud / td, td, "{:,}".format(md)))
    log("  %-34s %7.1f%% %8d %14s"
        % ("canal NAO esta no corpus", 100 * uf / tf, tf, "{:,}".format(mf)))
    log("  -> diferenca %+.1f p.p.  IC95%% [%+.1f, %+.1f]" % (d, lo, hi))
    res["corpus_x_nao_corpus"] = {
        "no_corpus": {"ugc_pct": round(100 * ud / td, 1), "n": td, "inscritos_mediana": md},
        "fora_corpus": {"ugc_pct": round(100 * uf / tf, 1), "n": tf, "inscritos_mediana": mf},
        "delta_pp": round(d, 1), "ic95": [round(lo, 1), round(hi, 1)]}

    log("")
    log("  e o filtro de palavra-chave DENTRO de cada estrato:")
    res["filtro_por_estrato"] = {}
    for rot, g in (("canal no corpus", dentro), ("canal fora do corpus", fora_c)):
        pa = [v for v in g if v["passa_filtro"]]
        ba = [v for v in g if not v["passa_filtro"]]
        if not (pa and ba):
            continue
        x, nx, _ = perfil_api(pa)
        y, ny, _ = perfil_api(ba)
        dd = 100 * y / ny - 100 * x / nx
        log("    %-22s passa %5.1f%% (n=%4d) | descarta %5.1f%% (n=%4d) | delta %+.1f"
            % (rot, 100 * x / nx, nx, 100 * y / ny, ny, dd))
        res["filtro_por_estrato"][rot] = {"passa_pct": round(100 * x / nx, 1),
                                          "descartado_pct": round(100 * y / ny, 1),
                                          "delta_pp": round(dd, 1)}

    # --- categorias, base completa ---
    def cats(grupo):
        c = collections.Counter()
        for v in grupo:
            r = canais.get(v["channel_id"])
            k = primeira_cat(r["topic_categories"]) if r else None
            if k:
                c[k] += 1
        tot = sum(c.values())
        return {k: round(100 * n / tot, 1) for k, n in c.most_common(8)}, tot
    cp, ntp = cats(passa)
    cb, ntb = cats(barra)
    todas = sorted(set(cp) | set(cb), key=lambda k: -(cp.get(k, 0) + cb.get(k, 0)))
    log("")
    log("== categorias de canal (API, 1a categoria) ==")
    log("  %-26s %8s %11s %8s" % ("categoria", "passa", "descartado", "delta"))
    for k in todas[:8]:
        log("  %-26s %7.1f%% %10.1f%% %+7.1f"
            % (k, cp.get(k, 0), cb.get(k, 0), cb.get(k, 0) - cp.get(k, 0)))
    res["categorias_api"] = {"passa": cp, "descartado": cb,
                             "n_passa": ntp, "n_descartado": ntb}

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    log("")
    log("escrito em %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
