# Prompt — abrir o sétimo caso: modelagem de tópico no Reddit

> Escrito em **22/ago/2026**, depois de a Mariana decidir abrir o caso (rodada de
> revisão 4 → 5). Cole o bloco abaixo numa sessão nova. Ele é auto-contido de
> propósito: diz o alvo, o desenho, as travas, os portões de decisão e as
> condições de parada, sem depender do histórico de nenhuma conversa.
>
> O levantamento que escolheu o alvo está em
> [`ALVOS_modelagem_topicos.md`](ALVOS_modelagem_topicos.md).

---

```
Abra o sétimo caso de replicação da dissertação: modelagem de tópico no Reddit.
Leia primeiro, nesta ordem: ESTADO.md da raiz, CLAUDE.md da raiz, e
casos/ALVOS_modelagem_topicos.md (que é o levantamento que escolheu o alvo).

POR QUE ESTE CASO EXISTE
Modelagem de tópico é o 4º tipo de análise mais frequente do levantamento (408
artigos, 19,1%) e o único tipo frequente SEM caso executado. Hoje isso está
declarado no corpo.tex como limitação de cobertura (§9.3) e como próximo passo
(§9.4). O objetivo deste caso é converter essa limitação em duas linhas da tabela
mestre (tab:mestre, §9.1).

O ALVO
Melton, Olusanya, Ammar & Shaban-Nejad (2021), "Public sentiment analysis and
topic modeling regarding COVID-19 vaccines on the Reddit social media platform:
A call to action for strengthening vaccine confidence", Journal of Infection and
Public Health 14(10):1505-1512. Preprint aberto: arXiv:2108.13293.
178 citações (Semantic Scholar, 22/ago/2026).

A sub-coleta dele é o ponto: ~18.000 posts de 13 subreddits, colhidos com PRAW
(a API oficial) numa ÚNICA passada em 16/mai/2021, cobrindo 01/dez/2020 a
15/mai/2021. A API devolve ~1.000 itens por listagem — logo aquilo é o topo das
listagens, não a população. É a mesma falha estrutural do caso Buntain
(top-100 posts × top-200 comentários), que deu o maior efeito de sub-coleta da
dissertação. Os 13 subreddits: Vaccines, CovidVaccine, CovidVaccinated,
AntiVaxxers, vaxxhappened, antivaccine, conspiracy, conspiracytheories,
NoNewNormal, conspiracy_commons, COVID19, COVID, coronavirus.

DUAS AFIRMAÇÕES A TESTAR (confirme-as no full text antes de fixar)
 T1 (modelagem de tópico) — o ranking dos tópicos: as comunidades falam mais de
    efeitos colaterais do que de teorias conspiratórias.
 T2 (sentimento) — o balanço é mais positivo que negativo, e estático ao longo
    do tempo.
As duas rodam sobre o MESMO corpus, o que repete o desenho que respondeu à PP3
no caso vacinal e acrescenta à tabela mestre um par que ela não tem:
modelagem de tópico × sentimento.

ESTRUTURA DE PASTA (espelhe casos/reddit-buntain/)
  casos/reddit-topicos/
    README.md
    ARTIGO_MELTON_alvo.md      <- as afirmações numeradas, tiradas do full text
    core/  pipeline/  analise/  data/repl/melton2021/

===================================================================
PORTÃO 1 — Fase 0 + dimensionamento. NÃO PULE, NÃO INVERTA A ORDEM.
===================================================================
a) LEIA O FULL TEXT INTEIRO (arXiv:2108.13293), apêndices inclusive, e extraia as
   afirmações numeradas para o ARTIGO_MELTON_alvo.md: quantos tópicos, qual k,
   que pré-processamento, se o "ranking" é ranking mesmo ou prosa, se os 18 mil
   são submissões, comentários ou os dois, e a data exata da coleta.
   ⚠ ISTO NÃO É FORMALIDADE. Em 22/ago/2026 descobriu-se que o caso de TikTok
   tinha sido fechado sobre os DADOS publicados sem que o TEXTO do alvo fosse
   lido, e por isso reivindicou como achado próprio uma coisa que estava no
   Apêndice C do próprio artigo (ESTADO.md §4.22). Não repita isso.

b) DIMENSIONE a população dos 13 subreddits na janela ANTES de baixar dump
   nenhum. Use o endpoint de agregação do Arctic Shift, reaproveitando o código
   de casos/reddit-buntain/ e casos/reddit-massachs/.
   ⚠ Foi exatamente aqui que o reddit-massachs travou: 34/34 agregações voltaram
   incompletas nos subreddits grandes. coronavirus, conspiracy e COVID19 são
   grandes. Se falhar do mesmo jeito, o caminho é dump por subreddit no Academic
   Torrents — e aí o custo é de transferência e disco, não de código.

c) VERIFIQUE se NoNewNormal e antivaccine foram banidos. Subreddits banidos somem
   da API mas continuam nos dumps históricos. Se for o caso, registre: é achado
   (a rota oficial de hoje nem alcança parte do corpus do artigo), e é obstáculo.

d) RELATE ao fim do portão: tamanho estimado da população, rota de coleta viável,
   espaço em disco e tempo de transferência estimados. PARE e espere decisão da
   Mariana se a estimativa passar de ~24h de transferência ou se a rota exigir
   Academic Torrents.

===================================================================
PORTÃO 2 — Pré-registro. Antes de rodar QUALQUER análise sobre o superconjunto.
===================================================================
Grave um .md versionado em data/repl/melton2021/ com:
  - a semente do sorteio, o número de réplicas por ponto e as frações da curva;
  - o que conta como mudança em T1 e em T2, decidido ANTES (para T1, defina como
    se compara um ranking de tópicos entre duas execuções — similaridade de
    partição, sobreposição de termos no topo, RBO; o .bib já tem webber2010rbo e
    danon2005nmi);
  - a aposta, por escrito. A registrada até aqui: o ranking dos tópicos
    principais NÃO se inverte, mas o balanço de sentimento SIM, porque o topo da
    listagem é engajamento e engajamento seleciona polaridade.
Reportar honestamente quando a aposta falha é regra do projeto (CLAUDE.md §7), e
já falhou duas vezes (H1 do Ituassu, P1 do YouTube).

===================================================================
FASES 1 a 4
===================================================================
1. População completa dos 13 subreddits na janela, congelada em SQLite local e
   versionada. Rode na cópia com dados (Documents/dissertacao/), traga de volta
   só os arquivos que mudarem — NUNCA sincronize pasta inteira (CLAUDE.md, topo).
2. Reproduza o ponto original. ⚠ O artigo NÃO publica o corpus. Reconstruir pela
   mesma janela e mesmos subreddits é o mais próximo possível, e a diferença
   entre o corpus reconstruído e os 18 mil deles É a medida da sub-coleta.
   Documente essa diferença como resultado, não como ruído.
3. Curva A(volume): LDA e sentimento refeitos em frações crescentes, com réplicas
   por ponto e banda por bootstrap de percentis. FIXE LDA — é o algoritmo do
   alvo, e trocar por BERTopic confundiria efeito de coleta com efeito de método.
   BERTopic entra depois, se entrar, como análise de sensibilidade SEPARADA.
4. Duas linhas novas na tab:mestre do corpo.tex, no formato das existentes.

TRAVAS
- Não use a API oficial do Reddit para volume. A rota é Arctic Shift / dumps.
- Orçamento de LLM: NÃO gaste no ANTHROPIC_VACINAS_API_KEY (teto de US$ 25, é do
  rotulador do stance). Este caso não deveria precisar de LLM nenhum — LDA e
  VADER são locais. Se algum passo parecer precisar, pare e pergunte.
- Rastreabilidade: todo número que for para o corpo.tex sai de um JSON congelado
  por script. Nada de número digitado à mão, em texto ou em figura.

CONDIÇÕES DE PARADA
- Se o Portão 1 mostrar que a coleta não cabe no tempo até a defesa (29/set/2026),
  PARE e reporte. O caso vale mais como próximo passo bem documentado do que como
  meio caso mal feito.
- Se o full text revelar que T1 e T2 não são inversíveis (por exemplo, se o
  "ranking" for prosa vaga sem ordenação), PARE: o alvo não serve, e a lista de
  alternativas está em ALVOS_modelagem_topicos.md §3.
- Qualquer bloqueio ou rate-limit agressivo: pare, não contorne.

O QUE NÃO FAZER
- NÃO mexa no corpo.tex enquanto a Mariana não tiver lido o revisao-5.pdf. O PDF
  que ela comenta tem de bater com a fonte. Acumule os resultados nos .md do caso
  e escreva o capítulo depois — foi assim com todos os outros.
- Não trate "ter um sétimo caso" como o objetivo. O objetivo é o veredito
  mudou?/convergiu? para modelagem de tópico. Um caso que conclua "não mudou, e
  já tinha convergido" fecha a lacuna igualmente bem.

AO TERMINAR QUALQUER ETAPA
Atualize o ESTADO.md e os .md do contrato de documentação (skill docs-em-dia).
Trabalho só termina quando o .md correspondente reflete a realidade.
```

---

## O que decide se este caso entra na dissertação

O **Portão 1**. A defesa é em **29/set/2026** e a coleta é maior que a do
`reddit-buntain` (que fechou em 43.479 submissões + 1.015.247 comentários);
treze subreddits grandes ao longo de 5,5 meses é outra ordem de esforço. Se o
dimensionamento disser que não cabe, o resultado honesto é o caso ficar como
**próximo passo já instruído** — e aí este arquivo terá servido de qualquer
modo, porque a §9.4 passa a apontar para um alvo escolhido em vez de uma rota
genérica.

⚠ **A prioridade da Mariana não muda por causa disto:** ler o `revisao-5.pdf` —
sobretudo os Caps. 5 a 7, sem comentário desde o `revisao-2.pdf` — e rotular as
210 do teste cego do stance, que fecham a linha 10 da tabela mestre (o dev de 110 fechou em 22/ago/2026). Este caso roda em
paralelo, do lado do assistente.
