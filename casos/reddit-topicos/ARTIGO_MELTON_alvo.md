# O alvo — Melton, Olusanya, Ammar & Shaban-Nejad (2021)

> **Afirmações numeradas, extraídas do full text**, para servir de contrato do caso.
> Tudo aqui saiu da leitura integral do PDF (8 páginas, *article in press*, sem
> apêndices) — Portão 1(a) do [`PROMPT_caso_topicos.md`](../PROMPT_caso_topicos.md).
> Data da leitura: **22/ago/2026**.
>
> Citações entre aspas são **verbatim** do artigo. Onde o artigo se contradiz, a
> contradição está marcada com ⚠ e é ela própria material do caso.

---

## 0. Identificação

| | |
|---|---|
| **Referência** | Melton CA, Olusanya OA, Ammar N, Shaban-Nejad A. *Public sentiment analysis and topic modeling regarding COVID-19 vaccines on the Reddit social media platform: A call to action for strengthening vaccine confidence.* **Journal of Infection and Public Health** 14(10):1505–1512, 2021 |
| **DOI** | `10.1016/j.jiph.2021.08.010` — **CC BY**, acesso aberto |
| **Preprint** | [arXiv:2108.13293](https://arxiv.org/abs/2108.13293) |
| **Datas** | recebido 8/jun/2021 · revisado 6/ago/2021 · aceito 9/ago/2021 |
| **Tração** | **178 citações** (Semantic Scholar, 22/ago/2026) |
| **Repositório** | `github.com/Cheltone/NLP_Reddit` — criado 13/mai/2021, último commit 5/ago/2021 |

---

## 1. A coleta (série M) — é aqui que mora a sub-coleta

**M1 — o instrumento e a data.** Verbatim:

> "We harvested approximately 18,000 posts from thirteen subreddits (*Vaccines,
> CovidVaccine, CovidVaccinated, AntiVaxxers, vaxxhappened, antivaccine, conspiracy,
> conspiracytheories, NoNewNormal, conspiracy_commons, COVID19, COVID, and
> coronavirus*) through the Reddit API on **May 16, 2021**."

Uma passada só, na **API oficial**, num dia só. É o teto de ~1.000 itens por
listagem — o topo das listagens, não a população. Mesma falha estrutural do caso
[`reddit-buntain`](../reddit-buntain/README.md) (top-100 × top-200).

**M2 — a janela.** "collective data ranging from **December 1st, 2020 to May 15,
2021**", 5,5 meses.

**M3 — o segundo filtro, por termo.** Os dados foram "queried for terms
specifically related to the COVID-19 vaccine". Os 22 termos, verbatim: *COVID
vaccine, vaccine, vaccination, immune, immunity, COVID vaccination, corona vaccine,
COVID19 vaccination, COVID-19 vaccination, coronavirus vaccination, COVID-19
vaccine, coronavirus vaccine, coronavirus vaccination, Moderna, Pfizer, J&J,
Johnson & Johnson, COVID vax, corona vax, covid-19 vax, covid19 vax, coronavirus
vax*.

⭐ **M4 — o corpus analisado NÃO é 18.000.** Verbatim:

> "Our finalized dataset consisted of **1401 posts and 10,240 comments (11,641 in
> total)** written by greater than or equal to 8281 authors/users, 1048 of whom
> posted multiple times."

**São as duas coisas** (submissões *e* comentários), e o total analisado é
**11.641**, não 18.000. O resumo e o `ALVOS_modelagem_topicos.md` dizem "~18.000
posts"; os 18.000 são a **colheita bruta**, e o corpus que sustenta cada número do
artigo tem **11.641 itens**. Esta distinção não é detalhe: é o denominador de toda
a Fase 2.

**M5 — por que estes 13.** "These subreddits were also chosen due to a large number
of members (approximately **five million** members)."

⚠ **M6 — a janela dos gráficos não bate com a janela declarada.** O eixo x das
Figs. 1 e 2 começa em **`2020-09-04T13:53:29`**, três meses **antes** do 1º/dez/2020
declarado em M2. Ou os gráficos incluem itens fora da janela, ou o eixo é rótulo
mal gerado. Não há como decidir pelo publicado — registrar como divergência.

