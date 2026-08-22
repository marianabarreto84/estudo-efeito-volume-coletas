# Diário de decisões do eixo *stance* — rotulagem

> Espelha o [`DECISOES_ROTULADOR.md`](../../../../../vacinas/data/repl/vacinas2022/DECISOES_ROTULADOR.md)
> do caso vacinas. Registra, em ordem cronológica, **toda** decisão de método tomada
> depois do [pré-registro](PRE_REGISTRO_stance.md) — inclusive as que o pré-registro não
> previu. O pré-registro **não se reescreve**; o que muda entra aqui, datado.

---

## 22/ago/2026 — pré-anotação automática do **dev**, declarada

### A decisão

A Mariana pediu que a rotulagem manual fosse pré-preenchida por LLM, cabendo a ela
revisar. O desenho **aceito** foi mais estreito do que o pedido, e a diferença é o que
mantém o κ interpretável:

| conjunto | n | como é rotulado |
|---|--:|---|
| **dev** | 110 | a Mariana rotula **às cegas, em lotes de 20**; ao fechar cada lote, vê a pré-anotação automática e as divergências |
| **teste** | 210 | **cego, sem exceção.** Nenhum rótulo automático é gerado, exibido ou consultado antes de o gabarito humano estar fechado |
| **reteste** | 40 | da Mariana, sozinha, ≥7 dias depois. Mede o teto intracodificador |

**Por que não pré-anotar o teste.** O critério de aceite (§4 do pré-registro) compara um
rotulador LLM contra o gabarito humano. Se o gabarito for produzido revisando rótulos de
LLM, os dois lados compartilham o mesmo viés — sobretudo nos itens ambíguos (ironia, link
morto, crítica à mídia), que são justamente os que decidem o κ. A concordância subiria sem
que a validade subisse: é a mesma circularidade já registrada no §5 do pré-registro para a
tabela de hashtags.

**Por que pré-anotar o dev é aceitável.** O dev não mede nada — serve para calibrar o
prompt e para achar buracos no codebook. Ancoragem ali não contamina o número publicado, e
a comparação lote a lote transforma o dev no que ele deveria ser: uma conversa sobre as
regras, com as divergências à vista.

### Artefatos

| arquivo | o que é |
|---|---|
| [`prerotulagem_dev_LLM.csv`](prerotulagem_dev_LLM.csv) | os 110 rótulos automáticos do dev. Coluna `fonte` = `pre-anotacao_LLM_opus5_2026-08-22`. **Não abrir antes de rotular** |
| [`rotulagem_dev.html`](rotulagem_dev.html) | página local de rotulagem (sem rede, roda por `file://`). Um tweet por tela, atalhos, salva sozinha, exporta `gold_stance_dev_MARIANA.csv` no formato do gold set |
| [`../../../../analise/gera_pagina_rotulagem.py`](../../../../analise/gera_pagina_rotulagem.py) | gerador da página, a partir do gold set + split + pré-anotação |

A pré-anotação vai embutida na página em base64 e só é decodificada ao fechar um lote.
É anteparo contra ver sem querer, **não** criptografia.

### O que está deliberadamente omitido daqui

A **distribuição agregada** dos 110 rótulos automáticos (quantos EA / ED / NDA) não é
reportada neste arquivo nem em conversa antes de o dev fechar: saber de antemão que "deu
muito NDA" ancoraria a leitura das 110 linhas de uma vez, que é exatamente o que o desenho
acima evita. Ela está no `prerotulagem_dev_LLM.csv` e entra aqui quando o dev fechar.

### Lacunas de regra do codebook — a decidir **antes** de rotular

Não são casos particulares: são regras que o [codebook](../../../../CODEBOOK_stance.md) não
cobre e que apareceram em volume no dev. Como é regra, a autora decide; o enunciado vai
aqui sem a resposta que a pré-anotação adotou, para não anteciparem-se os itens.

1. **Manchete de notícia com valência clara, retuitada sem comentário.** O caso-limite 3
   decide só a notícia *sem* valência (pesquisa eleitoral → NDA). Falta a regra para a
   manchete que favorece ou prejudica um lado de forma inequívoca sem que o retuitador
   comente nada. As duas leituras são defensáveis: pelo caso-limite 1 (RT é endosso) sai
   um lado; por analogia com o caso-limite 3, sai NDA.
