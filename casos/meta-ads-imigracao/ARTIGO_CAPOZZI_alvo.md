# O alvo destrinchado — Capozzi et al., anúncios de imigração na Itália

> Gerado em **7/ago/2026** por leitura documental. **Os dois artigos foram lidos na
> íntegra** — o SocInfo 2020 (15 p., incluindo o Apêndice A) e o CHI 2021 (15 p.), este
> último em 7/ago/2026, fechando a pendência de proveniência que existia na primeira
> versão deste documento. Ver [FASE0](data/repl/metaads2019/FASE0_descoberta.md).

## 1. Os dois artigos

| | **SocInfo 2020** | **CHI 2021** |
|---|---|---|
| Título | *Facebook Ads: Politics of Migration in Italy* | *Clandestino or Rifugiato? Anti-immigration Facebook Ad Targeting in Italy* |
| Autores | Capozzi, De Francisci Morales, Mejova, Monti, Panisson, Paolotti (ISI Foundation, Turim) | os mesmos |
| Citações (Semantic Scholar, 7/ago/2026) | 16 | **29** |
| Venue | LNCS / Springer | **CHI** |
| Análise | caracterização (gasto, impressões, Gini, targeting) | **classificação pró/anti + targeting + Granger vs. notícias** |
| Estado da leitura | ✅ íntegra | ✅ íntegra (7/ago/2026) |

O **eixo B (classificação)** é o que preenche a célula `Classificação` da `tab:casos`, e
vem do CHI 2021. O eixo A vem do SocInfo 2020, que é o que tem **dataset publicado**.

## 2. A coleta (SocInfo 2020 §3 — lido)

- **Fonte:** Facebook Ads Library API. O arquivo cobre anúncios sobre *"social issues,
  elections or politics"* **no Facebook e no Instagram desde março de 2019**.
- **Consulta única em 30/mar/2020**, anúncios originados na Itália.
- **Filtro por 26 palavras-chave em italiano** (Apêndice A, transcrito na íntegra):
  `migrante`, `migranti`, `immigrato`, `immigrati`, `immigrata`, `immigrate`, `ius soli`,
  `ius culturae`, `sbarchi`, `sbarco`, `migrazioni`, `migrazione`, `clandestino`,
  `clandestini`, `clandestina`, `clandestine`, `profugo`, `profughi`, `profughe`,
  `profuga`, `scafisti`, `scafista`, `extracomunitario`, `extracomunitari`,
  `extracomunitaria`, `extracomunitarie`.
  Lista construída iterativamente a partir de `migrante`/`immigrato`, expandida por
  similaridade de embeddings **FastText**.
- **⚠ A decisão que funda o caso:** *"In particular, we search for ads appearing **only on
  Facebook (not Instagram)**."* (§3, grifo nosso). A plataforma foi descartada por
  construção, não por indisponibilidade.
- **Exclusão manual** de anunciantes fora do escopo (marcas, publicidade de emigração).
- **Resultado:** **2.312 anúncios de 733 páginas únicas**.
- **Baseline político:** para as **208 páginas** de políticos filiados a PD, Lega, M5S,
  FdI e IV, baixaram **todos** os anúncios **sem restrição de keyword** → **17.014
  anúncios**. É a medida direta de quanto o filtro temático encolheu a coleta.
- **Enriquecimento externo:** páginas casadas com **WikiData** (partidos, políticos,
  jornalistas, ONGs) e com a lista de administradores locais do Ministério do Interior →
  249 páginas de políticos individuais e 53 de partidos.

## 3. Afirmações testáveis

Do SocInfo 2020 (lidas no texto):

- **CA1** — o maior anunciante sobre migração é **Matteo Salvini** (Lega): >50.000 € e
  quase **8.000.000** de impressões.
- **CA2** — a distribuição de impressões é muito desigual: **Gini 0,465** por página e
  **0,800** por anúncio.
- **CA3** — as impressões acompanham o calendário eleitoral; o maior pico é nas semanas
  anteriores às **eleições europeias de 23-26/mai/2019**.
- **CA4** — anúncios sobre migração atingem público **mais masculino** que os anúncios
  políticos gerais dos mesmos autores: todos os partidos exceto o M5S têm odds maiores de
  atingir homens, em média **~20% maiores** (Fisher, p < 0,0001).
- **CA5** — o micro-targeting **não** explica o custo por impressão: correlação entre CPM
  e entropia demográfica ρ_d = −0,112; e entropia geográfica ρ_g = −0,243.

Do CHI 2021 (✅ conferidas no full text em 7/ago/2026):

- **CB1** — classificação em **duas etapas**, não uma: um classificador de *relevância*
  (Random Forest, **F1 = 0,74**) e um de *inclinação* pró/anti (Naive Bayes multinomial,
  **F1 = 0,85**). O "F1 = 0,85" do resumo é só o segundo — a qualidade do pipeline é
  limitada pelos dois.
