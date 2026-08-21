"""
Descoberta — lista tabelas do eTC_Producao e procura a coleta de 2022 (Heine).

A dissertacao do Heine coletou ~57,9 mi de tweets das eleicoes 2022 (Lula x
Bolsonaro), inicialmente no MongoDB, depois carregados no PostgreSQL (esquema
TreeTech). Esta coleta deve estar no mesmo eTC_Producao / vm067 que guarda o
ituassu_2014. Este script lista as tabelas maiores e mostra as colunas das
candidatas, para achar o nome exato da tabela 2022.

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

    print("\n== TABELAS cujo nome sugere 2022 / eleicoes / lula / bolsonaro ==")
    cands = q(cur, """
        SELECT tablename FROM pg_tables
        WHERE schemaname='public'
          AND (tablename ILIKE '%2022%' OR tablename ILIKE '%elei%'
               OR tablename ILIKE '%lula%' OR tablename ILIKE '%bolsonaro%'
               OR tablename ILIKE '%heine%' OR tablename ILIKE '%treetech%')
        ORDER BY 1;""")
    for r in cands:
        print(f"  candidata: {r[0]}")

    # Mostra as colunas de cada candidata (ate 8)
    for (t,) in cands[:8]:
        print(f"\n-- COLUNAS de {t} --")
        for c in q(cur, """
            SELECT column_name, data_type FROM information_schema.columns
            WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position;""", (t,)):
            print(f"     {c[0]:<28} {c[1]}")

    cur.close()