2. **Conta de altíssimo volume que só retuíta manchete.** O codebook manda marcar `N` para
   "agregador automático / bot", mas não dá limiar. Há no dev contas com 200–550 mil tweets
   e poucos seguidores, sem 1ª pessoa. `S`, `N` ou `?`.
3. **Nome de exibição que declara lado, tweet que não declara.** Ex.: perfil chamado
   "#Lula13Presidente" retuitando manchete neutra. O codebook diz que o stance é o
   "expresso **neste tweet**", o que empurra para NDA, mas o portão `cidadao` já autoriza
   a olhar handle e nome — falta dizer se o nome conta como sinal de lado.

Decidido isto, a pré-anotação do dev é **regerada** sob a regra escolhida antes de qualquer
comparação, para que as divergências dos lotes sejam de leitura e não de regra.

### O que ainda não existe

`valida_rotulador` (o script do §6.1 do pré-registro) — a escrever quando o gabarito
humano do dev fechar. Nenhuma chamada de LLM foi feita à API paga até aqui: a pré-anotação
do dev saiu da sessão de trabalho, não do orçamento do
[`orcamento.py`](../../../../../vacinas/core/orcamento.py). Saldo intacto em **US$ 9,58**.

---

## 22/ago/2026 — **dev v1 fechado** (110/110) e rodada de revisão aberta

A Mariana rotulou as 110 do dev na página, em lotes de 20, e exportou
[`gold_stance_dev_MARIANA.csv`](gold_stance_dev_MARIANA.csv). Com o dev fechado, cai a
omissão declarada acima: a distribuição agregada dos dois lados vai abaixo.

### Distribuições (dev, n = 110)

| | EA | ED | NDA | | `S` | `N` | `?` | | conf. 3 | 2 | 1 |
|---|--:|--:|--:|---|--:|--:|--:|---|--:|--:|--:|
| **humano (v1)** | 26 | 7 | **77** | | 99 | 5 | 6 | | 12 | 15 | **83** |
| **automático** | 34 | 12 | 64 | | 89 | 16 | 5 | | 68 | 33 | 9 |

### Concordância

| medida | valor |
|---|---|
| stance — concordância bruta | **84,5%** (93/110) |
| stance — **κ de Cohen** (3 classes) | **0,699** |
| portão `cidadao` — concordância | **82,7%** |
| portão `cidadao` — κ | **0,343** |
| divergências de **polo** (EA × ED) | **0** |
| divergências **lado × NDA** | 17 (em 15 delas o humano é o mais conservador) |
| divergências **só no portão** | 16 |

> ⚠ **Este κ não é o κ do critério de aceite.** O §4 do pré-registro mede *rotulador
> automático × gabarito humano* **no teste de 210**, com o prompt congelado. O 0,699 aqui
> é dev, contra uma pré-anotação não calibrada, e serve como **sinal do teto da tarefa** —
> um teto perto de 0,70 já era a aposta P4.

### Três achados que valem para o capítulo, não só para a calibragem

1. **Zero divergência de polo.** Em 110 itens, nunca um leu EA onde o outro leu ED.
   Quando há lado, os dois veem o mesmo lado; **toda** a discordância é sobre *haver ou
   não* lado. A fronteira frágil do rótulo do artigo é `lado × NDA`, não `EA × ED` — e é
   justamente a fronteira que decide a proporção de NDA que o artigo reporta em 23,4%.
2. **As duas leituras concordam na direção de P1 e discordam na magnitude.** NDA em
   **70%** (humano) e 58% (automático), contra os 23,4% do artigo. A aposta P1 (≥35%)
   está confirmada com folga nos dois, o que é raro e é bom: o efeito não depende de quem
   rotula.
3. **Confiança 1 em 83 dos 110 (75%).** O §4.3 do pré-registro promete reportar o κ
   *restrito a `confiança ≥ 2`*; com este perfil esse corte fica com **n = 27**, quase
   sem poder. Vale saber se o 1 saiu de dúvida genuína ou de tecla rápida — o dado sugere
   dúvida genuína, porque a concordância cai justamente ali (conf. 3: 11/12 · conf. 2:
   15/15 · conf. 1: 67/83), mas a decisão de como reportar é da autora.

