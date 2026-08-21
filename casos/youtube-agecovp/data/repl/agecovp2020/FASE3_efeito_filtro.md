# Fase 3 (parcial) — o efeito do filtro de palavra-chave

> Medido em **18/ago/2026** sobre **50 das 85** combinações de busca (a cota do dia
> acabou antes). Script: [`analise/fase3_efeito_filtro.py`](../../../analise/fase3_efeito_filtro.py).
> ⚠ **Parcial:** percentuais são estáveis; contagens absolutas, não.

---

## 1. Quanto o filtro descarta

| | n | % |
|---|--:|--:|
| coletados | 2.320 | 100 |
| passam o filtro | 923 | 39,8 |
| **descartados** | **1.397** | **60,2** |

O artigo declara **52,1%** de descarte no ramo da busca (6.997 → 3.353). Nossa
reconstrução descarta **60,2%** — mesma ordem, um pouco mais agressiva. A diferença
provável é de profundidade (2 páginas × 50 combinações contra 12 páginas × 85), que muda
a mistura de resultados: páginas mais fundas trazem itens menos relevantes.

---

## 2. ✅ A reconstrução é fiel — e o filtro é o mecanismo

O teste mais importante desta rodada. Cruzando nossos vídeos com os **3.773 IDs únicos**
do corpus publicado:

| nosso grupo | n | também no corpus do artigo | |
|---|--:|--:|--:|
| **passam o filtro** | 923 | **305** | **33,0%** |
| **descartados** | 1.397 | 86 | **6,2%** |

**Os vídeos que o nosso filtro mantém têm 5,3× mais chance de estar no corpus do artigo do
que os que ele descarta.** Isso valida duas coisas de uma vez: nossa reimplementação do
filtro reproduz a lógica de seleção deles, e o filtro é de fato **o** mecanismo que define
quem entra no corpus — não um detalhe de limpeza.

Cobrimos **10,4%** do corpus deles com 50 das 85 buscas e 2 das 12 páginas. Coerente.

---

## 3. ❌ A predição P4 **falhou** — e a falha é informativa

**Aposta registrada na [Fase 0 §6](FASE0_descoberta.md):** ao soltar o filtro, a fatia
"Society" (categoria dos canais institucionais) **cairia**.

**Não caiu — subiu.** Categorias dos canais (via cruzamento com `channels.csv`, convenção
"primeira categoria", que é a que replica):

| categoria | passam | descartados | Δ |
|---|--:|--:|--:|
| Society | 70,3% | **74,4%** | **+4,1** |
| Knowledge | 11,5% | 4,9% | −6,6 |
| Politics | 6,1% | 5,7% | −0,4 |
| Lifestyle | 4,6% | 4,3% | −0,3 |
| **Sport** | 0,0% | **4,5%** | **+4,5** |
| **Baseball** | 0,0% | **3,4%** | **+3,4** |
| Health | 2,9% | 0,0% | −2,9 |

**O que os dados dizem, contra a aposta:** o conjunto descartado não é "o mesmo assunto
com outra embalagem". Ele traz **conteúdo fora do tema** — `Sport` e `Baseball` aparecem
**só** entre os descartados, somando 7,9%. São resultados que a busca devolveu e que não
falam de idosos na pandemia.

**Consequência para a leitura do caso, e é uma correção de rumo:** o filtro **não é
apenas** um introdutor de viés. Ele faz **dois** trabalhos ao mesmo tempo — remove ruído
genuinamente fora do tema **e** remove conteúdo dentro do tema que não repete a
palavra-chave. A crítica "o filtro descarta 99% dos sugeridos" continua válida, mas não se
sustenta sozinha: parte desse descarte é legítima.

**O teste que isso exige (e que a Fase 3 completa precisa fazer):** restringir a
comparação aos descartados que **estão no tema**, e só então perguntar se a composição
muda. Sem essa etapa, "coletar mais" importa ruído e a comparação fica contaminada — o que
seria uma objeção justa de banca.

