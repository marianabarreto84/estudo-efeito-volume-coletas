"""
Eixo MP/MC — curadoria do residuo `indefinido` (dominio real fora do dicionario).

Contexto: `analisa_midia_mp_mc.py` deixa em `indefinido` todo host que nao esta no
dicionario MP/MC. Sao 2.082 tweets / 692 hosts no snapshot inteiro (515 tweets na
janela 13-23/out do paper de 2018). Este script os classifica por REGRA auditavel e
grava o resultado em `indefinidos_curados.csv`, para inspecao e para uso pelo
script de sensibilidade.

Regra de curadoria (nesta ordem)
--------------------------------
  1. ENCURTADOR nao expandido (yhoo.it, flip.it, on-msn.com, clic.rs, ur1.ca...)
     -> `nao_resolvido`. Nao e "dominio desconhecido", e link que nao resolveu.
  2. NAO-MIDIA — plataforma (soundcloud, vimeo, play.google), institucional
     (.gov.br, .leg.br, .jus.br, senado, camara, assembleia), ONG/ativismo
     (.org/.org.br sem redacao), dominio a venda/parking (hugedomains).
  3. Todo o resto que seja veiculo jornalistico -> **MC**, porque sob a convencao
     ESTRITA do paper de 2018 MP e uma lista fechada de 26 marcas; nada fora dela
     pode virar MP. Isso vale inclusive para mainstream (Gazeta do Povo, Zero Hora,
     Correio Braziliense, Estado de Minas) e para midia internacional (Guardian,
     ABC.es, DW, AP).

⚠ Consequencia esperada: curar o residuo **aumenta MC** e portanto **reduz MP%**,
aproximando do 59% do paper. O script de sensibilidade mede o quanto.

Uso: PYTHONIOENCODING=utf-8 python -u analise/cura_indefinidos.py
Saida: data/repl/compos2014/indefinidos_curados.csv (host, n_tweets, classe, motivo)
"""
import csv
import pathlib
import re
import sqlite3
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.extrai_links import links_efetivos
from core.resolve_mp_mc import classe_mp_mc_do_primeiro_link, carrega_cache_mp_mc

D = pathlib.Path("data/repl/compos2014")
OUT_CSV = D / "indefinidos_curados.csv"
CACHE = carrega_cache_mp_mc(D / "expand_cache.sqlite")

# 1. encurtadores que sobraram sem expansao
ENCURTADORES_RESIDUAIS = {
    "yhoo.it", "on-msn.com", "clic.rs", "l1nks.co", "flip.it", "ur1.ca", "4sq.com",
    "jp86.co.vu", "je.inf.br", "migre.me", "tinyurl.com", "dlvr.it", "ift.tt",
    "wp.me", "shar.es", "sns.mx", "trib.al", "buff.ly", "amzn.to", "nyti.ms",
    "gu.com", "huff.to", "reut.rs", "cnn.it", "bbc.in", "econ.st", "read.bi",
    "spoti.fi", "goo.gl", "tinyurl.it", "ow.ly", "j.mp", "youtu.be",
}
RX_ENCURTADOR = re.compile(
    r"^([a-z0-9-]{1,7}\.(it|ly|me|gl|co|gs|st|to|ms|rs|in|is|us|ca|cc|tt|al|be))$")

# 2. nao-midia
RX_INSTITUCIONAL = re.compile(
    r"(\.gov\.br$|\.gov$|\.leg\.br$|\.jus\.br$|\.mp\.br$|senado|camara\.|"
    r"\.al\.[a-z]{2}\.gov|assembleia|tse\.|tre-|planalto|prefeitura)")
PLATAFORMAS = {
    "soundcloud.com", "vimeo.com", "play.google.com", "docs.google.com",
    "drive.google.com", "hugedomains.com", "instagram.com", "pinterest.com",
    "linkedin.com", "slideshare.net", "scribd.com", "issuu.com", "flickr.com",
    "tumblr.com", "ask.fm", "change.org", "avaaz.org", "peticaopublica.com.br",
    "wikipedia.org", "pt.wikipedia.org", "en.wikipedia.org", "amazon.com.br",
    "mercadolivre.com.br", "spotify.com", "itunes.apple.com", "apple.com",
    "paypal.com", "eventbrite.com.br", "doodle.com", "surveymonkey.com",
}
RX_ONG = re.compile(r"(\.org$|\.org\.br$)")
# Excecao explicita: veiculos JORNALISTICOS hospedados em .org, que a regra do
# .org classificaria erradamente como ONG. Lista curada a mao, auditavel.
JORNALISMO_EM_ORG = {
    "ponte.org",            # Ponte Jornalismo
    "vermelho.org.br",      # Portal Vermelho
    "rioonwatch.org.br",    # RioOnWatch (jornalismo comunitario)
    "diarioliberdade.org",  # Diario Liberdade
    "ler-qi.org",           # Esquerda Diario
    "opendemocracy.net",
    "propublica.org",
    "intercept.org",
}


def log(m):
    print(m, flush=True)


def cura(host):
    """Devolve (classe, motivo)."""
    if not host:
        return "nao_resolvido", "host vazio"
    h = host.lower()
    if h in ENCURTADORES_RESIDUAIS or RX_ENCURTADOR.match(h):
        return "nao_resolvido", "encurtador nao expandido"
    if h in PLATAFORMAS or any(h.endswith("." + p) for p in PLATAFORMAS):
        return "nao_midia", "plataforma / servico"
    if RX_INSTITUCIONAL.search(h):
        return "nao_midia", "institucional / governo"
    if RX_ONG.search(h) and h not in JORNALISMO_EM_ORG:
        return "nao_midia", "ONG / ativismo (.org)"
    # regra 3: veiculo fora das 26 -> MC sob a convencao estrita
    return "MC", "midia fora da lista fechada das 26 (convencao estrita)"


def main():
    log("== 1. Levantando hosts em `indefinido` ==")
    con = sqlite3.connect(D / "snapshot_hashtag.sqlite")
    con.row_factory = sqlite3.Row
    hosts = Counter()
    for r in con.execute("SELECT links, texto FROM tweets"):
        c, host = classe_mp_mc_do_primeiro_link(
            links_efetivos(r["links"], r["texto"]), CACHE)
        if c == "indefinido":
            hosts[host] += 1
    con.close()
    total = sum(hosts.values())
    log(f"   {total:,} tweets · {len(hosts)} hosts distintos")

    log("\n== 2. Curando por regra ==")
    linhas = []
    agg = Counter()
    agg_tw = Counter()
    for h, n in hosts.most_common():
        cl, motivo = cura(h)
        linhas.append({"host": h, "n_tweets": n, "classe": cl, "motivo": motivo})
        agg[cl] += 1
        agg_tw[cl] += n
    for cl in ("MC", "nao_midia", "nao_resolvido"):
        log(f"   {cl:<15} {agg[cl]:>4} hosts · {agg_tw[cl]:>5,} tweets "
            f"({100*agg_tw[cl]/total:>5.1f}%)")

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["host", "n_tweets", "classe", "motivo"])
        w.writeheader()
        w.writerows(linhas)
    log(f"\n   -> {OUT_CSV.name} ({len(linhas)} linhas, auditavel)")

    log("\n== 3. Amostra do que virou o quê (top 12 de cada classe) ==")
    for cl in ("MC", "nao_midia", "nao_resolvido"):
        ex = [l for l in linhas if l["classe"] == cl][:12]
        log(f"   {cl}: " + ", ".join(f"{l['host']}({l['n_tweets']})" for l in ex))


if __name__ == "__main__":
    main()
