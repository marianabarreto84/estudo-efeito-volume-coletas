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

> **Aposta da Mariana:** _(a preencher antes da 1ª rodada)_

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
