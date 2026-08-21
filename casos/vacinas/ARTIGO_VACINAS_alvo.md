# O alvo — Verjovsky et al. (2023): "Political quarrel overshadows vaccination advocacy"

> Leitura instrumental do artigo para a replicação por expansão. PDF do alvo:
> [political_quarrel.pdf](political_quarrel.pdf). **Publicado em _Vaccine_ (Elsevier),
> 7/set/2023** — revisado por pares (PubMed 37550146; ScienceDirect S0264410X23009210). O
> SSRN 4370287 era o **preprint**; a versão final saiu na _Vaccine_ (corrigido 07/ago/2026).
> Plano do caso em [REPLICACAO_CASO_VACINAS.md](REPLICACAO_CASO_VACINAS.md).

**Ficha.** *Political quarrel overshadows vaccination advocacy: How the vaccine debate
on Brazilian Twitter was framed by anti-vaxxers during Bolsonaro government.*
Marina Verjovsky, **Mariana Porto Barreto**, Isabella Carmo, Bruno Coutinho, Lilian
Thomer, **Sérgio Lifschitz** (BioBD/PUC-Rio) e Claudia Jurberg (IOC-Fiocruz/FAPERJ).
Contributor statement: *"Mariana Porto Barreto, Isabella Carmo and Bruno Coutinho
extracted the data."* — **a Mariana é coautora e foi quem extraiu os dados.**

---

## 1. O que o artigo fez

### 1.1 Coleta (a parte que o caso problematiza)

- **Rede:** Twitter. **Plataforma:** eTC (`https://etc.biobd.inf.puc-rio.br/`) — a
  mesma infraestrutura BioBD dos outros casos.
- **Termos-índice (PT):** "vacina", "vacinação", "vacinar", "anti-vacinação",
  "anti-vax", "vacinação infantil" (o texto lista em inglês: *vaccine, vaccination,
  to vaccinate, anti-vaccination, anti-vax, childhood vaccination*).
- **Janela:** **9/dez/2021** (abertura da consulta pública sobre vacinar crianças
  contra COVID-19) → **9/fev/2022** (1 mês após o início da vacinação infantil).
  Coleta de atualização (repercussões) em **8/mar/2022**.
- **Critério de inclusão:** *"All tweets from users who retweeted or retweeted someone
  in the period"* — ou seja, o corte é por **atividade de retweet**, não só por termo.
- **Volume bruto:** **>1 M tweets** e **~4 M retweets** no período.

### 1.2 Análises

1. **Rede / modularidade (Gephi 0.9.2):** algoritmo de comunidades (classes de
   modularidade) sobre o grafo de retweets; o algoritmo decide o número de grupos.
   Emergem **dois grupos bem definidos** (pró e anti-vacina).
2. **Análise de conteúdo (Bardin):** feita **só sobre os tweets virais (>500 RTs)**.
   Rotulagem manual por dois autores + terceiro árbitro: primeiro
   pró-vacina / anti-vacina / não-relevante-ambíguo; depois **11 categorias temáticas
   binárias** (contém=1 / não contém=0), com subcategorias.
3. Ferramentas de apoio: Gephi, MS Excel, MAXQDA.

### 1.3 Material suplementar (importante para nós)

Apêndice A aponta uma **planilha Google Sheets** com o material suplementar —
presumivelmente os tweets virais **já rotulados** (verificar acesso; link no PDF,
p. 12). Se acessível, é o **gabarito** para validar rotulagem automatizada.

---

## 2. Resultados que viram afirmações testáveis

| # | Afirmação (como está no artigo) | Onde |
|---|---|---|
| **AV1** | Pró e anti têm volumes semelhantes: cada grupo ≈ 2/5 da amostra; juntos, **78%** dos posts do período (Tabela 1) | §3 |
| **AV2** | Entre os virais (>500 RT), os tweets pró mais populares receberam **2× mais RTs** que os anti mais populares (Tabela 2) | §3 |
| **AV3** | Dos **602 autores influentes**: **353 pró (58,6%) × 246 anti (40,9%)** (Tabela 3) | §3 |
| **AV4** | Concentração: top-10 autores = **15,7% de todos os RTs**; o top-10 é **dominado pelos anti (9 dos 10 tweets mais retuitados)**; 388 autores (64,5%) tiveram só 1 tweet viral; 6 (1%) tiveram >20 | §3 e §4 |
| **AV5** | **Ranking de framing** (Tabela 5): I. Política > II. Crianças > III. Políticas restritivas > IV. Desvantagens das vacinas > V. Pessoas anti-vacina > VI. Fontes de (des)informação > VII. Internacional > VIII. Vantagens das vacinas > IX. Riscos da COVID > X. Ciência e farmacêuticas > XI. Religião | §3–4 |
| **AV6** | Conclusão-título: **os anti-vax impuseram o enquadramento** do debate — mesmo o grupo pró gastou o discurso reagindo (criticando anti-vax e políticas) em vez de promover vantagens da vacinação | §4–5 |

Detalhes úteis por categoria (para checagens finas): político mais citado = Bolsonaro
(171 menções; 33% pró-, 14% anti-vacina); ANVISA 105 menções; anti-vax focados em
"liberdade" (330 comentários, 87% da categoria III); influenciadores anti = jornalistas,
líderes religiosos e políticos bolsonaristas; pró = maioria "cidadãos comuns" sem
articulação.

## 3. Limitações declaradas pelos autores

- Não distingue humanos de **bots** (RTs podem estar inflados).
- Sem análise de **geolocalização** (usuários não configuram).
- (Implícita, e é o nosso caso:) a análise de conteúdo cobre **apenas a elite viral**
  — o corte >500 RT é assumido como janela válida para "o debate".

## 4. Por que este alvo serve à dissertação

O artigo é o exemplar perfeito de **"filtragem por critério é a norma"**: a coleta até
foi larga (1 M tweets), mas a **análise substantiva** (conteúdo/framing) foi feita num
estrato definido por um limiar arbitrário de engajamento (>500 RT). A conclusão-título
(AV6) é, formalmente, uma afirmação **sobre a elite viral** generalizada para "o debate
no Twitter". O caso pergunta: *ela sobrevive quando se desce o limiar?* — ver eixos em
[REPLICACAO_CASO_VACINAS.md](REPLICACAO_CASO_VACINAS.md).

Bônus de linhagem: além de mesmo orientador e mesma plataforma (eTC), **a própria
autora da dissertação extraiu estes dados** — o caso aplica a lente "coletar mais" ao
trabalho anterior dela mesma, o que dá ao argumento um tom de autocrítica honesta em
vez de crítica externa.
