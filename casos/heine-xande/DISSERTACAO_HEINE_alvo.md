# Dissertação Heine (2025) — o alvo primário da replicação

> Doc de referência do trabalho-alvo deste caso, no mesmo espírito de
> `PAPER2018_palabra_clave.md` do caso Twitter. Plano de fases em
> [REPLICACAO_CASO_HEINE.md](REPLICACAO_CASO_HEINE.md); eixos em
> [EIXO_TOPICOS.md](EIXO_TOPICOS.md) e [EIXO_QUANTITATIVO.md](EIXO_QUANTITATIVO.md).

**Heine, A. A. P.; Lifschitz, S. (2025).** *Um Estudo sobre Amostragem em Grandes
Volumes de Dados em Redes Sociais Digitais.* Dissertação de Mestrado, Departamento
de Informática, PUC-Rio, 51 p. Orientador: Sérgio Lifschitz. Defesa: 11/04/2025
(banca: Colcher, Haeusler, Jonice de Oliveira/UFRJ). PDF:
`Dissertação_de_Mestrado_Alexandre Heine_VFinal_ajustada.pdf`.
Código: <https://github.com/Maxteralex/representative-dataset-problem>.

**Por que este caso é especial.** O Heine é da **mesma linhagem** (eTC/TreeTech,
orientador Lifschitz) e a dissertação dele é literalmente o **precursor metodológico**
da dissertação da Mariana: enquanto Ituassu et al. *sub-coletaram sem perceber*, o
**Heine já fez ele mesmo a comparação amostra × dataset completo** — e concluiu que
**a amostra falha** em reproduzir o todo (na modelagem de tópicos). Isto é o espelho
do caso Twitter: lá a expansão *derrubou* uma conclusão da amostra; aqui o autor **já
partiu** medindo os dois lados. O nosso valor agregado é (a) checar se a conclusão
dele replica no universo com método reprodutível, (b) medir *em que fração* cada
análise **converge**, e (c) atacar a **suspeita metodológica que o próprio Heine deixou
em aberto** (a fórmula de tamanho de amostra por proporção não governa a estabilidade
de uma "medida composta" como o sentido de um texto — ver §5).

---

## 1. O que o Heine coletou

- **Rede:** X/Twitter (API Acadêmica de Busca Histórica, coletada fev–mai/2023,
  pouco antes da API acadêmica gratuita ser desligada).
- **Tema:** 2º turno das eleições presidenciais brasileiras de **2022** (Lula × Bolsonaro),
  em parceria com o Prof. Ituassu (Comunicação/PUC-Rio) para montar a query.
- **Janela de coleta (dois blocos):**
  1. **2–16/out/2022** (2/out = votação do 1º turno);
  2. **24–31/out/2022** (30/out = votação do 2º turno).
- **Query (termos):** `Lula OR PT OR PL OR Bolsonaro OR Jair Bolsonaro OR
  #Eleições2022 OR #PT OR #PL OR #13 OR #22 OR #Bolsonaro OR #mito OR #Lula OR
  #bolsonaro2022 OR #bolsonaropresidente OR #SuperLiveBolsonaro22 OR
  #BolsonaroNoPrimeiroTurno OR #BolsonaroOrgulhoDoBrasil OR #BolsonaroReeleitoEm2022
  OR #PrimeiramenteLulaNaCadeia OR #LulaLadrao OR #BolsonaroPresidente22 OR
  #FelizAniversarioBolsonaro OR #lulapresidente OR #brasildaesperanca OR
  #LulaPresidente13 OR #ForaBolsonaro OR #BolsonaroVagabundo OR #3JForaBolsonaro OR
  #LulaNoPrimeiroTurno13 OR #LulaNo1ºTurno OR #LulaNoJN OR #LulaNoFlow` (p.22–23).
- **Volume:** **57,9 milhões** de tweets (≈16 GB), armazenados primeiro em **MongoDB**
  (resposta JSON da API) e depois carregados em **PostgreSQL** (esquema conceitual de
  RSD do grupo TreeTech, Fig. 5.1) para as análises quantitativas.

> ⚠ **Nota de escopo de query.** A query do Heine é **ampla por candidato/partido**
> (Lula/PT/PL/Bolsonaro + ~28 hashtags), não uma hashtag-âncora única como o
> #Eleições2014 do caso Twitter. Isso muda o eixo "escopo temático" (E2): aqui o
> escopo já nasce largo; a expansão de escopo interessante é *hashtag-a-hashtag* /
> *termo-a-termo* dentro dessa query, não abrir de uma tag para várias.

