"""
Fase 0 — Caracteriza a tabela 2022 (Heine) no eTC_Producao / vm067.

Passe o nome da tabela achado por lista_tabelas.py:
    PYTHONIOENCODING=utf-8 python diagnostico/explora_heine.py <tabela>

Faz: schema (colunas/tipos), índices, range de datas, contagem total, contagem do
dia 2/out/2022 (deve bater ~1,29 M do Cap. 4), preenchimento de likes/retweets/
quotes/replies (eixo B) e top hashtags — tudo em amostra quando a tabela é grande.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.db import conectar_auto as conectar


def q(cur, sql, args=None):
    cur.execute(sql, args)
    return cur.fetchall()


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python diagnostico/explora_heine.py <tabela>")
    tabela = sys.argv[1]
    # valida identificador simples (evita injeção no nome de tabela)
    if not tabela.replace("_", "").isalnum():
        raise SystemExit(f"nome de tabela inválido: {tabela}")

    with conectar(vm="vm067", dbname="eTC_Producao") as conn:
        cur = conn.cursor()

        print(f"== COLUNAS de {tabela} ==")
        cols = q(cur, """
            SELECT column_name, data_type FROM information_schema.columns
            WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position;""", (tabela,))
        for c in cols:
            print(f"  {c[0]:<28} {c[1]}")
        nomes = {c[0] for c in cols}

        print(f"\n== ÍNDICES ==")
        for r in q(cur, """SELECT indexname, indexdef FROM pg_indexes
                           WHERE schemaname='public' AND tablename=%s ORDER BY 1;""", (tabela,)):
            print(f"  {r[0]}: {r[1]}")

        print(f"\n== CONTAGEM TOTAL (estimada) ==")
        r = q(cur, """SELECT reltuples::bigint FROM pg_class WHERE relname=%s;""", (tabela,))
        print(f"  ~{r[0][0]:,} linhas (estimativa do planner)")

        # coluna de data: candidatos comuns
        col_data = next((c for c in ("data", "created_at", "data_criacao", "timestamp", "date") if c in nomes), None)
        if col_data:
            print(f"\n== RANGE DE DATAS (coluna '{col_data}', America/Sao_Paulo) ==")
            r = q(cur, f"""SELECT min({col_data} AT TIME ZONE 'America/Sao_Paulo'),
                                  max({col_data} AT TIME ZONE 'America/Sao_Paulo')
                           FROM {tabela};""")[0]
            print(f"  min={r[0]}  max={r[1]}")
            print(f"\n== CONTAGEM POR DIA (deve mostrar 2/out e 30/out como picos) ==")
            for r in q(cur, f"""
                SELECT ({col_data} AT TIME ZONE 'America/Sao_Paulo')::date AS dia, count(*)
                FROM {tabela} GROUP BY 1 ORDER BY 1;"""):
                print(f"  {r[0]}  {r[1]:>10,}")

        # campos de engajamento (eixo B)
        eng = [c for c in ("likes", "retweets", "replies", "quotes",
                           "num_likes", "num_retweets", "num_replies", "num_quotes") if c in nomes]
        if eng:
            print(f"\n== PREENCHIMENTO ENGAJAMENTO (amostra 200k): {eng} ==")
            sel = ", ".join(f"count({c}) FILTER (WHERE {c} IS NOT NULL) AS {c}_nn" for c in eng)
            r = q(cur, f"SELECT count(*) n, {sel} FROM (SELECT * FROM {tabela} LIMIT 200000) s;")[0]
            print(f"  amostra={r[0]:,}")
            for i, c in enumerate(eng):
                print(f"    {c}: não-nulos={r[i+1]:,}")

        cur.close()


if __name__ == "__main__":
    main()
