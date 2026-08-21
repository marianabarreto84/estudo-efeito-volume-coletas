# Codebook do eixo *stance* (EA / ED / NDA) — guia de rotulagem

> **Para quem vai rotular à mão.** Este é o guia operacional; o contexto de *por que*
> isso existe está em [STANCE_como_o_paper_fez_e_onde_estamos.md](STANCE_como_o_paper_fez_e_onde_estamos.md).
> Gerado em **18/ago/2026**, a partir do método do artigo (Ituassu & Lifschitz 2015,
> §*análise de sentimento*) e do fluxo já validado no caso vacinas
> (κ 0,759 — ver [DECISOES_ROTULADOR.md](../vacinas/data/repl/vacinas2022/DECISOES_ROTULADOR.md)).
>
> **Planilha:** `data/repl/compos2014/stance/gold_stance_para_rotular.csv` (320 linhas).
> **Regra de ouro:** na dúvida entre um lado e NDA, **é NDA** — e ponha `confianca=1`.

---

## 0. O que você preenche

Quatro colunas, no fim da planilha. As demais são contexto — não mexa nelas.

| Coluna | Valores | O que é |
|---|---|---|
| `cidadao` | `S` / `N` / `?` | a conta é de um **cidadão comum**? (Camada 0 do artigo) |
| `stance` | `EA` / `ED` / `NDA` | preferência eleitoral expressa **neste tweet** |
| `confianca` | `3` / `2` / `1` | 3 = óbvio · 2 = inferência razoável · 1 = chute informado |
| `notas` | texto livre | só quando algo não coube nas regras (ver §6 os códigos sugeridos) |

⚠ **Preencha `stance` sempre, inclusive quando `cidadao=N`.** O artigo descartava os
não-cidadãos antes de rotular; nós rotulamos os dois para poder medir **o recorte dele e
o universo inteiro** com o mesmo gabarito. Não custa mais e não dá para recuperar depois.

---

## 1. Camada 0 — a conta é de um cidadão comum?

O artigo só analisou **"perfis individuais"** (dos 700 tweets, **666**). Marque `N` para:

- **veículo de imprensa** e seus perfis-satélite (@g1, @folha, @VEJA, @jornaloglobo, @aovivozh…);
- **empresa / marca / agência** (inclusive publicidade e mídia exterior, ex. @elemidia);
- **órgão público, partido, campanha oficial, candidato** (@AecioNeves, @dilmabr, @PTbrasil);
- **agregador automático / bot** (só manchete + link, dezenas por dia, sem 1ª pessoa);
- **ativismo organizado com marca própria** (páginas/movimentos, não pessoas físicas).

Marque `S` para pessoa física, mesmo militante, mesmo com nome fantasia.
Marque `?` quando o handle não decide e o texto não ajuda.

**Colunas que ajudam:** `verificado` (1 = selo; quase sempre não-cidadão em 2014),
`seguidores`, `tweets_do_autor` (volume anormal sugere conta institucional/bot),
`nome_autor`.

> ⚠ **Assimetria declarada com o artigo:** eles viram *"algo no ícone do usuário"*
> (foto/avatar). Avatares de 2014 **não existem mais**. Onde eles tinham a foto, nós temos
> só handle + nome + métricas. Registrado como limite, não como falha.

---

## 2. Camada 1 — sinal explícito de lado

Se o tweet traz uma hashtag (ou expressão) que **já declara o lado**, o rótulo sai daí.

| Sinal | Lado |
|---|---|
| `#Dilma13`, `#EuVotoDilma13`, `#MelhorComDilma13`, `#QueroDilmaTreze`, `#SomosTodosDilma`, `#13rasilTodoComDilma`, `#DilmaEMichel13` | **ED** |
| `#Aecio45`, `#Aecio45PeloBrasil`, `#EAecio45Confirma`, `#EuVotoAecio45`, `#VotoAecioPeloBR45il`, `#AecioPresidente`, `#ForaDilma`, `#ForaPT` | **EA** |
| **`#AecioNever`** | **ED** ⚠ ver o aviso abaixo |

