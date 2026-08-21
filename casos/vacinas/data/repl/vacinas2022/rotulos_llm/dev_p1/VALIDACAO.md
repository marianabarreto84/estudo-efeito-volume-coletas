# Validacao do rotulador — conjunto `dev`, prompt `p1`

**REPROVADO** (n = 506)

| Metrica | Valor | Aceite | |
|---|---:|---:|---|
| kappa do stance | 0.714 | 0.70 | passou |
| mediana dos kappas das categorias | 0.599 | 0.60 | reprovou |
| acuracia do stance | 0.850 | — | |

## Por categoria

| # | Categoria | n (gabarito) | n (LLM) | kappa | precisao | recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| 2 | Children | 194 | 178 | 0.907 | 0.983 | 0.902 | 0.941 |
| 12 | Vaccines type or laboratories | 28 | 33 | 0.773 | 0.727 | 0.857 | 0.787 |
| 4 | Disadvantages of vaccines | 126 | 103 | 0.769 | 0.913 | 0.746 | 0.821 |
| 3 | Restrictive policies | 168 | 172 | 0.717 | 0.802 | 0.821 | 0.812 |
| 6 | International | 83 | 47 | 0.668 | 0.979 | 0.554 | 0.708 |
| 14 | Other drugs | 10 | 6 | 0.619 | 0.833 | 0.500 | 0.625 |
| 8 | COVID risks | 75 | 53 | 0.608 | 0.792 | 0.560 | 0.656 |
| 1 | Politics | 245 | 178 | 0.589 | 0.899 | 0.653 | 0.757 |
| 13 | Religion | 15 | 6 | 0.564 | 1.000 | 0.400 | 0.571 |
| 5 | Anti-vaccine people | 129 | 55 | 0.423 | 0.855 | 0.364 | 0.511 |
| 10 | Information sources | 59 | 20 | 0.422 | 0.900 | 0.305 | 0.456 |
| 7 | Advantages of vaccines | 77 | 80 | 0.344 | 0.438 | 0.455 | 0.446 |
| 11 | Science | 31 | 27 | 0.342 | 0.407 | 0.355 | 0.379 |
| 9 | Misinformation sources | 71 | 42 | 0.259 | 0.452 | 0.268 | 0.336 |