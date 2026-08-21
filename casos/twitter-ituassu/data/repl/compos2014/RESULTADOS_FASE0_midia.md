# Fase 0 — Resultados do eixo MÍDIA (MV/MH)

> Replicação Ituassu & Lifschitz (2015). Gerado por `analisa_midia.py` sobre o
> snapshot congelado `snapshot_hashtag.sqlite` + cache `expand_cache.sqlite`.
> Este eixo é 100% determinístico (não depende de stance EA/ED).

## Método
- Universo: `A_mais_hashtag` = hashtag normalizada (minúscula+sem acento) == `eleicoes2014`.
- Amostra `A_paper`: primeiros 100 tweets a partir da hora de pico (BRT) por dia,
  19–25/out. Pico: 21h dom/seg/ter, 14h qua (ver ressalva), 21h qui, 16h sex, 13h sáb.
- Mídia: classe do **1º link** (regra do paper), dicionário MV/MH em `midia_dominios.py`.
  Links encurtados expandidos via HTTP (`expandir_links.py`); dead links (goo.gl etc.)
  ficam `nao_resolvido`.

## Cobertura de classificação (universo, pós-expansão)
```
total: 140909
  MV               66370   47.1%
  NDA              37921   26.9%
  nao_resolvido    18480   13.1%
  MH               13233    9.4%
  indefinido        4905    3.5%
cobertura (classe definida): 86.9%  |  nao_resolvido: 13.1%
```

## A_paper reconstruída (amostra 100/dia)
| dia | n | MV | MH | NDA | n/res | ind | RTMV% | MV% | MH% |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 2014-10-19 | 100 | 84 | 3 | 4 | 8 | 1 | 77.0% | 84.0% | 3.0% |
| 2014-10-20 | 100 | 59 | 16 | 13 | 5 | 7 | 52.0% | 59.0% | 16.0% |
| 2014-10-21 | 100 | 54 | 11 | 11 | 17 | 7 | 48.0% | 54.0% | 11.0% |
| 2014-10-22 | 100 | 55 | 7 | 16 | 9 | 13 | 45.0% | 55.0% | 7.0% |
| 2014-10-23 | 100 | 62 | 13 | 6 | 12 | 7 | 53.0% | 62.0% | 13.0% |
| 2014-10-24 | 100 | 51 | 11 | 19 | 11 | 8 | 47.0% | 51.0% | 11.0% |
| 2014-10-25 | 100 | 19 | 10 | 42 | 25 | 4 | 16.0% | 19.0% | 10.0% |
| **TOTAL** | **700** | 384 | 71 | 111 | 87 | 47 | **48.3%** | **54.9%** | 10.1% |

## Universo on-hashtag 19–25/out
| dia | n | MV | MH | NDA | n/res | ind | RTMV% | MV% | MH% |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 2014-10-19 | 3063 | 1216 | 203 | 1303 | 270 | 71 | 34.1% | 39.7% | 6.6% |
| 2014-10-20 | 2992 | 1643 | 357 | 516 | 276 | 200 | 43.2% | 54.9% | 11.9% |
| 2014-10-21 | 3257 | 1633 | 498 | 522 | 435 | 169 | 40.5% | 50.1% | 15.3% |
| 2014-10-22 | 2908 | 1531 | 286 | 590 | 321 | 180 | 42.2% | 52.6% | 9.8% |
| 2014-10-23 | 6106 | 3601 | 615 | 878 | 765 | 247 | 51.2% | 59.0% | 10.1% |
| 2014-10-24 | 7246 | 2165 | 709 | 3539 | 581 | 252 | 24.9% | 29.9% | 9.8% |
| 2014-10-25 | 6621 | 2165 | 697 | 2574 | 973 | 212 | 27.3% | 32.7% | 10.5% |
| **TOTAL** | **32193** | 13954 | 3365 | 9922 | 3621 | 1331 | **36.1%** | **43.3%** | 10.5% |

## Leitura — H1 (predomínio de retweet de mídia vertical, RTMV > 50%)
- **Amostra (100/dia):** RTMV agregado **48.3%**
  (base resolvida 55.1%) — **grosso modo se mantém** (~50%),
  compatível com o paper.
- **Universo completo:** RTMV agregado **36.1%**
  (base resolvida 40.7%) — **NÃO se sustenta em escala**.
- **Achado central (efeito-de-volume):** a amostra de 100/dia nos horários de pico
  **superestima** a dominância de RT de mídia vertical. No volume cheio, o conteúdo
  sem link (NDA — sobretudo 24–25/out, dia da votação) dilui a proporção de MV.

## Ressalvas
- 3621 tweets no universo (11.2%) têm
  1º link não-resolvido (encurtador morto). Mesmo no cenário otimista (todos MV), o
  RTMV do universo não alcançaria os >50% do paper.
- Quarta 22/out: hora de pico ambígua (texto=14h; nota de rodapé=21h). Usado 14h.
- H2/H3 e temas dependem da classificação de stance (Fase 0.5, adiada).
