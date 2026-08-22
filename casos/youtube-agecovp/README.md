# Caso de replicação · YouTube · Ghenai et al. (2025) — AGECovP

**Leia primeiro:** [data/repl/agecovp2020/FASE0_descoberta.md](data/repl/agecovp2020/FASE0_descoberta.md).

Célula **YouTube** da `tab:casos`. Alvo: **AGECovP** (*EPJ Data Science* 14:65, 2025) —
discurso sobre idosos na pandemia, com **modelagem de tópicos + sentimento + toxicidade**.
Nasceu em **18/ago/2026**, e é o caso mais rápido do lineup a sair do zero: da escolha do
alvo à coleta rodando, na mesma sessão.

## Por que este caso existe

Os outros dois candidatos de rede nova **travaram na coleta**, não na análise: o Meta Ads
espera conta com documento verificado e o TikTok teve a credencial do eTC revogada. O
YouTube foi o único onde a rota estava viva — **chave de API em 5 minutos, grátis, sem
verificação** — e onde o dado **persiste** (vídeos de 2020 seguem buscáveis hoje).

## Estado (21/ago/2026) — **caso fechado no eixo do filtro**

- ✅ **Fase 0 fechada** — artigo lido, funil extraído, termos e lista de filtro transcritos,
  alvos-teste e predições pré-registrados.
