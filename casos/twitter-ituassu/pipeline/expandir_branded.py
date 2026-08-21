"""
Expansao dos encurtadores "BRANDED" (glo.bo, oesta.do, uol.com...).

Por que faltava: `midia_dominios.ENCURTADOR_PARA_DOMINIO` mapeia o HOST do encurtador
branded direto para a marca (glo.bo -> globo.com), o que ja basta para classificar
MV/MH e MP/MC no nivel de HOST. Por isso `expandir_links.py` so expande os genericos.

Mas isso deixa o PATH invisivel — e o path e' o que distingue
  g1.globo.com/politica/...            (noticia  -> MP)
de
  oglobo.globo.com/brasil/noblat/...   (blog     -> MC no paper de 2018, Tab. 6)

Medido (janela 13-23): ~80% dos tweets MP tem o 1o link atras de um encurtador branded
(glo.bo 7.732, uol.com ~4.368, oesta.do 560) => a analise de blog-em-portal so enxergava
a minoria visivel, que NAO e representativa (Globo e UOL sao onde moram os blogs).

Este script NAO muda classificacao: so popula `final_url` no cache, para a analise de
path (diagnostico/blogs_em_portal.py). Idempotente.

Uso: python pipeline/expandir_branded.py [hashtag|full]
"""
import sqlite3, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
import pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parents[1]))
from core.midia_dominios import _norm_host, ENCURTADOR_PARA_DOMINIO
from core.extrai_links import links_efetivos
from pipeline.expandir_links import expande_uma, init_cache

_modo = sys.argv[1] if len(sys.argv) > 1 else "hashtag"
SNAP = Path(f"data/repl/compos2014/snapshot_{_modo}.sqlite")

# branded a expandir: os do mapa + `uol.com` (encurtador do UOL que hoje tratamos como
# dominio direto porque esta na lista MV/MP — o path dele tambem e' codigo curto).
BRANDED = set(ENCURTADOR_PARA_DOMINIO) | {"uol.com"}


def coleta():
    con = sqlite3.connect(SNAP)
    distintas = {}
    for links_json, texto in con.execute("SELECT links, texto FROM tweets"):
        links = links_efetivos(links_json, texto)
        if not links:
            continue
        u = links[0]
        try:
            h = _norm_host(urlparse(u).netloc)
        except Exception:
            continue
        if h in BRANDED:
            distintas[u] = distintas.get(u, 0) + 1
    con.close()
    return distintas


def main():
    urls = coleta()
    print(f"URLs branded DISTINTAS (1o link): {len(urls)}")
    con = init_cache()
    ja = {r[0] for r in con.execute("SELECT url FROM expand WHERE final_url IS NOT NULL")}
    pend = [(u, f) for u, f in urls.items() if u not in ja]
    print(f"ja resolvidas: {len(urls)-len(pend)} | a resolver: {len(pend)}")

    t0 = time.time(); feito = 0
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = {ex.submit(expande_uma, u): (u, f) for u, f in pend}
        buf = []
        for fut in as_completed(futs):
            u, f = futs[fut]
            final, host, status, code, erro = fut.result()
            buf.append((u, final, host, status, code, erro, f))
            feito += 1
            if len(buf) >= 100:
                con.executemany("INSERT OR REPLACE INTO expand VALUES (?,?,?,?,?,?,?)", buf)
                con.commit(); buf = []
                print(f"  ...{feito}/{len(pend)}  ({time.time()-t0:.0f}s)", flush=True)
        if buf:
            con.executemany("INSERT OR REPLACE INTO expand VALUES (?,?,?,?,?,?,?)", buf)
            con.commit()
    print(f"\nresolvido em {time.time()-t0:.0f}s")
    for r in con.execute("SELECT status, count(*) FROM expand GROUP BY status ORDER BY 2 DESC"):
        print(f"  {r[0]:<12}{r[1]:>6}")
    con.close()


if __name__ == "__main__":
    main()
