# Fase 1 — Coleta do universo (caso Buntain)

> Gerado em **7/ago/2026**. Fonte: **Arctic Shift** (`arctic-shift.photon-reddit.com`),
> API paginada por `created_utc`. Janela **julho/2013** (unix 1372636800–1375315200).
> Scripts: [`pipeline/probe_volume.py`](../../../pipeline/probe_volume.py) (sonda),
> [`core/arctic.py`](../../../core/arctic.py) (cliente), [`pipeline/collect.py`](../../../pipeline/collect.py)
> (coletor resumível → `snapshot_buntain.sqlite`). Rede confirmada daqui (User-Agent de
> navegador; a API oficial e o Pushshift dão 403).

## Volume do universo (sonda, jul/2013)

Cobertura **01–31/07** confirmada nos 13 subreddits. `~#coment` = soma de `num_comments`
das submissions (estimativa; a coleta real dos comentários arquivados tende a ser
**ligeiramente maior**, pois `num_comments` subconta comentários posteriores).

| Subreddit | #submissions | ~#comentários |
|---|--:|--:|
| IAmA | 4.525 | 298.813 |
| Movies | 17.078 | 267.241 |
| AskMen | 2.404 | 123.672 |
| AskWomen | 3.028 | 101.424 |
| MyLittlePony | 3.914 | 40.019 |
| AskScience | 8.124 | 39.969 |
| PersonalFinance | 2.211 | 33.285 |
| TalesFromTechSupport | 670 | 24.196 |
| WashingtonDC | 904 | 9.660 |
| CompSci | 183 | 2.015 |
| AskScienceDiscussion | 245 | 1.513 |
| MachineLearning | 132 | 1.036 |
| DesMoines | 61 | 584 |
| **TOTAL** | **43.479** | **~943.427** |

**Contraste com o paper:** Buntain coletou **top-100 submissions × ~top-200 comentários**
de cada, num só mês, e ainda cortou usuários com <20 arestas → **279 usuários**. O universo
tem **43,5 mil submissions e ~943 mil comentários** — 3–4 ordens de grandeza acima do
estrato analisado. É o "coletar mais" no seu grau máximo.

## Estado da coleta

- ✅ **Pipeline validado** ponta a ponta nos 4 menores (DesMoines, MachineLearning,
  CompSci, AskScienceDiscussion): 621 submissions + 5.360 comentários; contagens de
  submission batem com a sonda ao número; comentários **um pouco acima** do estimado
  (comentários arquivados > `num_comments` do post).
- ⏳ **Coleta dos 9 grandes rodando** (background) → `snapshot_buntain.sqlite`. Resumível
  (`collect_log`). Sem texto de comentário (RB3 e o grafo são estruturais).

## Próximo passo

Terminada a coleta, rodar [`analise/rb3.py`](../../../analise/rb3.py) — mede a fração de
usuários ativos em **>1** dos 13 subreddits (universo × limiar de atividade), contra os
**~3%** do paper. Predição pré-registrada: **sobe muito**.
