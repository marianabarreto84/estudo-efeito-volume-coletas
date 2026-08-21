"""
As duas regras de método que o artigo AGECovP **não publica**, definidas aqui.

Por que existem
---------------
1. `no_tema()` — a Fase 3 parcial mostrou que o conjunto descartado pelo filtro traz
   conteudo genuinamente FORA do tema (Sport, Baseball). Comparar "com filtro" x
   "sem filtro" sem separar isso mede ruido, nao vies. Entao precisamos de um teste
   de tema **independente** da regra de filtro do artigo.

2. `eh_ugc()` — o alvo-teste AG3 do artigo ("UGC representa menos de 7%") nao vem
   com regra publicada nem com coluna no gabarito. Sem uma regra, AG3 nao e
   testavel; com uma regra DECLARADA (nao ajustada ao resultado), e — e o veredito
   que ela produz e "nao reproduz". Ver o bloco de limiar abaixo.

Princípio comum: a regra e aplicada **identicamente** aos dois lados da comparacao
(o que passa e o que nao passa no filtro). Assim, mesmo que o valor absoluto divirja
do artigo, a COMPARACAO — que e o que a tese mede — continua valida.

Limiar do `eh_ugc` — decidido, NAO calibrado
--------------------------------------------
A intencao inicial era ajustar o limiar de inscritos ate reproduzir o "<7%" do
artigo. A medicao mostrou que isso exigiria definir UGC como "canal com menos de
~50 inscritos" — indefensavel. Decisao: limiar **declarado em 10.000**, com a
sensibilidade reportada ao lado, e AG3 registrado como **nao reproduz** (32,0% x
"<7%"). Detalhe e justificativa em
`data/repl/agecovp2020/DECISOES_regras.md` §D2.

O que a Fase 3 mede e a DIFERENCA entre os dois lados do filtro sob a mesma regra;
essa diferenca nao depende de onde o limiar esta.
"""
import re
import unicodedata

# --- termos de tema, das duas listas do artigo (Tabela 1) -------------------
IDOSOS = ["ageism", "ageist", "elderly", "older", "boomer", "senior", "aging",
          "ageing", "later life", "age-related", "retiree", "retired", "elders",
          "geriatric", "grandparent", "grandmother", "grandfather", "old people",
          "nursing home", "care home", "pensioner", "old age"]
COVID = ["covid", "coronavirus", "corona virus", "pandemic", "sars-cov", "lockdown",
         "quarantine", "vaccine", "vaccination"]

# --- marcadores de veiculo de imprensa / canal institucional ----------------
MARCADORES_IMPRENSA = [
    "news", "tv", "times", "post", "herald", "tribune", "journal", "media", "press",
    "radio", "broadcast", "network", "daily", "report", "bbc", "cnn", "abc", "nbc",
    "cbs", "fox", "sky", "reuters", "guardian", "telegraph", "wion", "ndtv",
    "aljazeera", "al jazeera", "euronews", "channel", "today", "live", "official",
    "magazine", "bulletin", "gov", "ministry", "health service", "university",
    "hospital", "clinic", "association", "foundation", "institute",
]


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def _tem(campo, termos):
    return any(re.search(r"\b" + re.escape(t), campo) for t in termos)


def no_tema(titulo, descricao, tags=""):
    """
    Teste de tema, CONJUNTIVO e independente da regra do artigo:
    o texto precisa mencionar **idosos** E **covid/pandemia**.

    Por que conjuntivo: o objeto do estudo e a interseccao "idosos x pandemia".
    Video de beisebol nao menciona nenhum dos dois; video de covid sem idosos, ou
    de idosos sem covid, esta fora do objeto declarado do artigo.

    Por que independente: se usasse os mesmos termos de busca, seria circular —
    reprovaria por construcao tudo o que o filtro do artigo reprova.
    """
    campo = norm(titulo) + " " + norm(descricao) + " " + norm(tags)
    return bool(_tem(campo, IDOSOS) and _tem(campo, COVID))


LIMIAR_INSCRITOS = 10000     # declarado (ver DECISOES_regras.md D2), nao calibrado


def eh_ugc(titulo_canal, inscritos, limiar_inscritos=LIMIAR_INSCRITOS):
    """
    UGC (conteudo de usuario) x canal institucional/imprensa.

    Institucional se: o titulo do canal traz marcador de imprensa/instituicao
    **ou** o canal tem inscritos >= limiar. UGC caso contrario.

    Os dois criterios sao necessarios: ha veiculo pequeno (jornal local) que o
    limiar nao pega, e ha criador individual enorme que o marcador nao pega.
    """
    t = norm(titulo_canal)
    if _tem(t, MARCADORES_IMPRENSA):
        return False
    try:
        n = int(float(inscritos))
    except (TypeError, ValueError):
        n = 0
    return n < limiar_inscritos
