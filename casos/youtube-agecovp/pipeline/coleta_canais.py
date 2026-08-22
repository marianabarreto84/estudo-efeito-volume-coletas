"""
Coleta os metadados de TODOS os canais do instantaneo (nao so os do gabarito).

Por que existe
--------------
A Fase 3 mediu "o filtro do artigo remove conteudo de usuario?" cruzando os nossos
canais com o `channels.csv` publicado pelos autores. Isso e circular: um canal so
esta naquele CSV se sobreviveu ao filtro DELES. O lado descartado ficava
representado por uma minoria nao aleatoria de canais, e a estimativa era instavel —
na coleta parcial deu +7,9 p.p. e na completa, -3,2 p.p.

Aqui buscamos inscritos e categorias de todo canal que aparece no instantaneo, pela
propria API (channels.list, 1 unidade por 50 ids). Assim os dois lados do filtro
sao medidos pela mesma fonte e com a mesma cobertura.

Uso: PYTHONIOENCODING=utf-8 python -u pipeline/coleta_canais.py [--dry-run]
"""
import argparse
import pathlib
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.youtube_api import YouTube, CotaEsgotada

D = pathlib.Path("data/repl/agecovp2020")
DB = D / "snapshot_agecovp.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS canais(
  channel_id TEXT PRIMARY KEY, title TEXT, published_at TEXT, country TEXT,
  inscritos INTEGER, inscritos_ocultos INTEGER, videos INTEGER, views INTEGER,
  topic_categories TEXT, description TEXT);
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cx = sqlite3.connect(DB)
    cx.executescript(SCHEMA)
    faltam = [r[0] for r in cx.execute(
        "SELECT DISTINCT v.channel_id FROM videos v"
        " LEFT JOIN canais c ON c.channel_id = v.channel_id"
        " WHERE v.channel_id IS NOT NULL AND c.channel_id IS NULL")]
    custo = -(-len(faltam) // 50)
    print("canais sem metadados: %d | custo: %d unidades" % (len(faltam), custo))
    if a.dry_run:
        return 0
    if not faltam:
        print("nada a fazer")
        return 0

    yt = YouTube()
    print("cota gasta hoje: %d | resta %d\n" % (yt.gasto_hoje(), yt.resta()))
    gravados = 0
    for i in range(0, len(faltam), 50):
        lote = faltam[i:i + 50]
        try:
            itens = yt.canais(lote)
        except CotaEsgotada as e:
            print("\n[COTA] %s" % e)
            break
        linhas = []
        for it in itens:
            sn = it.get("snippet") or {}
            st = it.get("statistics") or {}
            td = it.get("topicDetails") or {}
            linhas.append((
                it.get("id"), sn.get("title"), sn.get("publishedAt"), sn.get("country"),
                int(st["subscriberCount"]) if st.get("subscriberCount") else None,
                1 if st.get("hiddenSubscriberCount") else 0,
                int(st["videoCount"]) if st.get("videoCount") else None,
                int(st["viewCount"]) if st.get("viewCount") else None,
                ",".join(td.get("topicCategories") or []), sn.get("description")))
        cx.executemany("INSERT OR IGNORE INTO canais VALUES(%s)" % ",".join("?" * 10), linhas)
        cx.commit()
        gravados += len(linhas)
        print("  lote %3d: +%2d canais (total %4d | cota resta %d)"
              % (i // 50 + 1, len(linhas), gravados, yt.resta()))

    tot = cx.execute("SELECT COUNT(*) FROM canais").fetchone()[0]
    vivos = cx.execute("SELECT COUNT(*) FROM canais WHERE inscritos IS NOT NULL").fetchone()[0]
    print("\nCANAIS: %d gravados (%d com inscritos publicos)" % (tot, vivos))
    print("nao devolvidos pela API (apagados/suspensos): %d" % (len(faltam) - gravados))
    cx.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