- **CB2** — anúncios anti são **47,6% dos anúncios** e recebem **65,2% das impressões**
  (~15 M). ⚠ **Os dois denominadores são diferentes e o resumo erra um deles** — ver §5.1.
- **CB3** — cerca de **2/3** das campanhas usam targeting demográfico. No corpo (§5.3), a
  medida é em impressões: **62%** vêm de anúncios com algum targeting e **38%** de anúncios
  sem nenhum. Só **18 anúncios** miram exclusivamente um gênero (<0,2% das impressões).
- **CB4** — **17%** é o subconjunto dos **grandes partidos** (odds ratio 1,17). No conjunto
  inteiro o efeito é muito maior: **OR = 1,69** (69%). E os partidos anti-imigração miram
  público 24% mais masculino quando falam de migração do que quando falam de outros temas
  (OR 1,24).
- **CB5** — *riding the wave*: por Granger, as **notícias causam** as impressões dos
  anúncios com defasagem de 1 dia (significativo para o conjunto e para os anti; **não**
  para os pró), e **não há** causalidade no sentido inverso. Janela truncada em dez/2019
  para excluir a COVID.

**CB2 é o alvo-teste central do caso**: é uma afirmação de **balanço entre polos medida
num estrato**, exatamente a família de afirmação que já falhou três vezes no caso vacinas
(linhas 4b, 4c e 7 da [tabela mestre](../RESULTADOS_tabela_mestre.md)).

### 3.1 A distribuição de stance, em números (CHI §5.2)

| conjunto | anúncios | anti | pró | neutro/irrelevante |
|---|--:|--:|--:|--:|
| **todos os de migração** | 2.312 | **677** (29,3%) | **1.112** (48,1%) | 523 (22,6%) |
| **só de grandes partidos** | 773 | **368** (47,6%) | 309 (40,0%) | 96 (12,4%) |

Impressões: **35 M** no total dos anúncios de migração, das quais autores políticos
respondem por 24,5 M (69,5%) e ONGs por 2,9 M (8,3%).

## 4. O gabarito publicado ✅

