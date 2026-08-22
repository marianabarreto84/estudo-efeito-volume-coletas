# Fase 2 — o ponto original do Massachs, reproduzido

> Medido em **18/ago/2026** sobre o **gabarito publicado pelos próprios autores**.
> Script: [`analise/mh1_ponto_original.py`](../../../analise/mh1_ponto_original.py) ·
> saída: `mh1_ponto_original.json` · fonte: `reddit-politics-12-16.csv.bz2`.
> **Sem VPN, sem banco** — o dataset é público.

---

## 1. O dado

| item | valor | confere com o artigo? |
|---|---|---|
| origem | `github.com/JoanMassachs/reddit-data` (a Fase 0 registrou `JoanMG`, que **redireciona**) | — |
| `sha256` do `.bz2` | `ff15e5c3a09000dd…f548da51` | — |
| usuários (focus group) | **44.924** | ✅ **exato** |
| colunas de feature | 3.353 (766 `participation_12`, 985 `participation_16`, 766+766 scores, 69 de interação) | ✅ compatível |
| rótulo `y` = participou de r/The_Donald em 2016 | **7.083 (15,77%)** | ✅ artigo: 7.083 (15,8%) |

O `README` dos autores documenta cada família de feature — inclusive a definição
operacional do rótulo. **Não há nada a hidratar:** o ponto original é reproduzível
inteiramente offline.

---

## 2. MH1 — a ordenação **reproduz**

Regressão logística, 5-fold CV estratificado, F1 da classe positiva, features esparsas
(<500 usuários) removidas como o artigo declara. `class_weight='balanced'`.

| família (features de 2012) | F1 medido | F1 do artigo | Δ |
|---|--:|--:|--:|
| **participação (homofilia)** | **34,6%** ±0,2 | 34,8% | **−0,2 p.p.** |
| participação + scores | 34,1% ±0,3 | 35,3% | −1,2 p.p. |
| scores (feedback social) | 32,4% ±0,5 | 33,7% | −1,3 p.p. |
| **interações (influência direta)** | **26,8%** ±0,7 | 26,7% | **+0,1 p.p.** |
| baseline aleatório | 15,6% | 15,2% | +0,4 p.p. |

**MH1 = REPRODUZ.** A afirmação do artigo é uma *ordenação* — homofilia ≈ feedback ≫
influência direta — e ela sai idêntica, com as duas pontas a **menos de 0,25 p.p.** do
publicado. Precisão/recall do melhor modelo também batem: **0,25 / 0,54** contra
**0,27 / 0,56** do artigo.

**Uma divergência pequena, registrada:** no artigo o melhor modelo é
*participação+scores* (35,3%); aqui *participação sozinha* fica marginalmente à frente
(34,6% × 34,1%). A diferença é da ordem do desvio entre folds (±0,2–0,3), e a causa mais
provável é a **seleção de features** — ver §3.

**AUC:** 0,671 (participação) contra **0,70** do melhor modelo do artigo. É a maior
distância do conjunto, e aponta para o mesmo lugar: seleção de features.

---

## 3. Divergências de método, declaradas

| o que o artigo faz | o que fizemos | efeito esperado |
|---|---|---|
| remove features esparsas (<500 usuários) | **igual** (766 → 360 em participação) | — |
| seleção por Pearson `p<0,05` **e VIF** | **não reproduzido** — não há limiar de VIF publicado | o nosso modelo tem **menos** seleção; explica AUC 0,67 × 0,70 e o combinado ficar abaixo |
| árvore e random forest além da logística | só **logística** (é a que o artigo reporta em Tab. 1–2) | nenhum, para MH1 |
| rebalanceamento não explicitado | `class_weight='balanced'`, escolhido **porque** reproduz o perfil precisão 0,27/recall 0,56 declarado | sem ele, o F1 desaba (8,2% em participação): a classe positiva é 15,8% e o modelo passa a quase nunca prever positivo |

> ⚠ O achado do `sem peso` merece registro próprio: **a mesma família de features dá F1
> 34,6% ou 8,2% conforme o rebalanceamento** — um detalhe que o artigo não explicita.
> Não é crítica ao alvo (o perfil precisão/recall dele denuncia o rebalanceamento), mas é
> exemplo de decisão invisível que domina o resultado publicado.

---

## 4. O que isto libera

O ponto de partida está **fixado e conferido**, que é o pré-requisito da expansão:
qualquer mudança medida na Fase 3 é atribuível ao **estrato**, não a erro de reimplementação.

**Fase 3 (o "coletar mais"):** o estrato sub-coletado é o *focus group* — usuários com
**≥10 comentários em 2012 e ≥10 em 2016** nos 51 subreddits políticos. A pergunta do caso
é se a ordenação **sobrevive ao baixar esse limiar** (≥5, ≥3, ≥1), incluindo os usuários
periféricos que o filtro corta. Isso **exige os dumps de 2012 e 2016** (Arctic Shift /
Academic Torrents) — é o único passo pesado que resta, e não depende de VPN.