⚠ **M7 — a contagem de autores é declaradamente instável.** "In actuality, the
number of authors could have been as high as **9013**. These additional users are
probable because Reddit removes the user ID from posts after a user deletes their
account."

---

## 2. Os métodos (série A)

**A1 — sentimento é TextBlob, não VADER.** "*subjectivity* and *polarity* were
calculated with the **TextBlob** subjectivity and polarity functions." Léxico
pré-treinado, referência [26] = documentação do TextBlob 0.15.

> ⚠ **Correção ao `ALVOS_modelagem_topicos.md`**, que registrou "sentimento por
> VADER". É **TextBlob** — o mesmo instrumento do caso
> [`youtube-agecovp`](../youtube-agecovp/README.md), onde já se mediu que o limiar
> de neutralidade não declarado muda o resultado.

⚠ **A2 — as faixas de subjetividade se contradizem dentro do artigo.**
*Methods*: neutro = (0,4 – 0,6); "Highly Opinionated" > 0,6; "Least Opinionated"
< 0,4. *Results*: 73,15% "in between [0,25; 0,75]", 18,13% "less than 0,25",
8,72% "greater than 0,75". São **duas convenções diferentes** no mesmo artigo.

⚠ **A3 — o limiar de polaridade não é declarado.** O artigo classifica em
positivo/negativo/neutro mas **não diz o corte**. O plausível é `>0`, `<0`, `=0`,
e é o que a Fase 2 vai testar — mas é convenção **não publicada**, exatamente como
no caso do YouTube.

**A4 — o modelo de tópicos.** "The *Gensim LDAModel* algorithm was used to create
LDA models for each month." Pré-processamento declarado: limpeza por regex
(caracteres especiais e hyperlinks), remoção de *stop words*, lematização.
Escolha de k: "coherence values were tested on **50 different LDA models** to
determine the most statistically appropriate number of probable latent topics",
com a ressalva: "Though coherence values are insightful, topics were
**qualitatively** analyzed to double-check for content coherency rather than
numerical."

**A5 — k e coerência do modelo combinado.** "a total number of **five** latent
topics"; "The calculation returned a high score of **0.5641**" (Fig. 3: coerência
cai monotonicamente de ~0,55 em k≈5 para ~0,39 em k=50).

**A6 — modelos mensais e por polaridade.** Mensais: "latent topic quantities were
much smaller … (**less than or equal to three** latent topics)" — a Tab. 1 lista 2
tópicos por mês. Por polaridade (Tab. 2): **7** tópicos negativos, **8** neutros,
**8** positivos.

⚠ **A7 — os modelos mensais publicados NÃO têm "≤ 3 tópicos".** Os `k` lidos dos
sete HTML do repositório (§3) são:

| modelo | combinado | dez/20 | jan/21 | fev/21 | mar/21 | abr/21 | mai/21 |
|---|---|---|---|---|---|---|---|
| **k publicado** | 5 | 3 | **15** | 2 | **6** | **8** | 2 |

Três meses passam de 3, e **janeiro tem 15**. A Tab. 1 do artigo mostra 2 por mês
porque ela é, na própria legenda, um recorte — "It lists **two rows** of topics and
10 words from each" —, mas a prosa de A6 generaliza o recorte como se fosse o
modelo. É divergência entre o **texto** e o **artefato publicado pelos próprios
autores**, e não entre eles e nós.

---

## 3. ⭐ Gabarito parcial: o modelo ajustado dos autores está publicado

O corpus **não** está no repositório. Mas os sete `*.html` são saídas de
**pyLDAvis**, e o payload embutido carrega a **matriz tópico-termo e a fração de
tokens por tópico** do modelo que gerou o artigo. Isso é gabarito de verdade para
T1 — dá para comparar termo a termo (RBO) contra o nosso modelo, em vez de comparar
só prosa.

Modelo combinado (dez/2020–mai/2021), extraído de `CompleteData_LDA.html`
(ordem e rótulos do pyLDAvis, que **reordena por frequência** — não é a ordem da
Tab. 1 do artigo):

