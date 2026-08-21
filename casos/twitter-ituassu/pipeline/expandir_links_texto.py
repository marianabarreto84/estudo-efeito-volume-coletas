"""
Expansao dos encurtadores que estao NO TEXTO de tweets cujo campo `links` esta
vazio (retweets nativos de 2014). Complementa `expandir_links.py`, que so olha o
campo estruturado. Grava no MESMO cache (idempotente).

Achado (jul/2026): ~9% dos tweets da janela tem t.co so no texto -> sem isto,
viram NDA por engano. Ver core/extrai_links.py e RESULTADOS_FASE0_mp_mc.md.

Uso: python pipeline/expandir_links_texto.py [hashtag|full]
Muitos t.co de 2014 estao mortos hoje -> caem como 'morto' (teto de recuperacao).
"""
import sqlite3, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
import pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parents[1]))
from core.midia_dominios import _norm_host, ENCURTADORES, ENCURTADOR_PARA_DOMINIO
from core.extrai_links import extrai_urls_texto
from pipeline.expandir_links import expande_uma, init_cache

_modo = sys.argv[1] if len(sys.argv) > 1 else "hashtag"
SNAP = Path(f"data/repl/compos2014/snapshot_{_modo}.sqlite")
GENERICOS = ENCURTADORES - set(ENCURTADOR_PARA_DOMINIO)


def coleta_urls_texto():
    """URLs curtas (encurtador generico) que aparecem no TEXTO de tweets sem `links`."""
    con = sqlite3.connect(SNAP)
    distintas = {}
    for links_json, texto in con.execute("SELECT links, texto FROM tweets"):
        if links_json and links_json not in ("[]", "null"):
            continue  # ja tem link estruturado -> nao e o caso aqui
        for u in extrai_urls_texto(texto or ""):
            try:
                h = _norm_host(urlparse(u).netloc)
            except Exception:
                continue
            if h in GENERICOS:
                distintas[u] = distintas.get(u, 0) + 1
    con.close()
    return distintas


def main():
    urls = coleta_urls_texto()
    print(f"URLs curtas DISTINTAS no texto (tweets sem campo links): {len(urls)}")
    con = init_cache()
    ja = {r[0] for r in con.execute("SELECT url FROM expand")}
    pendentes = [(u, f) for u, f in urls.items() if u not in ja]
    print(f"ja no cache: {sum(1 for u in urls if u in ja)} | a resolver agora: {len(pendentes)}")

    t0 = time.time(); feito = 0
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = {ex.submit(expande_uma, u): (u, f) for u, f in pendentes}
        buf = []
        for fut in as_completed(futs):
            u, f = futs[fut]
            final, host, status, code, erro = fut.result()
            buf.append((u, final, host, status, code, erro, f))
            feito += 1
            if len(buf) >= 200:
                con.executemany("INSERT OR REPLACE INTO expand VALUES (?,?,?,?,?,?,?)", buf)
                con.commit(); buf = []
                print(f"  ...{feito}/{len(pendentes)}  ({time.time()-t0:.0f}s)", flush=True)
        if buf:
            con.executemany("INSERT OR REPLACE INTO expand VALUES (?,?,?,?,?,?,?)", buf)
            con.commit()

    print(f"\nresolvido em {time.time()-t0:.0f}s")
    print("\n== status (por URL distinta do texto que estava pendente) ==")
    for r in con.execute("SELECT status, count(*) FROM expand GROUP BY status ORDER BY 2 DESC"):
        print(f"  {r[0]:<12} urls={r[1]:>6}")
    con.close()


if __name__ == "__main__":
    main()
