# -*- coding: utf-8 -*-
"""Divide o capitulo do Reddit em dois -- um por caso (pedido da Mariana, 9/set/2026).

MOTIVO. Todo capitulo de caso do documento cobre um caso; so o do Reddit cobria
dois. E os titulos dos capitulos seguintes ja contavam como dois: o YouTube e
"Quinto Caso Executado" e o TikTok e o sexto, o que so fecha se o Reddit for o
terceiro E o quarto. A numeracao ja estava certa; a estrutura e que nao
acompanhava.

COMO. A §6.1 (papeis sociais) vira o Cap. 6 e a §6.2 (homofilia) vira o Cap. 7;
as subsecoes sobem para secoes. Os corpos sao reaproveitados VERBATIM do arquivo,
nao transcritos, para nao introduzir erro de copia.

A §6.3 ("O que os dois casos acrescentam ao conjunto") deixa de existir como
secao conjunta. Decisao da Mariana: cada capitulo ganha a SUA conclusao, sem
duplicar, e o contraste entre os dois aparece so no quarto caso. Assim:
  - Cap. 6 ganha "Leitura em termos de volume" propria, so sobre o seu caso;
  - Cap. 7 ganha a sua, e nela entram o contraste com o Cap. 6 e a leitura
    geral que dele decorre.
O nome da secao final segue o padrao dos Caps. 4 e 5, que ja fechavam assim.

LABELS. `cap:caso-reddit` era ambiguo com dois capitulos de Reddit; passa a
`cap:caso-papeis` e `cap:caso-homofilia`. As 10 referencias externas sao
reapontadas uma a uma (ver MAPA abaixo), e nao em bloco: 5 falavam de um caso
so, 4 falavam dos dois e 1 e generica.
"""
import io
import os
import re

P = (r"c:\Users\maria\Documents\GitHub\dissertacao-mestrado\escrita\dissertacao"
     r"\corpo.tex")
s = io.open(P, encoding="utf-8", newline="").read()

if r"\chapter{Terceiro Caso Executado: Papéis Sociais no Reddit}" in s:
    raise SystemExit("[parado] a divisao ja foi aplicada.")

ini = s.index("\\chapter{Terceiro e Quarto Casos")
fim = s.index("\\chapter{", ini + 10)
cap = s[ini:fim]


def entre(a, b=None):
    i = cap.index(a)
    j = cap.index(b) if b else len(cap)
    return cap[i:j]


def sobe(bloco):
    """subsection -> section (as subsecoes viram secoes ao subir de nivel)."""
    return bloco.replace("\\subsection{", "\\section{")


# --- corpos reaproveitados verbatim -----------------------------------
intro_buntain = entre("\\section{Papéis sociais:", "\\subsection{Uma sub-coleta")
intro_buntain = intro_buntain[intro_buntain.index("\n"):].strip("\n")
corpo_buntain = sobe(entre("\\subsection{Uma sub-coleta", "\\section{Homofilia"))

intro_massachs = entre("\\section{Homofilia:", "\\subsection{O ponto original")
intro_massachs = intro_massachs[intro_massachs.index("\n"):].strip("\n")
corpo_massachs = sobe(entre("\\subsection{O ponto original",
                            "\\section{O que os dois casos"))

BARRA = "% " + "=" * 69

