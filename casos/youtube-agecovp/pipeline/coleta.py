"""
Fase 1 (caso AGECovP) — recoleta das 85 combinacoes de busca, SEM o filtro do artigo.

Decisao central de desenho
--------------------------
O artigo aplica um filtro de regex (a palavra-chave tem de reaparecer no titulo ou na
descricao) que descarta **52% dos resultados da busca** e **99% dos videos sugeridos**.
Nos coletamos **tudo o que a busca devolve** e gravamos o resultado do filtro como uma
COLUNA (`passa_filtro`), em vez de descartar. Assim o mesmo snapshot serve aos dois
lados da comparacao — sub-coletado (o do artigo) e expandido — sem recoletar nada.

Janela: a mesma do gabarito (videos de 2020-01-01 a 2022-09-01).

Escopo reduzido, declarado: **2 paginas por combinacao** (100 videos), nao as 12 do
artigo. Motivo em FASE0 §8 — a cota e de 10.000 un./dia e a comparacao filtro x
sem-filtro nao depende da profundidade. Resumivel: rode de novo quando a cota virar.

Uso:
  python -u pipeline/coleta.py --dry-run
  python -u pipeline/coleta.py --paginas 2
  python -u pipeline/coleta.py --comentarios      # 2a etapa, barata (1 un./100 coment.)
"""
import argparse
import json
import pathlib
import re
import sqlite3
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.youtube_api import YouTube, CotaEsgotada

D = pathlib.Path("data/repl/agecovp2020")
DB = D / "snapshot_agecovp.sqlite"
TERMOS = D / "termos_agecovp.json"
DEPOIS, ANTES = "2020-01-01", "2022-09-01"

SCHEMA = """
CREATE TABLE IF NOT EXISTS videos(
  video_id TEXT PRIMARY KEY, channel_id TEXT, channel_title TEXT, published_at TEXT,
  title TEXT, description TEXT, termo_busca TEXT, passa_filtro INTEGER,
  views INTEGER, likes INTEGER, comments INTEGER, duration TEXT, categoria TEXT);
CREATE TABLE IF NOT EXISTS comentarios(
  comment_id TEXT PRIMARY KEY, video_id TEXT, author TEXT, published_at TEXT,
  like_count INTEGER, texto TEXT);
CREATE TABLE IF NOT EXISTS log_busca(
  termo TEXT PRIMARY KEY, n_encontrados INTEGER, done INTEGER);
CREATE TABLE IF NOT EXISTS log_comentarios(
  video_id TEXT PRIMARY KEY, n INTEGER, done INTEGER);
CREATE INDEX IF NOT EXISTS ix_v_filtro ON videos(passa_filtro);
CREATE INDEX IF NOT EXISTS ix_c_video ON comentarios(video_id);
"""


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def carrega_termos():
    t = json.loads(TERMOS.read_text(encoding="utf-8"))
    idosos = t["busca"]["older_adults_N17"]
    covid = sorted(set(t["busca"]["covid_N5_hipotese_de_trabalho"]))
    filtro = [norm(x) for x in t["filtro_palavras_chave"]["termos"]]
    combos = ["%s %s" % (a, b) for a in idosos for b in covid]
    return combos, filtro


