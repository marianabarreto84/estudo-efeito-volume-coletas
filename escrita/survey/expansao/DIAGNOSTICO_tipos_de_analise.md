# Diagnóstico — o rótulo "análise de conteúdo" e a tabela de tipos de análise

> Medido em **21/ago/2026**, a pedido da Mariana ("acho que muita coisa está indo
> errado com esse rótulo"). A suspeita se confirma, mas o defeito é maior e mais
> específico do que o rótulo: **ele é o pior caso de uma família inteira de
> rótulos**, e há um segundo defeito, estrutural, que independe deles.
>
> Nada aqui foi aplicado ao `.tex`. São medidas e uma recomendação; as decisões
> são da Mariana e estão listadas no §6.
>
> Reprodutível por [`audita_rotulo_conteudo.py`](audita_rotulo_conteudo.py) e pelos
> trechos de consulta citados em cada seção. Base: `research.db`, 2.139 artigos
> extraídos, dos quais **887** foram lidos pelos dois modelos.

---

## 1. O que se mediu, e por que não dá para medir pelo resumo

A pergunta é se o rótulo `análise de conteúdo` identifica trabalhos que fazem
análise de conteúdo — o método, com livro de códigos, categorias e codificadores
— ou se é um adesivo colado em qualquer trabalho que olhe para texto.

⚠ **A coluna `abstract` do `research.db` está vazia nos 2.139 artigos.** Qualquer
teste de "o artigo tem marca do método?" feito sobre título+resumo roda, na
prática, só sobre o **título** — e um título quase nunca diz "codebook". Uma
primeira versão desta medida foi feita assim e **foi descartada**: ela dizia que
99,5% dos rotulados não tinham marca metodológica, o que é artefato da coluna
vazia, não achado.

A medida que vale é contra o **texto integral do PDF**, que está em disco, e com
**grupo de controle** — sem controle, uma taxa isolada não diz nada.

## 2. O rótulo, medido

### 2.1 Os dois modelos não concordam sobre ele

Nos 887 artigos que Gemini e Claude Haiku leram:

| | valor |
|---|---:|
| **κ de Cohen** | **0,227** |
| concordância bruta | 60,1% |
| Gemini apõe o rótulo em | 50,0% do que lê |
| Claude apõe o rótulo em | 36,8% do que lê |
| os dois apõem | 235 artigos |
| só o Gemini | 263 |
| só o Claude | 91 |

κ = 0,227 é *slight-to-fair* na escala de Landis-Koch. Para comparação, no mesmo
banco e nos mesmos 887 artigos, **Twitter como plataforma tem κ = 0,976**.

### 2.2 Ele quase nunca vem sozinho

Em apenas **43** artigos `análise de conteúdo` é o único rótulo. Nos outros 1.118
ele vem pendurado em cima de um método concreto:

| co-ocorre com | vezes |
|---|---:|
| estatística descritiva | 437 |
| análise de sentimento | 435 |
| análise temporal de redes | 288 |
| análise de rede | 271 |
| modelagem de tópicos | 224 |

### 2.3 Contra o texto integral do PDF, com controle

150 artigos rotulados × 150 não rotulados, sorteados com semente `20260929`,
texto integral extraído com `pdfplumber`, casado contra expressões regulares em
dois graus:

- **marca forte**: `content analysis` / `análise de conteúdo` literal, Krippendorff,
  Bardin, Holsti, *codebook*, *coding scheme*, *inter-coder reliability*;
- **marca fraca**: kappa, *two coders*, *human coders*, *manual coding*,
  *thematic analysis*, diretrizes de anotação.

| | rotulados | controle | diferença | *p* |
|---|---:|---:|---:|---:|
| **marca forte** | 23,3% (35/150) | 13,3% (20/150) | **+10,0 p.p.** | **0,025** |
| forte ou fraca | 30,7% (46/150) | 22,0% (33/150) | +8,7 p.p. | 0,088 |
| **nenhuma marca** | **69,3%** | 78,0% | — | — |

**Leitura honesta.** O rótulo **não é ruído puro**: pelo critério forte ele separa,
e a diferença é significativa. Mas como classificador é inútil — de cada quatro
artigos que ele rotula, **três não têm no PDF inteiro vestígio nenhum do método**,
e ele deixa de fora 13,3% do controle, que têm. Aposto em metade do corpus, o que
ele descreve não é o método: é a presença de texto no objeto de estudo.

Exemplos entre os rotulados sem marca alguma: um corpus paralelo de língua de
sinais (#5208 e #1330), uma auditoria de recomendação do YouTube (#3056), um
paper de plataforma Hadoop (#2034), uma tarefa do SemEval de detecção de humor
(#8248).

### 2.4 O instrumento convida ao rótulo

`análise de conteúdo` é o **termo 22 da tabela `vocabulary`**, entregue ao modelo
dentro do prompt como vocabulário sugerido. É o termo mais vago da lista, e é o
único que descreve um gênero de trabalho em vez de uma técnica. O rótulo não
emergiu dos artigos: foi oferecido.

## 3. Ele não está sozinho — κ por bucket

Mesmos 887 artigos, aplicando os `ANALYSIS_BUCKETS` de `agg_results.py`:

| bucket | κ | | bucket | κ |
|---|---:|---|---|---:|
| Análise de rede | 0,734 | | Clusterização | 0,409 |
| Modelagem de tópico | 0,723 | | Desinformação/bots | 0,405 |
| Predição de links | 0,666 | | Influência | 0,337 |
| Detecção de comunidades | 0,583 | | Centralidade | 0,316 |
| Sentimento | 0,529 | | Temporal | 0,291 |
| Classificação | 0,525 | | **Estatística descritiva** | **0,282** |
| | | | *[rótulo] análise de conteúdo* | *0,227* |
| | | | PLN (NER/embed.) | 0,171 |

**O corte não é aleatório.** Comparando com os campos que descrevem a coleta, nos
mesmos artigos:

| campo | κ |
|---|---:|
| Reddit (plataforma) | 0,989 |
| Twitter (plataforma) | 0,976 |
| YouTube (plataforma) | 0,971 |
| `uses_preexisting_dataset` | 0,812 |
| `uses_api` | 0,803 |
| `uses_scraping` | 0,758 |
| `suggested_discard` | 0,736 |
| `mentions_database_tech` | 0,618 |
| `sampling_used` | 0,508 |
| filtragem | 0,443 |

> **O instrumento é confiável para o que é verificável no texto** — que plataforma,
> que API, que dataset — **e não é para o que exige interpretação** — que tipo de
> análise é esta. "Análise de conteúdo" é o pior caso porque é o rótulo mais vago,
> não porque seja um defeito isolado.
>
> Isso é boa notícia para o resto do trabalho: os campos de que a expansão do
> corpus depende (plataforma, método de coleta) estão entre os mais sólidos.
> `sampling_used` (0,508) e filtragem (0,443) são **moderados** — vale declarar,
> mas são de outra ordem de problema.

## 4. O defeito estrutural: união de modelos com cobertura desigual

Este independe dos rótulos e é, na prática, o mais grave.

A tabela de tipos de análise agrega pela **união** dos modelos
(`agg_results.py` §3: `for m in ACTIVE_MODELS: bs.add(b)`). Já a taxa de
amostragem/filtragem usa **só o Gemini** (§4: `gem(a)`), decisão registrada no
[STATUS.md](../STATUS.md) — *"reportado sobre Gemini, que cobre os 2.139; Claude
só 887"*. **O mesmo artigo usa dois critérios diferentes para dois achados.**

Consequência medida, base 1.718 pós-descarte:

| | n | buckets por artigo (média) |
|---|---:|---:|
| lido **só pelo Gemini** | 986 | **2,26** |
| lido **pelos dois** | 732 | **4,23** |
| | | **+87%** |

Os dois grupos entram na **mesma tabela de percentuais**. Um artigo aparece em
quase o dobro de linhas por ter sido lido por dois modelos — e quem foi lido por
dois **não é sorteio**: são os 887 que a cota da Anthropic alcançou antes de
esgotar, duas vezes, em mai/2026 ([ORCAMENTO.md §4](../../../../redes-sociais-digitais-survey/documentacao/ORCAMENTO.md)).

### 4.1 O ranking depende de a quem se pergunta

Nos 732 artigos que os dois leram (pós-descarte):

| bucket | Gemini | Claude | salto |
|---|---:|---:|---:|
| **Temporal** | #6 | **#1** | 5 |
| **Estatística descritiva** | **#1** | #6 | 5 |
| **Centralidade** | #10 | **#4** | 6 |
| Análise de rede | #3 | #7 | 4 |
| Sentimento | #2 | #2 | 0 |
| Modelagem de tópico | #5 | #5 | 0 |

τ de Kendall entre os dois rankings = **+0,564**. O top-5 do Gemini tem
*Estatística descritiva* e *Análise de rede*; o do Claude tem *Temporal* e
*Centralidade*.

### 4.2 Quanto a tabela se move ao trocar união por só-Gemini

Base 1.718:

| bucket | união (hoje) | só Gemini | Δ |
|---|---:|---:|---:|
| Estatística descritiva | 46,9% | 42,8% | −4,1 |
| Sentimento | 45,1% | 35,0% | **−10,1** |
| Classificação | 40,0% | 34,9% | −5,1 |
| Temporal | 36,6% | 19,5% | **−17,1** |
| Análise de rede | 29,0% | 26,6% | −2,4 |
| PLN (NER/embed.) | 23,2% | 16,0% | −7,2 |
| Modelagem de tópico | 22,9% | 19,1% | −3,8 |
| Detecção de comunidades | 18,8% | 14,8% | −4,0 |
| Centralidade | 17,7% | 7,7% | **−10,0** |
| Influência | 13,3% | 9,2% | −4,1 |

O **top-3 sobrevive** (Estatística descritiva > Sentimento > Classificação). As
magnitudes não. E a ordem 4ª/5ª troca: pela união, *Temporal*; por Gemini,
*Análise de rede*.

### 4.3 ⚠ Um erro que não depende de nada disto: o texto contradiz a própria tabela

Independente da escolha união × Gemini, há um erro factual dentro do `corpo.tex`.

A linha 279 afirma:

> *"A modelagem de tópico, que é **o quarto tipo mais frequente** do levantamento,
> não é instanciada por nenhum caso executado"*

A `tab:analises-survey`, **na mesma seção**, lista:

| # | tipo | % | | # | tipo | % |
|---:|---|---:|---|---:|---|---:|
| 1 | Estatística descritiva | 43,7 | | 6 | **Modelagem de tópico** | **19,1** |
| 2 | Sentimento | 40,4 | | 7 | Detecção de comunidades | 15,6 |
| 3 | Classificação | 35,3 | | 8 | Centralidade | 14,9 |
| 4 | **Temporal** | **31,1** | | 9 | Influência | 11,1 |
| 5 | Análise de rede | 24,6 | | 10 | Clusterização | 7,3 |

Pela própria tabela, modelagem de tópico é a **6ª**, e a 4ª é *Temporal*. Por
qualquer outro corte ela é 6ª ou 7ª — **em nenhum ela é a 4ª**. O ordinal
provavelmente veio de ler a tabela por coluna em vez de por posição: ela é a
**primeira entrada da segunda coluna**.

A lacuna continua inteiramente real e a limitação continua válida — só o ordinal
está errado. O `audita_contas.py` não pega isso porque é afirmação de ordem, não
de aritmética; vale virar uma linha da tabela `RELACOES` dele, para não voltar.

## 5. O que isto NÃO afeta

Para não superestimar o estrago:

- **Não afeta a expansão do corpus em curso.** Os achados pré-registrados
  (A1 mediana, A2 fração <1 mi, A3a/A3b amostragem e filtragem, A4 Twitter) não
  passam pelos `analysis_types`. O único que encosta é **B4/B5**, secundários.
- **Não afeta a escolha dos casos já executados.** Sentimento, análise de rede,
  modelagem de tópico e classificação estão entre os buckets de κ mais alto ou no
  topo dos dois rankings; nenhum caso do lineup foi escolhido por um bucket
  instável.
- **Não invalida a concordância de ≈85%** declarada na Metodologia — mas mostra
  que ela é uma **média sobre campos de confiabilidade muito diferente**, de 0,171
  a 0,989, e que reportá-la como número único esconde exatamente a distinção que
  importa.

## 6. Recomendações — decisões da Mariana

1. **Reportar tipos de análise só pelo Gemini**, como o artigo já faz para
   amostragem/filtragem. É a correção de maior efeito e a mais fácil de defender:
   remove a dependência de qual artigo a cota alcançou, e alinha os dois achados
   ao mesmo critério. Implica recomputar `tab:analises-survey` (dissertação) e a
   tabela de tipos de análise (survey).
2. **Manter `análise de conteúdo` fora da tabela** — o `corpo.tex` já faz isso,
   chamando-o de guarda-chuva. A justificativa agora é medida: κ = 0,227,
   precisão de 23,3% contra o texto integral. Vale trocar a nota de rodapé pela
   medida.
3. **Corrigir o ordinal da modelagem de tópico** (§4.2). A lacuna fica; o "quarto
   mais frequente" não.
4. **Declarar a concordância por família de campo**, não como média única: coleta
   e plataforma ≥ 0,74; amostragem/filtragem ≈ 0,44–0,51; tipos de análise
   0,17–0,73. Isso *fortalece* o trabalho — mostra onde ele é forte.
5. ⛔ **Não mexer no `vocabulary` antes de a expansão extrair os 800.** Se o termo
   22 sair agora, o estrato novo passa a ser extraído com instrumento diferente do
   da base antiga, e o `compara.py` deixa de medir viés de acesso: passa a medir
   mudança de prompt. A correção do vocabulário é **depois** da expansão — ou as
   duas coisas viram uma só e nenhuma das duas se lê.

⛔ Nada disso vai ao `corpo.tex` antes de a Mariana ler o `revisao-3.pdf`.
