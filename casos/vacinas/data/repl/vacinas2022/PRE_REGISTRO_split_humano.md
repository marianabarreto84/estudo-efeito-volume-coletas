# Pré-registro — split calibração/validação da rotulagem humana

> Congelado **antes** de escrever a `p6`. Gerado por
> `analise/congela_split_humano.py`.

## Por que existe

O rotulador precisa de material de calibração com a classe neutra
representada — o gabarito do paper não tem (ver `CALIBRAGEM_criterio.md`).
A fonte é a rotulagem da Mariana. Para não validar no mesmo material em
que se calibra, os 100 tweets do estrato baixo são divididos aqui.
**Nenhuma rotulagem adicional foi solicitada** — os 130 tweets já
rotulados bastam.

## Parâmetros

- Seed: `20260727` · fração de calibração: `0.5`
- Estratificado pelo rótulo humano (as três classes nos dois lados)
- `split_humano_baixo.csv` SHA-256: `98fbeb4798a199fe0e2c9dfff0b34cf379564e90ae2b56851e129cfd3c455023`

| partição | n | pro | anti | nenhum |
|---|---:|---:|---:|---:|
| calibração | 50 | 22 | 12 | 16 |
| reservado | 50 | 22 | 12 | 16 |

## Contaminação declarada

- **8 tweets** tiveram o texto exibido durante o
  diagnóstico dos erros da `p4` e da `p5`. Todos foram **forçados para
  a calibração**, de modo que a partição reservada contém apenas
  tweets cujo texto nunca foi lido.
- ⚠️ Ainda assim, as **estatísticas agregadas** dos 100 já eram
  conhecidas (taxa de `nenhum`, matriz de confusão) quando este split
  foi feito. A partição reservada é, portanto, **quase-cega**, não
  cega. É mais fraca que o teste cego do gabarito e deve ser reportada
  com essa ressalva.
- Os **30 tweets do estrato viral** (`CALIBRAGEM_criterio.csv`) ficam
  inteiros reservados: deles só foram vistos o κ e a matriz de
  confusão, nunca um texto individual. Servem como segunda checagem,
  em estrato diferente.

## Critério de aceite (registrado antes de medir)

κ de Cohen ≥ **0,70** contra a rotulagem humana, na partição reservada,
medido **uma única vez**. Mesmo patamar exigido do rotulador contra o
gabarito do paper.

## Aposta pré-registrada

- A `p6` com exemplos neutros deve passar de 0,591 (`p5`) para a faixa
  de 0,75–0,85: a classe `nenhum` deixa de depender só de prosa e passa
  a ter exemplos.
- Não deve chegar perto de 1: parte dos desacordos é irredutível —
  notícia selecionada e fala citada admitem leitura dupla, e alguns dos
  casos examinados pareciam mais defensáveis do lado do modelo.
- No estrato viral (os 30), espera-se **queda** de concordância com o
  gabarito do paper, por construção: adotar a classe neutra afasta o
  rotulador do esquema binário forçado. Isso é o desenho, não falha.