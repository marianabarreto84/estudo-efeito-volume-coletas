# Validação do rotulador de *stance* — teste cego (210)

> Medida **única**, sobre o teste cego, com o prompt congelado.
> Critérios escritos em `PRE_REGISTRO_stance.md` §4, **antes** de medir.

## 1. Critérios de aceite

| critério | medido | mínimo | passa? |
|---|---:|---:|:--:|
| κ de Cohen (stance, 3 classes) | 0.604 | 0.70 | ❌ |
| acurácia do portão `cidadao` | 0.781 | 0.90 | ❌ |

## 2. κ do stance nos quatro recortes

Reportados **em conjunto**, como o pré-registro exige.

| recorte | n | κ | acurácia |
|---|---:|---:|---:|
| todos | 210 | 0.604 | 0.805 |
| sem duplicatas | 179 | 0.608 | 0.810 |
| confianca >= 2 | 144 | 0.701 | 0.882 |
| confianca >= 2, sem dup. | 120 | 0.718 | 0.892 |

## 3. Portão `cidadao`

| base | n | acurácia | κ |
|---|---:|---:|---:|
| todos os itens | 210 | 0.781 | 0.354 |
| excluindo os `?` do gabarito | 189 | 0.868 | — |

⚠ O pré-registro §4.2 pedia a acurácia em **duas bases** — todos os itens e
só os decidíveis pelo CSV congelado —, porque o codebook permite à anotadora
abrir o perfil vivo e o rotulador não tem esse acesso. **A segunda base não é
computável**: a rotulagem não registrou em quais itens o perfil foi consultado.
A linha dos `?` acima é o que mais se aproxima, e não substitui. Fica como
limitação declarada, e como lição de instrumento: a consulta deveria ter sido
marcada em `notas`.

## 4. Matriz de confusão (linhas = gabarito, colunas = rotulador)

| | EA | ED | NDA |
|---|---|---|---|
| **EA** | 36 | 1 | 3 |
| **ED** | 3 | 11 | 6 |
| **NDA** | 17 | 11 | 122 |

Divergências: **41** de 210. Divergências de **polo** (EA lido como ED, ou o contrário): **4**.

## 5. Distribuições

| classe | gabarito | rotulador |
|---|---:|---:|
| EA | 40 | 56 |
| ED | 20 | 23 |
| NDA | 150 | 131 |

## 6. Teto da tarefa

O reteste intracodificador (40 itens, ≥ 7 dias depois) **ainda não foi feito**.
Sem ele não há teto medido, e o κ acima não tem contra o que ser relativizado.
No caso vacinas o teto foi 0,746.
