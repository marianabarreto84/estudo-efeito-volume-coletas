"""
DESCOBERTA: quais secoes dos dominios MP sao, na verdade, blog/coluna?

Motivo: o paper de 2018 codifica "Blog do Reinaldo Azevedo (Veja)", "Blog da Miriam
Leitao (O Globo)", "Blog Julia Duailibi (Estadao)", "Blog da Laura Capriglione (Yahoo)"
como MC (Tab. 6) — mas nossa regra olha so o HOST e chama tudo isso de MP. Este script
NAO decide nada: ranqueia os prefixos de path nos hosts MP para curadoria humana.

Fonte da URL completa:
  - link direto  -> a propria URL do tweet
  - encurtado    -> `final_url` do expand_cache (a coluna existe; carrega_cache so le
                    o host, por isso lemos o cache direto aqui)

Uso: python diagnostico/blogs_em_portal.py
Saida: data/repl/compos2014/BLOGS_EM_PORTAL_candidatos.md
"""
import sqlite3, re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.midia_dominios import _norm_host, ENCURTADORES, ENCURTADOR_PARA_DOMINIO
from core.midia_mp_mc import classificar_host_mp_mc
from core.extrai_links import links_efetivos

DB = Path("data/repl/compos2014/snapshot_hashtag.sqlite")
CACHE_DB = Path("data/repl/compos2014/expand_cache.sqlite")
OUT = Path("data/repl/compos2014/BLOGS_EM_PORTAL_candidatos.md")
W = "data_brt >= '2014-10-13' AND data_brt < '2014-10-24'"
GEN = ENCURTADORES - set(ENCURTADOR_PARA_DOMINIO)
# branded (glo.bo, oesta.do, uol.com...): o host ja mapeia p/ a marca, mas o PATH e'
# codigo curto -> tambem precisa do cache. Expandidos por pipeline/expandir_branded.py.
BRANDED = set(ENCURTADOR_PARA_DOMINIO) | {"uol.com"}
TOP = 60

# marcadores genericos de blog/coluna (o que da p/ pegar por regra)
BLOG_RE = re.compile(r'(^|/)(blog|blogs|coluna|colunas|colunista|colunistas)(/|$)'
                     r'|(^|/)blog[-_]d[aeo][-_]'
                     r'|^//?blog\.', re.I)


def carrega_final_urls():
    """url_curta -> final_url (so status ok)."""
    con = sqlite3.connect(CACHE_DB)
    d = {}
    for url, fu, st in con.execute("SELECT url, final_url, status FROM expand"):
        if st == "ok" and fu:
            d[url] = fu
    con.close()
    return d


FINAL = carrega_final_urls()


def url_final_do_tweet(links):
    """Devolve a URL COMPLETA final do 1o link (ou None se nao der p/ saber)."""
    if not links:
        return None
    u = links[0]
    try:
        h = _norm_host(urlparse(u).netloc)
    except Exception:
        return None
    if h in GEN or h in BRANDED:
        return FINAL.get(u)          # encurtado (generico OU branded): precisa do cache
    return u                          # dominio direto: a propria URL ja tem o path


def prefixo(url, n=2):
    """host + primeiros n segmentos do path."""
    p = urlparse(url)
    host = _norm_host(p.netloc)
    segs = [s for s in p.path.split("/") if s][:n]
    return host, "/" + "/".join(segs) if segs else "/"


def main():
    con = sqlite3.connect(DB)
    cont = Counter()
    marcados = Counter()
    mp_total = 0
    sem_url = 0
    for links_json, texto in con.execute(f"SELECT links, texto FROM tweets WHERE {W}"):
        links = links_efetivos(links_json, texto)
        cl, _ = None, None
        url = url_final_do_tweet(links)
        if not url:
            continue
        host = _norm_host(urlparse(url).netloc)
        host = ENCURTADOR_PARA_DOMINIO.get(host, host)
        if classificar_host_mp_mc(host) != "MP":
            continue
        mp_total += 1
        h, pref = prefixo(url)
        cont[(h, pref)] += 1
        if BLOG_RE.search(urlparse(url).path or ""):
            marcados[(h, pref)] += 1
    con.close()

    pegos = sum(marcados.values())
    linhas = [
        "# Blog/coluna hospedado em domínio MP — candidatos a MC (janela 13–23/out)",
        "",
        f"> Gerado por `diagnostico/blogs_em_portal.py`. Tweets cujo 1º link cai num host "
        f"**MP** e tem URL completa visível: **{mp_total}**. O regex genérico "
        f"(`/blog`, `/coluna`…) pega **{pegos}** ({100*pegos/mp_total if mp_total else 0:.1f}%) — "
        f"mas ele NÃO pega colunista nomeado sem marcador (ex.: "
        f"`oglobo.globo.com/economia/miriam-leitao/`). Por isso a lista abaixo é de "
        f"**prefixos de seção** para curadoria: marcar quais são blog/coluna (→ MC) vs "
        f"editoria de notícia (→ fica MP).",
        "",
        "| # | host | prefixo | tweets | regex pegou? | é blog/coluna? (marcar) |",
        "|--:|---|---|--:|:--:|:--:|",
    ]
    for i, ((h, pref), c) in enumerate(cont.most_common(TOP), 1):
        pego = "sim" if marcados.get((h, pref)) else ""
        linhas.append(f"| {i} | {h} | `{pref}` | {c} | {pego} | |")
    OUT.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    print(f"tweets com 1o link em host MP e URL visivel: {mp_total}")
    print(f"  regex generico de blog/coluna pegou: {pegos}  ({100*pegos/mp_total if mp_total else 0:.1f}%)")
    print(f"  prefixos distintos: {len(cont)}   -> top {TOP} em {OUT}")
    print(f"\ntop 30 prefixos de secao nos hosts MP (marcados com * = regex pegou):")
    for (h, pref), c in cont.most_common(30):
        star = "*" if marcados.get((h, pref)) else " "
        print(f" {star} {h:<26}{pref:<34}{c:>5}")


if __name__ == "__main__":
    main()
