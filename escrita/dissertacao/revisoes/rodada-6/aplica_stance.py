# -*- coding: utf-8 -*-
"""Leva o eixo de *stance* do caso de 2014 para o corpo da dissertacao (9/set/2026).

O eixo estava declarado como pendente em quatro lugares do texto e como uma das
tres linhas em aberto da tabela mestre. Ele fechou hoje:

  - gabarito humano: 210 do teste cego, rotulados a mao (Mariana), amostra
    congelada em 18/ago (sha dc8ee39ff69b);
  - rotulador automatico: REPROVADO no criterio pre-registrado (kappa 0,604 <
    0,70; portao 0,781 < 0,90). O criterio NAO foi alterado;
  - teto da tarefa, medido nas duplicatas do dev: kappa 0,625 excluindo a
    manchete que o codebook so passou a tratar depois (0,198 com ela). O
    rotulador esta a dois centesimos do teto;
  - estimativa corrigida sobre 5.000 tweets do universo, pela inversao da matriz
    de confusao, com bootstrap nas duas fontes de incerteza.

O desfecho e de dois sinais, e e assim que vai ao texto: o NDA muda muito e
converge cedo; a ordenacao EA/ED fica INDETERMINADA -- e a indeterminacao e de
instrumento, nao de volume, porque a curva e plana desde n=100.
"""
import io
import os
import re

P = (r"c:\Users\maria\Documents\GitHub\dissertacao-mestrado\escrita\dissertacao"
     r"\corpo.tex")
s = io.open(P, encoding="utf-8", newline="").read()

if "sec:stance" in s:
    raise SystemExit("[parado] ja aplicado.")


def rep(old, new, n=1):
    """Substitui tolerando quebras de linha: o .tex quebra onde quer, entao
    qualquer corrida de espaco no padrao casa qualquer corrida de espaco no
    arquivo."""
    global s
    if s.count(old) == n:
        s = s.replace(old, new)
        return
    padrao = r"\s+".join(re.escape(p) for p in old.split())
    achados = list(re.finditer(padrao, s))
    assert len(achados) == n, (len(achados), n, old[:70])
    for m in reversed(achados):
        s = s[:m.start()] + new + s[m.end():]


# ---------------------------------------------------------------- [1]
rep("""Os
resultados abaixo cobrem o eixo de mídia (classificação vertical\\slash
horizontal), determinístico e já rodado em escala; os eixos de stance
(preferência eleitoral) e de temas dependem de rotulagem manual ainda em
curso e não são avaliados aqui.""",
    """Os
resultados abaixo cobrem dois eixos: o de mídia (classificação vertical\\slash
horizontal), determinístico e rodado em escala, e o de \\emph{stance} (preferência
eleitoral), que exigiu construir um gabarito humano e é relatado na
Seção~\\ref{sec:stance}. O eixo de temas depende de rotulagem manual ainda não
feita e não é avaliado aqui.""")