[github.com/PotenteOpossum/Facebook-Ads-Politics-of-Migration-in-Italy](https://github.com/PotenteOpossum/Facebook-Ads-Politics-of-Migration-in-Italy)
— repositório **público e verificado em 7/ago/2026**. Baixado para
[data/repl/metaads2019/gabarito_capozzi2020.csv](data/repl/metaads2019/gabarito_capozzi2020.csv)
(945 KB). Conferência feita:

| | valor apurado no CSV | o que o paper afirma |
|---|---|---|
| anúncios (linhas = `ad_id` únicos) | **2.312** | 2.312 ✅ **bate** |
| páginas únicas (`page_id`) | **731** | 733 ⚠ **diverge em 2** |
| colunas | 42 | — |
| início de veiculação | 17/nov/2017 → 28/mar/2020 | arquivo "desde março de 2019" ⚠ **6 anúncios são anteriores** |

**Colunas:** `ad_id`, `page_id`, janelas de veiculação, `impressions_min/max`,
`spend_min/max`, 14 colunas de impressão por **gênero × 7 faixas etárias**, e 20 colunas
de **região italiana**.

⚠ **Ressalva:** este CSV **não tem texto nem criativo** — só metadados. Mas o segundo
repositório, abaixo, resolve isso em parte.

### 4.1 O segundo gabarito: os dados anotados do CHI 2021 ✅

Descoberto na nota de rodapé 10 do CHI 2021 e **verificado em 7/ago/2026**:
[github.com/PotenteOpossum/Clandestino-or-Rifugiato-Anti-immigration-Facebook-Ad-Targeting-in-Italy](https://github.com/PotenteOpossum/Clandestino-or-Rifugiato-Anti-immigration-Facebook-Ad-Targeting-in-Italy)
— público, **12 CSVs** (um por anotador). Baixados para
[data/repl/metaads2019/anotacoes_chi2021/](data/repl/metaads2019/anotacoes_chi2021/).

Conteúdo apurado: **600 anotações = 200 anúncios × 3 anotadores**, com as colunas
`ad_url`, **`ad_creative_body`**, `ad_creative_link_title`, `ad_creative_link_description`
e `Label`. Distribuição dos rótulos: `1`=108, `2`=106, `3`=107, `4`=94, `5`=92,
`irrelevant`=93. Nenhum texto vazio.

**Isso muda o planejamento em dois pontos:**

1. **O gabarito pró/anti existe e é público** — ao contrário do que esta seção afirmava na
   primeira versão. Não é preciso rotular do zero para validar um classificador próprio.
2. **O texto dos anúncios existe para esses 200** — parte do insumo do classificador está
   disponível **sem depender da API**, logo sem depender da retenção. Para os outros 2.112
   anúncios o texto continua exigindo re-consulta por `ad_id`.

**Esquema de rotulagem** (CHI §4.1): escala Likert de 5 pontos sobre a afirmação *"nosso
país se tornou um lugar pior para viver por causa de quem vem de outros países"* —
1 = discorda fortemente (pró-migração) … 5 = concorda fortemente (anti-migração) —
mais o rótulo `irrelevant`. 12 anotadores por conveniência, 50 anúncios cada, 3 anotações
por anúncio.

## 5. Divergências registradas (nenhuma corrigida — são do alvo)

### 5.1 ⚠ O denominador de CB2 no resumo não é o do corpo — **e isso atinge o alvo-teste**

O **resumo** do CHI 2021 diz: *"Although composing **47.6% of all migration-related ads**,
anti-immigration ones receive 65.2% of impressions."*

O **corpo (§5.2)** dá os números: dos **2.312** anúncios de migração, **677 são anti** —
**29,3%**, não 47,6%. Os 47,6% saem de **368/773**, que é o subconjunto dos **anúncios de
grandes partidos**. Ou seja, o resumo atribui a *todos* os anúncios uma proporção que é de
um **estrato** deles.

Os 65,2% das impressões têm ainda um **terceiro** denominador: como os anti somam ~15 M e o
total de anúncios de migração é 35 M, 15/35 = 42,9% — os 65,2% só fecham entre os anúncios
**com posição** (excluindo neutros/irrelevantes), ~23 M.

**Consequência para o caso:** CB2, como está no resumo, contrasta duas proporções com
**denominadores diferentes e nenhum deles é "todos os anúncios"**. A Fase 2 tem de fixar
qual das três leituras vai medir — e reportar as três, porque a diferença entre elas
(29,3% × 47,6%) é maior que qualquer efeito de volume que a expansão possa produzir. Não é
erro nosso nem achado de sub-coleta: é ambiguidade do alvo, e precisa estar declarada antes
de qualquer curva.

### 5.2 O `n` do α de duas polaridades não reproduz (141 × 150)

Ver [FASE0 §4.2](data/repl/metaads2019/FASE0_descoberta.md): o α publicado **reproduz**
(0,924 × 0,92), mas sobre **141** anúncios, não os **150** que o artigo declara. Nenhuma
convenção de filtragem testada devolve 150.

### 5.3 Demais divergências

1. **733 × 731 páginas** — o corpo do artigo diz 733; o CSV publicado tem 731 `page_id`
   distintos. Diferença de 0,3%, sem efeito nas conclusões, mas registrada porque a Fase 0
   precisa reproduzir o ponto publicado.
2. **7 × 6 anunciantes excluídos** — o §3 diz *"we exclude 7"*; o Apêndice A lista **6**
   nomes (`Move To Canada Today`, `Patagonia`, `VisaPlace - Niren & Associates Immigration
   Law Firm`, `Immigration Spot`, `Battlefield Italia-La pagina`, `Videodrome`).
3. **Cobertura do arquivo** — o artigo diz que a Ad Library cobre desde março de 2019, mas
   6 anúncios do próprio dataset começam antes (o mais antigo em 17/nov/2017). O CHI §3.1
   dá a explicação dos autores para a outra ponta do mesmo problema: *"We find only two ads
   in March 2019, with the bulk of the ads starting in April, which suggests that **the tool
   was not properly registering ads yet** at the beginning of the time period."* Ou seja, o
   próprio arquivo é **incompleto na borda inicial da janela** — o que é matéria-prima do
   caso, não ruído a descartar.
4. **Erro conhecido do classificador nas ONGs** — nota de rodapé 12 do CHI: os **4 anúncios
   de ONGs** classificados como anti-migração foram, na inspeção manual, **todos
   mal-classificados**. Taxa de erro publicada num estrato pequeno, útil como referência ao
   validar um classificador próprio.

## 6. Limitações que os próprios autores declaram (SocInfo 2020 §5)

Úteis porque **antecipam o argumento da dissertação**:

- *"We restricted our attention to a specific use case... our findings are limited to this
  specific context. Narrowing our scope in topic, time, and space, however, has the
  beneficial effect of removing potential confounding factors."* — a sub-coleta é
  **assumida e defendida** como escolha de desenho.
- Reconhecem que a API foi reportada como instável e **testam**: re-consultaram duas
  semanas depois e acharam **1 anúncio faltando** na coleta de migração e **3** na geral.
  → é uma medida publicada da estabilidade do instrumento, reaproveitável na Fase 1.
- Apontam como trabalho futuro exatamente o que o CHI 2021 fez (*"text and image mining to
  characterize ads"*).

---

*Docs irmãos: [REPLICACAO_CASO_META_ADS.md](REPLICACAO_CASO_META_ADS.md) ·
[FASE0_descoberta.md](data/repl/metaads2019/FASE0_descoberta.md).*
