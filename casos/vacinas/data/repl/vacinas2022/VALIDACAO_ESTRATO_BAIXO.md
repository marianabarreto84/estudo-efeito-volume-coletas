# Validação do rotulador no estrato BAIXO (10 < RT ≤ 100)

**REPROVADO** — n = 100 tweets rotulados à mão pela Mariana,
cegos aos rótulos do modelo.

> ## ⚠️ RETRATAÇÃO — a leitura abaixo foi derrubada
>
> O teste de calibragem (`CALIBRAGEM_criterio.md`) mostrou que a
> Mariana marca `nenhum` em **33% dos tweets VIRAIS** — praticamente a
> mesma taxa dos 32% que marcou no estrato baixo. Os neutros não são
> propriedade do estrato: são propriedade do critério dela, que difere
> do dos codificadores do paper (κ 0,350 entre os dois, no mesmo
> material).
>
> Portanto o κ medido aqui **não mede** transferência do instrumento
> entre estratos — mede distância entre dois padrões humanos de
> codificação. A conclusão original deste documento ("a sub-coleta
> contaminou o instrumento") era uma sobre-interpretação e está
> retirada. Ver `CALIBRAGEM_criterio.md` para o que ficou no lugar.

> Este é o teste que decide se o achado principal da Fase 3 — a
> inversão do stance ao descer o limiar — se sustenta. O κ de 0,759
> do teste cego foi medido só em >500 RT, e a conclusão depende do
> estrato baixo.

| Métrica | Valor | Aceite | |
|---|---:|---:|---|
| κ do stance | 0.473 | 0.70 | reprovou |
| mediana dos κ das categorias | — | 0.60 | não medido (rotulagem stance-only) |
| acurácia do stance | 0.660 | — | |

### Comparação com o estrato viral

| | >500 RT (teste cego) | 10–100 RT (aqui) |
|---|---:|---:|
| κ stance | 0,759 | 0.473 |
| mediana κ categorias | 0,650 | — |
| n | 1.018 | 100 |

## Distribuição do stance — humano × modelo

| | humano | modelo |
|---|---:|---:|
| pro | 44 (44%) | 56 (56%) |
| anti | 24 (24%) | 41 (41%) |
| nenhum | 32 (32%) | 3 (3%) |

### Matriz de confusão (linha = humano, coluna = modelo)

| humano ＼ modelo | pro | anti | nenhum |
|---|---:|---:|---:|
| **pro** | 40 | 3 | 1 |
| **anti** | 0 | 24 | 0 |
| **nenhum** | 16 | 14 | 2 |

## Onde o rotulador quebra — e onde não quebra

**Subtarefa `pro` × `anti`** (só os 68 tweets a que a humana
atribuiu lado):

- κ = **0.877** · acurácia = 0.941
- É **melhor** que no estrato viral (κ 0,759). Distinguir os polos o
  rotulador faz bem aqui.

**Toda a falha está na classe `nenhum`.** Dos 32 tweets que a humana
considerou sem posição, o modelo forçou 16 para `pro` e 14 para `anti`;
só 2 foram reconhecidos como sem posição.

### A causa é o prompt, e é rastreável

O prompt congelado (`p4`) instrui, literalmente:

> *“Estes são tweets **VIRAIS** de um debate polarizado: quase todos
> tomam partido (…). Não use `nenhum` como saída para o caso difícil.”*

Essa instrução nasceu da calibração no estrato viral, onde o gabarito
humano tem **3 neutros em 1.525** (0,2%). No estrato baixo os neutros
são **32%**. O prompt foi
endurecido contra detectar exatamente o que passou a existir.

> **Este é o achado metodológico do caso.** A sub-coleta não contaminou
> só os dados: contaminou o **instrumento**. O rotulador foi calibrado
> nas propriedades do estrato sub-coletado e, aplicado ao corpus amplo,
> importou essas propriedades como pressuposto. É a tese da dissertação
> acontecendo dentro do próprio método da dissertação.

## O que sobra do achado da Fase 3

A direção **sobrevive, e mais forte do que o instrumento indicava**:

| entre os tweets com lado atribuído | % pró |
|---|---:|
| humana, nesta amostra (n=68) | **64.7%** |
| modelo, nesta amostra | 57.7% |
| modelo, corpus >10 RT | 62,6% |
| humano (gabarito do paper), >500 RT | 48,4% |

Os neutros que o modelo força para um lado se dividem quase igualmente
(16 pró / 14 anti), o que
**atenua** a estimativa em direção a 50%. Logo o 62,6% medido no corpus
é um **piso**, não um teto: a rotulagem humana desta amostra dá
64.7%. A inversão pró/anti ao descer o limiar não é artefato —
a magnitude relatada é que estava subestimada.

## Leitura

O rotulador **não transfere** para o estrato baixo — mas a falha é **localizada, diagnosticada e de causa conhecida** (a instrução anti-`nenhum` do prompt, herdada da calibração no estrato viral). Não é ruído: é um erro de desenho meu, rastreável até a linha. Consequências: (a) os percentuais absolutos da §1 da Fase 3 estão errados e devem ser retirados; (b) a **direção** do achado sobrevive e é confirmada pela rotulagem humana; (c) o caso ganha um achado metodológico melhor do que o original — a sub-coleta contaminou o instrumento, não só os dados.

_Amostra congelada: `validacao_humana_amostra.csv` (seed 20260726),_
_estratificada em 10–25, 25–50 e 50–100 RT._