# ---------------------------------------------------------------- [2]
SECAO = """\\section{O eixo de \\emph{stance}, e um limite que não é de volume}
\\label{sec:stance}

A afirmação de \\emph{stance} é a mais forte do artigo. Dos setecentos tweets lidos,
666 foram atribuídos a perfis individuais, e destes 42,6\\% receberam o rótulo de
eleitor de Dilma, 33,9\\% o de eleitor de Aécio e 23,4\\% nenhum dos dois. É dela que
decorre a tese de que os públicos dos dois candidatos diferem.

Testá-la exigiu construir o instrumento que o artigo não publica. Da mesma janela de
19 a 25 de outubro, com 32.193 tweets, sorteou-se uma amostra aleatória estratificada
por dia de 320 itens, congelada com semente antes de qualquer medição; 110 serviram
para calibrar o procedimento e os \\textbf{210} restantes formaram um teste cego,
rotulados à mão sob um codebook derivado do método descrito no artigo.\\footnote{Amostra,
critérios de aceite e predições foram registrados em pré-registro antes de medir
(\\texttt{PRE\\_REGISTRO\\_stance.md}); os números desta seção provêm dos scripts
\\texttt{valida\\_rotulador.py} e \\texttt{estima\\_universo.py} do projeto de replicação.}

O gabarito humano já desloca a afirmação, e por muito. A fatia sem lado atribuível é
de \\textbf{71,4\\%} (IC95\\% [65,0; 77,1]) contra os 23,4\\% publicados, e mesmo
descartando todo item que a anotadora classificou como ambíguo restam 45,7\\% de
tweets sem preferência inequívoca --- ainda o dobro do total do artigo. Entre os que
recebem lado, 66,7\\% são de eleitor de Aécio, quando o artigo reporta maioria de
eleitores de Dilma. Parte dessa diferença é conhecida e tem direção conhecida: o
artigo amostrou o pico das 21 horas, onde o conteúdo é mais politizado, e os
encurtadores de 2014 hoje estão mortos, o que empurra itens para a categoria sem
lado. Mas as duas causas somadas não cobrem uma distância dessa ordem.

O passo seguinte do protocolo seria estender o rótulo ao universo por um classificador
automático, e é aqui que o caso encontra um limite de outra natureza. O classificador
foi medido uma única vez contra o teste cego, com o prompt congelado, e
\\textbf{reprovou} nos dois critérios escritos antes da medição: $\\kappa$ de Cohen de
0,604 contra o mínimo de 0,70, e acurácia de 78,1\\% no portão de conta contra o mínimo
de 90\\%. A reprovação fica registrada como tal, e o critério não foi revisto depois de
conhecido o resultado.

O que torna a reprovação interpretável é o teto da tarefa. O codebook manda rotular de
novo cada texto repetido, sem consultar o rótulo anterior, e a fase de calibragem
respeitou essa regra: há ali quinze pares em que a mesma pessoa decidiu duas vezes
sobre o mesmo texto, às cegas. A concordância dela consigo mesma é de $\\kappa=0{,}198$
sobre os quinze pares e de $0{,}625$ excluindo uma única manchete ambígua --- a de que
a irmã de Lula pedira votos para Aécio ---, que foi justamente o caso que levou à
criação de uma regra nova no codebook. Sob qualquer das duas leituras, o classificador
não está longe do máximo alcançável: ele reproduz o rótulo humano quase tão bem quanto
a própria anotadora reproduz o seu.

Um classificador reprovado ainda serve para estimar proporções, desde que o viés seja
corrigido em vez de ignorado. A matriz de confusão medida nos 210 diz o tamanho e a
direção do erro, e permite inverter a estimativa que ele produz.\\footnote{A correção
é declaradamente \\emph{post hoc}, e foi registrada no pré-registro antes de ser
executada. Ela não reabilita o classificador como instrumento de rótulo individual,
nem substitui o critério de aceite, que continua reprovado.} Aplicado a uma amostra
de 5.000 tweets do universo, o classificador atribui lado a 40,1\\% deles; corrigido,
o valor cai para 34,2\\%, e a fatia sem lado sobe a \\textbf{65,8\\%} (IC95\\%
[52,5; 75,1]). A correção anda na direção prevista, porque o erro dominante do
classificador é atribuir lado onde a anotadora não viu nenhum.

A conclusão do artigo, porém, não é adjudicada. A razão entre eleitores de Aécio e de
Dilma é de 1,01 na estimativa corrigida, contra 0,80 no artigo, mas o intervalo de
confiança vai de 0,36 a 2,35 e contém os dois valores. A causa da largura não é o
tamanho da coleta: a curva $A(\\text{volume})$ é praticamente plana desde cem tweets e
satisfaz o critério de convergência pré-registrado em dois mil. O que a alarga é a
matriz, estimada sobre vinte itens da classe menos frequente, e a inversão amplifica
essa imprecisão.

É um desfecho que o protocolo não previa, e que vale registrar como categoria. A
pergunta do volume tem resposta clara --- coletar mais não move o número, e a
composição já estava assentada muito antes do que o artigo coletou. A pergunta
substantiva não tem, porque o teto da tarefa de rotulagem não sustenta a distinção que
o artigo faz. A conclusão publicada não é confirmada nem refutada: ela é
\\emph{indecidível} com o instrumento que a tarefa admite. Diferentemente da
indeterminação de causa que o caso do YouTube encontrou
(Capítulo~\\ref{cap:caso-youtube}), esta é uma indeterminação de instrumento, e ela não
se resolve coletando mais.

"""

