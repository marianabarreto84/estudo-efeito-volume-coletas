# Fase 1 — Snapshot congelado (busca 178 → SQLite local)

> Extraído em **23/jul/2026** por `pipeline/extrai_snapshot_vacinas.py` (log em
> `extracao.log`). Fonte: vm031 / eTC_Producao, busca 178. Arquivo:
> `snapshot_vacinas.sqlite` (**1,78 GB** — nunca versionar).

## Conteúdo

| Tabela | Linhas | O que é |
|---|---|---|
| `originais` | **2.046.816** | tweets não-RT: texto, autor, data, likes/retweets/replies/quotes, idioma, seguidores, verificado. ⚠ as colunas `hashtags`/`mencoes` existem mas vieram **vazias** — ver Achado 1 |
| `rt_arestas` | **4.507.889** | retweets como arestas retuitador → autor original (sem texto) |
| `meta` | 9 | proveniência (busca, query, janela, datas, contagens) |

Índices: `retweets`, `autor`, `data` (originais); `tweet_referenciado_id`, `autor`,
`autor_original` (arestas).

## Validação (bate com a Fase 0)

- Contagens **exatas**: 2.046.816 originais / 4.507.889 RTs. ✓
- Estrato viral: **>500 RT = 1.686 tweets / 730 autores** (idêntico à Fase 0). ✓
- Range de datas: 2021-12-08T23:00 a 2022-02-08T22:59 (−03:00) — é a janela
  9/dez–9/fev em UTC. ✓

## ⚠ Achados a considerar nas Fases 2–3

1. **Colunas 100% vazias no snapshot** ⚠ *(revisto em 07/ago/2026 — a versão
   anterior deste item citava só `tweet_referenciado_id` e afirmava, **erradamente**,
   que `autor_referenciado` estava 100% preenchido; ele está 0%)*.

   Varredura completa de nulidade (`PRAGMA table_info` + contagem por coluna):

   | Tabela | 100% **vazias** | 100% **cheias** |
   |---|---|---|
   | `originais` (2.046.816) | `autor_id`, `tweet_tipo`, `tweet_referenciado_id`, `autor_original`, `conversa_id`, **`hashtags`**, **`mencoes`** | `twitter_id`, `autor`, `nome_autor`, `texto`, `data`, `idioma`, `likes`, `retweets`, `replies`, `quotes`, `num_seguidores`, `status_verificado` |
   | `rt_arestas` (4.507.889) | `autor_id`, `tweet_referenciado_id`, `autor_referenciado` | `twitter_id`, `autor`, `data`, `autor_original` |

   São **7 de 19** colunas em `originais` e **3 de 7** em `rt_arestas`. O padrão é
   sistemático: caem todos os **ids numéricos** de referência e os campos que o
   **schema antigo da vm031** provavelmente mantém em tabelas à parte
   (`hashtags`, `mencoes`, `tweet_tipo`).

   ### ✅ Causa verificada na fonte (07/ago/2026) — **é (a): vazias na origem**

   Rodado `diagnostico/checa_colunas_vazias_na_fonte.py` + contagem completa (sem
   `LIMIT`) na **vm031 / eTC_Producao**, sobre a busca 178 inteira:

   | coluna | originais (2.046.816) | retweets (4.507.889) |
   |---|--:|--:|
   | `hashtags`, `mencoes`, `tweet_tipo`, `conversa_id`, `autor_id`, `tweet_referenciado_id`, `autor_referenciado` | **0,00%** | **0,00%** |
   | `autor_original` | 0,00% | **100,00%** |
   | `texto`, `idioma`, `retweets` | 100,00% | **100,00%** |

   As colunas **existem** na tabela `tweet` da vm031 (tipos `ARRAY`, `bigint`,
   `varchar`) e estão **vazias para esta coleta**. O snapshot bate exatamente com a
   fonte: **a extração foi fiel, não há bug de pipeline**. Hipótese (b) — dado em
   outra tabela — descartada: não há tabela de relação de hashtag/menção no schema
   (só `tweet`, `adr_arestas`, `analise_de_retweeters`, `post_facebook`).

   ⚠ **Armadilha registrada:** o diagnóstico precisa usar `conectar(vm="vm031")`.
   Com `conectar_auto` cai-se na **vm067** (a da coleta contínua e da `ituassu_2014`)
   e a resposta é sobre o servidor errado — aconteceu na primeira execução.

   **O que isso permitiu mesmo assim:** o grafo de RT sai no **nível de autor**
   (`autor` → `autor_original`, ambos TEXT e 100% cheios), que é o que a
   modularidade do eixo A precisa; e "RTs por tweet" (AV2/AV4) usa a coluna
   `retweets` dos originais, sem precisar ligar RT→tweet.

   ### O que isso custa de verdade — **menos do que parecia**

   ⚠ *A versão anterior deste item dizia que "qualquer análise por hashtag ou menção
   fica impedida". **Errado.*** O `texto` está 100% preenchido nas duas tabelas:

   - **Hashtags e menções: recuperáveis por regex sobre `texto`**, e o `texto` dos
     originais **já está no snapshot local**. O E3 por hashtag **não precisa de
     re-extração nem de VPN** — é `#\w+` sobre `originais.texto`.
   - **Elo RT→tweet: parcialmente recuperável.** O `texto` dos retweets existe na
     fonte no formato clássico `RT @autor_original: <primeiros ~140 caracteres>`.
     Casar (`autor_original`, prefixo) contra `originais.texto` identifica o tweet
     retuitado na maioria dos casos (ambíguo só quando o mesmo autor publicou dois
     tweets com prefixo idêntico). **Mas exige re-extrair os textos dos RTs** — a
     extração original os descartou de propósito (`rt_arestas` é "sem texto"), são
     4,5 M linhas. Valor marginal moderado: já temos `retweets` por tweet pela API,
     e foi com ela que o AV4 reproduziu os 15,7% do artigo.
   - **Perda real e irrecuperável:** nenhuma identificada.
2. **Idiomas nos originais:** pt 1.713.885 (83,7%) · fr 151.046 · en 104.023 ·
   und 28.840 · es 26.940 · resto ~22 k. Os termos-índice em PT capturaram
   bastante não-PT (ex.: "vacina/vaccination" em outras línguas). O paper fala em
   narrativas **em português** — decidir e registrar na Fase 2 se as análises
   filtram `idioma='pt'` (e reportar sensibilidade a esse filtro; é mais um
   critério de recorte implícito do alvo).
3. Contagens de `retweets`/`likes` são da **re-coleta de mai/2022** (ver Fase 0):
   toda comparação com os números do paper (602 vs 730 autores etc.) deve citar
   essa diferença de época.
