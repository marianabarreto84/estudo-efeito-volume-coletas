# Pré-registro do eixo *stance* (caso twitter-ituassu)

> Registrado em **18/ago/2026**, **antes** de qualquer chamada de LLM e **antes** de
> qualquer tweet ser rotulado à mão. Espelha o que o caso vacinas fez em
> [PRE_REGISTRO_split.md](../../../../vacinas/data/repl/vacinas2022/DECISOES_ROTULADOR.md)
> (lá: split congelado antes da 1ª chamada, critério de aceite escrito antes de medir).
>
> Princípio §7 do `CLAUDE.md`: *"antes de rodar um caso no universo, registrar a aposta;
> reportar honestamente quando a aposta falha"*.

---

## 1. População, amostra e congelamento

| item | valor |
|---|---|
| snapshot | `snapshot_hashtag.sqlite` (#Eleições2014, extraído da `ituassu_2014`/vm067) |
| janela | **19–25/out/2014** — a mesma do artigo de 2015 e do eixo mídia |
| população | **32.193** tweets |
| amostra do gold set | **320** tweets, aleatória, estratificada por dia (proporcional, maior resto) |
| seed | `20260818` |
| split | **110 dev** (calibragem do prompt) / **210 teste** (cego) |
| reteste intracodificador | **40** itens, ordem própria, ≥ 7 dias depois |
| `sha256(ids)[:12]` | **`dc8ee39ff69b`** |
| congelado em | `split_stance.json` — o script se recusa a re-sortear sem `--refazer` |

Cotas por dia: 19/10=30, 20/10=30, 21/10=32, 22/10=29, 23/10=61, 24/10=72, 25/10=66.

**Por que amostra aleatória e não 100/dia como o artigo.** O artigo sorteou 100 tweets/dia
**a partir das 21h** (§*metodologia*) — um esquema com viés já demonstrado no eixo mídia
(o 48,3% de RTMV dele **não cabe** na banda de subamostras aleatórias de n=700; ver
[RESULTADOS_FASE3_curva_midia.md](../RESULTADOS_FASE3_curva_midia.md)). O gold set precisa
representar **a população**, não o esquema do artigo. A comparação com o esquema dele é
feita depois, aplicando o rotulador já validado às duas grades.

**Por que 320.** É o mínimo que sustenta um teste cego de 210 (IC de κ aceitável) mantendo
110 para calibrar o prompt sem contaminar a medida. O `ESTADO.md` estimava "~200–300"; 320
mantém a folga sem passar de ~4h de leitura humana.

---

## 2. Alvos do artigo (o que se quer reproduzir)

**2015** — 700 tweets, 666 cidadãos (95,1%):

| rótulo | n | % dos cidadãos |
|---|--:|--:|
| ED (Dilma) | 284 | 42,6% |
| EA (Aécio) | 226 | 33,9% |
| NDA | 156 | 23,4% |

**2018** — amostra D, n = 1.129 (só quem tinha mídia **e** preferência identificável):
EA 581 (51,5%) × ED 548 (48,5%). **A maioria inverteu entre os dois papers.**

---

## 3. Apostas pré-registradas (18/ago/2026)

Registradas por quem preparou o kit. ⏳ **A Mariana deve registrar as dela aqui abaixo
antes da primeira rodada** — divergir da aposta é dado, não é problema.

| # | aposta | por quê |
|---|---|---|
| **P1** | **NDA sobe muito** acima dos 23,4% do artigo — aposta: **≥ 35%** no universo | duas causas somadas e de direção conhecida: (a) o esquema do artigo amostra o **pico das 21h**, onde o conteúdo é mais politizado; (b) **link morto** força NDA no caso-limite 8 do codebook |
| **P2** | Entre os tweets **com lado atribuído**, **EA > ED** na janela | a própria expansão do grupo (700 → 1.129) já inverteu para EA; e a janela termina em 25/10, com #VemPraRua25deOutubro (EA 100%, 395 usos) no topo |
| **P3** | A composição EA/ED **converge tarde** — fração ≥ 0,5 — bem depois do eixo mídia (que fechou em n≈200) | é razão entre duas classes **próximas**; separar 51% de 49% exige muito mais n do que separar 36% de 50% |
| **P4** | O κ humano×humano (ou humano×ele mesmo, no reteste) fica **abaixo** do κ do caso vacinas (0,759) | lá o rótulo era de **conteúdo declarado**; aqui é **inferência de intenção** a partir de ironia e link morto — tarefa mais frouxa |

> **Aposta da Mariana** — registrada em **9/set/2026**, com o gabarito humano dos 210
> fechado e **antes** de o rotulador automático ser executado (nenhuma chamada de LLM
> havia sido feita sobre o teste; o `--dry-run` só contou tokens):
>
> **“Acho que ele não vai passar no critério de aceite. Mas não tenho muita certeza.”**
>
> Leitura operacional: aposta em **κ < 0,70** no stance dos 210 — ou seja, em
> **reprovar** o critério 1 do §4. A aposta é **declaradamente incerta**, e isso fica
> registrado: uma previsão hesitante que falha custa menos ao argumento do que uma
> previsão confiante que falha, e a diferença só é auditável se estiver escrita antes.
>
> Vale dizer que ela aponta na direção **oposta** à do kit em um ponto: P4 apostava que
> o κ ficaria abaixo dos 0,759 do caso vacinas, o que é compatível com passar em 0,70;
> a Mariana aposta que nem o piso se sustenta. Se ela acertar, o §4 manda **iterar o
> prompt só no dev** e, após três versões sem passar, **reportar o fracasso** — que é
> resultado publicável: um teto baixo significa que o rótulo de *stance* do artigo de
> 2015 é frágil, e isso é matéria da tese.
>
> ⚠ As apostas **P1 e P2 já estavam resolvidas** quando esta foi registrada, pelo
> próprio gabarito humano (NDA 71,4% — P1 confirma; EA 66,7% entre os com lado — P2
> confirma). Esta aposta não as alcança. **P3 segue aberta** e ainda admite aposta,
> até a curva rodar sobre os 32.193.

---

## 4. Critério de aceite do rotulador automático (escrito antes de medir)

Medido **uma única vez** no teste cego de 210, com o prompt já congelado:

1. **κ de Cohen (3 classes EA/ED/NDA) ≥ 0,70** — o mesmo patamar do caso vacinas;
2. **acurácia do portão `cidadao` ≥ 0,90**;
3. reportar **sempre em conjunto**, sem escolher o melhor: κ com duplicatas e **sem**;
   κ em todos os itens e **restrito a `confianca ≥ 2`**; e o **teto** (reteste humano).

**Se reprovar:** iterar o prompt **só no dev**, versionando cada mudança num diário de
decisões (como `DECISOES_ROTULADOR.md` do vacinas). Após **3 versões** sem passar,
**reportar o fracasso** — um teto baixo é resultado publicável: significa que o rótulo do
artigo é frágil, e isso é matéria da tese, não obstáculo a ela.

**Nunca:** olhar o teste para escolher prompt; re-sortear a amostra depois de medir;
reportar κ de uma rodada e não de outra.

---

## 5. Riscos e vieses declarados

| risco | direção conhecida | mitigação |
|---|---|---|
| **Link morto** (t.co de 2014) | **infla NDA** e reduz EA e ED | codebook §4 caso 8; `host1` resolvido é dado ao anotador; reportar a fração `nota=link_morto` |
| **Avatar inexistente** — o artigo usava *"algo no ícone do usuário"* | ruído no portão `cidadao` | declarado; medir acurácia do portão à parte |
| **Circularidade da tabela de hashtags** (apêndice §7 do codebook) | **infla κ** sem aumentar validade | a tabela é contexto e não regra; se ela entrar no prompt do LLM, o κ tem de ser reportado também **sem** os itens que a acionam |
| **Duplicatas** (90 de 320 itens em grupo repetido) | **infla κ** | κ reportado com e sem deduplicação |
| **Anotador único** | sem medida de concordância entre pessoas | o reteste de 40 dá o **teto intracodificador**; se houver 2ª pessoa, ela rotula o mesmo arquivo e mede-se κ humano×humano |

---

## 6. O que acontece depois do gabarito

1. `valida_rotulador` (a escrever, espelhando o do vacinas): LLM sobre o dev → prompt
   congelado → **uma** medida no teste.
2. Aprovado: aplicar ao universo da janela (**32.193**) sob teto de gasto rígido
   (`ANTHROPIC_VACINAS_API_KEY`, saldo restante **US$ 9,58** — o escopo cabe folgado com
   agrupamento de 10 tweets/chamada).
3. Fase 3: curva `A(volume)` da composição EA/ED/NDA → responde *mudou?* e *convergiu?*
   e fecha a **linha 10** da [tabela mestre](../../../../RESULTADOS_tabela_mestre.md).
4. Terceira pergunta (§4.9 do `ESTADO.md`): *o esquema 100/dia às 21h é não-viesado para
   a composição?* — operacionalizada como "o 42,6% ED do artigo cabe na banda de
   subamostras aleatórias de n=666?".

---

## 6. Estimativa corrigida sobre o universo (registrada em 9/set/2026)

> Registrada **antes** de sortear a amostra do universo e **antes** de qualquer
> chamada de LLM sobre ela. O que ja se sabia neste momento: o rotulador
> **reprovou** o criterio do §4 (κ 0,604 < 0,70; portão 0,781 < 0,90) e o teto
> estimado pelas duplicatas do dev é de κ ≈ 0,625 (15 pares; 0,198 com o texto
> da irmã de Lula, 0,625 sem ele).

### 6.1 Por que seguir com um rotulador reprovado

O κ nunca foi o objetivo: era o portão para decidir se dava para soltar o
rotulador sobre os 32.193 e construir a curva. Reprovado como instrumento de
**rótulo individual**, ele ainda pode servir como instrumento de **estimativa
agregada**, desde que o viés seja corrigido em vez de ignorado. A matriz de
confusão foi medida nos 210 e diz exatamente o tamanho e a direção do erro (a
máquina marca EA em 56 onde a humana marcou 40).

⚠ **O critério do §4 NAO e alterado.** Ele continua reportado como **reprovado**.
Esta seção acrescenta uma segunda medida, declaradamente *post hoc*, e a
distinção entre as duas tem de aparecer no capítulo. Baixar o 0,70 depois de ver
0,604 seria exatamente a prática que esta dissertação documenta nos seis casos.

### 6.2 Amostra do universo

| item | valor |
|---|---|
| população | **32.193** tweets (janela 19–25/out/2014, `snapshot_hashtag.sqlite`) |
| amostra | **5.000**, aleatória, estratificada por dia (proporcional, maior resto) |
| semente | `20260909` |
| congelamento | `amostra_universo_stance.json`, com `sha256(ids)[:12]` |
| modelo | `claude-haiku-4-5-20251001`, o **mesmo** prompt congelado dos 210 |

Por que 5.000 e não os 32.193: o saldo do livro-caixa é de US$ 9,42 e o universo
inteiro custaria ~US$ 15,8. 5.000 custa ~US$ 2,4 e já sustenta a curva e os
intervalos. A amostra **inclui** os 320 do gabarito, por serem parte da
população; a sobreposição será reportada.

### 6.3 Correção (declarada antes de medir)

Seja `M[i][j] = P(rótulo automático = j | rótulo humano = i)`, estimada na matriz
de confusão dos 210. Se `q` é o vetor de proporções que o rotulador produz na
amostra do universo, a estimativa corrigida é `p = (Mᵀ)⁻¹ q`, projetada no
simplex quando a inversão cair fora dele.

Incerteza por **bootstrap** (2.000 reamostragens), propagando as **duas** fontes:
a da matriz (reamostra os 210) e a da amostra do universo. O intervalo sai mais
largo que o ingênuo — e é esse o ponto: o preço de usar um rotulador ruidoso
aparece no intervalo, e não é escondido.

Reporta-se **sempre em conjunto**: a proporção bruta do rotulador e a corrigida.

### 6.4 Curva e critério de convergência

A curva `A(volume)` refaz a estimativa corrigida em subamostras de tamanho
crescente (100, 200, 500, 1.000, 2.000, 5.000), 200 sorteios por ponto.

**Convergiu** = a partir daquele volume, o IC95% da estimativa corrigida está
inteiro dentro de ± 3 pontos percentuais do valor em n = 5.000. Escrito agora,
antes de ver qualquer curva.

### 6.5 Predições (antes de rodar)

| # | predição | por quê |
|---|---|---|
| **P5** | A correção **derruba EA** em relação ao bruto do rotulador | a matriz mostra que a máquina inventa lado onde a humana viu NDA: 17 NDA→EA e 11 NDA→ED |
| **P6** | A conclusão do artigo (**ED > EA**) **não se sustenta** no universo, mesmo corrigida | o gabarito de 210 já dá EA 66,7% entre os com lado, e ele é amostra aleatória da mesma população |
| **P7** | O NDA corrigido fica **acima de 60%**, contra os 23,4% do artigo | o gabarito dá 71,4%, e a correção empurra NDA para cima, não para baixo |

> **Aposta da Mariana sobre a §6:** _(em aberto — pode ser registrada até o
> sorteio ser feito)_