alvo = "\\section{Leitura em termos de volume}"
i_cap4 = s.index("\\chapter{Primeiro Caso Executado")
i_cap5 = s.index("\\chapter{Segundo Caso Executado")
i_sec = s.index(alvo, i_cap4)
assert i_sec < i_cap5, "achei a secao errada"
s = s[:i_sec] + SECAO + s[i_sec:]

# ---------------------------------------------------------------- [3]
rep("""Falta ainda o eixo de stance (a tese H3, de que os públicos diferem),
dependente de rotulagem manual. É onde o artigo faz sua afirmação mais forte e
onde o teste de volume será mais informativo.""",
    """O eixo de \\emph{stance} (Seção~\\ref{sec:stance}) acrescenta a esse quadro um
desfecho de terceiro tipo. Ali a resposta de volume é limpa --- a composição não se
move a partir de cem tweets ---, mas a afirmação do artigo permanece indecidível,
porque o teto da própria tarefa de rotulagem não sustenta a distinção que ela faz.
Sub-coleta e limite de instrumento são coisas distintas, e o protocolo só separa uma
da outra porque mede as duas.""")

# ---------------------------------------------------------------- [4]
rep("""\\midrule
Deleção política (TikTok)""",
    """\\midrule
\\#Eleições\\-2014 (Twitter)
 & Sentimento
 & entre os cidadãos, 42,6\\% são eleitores de Dilma contra 33,9\\% de Aécio
 & \\textbf{sim} na fatia sem lado (23,4\\% $\\to$ 65,8\\%); \\textbf{indecidível} na razão entre os lados (1,01; IC95\\% [0,36; 2,35])
 & \\textbf{sim}, em $n\\approx2.000$; a curva é plana desde $n=100$, e o que limita é o instrumento, não o volume \\\\
\\midrule
Deleção política (TikTok)""")

# ---------------------------------------------------------------- [5]
rep("""As três linhas ainda em aberto do conjunto --- os dois eixos do caso
de tópicos em Twitter, que aguarda dados, e o eixo de \\emph{stance} do caso de 2014, que
aguarda rotulagem humana --- não figuram aqui.""",
    """As duas linhas ainda em aberto do conjunto --- os dois eixos do caso
de tópicos em Twitter, que aguarda dados --- não figuram aqui.""")

# ---------------------------------------------------------------- [6] e [7]
rep("Ela reúne quinze linhas fechadas, distribuídas pelos seis casos",
    "Ela reúne dezesseis linhas fechadas, distribuídas pelos seis casos")
rep("quatro das quinze linhas ---, e por isso viaja dentro da célula",
    "cinco das dezesseis linhas ---, e por isso viaja dentro da célula")
rep("""hoje anotada em quatro das quinze linhas fechadas da tabela mestre""",
    """hoje anotada em cinco das dezesseis linhas fechadas da tabela mestre""")

# ---------------------------------------------------------------- [8]
rep("""  \\item fechar o caso do Twitter: rotular stance (EA/ED) e temas,
  validar os classificadores contra rótulo humano e testar a tese central H3 (os
  públicos diferem?), o eixo em que o artigo faz sua afirmação mais forte;""",
    """  \\item fechar o eixo de temas do caso do Twitter, o único dos três que segue sem
  rotulagem. E, quanto ao eixo de \\emph{stance}, atacar o que ficou indecidível pelo
  lado do instrumento, e não pelo da coleta: medir o teto da tarefa por reteste
  intracodificador, que a versão atual estimou apenas pelas duplicatas, e ampliar o
  gabarito na classe menos frequente, que é o que estreitaria o intervalo da razão
  entre os lados (Seção~\\ref{sec:stance});""")

tmp = P + ".tmp"
with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
    fh.write(s)
os.replace(tmp, P)
print("stance aplicado ao corpo.tex: 8 edicoes")
