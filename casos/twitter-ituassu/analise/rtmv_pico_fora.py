"""RTMV dentro x fora do horario de pico, no universo da janela 19-25/out/2014.

Pedido da banca (Profa. Ana Carolina, nov/2026): tratar o horario de pico, que o artigo
usou como criterio de amostragem, como ATRIBUTO de cada tweet do universo, e comparar
direto a proporcao dentro e fora dele.

PREDICAO (registrada antes de rodar, 09/nov/2026): se a explicacao do Cap. 4 vale
("nos horarios de maior trafego circula sobretudo retuite de imprensa; fora deles cresce
o conteudo sem link"), o RTMV na hora de pico e MAIOR que fora dela e a NDA e MENOR.

Pico = a hora em que o artigo comecou a amostrar em cada dia (dicionario PICO de
stats_midia.py), de h:00 a h:59. Fora = as demais horas do mesmo dia.
Roda sobre o snapshot congelado (sem rede). Saida: data/repl/compos2014/rtmv_pico_fora.json
"""
import json
import math
import sqlite3
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.resolve_midia import carrega_cache, classe_do_primeiro_link  # noqa: E402
from core.extrai_links import links_efetivos  # noqa: E402

D = Path("data/repl/compos2014")
CACHE = carrega_cache(D / "expand_cache.sqlite")
PICO = {date(2014, 10, 19): 21, date(2014, 10, 20): 21, date(2014, 10, 21): 21,
        date(2014, 10, 22): 14, date(2014, 10, 23): 21, date(2014, 10, 24): 16,
        date(2014, 10, 25): 13}


def cls(links_json, texto):
    c, _ = classe_do_primeiro_link(links_efetivos(links_json, texto), CACHE)
    return c


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (c - m), 100 * (c + m)


def dif(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = 100 * (p1 - p2)
    return d, d - 196 * se, d + 196 * se


con = sqlite3.connect(D / "snapshot_hashtag.sqlite")
con.row_factory = sqlite3.Row
rows = con.execute("SELECT links, texto, status_retweet, data_brt FROM tweets "
                   "WHERE substr(data_brt,1,10) BETWEEN '2014-10-19' AND '2014-10-25'").fetchall()
con.close()

grupos = {"pico": [], "fora": []}
por_dia = {}
for r in rows:
    d = date.fromisoformat(r["data_brt"][:10])
    h = int(r["data_brt"][11:13])
    g = "pico" if h == PICO[d] else "fora"
    c = cls(r["links"], r["texto"])
    rt = bool(r["status_retweet"]) and str(r["status_retweet"]).lower() not in ("0", "false", "f")
    item = {"rtmv": rt and c == "MV", "nda": c == "NDA", "mv": c == "MV", "mh": c == "MH"}
    grupos[g].append(item)
    por_dia.setdefault(str(d), {"pico": [], "fora": []})[g].append(item)


def resumo(itens):
    n = len(itens)
    out = {"n": n}
    for k in ("rtmv", "nda"):
        x = sum(i[k] for i in itens)
        lo, hi = wilson(x, n)
        out[k] = {"k": x, "pct": round(100 * x / n, 1), "ic95": [round(lo, 1), round(hi, 1)]}
    mv, mh = sum(i["mv"] for i in itens), sum(i["mh"] for i in itens)
    out["mv_entre_midia_pct"] = round(100 * mv / (mv + mh), 1)
    return out


res = {"pico": resumo(grupos["pico"]), "fora": resumo(grupos["fora"])}
for k in ("rtmv", "nda"):
    d, lo, hi = dif(res["pico"][k]["k"], res["pico"]["n"], res["fora"][k]["k"], res["fora"]["n"])
    res["pico_menos_fora_" + k] = {"pp": round(d, 1), "ic95": [round(lo, 1), round(hi, 1)]}
res["por_dia"] = {d: {"hora_pico": PICO[date.fromisoformat(d)],
                      "pico": resumo(v["pico"]), "fora": resumo(v["fora"])}
                  for d, v in sorted(por_dia.items())}
res["predicao"] = "RTMV pico > fora e NDA pico < fora"
res["predicao_confirmada"] = (res["pico_menos_fora_rtmv"]["ic95"][0] > 0
                              and res["pico_menos_fora_nda"]["ic95"][1] < 0)

(D / "rtmv_pico_fora.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "por_dia"}, ensure_ascii=False, indent=1))
for d, v in res["por_dia"].items():
    print(d, v["hora_pico"], "RTMV pico", v["pico"]["rtmv"]["pct"], "n", v["pico"]["n"],
          "| fora", v["fora"]["rtmv"]["pct"], "n", v["fora"]["n"])
