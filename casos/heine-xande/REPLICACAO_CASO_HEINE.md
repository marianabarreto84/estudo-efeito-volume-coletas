# Caso de replicação · Twitter/X · Heine & Lifschitz (2025) — Amostragem 2022

> Caso da dissertação da Mariana espelhado no fluxo do caso Twitter/Ituassu
> (`../pesquisa-twitter-refeita`). Alvo: a **dissertação do Alexandre Heine (2025)**,
> *Um Estudo sobre Amostragem em Grandes Volumes de Dados em RSD* — o **precursor
> metodológico direto** da linhagem eTC/TreeTech. Rede: **Twitter/X**. Tema:
> eleições **2022** (Lula × Bolsonaro). Análises: **modelagem de tópicos** (eixo A) +
> **estatística quantitativa** (eixo B). Detalhe do alvo em
> [DISSERTACAO_HEINE_alvo.md](DISSERTACAO_HEINE_alvo.md).

**Valor deste caso no lineup.** Fecha a linhagem *por dentro*: o orientador (Lifschitz)
é o mesmo, e o Heine **já executou a comparação amostra × completo** que a dissertação
da Mariana generaliza. Diferente de todos os outros casos (onde o autor sub-coletou
sem testar), aqui o **próprio autor** mediu os dois lados e concluiu que **a amostra
falha na modelagem de tópicos**. A replicação vira, então, três coisas: (i) confirmar
o achado dele com método reprodutível; (ii) transformá-lo numa **curva de convergência**
(a que fração N cada análise estabiliza); (iii) responder à **pergunta que ele deixou
aberta** — a fórmula de tamanho de amostra por proporção é o instrumento errado para
"medida composta" (sentido de texto). Ver [alvo §5](DISSERTACAO_HEINE_alvo.md).

---

## 0. O que muda em relação ao caso Twitter/Ituassu

| Dimensão | Caso Ituassu (compos2014) | **Caso Heine (heine2022)** |
|---|---|---|
| Alvo | 2 papers (2015 n=700, 2018 n=1.129) | 1 dissertação (2025) |
| Ano dos dados | 2014 (Dilma × Aécio) | **2022 (Lula × Bolsonaro)** |
| Recorte de coleta | 1 hashtag-âncora (#Eleições2014) | **query ampla** (Lula/PT/PL/Bolsonaro + ~28 hashtags) |
| Análises replicadas | mídia (MV/MH → MP/MC) + stance | **tópicos (BERTopic)** + **quantitativa (engajamento/tempo)** |
| Volume no banco | 10,7 M (coleta 2014) | **57,9 M** (coleta 2022) |
| O autor testou amostra×todo? | **não** (sub-coletou sem perceber) | **sim** (é a tese dele) |
| Parte que trava | stance (rotulagem humana) | **nomeação de tópicos** (reprodutibilidade do LLM) |

**Consequência de desenho:** aqui a nossa contribuição não é "descobrir que a amostra
não bastava" (o Heine já disse), e sim **quantificar a convergência** e **corrigir o
diagnóstico** (o problema não é o tamanho da amostra por descuido, é a métrica de
tamanho ser inadequada à tarefa).

---

## 1. Afirmações testáveis (a camada substantiva)

Do **eixo A — tópicos** (Cap. 4 do Heine):

- **AH1 — amostra não reproduz os tópicos do todo** (ordem+proporção fora de ±1%).
- **AH2 — stratified > random, mas ainda falha.**
- **AH3 — o inverso também falha** (top-10 do todo ausente da amostra).
- **AH4 — só tópicos genéricos sobrevivem**, e com distribuição diferente.

Do **eixo B — quantitativa** (Cap. 5):

- **BH1 — engajamento quase long-tail**, com 3 primeiras faixas próximas e repique na
  última faixa.
- **BH2 — picos de volume nos dias de votação** (2/out e 30/out).
- **BH3 (metodológica) — o SGBD roda 57,9 M sem estourar** ("coletar mais" é viável).

---

## 2. A ressalva metodológica honesta

Como no caso Twitter, o banco eTC não é necessariamente o **universo exato** de onde o
Heine tirou os números — pode ser a mesma coleta (57,9 M) ou uma coleta vizinha. Duas
frentes:

- Se a tabela do banco **é** a coleta 2022 do Heine (57,9 M), então temos o **universo
  dele** — comparação limpa amostra × todo, sem efeito-de-escopo.
- Se for coleta vizinha (mais larga), separar **efeito-de-volume** de
  **efeito-de-escopo** como no caso Twitter (§3 daquele doc).

A Fase 0 (`diagnostico/`) resolve isso empiricamente antes de qualquer análise.

---

## 3. Os eixos de expansão (separáveis)

Cada análise do Heine ocupa um ponto restrito. Expandimos um eixo por vez.

| Eixo | Restrição (Heine) | Expansão | Isola a pergunta |
|---|---|---|---|
| **E1 · Volume (tópicos)** | amostra n≈16–19 mil (1 dia) | fração crescente até o dia completo (1,29 M) e além | "a amostra por fórmula bastava para tópicos?" |
| **E2 · Escopo temático** | query ampla por candidato | por termo/hashtag (Lula-only, Bolsonaro-only, tag-a-tag) | "o recorte de termos muda a estrutura de tópicos?" |
| **E3 · Extensão temporal** | 1 dia (2/out) p/ tópicos | vários dias / os dois blocos | "um dia representa a campanha?" |
| **E1' · Volume (quantitativa)** | — (ele já usou 57,9 M) | fração crescente de N | "em que fração as conclusões quantitativas convergem?" |

**Contraste-chave do caso:** a hipótese é que **E1' (quantitativa) converge cedo** (as
estatísticas agregadas — long-tail, picos temporais — estabilizam com poucos %), e
**E1 (tópicos) converge tarde ou nunca** dentro do orçamento amostral da fórmula. É o
mesmo objeto (coletar mais) com respostas opostas por **tipo de análise** — exatamente
a tese da dissertação.