### Rodada de revisão (aberta)

As **33 divergências** voltaram para uma segunda leitura em
[`revisao_dev.html`](revisao_dev.html) — mesma mecânica da página de rotulagem, agora com
o rótulo automático e **o motivo dele** à vista, e um campo em que a anotadora justifica
por escrito a decisão final. Saída: `revisao_dev_MARIANA.csv`, com `v1`, `v2`, o flag
`mudou` e a justificativa.

Os motivos do lado automático estão versionados em
[`justificativas_auto_dev.json`](justificativas_auto_dev.json); o gerador é
[`../../../../analise/gera_pagina_revisao.py`](../../../../analise/gera_pagina_revisao.py).

⚠ **Esta rodada é ancorada por construção** — a anotadora já viu o outro rótulo. É
aceitável **porque é dev**, que calibra e não mede, e fica registrado que o `v2` do dev é
um gabarito *de consenso*, não independente. O `v1` fica preservado no arquivo, e é dele
que sai qualquer número que precise de gabarito não-ancorado. O **teste de 210 não passa
por nada disso**.

### Pendências que a revisão deve resolver

- as **3 lacunas de regra** da seção anterior — 15 das 17 divergências de stance e boa
  parte das do portão caem nelas;
- dois itens em que o humano atribuiu lado e o automático não: o **item 44** (pesquisa
  Datafolha retuitada sem comentário, que o caso-limite 3 manda ler como NDA) e o
  **item 6** ('Samba #diva #rainhadanaçao');
- quatro contas que o §1 do codebook lista nominalmente como não-cidadãs e que ficaram
  como `S`: **@g1**, **@MPF_AP**, **@DiariodaCPTM** e **@ptrevisani** (jornalista
  verificado). A anotadora marcou `N` corretamente em @g1politica, @UOLNoticias, @geledes,
  @OpiniaoTV e @BlogOlhoNaMira, então não é leitura errada do portão — provavelmente são
  deslizes, e a revisão confirma ou não.

---

## 22/ago/2026 — **rodada 2 do dev**: as 33 divergências revistas

Entrada: [`revisao_dev_MARIANA.csv`](revisao_dev_MARIANA.csv) — **27 dos 33** itens
mudaram, **12** com justificativa escrita. Consolidado em
[`gold_stance_dev_v2.csv`](gold_stance_dev_v2.csv) (110 linhas; o `v1` fica intacto em
[`gold_stance_dev_MARIANA.csv`](gold_stance_dev_MARIANA.csv)).

| | EA | ED | NDA | `S` | `N` | `?` | stance × auto | portão × auto |
|---|--:|--:|--:|--:|--:|--:|---|---|
| **v1** (cego) | 26 | 7 | 77 | 99 | 5 | 6 | 84,5% · **κ 0,699** | 82,7% · κ 0,343 |
| **v2** (revisto) | 32 | 11 | 67 | 90 | 17 | 3 | 94,5% · **κ 0,900** | 96,4% · κ 0,884 |

> ⚠ Números **anteriores** à correção do item 38 (seção seguinte). Com ela, o `v2` passa a
> **95,5% · κ 0,916** no stance; o portão não muda.

### ★ O efeito de ancoragem, medido dentro do próprio caso

O mesmo anotador, sobre os mesmos 110 itens, sob o mesmo codebook, passou de **κ 0,699
para κ 0,900** depois de ver os rótulos da máquina — **+0,201**. É a estimativa mais
direta que este trabalho tem do que a pré-anotação faz com uma medida de concordância, e
ela vem de dado próprio, não da literatura.

Duas ressalvas, nas duas direções:

- é **limite superior** do efeito de ancoragem, porque parte do ganho é **correção
  legítima**: quatro contas que o §1 do codebook nomeia como não-cidadãs (@g1, @MPF_AP,
  @DiariodaCPTM, @ptrevisani) estavam como `S` por deslize, e voltar para `N` é acerto,
  não conformidade;
