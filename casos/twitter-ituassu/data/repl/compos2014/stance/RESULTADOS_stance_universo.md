# *Stance* no universo — estimativa corrigida pela matriz de confusão

> Desenho registrado em `PRE_REGISTRO_stance.md` §6, **antes** de sortear e de
> rotular. O rotulador **continua reprovado** no critério do §4 (κ 0,604 < 0,70);
> aqui ele é usado como instrumento de **estimativa agregada**, com o viés
> corrigido, e não como instrumento de rótulo individual.

## 1. Amostra

| item | valor |
|---|---|
| população | 32.193 tweets (19–25/out/2014) |
| amostra | 5.000 itens em 2.762 textos distintos |
| `sha256(ids)[:12]` | `9cde554b9b6e` |

## 2. Proporções

| classe | bruto (rotulador) | **corrigido** | IC95% |
|---|---:|---:|---:|
| EA | 25.5% | **17.2%** | [9.6%; 23.1%] |
| ED | 14.6% | **17.0%** | [8.5%; 31.9%] |
| NDA | 59.9% | **65.8%** | [52.5%; 75.1%] |

## 3. Curva `A(volume)`

Estimativa corrigida em subamostras crescentes, 200 sorteios por ponto.

| n | EA | ED | NDA |
|---:|---:|---:|---:|
| 100 | 17.5% | 16.8% | 65.8% |
| 200 | 16.8% | 17.2% | 66.0% |
| 500 | 17.1% | 16.9% | 66.0% |
| 1.000 | 17.0% | 17.1% | 65.9% |
| 2.000 | 17.3% | 16.9% | 65.8% |
| 5.000 | 17.2% | 17.0% | 65.8% |

**Convergência** (IC95 inteiro a menos de 3 p.p. do valor em n=5000):

- EA: n = 2.000
- ED: n = 2.000
- NDA: n = 2.000

## 4. A afirmação do artigo

O artigo de 2015 reporta, entre os 666 cidadãos: ED 284 (42,6%) contra EA 226
(33,9%) — razão EA/ED = **0.80**, isto é, **ED > EA**.

Aqui a razão EA/ED corrigida é **1.01** (IC95% [0.36; 2.35]).