---

## 4. Pipeline por fase

### Fase 0 — Localizar e caracterizar os dados 2022 (sanity check)
`diagnostico/lista_tabelas.py` acha a tabela 2022 no eTC_Producao; `explora_heine.py`
caracteriza schema, range de datas, preenchimento de `likes/retweets/quotes/replies`,
contagem por dia. **Checar:** o dia 2/out tem ~1,29 M? O total bate com 57,9 M? Os
pesos de engajamento reproduzem a Tab. 5.1?

### Fase 1 — Snapshot congelado
`pipeline/extrai_snapshot_heine.py` extrai para SQLite local:
- **snapshot_dia1.sqlite** — 2/out/2022 completo (universo de tópicos, ~1,29 M) — ou
  amostra materializada + metadados de estrato, se 1,29 M for grande demais p/ local.
- **snapshot_quant.sqlite** / views agregadas — para o eixo B (contagens por
  faixa/tempo; não precisa trazer as 57,9 M linhas cruas, e sim as **agregações** via
  SQL no servidor).

### Fase 2 — Curva de convergência (o coração)
- **Eixo A (tópicos):** frações crescentes do dia (p.ex. 1%, 5%, …, 100%), **≥30
  réplicas bootstrap/ponto**, medindo a distância entre a distribuição de tópicos da
  fração e a do todo (JS-divergence) e a estabilidade do ranking (RBO). Sobrepor o
  n=16.367 da fórmula e mostrar onde a curva realmente estabiliza.
- **Eixo B (quantitativa):** frações crescentes de N, medindo a estabilidade das faixas
  de engajamento (JS entre histogramas) e da série temporal. Esperado: platô cedo.

### Fase 3 — Divergência (métricas)

| Análise | Métrica | Afirmação que pode inverter/confirmar |
|---|---|---|
| **Tópicos** | JS(dist. tópicos fração × todo); RBO(rankings); nº tópicos-âncora sobreviventes | AH1–AH4 replicam? A que fração converge (vs n da fórmula)? |
| **Engajamento** | JS(histograma de faixas fração × todo); forma long-tail | BH1 estável a partir de que %? |
| **Temporal** | erro relativo da série por dia; posição dos picos | BH2 (picos nos dias de votação) estável a partir de que %? |

### Fase 4 — Tabela mestre + recomendação
Linha do caso: *a amostra bastava? × a conclusão mudou? × fração mínima que estabiliza
cada conclusão* — com o **contraste tópicos (tarde) × quantitativa (cedo)** como
resultado-título, e a **correção do diagnóstico do Heine** (métrica de tamanho errada
para tarefa composta) como contribuição metodológica.

---

## 5. Onde apostar (predições pré-registradas — antes de rodar)

- **Provável CONFIRMA (não muda):** AH1/AH3 — tópicos da amostra **não** reproduzem o
  todo. Efeito estrutural (alta dimensão). Mas ver contraponto: no caso Twitter uma
  aposta "robusta" foi refutada — registrar humildade.
- **Provável CONVERGE CEDO:** BH1/BH2 — engajamento e picos temporais estabilizam com
  poucos % (estatística agregada de baixa dimensão).
- **Incerto / mais interessante:** *a que fração exata* a estrutura de tópicos
  estabiliza, e **quão acima** do n=16.367 da fórmula isso fica. É o número que sustenta
  o argumento "a fórmula de proporção é o instrumento errado".

---

## 6. Decisões pendentes (específicas deste caso)

1. Tabela/colunas 2022 exatas (Fase 0). Confirmar universo 57,9 M vs coleta vizinha.
2. BERTopic reprodutível **sem GPU/Gemini** (CPU: umap-learn + hdbscan; nomeação por
   c-TF-IDF ou LLM documentado). Ver [EIXO_TOPICOS.md](EIXO_TOPICOS.md).
3. Cortes exatos das faixas de engajamento do Heine (extrair das figuras/consulta).
4. Tamanho local do snapshot do dia 2/out (1,29 M) — cabe em SQLite? senão, amostrar +
   guardar embeddings.
5. Reportar a **inadequação da fórmula de proporção** para tópicos como achado central
   (não só nota) — é a resposta ao Trabalho Futuro do próprio Heine.

---

*Docs irmãos: [DISSERTACAO_HEINE_alvo.md](DISSERTACAO_HEINE_alvo.md) (alvo detalhado) ·
[EIXO_TOPICOS.md](EIXO_TOPICOS.md) · [EIXO_QUANTITATIVO.md](EIXO_QUANTITATIVO.md).
Protocolo geral e caso-irmão em `../pesquisa-twitter-refeita/REPLICACAO_CASO_COMPOS2014.md`.*
