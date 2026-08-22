#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rodada de revisao 5 -> 6. Aplica no fonte LaTeX os 23 comentarios do
revisao-5.pdf. Escrita atomica (.tmp + os.replace); cada substituicao
verifica que o trecho procurado aparece exatamente uma vez."""

import io
import os

BASE = r"c:\Users\maria\Documents\GitHub\dissertacao-mestrado\escrita\dissertacao"
CORPO = os.path.join(BASE, "corpo.tex")
TESE = os.path.join(BASE, "dissertacao.tex")
BIB = os.path.join(BASE, "referencias.bib")


def ler(caminho):
    with io.open(caminho, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def grava(caminho, texto):
    tmp = caminho + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(texto)
    os.replace(tmp, caminho)


class Doc(object):
    def __init__(self, caminho):
        self.caminho = caminho
        self.s = ler(caminho)

    def rep(self, old, new, n=1):
        c = self.s.count(old)
        if c == 0 and new and self.s.count(new) >= 1:
            return  # ja aplicado numa execucao anterior
        assert c == n, (self.caminho, c, n, old[:90])
        self.s = self.s.replace(old, new)

    def salva(self):
        grava(self.caminho, self.s)


# =====================================================================
# dissertacao.tex -- legendas e colocacao de floats (comentarios 2 e 14)
# =====================================================================
t = Doc(TESE)

t.rep(
    r"""\usepackage[alf,bibjustif,abnt-emphasize=bf]{abntex2cite}

\npthousandsep{.}""",
    r"""\usepackage[alf,bibjustif,abnt-emphasize=bf]{abntex2cite}

%% --- Legendas de tabelas e figuras -----------------------------------
%% Pedido recorrente da revisao: a legenda vinha no mesmo corpo e na mesma
%% fonte do texto e se confundia com ele. Aqui ela fica menor, com o rotulo
%% em negrito, travessao no lugar dos dois-pontos e recuo das margens do
%% bloco de texto.
\captionsetup{font=footnotesize,labelfont=bf,labelsep=endash,
              justification=raggedright,singlelinecheck=false,
              margin=14pt,skip=6pt,belowskip=2pt}

%% --- Colocacao de floats ---------------------------------------------
%% Sem afrouxar estes parametros o LaTeX empurra tabela grande para pagina
%% propria, longe do trecho que a discute.
\renewcommand{\topfraction}{0.85}
\renewcommand{\bottomfraction}{0.70}
\renewcommand{\textfraction}{0.10}
\renewcommand{\floatpagefraction}{0.75}
\setcounter{topnumber}{3}
\setcounter{totalnumber}{4}