---

## 2. As duas análises do Heine (os alvos da replicação)

O Heine roda **duas** análises com objetivos metodológicos distintos:

| # | Análise | Pergunta metodológica do Heine | Resultado dele |
|---|---|---|---|
| **A** | **Modelagem de tópicos** (Cap. 4) | uma **amostra estatística** (n por fórmula de proporção) reproduz os tópicos do dataset completo? | **NÃO** — random e stratified falham |
| **B** | **Estatística quantitativa via SGBD** (Cap. 5) | um **banco relacional** consegue rodar as análises no volume inteiro sem estourar memória? | **SIM** — 57,9 mi sem problema |

São análises de **naturezas opostas** para a nossa tese: a **A** é o caso em que a
sub-coleta **quebra** a conclusão (tópicos são sensíveis a volume); a **B** é o caso
em que o volume inteiro é **viável e barato** (então "coletar mais" é grátis) — e,
como veremos, as conclusões quantitativas provavelmente **convergem cedo**. O contraste
**A × B** é o argumento-mãe deste caso.

---

## 3. Eixo A — Modelagem de tópicos (Cap. 4)

**Dataset:** **1.291.891** tweets de **um único dia** (2/out/2022, dia do 1º turno).
**Amostragem:** tamanho calculado pela fórmula de proporção (§5), com **nível de
confiança 99% e margem ±1%**:

```
n0 = Z²·p·q / e²  = 2,575²·0,5·0,5 / 0,01²  = 16.577   (população infinita)
n  = n0 / (1 + (n0−1)/N),  N = 1.291.891     = 16.367   (correção p/ finita)
```

Na prática o Heine usou **19.032** tweets (acima do mínimo). Duas amostragens:

- **Random sampling** — 19.032 tweets aleatórios. **80 tópicos**; os 8 maiores
  analisados (0 "Eleição de Lula", 1 "Política brasileira", …, 7 "Polarização").
