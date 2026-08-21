"""
Dicionario MP (Midia Principal) / MC (Midia Complementar) do paper de 2018
(Ituassu, Lifschitz, Capone, Vaz & Mannheimer — Palabra Clave 21(3)).

>>> CONVENCAO ESTRITA (decisao do usuario: "seguir exatamente como esta"). <<<

Regra do 2018 (p.871-872): MP = LISTA FECHADA das "26 grandes midias" mais
lembradas na Pesquisa Brasileira de Midia 2014. Tudo o mais que for midia = MC
(o paper catalogou "mais de 100 midias"), INCLUSIVE as redes sociais
("social media as complementary media"). Sem link => NDA. So o 1o link conta.

Ao pe da letra:
  - O texto diz "26" mas so NOMEIA 25 marcas -> usamos as 25 nomeadas e NAO
    inventamos a 26a (registrado como lacuna do paper).
  - Veiculos mainstream que NAO estao na lista das 26 (Valor, A Tarde,
    CartaCapital, BBC, WSJ...) caem em MC, mesmo aparecendo no topo das tabelas
    do proprio 2018. E o que a regra fechada manda.

Construcao (crosswalk auditavel): partimos do dicionario MV/MH ja vetado
(core.midia_dominios) e RE-BUCKETAMOS:
  MP = dominios das 25 marcas nomeadas
  MC = (MV_antigo  ∪  MH_antigo)  −  MP     (+ marcas MP novas que faltavam em MV)
Assim nada de cobertura se perde; so muda o rotulo. Ver PAPER2018_palabra_clave.md.
"""
import re
from urllib.parse import urlparse

from core.midia_dominios import (
    MV as _MV, MH as _MH,
    ENCURTADORES, ENCURTADOR_PARA_DOMINIO, _norm_host,
)

# ---------------------------------------------------------------------------
# MP — as 25 marcas NOMEADAS no 2018 (p.871-872), mapeadas para dominio(s).
# Uma marca -> seu(s) dominio(s) web. Comentario = marca do paper.
# ---------------------------------------------------------------------------
MP_POR_MARCA = {
    "Rede Bandeirantes": {"band.com.br", "band.uol.com.br", "noticias.band.uol.com.br",
                          "bandeirantes820.com.br"},  # radio AM do Grupo Band (decisao do usuario: MP)
    "Diario Gaucho":     {"diariogaucho.com.br"},
    "Epoca":             {"epoca.globo.com", "epoca.abril.com.br"},
    "O Estado de S.Paulo (Estadao)": {"estadao.com.br", "politica.estadao.com.br",
                                      "economia.estadao.com.br", "oesta.do"},
    "Extra":             {"extra.globo.com"},
    "Folha de S.Paulo":  {"folha.uol.com.br", "www1.folha.uol.com.br", "folha.com", "folha.com.br"},
    "Rede Globo":        {"globo.com", "redeglobo.globo.com", "g1.globo.com", "g1.com.br"},
    "O Globo":           {"oglobo.globo.com", "oglobo.com.br"},
    "Globo.com":         {"globo.com"},
    "Hoje em Dia (R7)":  {"hojeemdia.com.br"},
    "iG":                {"ig.com.br", "ultimosegundo.ig.com.br", "zip.net"},
    "IstoE":             {"istoe.com.br"},
    "Jornal do Brasil":  {"jb.com.br"},
    "Meia Hora":         {"meiahora.com", "meiahoraonline.com"},
    "O Dia":             {"odia.ig.com.br", "odia.com.br"},
    "O Povo":            {"opovo.com.br"},
    "R7 (portal)":       {"r7.com", "noticias.r7.com"},
    "Rede Record":       {"recordtv.r7.com", "rederecord.r7.com"},
    "Rede SBT":          {"sbt.com.br"},
    "Super Noticia":     {"supernoticia.com.br"},
    "Terra (portal)":    {"terra.com.br", "noticias.terra.com.br"},
    "UOL (portal)":      {"uol.com.br", "noticias.uol.com.br", "bol.uol.com.br",
                          "uol.com", "tvuol.tv"},
    "Veja":              {"veja.abril.com.br", "veja.com"},
    "Yahoo":             {"yahoo.com", "br.yahoo.com", "yahoo.com.br"},
    "Zero Hora":         {"zerohora.com.br", "zh.clicrbs.com.br", "gauchazh.clicrbs.com.br"},
}
# nota: o G1 e o portal de noticias da Globo -> agrupado sob "Rede Globo"/"Globo.com".
#       "Rede Record" na web = portal R7; mantido separado de "R7 (portal)" so p/ auditoria.

