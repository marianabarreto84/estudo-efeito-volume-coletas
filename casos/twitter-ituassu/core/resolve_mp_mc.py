"""
Classificacao MP/MC do 1o link de um tweet, consultando o cache de expansao.
Irmao de core.resolve_midia (que faz MV/MH por HOST); aqui a classificacao e' por
URL COMPLETA, para pegar blog/coluna hospedado em dominio MP (Tab. 6 do paper 2018).

classe_mp_mc_do_primeiro_link(links, cache) -> (classe, host_final)
  classes: 'MP', 'MC', 'nao_midia', 'NDA' (sem link), 'indefinido' (dominio real fora
  do dicionario), 'nao_resolvido' (encurtador generico morto/nao expandido).

O `cache` aqui e' o de `carrega_cache_mp_mc` (traz final_url, nao so final_host) —
NAO o de core.resolve_midia.carrega_cache.
"""
import sqlite3
from urllib.parse import urlparse
from core.midia_dominios import _norm_host, ENCURTADORES, ENCURTADOR_PARA_DOMINIO
from core.midia_mp_mc import classificar_host_mp_mc, classificar_url_mp_mc

GENERICOS = ENCURTADORES - set(ENCURTADOR_PARA_DOMINIO)
# Encurtadores "branded": o host ja revela a marca (glo.bo -> globo.com), mas o PATH e'
# codigo curto. Expandidos por pipeline/expandir_branded.py. `uol.com` entra aqui porque
# e' o encurtador do UOL, embora esteja na lista de dominios MP.
BRANDED = set(ENCURTADOR_PARA_DOMINIO) | {"uol.com"}


def carrega_cache_mp_mc(path):
    """url_curta -> (final_url, final_host, status). Traz a URL completa (para o path)."""
    con = sqlite3.connect(path)
    d = {}
    try:
        for url, fu, fh, st in con.execute(
                "SELECT url, final_url, final_host, status FROM expand"):
            d[url] = (fu, fh, st)
    except sqlite3.OperationalError:
        pass  # cache ainda nao existe
    con.close()
    return d


def classe_mp_mc_do_primeiro_link(links, cache):
    if not links:
        return "NDA", None
    u = links[0]
    try:
        host = _norm_host(urlparse(u).netloc)
    except Exception:
        return "indefinido", None
    if not host:
        return "indefinido", None

    if host in GENERICOS or host in BRANDED:
        fu, fh, st = cache.get(u, (None, None, None))
        if st == "ok" and (fu or fh):
            if fu:  # temos a URL completa -> da p/ checar blog/coluna no path
                return classificar_url_mp_mc(fu), _norm_host(urlparse(fu).netloc)
            return classificar_host_mp_mc(fh), _norm_host(fh)
        # nao resolveu:
        if host in BRANDED:
            # o host ja revela a marca -> classifica por host (path fica invisivel;
            # subcontagem conhecida de blog-em-portal). Mantem o comportamento antigo.
            canon = ENCURTADOR_PARA_DOMINIO.get(host, host)
            return classificar_host_mp_mc(canon), canon
        return "nao_resolvido", host

    # dominio direto: a propria URL ja tem o path
    return classificar_url_mp_mc(u), host