- é **limite inferior** do risco no teste, porque aqui a anotadora tinha o motivo escrito
  do outro lado e podia discordar — em **6 dos 33** ela discordou e manteve o `v1`, com
  argumento. Numa revisão apressada de 210 itens, sem esse atrito, a convergência seria
  maior.

De qualquer modo, **o número que o §4 do pré-registro exige continua vindo do teste cego
de 210**, e o `v2` do dev **não é** gabarito independente: é consenso. Onde a dissertação
precisar de gabarito não-ancorado do dev, usa-se o `v1`.

### Onde as duas leituras ainda não se encontram (10 itens)

Restam 10 divergências `v2 × automático`, e uma delas é **de polo** — a primeira do caso:

- **item 38** (CAA/MG, *"O povo brasileiro clama por mudanças #AntonioAnastasia"*): a
  anotadora leu **ED**, o automático leu **EA**. ⚠ Antônio Anastasia era o candidato ao
  Senado por Minas **na chapa do Aécio** (PSDB), sucessor dele no governo do estado, e
  *"clama por mudanças"* é o enquadramento da oposição. Fica anotado como **provável
  deslize factual, pendente de confirmação da autora** — não foi alterado.
- os outros 9 são as fronteiras já conhecidas: manchete com valência (itens 1, 9, 43, 82),
  portão de conta de alto volume (14, 105, 108, 7) e o item 6.

### As três lacunas de regra, respondidas pelas justificativas

As justificativas dela **decidem duas** das três lacunas abertas em 22/ago e deixam a
primeira com um resíduo:

