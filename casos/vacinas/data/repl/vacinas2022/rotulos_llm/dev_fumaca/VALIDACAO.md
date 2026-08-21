# Validacao do rotulador — conjunto `dev`, prompt `fumaca`

**REPROVADO** (n = 20)

| Metrica | Valor | Aceite | |
|---|---:|---:|---|
| kappa do stance | 0.714 | 0.70 | passou |
| mediana dos kappas das categorias | 0.599 | 0.60 | reprovou |
| acuracia do stance | 0.850 | — | |

## Por categoria

| # | Categoria | n (gabarito) | n (LLM) | kappa | precisao | recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| 10 | Information sources | 1 | 1 | 1.000 | 1.000 | 1.000 | 1.000 |
| 2 | Children | 8 | 7 | 0.894 | 1.000 | 0.875 | 0.933 |
| 3 | Restrictive policies | 4 | 5 | 0.857 | 0.800 | 1.000 | 0.889 |
| 4 | Disadvantages of vaccines | 10 | 7 | 0.700 | 1.000 | 0.700 | 0.824 |
| 12 | Vaccines type or laboratories | 2 | 1 | 0.643 | 1.000 | 0.500 | 0.667 |
| 6 | International | 4 | 2 | 0.615 | 1.000 | 0.500 | 0.667 |
| 1 | Politics | 6 | 3 | 0.583 | 1.000 | 0.500 | 0.667 |
| 7 | Advantages of vaccines | 3 | 4 | 0.483 | 0.500 | 0.667 | 0.571 |
| 8 | COVID risks | 3 | 5 | 0.385 | 0.400 | 0.667 | 0.500 |
| 11 | Science | 3 | 2 | 0.318 | 0.500 | 0.333 | 0.400 |
| 9 | Misinformation sources | 4 | 2 | 0.231 | 0.500 | 0.250 | 0.333 |
| 5 | Anti-vaccine people | 5 | 0 | 0.000 | — | 0.000 | — |
| 13 | Religion | 0 | 0 | — | — | — | — |
| 14 | Other drugs | 0 | 0 | — | — | — | — |