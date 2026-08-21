# Fase 3 (eixo mídia) — curva `A(volume)`: a que volume a conclusão converge?

> Gerado em **07/ago/2026** por `analise/curva_midia_por_volume.py` sobre
> `snapshot_hashtag.sqlite`. Números em `curva_midia.json`.
> Ponto original e universo em [RESULTADOS_analise_midia_MV_MH.md](../../RESULTADOS_analise_midia_MV_MH.md).

**Método.** Subamostras **aleatórias sem reposição** de tamanho `n` crescente,
**B = 300 réplicas** por ponto (o protocolo pede ≥30). A classe de mídia é
recomputada pelo **caminho canônico** (1º link efetivo: campo `links`; se vazio, 1ª
URL do texto, mais o cache de expansão).

> ⚠ **Não usar a coluna `classe_midia` gravada no snapshot** — ela é *pré*-correção
> de jul/2026 (MV 50.040 lá contra 66.370 no canônico). O script recomputa.
> **Validação:** a distribuição recomputada bate exatamente com o canônico —
> MV 66.370 · NDA 37.921 · não_resolvido 18.480 · MH 13.233 · indefinido 4.905.

---

## 1. RTMV% na janela 19–25/out (a quantidade de H1)

| n | média | IC95% (p2,5–p97,5) | largura | **poder de refutar H1** |
|---|--:|--:|--:|--:|
| 100 | 35,74% | 28,00–45,00 | 17,00 | **87,0%** |
| 200 | 35,95% | 30,00–42,50 | 12,50 | **99,7%** |
| 350 | 36,00% | 31,43–41,14 | 9,71 | 100% |
| **700** | **36,09%** | **32,57–39,86** | 7,29 | 100% |
| 1.400 | 36,07% | 33,21–38,71 | 5,50 | 100% |
| 2.800 | 36,11% | 34,54–37,79 | 3,25 | 100% |
| 5.600 | 36,10% | 34,93–37,20 | 2,27 | 100% |
| 11.200 | 36,08% | 35,38–36,76 | 1,38 | 100% |
| 22.400 | 36,09% | 35,77–36,43 | 0,66 | 100% |
| 32.193 | 36,10% | — | 0 | 100% |

*Poder* = fração das 300 réplicas em que um teste unicaudal (α = 0,05) rejeitaria
H₀: RTMV = 50% em favor de RTMV < 50%. É a pergunta operacional certa: não "a banda
exclui 50%?", e sim "com esse `n`, qual a chance de o pesquisador **concluir
corretamente**?".

## 2. P(MV | há mídia) no universo pleno (a dominância MV:MH)

| n | média | IC95% | largura |
|---|--:|--:|--:|
| 100 | 83,39% | 74,51–92,00 | 17,49 |
| **700** | **83,34%** | **79,27–86,83** | 7,56 |
| 2.800 | 83,33% | 81,47–85,26 | 3,79 |
| 22.400 | 83,36% | 82,80–83,92 | 1,12 |
| 140.909 | 83,38% | — | 0 |

---

## 3. As três leituras

### 3.1 A média **não se move** — só a banda encolhe

Em todos os `n`, de 100 a 32.193, a média é **36,1%**. Não há deriva com o volume:
o estimador é não-viesado desde o começo. O que muda é só a precisão (banda de 17,0
p.p. em n=100 a 0,66 p.p. em n=22.400). O mesmo vale para a dominância MV (83,3–83,4%
em todo `n`).

### 3.2 ⚠ Os 48,3% do artigo **não cabem** na banda de n=700

Em n=700 **aleatório**, RTMV cai entre **32,6% e 39,9%** em 95% das réplicas. O
artigo, com **o mesmo n=700**, obteve **48,3%** — fora da banda por ~8,5 pontos.

**Logo a divergência do artigo não é erro amostral: é viés do esquema** (100 tweets/dia
nos horários de pico). Com o mesmo volume, sorteando ao acaso, ele teria acertado.

### 3.3 Bastariam **200 tweets aleatórios** para refutar H1

| n aleatório | poder |
|---|--:|
| 100 | 87,0% |
| **200** | **99,7%** |
| 350+ | 100% |

O artigo coletou **700** — 3,5× mais que o suficiente — e ainda assim concluiu o
contrário, porque o problema nunca foi o tamanho.

---

## 3b. H2 por dia — não reproduz **em nenhum recorte**

> `analise/curva_h2_por_dia.py` → `curva_h2.json`. H2 é afirmação sobre **um dia**,
> então a curva é por dia. Rivalidade operacionalizada como **MH% ≥ MV%** no dia.

| dia | n | universo MV% | MH% | gap | amostra do artigo MV% | MH% | gap |
|---|--:|--:|--:|--:|--:|--:|--:|
| 19/out | 3.063 | 39,7% | 6,6% | 33,1 | 84,0% | 3,0% | 81,0 |
| 20/out | 2.992 | 54,9% | 11,9% | 43,0 | 59,0% | 16,0% | 43,0 |
| 21/out | 3.257 | 50,1% | **15,3%** | 34,8 | 54,0% | 11,0% | 43,0 |
| 22/out | 2.908 | 52,6% | 9,8% | 42,8 | 55,0% | 7,0% | 48,0 |
| **23/out** | 6.106 | **59,0%** | 10,1% | **48,9** | 62,0% | 13,0% | 49,0 |
| 24/out | 7.246 | 29,9% | 9,8% | 20,1 | 51,0% | 11,0% | 40,0 |
| 25/out | 6.621 | 32,7% | 10,5% | 22,2 | 19,0% | 10,0% | 9,0 |

