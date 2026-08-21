"""
Descoberta — lista tabelas do eTC_Producao e procura a coleta vacinas (2021-22).

O preprint Verjovsky et al. coletou via plataforma eTC >1 M tweets + ~4 M
retweets sobre vacinas (termos: vacina, vacinacao, vacinar, anti-vacinacao,
anti-vax, vacinacao infantil) entre 9/dez/2021 e 9/fev/2022 (+ update 8/mar).
Candidato natural: eTC_Producao / vm067 (coleta continua eTC, mesma casa do
ituassu_2014). Este script lista as tabelas maiores e mostra as colunas das
candidatas, para achar o nome exato da coleta.

Uso: PYTHONIOENCODING=utf-8 python diagnostico/lista_tabelas.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.db import conectar_auto as conectar


def q(cur, sql, args=None):
    cur.execute(sql, args)
    return cur.fetchall()


with conectar(vm="vm067", dbname="eTC_Producao") as conn:
    cur = conn.cursor()

    print("== TABELAS (schema public) por tamanho estimado de linhas ==")
    for r in q(cur, """
        SELECT c.relname,
               c.reltuples::bigint AS linhas_estimadas,
               pg_size_pretty(pg_total_relation_size(c.oid)) AS tamanho
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public' AND c.relkind = 'r'
        ORDER BY c.reltuples DESC
        LIMIT 60;"""):
        print(f"  {r[1]:>14}  {r[2]:>10}  {r[0]}")

    print("\n== TABELAS cujo nome sugere vacinas / covid / saude ==")
    cands = q(cur, """
        SELECT tablename FROM pg_tables
        WHERE schemaname='public'
          AND (tablename ILIKE '%vacin%' OR tablename ILIKE '%vaccin%'
               OR tablename ILIKE '%vax%' OR tablename ILIKE '%covid%'
               OR tablename ILIKE '%saude%' OR tablename ILIKE '%pandem%'
               OR tablename ILIKE '%2021%' OR tablename ILIKE '%2022%')
        ORDER BY 1;""")
    for r in cands:
        print(f"  candidata: {r[0]}")

    # A plataforma eTC pode guardar coletas num schema generico (tweets +
    # tabela de queries/colecoes). Procura tabelas de controle de coleta.
    print("\n== TABELAS de controle de coleta (query/search/colecao/term) ==")
    for r in q(cur, """
        SELECT tablename FROM pg_tables
        WHERE schemaname='public'
          AND (tablename ILIKE '%quer%' OR tablename ILIKE '%search%'
               OR tablename ILIKE '%colet%' OR tablename ILIKE '%collect%'
               OR tablename ILIKE '%term%' OR tablename ILIKE '%monitor%')
        ORDER BY 1;"""):
        print(f"  controle: {r[0]}")

    print("\n== SCHEMAS alem do public (a coleta pode morar em schema proprio) ==")
    for r in q(cur, """
        SELECT nspname FROM pg_namespace
        WHERE nspname NOT IN ('pg_catalog','information_schema','pg_toast')
        ORDER BY 1;"""):
        print(f"  schema: {r[0]}")

    # Mostra as colunas de cada candidata (ate 8)
    for (t,) in cands[:8]:
        print(f"\n-- COLUNAS de {t} --")
        for c in q(cur, """
            SELECT column_name, data_type FROM information_schema.columns
            WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position;""", (t,)):
            print(f"     {c[0]:<28} {c[1]}")

    cur.close()
