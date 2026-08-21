# Validacao do rotulador — conjunto `teste`, prompt `p4`

**APROVADO** (n = 1018)

| Metrica | Valor | Aceite | |
|---|---:|---:|---|
| kappa do stance | 0.759 | 0.70 | passou |
| mediana dos kappas das categorias | 0.650 | 0.60 | passou |
| acuracia do stance | 0.876 | — | |

## Por categoria

| # | Categoria | n (gabarito) | n (LLM) | kappa | precisao | recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| 2 | Children | 398 | 354 | 0.874 | 0.977 | 0.869 | 0.920 |
| 14 | Other drugs | 22 | 19 | 0.826 | 0.895 | 0.773 | 0.829 |
| 3 | Restrictive policies | 362 | 335 | 0.758 | 0.875 | 0.809 | 0.841 |
| 6 | International | 170 | 116 | 0.757 | 0.974 | 0.665 | 0.790 |
| 12 | Vaccines type or laboratories | 58 | 81 | 0.730 | 0.642 | 0.897 | 0.748 |
| 4 | Disadvantages of vaccines | 252 | 191 | 0.704 | 0.890 | 0.675 | 0.767 |
| 1 | Politics | 473 | 420 | 0.664 | 0.862 | 0.765 | 0.811 |
| 8 | COVID risks | 166 | 165 | 0.636 | 0.697 | 0.693 | 0.695 |
| 9 | Misinformation sources | 130 | 79 | 0.518 | 0.747 | 0.454 | 0.565 |
| 5 | Anti-vaccine people | 245 | 191 | 0.506 | 0.696 | 0.543 | 0.610 |
| 13 | Religion | 31 | 12 | 0.503 | 0.917 | 0.355 | 0.512 |
| 10 | Information sources | 119 | 51 | 0.469 | 0.843 | 0.361 | 0.506 |
| 11 | Science | 63 | 103 | 0.400 | 0.359 | 0.587 | 0.446 |
| 7 | Advantages of vaccines | 165 | 135 | 0.376 | 0.519 | 0.424 | 0.467 |

> Teste cego: medido uma unica vez, com o prompt ja congelado.
> Ajustar o prompt a partir daqui invalida este numero.