CAP6 = """\\chapter{Terceiro Caso Executado: Papéis Sociais no Reddit}
\\label{cap:caso-papeis}
""" + BARRA + """

Este é o primeiro caso executado fora do Twitter/X, e a mudança importa: os dois
primeiros dependeram de uma exceção, a de um acervo histórico preservado, que não se
reproduz por coleta nova. Ele e o caso seguinte replicam trabalhos sobre o Reddit,
atacam o eixo de \\emph{volume} --- e não o de largura de filtro ou o de forma do
critério --- e partem de alvos cuja sub-coleta é um estrato de atividade, isto é, um
recorte que retém apenas os participantes mais ativos.

O Reddit é, dos ambientes examinados, o mais favorável ao protocolo, e a
Seção~\\ref{sec:casos} já o registrava como caso ideal. Os arquivos históricos
distribuídos via Academic Torrents contêm a população completa de um subreddit numa
janela, ao passo que a interface oficial devolve cerca de mil itens por listagem. A
própria interface é, portanto, um esquema de amostragem a superar, e superá-lo não
depende de credencial, de acervo institucional nem de acordo com plataforma. É a
situação em que o ``coletar mais'' é literal.

O caso deste capítulo entrega o maior efeito de sub-coleta medido nesta dissertação.

""" + intro_buntain + """

""" + corpo_buntain + """\\section{Leitura em termos de volume}

As duas perguntas do protocolo recebem, aqui, respostas de sinais opostos. A conclusão
publicada \\emph{mudou}, e mudou por uma ordem de grandeza: a participação em mais de uma
comunidade não é de três por cento, e sim de 57,6\\% sob o mesmo corte de atividade que o
artigo aplicou. É o maior efeito de sub-coleta registrado neste trabalho. E a medida
\\emph{convergiu}, mas a convergência é da curva construída aqui, não do valor do artigo:
entre dez e cinquenta mensagens ela se move menos de três pontos percentuais, e nenhum
limiar aplicado ao universo devolve os três por cento publicados.

Essa assimetria é o que o caso acrescenta ao conjunto. Nos casos anteriores, o volume
maior deslocava uma estimativa; aqui ele revela um fenômeno que o recorte havia
suprimido. A quantidade que o artigo se propõe a contar --- reencontrar o mesmo
participante em comunidades distintas --- é justamente a que o topo de popularidade
torna improvável por construção, de modo que o número publicado descreve o desenho da
coleta e não a população. Nenhuma correção estatística aplicada aos 279 participantes
recuperaria os 57,6\\%, porque a evidência não foi enviesada: ela foi removida.

O caso traz ainda a \\emph{análise de rede} para o conjunto, tipo que os dois primeiros
não cobriam, e o faz sobre a afirmação estrutural do alvo, e não sobre a atribuição de
papéis, pela razão registrada na seção anterior.

"""

CAP7 = """\\chapter{Quarto Caso Executado: Homofilia no Reddit}
\\label{cap:caso-homofilia}
""" + BARRA + """

O segundo caso executado no Reddit partilha com o anterior a rede e o eixo, e vale para
ele o que a abertura do Capítulo~\\ref{cap:caso-papeis} registrou sobre a plataforma: a
expansão não depende de credencial nem de acervo institucional. O desfecho, porém, é o
oposto --- o ponto original reproduz com precisão incomum ---, e o que o caso acrescenta
não é um efeito de volume, e sim um achado sobre o que os artigos não declaram.

""" + intro_massachs + """

""" + corpo_massachs + """\\section{Leitura em termos de volume}

Este caso não responde às duas perguntas do protocolo, e a razão está registrada na
seção anterior: a expansão não foi executada. O que ele estabelece é o pré-requisito
delas. O ponto de partida reproduz a menos de um quarto de ponto percentual nas duas
pontas que sustentam a conclusão do artigo, de modo que qualquer divergência que a
expansão viesse a medir seria atribuível ao estrato, e não a erro de reimplementação.
Ele traz também a \\emph{homofilia} para o conjunto, tipo de análise que nenhum outro
caso cobre, e o achado sobre a reponderação de classes, que é a quarta rede em que uma
decisão não declarada governa um número publicado.

Vale o contraste com o caso anterior, porque os dois partilham a rede, o eixo e a
natureza da sub-coleta e chegam a desfechos opostos. A diferença não está no cuidado
dos autores, e sim no que cada recorte remove. O recorte de
\\citeonline{buntain2014socialroles} retém o topo de popularidade de cada comunidade, e a
quantidade que aquele artigo mede, a de participar de várias comunidades, é exatamente a
que o topo torna improvável. O recorte de \\citeonline{massachs2020trumpism} retém os
participantes persistentes, e a quantidade que este mede, a ordenação relativa entre três
famílias de preditores, não tem razão evidente para depender da persistência.

Formulada assim, a lição é a mesma que o eixo de mídia do primeiro caso executado já
sugeria e que o debate vacinal confirmou: o que decide não é o tamanho da coleta, e sim
a relação entre o critério que a recorta e a quantidade que se quer medir. Uma coleta
pequena pode bastar, e uma coleta grande pode não bastar; o que não se pode é deixar
essa relação por examinar, que é o que a literatura levantada faz de regra.

Resta uma diferença de natureza que este par torna visível. A expansão que aqui ficou
por fazer é uma pendência de \\emph{tempo}: os arquivos existem, são públicos e estão ao
alcance. Não é o que ocorre no TikTok, onde a porta está fechada por credencial
revogada, nem nas plataformas da Meta, onde ela está fechada por decisão comercial
(Seção~\\ref{sec:coleta-plataforma}). Uma pendência de tempo se resolve esperando; uma
pendência de acesso, não. É por isso que o Reddit é o ambiente recomendado a quem queira
dar continuidade a este protocolo depois desta dissertação.

"""

