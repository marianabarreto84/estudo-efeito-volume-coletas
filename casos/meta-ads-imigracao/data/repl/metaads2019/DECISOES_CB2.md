# Decisão de método — qual CB2 medir

> Gerado em **7/ago/2026**. Números do alvo com a seção do CHI 2021 como proveniência;
> números da réplica apurados por leitura direta de
> [`gabarito_capozzi2020.csv`](gabarito_capozzi2020.csv) (2.312 anúncios), determinístico e
> offline. Decisão **anterior à coleta** — fixa o que a Fase 2 vai medir.
>
> Doc irmão do [DECISOES_ROTULADOR.md](../../../../vacinas/data/repl/vacinas2022/DECISOES_ROTULADOR.md)
> do caso vacinas, que cumpre o mesmo papel lá.

## 1. O problema

CB2, no resumo do CHI 2021: *"Although composing **47.6% of all migration-related ads**,
anti-immigration ones receive **65.2% of impressions**."*

O corpo (§5.2) mostra que os dois números **não são calculados sobre a mesma população** —
e que o primeiro não é sobre "todos" coisa nenhuma:

| base | anúncios | anti | fatia de anúncios | fatia de impressões | **razão R** |
|---|--:|--:|--:|--:|--:|
| **A** · todos os de migração | 2.312 | 677 | **29,3%** | ~42,9% (15/35 M) | **1,46** |
| **B** · só de grandes partidos | 773 | 368 | **47,6%** | não publicada | — |
| **C** · só os com posição (pró+anti) | 1.789 | 677 | **37,8%** | **65,2%** | **1,72** |

Os "47,6%" do resumo são a base **B**; os "65,2%", a base **C**. **O resumo contrasta duas
proporções de populações diferentes**, e chama a isso de desproporção.

## 2. A afirmação substantiva, isolada

O que CB2 diz de fato é: **os anúncios anti-imigração capturam uma fatia de atenção maior
que sua fatia da população de anúncios.** Isso é uma afirmação sobre **desproporção**, e a
grandeza que a carrega é a razão

> **R = (fatia de impressões) ÷ (fatia de anúncios)**

não qualquer das duas porcentagens isoladas. R > 1 confirma a afirmação; R ≈ 1 a derruba.

**R é a métrica a levar para a curva `A(volume)`**, por uma razão prática: R é adimensional
e por isso **comparável entre estratos e entre plataformas**, enquanto as porcentagens
brutas se movem mecanicamente quando a população do denominador muda — que é exatamente o
que a expansão para o Instagram vai fazer.

## 3. Decisão

**Base primária: C (só os anúncios com posição).** Base companheira reportada sempre ao
lado: **A (todos)**. **B fica registrada, não vira teste.**

### Por que C

1. **É a única com denominador coerente.** Só em C as duas metades da afirmação são
   calculadas sobre a mesma população. A desproporção anunciada no resumo (47,6% → 65,2%)
   é, em parte, **artefato da troca de base**: sob uma base só, ela existe mas é menor
   (1,46 em A) ou maior (1,72 em C).
2. **Casa com o instrumento.** O classificador do alvo tem **duas etapas**: relevância
   (F1 = 0,74) e depois inclinação (F1 = 0,85). "Ter posição" é literalmente o domínio de
   saída do segundo. Neutro/irrelevante é uma **terceira** categoria produzida pela
   primeira etapa, não um polo. Medir o balanço **entre polos** dentro do domínio onde os
   polos existem é a única operacionalização que o instrumento sustenta.
3. **Mantém a comparabilidade com o resto da dissertação.** A linha 7 da
   [tabela mestre](../../../RESULTADOS_tabela_mestre.md) reporta a "fatia pró-vacina **entre
   os tweets a que se atribui lado**" — a mesma convenção. Como a leitura PP3 nº 3 (as
   afirmações sobre **balanço** são frágeis) se constrói **comparando casos**, trocar de
   convenção entre eles confundiria a comparação com o efeito que se quer medir.

### Por que A entra junto, e não é redundante