> ⚠ **Corrigindo um erro da nossa própria documentação.** O artigo cita
> *"#Aécionever ou #ForaDilma"* como exemplos de sinal explícito **sem dizer de que lado
> cada uma está**; o nosso `STANCE_...md` glosou as duas como "contra Dilma → EA". É
> falso para a primeira: *"Aécio never"* = **nunca Aécio**, logo **pró-Dilma**. Medido:
> nas 157 ocorrências da janela, ela co-ocorre **84×** com hashtags declaradamente
> pró-Dilma e **0×** com pró-Aécio (`analise/lean_hashtags.py`).

**Não use as hashtags de tema como sinal** (`#G1`, `#DebateNaGlobo`, `#Ibope`, `#Veja`,
`#Datafolha`, `#Politica`, `#Brasil`): elas são temáticas. Ainda que na janela apareçam
mais de um lado, isso é composição do público — não é declaração de quem posta.
O apêndice §7 traz a tabela medida; ela é **contexto, não regra**.

---

## 3. Camada 2 — o tom (a regra central do artigo)

Quando não há sinal explícito, vale a regra do artigo, **literal**:

> - conteúdo (texto ou link) **negativo** a um candidato/campanha/partido → eleitor do **adversário**;
> - conteúdo **positivo** a um candidato/campanha/partido → eleitor **dele**;
> - não dá para decidir, ou é apolítico → **NDA**.

Equivalências: **Dilma ≡ PT ≡ Lula ≡ governo/Petrobras-como-ataque** ↔ atacar isso ⇒ **EA**.
**Aécio ≡ PSDB ≡ FHC ≡ governo tucano de MG/SP** ↔ atacar isso ⇒ **ED**.

### Os exemplos do próprio artigo (gabarito de raciocínio)

| Tweet | Rótulo | Por quê |
|---|---|---|
| "32 capas de jornal que vão te lembrar do Brasil dos anos 90 e governo FHC" | **ED** | negativo ao lado do Aécio |
| vídeo do cachorro que late em "Dilma" e brinca em "Aécio" | **EA** | piada negativa a Dilma |
| "DILMA JÁ FOI ENQUADRADA. ELA SABIA DE TUDO SIM" + capa da *Veja* | **EA** | ataque direto a Dilma |
| "Vc aí falando de Aécio e Dilma... Ruim mesmo é o Chico Buarque!!!" | **NDA** | apolítico, não toma lado |
| "Cansado dessa ladainha entre DILMA x AECIO! que passe logo esse domingo" | **NDA** | reclama dos dois |

---

## 4. Casos-limite — as decisões que o artigo não tomou

O artigo não diz o que fazer nestes casos. Nós decidimos, e a decisão vale para o
gabarito humano **e** para o rotulador automático (é isso que torna o κ interpretável).

| # | Caso | Decisão | Nota |
|---|---|---|---|
| **1** | **RT sem comentário** (`eh_retweet=1`, texto começa com `RT @x:`) | o stance é **do retuitador**, e retuitar **é endosso** — rotule pelo conteúdo retuitado | é o que o artigo faz (o exemplo 3 dele é um RT) |
| **2** | **RT com comentário** que contradiz o conteúdo (ironia, "olha o absurdo") | vale o **comentário**, não o conteúdo | `nota=rt_ironico` |
| **3** | **Notícia neutra sem valência** ("Ibope: Dilma 53%, Aécio 47%") | **NDA** | número de pesquisa não é torcida, mesmo que favoreça alguém |
| **4** | Notícia neutra **com** comentário valorado ("53%! 🎉") | vale o comentário | |
| **5** | **Apoio a terceiro** (Marina, PSOL, nulo/branco) | **NDA** | `nota=terceiro` — não decide *entre os dois* |
| **6** | **Ironia / sarcasmo** | julgue pelo **alvo** da ironia; se não der, **NDA** com `confianca=1` | |
| **7** | **Idioma não-pt** (~4,5% da janela) | se entender, rotule normalmente; se não, **NDA** | `nota=idioma` |
| **8** | **Link morto/opaco** (`t.co` sem host resolvido) e texto que não decide | **NDA** | `nota=link_morto` ⚠ ver aviso |
| **9** | **Conta institucional com lado óbvio** (campanha, militância orgânica) | `cidadao=N` **e** o stance real | não deixe `stance` em branco |
| **10** | **Crítica à mídia** ("Veja é lixo", "Globo golpista") | ataque à *Veja*/Globo em 2014 = ataque ao antipetismo ⇒ **ED**; ataque a "mídia chapa-branca"/EBC ⇒ **EA** | `confianca` ≤ 2 |
| **11** | Tweet só com hashtags dos **dois** lados (spam de tags) | **NDA** | `nota=spam_tag` |
| **12** | **Duplicata** — você reconhece um texto já rotulado | rotule **de novo**, do mesmo jeito, sem procurar o anterior | ver §5 |

