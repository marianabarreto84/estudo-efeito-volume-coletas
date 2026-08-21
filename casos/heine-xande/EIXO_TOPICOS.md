# Eixo A — Modelagem de tópicos (BERTopic): como o Heine fez e como replicamos

> Eixo **tópicos** da replicação da dissertação do Heine (Cap. 4). É o eixo em que a
> sub-coleta **quebra** a conclusão: amostra estatística ≠ dataset completo. Plano em
> [REPLICACAO_CASO_HEINE.md](REPLICACAO_CASO_HEINE.md); alvo em
> [DISSERTACAO_HEINE_alvo.md](DISSERTACAO_HEINE_alvo.md).

## 1. O que o Heine fez (resumo operacional)

1. Dataset = **2/out/2022 completo** (1.291.891 tweets, dia do 1º turno).
2. Tamanho de amostra pela **fórmula de proporção** (99% conf., ±1% margem) → n=16.367;
   usou **19.032**.
3. Duas amostras: **random** e **stratified por hora**.
4. Pipeline **BERTopic**: Sentence-BERT multilíngue
   (`paraphrase-multilingual-MiniLM-L12-v2`) → UMAP → HDBSCAN → CountVectorizer →
   **nomeação por LLM (Gemini)**. GPU (cuML) para UMAP/HDBSCAN.
5. Dataset completo em **2 metades** com **mesclagem de tópicos** por similaridade de
   embeddings → 1.539 tópicos.
6. Comparou treinando-na-amostra-classificando-o-todo (Fig. 4.3/4.6) e o inverso
   (Fig. 4.11).

## 2. O que replicamos (e onde melhoramos)

- **Reprodutibilidade sem GPU/LLM proprietário.** Trocar cuML por `umap-learn` +
  `hdbscan` (CPU) e a nomeação-Gemini por **c-TF-IDF** (rótulo determinístico das
  top-palavras) — ou um LLM documentado/local, se nomear for necessário. A **comparação
  de distribuições** não depende do nome do tópico, só do *cluster*, então a nomeação
  vira cosmética.
- **De "sim/não reproduz" para curva de convergência.** Em vez de comparar só
  amostra(19k) × todo, medir a distância entre a distribuição de tópicos de **frações
  crescentes** (1%,5%,…,100%) e a do todo, com **≥30 réplicas bootstrap** por fração.
- **Corrigir o diagnóstico.** Sobrepor o n=16.367 (fórmula de proporção) à curva real
  de convergência e mostrar que a estabilização exige **muito mais** que isso → a
  fórmula escalar é inadequada à tarefa composta (resposta ao Trabalho Futuro do Heine,
  Cap. 6.3).

## 3. Métricas de "os tópicos mudaram?" (fixar no protocolo)

- **JS-divergence** entre a distribuição de proporção de tópicos da fração e a do todo
  (após projetar a fração no modelo do todo, como o Heine fez nas Figs. 4.3/4.6/4.11).
- **RBO** (rank-biased overlap) e **Kendall-τ** entre os rankings de tópicos.
- **Nº de tópicos-âncora sobreviventes** — quantos dos top-k do todo aparecem nos top-k
  da fração (o teste que o Heine fez à mão na Fig. 4.11).
- **Estabilidade de partição** entre réplicas (ARI/AMI) — sanidade do bootstrap.

## 4. Decisões pendentes do eixo

1. Motor de embeddings idêntico ao do Heine (`paraphrase-multilingual-MiniLM-L12-v2`)
   para comparabilidade — sim.
2. CPU vs GPU: CPU garante reprodutibilidade; GPU (se disponível) acelera as ≥30
   réplicas × ~10 frações. Decidir conforme hardware.
3. Nomeação: c-TF-IDF (reprodutível) como padrão; LLM só para o texto final da
   dissertação, marcado como interpretativo.
4. Semente/aleatoriedade do UMAP (estocástico) — fixar `random_state` e reportar
   variância entre réplicas.

## 5. Predição pré-registrada

A estrutura de tópicos **não** estabiliza no n da fórmula (16.367); a curva de JS só
achata numa fração **bem maior** (aposta: dezenas de % do dia, ou exige o dia inteiro).
Tópicos genéricos ("Lula presidente", "povo brasileiro") estabilizam antes dos
específicos. Registrar antes de rodar — como no caso Twitter, a aposta pode falhar.
