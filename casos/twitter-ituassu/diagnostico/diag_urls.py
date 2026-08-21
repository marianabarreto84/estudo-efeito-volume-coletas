"""Verifica se ha URLs expandidas em urls_detalhes / descricao_urls (viabilidade MV/MH)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.db import conectar
from core.midia_dominios import ENCURTADORES

NORM = ("translate(lower({c}),'áàâãäçéèêëíìîïóòôõöúùûüýÿñō','aaaaaceeeeiiiiooooouuuuyyno')")

with conectar(vm="vm067", dbname="eTC_Producao") as conn:
    cur = conn.cursor()
    # tipos reais das colunas de url
    cur.execute("""SELECT column_name, data_type, udt_name FROM information_schema.columns
                   WHERE table_name='ituassu_2014' AND column_name IN
                   ('links','urls_detalhes','descricao_urls') ORDER BY 1;""")
    print("== colunas de URL ==")
    for r in cur.fetchall(): print(f"  {r[0]}: {r[1]} ({r[2]})")

    print("\n== 12 tweets on-hashtag COM link: links vs urls_detalhes vs descricao_urls ==")
    cur.execute(f"""
        SELECT links, urls_detalhes, descricao_urls
        FROM ituassu_2014
        WHERE cardinality(links)>0
          AND EXISTS (SELECT 1 FROM unnest(hashtags) t WHERE {NORM.format(c='t')}='eleicoes2014')
        LIMIT 12;""")
    for links, ud, du in cur.fetchall():
        print(f"  links         = {links}")
        print(f"  urls_detalhes = {ud}")
        print(f"  descricao_urls= {du}")
        print("  ---")
    cur.close()
