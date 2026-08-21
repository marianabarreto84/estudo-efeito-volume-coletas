"""
Dimensiona o universo A_mais_full (eixo E2 = escopo tematico amplo) vs A_mais_hashtag.

Definicoes candidatas (a partir dos termos reais da coleta eTC 2014):
  - TABELA INTEIRA        = tudo que foi coletado (termos: Dilma, Rousseff, PT, PSDB,
                            Aecio, Aecio Neves, #Eleicoes2014, #PT, #PSDB, #AecioPeloBrasil,
                            #DilmaMudaMais, #13, #45) -> A_mais_full mais amplo (ruidoso).
  - HASHTAG ELEITORAL     = tem alguma das hashtags eleitorais (menos ruido que keyword).
  - SO #ELEICOES2014      = A_mais_hashtag (ja extraido).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.db import conectar

NORM = "translate(lower({c}),'áàâãäçéèêëíìîïóòôõöúùûüýÿñō','aaaaaceeeeiiiiooooouuuuyyno')"
# hashtags eleitorais normalizadas (da lista de termos da coleta)
HASHTAGS_ELEITORAIS = ("eleicoes2014", "pt", "psdb", "aeciopelobrasil", "dilmamudamais", "13", "45")

SQL = f"""
SELECT (data AT TIME ZONE 'America/Sao_Paulo')::date AS dia,
       count(*) AS total,
       count(*) FILTER (WHERE EXISTS (
           SELECT 1 FROM unnest(hashtags) t WHERE {NORM.format(c='t')} = ANY(%s))) AS com_hashtag_eleitoral,
       count(*) FILTER (WHERE EXISTS (
           SELECT 1 FROM unnest(hashtags) t WHERE {NORM.format(c='t')} = 'eleicoes2014')) AS so_eleicoes2014
FROM ituassu_2014
GROUP BY 1 ORDER BY 1;
"""

import time
t0=time.time()
with conectar(vm="vm067", dbname="eTC_Producao") as conn:
    cur = conn.cursor()
    cur.execute(SQL, (list(HASHTAGS_ELEITORAIS),))
    rows = cur.fetchall()
    cur.close()
print(f"(varredura {time.time()-t0:.0f}s)\n")
print(f"{'dia':<12}{'TABELA':>10}{'c/hashtag_elei':>16}{'so_elei2014':>13}")
print("-"*51)
tt=th=te=0
for dia,total,hh,ee in rows:
    tt+=total; th+=hh; te+=ee
    print(f"{str(dia):<12}{total:>10}{hh:>16}{ee:>13}")
print("-"*51)
print(f"{'TOTAL':<12}{tt:>10}{th:>16}{te:>13}")

import datetime as d
jan = lambda rs: (sum(r[1] for r in rs), sum(r[2] for r in rs), sum(r[3] for r in rs))
sem = [r for r in rows if d.date(2014,10,19)<=r[0]<=d.date(2014,10,25)]
st,sh,se = jan(sem)
print(f"\nJanela 19-25/out:")
print(f"  A_mais_full (tabela)      = {st}")
print(f"  A_mais_full (hashtag elei)= {sh}")
print(f"  A_mais_hashtag (#elei2014)= {se}")
