"""
Fase 3 (eixo midia) — curva A(volume) do H2, que e afirmacao sobre UM DIA.

H2 do artigo: "a midia horizontal (MH) chega a RIVALIZAR com a vertical (MV) em ao
menos um dia" — o artigo aponta 23/out (capa da Veja).

Por que este script existe separado da curva do H1
--------------------------------------------------
H1 e uma proporcao agregada da semana; H2 e uma comparacao DENTRO de um dia. O
universo por dia vai de 2.908 a 7.246 tweets, e a amostra do artigo e de 100/dia.
Subamostrar a semana inteira nao responde H2.

O que se mede, por dia
----------------------
  - universo do dia: MV%, MH% e a diferenca MV-MH (sobre TODOS os tweets do dia);
  - a amostra do ARTIGO reconstruida (100 do horario de pico) — o mesmo recorte de
    `analisa_midia.py`/`stats_midia.py`;
  - subamostras ALEATORIAS de n crescente, com B replicas: banda de MV-MH e, o que
    interessa, a **taxa de rivalidade** = fracao de replicas em que MH >= MV, isto
    e, com que frequencia um pesquisador VERIA H2 sustentada naquele dia.

A pergunta decisiva: a rivalidade que o artigo relata em 23/out aparece em amostras
aleatorias do mesmo tamanho? Se nao aparece em nenhuma, H2 e artefato do recorte por
horario de pico, e nao um efeito que mais volume corrigiria.

Uso: PYTHONIOENCODING=utf-8 python -u analise/curva_h2_por_dia.py
Saidas: stdout + data/repl/compos2014/curva_h2.json
"""
import json
import pathlib
import random
import sqlite3
import sys
import time
from collections import Counter
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.resolve_midia import carrega_cache, classe_do_primeiro_link
from core.extrai_links import links_efetivos

D = pathlib.Path("data/repl/compos2014")
OUT_JSON = D / "curva_h2.json"
CACHE = carrega_cache(D / "expand_cache.sqlite")

B = 300
TAMANHOS = (25, 50, 100, 200, 400, 800)
# mesmo recorte de pico usado em analisa_midia.py / stats_midia.py
PICO = {date(2014, 10, 19): 21, date(2014, 10, 20): 21, date(2014, 10, 21): 21,
        date(2014, 10, 22): 14, date(2014, 10, 23): 21, date(2014, 10, 24): 16,
        date(2014, 10, 25): 13}


def log(m):
    print(m, flush=True)


def cls(links_json, texto):
    c, _ = classe_do_primeiro_link(links_efetivos(links_json, texto), CACHE)
    return c


def pcts(classes):
    n = len(classes)
    if not n:
        return 0.0, 0.0
    c = Counter(classes)
    return 100 * c["MV"] / n, 100 * c["MH"] / n


