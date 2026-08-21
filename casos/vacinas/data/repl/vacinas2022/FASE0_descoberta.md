# Fase 0 — Descoberta dos dados (caso vacinas 2021-22)

> Log da localização da coleta do preprint Verjovsky et al. no cluster Cloud-DI
> (PUC-Rio). Executado em 23/jul/2026, ao vivo, via `core/db.py` (túnel SSH sobre a
> VPN). Consultas reproduzíveis; contagens exatas (não estimativas do planner).

## ✅ CONCLUSÃO: a coleta ESTÁ acessível — vm031 / eTC_Producao, busca id=178

| | |
|---|---|
| **VM / banco** | vm031 (10.50.0.32) / `eTC_Producao` |
| **Busca (tabela `busca`)** | **id_busca = 178** |
| **Assunto (query)** | `vacinar OR vacinação OR vacina OR antivacina OR antivax OR vacinação infantil` |
| **Janela declarada** | 2021-12-09 a 2022-02-09 (idêntica à do paper) |
| **Inserida em** | **2022-05-18** (re-coleta full-archive, posterior ao paper) |
| **Volume** | **6.554.705** registros = **4.507.889 retweets + 2.046.816 originais** |
| **Datas efetivas nos dados** | 2021-12-08 a 2022-02-08 (UTC vs America/Sao_Paulo explica o off-by-one) |

**Bate com o paper:** ">1 M tweets and 4 M retweets" → 2,0 M originais / 4,5 M RTs. ✓

Busca vizinha: **id=171** — `(vacinar OR vacinação OR vacina OR antivacina OR antivax)`,
só jan/2022, 1.228.495 registros, **0 retweets** (coleta sem RTs). Pode servir de
contraste de escopo, mas o universo do caso é a 178.

## Caminho do dado (schema eTC, vm031)

`busca (id_busca=178)` → `dia_de_busca (id_busca_id=178 → id_dia)` →
`tweet (id_dia_busca_id = dia_de_busca.id_dia)`.

Colunas úteis da `tweet`: `twitter_id, autor, autor_id, nome_autor, texto, data,
likes, retweets, replies, quotes, idioma, status_retweet, tweet_tipo,
tweet_referenciado_id, autor_original, hashtags, mencoes, num_seguidores,
status_verificado` — tem tudo para os dois eixos (grafo de RTs via
`status_retweet`/`tweet_referenciado_id`/`autor_original`; conteúdo via `texto`).

⚠ O schema da vm031 é uma versão mais antiga do eTC que a vm067 (a `busca` não tem
`plataforma`; a FK de `dia_de_busca` é `id_busca_id` e a PK é `id_dia`).

## Sanity check do estrato viral (originais da busca 178)

| Limiar | Tweets | Autores distintos |
|---|---|---|
| >500 RT | 1.686 | **730** |
| >250 RT | 3.384 | 1.200 |
| >100 RT | 6.836 | 2.223 |
| >50 RT | 11.207 | 3.546 |
| >10 RT | 34.866 | 11.317 |

O paper reporta **602 autores influentes** (>500 RT). Achamos **730** — mesma ordem,
e a diferença tem explicação natural: as contagens de `retweets` aqui são da
**re-coleta de mai/2022**, dois meses depois do update de 8/mar do artigo → mais
tweets cruzaram o limiar. Isso é um dado do caso, não um problema: reforça que o
estrato ">500 RT" é **instável no tempo**, além de arbitrário.
**A separar nas análises: efeito-de-época (contagens de RT) × efeito-de-limiar.**

## Descartado no caminho (rastreabilidade)

- **vm067 / eTC_Producao:** as 119 buscas são eleições municipais 2020, 2014 (id 121),
  2018 (124–128), corona mar/2020 (129), populismo (114), Reddit. **Nenhuma busca de
  vacinas**; as inserções pulam de dez/2021 direto para mar/2022 — a coleta vacinas
  nunca morou lá.
- A varredura ampla das 3 VMs já tinha sido feita na Fase 0 do caso Heine
  (`../../../../heine-xande/data/repl/heine2022/FASE0_descoberta.md`), que registrou
  de passagem: vm031 "dominado por buscas de vacina (id 178 = 6,5 M; id 171 = 1,2 M)"
  — foi a pista que este log confirma.

## Próximos passos (Fase 1)

1. `pipeline/extrai_snapshot_vacinas.py`: snapshot SQLite local da busca 178 —
   originais (2,0 M: texto + autor + engajamento) + arestas de RT (4,5 M:
   retuitador → autor_original/tweet_referenciado_id). Estimar tamanho antes;
   agregações pesadas via SQL no servidor.
2. Confirmar acesso à **planilha suplementar** do paper (Apêndice A) — gabarito dos
   rótulos para o eixo de conteúdo.
3. Registrar (com a Mariana) se o paper usou esta mesma busca 178 ou uma coleta
   streaming de época que a 178 re-coletou — afeta só a narrativa, não o desenho
   (o universo do caso é a 178).
