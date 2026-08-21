"""
Fase 1 — Snapshot congelado do caso Heine 2022 para SQLite local (introspectivo).

Auto-detecta as colunas da tabela via information_schema, então funciona com o
schema real assim que soubermos o nome (rode diagnostico/explora_heine.py antes).

Uso:
    # snapshot do dia do 1o turno (universo de tópicos, ~1,29 M):
    PYTHONIOENCODING=utf-8 python pipeline/extrai_snapshot_heine.py <tabela> --dia 2022-10-02
    # snapshot de um bloco inteiro (ex.: 2-16/out):
    PYTHONIOENCODING=utf-8 python pipeline/extrai_snapshot_heine.py <tabela> --de 2022-10-02 --ate 2022-10-16

Saída: data/repl/heine2022/snapshot_<rotulo>.sqlite + MANIFEST_<rotulo>.txt

Obs.: para o EIXO QUANTITATIVO (engajamento/tempo) NÃO é preciso baixar as 57,9 M
linhas — use analise/quantitativa_heine.py, que agrega no servidor via SQL.
Este snapshot serve ao EIXO TÓPICOS, que precisa do texto tweet-a-tweet.
"""
import argparse, sqlite3, time
from pathlib import Path
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.db import conectar_auto as conectar

OUT_DIR = Path("data/repl/heine2022")
OUT_DIR.mkdir(parents=True, exist_ok=True)

COL_DATA_CANDS = ("data", "created_at", "data_criacao", "timestamp", "date")


def detectar_colunas(cur, tabela):
    cur.execute("""SELECT column_name, data_type FROM information_schema.columns
                   WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position;""", (tabela,))
    return cur.fetchall()  # [(nome, tipo), ...]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tabela")
    ap.add_argument("--dia", help="YYYY-MM-DD (um único dia)")
    ap.add_argument("--de", help="YYYY-MM-DD (início do intervalo)")
    ap.add_argument("--ate", help="YYYY-MM-DD (fim do intervalo, inclusivo)")
    ap.add_argument("--rotulo", help="rótulo do arquivo de saída")
    args = ap.parse_args()
    if not args.tabela.replace("_", "").isalnum():
        raise SystemExit(f"nome de tabela inválido: {args.tabela}")

    with conectar(vm="vm067", dbname="eTC_Producao") as conn:
        cur = conn.cursor()
        cols = detectar_colunas(cur, args.tabela)
        if not cols:
            raise SystemExit(f"tabela {args.tabela} sem colunas / inexistente")
        nomes = [c[0] for c in cols]
        tipos = {c[0]: c[1] for c in cols}
        col_data = next((c for c in COL_DATA_CANDS if c in nomes), None)
        if not col_data:
            raise SystemExit(f"nenhuma coluna de data encontrada em {nomes}")

        # filtro temporal
        if args.dia:
            where = f"({col_data} AT TIME ZONE 'America/Sao_Paulo')::date = %s"
            params = (args.dia,)
            rotulo = args.rotulo or f"dia_{args.dia}"
        elif args.de and args.ate:
            where = f"({col_data} AT TIME ZONE 'America/Sao_Paulo')::date BETWEEN %s AND %s"
            params = (args.de, args.ate)
            rotulo = args.rotulo or f"{args.de}_a_{args.ate}"
        else:
            raise SystemExit("informe --dia OU (--de e --ate)")

        # arrays viram TEXT (JSON) no SQLite; demais colunas cruas
        array_cols = {n for n, t in tipos.items() if t == "ARRAY"}
        sel_cols = ", ".join(f'"{n}"' for n in nomes)
        select_sql = (f"SELECT {sel_cols}, ({col_data} AT TIME ZONE 'America/Sao_Paulo') AS data_brt "
                      f"FROM {args.tabela} WHERE {where}")

        db_path = OUT_DIR / f"snapshot_{rotulo}.sqlite"
        if db_path.exists():
            db_path.unlink()
        loc = sqlite3.connect(db_path)
        ddl = ", ".join(f'"{n}" TEXT' if n in array_cols else f'"{n}"' for n in nomes)
        loc.execute(f'CREATE TABLE tweets ({ddl}, data_brt TEXT);')

        import json
        t0 = time.time(); n = 0
        scur = conn.cursor(name="stream_heine")
        scur.itersize = 5000
        scur.execute(select_sql, params)
        ins = f'INSERT INTO tweets VALUES ({",".join("?"*(len(nomes)+1))})'
        batch = []
        for row in scur:
            vals = []
            for i, nome in enumerate(nomes):
                v = row[i]
                vals.append(json.dumps(v, ensure_ascii=False, default=str) if nome in array_cols else v)
            data_brt = row[len(nomes)]
            vals.append(data_brt.isoformat() if data_brt else None)
            batch.append(vals)
            if len(batch) >= 5000:
                loc.executemany(ins, batch); loc.commit(); n += len(batch); batch = []
                print(f"  ...{n:,} linhas", flush=True)
        if batch:
            loc.executemany(ins, batch); loc.commit(); n += len(batch)
        scur.close()
        loc.execute("CREATE INDEX ix_data ON tweets(data_brt);")
        loc.commit()
        dt = time.time() - t0

        (OUT_DIR / f"MANIFEST_{rotulo}.txt").write_text(
            f"Snapshot caso Heine 2022 — {rotulo}\n"
            f"origem: vm067 / eTC_Producao / public.{args.tabela}\n"
            f"filtro: {where % params if False else where}  params={params}\n"
            f"linhas: {n}\n"
            f"colunas: {', '.join(nomes)}, data_brt\n"
            f"extraido_em_segundos: {dt:.1f}\n", encoding="utf-8")
        print(f"\n[ok] {n:,} linhas -> {db_path}  ({dt:.1f}s)")


if __name__ == "__main__":
    main()
