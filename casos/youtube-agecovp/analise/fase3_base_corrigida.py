"""
Fase 3: as contas do capitulo que ainda nao tinham versao na base com a descricao
completa (description_full).

Por que existe
--------------
Nov/2026, versao pos-defesa da dissertacao: o capitulo do YouTube migra para a base
corrigida (1.833 videos no tema, ver FASE3_sentimento_videos.md §2), que e a dos slides
da defesa. fase3_data_publicacao.py ja da o filtro, o funil e o residuo nessa base;
faltavam (a) a mediana de inscritos dos dois lados do filtro e dos dois lados do funil e
(b) o efeito do filtro dentro de cada estrato do funil (canal dentro x fora do corpus
publicado).

Controle: as mesmas contas sobre a descricao truncada tem de reproduzir os numeros do
texto entregue (28 mil x 61,5 mil; 199 mil x 1.070; -3,5 e -11,1 p.p.).

Uso: PYTHONIOENCODING=utf-8 python -u analise/fase3_base_corrigida.py
Saida: stdout + data/repl/agecovp2020/fase3_base_corrigida.json
"""
import csv
import json
import pathlib
import sqlite3
import statistics
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.regras import no_tema, eh_ugc, LIMIAR_INSCRITOS

csv.field_size_limit(10 ** 8)
D = pathlib.Path("data/repl/agecovp2020")
G = D / "gabarito_zenodo"
OUT = D / "fase3_base_corrigida.json"


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def main():
    t = json.loads((D / "termos_agecovp.json").read_text(encoding="utf-8"))
    lista = [norm(x) for x in t["filtro_palavras_chave"]["termos"]]

    def filtro_corrigido(tit, desc, termo):
        campo = norm(tit) + " " + norm(desc)
        if all(w in campo for w in norm(termo).split()):
            return 1
        return 1 if any(k in campo for k in lista) else 0

    cx = sqlite3.connect(D / "snapshot_agecovp.sqlite")
    cx.row_factory = sqlite3.Row
    vids = [dict(r) for r in cx.execute(
        "SELECT video_id, channel_id, title, description, description_full,"
        " termo_busca, passa_filtro FROM videos")]
    canais = {r["channel_id"]: dict(r) for r in cx.execute("SELECT * FROM canais")}
    cx.close()
    gab_ch = set()
    with open(G / "channels.csv", encoding="utf-8", errors="replace", newline="") as f:
        for r in csv.DictReader(f):
            gab_ch.add(r["Channel_id"])

    def ugc(v):
        r = canais.get(v["channel_id"])
        if not r:
            return None
        return 1 if eh_ugc(r.get("title"), r.get("inscritos"), LIMIAR_INSCRITOS) else 0

    def mediana_inscritos(grupo):
        xs = [canais[v["channel_id"]]["inscritos"] for v in grupo
              if v["channel_id"] in canais and canais[v["channel_id"]].get("inscritos") is not None]
        return statistics.median(xs) if xs else None

    def pct_ugc(grupo):
        us = [ugc(v) for v in grupo]
        us = [u for u in us if u is not None]
        return 100 * sum(us) / len(us), len(us)

    res = {"limiar_inscritos": LIMIAR_INSCRITOS}
    for conv, campo, refaz in (("truncada (texto entregue)", "description", False),
                               ("corrigida (descricao completa)", "description_full", True)):
        tema = [v for v in vids if no_tema(v["title"], v[campo])]

        def aprova(v):
            return (filtro_corrigido(v["title"], v[campo], v["termo_busca"])
                    if refaz else v["passa_filtro"])
        p = [v for v in tema if aprova(v)]
        b = [v for v in tema if not aprova(v)]
        dentro = [v for v in tema if v["channel_id"] in gab_ch]
        fora = [v for v in tema if v["channel_id"] not in gab_ch]
        estratos = {}
        for nome, grupo in (("canal no corpus", dentro), ("canal fora do corpus", fora)):
            gp = [v for v in grupo if aprova(v)]
            gb = [v for v in grupo if not aprova(v)]
            (up, np_), (ub, nb) = pct_ugc(gp), pct_ugc(gb)
            estratos[nome] = {"ugc_passa_pct": round(up, 1), "n_passa": np_,
                              "ugc_descarta_pct": round(ub, 1), "n_descarta": nb,
                              "delta_pp": round(ub - up, 1)}
        res[conv] = {
            "n_tema": len(tema),
            "mediana_inscritos": {"aprovados": mediana_inscritos(p),
                                  "descartados": mediana_inscritos(b),
                                  "canal_no_corpus": mediana_inscritos(dentro),
                                  "canal_fora_do_corpus": mediana_inscritos(fora)},
            "filtro_dentro_de_cada_estrato": estratos,
        }
        print(conv)
        print(json.dumps(res[conv], ensure_ascii=False, indent=1))

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n-> %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
