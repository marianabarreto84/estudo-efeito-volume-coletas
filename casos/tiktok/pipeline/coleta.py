"""
Fase 1 (TikTok) — coleta local resumivel para snapshot SQLite congelado.

Mesmo padrao do coletor do caso reddit-buntain: um `collect_log` guarda o ponto
alcancado por (consulta, janela); reexecutar retoma de onde parou. A analise
posterior roda **sobre o snapshot**, sem rede — Fase 1 -> Fases 2-3 do protocolo.

Uso:
  python -u pipeline/coleta.py --hashtag eleicoes2026 --regiao BR \
        --inicio 20260801 --fim 20260831 --saida data/snapshot_tiktok.sqlite

  --limite-chamadas N   teto rigido de chamadas de API nesta execucao (default 200).
                        A cota e COMPARTILHADA com o coletor do eTC — ver o aviso
                        em core/tiktok_api.py. O teto existe para nao estourar a
                        cota do grupo por engano.
  --dry-run             so mostra o plano de janelas; nao chama a API.
"""
import argparse
import json
import pathlib
import sqlite3
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.tiktok_api import TikTokAPI, fatia_janela

SCHEMA = """
CREATE TABLE IF NOT EXISTS videos(
  id TEXT PRIMARY KEY, username TEXT, video_description TEXT, create_time INTEGER,
  region_code TEXT, share_count INTEGER, view_count INTEGER, like_count INTEGER,
  comment_count INTEGER, music_id TEXT, hashtag_names TEXT, effect_ids TEXT,
  playlist_id TEXT, voice_to_text TEXT, consulta TEXT, coletado_em INTEGER);
CREATE TABLE IF NOT EXISTS collect_log(
  consulta TEXT, inicio TEXT, fim TEXT, n INTEGER, done INTEGER,
  PRIMARY KEY(consulta, inicio, fim));
CREATE INDEX IF NOT EXISTS ix_v_user ON videos(username);
CREATE INDEX IF NOT EXISTS ix_v_time ON videos(create_time);
"""

COLS = ["id", "username", "video_description", "create_time", "region_code",
        "share_count", "view_count", "like_count", "comment_count", "music_id",
        "hashtag_names", "effect_ids", "playlist_id", "voice_to_text"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hashtag", nargs="*", default=[])
    ap.add_argument("--palavra", nargs="*", default=[])
    ap.add_argument("--regiao", default=None)
    ap.add_argument("--inicio", required=True)
    ap.add_argument("--fim", required=True)
    ap.add_argument("--saida", default="data/snapshot_tiktok.sqlite")
    ap.add_argument("--limite-chamadas", type=int, default=200)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    consulta = json.dumps({"hashtag": sorted(a.hashtag), "palavra": sorted(a.palavra),
                           "regiao": a.regiao}, ensure_ascii=False, sort_keys=True)
    janelas = fatia_janela(a.inicio, a.fim)
    print("consulta: %s" % consulta)
    print("janela %s..%s -> %d pedaco(s) de ate 30 dias:" % (a.inicio, a.fim, len(janelas)))
    for i, f in janelas:
        print("   %s .. %s" % (i, f))
    print("teto desta execucao: %d chamadas de API" % a.limite_chamadas)
    if a.dry_run:
        print("\n--dry-run: nada foi chamado.")
        return 0

    saida = pathlib.Path(a.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    cx = sqlite3.connect(saida)
    cx.executescript(SCHEMA)

    api = TikTokAPI()
    ins = ("INSERT OR IGNORE INTO videos(%s,consulta,coletado_em) VALUES(%s)"
           % (",".join(COLS), ",".join(["?"] * (len(COLS) + 2))))
    total = 0
    for ini, fim in janelas:
        r = cx.execute("SELECT done FROM collect_log WHERE consulta=? AND inicio=? AND fim=?",
                       (consulta, ini, fim)).fetchone()
        if r and r[0]:
            print("[pulando] %s..%s ja completo" % (ini, fim))
            continue
        n = 0
        for lote in api.busca_videos(inicio=ini, fim=fim, hashtags=a.hashtag or None,
                                     palavras=a.palavra or None, regiao=a.regiao):
            agora = int(time.time())
            cx.executemany(ins, [[v.get(c) if not isinstance(v.get(c), (list, dict))
                                  else json.dumps(v.get(c), ensure_ascii=False)
                                  for c in COLS] + [consulta, agora] for v in lote])
            cx.commit()
            n += len(lote)
            cx.execute("INSERT OR REPLACE INTO collect_log VALUES(?,?,?,?,0)",
                       (consulta, ini, fim, n))
            cx.commit()
            if api.chamadas >= a.limite_chamadas:
                print("\n[TETO] %d chamadas atingidas — parando. Reexecute para continuar "
                      "(a coleta e resumivel)." % api.chamadas)
                cx.close()
                return 0
        cx.execute("INSERT OR REPLACE INTO collect_log VALUES(?,?,?,?,1)",
                   (consulta, ini, fim, n))
        cx.commit()
        total += n
        print("[ok] %s..%s -> %d videos" % (ini, fim, n))

    tot = cx.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
    print("\nSNAPSHOT: %d videos no total (%d novos nesta execucao) -> %s"
          % (tot, total, saida.resolve()))
    print("chamadas de API gastas: %d" % api.chamadas)
    cx.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