def passa_filtro(titulo, descricao, termo, lista_filtro):
    """
    Regra do artigo: a palavra-chave da busca precisa aparecer no titulo OU na
    descricao. Aplicamos a versao estrita (os termos da propria busca) e, em
    seguida, a lista ampla de palavras-chave publicada em nota de rodape.
    """
    campo = norm(titulo) + " " + norm(descricao)
    if all(p in campo for p in norm(termo).split()):
        return 1
    return 1 if any(k in campo for k in lista_filtro) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paginas", type=int, default=2)
    ap.add_argument("--comentarios", action="store_true")
    ap.add_argument("--max-videos-comentarios", type=int, default=400)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    combos, lista_filtro = carrega_termos()
    print("combinacoes de busca: %d (%d idosos x %d covid unicos)"
          % (len(combos), 17, len(combos) // 17))
    print("janela: %s a %s | paginas por combinacao: %d" % (DEPOIS, ANTES, a.paginas))
    custo = len(combos) * a.paginas * 100
    print("custo estimado da busca: %d unidades (~%.1f dias de cota)" % (custo, custo / 10000))
    if a.dry_run:
        print("\n--dry-run: nada chamado.\n exemplos: %s" % ", ".join(combos[:4]))
        return 0

    DB.parent.mkdir(parents=True, exist_ok=True)
    cx = sqlite3.connect(DB)
    cx.executescript(SCHEMA)
    yt = YouTube()
    print("cota ja gasta hoje: %d un. | resta %d\n" % (yt.gasto_hoje(), yt.resta()))

    if not a.comentarios:
        for termo in combos:
            r = cx.execute("SELECT done FROM log_busca WHERE termo=?", (termo,)).fetchone()
            if r and r[0]:
                continue
            n = 0
            try:
                for pagina in yt.busca(termo, depois=DEPOIS, antes=ANTES,
                                       max_paginas=a.paginas):
                    linhas = []
                    for it in pagina:
                        vid = (it.get("id") or {}).get("videoId")
                        sn = it.get("snippet") or {}
                        if not vid:
                            continue
                        linhas.append((vid, sn.get("channelId"), sn.get("channelTitle"),
                                       sn.get("publishedAt"), sn.get("title"),
                                       sn.get("description"), termo,
                                       passa_filtro(sn.get("title"), sn.get("description"),
                                                    termo, lista_filtro),
                                       None, None, None, None, None))
                    cx.executemany(
                        "INSERT OR IGNORE INTO videos VALUES(%s)" % ",".join("?" * 13), linhas)
                    cx.commit()
                    n += len(linhas)
            except CotaEsgotada as e:
                print("\n[COTA] %s" % e)
                cx.execute("INSERT OR REPLACE INTO log_busca VALUES(?,?,0)", (termo, n))
                cx.commit()
                break
            cx.execute("INSERT OR REPLACE INTO log_busca VALUES(?,?,1)", (termo, n))
            cx.commit()
            tot = cx.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
            print("%-34s +%3d  (total unico: %5d | cota resta %d)"
                  % (termo, n, tot, yt.resta()))
    else:
        ids = [r[0] for r in cx.execute(
            "SELECT video_id FROM videos WHERE video_id NOT IN "
            "(SELECT video_id FROM log_comentarios WHERE done=1) LIMIT ?",
            (a.max_videos_comentarios,))]
        print("coletando comentarios de %d videos" % len(ids))
        for i, vid in enumerate(ids, 1):
            n = 0
            try:
                for pagina in yt.comentarios(vid, max_paginas=3):
                    linhas = []
                    for it in pagina:
                        top = ((it.get("snippet") or {}).get("topLevelComment") or {})
                        sn = top.get("snippet") or {}
                        linhas.append((top.get("id"), vid, sn.get("authorDisplayName"),
                                       sn.get("publishedAt"), sn.get("likeCount"),
                                       sn.get("textDisplay")))
                    cx.executemany("INSERT OR IGNORE INTO comentarios VALUES(?,?,?,?,?,?)",
                                   linhas)
                    cx.commit()
                    n += len(linhas)
            except CotaEsgotada as e:
                print("\n[COTA] %s" % e)
                break
            cx.execute("INSERT OR REPLACE INTO log_comentarios VALUES(?,?,1)", (vid, n))
            cx.commit()
            if i % 25 == 0:
                print("  %d/%d videos | %d comentarios | cota resta %d"
                      % (i, len(ids), cx.execute("SELECT COUNT(*) FROM comentarios").fetchone()[0],
                         yt.resta()))

    v = cx.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
    f = cx.execute("SELECT COUNT(*) FROM videos WHERE passa_filtro=1").fetchone()[0]
    c = cx.execute("SELECT COUNT(*) FROM comentarios").fetchone()[0]
    print("\nSNAPSHOT: %d videos (%d passam o filtro = %.1f%%), %d comentarios"
          % (v, f, 100 * f / v if v else 0, c))
    print("cota gasta hoje: %d un." % yt.gasto_hoje())
    cx.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
