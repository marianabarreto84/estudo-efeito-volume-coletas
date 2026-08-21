"""
Rankeia os dominios 'indefinido' (1o link resolvido, mas fora do dicionario MP/MC)
na janela 13-23/out. Insumo para a decisao (2): quais entram na lista de MC.

Nao decide nada — so lista por frequencia, para curadoria humana. Rode depois da
expansao (expandir_links.py + expandir_links_texto.py) para pegar o t.co resolvido.

Uso: python diagnostico/top_indefinidos.py
Saida: data/repl/compos2014/INDEFINIDOS_candidatos_MC.md
"""
import sqlite3
from collections import Counter
from pathlib import Path
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.resolve_mp_mc import classe_mp_mc_do_primeiro_link, carrega_cache_mp_mc
from core.extrai_links import links_efetivos

DB = Path("data/repl/compos2014/snapshot_hashtag.sqlite")
CACHE = carrega_cache_mp_mc(Path("data/repl/compos2014/expand_cache.sqlite"))
OUT = Path("data/repl/compos2014/INDEFINIDOS_candidatos_MC.md")
W = "data_brt >= '2014-10-13' AND data_brt < '2014-10-24'"
TOP = 60


def host_final(links, cache):
    """Host final do 1o link. `cache` = carrega_cache_mp_mc -> (final_url, final_host, status)."""
    from urllib.parse import urlparse
    from core.midia_dominios import _norm_host, ENCURTADOR_PARA_DOMINIO
    from core.resolve_mp_mc import GENERICOS, BRANDED
    if not links:
        return None
    u = links[0]
    try:
        h = _norm_host(urlparse(u).netloc)
    except Exception:
        return None
    if h in GENERICOS or h in BRANDED:
        fu, fh, st = cache.get(u, (None, None, None))
        if st == "ok" and (fu or fh):
            return _norm_host(urlparse(fu).netloc) if fu else _norm_host(fh)
        return ENCURTADOR_PARA_DOMINIO.get(h, h) if h in BRANDED else None
    return ENCURTADOR_PARA_DOMINIO.get(h, h)


def main():
    con = sqlite3.connect(DB)
    cont = Counter()
    for links_json, texto in con.execute(f"SELECT links, texto FROM tweets WHERE {W}"):
        links = links_efetivos(links_json, texto)
        cl, _ = classe_mp_mc_do_primeiro_link(links, CACHE)
        if cl == "indefinido":
            h = host_final(links, CACHE)
            if h:
                cont[h] += 1
    total = sum(cont.values())
    linhas = ["# Domínios `indefinido` — candidatos à lista MC (janela 13–23/out)",
              "",
              f"> Gerado por `diagnostico/top_indefinidos.py`. Total de tweets `indefinido`: "
              f"**{total}**. 1º link resolvido, fora do dicionário MP/MC atual. Decisão (2): "
              f"marcar quais viram MC (mídia complementar de verdade) vs. lixo/não-mídia.",
              "",
              "| # | domínio | tweets | MC? (marcar) |",
              "|--:|---|--:|:--:|"]
    for i, (h, c) in enumerate(cont.most_common(TOP), 1):
        linhas.append(f"| {i} | {h} | {c} | |")
    OUT.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"[ok] {total} tweets indefinidos; top {TOP} -> {OUT}")
    for h, c in cont.most_common(25):
        print(f"  {h:<36}{c:>6}")


if __name__ == "__main__":
    main()