- **Stratified sampling** — estratificado **por hora do dia** (proporção horária igual
  à do dia completo). **81 tópicos**; tópicos 0–7 identificados (0 "Votação nos
  candidatos", …).

**Pipeline (BERTopic):** Sentence-BERT multilíngue
(`paraphrase-multilingual-MiniLM-L12-v2`) → UMAP (cuML/GPU) → HDBSCAN (cuML) →
CountVectorizer (sklearn) → **nomeação dos tópicos por LLM (Gemini)**.

**Dataset completo:** processado em **2 metades**, tópicos de cada metade **mesclados**
por similaridade de embeddings de tópico (recurso do BERTopic). Resultou em **1.539
tópicos** (muitos pequenos — efeito do volume maior). Tópicos 0–6 + 11 identificados
(0 "Brasil e questões políticas/sociais", …, 11 "discriminação/preconceito ligados a
Bolsonaro").

### Achados do eixo A (o que replicar/derrubar)

- **AH1 — a amostra não reproduz a distribuição de tópicos do todo.** Treinando o
  modelo na amostra e classificando o dataset completo, a **ordem** dos tópicos e as
  **proporções** não batem (fora da margem ±1%), exceto os 2 primeiros. Fig. 4.3 (random).
- **AH2 — stratified é um pouco melhor que random, mas ainda falha.** Mais tópicos da
  amostra sobrevivem no todo, porém ainda fora da margem. Fig. 4.6.
- **AH3 — o caminho inverso também falha.** Treinando no **todo** e classificando a
  amostra, **os 10 tópicos principais do todo não estão entre os principais da
  amostra** (Fig. 4.11) → "random garante ausência de viés, mas falha na
  representatividade para tópicos".
- **AH4 — só sobrevivem tópicos genéricos** ("povo brasileiro", "Lula presidente já no
  1º turno"), e mesmo esses com **distribuição diferente** entre amostra e todo.
- **Conclusão do Heine (Cap. 6.1):** amostragem aleatória **não** obteve o resultado
  esperado, *mesmo com o n calculado por fórmula*. O dataset completo (por mesclagem de
  clusters) é viável e é o que garante representatividade.

---

## 4. Eixo B — Estatística quantitativa via SGBD (Cap. 5)

**Dataset:** os **57,9 mi** de tweets (os dois blocos de out/2022). **Ferramenta:**
PostgreSQL com o esquema conceitual TreeTech (Fig. 5.1). Duas análises:

- **B1 — postagens por faixa de engajamento.** Engajamento por tweet via pesos de
  `likes/retweets/quotes/replies`, calibrados pelo **ETA** (Engajamento Total da
  Amostra). Pesos obtidos (Tab. 5.1): eta ≈ 2,894×10¹¹; peso_like ≈ 40,90;
  peso_retweet ≈ 0,252; peso_quote ≈ 1847,8; peso_reply ≈ 879,3.
  - **Achado B1:** distribuição **quase long-tail** — mas as **3 primeiras faixas** têm
    contagens próximas (queda gradual, não abrupta) e a **última faixa cresce** em
    relação à penúltima. Queda gradual abaixo de 10.000 de engajamento.
- **B2 — postagens ao longo do tempo.** Contagem por dia nos dois blocos.
  - **Achado B2:** picos **exatamente nos dias de votação** (2/out e 30/out); aumento
    nos dias que antecedem o 2º turno.
- **Conclusão do Heine (Cap. 6.2):** o SGBD relacional rodou as 57,9 mi de linhas com
  várias operações encadeadas **sem estourar hardware** → viabilidade do "coletar mais"
  para análise quantitativa.

---

## 5. ⚠ A suspeita metodológica que o Heine deixou em aberto (nosso gancho de ouro)

Nos **Trabalhos Futuros** (Cap. 6.3), o Heine levanta *ele mesmo* a dúvida central:

> *"é importante verificar se a discrepância entre a amostragem aleatória e a análise
> do conjunto completo ocorreu devido ao tamanho da amostra não ser suficiente, ou
> seja, à premissa de que as fórmulas para cálculo da quantidade de dados … também
> deveriam funcionar para uma medida composta como o sentido de um texto."*

E conjectura: como o sentido vive num **vetor de embeddings**, a margem de erro do
"sentido" seria o **produtório** das margens por posição do vetor — logo o n correto
seria muito maior que o da fórmula de proporção escalar.

**Isto é a fresta que a replicação da Mariana ocupa.** A fórmula
`n0 = Z²pq/e²` governa a estabilidade de **uma proporção escalar** (uma classe binária),
não de um objeto de **alta dimensão** (a distribuição de tópicos sobre um espaço de
embeddings). Nossa contribuição no eixo A é **medir a curva de convergência real**: a
que fração N a distribuição de tópicos (por JS-divergence / RBO entre rankings)
estabiliza — e mostrar empiricamente que esse ponto é **muito acima** do n=16.367 da
fórmula. Ou seja: o Heine **não errou o n por descuido** — o n de proporção é
**inaplicável** à tarefa. Isso conversa direto com o achado da survey (amostragem
estatística é rara e, quando usada, é calibrada para a métrica errada).

---

## 6. Decisões pendentes deste caso (a fixar antes de rodar)

1. **Localizar a tabela 2022 no eTC_Producao** (nome/colunas) e confirmar se são as
   57,9 mi completas ou uma coleta vizinha (como no caso 2014). Script:
   `diagnostico/lista_tabelas.py` + `diagnostico/explora_heine.py`.
2. **Reproduzir o subconjunto de tópicos** = o "1 dia (2/out)" com ~1,29 mi. Confere
   com a contagem do banco? Se não bater, já é achado (a própria base mudou).
3. **Reconstruir os pesos de engajamento (ETA)** e ver se batem com a Tab. 5.1 —
   sanity check agregado do eixo B.
4. **BERTopic reprodutível sem GPU/Gemini.** O Heine usou cuML (GPU) + Gemini para
   nomear. Para reprodutibilidade: rodar CPU (umap-learn/hdbscan) e nomear tópicos por
   c-TF-IDF (sem LLM), ou LLM local/documentado. Decidir o classificador de nome.
5. **Métrica de "os tópicos mudaram?".** Fixar: JS-divergence entre distribuições de
   tópicos; RBO/Kendall-τ entre rankings de tópicos; nº de tópicos-âncora que
   sobrevivem. (Análogo às métricas do protocolo do caso Twitter.)
6. **Faixas de engajamento.** Reproduzir exatamente os cortes de faixa do Heine para o
   B1 (o PDF mostra os gráficos, não a tabela de cortes — extrair da consulta/figuras).

---

*Docs irmãos: [REPLICACAO_CASO_HEINE.md](REPLICACAO_CASO_HEINE.md) (plano de fases) ·
[EIXO_TOPICOS.md](EIXO_TOPICOS.md) · [EIXO_QUANTITATIVO.md](EIXO_QUANTITATIVO.md).*
