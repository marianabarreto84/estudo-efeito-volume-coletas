# Pre-registro do split dev/teste — eixo B (rotulador de conteudo)

> **Congelado ANTES de qualquer chamada a API.** Este arquivo e o
> compromisso: o conjunto de teste so foi olhado depois que o prompt
> do rotulador ficou congelado. Refazer o split depois disso invalida
> o kappa reportado.

## Parametros (reprodutiveis)

- Gabarito: `suplementar_rotulos.xlsx` / aba `Spreadsheet 1` (1525 tweets virais >500 RT)
- Codebook: `codebook_v1.json` (14 categorias amplas)
- Seed: `20260726` | fracao dev: `0.3333`
- Estratificacao: stance x categoria mais rara presente (33 estratos)
- Estratos de tamanho 1 vao inteiros para o TESTE

## Resultado

- **dev = 506** (ajuste de prompt permitido)
- **teste = 1019** (cego ate o rotulador congelar)
- `split_dev_teste.csv` SHA-256: `4fd17e9d6d8d5a0a643c525a003c84e2b6044b544fca58ca7b5b0aab7d3c93f3`

| Stance | dev | teste |
|---|---:|---:|
| pro | 246 | 492 |
| anti | 260 | 524 |
| nenhum | 0 | 3 |

### Cobertura por categoria (nenhuma categoria fica fora de um dos lados)

| # | Categoria | Total | dev | teste |
|---|---|---:|---:|---:|
| 1 | Politics | 719 | 245 | 474 |
| 2 | Children | 592 | 194 | 398 |
| 3 | Restrictive policies | 531 | 168 | 363 |
| 4 | Disadvantages of vaccines | 378 | 126 | 252 |
| 5 | Anti-vaccine people | 375 | 129 | 246 |
| 6 | International | 253 | 83 | 170 |
| 7 | Advantages of vaccines | 242 | 77 | 165 |
| 8 | COVID risks | 241 | 75 | 166 |
| 9 | Misinformation sources | 201 | 71 | 130 |
| 10 | Information sources | 179 | 59 | 120 |
| 11 | Science | 94 | 31 | 63 |
| 12 | Vaccines type or laboratories | 86 | 28 | 58 |
| 13 | Religion | 46 | 15 | 31 |
| 14 | Other drugs | 32 | 10 | 22 |

## Criterio de aceite (registrado antes de rodar)

- kappa de Cohen do **stance** >= **0.70**
- **mediana** dos kappas das 14 categorias >= **0.60**
- Ambos medidos **no teste cego**, uma unica vez.
- Se reprovar: nao se ajusta o prompt contra o teste. Ou se volta ao dev,
  ou se troca de modelo (Sonnet), ou se reporta a reprovacao e o eixo B
  fica limitado ao estrato ja rotulado a mao pelo paper.

## Aposta pre-registrada (principio da rastreabilidade do projeto)

- Stance passa folgado (tarefa binaria, sinal forte no texto).
- A mediana das categorias passa, mas as categorias raras
  (Religion n=46, Other drugs n=32, Vaccines type/labs n=86) ficam
  abaixo do corte individualmente — e esse e um achado a favor da tese:
  analise composta exige mais dados do que parece.
- Categorias agregadas amplas (Politics n=719, Children n=592) devem ter
  os melhores kappas.

> Reportar honestamente se a aposta falhar.