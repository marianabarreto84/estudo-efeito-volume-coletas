# Material suplementar do paper — baixado (o gabarito do eixo B)

> Baixado em **23/jul/2026** do Google Sheets do Apêndice A do preprint
> (id `1coSfc_t47I7GQ4YADtBxZ6NJVqQibScutmak-9sXGW4`, export público) →
> `suplementar_rotulos.xlsx` (1,07 MB). Snapshot congelado local; a planilha
> online pode mudar — a referência do caso é ESTE arquivo.

## Abas e o que servem

| Aba | Linhas | Conteúdo | Serve para |
|---|---|---|---|
| `Spreadsheet 1` | **1.525** | tweets virais rotulados: texto, ID, `Tweet_ProVax`/`Tweet_AntiVax` + ~150 colunas temáticas binárias (11 categorias + subcategorias refinadas) | **gabarito do rotulador automatizado** (validação por κ antes de descer o limiar) |
| `Authors` | **602** | os autores influentes do paper, com soma/média/ranking de RTs por autor | validação direta de **AV3** (58,6% × 40,9%) e **AV4** |
| `Table broad categories` | 16 | as 11 categorias com totais/percentuais/rankings pró e anti (= Tabela 5) | reprodução numérica de **AV5** |
| `Table subcategories` | 147 | subcategorias com totais pró/anti | checagens finas por categoria |
| `Table tweets and retweets` | 15 | distribuição tweets × retweets (= Tabela 1) | **AV1** |
| `Authors`/`Table authors` | 999 | distribuição de nº de tweets virais por autor (= Tabela 4) | AV4 (cauda) |
| `Examples` | 20 | exemplos citados no texto (tema, ID, tweet) | conferência de IDs |
| `MAXQDA spreadsheet` | 1.525 | segmentos MAXQDA: categorização nova/antiga, autor, retweets e **coluna "Grupo eTC"** | **mapa comunidade→pró/anti deles** — comparável direto com o nosso Louvain (eixo A!) |
| `MAXQDA  Categories` | 999 | tabela dinâmica das categorias MAXQDA (a favor/contra/indeterminado) | apoio |

## Implicações imediatas

1. **O eixo B está desbloqueado por completo:** 1.525 exemplos rotulados (com o
   texto) para treinar/validar o rotulador — o que o caso Ituassu nunca teve no
   stance.
2. **A coluna "Grupo eTC"** dá o rótulo pró/anti *por comunidade* que o paper usou:
   permite alinhar as nossas comunidades Louvain com as deles sem re-julgar nada —
   fecha o circuito do eixo A (qual comunidade nossa é a "pró" e qual é a "anti").
3. Os totais das tabelas (broad/sub) permitem reproduzir AV5 **numericamente**
   (não só o ranking).

## Proveniência

- URL de origem: link do Apêndice A do PDF (p. 12); export `?format=xlsx`.
- ⚠ O arquivo contém textos de tweets e handles de autores — mesmo padrão de
  cuidado dos snapshots: **não versionar em repositório público.**