\npthousandsep{.}""",
)

t.salva()


# =====================================================================
# referencias.bib -- a dissertacao do Heine (comentario 12)
# =====================================================================
b = Doc(BIB)

b.rep(
    r"""@inproceedings{salgueiro2022dbmodels,""",
    r"""@mastersthesis{heine2025amostragem,
  author = {Heine, Alexandre A. P.},
  title  = {Um Estudo sobre Amostragem em Grandes Volumes de Dados em Redes Sociais Digitais},
  school = {Pontif\'icia Universidade Cat\'olica do Rio de Janeiro (PUC-Rio)},
  year   = {2025},
  type   = {Disserta\c{c}\~ao de Mestrado},
  address= {Rio de Janeiro},
  note   = {Departamento de Inform\'atica. Orientador: S\'ergio Lifschitz}
}

@inproceedings{salgueiro2022dbmodels,""",
)

b.salva()


# =====================================================================
# corpo.tex
# =====================================================================
c = Doc(CORPO)

# --- [1] p.12: o paragrafo do Salgueiro nao abre bem a dissertacao ----
c.rep(
    r"""Uma palavra antes sobre o termo. \emph{Redes sociais digitais} (RSD) é empregado
aqui no sentido que lhe dá \citeonline{salgueiro2023}, em trabalho desenvolvido no
mesmo grupo de pesquisa: o de plataformas que, por baixo de interfaces e modelos de
negócio distintos, compartilham uma estrutura conceitual comum --- atores, laços entre
atores e conteúdo publicado --- a ponto de admitirem uma especificação única. É essa
estrutura comum que autoriza tratar Twitter/X, Reddit, YouTube e TikTok como
instâncias de um mesmo objeto ao longo desta dissertação, ainda que a unidade
efetivamente coletada mude de uma para outra.

Para fundamentar a motivação, este trabalho conduziu um levantamento
sistemático da literatura que emprega coleta automatizada em RSD, reportado em
artigo autônomo~\cite{barreto2026survey}.""",
    r"""Para fundamentar a motivação, este trabalho conduziu um levantamento sistemático
da literatura que emprega coleta automatizada em redes sociais digitais (RSD ---
plataformas que, sob interfaces e modelos de negócio distintos, compartilham a mesma
estrutura de atores, laços entre atores e conteúdo publicado, o que autoriza tratar
Twitter/X, Reddit, YouTube e TikTok como instâncias de um mesmo objeto; conceito
discutido em detalhe por \citeonline{salgueiro2023}, no mesmo grupo de pesquisa),
reportado em artigo autônomo~\cite{barreto2026survey}.""",
)

# --- [2] legenda da Tab. 1.1: uma frase; o resto vira nota sob a tabela
c.rep(
    r"""\begin{table}[t]
\centering
\caption[Tipos de análise no corpus do levantamento]{Tipos de análise no corpus do levantamento ($N=2.139$
artigos)~\cite{barreto2026survey}. ``Análise de conteúdo'' (1.396 menções) é
omitida por ser um guarda-chuva, não um método.}
\label{tab:analises-survey}""",
    r"""\begin{table}[htbp]
\centering
\caption[Tipos de análise no corpus do levantamento]{Tipos de análise no corpus do
levantamento ($N=2.139$ artigos).}
\label{tab:analises-survey}""",
)

c.rep(
    r"""Análise de rede        & 527 & 24,6 & Clusterização        & 157 & 7,3 \\
\bottomrule
\end{tabular}
\end{table}""",
    r"""Análise de rede        & 527 & 24,6 & Clusterização        & 157 & 7,3 \\
\bottomrule
\end{tabular}

\vspace{2pt}
{\footnotesize \textit{Notas.} Fonte: \citeonline{barreto2026survey}. Um mesmo artigo
pode empregar mais de um tipo de análise, de modo que os percentuais não somam 100\%.
``Análise de conteúdo'' (1.396 menções) é omitida por ser um guarda-chuva, e não um
método.\par}
\end{table}""",
)

# --- [3] p.14: o que e "evidencia transferivel" -----------------------
c.rep(
    r"""Mais do que caracterizar as RSD, o alvo é produzir, no domínio em que o
efeito é mensurável, evidência transferível sobre para quais tipos de análise o
volume de coleta é decisivo, e não uma prescrição numérica única de quanto
coletar.""",
    r"""Mais do que caracterizar as RSD, o alvo é produzir evidência sobre para
quais tipos de análise o volume de coleta é decisivo, e não uma prescrição numérica
única de quanto coletar. Essa evidência é obtida nas RSD por serem o domínio em que o
efeito é mensurável, mas o que ela descreve é o \emph{tipo de análise}, e não a
plataforma: dizer que uma partição de comunidades se desfaz com pouco dado, e que uma
proporção agregada não se desfaz, não é um enunciado sobre o Twitter ou sobre o
Reddit, e vale, em princípio, onde quer que essas mesmas análises sejam feitas.""",
)

# --- [4] p.16: abertura do Cap. 2 soa defensiva -----------------------
c.rep(
    r"""A pergunta desta dissertação --- coletar mais muda a conclusão? --- encosta em quatro
linhas de trabalho que já existem e não se confundem com ela. A primeira mede o quanto
uma amostra devolvida por um canal de coleta difere do todo. A segunda faz a crítica
metodológica do dado social e prescreve o que declarar. A terceira replica achados
publicados. A quarta estuda a sensibilidade de métodos específicos ao dado disponível.
Este capítulo percorre as quatro e termina dizendo, com toda a clareza possível, o que
resta por fazer e que este trabalho faz.""",
    r"""A pergunta desta dissertação --- coletar mais muda a conclusão? --- apoia-se em
quatro linhas de trabalho já estabelecidas. A primeira mede o quanto uma amostra
devolvida por um canal de coleta difere do todo. A segunda faz a crítica metodológica
do \emph{dado social} --- o rastro que as plataformas guardam do comportamento de seus
usuários --- e prescreve o que declarar ao publicar. A terceira replica achados
publicados. A quarta estuda a sensibilidade de métodos específicos ao dado disponível.
Este capítulo percorre as quatro, dizendo de cada uma o que ela já resolve, e termina
localizando na Seção~\ref{sec:rel-lacuna} o ponto em que este trabalho se insere.""",
)

# --- [5] titulos das secoes do Cap. 2 com o autor de referencia -------
c.rep(
    r"""\section{A amostra contra o todo: o que os canais de coleta devolvem}""",
    r"""\section[A amostra contra o todo: Morstatter e a linha que se seguiu]{A amostra
contra o todo: Morstatter e a linha que se seguiu}""",
)
c.rep(
    r"""\section{A crítica metodológica ao dado social}""",
    r"""\section[A crítica metodológica ao dado social: de boyd e Crawford ao erro
total]{A crítica metodológica ao dado social: de boyd e Crawford ao erro total}""",
)
c.rep(
    r"""\section{Replicação em ciência social computacional}""",
    r"""\section[Replicação em ciência social computacional: Liang e Fu]{Replicação em
ciência social computacional: Liang e Fu}""",
)
c.rep(
    r"""\section{A sensibilidade dos métodos ao dado disponível}""",
    r"""\section[A sensibilidade dos métodos ao dado disponível: de Kossinets ao
multiverso]{A sensibilidade dos métodos ao dado disponível: de Kossinets ao
multiverso}""",
)

# Morstatter como o trabalho que inaugura a linha
c.rep(
    r"""A linha mais próxima em espírito compara o que uma interface de coleta entrega com o
que existe do outro lado dela. O trabalho de referência é
\citeonline{morstatter2013sample}, que confrontou a amostra da \emph{Streaming API} do
Twitter com o \emph{Firehose} completo sobre o mesmo período, comparando métricas de
tópicos, de rede e de localização.""",
    r"""A linha mais próxima em espírito compara o que uma interface de coleta entrega com o
que existe do outro lado dela. Ela começa em \citeonline{morstatter2013sample}, que
confrontou a amostra da \emph{Streaming API} do Twitter com o \emph{Firehose} completo
sobre o mesmo período, comparando métricas de tópicos, de rede e de localização; os
trabalhos citados a seguir são desdobramentos desse desenho.""",
)

# --- [9] "dado social": definir na secao que leva o termo no titulo ---
c.rep(
    r"""Uma segunda linha, mais antiga e mais ampla, discute o que se pode e o que não se pode
afirmar a partir de rastros de plataforma.""",
    r"""\emph{Dado social} é a tradução corrente de \emph{social data}: o registro que as
plataformas guardam do comportamento de quem as usa --- publicações, curtidas,
compartilhamentos, laços de seguidor, buscas. A característica que importa aqui é que
ninguém o produziu para pesquisar coisa alguma. Ele é subproduto do funcionamento da
plataforma, e chega ao pesquisador já recortado por ela. Uma segunda linha de trabalho,
mais antiga e mais ampla que a anterior, discute o que se pode e o que não se pode
afirmar a partir dele.""",
)

# --- [6] boyd em minuscula: nota de rodape ----------------------------
c.rep(
    r"""provocações fundadoras, entre elas a de que dado grande não é automaticamente dado bom.""",
    r"""provocações fundadoras, entre elas a de que dado grande não é automaticamente dado
bom.\footnote{A grafia do sobrenome em minúscula, aqui e nas referências, é a que a
própria autora adota e registra em suas publicações. Não é erro tipográfico.}""",
)

# --- [8] Ruths e Pfeffer: dizer o que eles de fato apontam ------------
c.rep(
    r"""\citeonline{ruths2014socialmedia} argumentaram, em termos normativos, que
estudos de comportamento em larga escala precisam ser submetidos a padrões
metodológicos mais altos.""",
    r"""\citeonline{ruths2014socialmedia} dirigiram a mesma preocupação
especificamente às RSD, apontando três coisas: cada plataforma tem a sua própria
população de usuários e os seus próprios mecanismos de exibição, de modo que um achado
obtido numa delas não se transfere para as outras; o material recolhido por
palavra-chave, por \emph{hashtag} ou pelo que uma interface proprietária resolve
devolver não é amostra de população nenhuma bem definida; e contas automatizadas
entram na contagem sem se distinguirem das humanas. A recomendação deles é de relato:
declarar como o conjunto foi obtido e por quais filtros passou, sob pena de o
resultado não ser interpretável por quem lê.""",
)

# --- [7] Sen et al.: reescrever a frase do erro total -----------------
c.rep(
    r"""e \citeonline{sen2021tedon} propuseram um arcabouço de erro total para
rastros digitais, transposto do erro total de pesquisas amostrais.""",
    r"""e \citeonline{sen2021tedon} adaptaram para rastros digitais a
contabilidade de erro que a pesquisa por amostragem já fazia: em vez de tratar o viés
como um problema único, decompõem o percurso do dado --- quem está na plataforma, o
que a plataforma registra, o que a interface devolve, o que o pesquisador filtra --- e
localizam em cada etapa o erro que ela introduz.""",
)

# --- [10] "que conclusoes ficam ao alcance" ---------------------------
c.rep(
    r"""\citeonline{mayr2017think} montaram vários conjuntos de dados sobre o mesmo evento --- as
eleições alemãs de 2013 --- por métodos de coleta distintos, para mostrar que a
estratégia de coleta determina que conclusões ficam ao alcance.""",
    r"""\citeonline{mayr2017think} montaram vários conjuntos de dados sobre o mesmo evento --- as
eleições alemãs de 2013 --- por métodos de coleta distintos, e mostraram que os
conjuntos resultantes diferem em tamanho, em composição e em quais contas aparecem como
centrais. A escolha do método de coleta, feita antes de qualquer análise, já delimita
portanto que perguntas o material recolhido poderá responder.""",
)

# --- [11] "insumo empirico" -------------------------------------------
c.rep(
    r"""É
exatamente essa medida que o protocolo do Capítulo~\ref{cap:experimento} instrumenta, e
dela que sai o insumo empírico para dizer quando a ressalva é indispensável e quando é
dispensável.""",
    r"""É
exatamente essa medida que o protocolo do Capítulo~\ref{cap:experimento} instrumenta, e
é dela que sai a evidência para dizer quando a ressalva é indispensável e quando é
dispensável.""",
)

# --- [12] a dissertacao do Heine entra em trabalhos relacionados ------
c.rep(
    r"""O que separa toda essa linha do que se faz aqui é o objeto medido.""",
    r"""Dentro do mesmo grupo de pesquisa em que esta dissertação foi desenvolvida,
\citeonline{heine2025amostragem} fez a pergunta pela via oposta. Em vez de comparar o
que uma interface devolve com um todo que ela não alcança, partiu de uma coleta própria
já completa --- 57,9 milhões de tweets das eleições brasileiras de 2022 --- e dela
extraiu amostras, aleatórias e estratificadas, para verificar se reproduziam o conjunto
de onde saíram. Não reproduziram: os tópicos obtidos da amostra divergem dos do
conjunto completo em ordem e em proporção, e o tamanho de amostra calculado pela
fórmula usual para proporções não garantiu a estabilidade da quantidade que de fato
interessava. É o antecedente mais direto deste trabalho, e a diferença está no alcance:
ali a comparação é entre amostra e todo, num único corpus, feita pelo próprio autor do
corpus e sobre um tipo de análise; aqui ela é entre a coleta de um artigo publicado e
um superconjunto do mesmo tema, ao longo de volumes crescentes e de seis tipos de
análise. Uma réplica daquele trabalho pelo protocolo desta dissertação está preparada
e aguarda acesso aos dados originais, e é uma das linhas ainda em aberto da
Tabela~\ref{tab:mestre}.

O que separa toda essa linha do que se faz aqui é o objeto medido.""",
)

# --- [13] fechamento do Cap. 2: cortar a primeira ressalva ------------
c.rep(
    r"""respostas separadamente --- se a afirmação mudou e se ela já estava estável. É esse o
espaço que esta dissertação ocupa.""",
    r"""respostas separadamente --- se a afirmação mudou e se ela já estava estável. É esse o
espaço que esta dissertação ocupa: não o de contestar as quatro linhas, que ela toma
como estabelecidas e das quais tira o seu instrumental, mas o de responder à pergunta
que nenhuma delas formula --- se a afirmação que um artigo publicou sobrevive a ter
sido feita sobre mais dado do mesmo tema.""",
)

c.rep(
    r"""Duas ressalvas honestas fecham o capítulo. A primeira é que a busca por trabalhos
``extremamente parecidos'' não retornou nenhum, mas isso vale para o que este
levantamento alcançou, e não é prova de inexistência --- a mesma restrição de acesso a
texto completo que a Seção~\ref{sec:contexto-survey} declara sobre o levantamento
sistemático se aplica aqui. A segunda é que a ausência de trabalho idêntico não é, por
si, mérito: parte da explicação para ela está na dificuldade de montar o superconjunto,
que a Seção~\ref{sec:coleta-plataforma} percorre plataforma a plataforma e que, em
duas das seis células deste trabalho, só foi contornada por acervo preservado.""",
    r"""Uma ressalva fecha o capítulo. Que não se tenha encontrado trabalho com esse desenho
não é, por si, mérito: parte da explicação está na dificuldade de montar o
superconjunto, que a Seção~\ref{sec:coleta-plataforma} percorre plataforma a plataforma
e que, em duas das seis células deste trabalho, só foi contornada por acervo
preservado. O espaço existe, em boa medida, porque ocupá-lo depende de um acesso ao
dado que nem toda plataforma concede.""",
)

# --- [14] colocacao das tabelas do Cap. 3 -----------------------------
c.rep(
    r"""\begin{table}[t]
\centering
\caption[Eixos de expansão da coleta]""",
    r"""\begin{table}[htbp]
\centering
\caption[Eixos de expansão da coleta]""",
)
c.rep(
    r"""\begin{table}[t]
\centering\footnotesize
\caption[O que foi comparado em cada tipo de análise]""",
    r"""\begin{table}[htbp]
\centering\footnotesize
\caption[O que foi comparado em cada tipo de análise]""",
)

# --- [2/14] legenda da tab:casos: uma frase; o resto vira nota --------
c.rep(
    r"""\begin{table}[t]
\centering\footnotesize
\caption[O conjunto de casos do estudo]{O conjunto de casos do estudo, cobrindo os tipos de análise mais
recorrentes do levantamento em quatro redes sociais, na ordem em que são relatados
(Capítulos~\ref{cap:caso-twitter} a~\ref{cap:caso-tiktok}). Cinco foram executados
por inteiro; no último, o de TikTok, o ponto original do alvo é reproduzido mas a
expansão de coleta não chega a ocorrer, por credencial revogada.}
\label{tab:casos}""",
    r"""\begin{table}[htbp]
\centering\footnotesize
\caption[O conjunto de casos do estudo]{O conjunto de casos do estudo, na ordem em que
são relatados.}
\label{tab:casos}""",
)

c.rep(
    r"""Análise de conteúdo & TikTok (PoliTok-DE 2025) & 939 mil posts de duas eleições alemãs; disponibilidade checada em datas fixas & eixo temporal: rechecagem em datas sucessivas \\
\bottomrule
\end{tabularx}
\end{table}""",
    r"""Análise de conteúdo & TikTok (PoliTok-DE 2025) & 939 mil posts de duas eleições alemãs; disponibilidade checada em datas fixas & eixo temporal: rechecagem em datas sucessivas \\
\bottomrule
\end{tabularx}

\vspace{2pt}
{\footnotesize \textit{Notas.} Os seis casos cobrem quatro redes sociais e os tipos de
análise mais recorrentes do levantamento, e são relatados nos
Capítulos~\ref{cap:caso-twitter} a~\ref{cap:caso-tiktok}. Cinco foram executados por
inteiro; no último, o de TikTok, o ponto original do alvo é reproduzido mas a expansão
de coleta não chega a ocorrer, por credencial revogada.\par}
\end{table}""",
)

# --- [2] legendas das demais tabelas: uma frase + nota ----------------
c.rep(
    r"""\caption[Participação em mais de uma comunidade, por recorte de coleta]{Participação em mais de uma comunidade, por recorte de coleta. A
comparação que decide a questão é a da última linha, por ser a que aplica ao
universo o mesmo corte de atividade do artigo.}""",
    r"""\caption[Participação em mais de uma comunidade, por recorte de coleta]{Participação
em mais de uma comunidade, por recorte de coleta.}""",
)
c.rep(
    r"""\textbf{Universo, sob o mesmo corte de atividade} ($\geq$20 mensagens) & 5.991 & 3.450 & \textbf{57,6\%} \\
\bottomrule
\end{tabularx}
\end{table}""",
    r"""\textbf{Universo, sob o mesmo corte de atividade} ($\geq$20 mensagens) & 5.991 & 3.450 & \textbf{57,6\%} \\
\bottomrule
\end{tabularx}

\vspace{2pt}
{\footnotesize \textit{Notas.} A comparação que decide a questão é a da última linha,
por ser a única que aplica ao universo o mesmo corte de atividade do artigo.\par}
\end{table}""",
)

c.rep(
    r"""\caption[O funil de coleta do artigo replicado]{O funil de coleta do artigo replicado. As duas etapas de descarte usam o
mesmo critério, o de que a palavra buscada reapareça no título ou na descrição do
vídeo. É esse critério, de \emph{forma} e não de assunto, que o caso põe à prova.}""",
    r"""\caption[O funil de coleta do artigo replicado]{O funil de coleta do artigo
replicado, etapa a etapa.}""",
)
c.rep(
    r"""União dos dois ramos, após o filtro de idioma & 4.378 & 3.782 & 14\% \\
\bottomrule
\end{tabularx}
\end{table}""",
    r"""União dos dois ramos, após o filtro de idioma & 4.378 & 3.782 & 14\% \\
\bottomrule
\end{tabularx}

\vspace{2pt}
{\footnotesize \textit{Notas.} As duas etapas de descarte usam o mesmo critério, o de
que a palavra buscada reapareça no título ou na descrição do vídeo. É esse critério, de
\emph{forma} e não de assunto, que o caso põe à prova.\par}
\end{table}""",
)

c.rep(
    r"""\caption[Reprodução do ponto original sobre os dados publicados pelos autores]{Reprodução do ponto original sobre o conjunto de dados publicado pelos
próprios autores. Onde houve divergência, a causa foi sempre a mesma: um parâmetro
de convenção deixado implícito no artigo.}""",
    r"""\caption[Reprodução do ponto original sobre os dados publicados pelos
autores]{Reprodução do ponto original sobre o conjunto de dados publicado pelos
próprios autores.}""",
)
c.rep(
    r"""O corpus é dominado por veículos de imprensa & sem veredito & o artigo afirma as duas coisas opostas (próxima seção) e não publica os rótulos que decidiriam \\
\bottomrule
\end{tabularx}""",
    r"""O corpus é dominado por veículos de imprensa & sem veredito & o artigo afirma as duas coisas opostas (próxima seção) e não publica os rótulos que decidiriam \\
\bottomrule
\end{tabularx}

\vspace{2pt}
{\footnotesize \textit{Notas.} Onde houve divergência, a causa foi sempre a mesma: um
parâmetro de convenção deixado implícito no artigo.\par}""",
)

# --- [15] repeticoes de "convem" --------------------------------------
c.rep(
    r"""Convém precisar de onde vem o erro, porque a""",
    r"""Vale localizar de onde vem o erro, porque a""",
)
c.rep(
    r"""percentual, e convém dizer que ela não é um achado empírico surpreendente, para que""",
    r"""percentual, e é preciso dizer que ela não é um achado empírico surpreendente, para que""",
)
c.rep(
    r"""Convém precisar o que essa segunda constatação significa, porque ela não é uma""",
    r"""Cabe precisar o que essa segunda constatação significa, porque ela não é uma""",
)
c.rep(
    r"""afeta os dois lados da fração. Ao replicar por expansão, convém identificar antes""",
    r"""afeta os dois lados da fração. Ao replicar por expansão, é preciso identificar antes""",
)
c.rep(
    r"""Convém sublinhar que os achados acima são medições independentes, em três unidades""",
    r"""Note-se que os achados acima são medições independentes, em três unidades""",
)
c.rep(
    r"""Convém dizer com todas as letras o que isso significa e o que não significa.""",
    r"""Vale dizer com todas as letras o que isso significa e o que não significa.""",
)

# --- [19] "companion" em portugues ------------------------------------
c.rep(
    r"""da análise companion do projeto \texttt{pesquisa-twitter-refeita} (script""",
    r"""do projeto de replicação \texttt{pesquisa-twitter-refeita} (script""",
)
c.rep(
    r"""deste capítulo provêm do projeto companion do caso (scripts""",
    r"""deste capítulo provêm do projeto de replicação do caso (scripts""",
)
c.rep(
    r"""script \texttt{analise/rb3.py} do projeto companion, sobre um instantâneo próprio de""",
    r"""script \texttt{analise/rb3.py} do projeto de replicação, sobre um instantâneo próprio de""",
)
c.rep(
    r"""\texttt{analise/mh1\_ponto\_original.py} do projeto companion, sobre o conjunto de dados""",
    r"""\texttt{analise/mh1\_ponto\_original.py} do projeto de replicação, sobre o conjunto de dados""",
)
c.rep(
    r"""e \texttt{analise/fase3\_no\_tema.py} do projeto companion do caso, sobre o conjunto""",
    r"""e \texttt{analise/fase3\_no\_tema.py} do projeto de replicação do caso, sobre o conjunto""",
)

# --- [16] "codigos de estado" -----------------------------------------
c.rep(
    r"""A sétima não fecha, e falha pelo motivo que já se tornou recorrente neste conjunto de
casos. O artigo afirma que a plataforma, e não o autor, removeu 13,0\% de todas as
publicações, mas não informa quais códigos de estado atribui à plataforma. Testadas
cinco convenções plausíveis sobre os códigos disponíveis, a mais próxima produz
11,6\%, a 1,4 ponto percentual do publicado. A afirmação replica aproximadamente, sob
convenção que precisou ser reconstruída.

Também as duas afirmações de anotação replicam apenas sob uma convenção não declarada:
os valores publicados correspondem à contagem \emph{por anotação}, e não por post.
Como 300 dos 360 posts anotados receberam mais de uma anotação, contar por post com
voto majoritário desloca a intolerância de 20,5\% para 16,1\%. A conclusão qualitativa
sobrevive nas duas convenções; o número, não.""",
    r"""A sétima não fecha, e falha pelo motivo que já se tornou recorrente neste conjunto de
casos. O artigo afirma que a plataforma, e não o autor, removeu 13,0\% de todas as
publicações. Só que o que os autores publicam, para cada publicação que sumiu, não é o
motivo do sumiço: é o rótulo técnico que a interface do TikTok devolveu ao ser
consultada --- \texttt{status\_deleted}, \texttt{status\_reviewing},
\texttt{status\_audit\_not\_pass}, \texttt{author\_secret} e outros ---, e o artigo não
diz quais desses rótulos ele conta como remoção pela plataforma e quais atribui ao
autor. Testadas cinco atribuições plausíveis, a mais próxima produz 11,6\%, a 1,4 ponto
percentual do publicado. A afirmação replica aproximadamente, sob uma convenção que
precisou ser reconstruída.

As duas afirmações de anotação humana dependem, do mesmo modo, de uma convenção que o
artigo não declara: como a maior parte dos posts anotados recebeu mais de um rótulo,
contá-los por rótulo ou por post dá números diferentes, e a intolerância vai de 20,5\%
para 16,1\% conforme a escolha. Vale para elas o mesmo que valeu para os outros alvos
deste conjunto: a leitura qualitativa sobrevive às duas convenções, o número não.""",
)

# --- [18] §8.3 menos tecnica: a escolha da base vai para a nota -------
c.rep(
    r"""\vspace{2pt}
{\footnotesize \textit{Notas.} Painel é o conjunto de posts com estado válido nas
\emph{três} datas: 100.926 posts aqui, 102.953 no artigo. Dados em
\texttt{fase2\_politok.json}.\par}
\end{table}

A escolha da base não é detalhe. Cerca de 46\% da coleta não foi reverificada nas duas
primeiras datas, de modo que há três séries possíveis sobre o mesmo dado: a do painel,
acima; a dos posts efetivamente reverificados em cada data, que dá 6,3\%, 17,3\% e
18,9\%; e a que toma a coleta inteira como denominador, que dá 3,3\%, 9,5\% e 18,7\%.
Só a primeira é uma curva, porque só nela o denominador não muda de um ponto para o
outro. As outras duas misturam bases, e a terceira faz o crescimento parecer bem maior
do que ele é --- um lembrete de que o problema de escolher a base de comparação, que
atravessa todos os casos deste trabalho, também se aplica a ele próprio.

O que este caso acrescenta, então, não é o fato, e sim a consequência dele para o
protocolo.""",
    r"""\vspace{2pt}
{\footnotesize \textit{Notas.} Painel é o conjunto de posts com estado válido nas
\emph{três} datas: 100.926 posts aqui, 102.953 no artigo. Cerca de 46\% da coleta não
foi reverificada nas duas primeiras datas, e por isso o mesmo dado admite outras duas
séries, nenhuma delas uma curva: tomando os posts efetivamente reverificados em cada
data, 6,3\%, 17,3\% e 18,9\%; tomando a coleta inteira como denominador, 3,3\%, 9,5\% e
18,7\%. Dados em \texttt{fase2\_politok.json}.\par}
\end{table}

A escolha da base não é detalhe, e as notas da tabela registram as três séries que o
mesmo dado admite. Só a do painel é uma curva, porque só nela o denominador não muda de
um ponto para o outro; as outras duas misturam bases, e uma delas faz o crescimento
parecer bem maior do que é. O problema de escolher a base de comparação atravessa todos
os casos deste trabalho, e este não é exceção.

O que este caso acrescenta, então, não é o fato, e sim a consequência dele para o
protocolo.""",
)

c.rep(
    r"""A segunda pergunta não se responde, e é instrutivo que não se responda. O crescimento
desacelera --- 11,1 pontos percentuais entre a primeira e a segunda verificação, 3,5
entre a segunda e a terceira ---, o que sugere a mesma forma das curvas de volume dos
capítulos anteriores. Mas a coleta federal do mesmo artigo, verificada uma única vez
dezesseis meses depois da eleição, marca 39,7\%, quase o dobro do que a estadual marca
aos quatro meses e meio. Ou as duas eleições não são comparáveis --- e o próprio artigo
adverte que não as compara diretamente, justamente por terem horizontes distintos ---,
ou a curva temporal não havia assentado em lugar nenhum aos quatro meses e meio. Não há
como decidir entre as duas leituras com o que está publicado, e a resposta honesta é que
a convergência no eixo temporal fica em aberto. Vale registrar a assimetria: a pergunta
``mudou?'' se responde com uma única coleta reverificada, ao passo que a pergunta ``já
havia assentado?'' exigiria reverificações que se estendessem até a medida parar de
subir --- e ninguém sabe de antemão quando isso é.

Isso amplia o quadro que os casos anteriores vinham desenhando. O debate vacinal
mostrou que volume e largura de filtro são eixos independentes, que podem responder em
direções opostas. O caso do YouTube acrescentou a forma do critério de seleção. Este
acrescenta o momento. São quatro decisões de coleta que governam o resultado publicado,
e apenas a primeira é rotineiramente reportada. Para conclusões sobre conteúdo que a
plataforma modera, a data da coleta não é detalhe de procedimento: é parte da definição
da quantidade medida.""",
    r"""A segunda pergunta não se responde, e vale dizer por quê. O crescimento desacelera, o
que faria supor uma curva assentando. Mas a outra coleta do mesmo artigo, verificada uma
única vez dezesseis meses depois da eleição, marca 39,7\%, quase o dobro do que a
estadual marca aos quatro meses e meio --- e o próprio artigo adverte que as duas não
são diretamente comparáveis, por terem horizontes distintos. Ou a comparação não vale,
ou a curva ainda subia. Com o que está publicado não há como decidir, e a convergência
no eixo temporal fica declarada em aberto.

O que isso acrescenta ao trabalho é uma linha a mais na mesma lista. O debate vacinal
mostrou que o volume coletado e a largura do filtro temático são decisões independentes,
capazes de responder em direções opostas. O caso do YouTube acrescentou a forma do
critério de seleção. Este acrescenta a data. São quatro decisões de coleta capazes de
governar o resultado publicado, e apenas a primeira costuma ser reportada. Para
qualquer conclusão sobre conteúdo que a plataforma modera, dizer quanto se coletou sem
dizer quando se verificou é publicar um número sem sentido definido.""",
)

# --- [19] "companion" e paragrafo longo na abertura do Cap. 9 ---------
c.rep(
    r"""Esta dissertação articula um levantamento sistemático companion de~\citeonline{barreto2026survey} e um protocolo que dele decorre,
tomando as RSD como caso de estudo de uma pergunta metodológica mais
ampla, a de saber se coletar pouco ou muito muda a conclusão a que uma análise chega.
O levantamento mostra que a literatura de RSD dimensiona sua coleta por
conveniência e quase nunca verifica que o volume coletado bastava; o protocolo
propõe medir, diretamente, se coletar mais muda a conclusão e se coletar menos
teria bastado, por tipo de análise e por rede social, com um conjunto fixado de
casos replicáveis, distribuídos por quatro redes sociais
(Tabela~\ref{tab:casos}). Cinco deles foram executados por inteiro; no sexto, o de
TikTok, só o ponto original do alvo pôde ser reproduzido, porque a rota de coleta
estava fechada. A replicação de
\#Eleições2014 no Twitter (Capítulo~\ref{cap:caso-twitter}) mostra, no eixo de
mídia, os dois lados esperados.""",
    r"""Esta dissertação articula duas peças. A primeira é o levantamento sistemático
reportado em~\citeonline{barreto2026survey}, feito como parte do mesmo projeto, que
mostra que a literatura de RSD dimensiona sua coleta por conveniência e quase nunca
verifica que o volume coletado bastava. A segunda é um protocolo que dele decorre, e
que propõe medir diretamente, por tipo de análise e por rede social, se coletar mais
muda a conclusão e se coletar menos teria bastado. As duas tomam as RSD como caso de
estudo de uma pergunta metodológica mais ampla, a de saber se coletar pouco ou muito
muda a conclusão a que uma análise chega.

O protocolo foi instanciado por um conjunto fixado de casos replicáveis, distribuídos
por quatro redes sociais (Tabela~\ref{tab:casos}). Cinco deles foram executados por
inteiro; no sexto, o de TikTok, só o ponto original do alvo pôde ser reproduzido,
porque a rota de coleta estava fechada.

A replicação de \#Eleições2014 no Twitter (Capítulo~\ref{cap:caso-twitter}) mostra, no
eixo de mídia, os dois lados esperados.""",
)

c.rep(
    r"""Seção~\ref{sec:curva-midia}, a de se o esquema é não-viesado para a quantidade de
interesse, que passa a integrar o protocolo para todo alvo que amostra. A replicação do
debate vacinal de 2021--22""",
    r"""Seção~\ref{sec:curva-midia}, a de se o esquema é não-viesado para a quantidade de
interesse, que passa a integrar o protocolo para todo alvo que amostra.

A replicação do debate vacinal de 2021--22""",
)

# --- [20] as duas ultimas frases da §9.2 ------------------------------
c.rep(
    r"""Declarar o volume é prática de relato; poder alcançá-lo é
prática de infraestrutura. As duas se sustentam, e a segunda é a que decide se a
primeira terá algo de interessante para declarar.""",
    r"""Dito de outro modo: declarar quanto se coletou é uma questão de como se
escreve o artigo, mas poder coletar mais, para verificar se aquele volume bastava, é
uma questão de que infraestrutura se tem. Sem a segunda, a primeira declara um número
que ninguém consegue pôr à prova --- nem mesmo o autor que o declarou.""",
)

# --- [23] a teoria de amostragem sobe para o topo das limitacoes ------
c.rep(
    r"""  \item Cobertura por tipo de análise: os casos executados cobrem seis tipos, mas""",
    r"""  \item Teoria de amostragem fora do escopo: a questão estatística da amostragem
  --- garantias de representatividade, inferência de uma amostra para um todo --- não
  é tratada. O efeito do volume é medido empiricamente, comparando coletar mais e
  coletar menos sobre o mesmo tema, sem modelar a coleta como esquema de amostragem
  inferencial. Uma consequência prática é que este trabalho não diz quanto se deveria
  coletar; diz apenas se o que se coletou bastou para a conclusão que se tirou.

  \item Cobertura por tipo de análise: os casos executados cobrem seis tipos, mas""",
)

c.rep(
    r"""  \item Teoria de amostragem fora do escopo: a questão estatística de
  sampling (garantias de representatividade, inferência sobre um todo) não
  é tratada; o efeito do volume é medido empiricamente, comparando coletar
  mais e menos sobre o mesmo tema, sem modelar a coleta como esquema de
  amostragem inferencial.
""",
    "",
)

# --- [21] modelo/algoritmo --------------------------------------------
c.rep(
    r"""  \item Confusão coleta versus método: mitigada fixando o modelo/
  algoritmo de cada análise ao do artigo original, isolando o efeito da coleta.""",
    r"""  \item Confusão coleta versus método: mitigada fixando o modelo e/ou o
  algoritmo de cada análise ao do artigo original, isolando o efeito da coleta.""",
)

# --- [22] a limitacao do "porque" -------------------------------------
c.rep(
    r"""  \item Explicação (o ``porquê'') fora do escopo: reporta-se se e
  para quais tipos de análise o volume de coleta muda a conclusão, não
  por que uma análise é sensível ou robusta ao volume. O mecanismo (por exemplo, por que a análise de sentimento reagiria a um conjunto
  maior enquanto a estatística descritiva não) fica como agenda, não como
  resultado.""",
    r"""  \item O ``porquê'' fica fora do escopo: este trabalho mede \emph{quais} tipos de
  análise mudam de conclusão quando se coleta mais, e não \emph{o que}, dentro de cada
  tipo, faz com que mudem. Sabe-se, por exemplo, que a partição de comunidades do caso
  do debate vacinal ainda se movia em três quartos da coleta, e que a proporção de
  mídia do caso de 2014 já estava assentada em cem tweets; dizer por que uma dessas
  quantidades assenta cedo e a outra não exigiria estudar o método em si, e não a
  coleta que o alimenta. Fica como agenda, e não como resultado.""",
)

c.salva()

print("ok")
