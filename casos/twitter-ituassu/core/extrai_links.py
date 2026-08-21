"""
Extracao do "1o link efetivo" de um tweet.

Motivo (achado jul/2026): ~9% dos tweets da janela tem o campo estruturado `links`
VAZIO mas uma URL (quase sempre t.co) EMBUTIDA NO TEXTO — tipico de retweets
nativos de 2014. A analise de midia do paper olha "o link" da mensagem; para nao
perder esses, quando o campo `links` esta vazio caimos para a 1a URL do texto.

links_efetivos(links_json, texto) -> lista de URLs (campo links; senao, do texto).
So o 1o elemento importa para a classificacao (regra do paper: 1o link).
"""
import json
import re

# '…' = reticencias (…) com que tweets de 2014 truncados a 140 chars terminam;
# nao faz parte da URL. Excluida da captura e removida da cauda.
_URL_RE = re.compile(r'https?://[^\s<>"\')…]+', re.IGNORECASE)


def extrai_urls_texto(texto: str):
    """URLs http(s) no texto, na ordem de aparicao (sem pontuacao/reticencias na cauda)."""
    if not texto:
        return []
    out = []
    for m in _URL_RE.findall(texto):
        u = m.rstrip('.,;:!?)…')
        # descarta fragmentos obviamente truncados (so o host, sem path util)
        if len(u) > len("https://a.bc"):
            out.append(u)
    return out


def links_efetivos(links_json, texto):
    """Campo `links` se houver; senao, URLs extraidas do texto. Devolve lista."""
    try:
        links = json.loads(links_json) if links_json else []
    except Exception:
        links = []
    if links:
        return links
    return extrai_urls_texto(texto)