A e C diferem exatamente pela **fatia sem posição** (523 de 2.312 = 22,6%). Reportar as
duas separa dois efeitos que a expansão vai misturar:

- **os polos se rebalancearam** (muda R dentro de C);
- **mudou quanto do corpus toma partido** (muda o tamanho de C dentro de A).

Essa separação não é hipotética: é o mecanismo que o caso vacinas **já encontrou** — a
fatia sem posição cresceu de 24,6% para 33,4% ao sair do estrato viral, e a conclusão foi
que *"a viralidade seleciona quem toma partido"* (linha 7). Aqui o análogo é direto: se ao
incluir o Instagram a fatia sem posição mudar, A e C vão divergir, e a divergência **é o
achado**, não ruído.

### Por que B fica de fora do teste

É um estrato do estrato — anúncios de grandes partidos são **773 de 2.312 (33,4%)** — e o
artigo **não publica a fatia de impressões correspondente**, então R nem é calculável ali
sem refazer a classificação. Fica como célula reportada, com a nota de que é o número que o
resumo imprime.

## 4. ⚠ O problema que apareceu ao conferir: as impressões não reproduzem

Ao tentar confirmar os 35 M de impressões do CHI §5.2 a partir do CSV publicado:

| regra de colapso do intervalo | total de impressões |
|---|--:|
| soma dos `impressions_min` | **36.508.000** |
| **média dos extremos** (a regra **declarada** no SocInfo §3) | **49.780.849** |
| soma dos `impressions_max` | 63.053.698 |
| **o que o CHI reporta** | **~35.000.000** |

Confirmado por caminho independente: somar as 14 colunas demográficas dá **49.654.210**,
consistente com a média dos extremos. A hipótese de que os 35 M seriam só as impressões
localizadas na Itália foi **testada e descartada** — ponderando pela soma das frações
regionais o total fica em 49.709.052 (as frações somam 1,000 na mediana; só 17 anúncios de
2.312 somam menos de 0,99).

**Ou seja: o total publicado está perto da soma dos mínimos, não da média dos extremos que
o método declara usar.** A diferença é de **+42%** entre o declarado e o reportado.

**Consequência direta para CB2:** os 65,2% são uma **fatia de impressões** e herdam essa
ambiguidade. Se os anúncios anti e pró tiverem distribuições de intervalo diferentes — e
não há razão para supor que não tenham, já que os anti são muito mais veiculados — a regra
de colapso **move o número**.

**Regra fixada aqui:** a Fase 2 computa R sob as **duas** convenções (soma dos mínimos e
média dos extremos) e reporta as duas. Se R for robusto às duas, a conclusão não depende da
escolha; se não for, a sensibilidade entra como ressalva da linha 13, no mesmo espírito das
"duas bases de contagem" do AV1 no caso vacinas.

## 5. O que fica registrado para a Fase 2

1. **Métrica primária:** R = fatia de impressões ÷ fatia de anúncios, na base **C**.
2. **Sempre ao lado:** R na base **A**, e o tamanho de C dentro de A (a fatia com posição).
3. **Sempre ao lado:** as duas regras de colapso de intervalo (§4).
4. **Reportada, não testada:** a fatia de anúncios na base **B** (os 47,6% do resumo).
5. **Ponto de partida a bater na Fase 1:** R = 1,72 em C e 1,46 em A — ambos derivados,
   não publicados. O único número publicado que se reproduz diretamente é a contagem de
   anúncios (677 / 1.112 / 523), que **não** depende de nenhuma das ambiguidades acima.

⚠ **Ressalva sobre os próprios 1,72 e 1,46:** dependem do "~15 M" de impressões anti, que o
CHI dá **arredondado** ("nearly 15M"), e do total de 35 M, que §4 mostra não ser
reproduzível. São, portanto, **estimativas do ponto de partida**, não valores canônicos. A
Fase 1 deve recalculá-los a partir do dado, e é bem possível que o ponto publicado **não
reproduza** — o que seria, por si, um resultado da mesma família do "não reproduz o valor
publicado" da linha 3b do Ituassu.