MP = set().union(*MP_POR_MARCA.values())

# ---------------------------------------------------------------------------
# MC_EXTRA — dominios curados da revisao dos `indefinido` (jul/2026, com o usuario).
# Midia complementar de verdade que aparecia como link mas faltava no dicionario.
# (★ = confirmados na Tabela 6 do proprio paper 2018.)
# ---------------------------------------------------------------------------
MC_EXTRA = {
    # news alternativo / regional / revistas fora das 26
    "gospelprime.com.br", "elpais.com", "geledes.org.br", "gentedeopiniao.com.br",
    "redebrasilatual.com.br", "jornalnh.com.br", "diariosp.com.br", "tvtnews.com.br",
    "revistaforum.com.br", "emtempo.com.br", "folhapolitica.org", "apublica.org",
    "minassemcensura.com.br", "portaltucuma.com.br", "sganoticias.com.br",
    "jornalggn.com.br", "otempo.com.br", "diariodocentrodomundo.com.br",
    "implicante.org", "redecomsc.com.br", "anonymousbr4sil.net",
    # blogs pessoais / de opiniao
    "rogeriocerqueiraleite.com.br", "blogdaboitempo.com.br", "blogdecaucaia.com",
    "kikacastro.com.br", "marcogomes.com",
    "conversaafiada.com.br",       # ★ Tab.6 (ED)
    "pragmatismopolitico.com.br",  # ★ Tab.6 (ED)
    "olavodecarvalho.org",         # ★ Tab.6 (EA)
    "blogdoeveraldo.com.br",       # ★ Tab.6 (EA)
    # redes sociais (resolvem p/ plataforma)
    "x.com", "plus.google.com", "twishort.com",
    # campanha/candidato (decisao do usuario: MC, como o paper conta material de militancia)
    "aecioneves.com.br", "mudamais.com",
    # nicho religioso (decisao do usuario: MC)
    "adventistas.org",
}

# ---------------------------------------------------------------------------
# NAO_MIDIA — link identificado que NAO e veiculo de midia: sai da base (nem MP
# nem MC). Governo/Estado (decisao do usuario: excluir), lixo, ferramentas.
# Efeito: tweet vira "sem compartilhamento de midia" (fora da Amostra C), igual NDA.
# ---------------------------------------------------------------------------
NAO_MIDIA = {
    # governo / Estado (decisao do usuario)
    "camara.leg.br", "senado.leg.br", "tse.jus.br", "mpf.mp.br", "amb.com.br",
    # lixo / estacionado / ferramentas / desconhecido
    "sedo.com", "messagepresident.com", "feedly.com", "portaldaabelhinha.com.br",
    "boqnews.tk", "appnion.com.br", "voceaki.com", "bdbrasil.org",
}

# ---------------------------------------------------------------------------
# MC — crosswalk (MV∪MH)−MP, mais os curados, menos o que virou nao-midia.
# ---------------------------------------------------------------------------
MC = ((_MV | _MH) - MP | MC_EXTRA) - NAO_MIDIA

# dominios que ficam FORA das 26 e viram MC — explicito para a auditoria/relatorio
MAINSTREAM_REBAIXADA_PARA_MC = sorted(d for d in _MV if d not in MP)


def classificar_host_mp_mc(host: str) -> str:
    """Retorna 'MP', 'MC', 'encurtador' ou 'indefinido' para um host.

    Espelha core.midia_dominios.classificar_host, trocando o alvo MV/MH por MP/MC.
    Dominio real fora do dicionario => 'indefinido' (NAO vira MC automaticamente:
    mantemos o residuo visivel para curadoria, em vez de inflar a MC com ruido —
    ver ressalva em PAPER2018_palabra_clave.md §7).
    """
    h = _norm_host(host)
    if not h:
        return "indefinido"
    if h in ENCURTADOR_PARA_DOMINIO:
        h = ENCURTADOR_PARA_DOMINIO[h]
    if h in ENCURTADORES:
        return "encurtador"
    for dom in NAO_MIDIA:
        if h == dom or h.endswith("." + dom):
            return "nao_midia"
    for dom in MP:
        if h == dom or h.endswith("." + dom):
            return "MP"
    for dom in MC:
        if h == dom or h.endswith("." + dom):
            return "MC"
    return "indefinido"


