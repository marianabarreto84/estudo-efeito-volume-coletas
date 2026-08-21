# Validacao do rotulador — conjunto `dev`, prompt `p2`

**APROVADO** (n = 506)

| Metrica | Valor | Aceite | |
|---|---:|---:|---|
| kappa do stance | 0.738 | 0.70 | passou |
| mediana dos kappas das categorias | 0.602 | 0.60 | passou |
| acuracia do stance | 0.866 | — | |

## Por categoria

| # | Categoria | n (gabarito) | n (LLM) | kappa | precisao | recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| 2 | Children | 194 | 176 | 0.889 | 0.977 | 0.887 | 0.930 |
| 4 | Disadvantages of vaccines | 126 | 105 | 0.759 | 0.895 | 0.746 | 0.814 |
| 3 | Restrictive policies | 168 | 178 | 0.719 | 0.792 | 0.839 | 0.815 |
| 12 | Vaccines type or laboratories | 28 | 40 | 0.654 | 0.575 | 0.821 | 0.676 |
| 8 | COVID risks | 75 | 52 | 0.650 | 0.846 | 0.587 | 0.693 |
| 6 | International | 83 | 44 | 0.636 | 0.977 | 0.518 | 0.677 |
| 10 | Information sources | 59 | 37 | 0.611 | 0.838 | 0.525 | 0.646 |
| 1 | Politics | 245 | 177 | 0.593 | 0.904 | 0.653 | 0.758 |
| 11 | Science | 31 | 23 | 0.531 | 0.652 | 0.484 | 0.556 |
| 14 | Other drugs | 10 | 5 | 0.527 | 0.800 | 0.400 | 0.533 |
| 5 | Anti-vaccine people | 129 | 95 | 0.510 | 0.726 | 0.535 | 0.616 |
| 13 | Religion | 15 | 5 | 0.492 | 1.000 | 0.333 | 0.500 |
| 9 | Misinformation sources | 71 | 42 | 0.378 | 0.595 | 0.352 | 0.442 |
| 7 | Advantages of vaccines | 77 | 80 | 0.344 | 0.438 | 0.455 | 0.446 |