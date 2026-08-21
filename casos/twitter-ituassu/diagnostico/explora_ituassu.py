"""Caracterizacao da tabela public.ituassu_2014 (vm067 / eTC_Producao)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.db import conectar

def q(cur, sql, args=None):
    cur.execute(sql, args)
    return cur.fetchall()

with conectar(vm="vm067", dbname="eTC_Producao") as conn:
    cur = conn.cursor()

    print("== INDICES ==")
    for r in q(cur, """
        SELECT indexname, indexdef FROM pg_indexes
        WHERE schemaname='public' AND tablename='ituassu_2014' ORDER BY 1;"""):
        print(f"  {r[0]}: {r[1]}")

    print("\n== RANGE DE DATAS (coluna 'data', em America/Sao_Paulo) ==")
    r = q(cur, """
        SELECT min(data AT TIME ZONE 'America/Sao_Paulo'),
               max(data AT TIME ZONE 'America/Sao_Paulo'),
               count(*) FILTER (WHERE data IS NULL) AS nulos
        FROM ituassu_2014;""")[0]
    print(f"  min={r[0]}  max={r[1]}  datas_nulas={r[2]}")

    print("\n== PREENCHIMENTO DE CAMPOS-CHAVE (amostra de 200k linhas) ==")
    r = q(cur, """
        SELECT
          count(*) AS n,
          count(*) FILTER (WHERE hashtags IS NOT NULL AND cardinality(hashtags)>0) AS com_hashtags,
          count(*) FILTER (WHERE links IS NOT NULL AND cardinality(links)>0) AS com_links,
          count(*) FILTER (WHERE status_retweet IS TRUE) AS retweets,
          count(*) FILTER (WHERE status_retweet IS NULL) AS rt_nulo,
          count(*) FILTER (WHERE texto ILIKE '%elei%2014%') AS texto_elei2014
        FROM (SELECT * FROM ituassu_2014 LIMIT 200000) s;""")[0]
    print(f"  linhas_amostradas={r[0]}")
    print(f"  com_hashtags={r[1]}  com_links={r[2]}")
    print(f"  status_retweet=TRUE:{r[3]}  NULL:{r[4]}")
    print(f"  texto contem 'elei...2014': {r[5]}")

    print("\n== TOP 25 HASHTAGS (amostra 200k) ==")
    for r in q(cur, """
        SELECT lower(tag) AS h, count(*) c
        FROM (SELECT * FROM ituassu_2014 LIMIT 200000) s,
             LATERAL unnest(s.hashtags) AS tag
        GROUP BY 1 ORDER BY c DESC LIMIT 25;"""):
        print(f"  {r[1]:>7}  #{r[0]}")

    print("\n== AMOSTRA DE 3 LINHAS (campos selecionados) ==")
    for r in q(cur, """
        SELECT id_tweet, data AT TIME ZONE 'America/Sao_Paulo', autor,
               left(texto,80), hashtags, links, status_retweet, autor_original, tweet_tipo
        FROM ituassu_2014 LIMIT 3;"""):
        print(f"  id={r[0]} data={r[1]} autor={r[2]}")
        print(f"    texto={r[3]!r}")
        print(f"    hashtags={r[4]} links={r[5]}")
        print(f"    RT={r[6]} autor_original={r[7]} tipo={r[8]}")

    cur.close()
