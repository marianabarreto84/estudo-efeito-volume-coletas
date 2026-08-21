"""Conta o universo #Eleicoes2014 (normalizado) por dia. Uma varredura da tabela."""
import time
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.db import conectar

# normalizacao acento->ascii feita no proprio Postgres (sem depender da extensao unaccent)
NORM = ("translate(lower({c}),"
        "'áàâãäçéèêëíìîï"
        "óòôõöúùûüýÿñō',"
        "'aaaaaceeeeiiiiooooouuuuyyno')")

SQL = f"""
SELECT (data AT TIME ZONE 'America/Sao_Paulo')::date AS dia,
       count(*) AS n,
       count(*) FILTER (WHERE status_retweet) AS rts,
       count(*) FILTER (WHERE links IS NOT NULL AND cardinality(links)>0) AS com_link
FROM ituassu_2014
WHERE EXISTS (
    SELECT 1 FROM unnest(hashtags) tag
    WHERE {NORM.format(c='tag')} = 'eleicoes2014'
)
GROUP BY 1 ORDER BY 1;
"""

t0 = time.time()
with conectar(vm="vm067", dbname="eTC_Producao") as conn:
    cur = conn.cursor()
    cur.execute(SQL)
    rows = cur.fetchall()
    cur.close()
dt = time.time() - t0

print(f"(varredura levou {dt:.1f}s)\n")
print(f"{'dia':<12}{'total':>9}{'retweets':>10}{'%RT':>7}{'com_link':>10}")
print("-"*48)
tot=totrt=totlink=0
for dia,n,rt,link in rows:
    tot+=n; totrt+=rt; totlink+=link
    print(f"{str(dia):<12}{n:>9}{rt:>10}{100*rt/n:>6.1f}%{link:>10}")
print("-"*48)
print(f"{'TOTAL':<12}{tot:>9}{totrt:>10}{100*totrt/tot:>6.1f}%{totlink:>10}")

# janela do paper: 19-25/out
import datetime as dt_
sem = [r for r in rows if dt_.date(2014,10,19)<=r[0]<=dt_.date(2014,10,25)]
semtot = sum(r[1] for r in sem)
print(f"\nUniverso na janela do paper (19-25/out): {semtot} tweets em {len(sem)} dias")
print(f"Amostra do paper foi 700 (100/dia) -> fracao analisada = {700/semtot*100:.2f}% do universo on-hashtag")