**Taxa de rivalidade** (fração das 300 réplicas com MH ≥ MV), por dia e por `n`
aleatório:

| dia | n=25 | n=50 | n=100 | n=200 | n≥400 |
|---|--:|--:|--:|--:|--:|
| 19/out | 0,3% | 0,0% | 0,0% | 0,0% | 0,0% |
| 21/out | 2,0% | 0,3% | 0,0% | 0,0% | 0,0% |
| **23/out** | **0,0%** | 0,0% | **0,0%** | 0,0% | 0,0% |
| 24/out | 7,7% | 1,0% | 0,0% | 0,0% | 0,0% |
| 25/out | 4,7% | 0,3% | 0,0% | 0,0% | 0,0% |

### O que isso mostra

1. **Em nenhum dia, em nenhum `n` a partir de 50, alguma réplica produz rivalidade.**
   No dia que o artigo aponta (23/out), a taxa é **0% já em n=25**, e o gap médio é
   de 48,8 p.p. — o pior caso em 300 réplicas ainda deixa a MV **31 pontos à frente**.
2. **A amostra do próprio artigo, reconstruída, também não mostra rivalidade em
   23/out**: MV 62,0% × MH 13,0%. Ou seja, H2 não falha por volume **nem** por viés
   de esquema — não se reproduz nem sob o recorte que o artigo usou.
3. **Sob a leitura alternativa** ("MH atinge seu pico na semana"), 23/out também não
   é o dia: no universo o pico de MH é **21/out (15,3%)**; na amostra reconstruída,
   **20/out (16,0%)**.

**Veredito:** H2 **não reproduz sob nenhuma das leituras testadas**, e a divergência
não é atribuível a volume nem a esquema de amostragem. Fica em aberto se ela vem de
uma operacionalização de "rivalizar" diferente da testada aqui, ou da amostra
específica dos autores, que a nossa reconstrução não reproduz exatamente.

⚠ **Ressalva sobre a reconstrução da amostra:** o artigo diz "100 tweets/dia em
horários de pico" sem detalhar o procedimento; a reconstrução usa os 100 primeiros
tweets a partir da hora de pico de cada dia, e a hora de 22/out é ambígua no próprio
artigo (o texto diz 14h, a nota de rodapé 7 sugere ~21h). Os números da coluna
"amostra do artigo" são, portanto, uma **aproximação** do recorte deles.

---

## 4. ⚠ Consequência: a linha 2 da tabela mestre estava errada

A [tabela mestre](../../../RESULTADOS_tabela_mestre.md) registrava, para H1:
*mudou? **SIM** · convergiu? **NÃO***. O "convergiu? NÃO" **não se sustenta**: a
conclusão converge em n ≈ 100–200, muito abaixo do que o artigo coletou.

| | antes | **corrigido** |
|---|---|---|
| Mudou? | SIM (inverte) | SIM (inverte) |
| Convergiu? | NÃO | **SIM — em n ≈ 200** |
| Causa da falha do alvo | volume insuficiente | **viés do esquema de amostragem** |

**O que isso muda na narrativa do caso.** Dizer que "coletar mais era necessário para
chegar à conclusão correta" é **falso** para H1. Coletar mais *revelou* o erro, mas
não era necessário para evitá-lo: uma amostra aleatória **3,5× menor** teria bastado.
O que era necessário era **coletar de outro jeito**.

---

## 5. Implicação metodológica para o protocolo

O par **mudou? / convergiu?** é insuficiente para descrever este caso, e pode
**atribuir a volume uma falha que é de desenho amostral**. Aqui a conclusão *havia*
convergido no volume do artigo, e ainda assim o artigo errou.

Sugere-se uma terceira pergunta no protocolo, quando a coleta original é uma amostra
e não um universo:

> **O esquema de amostragem é não-viesado para a quantidade de interesse?**
> Operacionalização: a estimativa publicada cabe na banda de subamostras
> **aleatórias** do mesmo tamanho? Se não cabe, a divergência é de esquema, não de
> volume — e coletar mais é remédio caro para o problema errado.

Esse teste **não** se aplica aos casos em que o alvo já analisou o universo (é o caso
do eixo A do `vacinas`), mas se aplica a todo alvo que amostrou.

---

## 6. Ressalvas

1. **A subamostragem aleatória é do universo preservado**, que é vizinho e não
   idêntico ao do artigo (ver a ressalva de escopo do caso). A banda mede variação
   amostral dentro do nosso acervo, não dentro do deles.
2. **O poder de §3.3 supõe amostragem aleatória simples.** O artigo amostrou por
   pico, e nenhum `n` corrige um esquema viesado — o poder ali é o de *concluir*,
   não o de *acertar*.
3. A classe de mídia herda o resíduo de **13,1% de link morto** (§6 do canônico);
   as proporções são calculadas sobre a base resolvida em todos os pontos da curva,
   então o viés é constante ao longo do eixo e não afeta a **forma** da curva.
4. `classe_midia` do snapshot é pré-correção e não foi usada (ver cabeçalho).
