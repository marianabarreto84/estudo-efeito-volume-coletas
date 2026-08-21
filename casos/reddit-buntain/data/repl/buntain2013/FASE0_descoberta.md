# Fase 0 — Alvo e viabilidade do dado (caso Reddit / Buntain 2014)

> Gerado em **7/ago/2026** por análise documental **offline** (leitura do PDF do alvo +
> rota de coleta herdada do caso #207 descartado). Sem consulta a banco/rede. Números do
> alvo com a seção do paper como proveniência (ver [ARTIGO_BUNTAIN_alvo.md](../../../ARTIGO_BUNTAIN_alvo.md)).

## O que o alvo é (resumo operacional)

- **Buntain & Golbeck 2014** (WWW, 133 cit.). Reconstruiu redes de interação por subreddit
  e identificou o papel *answer-person* por **estrutura de rede**.
- Coleta = **estrato de topo por limite de API**: top-100 submissions de **julho/2013**,
  top-200 comentários cada, em **13 subreddits**, com **corte de <20 arestas** → **279
  usuários**.
- Afirmação-alvo central (**RB3**): só **7 de 279 (~3%)** participam de >1 comunidade.

## O que "coletar mais" exige (o universo-alvo)

O universo *on-theme* = **todas** as submissions e **todos** os comentários dos **mesmos
13 subreddits**, sem o corte de grau — em julho/2013 (fiel) e, para o eixo temporal, numa
janela maior. O tema (os 13 subreddits) é preservado; o n=279 é um subconjunto por `score`
+ limiar de grau do universo que vamos materializar.

**Tamanho esperado (a confirmar na Fase 1):** 13 subreddits × 1 mês, incluindo gigantes
como IAmA/AskMen/AskScience → provável **centenas de milhares a poucos milhões** de
comentários. Maior que o #207, mas ainda tratável em SQLite/Parquet local. Janela maior
(E4) escala proporcional.

## Viabilidade — rota de coleta ✅

**Dados de julho/2013 estão plenamente disponíveis.** 2013 está no **coração** da cobertura
dos dumps históricos do Reddit (Pushshift original / Academic Torrents / **Arctic Shift**).
Rota herdada do #207 (mesmo raciocínio, ver [tombstone](../../../../reddit-companhia-ia/README.md)):

| Rota | Estado |
|---|---|
| **Arctic Shift** (`arctic-shift.photon-reddit.com`) | ✅ **rota escolhida** — dumps por subreddit/janela, com submissions **e** comentários. 2013 coberto |
| **Academic Torrents** (dumps mensais RS_/RC_2013-07) | fallback robusto; o arquivo mensal de jul/2013 é filtrável offline pelos 13 subreddits |
| **API oficial + PRAW** (o que o paper usou) | ❌ reproduz a sub-coleta (teto ~1.000); serve no máximo para o ponto n=279 |
| **Crawler do autor** (`github.com/cbuntain/redditResponseExtractor`) | só re-executa a coleta capada; útil como referência de método, não p/ o universo |

**Gabarito do paper:** os **279 usuários rotulados** (answer × non-answer) **não constam
publicados** (o repo do autor é só o crawler). Consequências:
- **RB3 não precisa do gabarito** — é contagem estrutural, reconstruível 100% da coleta.
- **RB1/RB2 precisam de rótulos** — reconstruir por rotulagem própria (fluxo do vacinas) se
  formos testá-los. Ver [REPLICACAO §5](../../../REPLICACAO_CASO_BUNTAIN.md).

## Bloqueios e o que destrava (tudo offline, sem VPN)

1. ✅ **Rota** — Arctic Shift (2013 coberto). 2. ✅ **Alvo** — publicado e influente (133
cit.). 3. ⏳ **Só falta rodar** a Fase 1 (baixar os 13 subreddits de jul/2013 e congelar o
snapshot). Nenhum depende de VPN.

## Predições pré-registradas

(Detalhe em [REPLICACAO §4](../../../REPLICACAO_CASO_BUNTAIN.md).)

- **Muda (forte):** RB3 — os **~3% sobem muito** ao coletar todos os posts/comentários sem
  o corte de grau. Direção: a sub-coleta esconde atividade cruzada por construção.
- **Confirma:** RB1 — o papel answer-person existe.
- **Incerto:** RB2 — a assinatura estrutural pode borrar sem o corte de comentários.
- **Não convergiu:** n=279 é minúsculo para RB3.