- ✅ **Gabarito publicado, baixado e conferido** — [Zenodo 15800324](https://zenodo.org/records/15800324):
  **3.782 vídeos, 2.243 canais, 69.425 comentários, 4.389 comentários rotulados** para
  ageísmo (810 = 18,5% positivos). Tudo bate com o artigo. Vem com sentimento (VADER e
  TextBlob) e toxicidade já computados — as análises do artigo são reproduzíveis **sem
  gastar cota**.
- ✅ **Fase 1 COMPLETA** (21/ago/2026) — **85/85 combinações, 3.446 vídeos**, dos quais
  1.299 (37,7%) passam o filtro. Mais os **2.165 canais** do instantâneo buscados pela
  própria API (`pipeline/coleta_canais.py`, 44 unidades, **cobertura de 100%**).
- ✅ **Fase 2 fechada** — o ponto original reproduz; ver
  [FASE2](data/repl/agecovp2020/FASE2_ponto_original.md).
- ✅ **Fase 3 fechada** — ver [FASE3 §7](data/repl/agecovp2020/FASE3_efeito_filtro.md).
  **A predição P1 foi refutada** e o achado do caso mudou de lugar (abaixo).
- ⏳ **Só falta** o eixo dos comentários (AG1/AG2 sobre a nossa coleta): custa ~1 unidade
  por 100 comentários, cabe numa cota diária. Não bloqueia a linha 15 da tabela mestre,
  que já fechou pelo eixo do filtro.

## ★ O resultado (21/ago/2026)

**A predição falhou, e o achado real é maior.** Apostou-se que o filtro de palavra-chave
removeria conteúdo de usuário comum, institucionalizando o corpus. Medido sobre a coleta
completa e com cobertura total de canais, o filtro faz o **contrário**: UGC 39,0% entre os
aprovados × 32,7% entre os descartados, Δ **−6,4 p.p.** (IC95% [−11,4; −1,4]), sinal
robusto a cinco limiares e confirmado sem limiar nenhum pela mediana de inscritos
(28 mil × 61,5 mil).

**Mas o efeito de seleção existe e é enorme — só não é do filtro.** Entre os vídeos no
tema que as mesmas buscas devolvem, os canais que terminaram no corpus publicado são
23,5% UGC contra **61,7%** dos que ficaram de fora: Δ **+38,3 p.p.** (IC95%
[+33,5; +43,0]), mediana de inscritos **199.000 × 1.070**. A conclusão do capítulo — a
explicação do artigo é parcialmente circular — **sai reforçada**; o que cai é a
atribuição do mecanismo. O passo do funil responsável **não foi isolado**, e o maior
suspeito (o ramo dos sugeridos, 99% de descarte) é irreproduzível desde ago/2023.

## O caso em uma frase

O artigo aplica um filtro de regex — *a palavra-chave da busca tem de reaparecer no título
ou na descrição* — que descarta **52% dos resultados da busca** e **99% dos vídeos
sugeridos** (104.172 → 1.025). É um critério de **forma**, não de assunto: quem escreve
título com palavra-chave é veículo de imprensa, não usuário comum. A pergunta do caso é se
as conclusões sobrevivem a soltar esse filtro.

**Decisão de desenho:** coletamos **tudo** e gravamos o filtro como **coluna**
(`passa_filtro`), em vez de descartar. O mesmo snapshot serve aos dois lados da comparação.

## Alvos-teste

| # | afirmação | família | predição |
|---|---|---|---|
| **AG1** | sentimento dos comentários (TextBlob 39/39/22) | descritiva | **muda** (mais negativo) |
| **AG2** | comentários mais negativos que vídeos | **comparativa** | **não muda** |
| **AG3** | **UGC < 7%** — conteúdo dirigido por imprensa | descritiva | **muda muito** (mais que dobra) |
| **AG4** | categorias de canal (Society 56,4%) | descritiva | muda (Society cai) |

Se AG1/AG3 mudarem e AG2 sobreviver, o caso converge com o padrão dos anteriores —
comparativo robusto, descritivo frágil — numa **quarta rede**.

## Duas ressalvas declaradas

1. **Tração fraca:** 0 citações (publicado em ago/2025). Nenhum alvo de YouTube do corpus
   tem tração; o critério que resta é o **veículo** (periódico revisado). Dito no capítulo.
2. **Um ramo do funil é irreproduzível:** o parâmetro `relatedToVideoId` foi **removido da
   API em ago/2023**, então os 104.172 vídeos sugeridos não são recoletáveis. Testa-se o
   mesmo filtro no ramo da **busca** (onde descarta 52%). Isso é, por si, um achado sobre
   perecibilidade: um trabalho de 2025 já tem etapa de coleta irreproduzível.

## Estrutura

```
youtube-agecovp/
├── README.md
├── core/youtube_api.py         <- cliente da Data API v3 com livro-caixa de cota
├── core/regras.py              <- as 2 regras que o artigo não publica (`no_tema`, `eh_ugc`)
├── pipeline/coleta.py          <- Fase 1: coleta sem filtrar, marca `passa_filtro`
├── pipeline/coleta_canais.py   <- Fase 1b: metadados de TODOS os canais (tira o viés de base)
├── analise/fase2_ponto_original.py  <- Fase 2, sobre o gabarito (sem cota)
├── analise/fase3_efeito_filtro.py   <- Fase 3: quanto o filtro descarta
├── analise/fase3_no_tema.py         <- Fase 3 restrita ao tema (⚠ base do gabarito; superada)
├── analise/fase3_ugc_completo.py    <- Fase 3 **definitiva**: P1 + o funil inteiro, com IC
├── analise/fase3_comentarios.py     <- Fase 3, eixo dos comentários: AG1/AG2 e as predições P2/P3
├── requirements.txt            <- `requests`, `textblob`, `vaderSentiment` (o resto é padrão)
└── data/repl/agecovp2020/
    ├── FASE0_descoberta.md     <- alvo, funil, gabarito, alvos-teste, predições
    ├── FASE2_ponto_original.md <- o que reproduz do artigo
    ├── FASE3_efeito_filtro.md  <- o efeito do filtro; **§7 é o resultado canônico**
    ├── DECISOES_regras.md      <- por que `no_tema` e `eh_ugc` são assim
    ├── termos_agecovp.json     <- os 85 pares de busca + as 88 palavras do filtro
    ├── gabarito_zenodo/        <- os 4 CSVs dos autores, conferidos
    └── snapshot_agecovp.sqlite <- nossa coleta: 3.446 vídeos + 2.165 canais
```

## Cota

10.000 unidades/dia, grátis. `search.list` custa **100** por chamada; comentários custam
**1** por 100. O cliente mantém livro-caixa persistente (`data/cota_youtube.json`) e
recusa a chamada que estouraria o teto — mesmo espírito do teto de gasto de LLM do caso
vacinas. **A cota zera à meia-noite do Pacífico**, 4h–5h no Brasil.