> ⚠ **Link morto é a maior assimetria com o artigo.** Em 2014 os anotadores **abriram**
> os links; em 2026 a maioria dos `t.co` está morta. Da amostra, **219 de 320 (68%)** têm
> link, e o host final está resolvido em todos eles — mas *host* não é *conteúdo*.
> Quando o host já decide (ex.: `blogdodilmiro`, `revistaforum`, `veja.abril`), use-o;
> quando não, o caso 8 manda NDA. Isso **por construção infla o NDA** em relação ao
> artigo: é um viés conhecido, com direção conhecida, e tem de ser dito no capítulo.

---

## 5. Duplicatas e reteste

- Na amostra, **320 tweets** correspondem a **259 textos distintos**: 90 itens estão em
  grupo repetido (RTs do mesmo original). Isso é **peso real no universo** e por isso
  ficou. Consequência: o κ será reportado **com e sem** deduplicação, porque duplicata
  infla concordância artificialmente.
- **Não procure** o que você rotulou antes ao reencontrar um texto. Se você "corrige" o
  anterior, destrói a medida de consistência.
- A planilha `gold_stance_RETESTE.csv` (40 itens, já sorteados) é para ser preenchida
  **pelo menos 7 dias depois** da primeira rodada, sem consultar a primeira. Ela mede o
  **teto da tarefa**: nenhum rotulador automático pode passar da consistência do próprio
  humano consigo mesmo. (No caso vacinas esse teto deu **0,746**.)

---

## 6. Códigos sugeridos para `notas`

`rt_ironico` · `terceiro` · `idioma` · `link_morto` · `spam_tag` · `conta_dupla` ·
`nao_entendi` · qualquer texto livre. São para triagem depois, não é obrigatório.

---

## 7. Apêndice — lado das hashtags medido nos dados (contexto, **não** regra)

Fonte: `analise/lean_hashtags.py` → `data/repl/compos2014/stance/lean_hashtags.json`.
Método: co-ocorrência com sementes de lado auto-evidente, na janela 19–25/out.
"Lado X, p%" = entre os tweets em que a hashtag aparece com sementes de **um só** lado,
p% eram desse lado.

| hashtag | total | lado medido |
|---|--:|---|
| `#aecionever` | 157 | **ED 100%** (84 × 0) |
| `#desesperodaveja` | 128 | **ED 100%** |
| `#pt` | 519 | ED 65% ⚠ mista |
| `#vemprarua25deoutubro` | 395 | **EA 100%** |
| `#mudabrasil` | 383 | **EA 100%** |
| `#acordabrasil` | 149 | **EA 100%** |
| `#corrupcao` | 90 | **EA 100%** |
| `#aecio`, `#aecioneves`, `#lula` | 1.322 / 190 / 339 | EA 93–96% |
| `#g1`, `#debatenaglobo`, `#brasil`, `#dilma` | — | EA 61–85% ⚠ **temáticas, não use** |
| `#ovotonarecord`, `#hojeemdia`, `#veja`, `#ibope`, `#datafolha`, `#politica` | — | sem lado detectável |

⚠ **Por que "contexto, não regra":** se este apêndice virar regra tanto no gabarito
humano quanto no rotulador automático, os dois concordam por usarem a mesma heurística —
e o κ mede a heurística, não a validade. Use-o para desempatar, nunca no lugar de ler.
Registrado como risco em
[PRE_REGISTRO_stance.md](data/repl/compos2014/stance/PRE_REGISTRO_stance.md) §5.
