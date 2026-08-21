# Fase 0 — Descoberta dos dados (caso Heine 2022)

> Log da caça à coleta 2022 do Heine no cluster Cloud-DI (PUC-Rio). Gerado durante a
> execução; números vêm de consultas ao vivo (rastreáveis).

## Infra confirmada
- VPN Cloud-DI no ar → VMs internas: **vm031** (10.50.0.32), **vm037** (10.50.0.38),
  **vm067** (10.50.0.68). SSH como `cloud-di`. Postgres via túnel (localhost:5432).
- Credenciais Postgres `postgres/postgres` funcionam em **vm031** e **vm067**;
  **na vm037 o Postgres rejeita** essas credenciais (senha do banco é outra).

## Onde procurei (e o que tem)

### vm067 / eTC_Producao (o banco do caso Twitter/Ituassu)
- `tweet` (15,2 M / 16 GB), `ituassu_2014` (10,7 M — fonte do caso 2014),
  `reddit_posts`/`comments_reddit` (caso Reddit do lineup!).
- Buscas: 2014 (id 121 = #Eleições2014), 2018 (#Eleições2018). **2022 = só testes**
  ('teste', 'natal', 'ancap', '@franciamarquezm'). → **não é a coleta do Heine.**

### vm031 / eTC_Producao
- `tweet` (20,2 M / 16 GB), dominado por buscas de **vacina** (id 178 = 6,5 M;
  id 171 = 1,2 M) e coleta contínua 2020.
- Única busca eleitoral 2022: **id=245** `'Lula, Bolsonaro, #Eleicoes2022 -is:reply
  -is:retweet'`, 30/set–30/out/2022, **24.907 tweets** — 50× menor que o 1,29 M/dia
  do Heine. id=209 `'#Eleicoes2022 #debatenaglobo'` = 15.110.
- → a busca eleitoral registrada é **pequena demais** para ser o dataset do Heine.

### vm031 / crawler · crawler_teste_2 · tcweb · tcweb_teste
- Schema `tweet_collected` (tweet_id, tweet_text, tweet_timestamp, tweet_likes/
  retweets/replies, tweet_views, tweet_media, tweet_links) — **modelo "MongoDB→PG"**,
  diferente do eTC. Tamanhos 0,6–2,0 M.
- ⚠ Datas **2010–2021** em todos → **não são 2022**. (O 1,29 M de `tcweb_teste` foi
  coincidência: é 2018–2021.)

### vm031 / etc_hanna · etc_oliver · etc_tomaz
- Vazios (sem tabelas de tweets).

### vm037
- SSH ok (senha `VM_037_PASSWORD`), **Postgres pede credencial própria** (pendente).

## Teste decisivo — FEITO (elimina a vm031)
Contagem direta em **vm031/eTC_Producao.tweet** (range global 2010-10 a 2023-06):
- **2022-10-02: 7.970** tweets (alvo do Heine: ~1.291.891) ❌
- **out/2022 inteiro: 88.047** tweets (alvo: parte dos 57,9 M) ❌
→ a coleta do Heine **NÃO está na vm031**. Por eliminação (vm067 e vm031 varridos),
está na **vm037**, cujo **Postgres exige credencial própria** (SSH já ok). **Bloqueado
aguardando o usuário/PG-creds da vm037** (ou o schema/DSN no repo do Heine).

## Pista da dissertação + repo (analisado)
Heine (p.15): código em `github.com/Maxteralex/representative-dataset-problem`;
dataset completo "por contato via https://etc.biobd.inf.puc-rio.br/".

**Repo analisado** (notebooks `bertopic_use_case_1st_turn_day/berttopic_{random,
stratified,full}.ipynb`): os notebooks **leem de CSV**, não do Postgres:
- `1st_turn_day.csv` — dataset completo do 1º dia (2/out, ~1,29 M);
- `1st_turn_day_random_sample.csv` — amostra random.
- Coluna de texto: **`content_text`** (schema próprio — nem `texto` do eTC nem
  `tweet_text` do crawler → reforça que a base do Heine é dedicada, provável vm037).

**Parâmetros exatos do BERTopic do Heine (para replicar fiel):**
- embeddings `paraphrase-multilingual-MiniLM-L12-v2` (device cuda);
- UMAP (cuML): `n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42`;
- HDBSCAN (cuML): `min_cluster_size=15, metric='euclidean', cluster_selection_method='eom'`;
- CountVectorizer: `stop_words=portuguese, min_df=2, ngram_range=(1,2)`.

## vm037 — verificada (postgres com senha da VM): é o servidor de DISCIPLINAS
Bancos: `BDTeste` (aluno/endereco/computador), `bd124201..230`, `bd125101..115`,
`bd1sergio251B1..12`, `bd1teste24201..285`, `monitorsergio`, `sgbdbio`. São bancos de
**alunos da matéria de BD** (Lifschitz), quase todos vazios. **Sem dados de pesquisa,
sem `content_text`.**

## CONCLUSÃO da Fase 0 (busca exaustiva)
Varridos **3 VMs / 29 bancos**. Resultado:
- **Nenhuma** tabela com coluna `content_text` (assinatura do dataset do Heine).
- **Nenhuma** tabela perto de 57,9 M (a maior é 20 M, vm031/eTC_Producao.tweet, com só
  88 k em out/2022).
→ Os dados que o Heine **de fato** usou (CSVs `1st_turn_day*.csv`, coluna `content_text`)
**não estão nos Postgres alcançáveis**. Coerente com a dissertação: o bruto (57,9 M) foi
guardado em **MongoDB** (Cap. 3) e ele **exportou CSVs** para as análises. O Postgres da
vm031/067 é a coleta contínua do eTC (2014/2018/2020), não a coleta 2022 do Heine.

## MongoDB (vm031) — VERIFICADO (é onde o Heine guardou coletas)
Mongo roda **só na vm031** (em vm067/vm037 a porta abre no túnel mas o remoto recusa).
Bancos existentes:
- **`xande_search_2022-10-01` … `-31`** (um por dia) — coleção `posts`. **"xande" =
  Alexandre Heine.** ⚠ **platform = Instagram** (schema CrowdTangle: subscriberCount,
  score, statistics, account, imageText, postUrl). **Total ≈ 628.066 posts** (Out/1 =
  319 k é o maior; Out/2 = 14,8 k). Description confirma eleição 2022.
- **`reddit`** — `reddit_posts_2024-...` (714 MB) → serve ao caso Reddit do lineup.
- Sem `admin/config/local` relevantes. **Nenhum banco Twitter.**

## ⛔ CONCLUSÃO FINAL DA FASE 0
Busca exaustiva: **3 VMs, 29 bancos Postgres, 3 MongoDBs, filesystem local, repo GitHub.**
- **O Twitter 57,9 M / 1,29 M-do-dia-2 do Heine NÃO está em nada acessível.** Nem
  Postgres, nem no Mongo (que só tem a coleta **Instagram** dele), nem em CSV local.
- Provável destino do Twitter bruto: servidor/backup fora do meu alcance, máquina do
  próprio Heine, ou a ferramenta `etc.biobd.inf.puc-rio.br` (que ele indica para "acesso
  ao dataset completo"). Coerente: 16 GB de Mongo Twitter podem ter sido limpos após a
  defesa (abr/2025).

**Dado do Heine que ESTÁ acessível:** a coleta **Instagram** (xande_search, 628 k,
eleição 2022) + **Reddit**. Pode virar substrato de replicação (mesma autoria/tema), mas
**não** reproduz os números Twitter da dissertação (é outra rede, e menor).

→ **Decisão da Mariana necessária** (ver mensagem): apontar o Twitter, pivotar para o
Instagram/Reddit acessível, ou obter os CSVs do Heine.
