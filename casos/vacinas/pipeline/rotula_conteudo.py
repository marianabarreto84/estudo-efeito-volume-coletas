"""
Eixo B / passo 3 — Rotulador de conteudo (stance + 14 categorias) via LLM.

Opcao A do EIXO_CONTEUDO.md: Claude Haiku 4.5 pinado, temperatura 0, Batch API
(-50%), prompt versionado, saida JSON estruturada, requests e respostas brutas
salvas em disco. O que legitima o rotulador nao e o modelo — e o kappa contra o
gabarito humano, medido no TESTE CEGO congelado por congela_split.py.

TETO DE GASTO: nenhum lote e enviado sem passar por core/orcamento.Orcamento.
A reserva usa o PIOR CASO (saida inteira em max_tokens), entao o gasto real
fica sempre abaixo do reservado. Ver o cabecalho de core/orcamento.py.

Uso:
    # 1. quanto custaria, sem gastar nada:
    python -u pipeline/rotula_conteudo.py --conjunto dev --dry-run

    # 2. calibracao (pode olhar o resultado e mexer no prompt):
    python -u pipeline/rotula_conteudo.py --conjunto dev

    # 3. teste cego (uma vez so, com o prompt ja congelado):
    python -u pipeline/rotula_conteudo.py --conjunto teste

Saida: data/repl/vacinas2022/rotulos_llm/<conjunto>_<prompt>/
  - pedidos.jsonl / respostas.jsonl  (bruto, para auditoria)
  - rotulos.csv                      (ID, stance, cat_1..cat_14)
  - execucao.json                    (modelo, prompt, custo, uso de tokens)
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
import time
from collections import Counter

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.llm import cliente, MODELO_PADRAO
from core.orcamento import Orcamento, OrcamentoEstourado, custo_usd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
DADOS = RAIZ / "data" / "repl" / "vacinas2022"
XLSX = DADOS / "suplementar_rotulos.xlsx"
CODEBOOK = DADOS / "codebook_v1.json"
SPLIT = DADOS / "split_dev_teste.csv"
SAIDA = DADOS / "rotulos_llm"
SNAPSHOT = DADOS / "snapshot_vacinas.sqlite"

# Saida por tweet: stance + numeros das categorias. Numeros em vez de 14
# booleanos porque a saida e o token caro (5x a entrada) — e o formato nao
# muda a tarefa.
MAX_TOKENS_POR_TWEET = 60
MARGEM_SEGURANCA = 1.25  # a reserva assume 25% a mais que o pior caso medido


def _humaniza(coluna):
    """`About_AstraZenecaOxford_L7` -> `AstraZenecaOxford`."""
    t = re.sub(r"_(L|A)\d+$", "", coluna)
    t = re.sub(r"^(About_|All_|ALL_)", "", t)
    return re.sub(r"\s+", " ", t.replace("_", " ")).strip()


def rotulos_da_categoria(c, maximo=14):
    """
    Lista curta e informativa do que a categoria abrange, para o prompt.

    O suplemento nem sempre poe a informacao no mesmo lugar: em "Restrictive
    policies" ela esta no nome refinado, mas em "International" (35 paises) e
    "Vaccines type or laboratories" (11 laboratorios) os nomes refinados
    colidem ("About countries other than Brazil", "Vaccine labs") e quem
    distingue e o nome da coluna. Detectamos o caso pela colisao.
    """
    subs = [s for s in c["subcategorias"] if s["coluna"] != c["coluna"]]
    refinadas = [s["refinada"] for s in subs
                 if not s["refinada"].lower().startswith("all ")]
    distintas = list(dict.fromkeys(refinadas))

    if subs and len(distintas) <= 3 and len(subs) >= 5:
        brutos = [_humaniza(s["coluna"]) for s in subs]
    else:
        brutos = distintas

    rotulos = [r for r in dict.fromkeys(brutos)
               if r.lower() != c["nome_en"].lower()]
    if len(rotulos) > maximo:
        return rotulos[:maximo] + ["entre outros"]
    return rotulos


# Notas de fronteira acrescentadas na p2. Cada uma responde a um erro medido
# no dev com a p1 — a justificativa completa esta em DECISOES_ROTULADOR.md.
# Sao esclarecimentos de DEFINICAO, nunca dicas de frequencia: informar ao
# modelo a taxa-base de cada categoria cozinharia a distribuicao do estrato
# >500 RT dentro do rotulador, e o E1 existe justamente para descer a outro
# estrato onde essa distribuicao pode mudar.
NOTAS_P2 = {
    5: "conta tambem mencao generica a pessoas antivacina ('os negacionistas', "
       "'quem nao se vacina'), nao so a pessoa nomeada",
    7: "ATENCAO: o codebook do paper coloca 'desmentir desinformacao sobre "
       "riscos da vacina' DENTRO desta categoria, e nao na 9",
    9: "use so quando o tweet trata da desinformacao ENQUANTO TAL: mentira, "
       "boato, fake news, checagem, desmentido",
    10: "use quando o tweet trata de veiculos e canais de informacao enquanto "
        "tais (imprensa, TV, redes sociais, jornalistas), sem juizo sobre "
        "serem falsos; se o ponto e a falsidade, use a 9",
}


def monta_prompt(codebook, versao="p1"):
    """
    System prompt versionado. Instrucoes em PT (o corpus e em PT), nomes e
    definicoes das categorias em INGLES, identicos ao suplemento do paper —
    traduzir introduziria deriva semantica justamente no que esta sendo medido.

    p1 = versao inicial. p2 = p1 + 4 correcoes medidas no dev (ver
    DECISOES_ROTULADOR.md). Versoes antigas continuam reproduziveis.
    """
    if versao.startswith("p6"):
        return _prompt_p6(codebook, diagnostico_cobertura(
            codebook, pd.read_excel(XLSX, "Spreadsheet 1")))
    if versao.startswith("p5"):
        return _prompt_p5(codebook, diagnostico_cobertura(
            codebook, pd.read_excel(XLSX, "Spreadsheet 1")))
    if versao.startswith("p4"):
        # o diagnostico de exaustividade sai do gabarito, nao de intuicao
        return _prompt_p4(codebook, diagnostico_cobertura(
            codebook, pd.read_excel(XLSX, "Spreadsheet 1")))
    if versao.startswith("p3"):
        return _prompt_p3(codebook)
    if versao.startswith("p2"):
        return _prompt_p2(codebook)
    linhas = [
        "Voce e um codificador de analise de conteudo replicando o livro de",
        "codigos de Verjovsky et al. (2023) sobre o debate vacinal brasileiro",
        "no Twitter (dez/2021 a mar/2022).",
        "",
        "Para CADA tweet, produza dois rotulos:",
        "",
        "1) stance — a posicao do tweet sobre a vacinacao contra COVID-19:",
        '   "pro"    = defende, promove ou apoia a vacinacao;',
        '   "anti"   = questiona, ataca ou desencoraja a vacinacao;',
        '   "nenhum" = nao expressa posicao (use com muita parcimonia: no',
        "              gabarito humano apenas 3 de 1525 tweets caem aqui).",
        "   Julgue a posicao do AUTOR do tweet, nao a de quem ele cita. Ironia,",
        "   sarcasmo e citacao critica sao comuns: um tweet que reproduz uma",
        "   fala anti-vacina para ridiculariza-la e 'pro'.",
        "",
        "2) categorias — TODOS os temas presentes, da lista abaixo (0, 1 ou",
        "   varios por tweet; use o NUMERO). Marque um tema so quando ele for",
        "   efetivamente mencionado ou aludido, nao quando for apenas plausivel.",
        "",
        "CATEGORIAS:",
    ]
    for c in codebook["categorias"]:
        # as subcategorias sao o que delimita a fronteira da categoria; sem
        # elas o modelo inventa a propria. Categorias atomicas (Religion,
        # Science) nao tem o que detalhar — o nome ja e a definicao.
        rotulos = rotulos_da_categoria(c)
        if rotulos:
            linhas.append(f"{c['numero']}. {c['nome_en']} — abrange: "
                          + "; ".join(rotulos))
        else:
            linhas.append(f"{c['numero']}. {c['nome_en']}")
    linhas += [
        "",
        "Responda SOMENTE com o JSON pedido, um objeto por tweet, na mesma",
        "ordem em que os tweets foram apresentados, repetindo o id recebido.",
    ]
    return "\n".join(linhas)


def _e_rollup(coluna):
    """Colunas agregadas (`About_All_...`, `..._OR_...`) nao sao gatilho."""
    c = coluna.lower()
    return c.startswith(("all_", "about_all_")) or "_or_" in c


def gatilhos_da_categoria(c, maximo=24):
    """
    Lista EXTENSIONAL do que dispara a categoria (base da p3).

    UM rotulo por subcategoria, escolhido entre as duas fontes do suplemento,
    que carregam informacao diferente:
      - o nome refinado descreve o TIPO ("Ineffectiveness of vaccines");
      - o nome da coluna carrega a ENTIDADE ("Bolsonaro", "Anvisa", "Pfizer").

    Criterio: se o mesmo nome refinado cobre VARIAS colunas da categoria, e
    porque o tipo nao distingue e a entidade e que faz o gabarito disparar
    (`Politics`: "Government politicians" cobre Bolsonaro e governo federal;
    `International`: um unico tipo cobre 34 paises) — nesse caso vale a
    coluna. Quando o nome refinado e unico, ele e mais legivel que a
    abreviacao da coluna ("Ineffectiveness of vaccines" > "vacc INEFFECTIVE").

    Categorias atomicas (sem subcategoria) caem para a propria coluna, que as
    vezes nomeia a entidade — `About_OtherDrugs_CloroquinaORIvermectna`.
    """
    subs = [s for s in c["subcategorias"]
            if s["coluna"] != c["coluna"] and not _e_rollup(s["coluna"])]

    frequencia = Counter(s["refinada"] for s in subs)
    vistos, gatilhos = set(), []

    def acrescenta(rotulo):
        r = re.sub(r"\s+", " ", str(rotulo)).strip(" /,")
        if r and r.lower() not in vistos and r.lower() != c["nome_en"].lower():
            vistos.add(r.lower())
            gatilhos.append(r)

    for s in subs:
        # nome refinado ambiguo dentro da categoria -> a entidade e que informa
        acrescenta(_humaniza(s["coluna"]) if frequencia[s["refinada"]] > 1
                   else s["refinada"])

    if not subs:  # atomica: a propria coluna pode nomear a entidade
        proprio = _humaniza(c["coluna"])
        if proprio.lower() != c["nome_en"].lower():
            for parte in re.split(r"(?<=[a-z])OR(?=[A-Z])|,", proprio):
                acrescenta(parte)

    if len(gatilhos) > maximo:
        return gatilhos[:maximo] + ["entre outros do mesmo tipo"]
    return gatilhos


def diagnostico_cobertura(codebook, gab):
    """
    Classifica cada categoria pela EXAUSTIVIDADE da sua lista de subcategorias,
    medida no proprio gabarito: dos tweets que a coluna agregada marca, quantos
    NENHUMA subcategoria listada pega ("orfaos")?

    E o que decide o tratamento na p4. O criterio sai dos dados, nao da leitura
    que eu faco dos erros — em `Children` a lista cobre 115 de 592 (81% orfaos)
    e transforma-la em lista de gatilhos estreita a categoria a um quinto do que
    ela e; em `Politics` a lista cobre 712 de 719 e a mesma operacao ganha 0,08
    de kappa.
    """
    diag = {}
    for c in codebook["categorias"]:
        subs = [s["coluna"] for s in c["subcategorias"]
                if s["coluna"] != c["coluna"] and not _e_rollup(s["coluna"])
                and s["coluna"] in gab.columns]
        agregado = gab[c["coluna"]] == 1
        cobertos = ((gab[subs] == 1).any(axis=1) if subs
                    else pd.Series(False, index=gab.index))
        n = int(agregado.sum())
        orfaos = int((agregado & ~cobertos).sum())
        fracao = orfaos / n if n else 1.0
        if not subs:
            tipo = "atomica"
        elif fracao <= 0.02:
            tipo = "exaustiva"
        else:
            tipo = "parcial"
        diag[c["numero"]] = {"tipo": tipo, "n": n, "orfaos": orfaos,
                             "fracao_orfaos": round(fracao, 4)}
    return diag


# Bloco de stance da p5. A p1 dizia "no gabarito humano apenas 3 de 1525 caem
# aqui"; a p2-p4 diziam "sao tweets VIRAIS, quase todos tomam partido". As duas
# sao AFIRMACOES DE FREQUENCIA colhidas no estrato viral — e as duas erraram,
# em direcoes opostas: a p1 usou 'nenhum' demais no dev, a p4 de menos no
# estrato baixo (2 de 32 reais). A p5 nao afirma frequencia nenhuma: define
# 'nenhum' por CRITERIO, com indicadores positivos, para que a decisao dependa
# do tweet e nao do estrato de onde ele veio.
STANCE_P5 = [
    "1) stance — a posicao do tweet sobre a vacinacao contra COVID-19:",
    '   "pro"    = defende, promove ou apoia a vacinacao;',
    '   "anti"   = questiona, ataca ou desencoraja a vacinacao;',
    '   "nenhum" = o tweet NAO emite juizo sobre a vacinacao.',
    "",
    "   Julgue a posicao do AUTOR, nao a de quem ele cita. Ironia, sarcasmo e",
    "   citacao critica sao comuns: um tweet que reproduz uma fala anti-vacina",
    "   para ridiculariza-la e 'pro'.",
    "",
    "   Use 'nenhum' quando o tweet for, por exemplo:",
    "   - noticia ou dado relatado sem avaliacao (numeros de doses, agenda de",
    "     vacinacao, resultado de estudo, cobertura factual);",
    "   - pergunta genuina, pedido de informacao ou duvida pratica;",
    "   - so link, so mencao a outro usuario, ou fragmento sem conteudo",
    "     avaliavel;",
    "   - assunto alheio que apenas encosta no vocabulario da vacina;",
    "   - texto ambiguo demais para decidir sem inventar a intencao.",
    "",
    "   REGRA DE ATRIBUICAO (decidida com a codificadora, 27/jul/2026):",
    "   o stance e propriedade do que o TWEET AFIRMA sobre a vacinacao, e nao",
    "   do que se pode inferir sobre o AUTOR. Dai decorre:",
    "   - reproduzir fala de terceiro sem comentario proprio nao e tomar",
    "     posicao, ainda que a fala citada seja enfatica;",
    "   - tomar posicao sobre tema ADJACENTE (passaporte vacinal, restricoes a",
    "     nao-vacinados, obrigatoriedade, politica de governo) nao e tomar",
    "     posicao sobre vacinar-se — marque a categoria tematica correspondente",
    "     e deixe o stance em 'nenhum', a menos que o tweet tambem se posicione",
    "     sobre a vacinacao em si;",
    "   - um autor evidentemente pro-vacina pode escrever um tweet que nao e",
    "     um tweet pro-vacina.",
    "",
    "   'nenhum' nao e a saida para o caso dificil nem para o caso raro: e a",
    "   classificacao correta do tweet que nao toma posicao. Se houver juizo,",
    "   ainda que indireto ou ironico, escolha 'pro' ou 'anti'; se nao houver,",
    "   escolha 'nenhum' sem hesitar. NAO tente acertar nenhuma proporcao",
    "   esperada entre as tres classes — decida cada tweet por si.",
]


N_EXEMPLOS_POR_CLASSE = 4


def exemplos_de_calibracao(n=N_EXEMPLOS_POR_CLASSE):
    """
    Exemplos rotulados a mao, tirados SO da particao de calibracao congelada
    em `split_humano_baixo.csv`. Nunca da particao reservada — usar exemplo de
    validacao dentro do prompt e vazamento direto.

    Selecao deterministica: por classe, ordena por id e pega os n de tamanho
    mais proximo da mediana da classe (evita exemplo minusculo ou gigante sem
    escolher a mao).
    """
    split = pd.read_csv(DADOS / "split_humano_baixo.csv", dtype={"ID": str})
    split = split[split.particao == "calibracao"]
    textos = pd.read_excel(DADOS / "VALIDACAO_HUMANA_amostra.xlsx", "ROTULAR",
                           dtype={"ID": str}).set_index("ID")
    fora = []
    for classe in ("pro", "anti", "nenhum"):
        ids = sorted(split[split.stance_humano == classe].ID)
        if not ids:
            continue
        cand = [(i, " ".join(str(textos.loc[i, "tweet"]).split())) for i in ids]
        mediana = sorted(len(x) for _, x in cand)[len(cand) // 2]
        cand.sort(key=lambda par: (abs(len(par[1]) - mediana), par[0]))
        for _, texto in cand[:n]:
            fora.append((classe, texto[:260]))
    return fora


def _prompt_p6(codebook, diag):
    """
    p6 — PADRAO B: o rotulador passa a codificar segundo o criterio de tres
    classes, com exemplos.

    Diagnostico que a motiva (D7): o gabarito do paper nao contem exemplos de
    tweet TOPICAMENTE RELEVANTE mas SEM POSICAO — a terceira classe de la
    ('non-relevant/ambiguous') marcava assunto fora do tema. Um rotulador
    calibrado naquele material nunca viu a situacao e por isso atribui lado a
    ela. Prosa nao resolveu: a p5, so com criterio escrito, foi de kappa 0,473
    para 0,591 e parou.

    A p6 acrescenta EXEMPLOS das tres classes, tirados da particao de
    calibracao da rotulagem humana. Consequencia assumida e declarada: o
    rotulador deixa de reproduzir o esquema binario do paper e passa a
    reproduzir o esquema de tres classes — que e o unico coerente entre
    estratos, e por isso o unico que permite a comparacao do E1.
    """
    base = _prompt_p5(codebook, diag)
    exemplos = exemplos_de_calibracao()
    if not exemplos:
        return base
    bloco = ["", "EXEMPLOS DE STANCE (rotulados a mao por uma codificadora",
             "experiente; note que 'nenhum' e comum e legitimo):", ""]
    for classe, texto in exemplos:
        bloco.append(f'   [{classe}] "{texto}"')
    bloco.append("")
    corte = base.index("2) categorias")
    return base[:corte] + "\n".join(bloco) + "\n" + base[corte:]

def _prompt_p5(codebook, diag):
    """
    p5 = p4 com o bloco de stance refeito (STANCE_P5). Motivada pela reprovacao
    no estrato baixo: kappa 0,473 la contra 0,759 no viral, com a falha inteira
    concentrada na classe 'nenhum' (o modelo reconheceu 2 de 32). A parte de
    categorias da p4 nao mudou — nada indica problema nela.
    """
    base = _prompt_p4(codebook, diag)
    inicio = base.index("1) stance")
    fim = base.index("2) categorias")
    return base[:inicio] + "\n".join(STANCE_P5) + "\n\n" + base[fim:]

def _prompt_p4(codebook, diag):
    """
    p4 — trata cada categoria conforme a NATUREZA dela, e nao com uma politica
    unica para as 14.

    O erro comum da p2 e da p3 foi o mesmo em direcoes opostas: a p2 mandou
    todas marcarem mais, a p3 transformou todas em lista. Cada uma acertou o
    subconjunto que casava com a sua politica e errou o resto.

      exaustiva  -> lista de gatilhos (o que funcionou na p3)
      parcial    -> lista + clausula de abertura, para nao estreitar a
                    categoria (o erro que derrubou Children de 0,889 p/ 0,786)
      atomica    -> enquadramento tematico + empurrao de inclusividade
                    ESCOPADO nelas (o empurrao global da p2 estragava as
                    categorias ja calibradas); se o nome da propria coluna
                    carrega entidade, ela vira gatilho (Other drugs: 0,839)
    """
    linhas = [
        "Voce e um codificador de analise de conteudo replicando o livro de",
        "codigos de Verjovsky et al. (2023) sobre o debate vacinal brasileiro",
        "no Twitter (dez/2021 a mar/2022).",
        "",
        "Para CADA tweet, produza dois rotulos:",
        "",
        "1) stance — a posicao do tweet sobre a vacinacao contra COVID-19:",
        '   "pro"    = defende, promove ou apoia a vacinacao;',
        '   "anti"   = questiona, ataca ou desencoraja a vacinacao;',
        '   "nenhum" = reserve para o tweet que nao permite decidir de lado',
        "              nenhum. Estes sao tweets VIRAIS de um debate polarizado:",
        "              quase todos tomam partido, ainda que de forma indireta,",
        "              ironica ou por quem ataca. Se houver qualquer indicio de",
        "              posicao, escolha 'pro' ou 'anti' — nao use 'nenhum' como",
        "              saida para o caso dificil.",
        "   Julgue a posicao do AUTOR do tweet, nao a de quem ele cita. Ironia,",
        "   sarcasmo e citacao critica sao comuns: um tweet que reproduz uma",
        "   fala anti-vacina para ridiculariza-la e 'pro'.",
        "",
        "2) categorias — use o NUMERO de cada uma que se aplique (0, 1 ou",
        "   varias por tweet). Basta o tema ou o item aparecer, ainda que de",
        "   passagem e ainda que nao seja o assunto principal do tweet: um",
        "   tweet sobre vacinacao infantil que menciona a agencia reguladora",
        "   de passagem conta TAMBEM como Politics.",
        "",
        "   As categorias vem em dois formatos, e a pergunta muda:",
        "   - com 'gatilhos:' — pergunte 'o tweet CITA ou ALUDE a algum destes?';",
        "     basta UM. Quando a lista terminar em 'e qualquer outra mencao a X',",
        "     ela e ilustrativa, nao fechada: vale qualquer coisa do tipo X.",
        "   - sem 'gatilhos:' — pergunte 'o tema aparece no tweet?'. Sao temas",
        "     amplos; uma mencao de passagem ja conta.",
        "",
        "CATEGORIAS:",
    ]
    for c in codebook["categorias"]:
        numero = c["numero"]
        tipo = diag[numero]["tipo"]
        gat = gatilhos_da_categoria(c)
        linha = f"{numero}. {c['nome_en']}"
        if tipo == "exaustiva" and gat:
            linha += "\n    gatilhos: " + "; ".join(gat)
        elif tipo == "parcial" and gat:
            # a lista existe mas nao esgota a categoria: abrir explicitamente,
            # senao a lista vira um limite em vez de uma ajuda. O marcador de
            # truncamento sai — a clausula de abertura ja diz o mesmo, melhor.
            itens = [g for g in gat if g != "entre outros do mesmo tipo"]
            linha += ("\n    gatilhos: " + "; ".join(itens)
                      + f"; e qualquer outra mencao a {c['nome_en']}")
        elif gat:  # atomica cujo nome de coluna carregava entidade
            linha += "\n    gatilhos: " + "; ".join(gat)
        else:      # atomica sem lista: empurrao de inclusividade escopado aqui
            linha += ("\n    tema amplo — marque sempre que aparecer, ainda que"
                      " de passagem")
        if numero in NOTAS_P2:
            linha += f"\n    [{NOTAS_P2[numero]}]"
        linhas.append(linha)
    linhas += [
        "",
        "Responda SOMENTE com o JSON pedido, um objeto por tweet, na mesma",
        "ordem em que os tweets foram apresentados, repetindo o id recebido.",
    ]
    return "\n".join(linhas)


def _prompt_p3(codebook):
    """
    p3 — testa a hipotese D3: as categorias agregadas do gabarito sao
    EXTENSIONAIS (`OR` de dezenas de itens concretos), e o modelo estava
    julgando intensionalmente ("este tweet e *sobre* politica?").

    Duas mudancas em relacao a p2:
      (1) cada categoria vira uma lista de GATILHOS concretos, com a pergunta
          reformulada de "e sobre este tema?" para "cita algum destes?";
      (2) sai a instrucao global "na duvida, MARQUE" (D2.2), cujo efeito
          colateral foi medido: empurrou para a super-marcacao justamente as
          categorias ja bem calibradas (Vaccines/labs caiu de 0,773 para
          0,654). A inclusividade passa a vir da definicao de cada categoria,
          nao de um empurrao global.

    Mantidas as duas correcoes que funcionaram na p2: o estreitamento do
    "nenhum" (D2.1) e a fronteira 9 x 10 (D2.3).
    """
    linhas = [
        "Voce e um codificador de analise de conteudo replicando o livro de",
        "codigos de Verjovsky et al. (2023) sobre o debate vacinal brasileiro",
        "no Twitter (dez/2021 a mar/2022).",
        "",
        "Para CADA tweet, produza dois rotulos:",
        "",
        "1) stance — a posicao do tweet sobre a vacinacao contra COVID-19:",
        '   "pro"    = defende, promove ou apoia a vacinacao;',
        '   "anti"   = questiona, ataca ou desencoraja a vacinacao;',
        '   "nenhum" = reserve para o tweet que nao permite decidir de lado',
        "              nenhum. Estes sao tweets VIRAIS de um debate polarizado:",
        "              quase todos tomam partido, ainda que de forma indireta,",
        "              ironica ou por quem ataca. Se houver qualquer indicio de",
        "              posicao, escolha 'pro' ou 'anti' — nao use 'nenhum' como",
        "              saida para o caso dificil.",
        "   Julgue a posicao do AUTOR do tweet, nao a de quem ele cita. Ironia,",
        "   sarcasmo e citacao critica sao comuns: um tweet que reproduz uma",
        "   fala anti-vacina para ridiculariza-la e 'pro'.",
        "",
        "2) categorias — use o NUMERO de cada uma que se aplique (0, 1 ou",
        "   varias por tweet).",
        "",
        "   IMPORTANTE — como decidir. NAO pergunte 'este tweet e SOBRE este",
        "   tema?'. Pergunte 'o tweet CITA ou ALUDE a algum dos itens da",
        "   lista?'. Cada categoria abaixo e uma lista de gatilhos concretos, e",
        "   basta UM deles aparecer — ainda que de passagem, ainda que nao seja",
        "   o assunto principal — para a categoria valer. Um tweet sobre",
        "   vacinacao infantil que menciona a Anvisa de passagem conta como",
        "   Politics, porque a Anvisa esta na lista da Politics.",
        "",
        "CATEGORIAS (cada uma: marque se o tweet citar ou aludir a qualquer",
        "um dos gatilhos):",
    ]
    for c in codebook["categorias"]:
        gat = gatilhos_da_categoria(c)
        linha = f"{c['numero']}. {c['nome_en']}"
        if gat:
            linha += "\n    gatilhos: " + "; ".join(gat)
        if c["numero"] in NOTAS_P2:
            linha += f"\n    [{NOTAS_P2[c['numero']]}]"
        linhas.append(linha)
    linhas += [
        "",
        "Responda SOMENTE com o JSON pedido, um objeto por tweet, na mesma",
        "ordem em que os tweets foram apresentados, repetindo o id recebido.",
    ]
    return "\n".join(linhas)


def _prompt_p2(codebook):
    """
    p2 — quatro correcoes, cada uma respondendo a um erro medido no dev/p1:

      (1) stance: a p1 anunciava que "nenhum" e raro e mesmo assim o modelo o
          usou 26x em 506, contra 0 ocorrencias no gabarito do dev. Anunciar
          que uma saida e rara nao impede o modelo de se refugiar nela; aqui
          a condicao de uso fica explicita e estreita.
      (2) marcacao: a p1 pedia cautela ("nao marque o apenas plausivel") e
          produziu sub-marcacao sistematica (Information sources 59->20,
          Anti-vaccine people 129->55, Politics 245->178). Os codificadores
          humanos do paper sao generosos; o limiar passa a ser inclusivo.
      (3) fronteira 9 x 10: as duas se canibalizavam (kappa 0,26 e 0,42) —
          na p1 a 9 nao tinha cláusula explicativa nenhuma.
      (4) fronteira 7: contagem certa (77 x 80) com kappa 0,34, isto e, os
          tweets errados. O codebook do paper poe "desmentir desinformacao
          sobre riscos" dentro de Advantages, o que nao e adivinhavel.
    """
    linhas = [
        "Voce e um codificador de analise de conteudo replicando o livro de",
        "codigos de Verjovsky et al. (2023) sobre o debate vacinal brasileiro",
        "no Twitter (dez/2021 a mar/2022).",
        "",
        "Para CADA tweet, produza dois rotulos:",
        "",
        "1) stance — a posicao do tweet sobre a vacinacao contra COVID-19:",
        '   "pro"    = defende, promove ou apoia a vacinacao;',
        '   "anti"   = questiona, ataca ou desencoraja a vacinacao;',
        '   "nenhum" = reserve para o tweet que nao permite decidir de lado',
        "              nenhum. Estes sao tweets VIRAIS de um debate polarizado:",
        "              quase todos tomam partido, ainda que de forma indireta,",
        "              ironica ou por quem ataca. Se houver qualquer indicio de",
        "              posicao, escolha 'pro' ou 'anti' — nao use 'nenhum' como",
        "              saida para o caso dificil.",
        "   Julgue a posicao do AUTOR do tweet, nao a de quem ele cita. Ironia,",
        "   sarcasmo e citacao critica sao comuns: um tweet que reproduz uma",
        "   fala anti-vacina para ridiculariza-la e 'pro'.",
        "",
        "2) categorias — TODOS os temas presentes, da lista abaixo (0, 1 ou",
        "   varios por tweet; use o NUMERO).",
        "   Seja INCLUSIVO: marque o tema sempre que ele for mencionado ou",
        "   aludido, mesmo de passagem, mesmo que nao seja o assunto principal",
        "   do tweet. Os codificadores humanos que produziram o gabarito marcam",
        "   com generosidade — um tweet costuma acumular varios temas. Na",
        "   duvida entre marcar e nao marcar, MARQUE.",
        "",
        "CATEGORIAS:",
    ]
    for c in codebook["categorias"]:
        rotulos = rotulos_da_categoria(c)
        linha = f"{c['numero']}. {c['nome_en']}"
        if rotulos:
            linha += " — abrange: " + "; ".join(rotulos)
        if c["numero"] in NOTAS_P2:
            linha += f"\n    [{NOTAS_P2[c['numero']]}]"
        linhas.append(linha)
    linhas += [
        "",
        "Responda SOMENTE com o JSON pedido, um objeto por tweet, na mesma",
        "ordem em que os tweets foram apresentados, repetindo o id recebido.",
    ]
    return "\n".join(linhas)


def esquema(n_categorias=14):
    return {
        "type": "object",
        "properties": {
            "rotulos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "stance": {"type": "string", "enum": ["pro", "anti", "nenhum"]},
                        "categorias": {
                            "type": "array",
                            "items": {"type": "integer",
                                      "enum": list(range(1, n_categorias + 1))},
                        },
                    },
                    "required": ["id", "stance", "categorias"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["rotulos"],
        "additionalProperties": False,
    }


def monta_lotes(tweets, por_chamada):
    """Agrupa tweets em requests. Amortizar o system prompt e o que cabe no teto."""
    for i in range(0, len(tweets), por_chamada):
        yield tweets[i:i + por_chamada]


def texto_do_lote(lote):
    partes = []
    for t in lote:
        # delimitador explicito: tweets contem quebras de linha e emoji
        partes.append(f"<tweet id=\"{t['id']}\">\n{t['texto']}\n</tweet>")
    return (f"Rotule os {len(lote)} tweets abaixo.\n\n" + "\n\n".join(partes))


def carrega_do_snapshot(limiar, idioma="pt", limite=None):
    """
    Tweets originais do snapshot congelado, acima do limiar de viralidade.

    Filtro de idioma: o corpus tem ~14% de tweets que nao sao pt em >10 RT, e
    a amostragem confirmou que sao frances e ingles DE VERDADE (os termos
    provax/antivax pegaram o debate internacional), nao portugues mal
    classificado; `und` sao tweets so com link, sem texto a rotular. O codebook,
    o gabarito e o paper tratam do debate brasileiro. Indicio de que o paper
    fez o mesmo corte: eles rotularam 1.525 tweets do estrato >500 RT, e o
    subconjunto pt desse estrato tem 1.560.
    """
    import sqlite3
    con = sqlite3.connect(SNAPSHOT)
    sql = ("SELECT twitter_id, texto FROM originais "
           "WHERE retweets > ? AND texto IS NOT NULL AND trim(texto) != ''")
    params = [limiar]
    if idioma:
        sql += " AND idioma = ?"
        params.append(idioma)
    sql += " ORDER BY twitter_id"
    if limite:
        sql += f" LIMIT {int(limite)}"
    linhas = con.execute(sql, params).fetchall()
    con.close()
    return [{"id": str(i), "texto": str(txt).strip()} for i, txt in linhas]


def carrega_tweets(conjunto, limite=None):
    gab = pd.read_excel(XLSX, "Spreadsheet 1")
    if conjunto in ("dev", "teste"):
        if not SPLIT.exists():
            raise SystemExit("[erro] rode antes: python pipeline/congela_split.py")
        split = pd.read_csv(SPLIT)
        ids = set(split[split.particao == conjunto].ID)
        gab = gab[gab.ID.isin(ids)]
    elif conjunto != "tudo":
        raise SystemExit(f"[erro] conjunto desconhecido: {conjunto}")
    gab = gab.sort_values("ID")
    if limite:
        gab = gab.head(limite)
    return [{"id": str(r.ID), "texto": str(r.Tweet).strip()}
            for r in gab.itertuples()]


def estima_custo(cli, modelo, sistema, lotes, por_chamada):
    """
    Custo MAXIMO do conjunto de lotes, em dolares.

    Conta tokens de verdade (count_tokens e gratuito) numa amostra dos lotes
    maiores, toma o pior, aplica margem e multiplica. A saida entra pelo teto
    de max_tokens, nunca pelo esperado — reserva sempre >= gasto real.
    """
    amostra = sorted(lotes, key=lambda l: sum(len(t["texto"]) for t in l),
                     reverse=True)[:5]
    pior_entrada, fonte = 0, "count_tokens"
    for lote in amostra:
        corpo = texto_do_lote(lote)
        try:
            r = cli.messages.count_tokens(
                model=modelo, system=sistema,
                messages=[{"role": "user", "content": corpo}],
            )
            n = r.input_tokens
        except Exception as e:
            # count_tokens e gratuito, mas exige conta com credito. Sem ela,
            # caimos num limite superior local: 2,5 chars/token e conservador
            # para portugues com emoji (o real fica em ~3,2), entao a
            # estimativa SUPERESTIMA — que e o lado seguro para um teto.
            fonte = f"estimativa local (count_tokens indisponivel: {type(e).__name__})"
            n = int((len(sistema) + len(corpo)) / 2.5)
        pior_entrada = max(pior_entrada, n)

    entrada = int(pior_entrada * MARGEM_SEGURANCA) * len(lotes)
    saida = MAX_TOKENS_POR_TWEET * por_chamada * len(lotes)
    usd = custo_usd(modelo, entrada=entrada, saida=saida, batch=True)
    return usd, pior_entrada, fonte


def envia_lote(cli, modelo, sistema, lotes, por_chamada, destino):
    """Submete um Batch, espera terminar e devolve (rotulos, uso)."""
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    pedidos = []
    for i, lote in enumerate(lotes):
        pedidos.append(Request(
            custom_id=f"lote-{i:05d}",
            params=MessageCreateParamsNonStreaming(
                model=modelo,
                max_tokens=MAX_TOKENS_POR_TWEET * por_chamada + 64,
                temperature=0,
                system=sistema,
                messages=[{"role": "user", "content": texto_do_lote(lote)}],
                output_config={"format": {"type": "json_schema",
                                          "schema": esquema()}},
            ),
        ))

    with (destino / "pedidos.jsonl").open("w", encoding="utf-8") as f:
        for i, lote in enumerate(lotes):
            f.write(json.dumps({"custom_id": f"lote-{i:05d}",
                                "ids": [t["id"] for t in lote]},
                               ensure_ascii=False) + "\n")

    lote_api = cli.messages.batches.create(requests=pedidos)
    print(f"[batch] id={lote_api.id} ({len(pedidos)} requests) — aguardando...")

    inicio = time.time()
    while True:
        b = cli.messages.batches.retrieve(lote_api.id)
        if b.processing_status == "ended":
            break
        print(f"  ... {b.processing_status} "
              f"(ok={b.request_counts.succeeded} erro={b.request_counts.errored} "
              f"proc={b.request_counts.processing}) "
              f"[{time.time()-inicio:.0f}s]", flush=True)
        time.sleep(20)

    ids_por_lote = {f"lote-{i:05d}": [t["id"] for t in lote]
                    for i, lote in enumerate(lotes)}
    rotulos, uso = {}, {"entrada": 0, "saida": 0, "cache_leitura": 0,
                        "cache_escrita": 0}
    falhas, trocas = [], []
    with (destino / "respostas.jsonl").open("w", encoding="utf-8") as f:
        for res in cli.messages.batches.results(lote_api.id):
            if res.result.type != "succeeded":
                falhas.append((res.custom_id, res.result.type))
                continue
            msg = res.result.message
            u = msg.usage
            uso["entrada"] += u.input_tokens
            uso["saida"] += u.output_tokens
            uso["cache_leitura"] += getattr(u, "cache_read_input_tokens", 0) or 0
            uso["cache_escrita"] += getattr(u, "cache_creation_input_tokens", 0) or 0
            texto = next((b.text for b in msg.content if b.type == "text"), "")
            f.write(json.dumps({"custom_id": res.custom_id, "texto": texto},
                               ensure_ascii=False) + "\n")
            try:
                devolvidos = json.loads(texto)["rotulos"]
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                falhas.append((res.custom_id, f"json invalido: {e}"))
                continue

            # O modelo ocasionalmente erra a TRANSCRICAO do id ao ecoa-lo
            # (medido no teste cego: devolveu '538' no lugar de '539', 1 em
            # 1019 = 0,1%). Como a ordem e preservada e o pedido tem tamanho
            # conhecido, alinhamos por POSICAO quando as contagens batem —
            # correcao mecanica, sem juizo sobre o conteudo do rotulo.
            pedidos_do_lote = ids_por_lote.get(res.custom_id, [])
            if len(devolvidos) == len(pedidos_do_lote):
                for id_certo, r in zip(pedidos_do_lote, devolvidos):
                    if str(r.get("id")) != id_certo:
                        trocas.append((res.custom_id, r.get("id"), id_certo))
                    rotulos[id_certo] = r
            else:
                # contagens divergem: nao da para confiar na posicao, cai para
                # o id ecoado e reporta o que sobrar como falta
                for r in devolvidos:
                    rotulos[str(r.get("id"))] = r
                falhas.append((res.custom_id,
                               f"devolveu {len(devolvidos)} rotulos para "
                               f"{len(pedidos_do_lote)} tweets"))

    if falhas:
        print(f"[aviso] {len(falhas)} requests sem rotulo: {falhas[:5]}")
    if trocas:
        print(f"[aviso] {len(trocas)} ids corrigidos por posicao "
              f"(o modelo transcreveu errado): {trocas[:5]}")
    return rotulos, uso, lote_api.id, trocas


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conjunto", default="dev",
                    choices=["dev", "teste", "tudo", "snapshot", "amostra_humana", "calibragem"],
                    help="'snapshot' = corpus do E1 acima de --limiar")
    ap.add_argument("--limiar", type=int, default=10,
                    help="RT minimo (so com --conjunto snapshot)")
    ap.add_argument("--idioma", default="pt",
                    help="filtro de idioma no snapshot ('' desliga)")
    ap.add_argument("--bloco", type=int, default=400,
                    help="requests por batch; cada bloco reserva e concilia "
                         "orcamento separado, e o progresso e retomavel")
    ap.add_argument("--modelo", default=MODELO_PADRAO)
    ap.add_argument("--por-chamada", type=int, default=10,
                    help="tweets por request (amortiza o system prompt)")
    ap.add_argument("--limite", type=int, default=None,
                    help="usa so os N primeiros tweets (teste de fumaca)")
    ap.add_argument("--prompt", default="p1", help="rotulo da versao do prompt")
    ap.add_argument("--dry-run", action="store_true",
                    help="so estima o custo; nao envia nada")
    args = ap.parse_args()

    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    sistema = monta_prompt(codebook, args.prompt)
    sha_prompt = hashlib.sha256(sistema.encode("utf-8")).hexdigest()[:12]

    if args.conjunto == "calibragem":
        # os 30 tweets VIRAIS que a Mariana rotulou as cegas no teste de
        # criterio. Reservados desde o inicio: deles so foram vistos kappa e
        # matriz, nunca um texto. Segunda checagem, em estrato diferente.
        cg = pd.read_csv(DADOS / "calibragem_criterio_ids.csv", dtype={"ID": str})
        tweets = [{"id": r.ID, "texto": str(r.tweet).strip()} for r in cg.itertuples()]
        nome = "calibragem_viral"
    elif args.conjunto == "amostra_humana":
        # os 100 tweets que a Mariana rotulou a mao. Depois de servirem de
        # diagnostico eles sao conjunto de DESENVOLVIMENTO, nao de teste:
        # consertar o prompt olhando para eles e legitimo, validar nao.
        am = pd.read_csv(DADOS / "validacao_humana_amostra.csv", dtype={"ID": str})
        tweets = [{"id": r.ID, "texto": str(r.tweet).strip()}
                  for r in am.itertuples()]
        if args.limite:
            tweets = tweets[:args.limite]
        nome = "amostra_humana"
    elif args.conjunto == "snapshot":
        tweets = carrega_do_snapshot(args.limiar, args.idioma or None, args.limite)
        nome = f"e1_lim{args.limiar}{'_' + args.idioma if args.idioma else ''}"
    else:
        tweets = carrega_tweets(args.conjunto, args.limite)
        nome = args.conjunto
    destino = SAIDA / f"{nome}_{args.prompt}"

    # Retomada: o que ja foi rotulado numa execucao anterior nao se paga de
    # novo. O CSV parcial e a fonte da verdade do progresso.
    prontos, ja = set(), []
    parcial = destino / "rotulos.csv"
    if parcial.exists():
        antigo = pd.read_csv(parcial, dtype={"ID": str})
        ja = antigo.to_dict("records")
        prontos = set(antigo.ID)
        tweets = [x for x in tweets if x["id"] not in prontos]
        print(f"[retomada] {len(prontos):,} ja rotulados; faltam {len(tweets):,}")

    lotes = list(monta_lotes(tweets, args.por_chamada))
    print(f"[info] conjunto={args.conjunto} tweets={len(tweets):,} "
          f"lotes={len(lotes):,} ({args.por_chamada}/chamada)")
    print(f"[info] modelo={args.modelo} prompt={args.prompt} sha={sha_prompt}")

    cli = cliente()
    maximo, pior, fonte = estima_custo(cli, args.modelo, sistema, lotes,
                                       args.por_chamada)
    print(f"[custo] pior request: {pior} tokens de entrada ({fonte})")
    print(f"[custo] teto do conjunto: US$ {maximo:.4f} "
          f"(pior caso, com margem de {MARGEM_SEGURANCA:.0%})")

    orc = Orcamento()
    print(f"[orcamento] {orc.resumo()}")

    if args.dry_run:
        cabe = "CABE" if maximo <= orc.saldo else "NAO CABE"
        print(f"[dry-run] {cabe} no saldo. Nada enviado.")
        return 0
    if not lotes:
        print("[ok] nada a fazer — tudo ja rotulado.")
        return 0

    destino.mkdir(parents=True, exist_ok=True)

    # Blocos: cada um reserva, envia e concilia por conta propria, e grava o
    # CSV acumulado ao fim. Assim uma interrupcao no meio de 30 mil tweets nao
    # perde o que ja foi pago, e o teto e conferido a cada bloco (nao uma vez
    # so no inicio, quando o saldo ainda parecia folgado).
    blocos = [lotes[i:i + args.bloco] for i in range(0, len(lotes), args.bloco)]
    custo_por_lote = maximo / max(len(lotes), 1)
    linhas, batch_ids = list(ja), []
    uso_total = {"entrada": 0, "saida": 0, "cache_leitura": 0, "cache_escrita": 0}
    faltando, trocas_total, gasto_total = [], [], 0.0

    for n, bloco in enumerate(blocos, 1):
        tweets_bloco = [x for lote in bloco for x in lote]
        teto_bloco = custo_por_lote * len(bloco)
        print(f"\n[bloco {n}/{len(blocos)}] {len(tweets_bloco):,} tweets, "
              f"teto US$ {teto_bloco:.4f} | saldo US$ {orc.saldo:.4f}")
        try:
            reserva = orc.reservar(
                teto_bloco, f"rotulagem {nome} ({args.prompt}) bloco {n}",
                {"tweets": len(tweets_bloco), "lotes": len(bloco),
                 "modelo": args.modelo, "sha_prompt": sha_prompt})
        except OrcamentoEstourado as e:
            print(f"[BLOQUEADO] {e}")
            print(f"[parcial] {len(linhas):,} tweets rotulados antes de parar.")
            break

        try:
            rot, uso, bid, trocas = envia_lote(
                cli, args.modelo, sistema, bloco, args.por_chamada, destino)
        except Exception:
            orc.libera(reserva, f"excecao no bloco {n}")
            raise

        gasto_total += orc.concilia(
            reserva, args.modelo, entrada=uso["entrada"], saida=uso["saida"],
            cache_leitura=uso["cache_leitura"],
            cache_escrita=uso["cache_escrita"], batch=True)
        batch_ids.append(bid)
        trocas_total += trocas
        for k in uso_total:
            uso_total[k] += uso[k]

        for x in tweets_bloco:
            r = rot.get(x["id"])
            if r is None:
                faltando.append(x["id"])
                continue
            cats = set(r.get("categorias") or [])
            linha = {"ID": x["id"], "stance": r["stance"]}
            for c in codebook["categorias"]:
                linha[f"cat_{c['numero']}"] = int(c["numero"] in cats)
            linhas.append(linha)

        # grava a cada bloco: se cair aqui, o proximo run retoma daqui
        pd.DataFrame(linhas).to_csv(destino / "rotulos.csv", index=False,
                                    encoding="utf-8")
        print(f"[bloco {n}/{len(blocos)}] acumulado {len(linhas):,} tweets | "
              f"{orc.resumo()}")

    real, batch_id, trocas = gasto_total, batch_ids, trocas_total
    uso = uso_total

    (destino / "execucao.json").write_text(json.dumps({
        "conjunto": args.conjunto, "modelo": args.modelo,
        "prompt_versao": args.prompt, "prompt_sha256_12": sha_prompt,
        "por_chamada": args.por_chamada, "temperatura": 0,
        "batch_id": batch_id, "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "n_tweets": len(tweets), "n_rotulados": len(linhas),
        "n_faltando": len(faltando), "ids_faltando": faltando[:50],
        "n_ids_corrigidos_por_posicao": len(trocas), "ids_corrigidos": trocas[:50],
        "uso_tokens": uso, "custo_reservado_usd": round(maximo, 6),
        "custo_real_usd": round(real, 6),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    (destino / "prompt_sistema.txt").write_text(sistema, encoding="utf-8")

    print(f"[ok] rotulados {len(linhas)}/{len(tweets)} "
          f"({len(faltando)} sem resposta)")
    print(f"[custo] real US$ {real:.4f} (reservado US$ {maximo:.4f})")
    print(f"[orcamento] {orc.resumo()}")
    print(f"[ok] escrito: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
