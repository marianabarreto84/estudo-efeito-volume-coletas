"""
Fase 0 — Caracteriza a tabela candidata da coleta vacinas no eTC_Producao / vm067.

Passe o nome da tabela achado por lista_tabelas.py:
    PYTHONIOENCODING=utf-8 python diagnostico/explora_vacinas.py <tabela>

Faz: schema (colunas/tipos), indices, range de datas, contagem por dia na janela
do paper (9/dez/2021-8/mar/2022 — deve somar ~1 M tweets + ~4 M RTs), distribuicao
de retweets (quantos passam o limiar >500 do artigo?) e presenca dos termos-indice.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.db import conectar_auto as conectar

JANELA_INI = "2021-12-09"   # abertura da consulta publica (inicio da coleta)
JANELA_FIM = "2022-03-08"   # coleta de atualizacao do artigo


def q(cur, sql, args=None):
    cur.execute(sql, args)
    return cur.fetchall()


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python diagnostico/explora_vacinas.py <tabela>")
    tabela = sys.argv[1]
    # valida identificador simples (evita injecao no nome de tabela)
    if not tabela.replace("_", "").isalnum():
        raise SystemExit(f"nome de tabela invalido: {tabela}")

    with conectar(vm="vm067", dbname="eTC_Producao") as conn:
        cur = conn.cursor()

        print(f"== COLUNAS de {tabela} ==")
        cols = q(cur, """
            SELECT column_name, data_type FROM information_schema.columns
            WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position;""", (tabela,))
        for c in cols:
            print(f"  {c[0]:<28} {c[1]}")
        nomes = {c[0] for c in cols}

        print(f"\n== INDICES ==")
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
            print(f"\n== CONTAGEM POR DIA na janela do paper ({JANELA_INI} a {JANELA_FIM}) ==")
            print("   (soma deve ficar na ordem de 1 M tweets / 5 M com RTs)")
            for r in q(cur, f"""
                SELECT ({col_data} AT TIME ZONE 'America/Sao_Paulo')::date AS dia, count(*)
                FROM {tabela}
                WHERE ({col_data} AT TIME ZONE 'America/Sao_Paulo')::date BETWEEN %s AND %s
                GROUP BY 1 ORDER BY 1;""", (JANELA_INI, JANELA_FIM)):
                print(f"  {r[0]}  {r[1]:>10,}")

        # distribuicao de retweets: quantos passam o limiar >500 do artigo?
        col_rt = next((c for c in ("retweets", "num_retweets", "retweet_count", "rts") if c in nomes), None)
        if col_rt:
            print(f"\n== DISTRIBUICAO DE RTs (coluna '{col_rt}') na janela ==")
            print("   (o artigo achou 602 autores influentes com tweets >500 RT)")
            filtro_data = (f"WHERE ({col_data} AT TIME ZONE 'America/Sao_Paulo')::date "
                           f"BETWEEN '{JANELA_INI}' AND '{JANELA_FIM}'") if col_data else ""
            for limiar in (500, 250, 100, 50, 10, 1, 0):
                r = q(cur, f"SELECT count(*) FROM {tabela} {filtro_data} "
                           f"{'AND' if filtro_data else 'WHERE'} {col_rt} > %s;", (limiar,))
                print(f"  RTs > {limiar:>4}: {r[0][0]:>12,} tweets")

        # texto: os termos-indice do artigo aparecem?
        col_txt = next((c for c in ("texto", "text", "content_text", "tweet_text", "conteudo") if c in nomes), None)
        if col_txt:
            print(f"\n== TERMOS-INDICE (amostra 100k da coluna '{col_txt}') ==")
            for termo in ("vacina", "vacinação", "vacinar", "anti-vacinação", "anti-vax", "vacinação infantil"):
                r = q(cur, f"""SELECT count(*) FROM (SELECT {col_txt} FROM {tabela} LIMIT 100000) s
                               WHERE s.{col_txt} ILIKE %s;""", (f"%{termo}%",))
                print(f"  contem '{termo}': {r[0][0]:,} / 100.000")

        cur.close()


if __name__ == "__main__":
    main()
