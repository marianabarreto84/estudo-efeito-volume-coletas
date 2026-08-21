# Validacao do rotulador — conjunto `dev`, prompt `p3`

**APROVADO** (n = 506)

| Metrica | Valor | Aceite | |
|---|---:|---:|---|
| kappa do stance | 0.735 | 0.70 | passou |
| mediana dos kappas das categorias | 0.621 | 0.60 | passou |
| acuracia do stance | 0.864 | — | |

## Por categoria

| # | Categoria | n (gabarito) | n (LLM) | kappa | precisao | recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| 14 | Other drugs | 10 | 9 | 0.839 | 0.889 | 0.800 | 0.842 |
| 4 | Disadvantages of vaccines | 126 | 101 | 0.791 | 0.941 | 0.754 | 0.837 |
| 2 | Children | 194 | 149 | 0.786 | 0.987 | 0.758 | 0.857 |
| 3 | Restrictive policies | 168 | 134 | 0.690 | 0.881 | 0.702 | 0.781 |
| 6 | International | 83 | 54 | 0.690 | 0.926 | 0.602 | 0.730 |
| 12 | Vaccines type or laboratories | 28 | 43 | 0.683 | 0.581 | 0.893 | 0.704 |
| 1 | Politics | 245 | 188 | 0.677 | 0.936 | 0.718 | 0.813 |
| 13 | Religion | 15 | 6 | 0.564 | 1.000 | 0.400 | 0.571 |
| 8 | COVID risks | 75 | 30 | 0.511 | 0.967 | 0.387 | 0.552 |
| 10 | Information sources | 59 | 26 | 0.506 | 0.885 | 0.390 | 0.541 |
| 5 | Anti-vaccine people | 129 | 71 | 0.487 | 0.817 | 0.450 | 0.580 |
| 11 | Science | 31 | 13 | 0.434 | 0.769 | 0.323 | 0.455 |
| 7 | Advantages of vaccines | 77 | 52 | 0.373 | 0.558 | 0.377 | 0.450 |
| 9 | Misinformation sources | 71 | 24 | 0.332 | 0.750 | 0.254 | 0.379 |