def main():
    t0 = time.time()
    con = sqlite3.connect(D / "snapshot_hashtag.sqlite")
    con.row_factory = sqlite3.Row

    log("== Carregando e classificando (caminho canonico) ==")
    por_dia = {}
    for r in con.execute("SELECT links, texto, data_brt FROM tweets "
                         "WHERE substr(data_brt,1,10) BETWEEN '2014-10-19' "
                         "AND '2014-10-25'"):
        por_dia.setdefault(r["data_brt"][:10], []).append(cls(r["links"], r["texto"]))
    log(f"   {sum(len(v) for v in por_dia.values()):,} tweets em {len(por_dia)} dias")

    # amostra do artigo (100 do horario de pico), por dia
    amostra_paper = {}
    for dia, h in PICO.items():
        ini, fim = f"{dia.isoformat()}T{h:02d}:00:00", f"{dia.isoformat()}T23:59:59"
        rows = con.execute("SELECT links, texto FROM tweets WHERE data_brt>=? "
                           "AND data_brt<=? ORDER BY data_brt LIMIT 100",
                           (ini, fim)).fetchall()
        amostra_paper[dia.isoformat()] = [cls(r["links"], r["texto"]) for r in rows]
    con.close()

    log("\n== Por dia: universo x amostra do artigo ==")
    log(f"   {'dia':<12} {'n_dia':>7} | {'universo MV%':>12} {'MH%':>6} {'gap':>7} "
        f"| {'paper MV%':>10} {'MH%':>6} {'gap':>7} {'rival?':>7}")
    dias = []
    for dia in sorted(por_dia):
        uni = por_dia[dia]
        mv_u, mh_u = pcts(uni)
        pa = amostra_paper.get(dia, [])
        mv_p, mh_p = pcts(pa)
        rival_paper = mh_p >= mv_p
        dias.append({"dia": dia, "n_dia": len(uni),
                     "universo": {"mv_pct": round(mv_u, 1), "mh_pct": round(mh_u, 1),
                                  "gap_mv_mh": round(mv_u - mh_u, 1)},
                     "amostra_paper": {"n": len(pa), "mv_pct": round(mv_p, 1),
                                       "mh_pct": round(mh_p, 1),
                                       "gap_mv_mh": round(mv_p - mh_p, 1),
                                       "rivalidade": rival_paper}})
        log(f"   {dia:<12} {len(uni):>7,} | {mv_u:>11.1f}% {mh_u:>5.1f}% "
            f"{mv_u-mh_u:>6.1f} | {mv_p:>9.1f}% {mh_p:>5.1f}% {mv_p-mh_p:>6.1f} "
            f"{('SIM' if rival_paper else 'nao'):>7}")

    log("\n== Taxa de rivalidade (fracao de replicas com MH >= MV) ==")
    log(f"   {'dia':<12} " + " ".join(f"{('n='+str(n)):>8}" for n in TAMANHOS))
    for d in dias:
        dia = d["dia"]
        uni = por_dia[dia]
        idx = list(range(len(uni)))
        taxas = {}
        celulas = []
        for n in TAMANHOS:
            if n > len(uni):
                celulas.append(f"{'—':>8}")
                continue
            riv = 0
            gaps = []
            for b in range(B):
                sel = random.Random(20_000 + b).sample(idx, n)
                mv, mh = pcts([uni[i] for i in sel])
                gaps.append(mv - mh)
                if mh >= mv:
                    riv += 1
            taxas[n] = {"taxa_rivalidade_pct": round(100 * riv / B, 1),
                        "gap_medio": round(sum(gaps) / len(gaps), 1),
                        "gap_min": round(min(gaps), 1)}
            celulas.append(f"{100*riv/B:>7.1f}%")
        d["por_n"] = taxas
        log(f"   {dia:<12} " + " ".join(celulas))

    log("\n== Leitura ==")
    d23 = next(d for d in dias if d["dia"] == "2014-10-23")
    log(f"   23/out — o dia que o artigo aponta como exceção:")
    log(f"     universo: MV {d23['universo']['mv_pct']}% x MH "
        f"{d23['universo']['mh_pct']}% (gap {d23['universo']['gap_mv_mh']} p.p.)")
    log(f"     amostra do artigo (pico, n={d23['amostra_paper']['n']}): "
        f"MV {d23['amostra_paper']['mv_pct']}% x MH {d23['amostra_paper']['mh_pct']}%")
    t100 = d23["por_n"].get(100)
    if t100:
        log(f"     em n=100 ALEATORIO: rivalidade em {t100['taxa_rivalidade_pct']}% "
            f"das replicas; gap medio {t100['gap_medio']} p.p., "
            f"pior caso {t100['gap_min']} p.p.")
    algum = [d["dia"] for d in dias if d["por_n"].get(100, {}).get(
        "taxa_rivalidade_pct", 0) > 5]
    log(f"   Dias em que n=100 aleatorio produz rivalidade em >5% das replicas: "
        f"{algum or 'NENHUM'}")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/curva_h2_por_dia.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "B_replicas": B,
        "definicao_rivalidade": "MH% >= MV% no dia",
        "dias": dias,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
