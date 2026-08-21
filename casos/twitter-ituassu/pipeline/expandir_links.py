"""
Expansao de URLs curtas (encurtadores) do snapshot A_mais_hashtag.

Motivo: a analise de midia (MV/MH) do paper olha o dominio do 1o link. Em 2014
esses links foram encurtados (bit.ly, goo.gl, ow.ly, ...). Para classificar o
dominio final hoje, precisamos expandi-los seguindo os redirects HTTP.

Metodo:
  - coleta as URLs curtas DISTINTAS que sao 1o link de algum tweet e cujo host e
    um encurtador generico (classe 'encurtador' em midia_dominios).
  - resolve cada uma com urllib (GET, sem baixar corpo; segue redirects; timeout).
  - grava host final + status em cache SQLite (idempotente/reproduzivel).
  - encurtadores mortos (ex.: goo.gl, desligado ago/2025) caem como 'morto'.

Saida: data/repl/compos2014/expand_cache.sqlite  (url, final_url, final_host,
       status, http_code, erro)  +  relatorio no stdout.

Re-executar e barato: URLs ja no cache sao puladas.
"""
import json, sqlite3, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.midia_dominios import _norm_host, ENCURTADORES, ENCURTADOR_PARA_DOMINIO

# snapshot alvo via CLI: python expandir_links.py [hashtag|full]
_modo = sys.argv[1] if len(sys.argv) > 1 else "hashtag"
SNAP = Path(f"data/repl/compos2014/snapshot_{_modo}.sqlite")
CACHE = Path("data/repl/compos2014/expand_cache.sqlite")  # cache compartilhado entre snapshots
GENERICOS = ENCURTADORES - set(ENCURTADOR_PARA_DOMINIO)  # os que sobram como 'encurtador'
UA = "Mozilla/5.0 (replicacao-academica; expansao de links 2014)"
TIMEOUT = 8
WORKERS = 24


def coleta_urls_curtas():
    con = sqlite3.connect(SNAP)
    distintas = {}
    for (links_json,) in con.execute("SELECT links FROM tweets"):
        links = json.loads(links_json) if links_json else []
        if not links:
            continue
        u = links[0]
        try:
            h = _norm_host(urlparse(u).netloc)
        except Exception:
            continue
        if h in GENERICOS:
            distintas[u] = distintas.get(u, 0) + 1
    con.close()
    return distintas  # url -> frequencia


def expande_uma(url):
    """Segue redirects e devolve (final_url, final_host, status, http_code, erro)."""
    try:
        req = Request(url, method="GET", headers={"User-Agent": UA})
        # urlopen segue 301/302 automaticamente; nao lemos o corpo.
        resp = urlopen(req, timeout=TIMEOUT)
        final = resp.geturl()
        code = resp.getcode()
        resp.close()
        host = _norm_host(urlparse(final).netloc)
        # se ainda for um encurtador, considera nao resolvido de fato
        status = "ok" if host and host not in GENERICOS else "ainda_curto"
        return final, host, status, code, None
    except HTTPError as e:
        # muitos encurtadores mortos devolvem 404/410
        final = getattr(e, "url", url)
        host = _norm_host(urlparse(final).netloc)
        return final, host, "morto", e.code, f"HTTP {e.code}"
    except (URLError, TimeoutError, Exception) as e:
        return None, None, "erro", None, f"{type(e).__name__}: {e}"[:120]


def init_cache():
    con = sqlite3.connect(CACHE)
    con.execute("""CREATE TABLE IF NOT EXISTS expand(
        url TEXT PRIMARY KEY, final_url TEXT, final_host TEXT,
        status TEXT, http_code INTEGER, erro TEXT, freq INTEGER)""")
    con.commit()
    return con


def main():
    urls = coleta_urls_curtas()
    print(f"URLs curtas distintas (1o link, encurtador generico): {len(urls)}")
    con = init_cache()
    ja = {r[0] for r in con.execute("SELECT url FROM expand")}
    pendentes = [(u, f) for u, f in urls.items() if u not in ja]
    print(f"ja no cache: {len(ja)} | a resolver agora: {len(pendentes)}")

    t0 = time.time()
    feito = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
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

    # relatorio
    print(f"\nresolvido em {time.time()-t0:.0f}s")
    print("\n== status da expansao (por URL distinta) ==")
    for r in con.execute("SELECT status, count(*), sum(freq) FROM expand GROUP BY status ORDER BY 2 DESC"):
        print(f"  {r[0]:<12} urls={r[1]:>6}  tweets={r[2]:>7}")
    print("\n== top 20 hosts finais resolvidos (por tweets) ==")
    for r in con.execute("""SELECT final_host, count(*), sum(freq) FROM expand
                            WHERE status='ok' GROUP BY final_host ORDER BY 3 DESC LIMIT 20"""):
        print(f"  {r[0]:<32} urls={r[1]:>5} tweets={r[2]:>6}")
    con.close()
    print(f"\n[ok] cache -> {CACHE}")


if __name__ == "__main__":
    main()
