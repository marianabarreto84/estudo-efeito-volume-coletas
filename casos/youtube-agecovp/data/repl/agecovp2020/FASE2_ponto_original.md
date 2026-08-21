# Fase 2 — o ponto original do AGECovP, reproduzido

> Medido em **18/ago/2026** sobre o gabarito publicado pelos autores
> ([Zenodo 15800324](https://zenodo.org/records/15800324)), **inteiramente offline** —
> nenhuma chamada de API, nenhuma unidade de cota.
> Script: [`analise/fase2_ponto_original.py`](../../../analise/fase2_ponto_original.py) ·
> saída: `fase2_ponto_original.json`.

---

## 1. AG4 — categorias de canal: replica, e **revela uma convenção não declarada**

Alvo: Society **56,4%**, Lifestyle 13,6%, Knowledge 12,1%, Politics 4,1%, Health 3,7%.

Os canais têm **múltiplas** categorias, e o artigo não diz como as conta. Testadas quatro
convenções:

| convenção | Society | Lifestyle | Knowledge | Politics | Health | erro total |
|---|--:|--:|--:|--:|--:|--:|
| por canal (fração dos canais) | 76,6 | 35,1 | 26,8 | 10,3 | 11,9 | 70,8 p.p. |
| por atribuição | 39,0 | 17,9 | 13,6 | 5,3 | 6,1 | 26,8 p.p. |
| **só a primeira categoria** | **55,4** | **14,0** | **12,2** | **3,8** | **3,8** | **1,9 p.p.** ✅ |
| por canal, só quem tem categoria | 78,3 | 35,9 | 27,4 | 10,6 | 12,2 | 74,5 p.p. |

**Replica** — mas só sob a convenção *"conta apenas a primeira categoria de cada canal"*,
que **o artigo não declara**. As outras erram por 27 a 75 pontos percentuais. É o mesmo
tipo de achado do AV1 do caso vacinas: o número publicado só existe dentro de uma
convenção de contagem que ficou implícita.

⚠ 50 dos 2.243 canais não têm categoria alguma.

---

## 2. AG1 — sentimento dos comentários: **VADER replica, TextBlob não**

| | medido | artigo | erro |
|---|---|---|--:|
| **VADER** (limiar ±0,05) | positivo **39,4** · negativo **38,6** · neutro **22,0** | 39 / 39 / 22 | **0,8 p.p.** ✅ |
| **TextBlob** (limiar 0) | positivo 42,4 · neutro 33,0 · negativo 24,6 | 39 / 39 / 22 | 12,0 p.p. ✘ |

O VADER bate quase exatamente. O TextBlob não — e a causa é o **limiar de neutralidade**,
que o artigo não publica. Varrendo a banda:

| banda | positivo | neutro | negativo | erro |
|---|--:|--:|--:|--:|
| 0 (estrito) | 42,4 | 33,0 | 24,6 | 12,0 |
| ±0,03 | 40,5 | 36,5 | 23,0 | 5,0 |
| **±0,05** | **38,2** | **40,8** | **21,1** | **3,5** ✅ melhor |
| ±0,075 | 36,2 | 44,2 | 19,6 | 10,4 |
| ±0,1 | 32,5 | 50,2 | 17,3 | 22,4 |

O mínimo cai em **±0,05** — o mesmo limiar que o VADER usa. A leitura mais provável é que
aplicaram a banda do VADER também ao TextBlob. Mesmo no melhor caso sobra **3,5 p.p.**, e
a diferença fica **sem causa atribuída**.

**Registro de método:** a segunda coluna do artigo é reproduzível a menos de 1 p.p.; a
primeira, não, e a distância depende de um parâmetro não publicado. Vale como limite de
reprodutibilidade do alvo.

---

## 3. AG2 — o alvo comparativo: **replica**

O artigo afirma *"a maior proporção de conteúdo negativo nos comentários em comparação
com os vídeos"*.

| | média de toxicidade | n |
|---|--:|--:|
| vídeos | **0,0019** | 3.782 |
| comentários | **0,1410** | 69.425 |

Os comentários são **74× mais tóxicos** que os vídeos. A afirmação comparativa replica com
folga enorme.

⚠ **Ressalva de medida:** o gabarito traz *sentimento* só dos comentários; a comparação
vídeo × comentário teve de ser feita por **toxicidade**, que existe nos dois lados. É uma
proxy do que o artigo afirma, não a mesma medida. Declarar no capítulo.

---

## 4. AG3 — fica **pendente**, e o motivo importa

O artigo afirma que *"UGC representa menos de 7%"* — o conteúdo é dirigido por veículos de
imprensa, não por usuários. **Não é verificável no gabarito:** os autores não publicam a
regra que separa "user-generated" de "veículo", e não há coluna correspondente nos CSVs.

Isso é inconveniente porque **AG3 é justamente o alvo mais exposto ao filtro** (predição
P1 da [Fase 0](FASE0_descoberta.md)). Saída para a Fase 3: definir a regra nós mesmos,
declará-la, e aplicá-la **igual** aos dois lados (com filtro e sem filtro) — o que preserva
a comparação mesmo sem reproduzir o valor absoluto do artigo.

---

## 5. Leitura

O ponto original **replica em 2 dos 3 alvos verificáveis** (AG4 e AG2), e o terceiro (AG1)
replica pela metade — uma biblioteca sim, a outra não. Nos dois casos em que houve
divergência, a causa foi a **mesma**: um parâmetro de convenção que o artigo não publica
(como contar categorias; onde cortar a neutralidade).

Com isso o ponto de partida está fixado: qualquer mudança medida na Fase 3 é atribuível ao
**filtro**, e não a erro de reimplementação nossa.

---

## 6. Linha na tabela mestre

Preenche a coluna *"o ponto original replica?"* da linha do caso YouTube:
**replica sob convenção declarada** (AG4 a 1,9 p.p., AG2 com folga, AG1 só no VADER).
As colunas *mudou?* e *convergiu?* seguem ⏳ até a Fase 3.