⚠ **Atualização (19/ago):** a Fase 3 **saiu do escopo** da entrega de 31/ago — ver §6.
O parágrafo acima descreve o desenho, que continua válido para depois da defesa.

**Predição pré-registrada, antes de baixar dump nenhum (18/ago/2026):** a ordenação
*inverte parcialmente* — homofilia cai mais que influência ao incluir periféricos, porque
participação é feature **densa em quem posta muito** e vira esparsa na cauda, enquanto
interação direta já é esparsa nos dois regimes. Aposta: a distância 34,6 − 26,8 = **7,8
p.p. encolhe para menos de 4 p.p.** no limiar ≥1. *(Se falhar, reportar — princípio §7.)*

---

## 5. Linhas na tabela mestre

Este resultado preenche a coluna *"o ponto original replica?"* da **linha 12**
(reddit-massachs / homofilia) de [`RESULTADOS_tabela_mestre.md`](../../../../RESULTADOS_tabela_mestre.md):
**replica** (Δ ≤ 0,25 p.p. nas duas pontas da ordenação). As colunas *mudou?* e
*convergiu?* ficam **declaradas como não executadas** na versão de 31/ago, com o motivo
em §6 — não são um ⏳ que a sessão seguinte resolve.

---

## 6. ⛔ A Fase 3 não é dimensionável pela API — beco documentado (19/ago/2026)

Para saber quanto custaria a expansão (todos os comentários dos 34 subreddits políticos
em 2012 e 2016), tentou-se o endpoint de **agregação** do Arctic Shift, que devolve
contagem exata sem baixar itens. Duas rodadas:

| tentativa | método | resultado |
|---|---|---|
| 1ª | uma consulta por subreddit-ano | **20 de 34 falharam** (timeout nos grandes: `politics`, `news`, `worldnews`, `atheism`…) |
| 2ª | **mês a mês** (12 consultas por ano) | **34 de 34 incompletos** |

⚠ **A 1ª rodada produziu um número falso** — o script somava os que respondiam e
imprimia "universo da Fase 3: 2.272.918 comentários; 7 horas de API". Não era o
universo: era a soma dos que não falharam. **Corrigido**: a contagem agora é mês a mês e
o script **se recusa a imprimir total** quando há qualquer falha, gravando
`COMPLETO: false` no JSON. A 2ª rodada, com o script corrigido, falhou honestamente.

**Leitura:** o endpoint de agregação não sustenta subreddits do porte de `r/politics`
em janelas longas, e a estratégia mês a mês transforma qualquer falha isolada em falha
do subreddit inteiro. Pode ser limitação de taxa acumulada das tentativas anteriores;
pode ser limite do serviço. Não foi investigado além disso — ver abaixo.

> ⚠ **Atualização de 22/ago/2026 — a dúvida acima foi parcialmente resolvida, e em
> desfavor desta leitura.** O caso [`reddit-topicos`](../../../../reddit-topicos/README.md),
> ao dimensionar outros 13 subreddits no mesmo endpoint, mediu que a mensagem
> `"Timeout. Maybe slow down a bit"` aparece por **duas** causas que ela não distingue:
> **estrangulamento por taxa** (um subreddit de 222 submissões falhou sob uso intenso e
> respondeu bem após **~5 min de silêncio**) e **tamanho real da consulta** (um
> subreddit grande falhou em 14 s mesmo após silêncio total). Ou seja: **as duas
> hipóteses levantadas aqui são verdadeiras ao mesmo tempo**, e uma sonda que insiste
> rápido converte estrangulamento em algo que parece limite de serviço.
>
> **O que isso muda, e o que não muda.** Não muda a decisão: `politics`, `news` e
> `worldnews` são grandes, e para grandes a falha é real. Mas o **"34 de 34"** pode
> estar **inflado** — a 2ª rodada rodou logo depois da 1ª, sem recuo entre elas, que é
> exatamente a receita do estrangulamento. **Antes de a dissertação afirmar em
> definitivo que a expansão do Massachs não é dimensionável pela API, vale uma
> reconferência paciente** (uma consulta por vez, com ≥5 min de folga). Registrado em
> [ESTADO.md §4.23](../../../../../ESTADO.md).

**Decisão:** a Fase 3 do Massachs **fica fora do escopo** da versão de 31/ago/2026. O
caminho realista é o **dump por subreddit no Academic Torrents** (para o qual o próprio
Arctic Shift aponta), que é download pesado e não cabe no prazo.

**O que o caso entrega assim mesmo:** o ponto original replicado (§2), que é resultado
fechado e suficiente para a linha 12 da tabela mestre na coluna *"o ponto original
replica?"*. As colunas *mudou?* e *convergiu?* ficam declaradas como não executadas,
com o motivo registrado aqui.