⚠ Registrado conforme o princípio §7 do `CLAUDE.md`: *reportar honestamente quando a
aposta falha*.

---

## 4. O que falta

| item | estado |
|---|---|
| completar as 35 combinações restantes | ⏳ cota nova (4h, horário de Brasília) |
| classificar "no tema / fora do tema" nos descartados | ⏳ é o que destrava a §3 |
| AG3 (UGC × imprensa) | ⏳ depende da regra a definir (Fase 2 §4) |
| AG1/AG2 sobre a nossa coleta | ⏳ precisa dos comentários (1 un./100 — barato) |

---

## 5. Ressalvas

- O gabarito tem **3.782 linhas** mas **3.773 IDs únicos** — 9 duplicatas, não
  mencionadas pelos autores.
- O cruzamento de categorias só alcança canais presentes no gabarito (589 dos que passam,
  507 dos descartados); os demais não têm categoria conhecida.
- Tudo aqui é sobre o ramo da **busca**. O ramo dos **sugeridos** (99% de descarte) é
  irreproduzível: `relatedToVideoId` saiu da API em ago/2023.

---

## 6. ✅ Versão corrigida — a comparação **restrita ao tema** (19/ago/2026)

Refeita com `core.regras.no_tema`, que isola o ruído apontado na §3.
Script: [`analise/fase3_no_tema.py`](../../../analise/fase3_no_tema.py).

### 6.1 O filtro age de modo muito diferente dentro e fora do tema

| | passa | descarta | taxa de descarte |
|---|--:|--:|--:|
| **no tema** | 817 | 273 | **25,0%** |
| fora do tema | 106 | 1.124 | **91,4%** |

**Isto é, em boa medida, uma defesa do filtro:** ele descarta 91% do que está fora do
tema e só 25% do que está dentro. A crítica ingênua ("descarta 60% de tudo") não se
sustenta — a maior parte do descarte é limpeza legítima.

**Mas o resíduo é real:** dos **1.397** vídeos descartados, **273 (19,5%) estão no tema**.
Um em cada cinco descartes é perda de conteúdo válido, não remoção de ruído.

### 6.2 ✅ P1 **confirma**: o filtro remove conteúdo de usuário

Entre os vídeos **no tema**, comparando os dois lados sob a mesma regra
(marcador de imprensa **ou** ≥10.000 inscritos):

| | fatia de UGC |
|---|--:|
| passam o filtro | **30,9%** |
| **descartados** | **38,8%** |
| diferença | **+7,9 p.p.** |

O conteúdo que o filtro descarta é **sistematicamente mais de usuário comum** que o
conteúdo que ele mantém. É exatamente o mecanismo previsto na [Fase 0 §6](FASE0_descoberta.md):
exigir a palavra-chave no título ou na descrição é uma prática editorial — quem titula
assim é veículo; quem posta "my grandma got covid" não.

**Consequência substantiva:** o próprio artigo usa a predominância de imprensa para
explicar o sentimento positivo e a toxicidade baixa dos vídeos. Se o filtro é parte da
causa dessa predominância, a explicação é **parcialmente circular** — o corpus é mais
institucional porque o filtro o tornou mais institucional.

### 6.3 ❌ P4 continua falhando, mesmo no tema

"Society" segue **subindo** entre os descartados (68,9% → 77,0%). Caem `Knowledge`
(−4,3), `Lifestyle` (−5,1) e `Politics` (−3,2). A aposta de que a categoria institucional
cairia estava errada nos dois recortes — registrada como falha.

### 6.4 Ressalvas

- Amostra pequena do lado descartado: só **165** canais reconhecidos no gabarito (contra
  531 do lado que passa). O ±7,9 p.p. precisa ser refeito com a coleta completa e com
  `channels.list` para os canais fora do gabarito.
- `no_tema` não é perfeito: `Sport` (3,0%) e `Religion` (2,4%) ainda aparecem entre os
  descartados no tema — vídeos que mencionam idosos e covid de passagem.
- Parcial: 50 de 85 combinações.