1. **Manchete com valência, retuitada sem comentário.** A prática do `v2` não é "sempre
   NDA" nem "sempre o lado": ela atribui lado quando a notícia é **fato de terceiro** que
   favorece ou fere uma campanha (itens 2, 11 → EA; 80, 100 → ED; 7 → ED "mas é chute"), e
   mantém **NDA** quando a manchete é a **fala do próprio candidato** — *"pode apenas estar
   compartilhando uma notícia"*, *"é mais compartilhamento de notícia importante"* (itens
   43, 82, 9). ⚠ **Resíduo:** o item 24 ("*Ataque à Veja é ataque à democracia*, diz
   Aécio") também é fala de candidato e foi para **EA**, contra a regra que os outros três
   sugerem. A regra precisa do aval da autora e o item 24, de decisão.
2. **Conta de altíssimo volume que só retuíta manchete.** Volume **não** basta: a
   anotadora **abriu os perfis** e decidiu por eles (*"entrei no perfil e é de um cidadão
   comum sim"* — item 14 → `S`; item 5 → `S`). O `?` fica para quando o perfil não decide
   (itens 33, 107). ⚠ **Assimetria nova, e não é pequena:** isso usa informação que **não
   está no snapshot congelado** e que o rotulador automático **não tem como consultar** —
   e, pior, é o perfil **de 2026**, não o de 2014. Ver a seção seguinte.
3. **Nome de exibição que declara lado, tweet que não declara.** Não foi contestada em
   nenhum item: os dois perfis nessa situação (21 e 76) ficaram **NDA** no `v1` e não
   entraram nas divergências. Regra: **o nome não conta como sinal de lado**; o portão
   `cidadao` continua podendo olhar handle e nome.

### ⚠ Consulta ao perfil vivo — decisão pendente da autora

Em pelo menos dois itens o portão `cidadao` do `v2` foi decidido consultando o perfil na
web **hoje**. Consequências, para constar antes do teste de 210:

- **o gabarito deixa de ser reproduzível a partir do snapshot** — quem tiver o CSV
  congelado não chega ao mesmo rótulo;
- **o critério de aceite do portão fica injusto com a máquina** (§4.2: acurácia ≥ 0,90):
  o rotulador automático vê handle, nome e métricas de 2014; o humano viu o perfil de
  2026;
- **contas mudam em 12 anos** — o que hoje parece cidadão comum pode ter sido outra coisa
  em out/2014, e vice-versa.

Três saídas, e a escolha é da autora: (a) proibir a consulta e refazer os itens afetados
só com o congelado; (b) permitir, declarar no capítulo e **medir o portão à parte**, sem
o critério de 0,90; (c) permitir e dar a mesma informação à máquina, o que exigiria
coletar os perfis atuais — trabalho novo e fora do escopo. **Nada foi alterado enquanto
não se decide.**

### Perfil de confiança — praticamente inalterado

`1` em **77** dos 110 (era 83), `2` em 22, `3` em 11. O corte pré-registrado
"κ restrito a `confiança ≥ 2`" segue com **n = 33**. Continua de pé a decisão de como
reportar.

---

## 22/ago/2026 — as **três decisões da autora**, e o codebook atualizado

Fecham as pendências da rodada 2. As duas primeiras alteram o
[codebook](../../../CODEBOOK_stance.md), que passa a valer **para o teste cego de 210**.

### 1. Consulta ao perfil vivo — **permitida**

> *"Eu acho justo porque acaba sendo a verdade."*

O gabarito humano pode abrir o perfil na web quando handle, nome e métricas não decidirem
o portão `cidadao`. A justificativa é que o gabarito precisa ser **verdadeiro**; se a
máquina não alcança essa informação, o limite é da máquina.

Duas consequências ficam declaradas, e nenhuma delas desfaz a decisão:

- **a acurácia do portão passa a ser reportada em duas versões** — em todos os itens e
  restrita aos **decidíveis pelo congelado**. O critério de aceite de ≥ 0,90 (§4.2 do
  pré-registro) só é justo na segunda, e é assim que vai ao capítulo. Não é mudança de
  critério: é a mesma medida, com a base explicitada;
- o perfil consultado é o de **2026**. Onde ele contradisser o que o tweet de 2014
  aparenta, o codebook agora pede `nota=perfil_2026`, para que a fração seja mensurável em
  vez de invisível.

### 2. Manchete com valência — regra **graduada**, não binária

> *"nem toda manchete contra a Dilma e o Aécio é favorável ao outro lado, algumas sim […]
> outras são tão criticaszinhas que eu acho que é mais NDA mesmo."*

Vira o **caso-limite 13**: vale o **lado** quando a manchete é **fato de terceiro** com
valência inequívoca (a irmã do adversário pedindo voto; propaganda suspensa pelo TSE); é
**NDA** quando é a **fala do próprio candidato** ou crítica fraca — quem retuíta pode
apenas estar circulando notícia de eleição. O critério não é só *quem fala*: é também
*quão forte*.

O **item 24** (*"Ataque à Veja é ataque à democracia", diz Aécio*) fica como ela decidiu na
revisão, **EA**, e é o caso-fronteira da regra: é fala de candidato, mas não é criticazinha
— é enquadramento de campanha em carga alta. Registrado como fronteira, não como exceção
arbitrária.

Entrou junto o **caso-limite 14** (nome de exibição que declara lado ≠ stance do tweet →
**NDA**), que a rodada 2 não contestou, e a nota no §1 de que **volume de tweets não
decide sozinho** o portão.

### 3. Item 38 — corrigido

> *"Desculpa marquei errado, era para ser EA, pode trocar."*

`gold_stance_dev_v2.csv`: CAA/MG passa de **ED** para **EA**, com `nota=corrigido_22ago_deslize`.
O `v1` e o `revisao_dev_MARIANA.csv` **não** foram tocados — são a entrada crua.

**Dev v2, final:** EA 33 · ED 10 · NDA 67 · portão `S` 90 / `N` 17 / `?` 3.
Contra o automático: stance **95,5% · κ 0,916**; portão **96,4% · κ 0,884**;
**zero divergência de polo**.

### Uma promessa que cai

O registro de 22/ago dizia que, decididas as lacunas, a pré-anotação do dev seria
**regerada** sob a regra nova "antes de qualquer comparação". Isso não se aplica mais: a
comparação já aconteceu, e foi **ela** que produziu as regras — 15 das 17 divergências de
stance caíam justamente nas lacunas. Regerar agora só produziria concordância por
construção. A pré-anotação do dev fica como está, datada e sob as regras antigas; o que
passa a valer o codebook novo é **o prompt do rotulador automático**, que ainda vai ser
escrito.