s = s[:ini] + CAP6 + BARRA + "\n" + CAP7 + s[fim:]

# --- as 10 referencias externas, reapontadas UMA A UMA ----------------
# Casa por contexto (as ~240 letras antes da chamada), e nao por trecho
# literal: o .tex quebra linha em lugares imprevisiveis. Cada ocorrencia e
# classificada e substituida pela posicao.
#
# MAPA (o que cada uma diz -> para onde passa a apontar):
#   "corte de vinte arestas ... papeis sociais"      -> papeis
#   "papeis sociais no Reddit sao locais"            -> papeis
#   "Rede e papeis sociais" (tab:analises)           -> papeis
#   "a homofilia prediz melhor que a influencia"     -> homofilia
#   "Homofilia e classificacao" (tab:analises)       -> homofilia
#   "caso de homofilia ... tempo de transferencia"   -> homofilia
#   "predicao ja registrada"                         -> homofilia
#   "os dois casos de Reddit"                        -> os DOIS
#   "Os dois casos executados no Reddit"             -> os DOIS
#   "montada pelos dois casos executados"            -> os DOIS
REGRAS = [
    ("vinte arestas",                 "papeis"),
    ("s\u00e3o locais",                   "papeis"),
    ("Rede e pap\u00e9is sociais",         "papeis"),
    ("homofilia prediz melhor",       "homofilia"),
    ("Homofilia e classifica\u00e7\u00e3o",   "homofilia"),
    ("tempo de transfer\u00eancia",        "homofilia"),
    ("predi\u00e7\u00e3o j\u00e1 registrada",     "homofilia"),
    ("os dois casos de Reddit",       "dois"),
    ("dois casos executados no Reddit", "dois"),
    ("dois casos executados nessa plataforma", "dois"),
]

ALVO = {"papeis": "cap:caso-papeis", "homofilia": "cap:caso-homofilia"}
DOIS = ("Cap\u00edtulos~\\ref{cap:caso-papeis} "
        "e~\\ref{cap:caso-homofilia}")

ocor = [m for m in re.finditer(r"(Cap\u00edtulos?~)?\\ref\{cap:caso-reddit\}", s)]
if len(ocor) != 10:
    raise SystemExit("[erro] esperava 10 chamadas, achei %d" % len(ocor))

feitas = []
for m in reversed(ocor):                       # de tras para frente: indices estaveis
    ctx = " ".join(s[max(0, m.start() - 260):m.start()].split())  # colapsa quebras
    tipo = next((t for chave, t in REGRAS if chave in ctx), None)
    if tipo is None:
        raise SystemExit("[erro] nao classifiquei:\n...%s" % " ".join(ctx[-160:].split()))
    if tipo == "dois":
        novo = DOIS
    else:
        novo = (m.group(1) or "") + "\\ref{%s}" % ALVO[tipo]
    s = s[:m.start()] + novo + s[m.end():]
    feitas.append(tipo)

print("reapontadas:", {t: feitas.count(t) for t in set(feitas)})
if "cap:caso-reddit" in s:
    raise SystemExit("[erro] sobrou referencia ao label antigo")

tmp = P + ".tmp"
with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
    fh.write(s)
os.replace(tmp, P)
print("capitulo dividido: Cap. 6 (papeis sociais) + Cap. 7 (homofilia)")
print("10 referencias externas reapontadas; nenhuma sobrou apontando para o label antigo")