# ---------------------------------------------------------------------------
# BLOG/COLUNA hospedado em dominio MP  ->  o paper de 2018 codifica como MC.
#
# Evidencia: a Tab. 6 do paper lista como MIDIA COMPLEMENTAR blogs que moram em
# dominios MP — "Blog do Reinaldo Azevedo (Veja)", "Blog da Miriam Leitao (O Globo)",
# "Blog do Noblat (O Globo)", "Blog Julia Duailibi (Estadao)", "Blog da Laura
# Capriglione (Yahoo)". A Tab. 4 lista "Jornalismo Wando" (Yahoo). Nossa regra de
# HOST chamava tudo isso de MP. Classificar pelo PATH corrige.
#
# So funciona com a URL FINAL (o path de um encurtador e' codigo curto) — por isso
# `pipeline/expandir_branded.py` expande glo.bo/uol.com/oesta.do. Quando o encurtador
# esta morto o path fica invisivel e o tweet permanece MP (subcontagem conhecida).
# Curadoria aberta em `data/repl/compos2014/BLOGS_EM_PORTAL_candidatos.md`.
# ---------------------------------------------------------------------------
_BLOG_PATH_RE = re.compile(
    r'(^|/)(blogs?|colunas?|colunistas?)(/|$)'      # /blog/ /blogs/ /coluna/ /colunas/
    r'|(^|/)blog[-_]d[aeo][-_]',                    # /blog-do-fausto-macedo/
    re.I)
_BLOG_HOST_RE = re.compile(r'(^|\.)blogs?\.|blogfolha', re.I)  # blog.estadao / blogfolha.uol

# colunistas/blogs nomeados SEM marcador no path (evidenciados na Tab. 6 do paper)
_COLUNISTAS_SEM_MARCADOR = (
    "miriam-leitao",   # oglobo.globo.com/economia/miriam-leitao/
    "noblat",          # oglobo.globo.com/brasil/noblat/
)


def eh_blog_ou_coluna(url: str) -> bool:
    """True se a URL (FINAL) aponta para blog/coluna, mesmo em dominio MP."""
    if not url:
        return False
    try:
        p = urlparse(url)
    except Exception:
        return False
    host = _norm_host(p.netloc)
    path = p.path or ""
    if _BLOG_HOST_RE.search(host):
        return True
    if _BLOG_PATH_RE.search(path):
        return True
    return any(c in path.lower() for c in _COLUNISTAS_SEM_MARCADOR)


def classificar_url_mp_mc(url: str) -> str:
    """Classifica pela URL COMPLETA: host define MP/MC/nao_midia; o path pode
    REBAIXAR MP -> MC quando for blog/coluna hospedado no portal (Tab. 6 do paper).

    Passe sempre a URL **final** (pos-expansao). Para classificar so pelo host, use
    `classificar_host_mp_mc`.
    """
    try:
        host = _norm_host(urlparse(url).netloc)
    except Exception:
        return "indefinido"
    cl = classificar_host_mp_mc(host)
    if cl == "MP" and eh_blog_ou_coluna(url):
        return "MC"
    return cl


if __name__ == "__main__":
    print(f"MP: {len(MP_POR_MARCA)} marcas nomeadas, {len(MP)} dominios")
    print(f"MC: {len(MC)} dominios (crosswalk (MV∪MH)−MP)")
    print(f"mainstream rebaixada p/ MC (fora das 26): {MAINSTREAM_REBAIXADA_PARA_MC}")
    for t in ["g1.globo.com", "www.folha.uol.com.br", "valor.com.br", "atarde.com.br",
              "cartacapital.com.br", "bbc.com", "facebook.com", "brasil247.com",
              "reinaldoazevedo.com.br", "oesta.do", "t.co", "desconhecido.xyz"]:
        print(f"  {t:<28} -> {classificar_host_mp_mc(t)}")
