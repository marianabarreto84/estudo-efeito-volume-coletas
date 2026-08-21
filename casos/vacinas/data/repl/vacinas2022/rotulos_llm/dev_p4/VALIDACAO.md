# Validacao do rotulador — conjunto `dev`, prompt `p4`

**APROVADO** (n = 506)

| Metrica | Valor | Aceite | |
|---|---:|---:|---|
| kappa do stance | 0.755 | 0.70 | passou |
| mediana dos kappas das categorias | 0.646 | 0.60 | passou |
| acuracia do stance | 0.874 | — | |

## Por categoria

| # | Categoria | n (gabarito) | n (LLM) | kappa | precisao | recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| 14 | Other drugs | 10 | 8 | 0.887 | 1.000 | 0.800 | 0.889 |
| 2 | Children | 194 | 178 | 0.881 | 0.966 | 0.887 | 0.925 |
| 4 | Disadvantages of vaccines | 126 | 96 | 0.759 | 0.938 | 0.714 | 0.811 |
| 3 | Restrictive policies | 168 | 160 | 0.729 | 0.838 | 0.798 | 0.817 |
| 6 | International | 83 | 52 | 0.703 | 0.962 | 0.602 | 0.741 |
| 1 | Politics | 245 | 213 | 0.682 | 0.887 | 0.771 | 0.825 |
| 12 | Vaccines type or laboratories | 28 | 43 | 0.653 | 0.558 | 0.857 | 0.676 |
| 8 | COVID risks | 75 | 75 | 0.640 | 0.693 | 0.693 | 0.693 |
| 13 | Religion | 15 | 6 | 0.564 | 1.000 | 0.400 | 0.571 |
| 5 | Anti-vaccine people | 129 | 104 | 0.528 | 0.712 | 0.574 | 0.635 |
| 10 | Information sources | 59 | 25 | 0.514 | 0.920 | 0.390 | 0.548 |
| 9 | Misinformation sources | 71 | 36 | 0.370 | 0.639 | 0.324 | 0.430 |
| 11 | Science | 31 | 40 | 0.349 | 0.350 | 0.452 | 0.394 |
| 7 | Advantages of vaccines | 77 | 59 | 0.271 | 0.424 | 0.325 | 0.368 |