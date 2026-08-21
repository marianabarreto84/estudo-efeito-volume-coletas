"""
Dicionario de classificacao de midia MV (vertical) / MH (horizontal),
reconstruido do paper Ituassu & Lifschitz (2015), secao 4 e Tabelas 3-4.

Regra do paper: olha-se APENAS o 1o link do tweet; classifica-se o dominio como
MV (grande midia, fluxo de cima p/ baixo) ou MH (nicho/individual/redes sociais).
Tweets sem link => NDA (nenhuma midia).

ATENCAO (decisao pendente §6.1): o paper lista exemplos, nao a tabela completa.
Este dicionario e uma reconstrucao explicita e versionada. Dominios nao listados
caem em 'indefinido' e devem ser revisados/expandidos ao rodar sobre o universo.
"""

# --- Midia Vertical (MV): grande midia / mainstream ---
# Citados no texto (§4) + Tabela 3 (dominios efetivamente retweetados).
MV = {
    # Portais/sistemas Globo
    "g1.globo.com", "g1.com.br", "globo.com", "oglobo.globo.com", "oglobo.com.br",
    "extra.globo.com", "epoca.globo.com", "valor.com.br", "valoreconomico.com.br",
    # Estadao
    "estadao.com.br", "politica.estadao.com.br", "economia.estadao.com.br",
    "oesta.do",  # encurtador oficial do Estadao
    # Folha (grupo)
    "folha.uol.com.br", "www1.folha.uol.com.br", "folha.com", "folha.com.br",
    # UOL / BOL  (uol.com == uol.com.br; tvuol e o video do UOL)
    "uol.com.br", "noticias.uol.com.br", "bol.uol.com.br", "uol.com", "tvuol.tv",
    # Outros jornais de grande circulacao (regionais de peso) e internacionais
    "jb.com.br",          # Jornal do Brasil
    "atarde.com.br",      # A Tarde (BA)
    "terranews.com.br",   # Terra
    "wsj.com", "on.wsj.com",
    "ig.com.br", "zip.net",  # portal iG
    # Revistas mainstream
    "veja.abril.com.br", "veja.com", "abril.com.br", "istoe.com.br", "cartacapital.com.br",
    # Outras grandes / agregadores citados
    "terra.com.br", "noticias.terra.com.br", "br.yahoo.com", "yahoo.com",
    "band.com.br", "noticias.band.uol.com.br", "r7.com",
    "odia.ig.com.br", "odia.com.br",  # O Dia (aparece na Tab.3 do lado ED)
    "bbc.com", "bbc.co.uk",  # BBC Brasil (grande midia internacional) - revisar
}

# --- Midia Horizontal (MH): nicho / individual / blogs / redes sociais ---
# Citados no texto (§4) + Tabela 4 (blogs/agencias efetivamente retweetados).
MH = {
    # Redes sociais (quando usadas por individuos/orgs nao-verticais)
    "facebook.com", "m.facebook.com", "fb.com",
    "youtube.com", "youtu.be", "m.youtube.com",
    "instagram.com", "twitter.com", "twitpic.com", "vine.co", "tumblr.com",
    # Sites/blogs de nicho citados no texto
    "brasildefato.com.br", "catracalivre.com.br", "brasildagente.com.br",
    "brasilwire.com", "humbertotobe.com.br",  # blogs de nicho (top indefinido)
    "congressoemfoco.uol.com.br", "congressoemfoco.com.br",
    "jornalistasdeminas.com.br", "folhademaringa.com.br",
    # Tabela 4 (EA)
    "agoraaporetica.blogspot.com", "diariodopoder.com.br",
    "reinaldoazevedo.com.br",  # Blog do Reinaldo Azevedo (Veja) - nota: caso limitrofe
    "brasilindignado.com.br", "revistabzzz.com.br",
    # Tabela 4 (ED)
    "jcm.com.br", "blogdojosiasdesouza.com",  # revisar mapeamentos
    "brasilpost.com.br", "huffpostbrasil.com",
    # blog 247 / brasil 247
    "brasil247.com", "www.brasil247.com",
    # Agencia Brasil (agencia publica) - aparece nos dois lados da Tab.4
    "agenciabrasil.ebc.com.br", "memoria.ebc.com.br",
    # blogosfera generica
    "blogspot.com", "blogspot.com.br", "wordpress.com",
}

# Encurtadores comuns (2014). NAO sao midia; precisam ser expandidos antes de
# classificar. Mapeados aqui so para deteccao (o valor indica se ha como expandir).
ENCURTADORES = {
    "t.co", "bit.ly", "goo.gl", "ow.ly", "dlvr.it", "ift.tt", "fb.me",
    "abr.ai", "oesta.do", "glo.bo", "migre.me", "tinyurl.com", "is.gd",
    "buff.ly", "wp.me", "youtu.be",
    # genericos adicionais vistos no 'indefinido' do universo
    "ln.is", "bitly.com", "zhora.co", "naofo.de", "likedeck.tk", "j.mp",
    # encurtadores vistos na revisao dos indefinidos (jul/2026) — mandar p/ expansao
    "scup.it", "svmar.es", "clic.sc", "klou.tt", "twixar.me", "flwcs.co",
    "leiaja.me", "casseta.me",
}
# obs: alguns encurtadores sao "proprios" de um veiculo e ja indicam o dominio:
#   oesta.do -> Estadao (MV) ; glo.bo -> Globo (MV) ; abr.ai -> ? (verificar)
ENCURTADOR_PARA_DOMINIO = {
    "oesta.do": "estadao.com.br",   # MV
    "glo.bo": "globo.com",          # MV
    "fb.me": "facebook.com",        # MH
    "youtu.be": "youtube.com",      # MH
    "bbc.in": "bbc.com",            # MV (encurtador oficial BBC)
    "on.wsj.com": "wsj.com",        # MV
    "huff.to": "huffpostbrasil.com",# MH (HuffPost/Brasil Post)
    "tmblr.co": "tumblr.com",       # MH
    "ebcnare.de": "agenciabrasil.ebc.com.br",  # MH/publica (EBC/Agencia Brasil)
    "swarmapp.com": "instagram.com",# MH (check-in social; trata como social)
    "on.fb.me": "facebook.com",     # encurtador oficial do Facebook -> social (MC)
}


def _norm_host(host: str) -> str:
    host = (host or "").strip().lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def classificar_host(host: str) -> str:
    """Retorna 'MV', 'MH', 'encurtador' ou 'indefinido' para um host."""
    h = _norm_host(host)
    if not h:
        return "indefinido"
    if h in ENCURTADOR_PARA_DOMINIO:
        h = ENCURTADOR_PARA_DOMINIO[h]
    if h in ENCURTADORES:
        return "encurtador"
    # match por sufixo de dominio (cobre subdominios nao listados)
    for dom in MV:
        if h == dom or h.endswith("." + dom):
            return "MV"
    for dom in MH:
        if h == dom or h.endswith("." + dom):
            return "MH"
    return "indefinido"


if __name__ == "__main__":
    testes = ["g1.globo.com", "www.folha.uol.com.br", "oesta.do", "t.co",
              "facebook.com", "brasil247.com", "exemplo-desconhecido.com"]
    for t in testes:
        print(f"  {t:<30} -> {classificar_host(t)}")