| Tópico | % dos tokens | 15 termos mais relevantes |
|---|---|---|
| 1 | **36,10%** | vaccine, people, effect, time, many, thing, year, death, month, good, risk, safe, number, work, virus |
| 2 | **22,88%** | vaccine, virus, people, immune, system, year, antibody, vaccination, immunity, body, cell, infection, time, disease, protein |
| 3 | **18,32%** | vaccine, people, dose, mask, thing, group, datum, year, immunity, efficacy, time, first, second, case, normal |
| 4 | **13,38%** | vaccine, **effect, side**, week, hour, day, second, **fever, symptom, sore**, shot, vaccination, **headache, pain**, today |
| 5 | **9,31%** | vaccine, question, contact, concern, action, people, source, news, moderator, answer, science, full, mind, **misinformation** |

Os 13,38% batem com a legenda da Fig. 4 do artigo ("Top-30 Most Relevant Terms for
Topic 4 — **13.4% of tokens**"), o que confirma que o HTML publicado é o modelo do
artigo.

★ **Nenhum dos 5 tópicos é de teoria da conspiração** — e o tópico de **efeitos
colaterais é o penúltimo em massa (13,38%)**, não o primeiro. Isto é decisivo para
como T1 tem de ser formulado (§4).

---

## 4. T1 — a afirmação de modelagem de tópico

⚠ **T1 não é um ranking.** O prompt de abertura supôs "o ranking dos tópicos". O
full text **não ordena** tópicos por prevalência em lugar nenhum: a afirmação é de
**detectabilidade**. As três formulações, verbatim:

> *(resumo)* "Topic modeling revealed community members **mainly focused on side
> effects rather than outlandish conspiracy theories**."

> *(resultados)* "**Topics 1–4** appear to be closely related to a broader
> discussion of the vaccine, safety concerns, efficacy, and potential side effects."

> *(discussão)* "Significantly, **one constant topic that was detected throughout
> each month, regardless of polarity, was side effects.** … It is also mentionable
> that the **majority of conspiracy theories were not detectable by the LDA models,
> indicating a minimal occurrence.** Besides the mention of *autism*, most manually
> read conspiracy theories were mostly sarcastic."

Operacionalizada, T1 vira **duas asserções binárias e verificáveis**, não prosa
vaga:

- **T1a (persistência).** Existe um tópico de **efeitos colaterais** entre os k
  tópicos do modelo combinado, e ele reaparece em **todo mês** e em **toda
  polaridade**. *No gabarito: sim — Tópico 4 do combinado, e "side effects" na Tab. 1
  em dez, jan, fev, mar, mai.*
- **T1b (ausência).** **Nenhum** tópico de teoria da conspiração é detectável pelo
  LDA. *No gabarito: sim — nenhum dos 5 tópicos combinados, nem dos 23 por
  polaridade, tem termo de conspiração.*

**T1b é o alvo forte do caso**, e é invertível de modo limpo: basta que um tópico de
conspiração emerja no LDA da população para a afirmação cair. E é plausível que
caia, porque **6 dos 13 subreddits são de conspiração/antivacina** (`conspiracy`,
`conspiracytheories`, `NoNewNormal`, `conspiracy_commons`, `antivaccine`,
`AntiVaxxers`) e mesmo assim nenhum tópico de conspiração apareceu — o que só se
explica por (i) o topo da listagem selecionar contra eles, (ii) o filtro de 22
termos (todos clínicos/farmacêuticos: *Moderna, Pfizer, immunity*…) excluir o
vocabulário conspiratório, ou (iii) o fenômeno ser mesmo raro. **Separar (i)+(ii) de
(iii) é exatamente o que este caso mede.**

> **Portanto: o alvo NÃO cai na condição de parada** do prompt ("se o *ranking* for
> prosa vaga sem ordenação, PARE"). Não há ranking, mas o que há é mais nítido que um
> ranking: uma afirmação de **ausência**, falsificável por uma única detecção.

### ★ T1b já está sob tensão no próprio gabarito dos autores

O modelo de **janeiro/2021** publicado pelos autores tem **k = 15** (A7), e nele
aparecem dois tópicos que a prosa do artigo diz não existirem:

| tópico | 10 termos mais relevantes |
|---|---|
| **T14** | slight, thing, good, neurological, vaccine, **autism**, **damage**, mother, stuff, local |
| **T15** | negative, couple, well, pfizer, thank, week, pressure, vaccine, temp, **microchip** |

*Microchip* é o vocabulário conspiratório canônico do debate vacinal de 2021, e
*autism* é o único que o artigo admite ter visto ("Besides the mention of autism…").
Ou seja: **quando o modelo tem resolução (k=15), o tópico de conspiração aparece;
quando tem k ≤ 5, some.** A afirmação de ausência de T1b é, ao menos em parte,
**efeito da resolução do modelo**, não do conteúdo do corpus.

Isso é bom para o caso e exige cuidado na leitura:

1. **Bom** porque dá um mecanismo concreto e mensurável. `k` é escolhido por
   coerência, e a curva de coerência depende do tamanho e da composição do corpus —
   logo *coletar mais* pode mover `k` e, com ele, a detectabilidade. A pergunta
   "mudou?" ganha um caminho causal explícito, em vez de depender só do sorteio.
2. **Exige cuidado** porque essa parte da tensão é **do lado do artigo**, e não da
   sub-coleta: mesmo com os 11.641 itens deles, o tópico de conspiração era
   detectável a k=15. A Fase 2 tem de separar as duas coisas —
   **efeito de resolução** (k) e **efeito de coleta** (volume) —, e a Fase 3 tem de
   variar as duas, senão o caso mede k e diz que mediu coleta. É o mesmo erro que o
   caso do YouTube cometeu e teve de corrigir (mecanismo não isolado).
3. ⚠ **Ressalva de proveniência.** Nada no repositório diz que `LDA_Jan.html` é o
   modelo que sustenta a Tab. 1; pode ser exploratório. O que se pode afirmar com
   segurança é o que está escrito acima: *o artefato que o artigo manda consultar
   ("see [the repo] for an interactive topic model") contém tópicos de conspiração*.

---

## 5. T2 — a afirmação de sentimento

**T2a — o balanço.** Conjunto combinado: **56,68% positivos, 27,69% negativos,
15,63% neutros**. Polaridade média **0,0520** (variância 0,0415). Subjetividade
média **0,4450** (variância 0,0560).

**T2b — a estabilidade no tempo.** Verbatim, no resumo e repetida na conclusão:

> "the sentiments expressed in these social media communities are **overall more
> positive than negative and have not meaningfully changed since December 2020**."

Mês a mês (% de posts), do texto:

| Mês | positivo | negativo | neutro |
|---|---|---|---|
| dez/2020 | 57,63 | 26,21 | 16,16 |
| jan/2021 | 59,49 | 25,52 | 14,99 |
| fev/2021 | 57,93 | 28,10 | 13,97 |
| mar/2021 | 57,13 | 25,97 | 16,90 |
| abr/2021 | 54,98 | 28,96 | 16,06 |
| mai/2021 | **53,05** | **30,57** | 16,38 |

O próprio artigo nota que "May reported the least positive sentiment and highest
negative sentiment". A tendência dez→mai é de **−4,6 p.p. em positivo e +4,4 p.p.
em negativo**, e mesmo assim é lida como "not meaningfully changed" — sem teste
estatístico. É afirmação de estabilidade **sem instrumento**, e portanto invertível
por instrumento.

**T2c — o balanço ponderado por upvote inverte de peso, não de sinal.** Comentários
negativos somam 133.305 upvotes (23,24%), neutros 94.641 (16,50%) e positivos
345.607 (60,26%), de um total de **612.217** upvotes.

---

## 6. O que o artigo NÃO publica (e por isso a Fase 2 tem de reconstruir)

- ❌ **o corpus** — nem os 18.000 brutos, nem os 11.641 analisados, nem os IDs;
- ❌ **o limiar de polaridade** (A3) e **qual** das duas convenções de subjetividade
  vale (A2);
- ❌ **como os 18.000 viraram 11.641** — se o filtro de termo foi sobre título, corpo,
  ou os dois; se comentários herdam o filtro da submissão;
- ❌ **o k de cada mês** (diz "≤ 3"; a Tab. 1 mostra 2);
- ❌ a semente do LDA, o número de passes, e o `alpha`/`eta`;
- ✅ **publica o modelo ajustado** (§3) — que é o que salva a Fase 2 de ser cega.
