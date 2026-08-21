"""
Classificacao de midia do 1o link de um tweet, consultando o cache de expansao.

classe_do_primeiro_link(links, cache) -> (classe, host_final)
  classes possiveis: 'MV', 'MH', 'NDA' (sem link), 'indefinido' (dominio real fora
  do dicionario), 'nao_resolvido' (encurtador morto/erro/nao expandido).
"""
import sqlite3
from urllib.parse import urlparse
from core.midia_dominios import (_norm_host, classificar_host,
                            ENCURTADORES, ENCURTADOR_PARA_DOMINIO)

GENERICOS = ENCURTADORES - set(ENCURTADOR_PARA_DOMINIO)


def carrega_cache(path):
    con = sqlite3.connect(path)
    d = {}
    try:
        for url, fh, status in con.execute("SELECT url, final_host, status FROM expand"):
            d[url] = (fh, status)
    except sqlite3.OperationalError:
        pass  # cache ainda nao existe
    con.close()
    return d


def classe_do_primeiro_link(links, cache):
    if not links:
        return "NDA", None
    u = links[0]
    try:
        host = _norm_host(urlparse(u).netloc)
    except Exception:
        return "indefinido", None
    if not host:
        return "indefinido", None
    if host in GENERICOS:
        # encurtador generico: usa o host final do cache, se resolvido
        fh, status = cache.get(u, (None, None))
        if status == "ok" and fh:
            return classificar_host(fh), fh
        return "nao_resolvido", host
    # dominio direto ou encurtador branded (classificar_host ja mapeia os branded)
    return classificar_host(host), host
