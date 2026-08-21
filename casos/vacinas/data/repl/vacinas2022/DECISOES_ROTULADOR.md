# Diário de decisões do rotulador (eixo B — conteúdo/framing)

> Registro corrido de **toda** escolha de método do rotulador automatizado:
> o que foi decidido, por quê, com que evidência, e o que foi **rejeitado**.
> Serve para a seção de método da dissertação e para a arguição na banca —
> onde a pergunta não será "qual foi o κ" e sim "por que o prompt é esse".
>
> Regra: nada de mudança de prompt sem uma linha aqui. Cada versão do prompt
> (`p1`, `p2`, …) tem seu bloco, com o κ que a motivou e o κ que produziu.
>
> Artefatos irmãos: `CODEBOOK.md` (o que se rotula), `PRE_REGISTRO_split.md`
> (onde se mede), `VALIDACAO.md` de cada rodada (quanto deu).

---

## D0. Decisões estruturais (26/jul/2026, antes de qualquer chamada)

### D0.1 — Rotulador por LLM, e não classificador supervisionado

**Decisão:** opção A do `EIXO_CONTEUDO.md` (Claude Haiku 4.5), confirmada pela
Mariana.

**Por quê:** o gargalo é o κ contra o gabarito humano, e 1.525 exemplos para
12+ rótulos é pouco para treinar um classificador — as categorias raras
(Religion n=46, Other drugs n=32) não têm massa. O custo do LLM é irrisório no
escopo do E1.

**Rejeitado:** opção B (embeddings + regressão logística). A inadequação dela
é, ela mesma, um dado a favor da tese: análises compostas exigem mais dados do
que parece.

**Em aberto:** a opção C (híbrida, B como robustez) segue possível se sobrar
cronograma.

### D0.2 — 14 categorias, não 11

**Decisão:** usar as **14** categorias amplas numeradas no material suplementar.

**Evidência:** o corpo do preprint fala em 11 categorias; a aba
`Table broad categories` numera 14. Os 14 totais da coluna agregada batem
**exatamente** com a Tabela 5 publicada (conferência automática em
`extrai_codebook.py`, que aborta se divergir).

**Por quê:** princípio do projeto — se o texto diverge dos dados, os dados
vencem. Sinalizado à Mariana.

### D0.3 — Teto de gasto de US$ 25, em três camadas

**Decisão:** teto rígido de US$ 25, exigido explicitamente pela Mariana.

| Camada | Onde | Força |
|---|---|---|
| Saldo pré-pago de US$ 25 sem recarga automática | conta Anthropic | **rígida** — o servidor recusa |
| Reserva-antes-de-enviar (pior caso) | `core/orcamento.py` | bloqueia o lote antes do envio |
| Livro-caixa persistente | `gastos_llm.json` | sobrevive a reinício do script |

**Por quê três:** nenhum código em Python impede uma chamada que já saiu. Só o
servidor impede. As camadas 2 e 3 são defesa em profundidade, não substituto —
e a reserva usa o **pior caso** (saída inteira em `max_tokens`), então o gasto
real fica sempre abaixo do reservado; o teto nunca é furado por subestimativa.

**Ressalva registrada:** se a recarga automática for ligada na conta, a camada
1 evapora sem aviso.

### D0.4 — Modelo pinado, temperatura 0, brutos em disco

**Decisão:** `claude-haiku-4-5-20251001` (ID datado, não alias), `temperature=0`,
saída JSON estruturada por schema, requests e respostas brutas salvos.

**Por quê:** reprodutibilidade é o calcanhar de Aquiles do rotulador por LLM.
Mitigação: modelo pinado + prompt versionado + brutos em disco + **rótulos
congelados no snapshot**. Quem replicar a dissertação usa os rótulos
publicados; re-rodar o LLM é verificação extra, não requisito.

**Consequência:** trocar de modelo invalida o κ medido. Refazer a validação.

### D0.5 — 10 tweets por chamada

**Decisão:** agrupar 10 tweets por request (`--por-chamada 10`).

**Por quê:** é o que faz o escopo completo do E1 caber no teto. O system
prompt (~1.000 tokens) é amortizado 10×.

**Correção a uma premissa da §2 do `EIXO_CONTEUDO.md`:** a estimativa original
de US$ 15–20 assumia *cache* do system prompt. **Não haverá cache** — o mínimo
cacheável do Haiku 4.5 é 4.096 tokens e o nosso prompt tem ~1.000. A economia
vem do agrupamento, não do cache.

**Risco assumido:** agrupar pode degradar a qualidade por diluição de atenção.

**Em aberto:** comparar `--por-chamada 1` contra `10` no dev (custa ~US$ 0,35)
e deixar o κ decidir, em vez de decidir por custo. **Ainda não feito.**

### D0.6 — Split dev/teste congelado antes da primeira chamada

**Decisão:** 506 dev / 1.019 teste, seed `20260726`, estratificado por
stance × categoria mais rara presente. Congelado **antes** de qualquer chamada
de API; `congela_split.py` se recusa a rodar de novo sem `--refazer`.

**Por quê a estratificação dupla:** num sorteio simples, Religion (n=46) e
Other drugs (n=32) poderiam sumir de um dos lados — e são justamente onde o
rotulador tem mais chance de falhar. Amarrar pela categoria mais rara garante
os dois lados. Estratos de tamanho 1 vão inteiros para o teste (não se gasta
raridade em calibração).

**Por quê antes:** sem isso, o κ reportado mede overfitting ao próprio teste.

### D0.7 — Critério de aceite registrado antes de medir

κ do stance ≥ 0,70 **e** mediana dos κ das 14 categorias ≥ 0,60, medidos **uma
única vez** no teste cego. Registrado em `PRE_REGISTRO_split.md` junto com a
aposta pré-registrada.

---

## D1. Prompt `p1` — versão inicial

**SHA-256 (12):** `dfa44ec92416` · **Rodada:** `rotulos_llm/dev_p1/`

### Decisões de construção

| # | Decisão | Motivo |
|---|---|---|
| D1.1 | Instruções em PT, **nomes e definições de categoria em inglês** (idênticos ao suplemento) | traduzir introduziria deriva semântica justamente no que está sendo medido |
| D1.2 | Subcategorias entram no prompt | são elas que delimitam a fronteira; sem elas o modelo inventa a sua |
| D1.3 | Saída = número das categorias, não 14 booleanos | o token de saída custa 5× o de entrada; o formato não muda a tarefa |
| D1.4 | Rótulo informativo extraído da **coluna** quando os nomes refinados colidem | em `International` (35 países) e `Vaccines/labs` (11 laboratórios) o nome refinado é uniforme e quem distingue é a coluna; sem isso o prompt dizia "Vaccine labs" 11 vezes seguidas |

### Resultado no dev (n=506) — **REPROVADO**

| Métrica | Valor | Aceite | |
|---|---:|---:|---|
| κ stance | 0,714 | 0,70 | passou raspando |
| mediana κ categorias | **0,599** | 0,60 | **reprovou por 0,001** |

Custo: US$ 0,083.

### Diagnóstico (quatro defeitos, todos do prompt)

**P1-a — refúgio no "nenhum".** O modelo usou `nenhum` 26× em 506; o gabarito
do dev tem **zero**. A p1 já *avisava* que a saída era rara ("apenas 3 de
1525") e ainda assim ele se refugiou nela. Lição: anunciar que uma saída é
rara não impede o modelo de usá-la como escape para o caso difícil — é preciso
estreitar a *condição de uso*, não informar a frequência.

**P1-b — sub-marcação sistemática.** Em 12 das 14 categorias, `n_llm < n_ouro`:

| Categoria | gabarito | modelo | κ |
|---|---:|---:|---:|
| Information sources | 59 | 20 | 0,42 |
| Anti-vaccine people | 129 | 55 | 0,42 |
| Politics | 245 | 178 | 0,59 |
| International | 83 | 47 | 0,67 |
| Misinformation sources | 71 | 42 | 0,26 |

Causa: a instrução da p1 ("marque só quando efetivamente mencionado, não
quando apenas plausível") calibrou um limiar mais conservador que o dos
codificadores humanos, que são generosos.

**P1-c — categorias 9 e 10 se canibalizando.** `Misinformation sources`
(κ=0,26, a pior de todas) e `Information sources` (κ=0,42) são vizinhas e a p1
não as distinguia: a 9 saiu **sem cláusula explicativa nenhuma** (é atômica no
suplemento) e a 10 só dizia "Social media; Official media".

**P1-d — `Advantages of vaccines`: contagem certa, tweets errados.** 77 no
gabarito contra 80 no modelo, mas κ=0,34. Ao conferir o codebook: os autores
puseram a subcategoria "Misinformation on vaccine risks" **dentro** de
Advantages, e não em Misinformation. Não é adivinhável.

---

## D2. Prompt `p2` — quatro correções de fronteira

**Rodada:** `rotulos_llm/dev_p2/` · **Motivada por:** D1 acima.

| # | Correção | Responde a |
|---|---|---|
| D2.1 | `nenhum` passa a ter condição de uso explícita e estreita ("não use como saída para o caso difícil"), sem citar frequência | P1-a |
| D2.2 | Política de marcação **invertida para inclusiva**: "na dúvida, MARQUE" | P1-b |
| D2.3 | Fronteira 9 × 10 explicitada nos dois sentidos (9 = a desinformação enquanto tal; 10 = o veículo enquanto tal) | P1-c |
| D2.4 | Nota em 7 avisando que "desmentir desinformação sobre riscos" pertence a Advantages | P1-d |

### **Rejeitado: informar as taxas-base das categorias**

A correção mais fácil para P1-b seria dizer ao modelo a frequência de cada
categoria ("Politics aparece em ~48% dos tweets"). **Rejeitada por
contaminação experimental.**

As taxas-base viriam do estrato >500 RT. O objetivo inteiro do E1 é **descer o
limiar até >10 RT**, onde a distribuição temática pode ser outra — é
exatamente isso que o experimento pretende medir. Embutir as taxas do estrato
original no rotulador faria o rotulador *impor* a distribuição de >500 RT ao
estrato novo, e a Fase 3 então "descobriria" que a distribuição se manteve.
Seria circular: o achado estaria escrito no instrumento.

Corrige-se por **definição de fronteira**, nunca por *prior* de frequência.

> Vale como regra geral para o eixo B: nenhuma informação derivada da
> distribuição do estrato de validação entra no prompt.

### Resultado no dev (n=506) — **aprovado por 0,002**

**SHA-256 (12):** `7e011852f2a0` · Custo: US$ 0,091.

| Métrica | p1 | p2 | Aceite | |
|---|---:|---:|---:|---|
| κ stance | 0,714 | **0,738** | 0,70 | passou |
| mediana κ categorias | 0,599 | **0,602** | 0,60 | passou **por 0,002** |

> ⚠️ **Aprovação frágil, e no conjunto onde se calibrou.** A mediana de 14
> valores é a média do 7º e 8º ordenados — aqui, Politics (0,593) e
> Information sources (0,611). Um deslize de 0,01 em qualquer um dos dois
> derruba o critério. E o teste cego, por não ter calibração, tende a vir
> **abaixo** do dev. Tratar como "passou" seria enganar a nós mesmas.

### Placar por correção — duas funcionaram, uma não pegou, uma foi nula

| Correção | Alvo | p1 → p2 | Veredito |
|---|---|---|---|
| D2.1 (`nenhum`) | stance | κ 0,714 → **0,738**; uso de `nenhum` 26 → 14 | ✅ funcionou (não zerou) |
| D2.3 (fronteira 9×10) | cat 9, 10 | 9: 0,259 → **0,378** · 10: 0,422 → **0,611** | ✅ a mais eficaz |
| D2.2 (marcação inclusiva) | sub-marcação geral | 1.000 → 1.059 marcações (gabarito: **1.311**) | ⚠️ mexeu pouco |
| D2.4 (nota na cat 7) | cat 7 | κ **0,344 → 0,344**; 40 predições mudaram | ❌ nula |

**D2.4 é o achado mais instrutivo:** a nota mudou 40 predições e o κ ficou
idêntico à terceira casa — trocou ~20 acertos por ~20 erros. Uma nota de
fronteira reposiciona o modelo sem necessariamente aproximá-lo do gabarito.
**Mudança de comportamento não é evidência de melhora**; só o κ é.

### Efeitos colaterais (a p2 piorou 5 categorias)

| Categoria | p1 | p2 | |
|---|---:|---:|---|
| Vaccines type or laboratories | 0,773 | 0,654 | agora **super**-marca (28 gabarito → 40) |
| Other drugs | 0,619 | 0,527 | |
| Religion | 0,564 | 0,492 | |
| International | 0,668 | 0,636 | |
| Children | 0,907 | 0,889 | |

A instrução global "na dúvida, MARQUE" (D2.2) não é neutra: ela empurra as
categorias já bem calibradas para a super-marcação. Instruções globais têm
custo distribuído — lição para a p3.

---

## D3. Hipótese para a `p3` — categorias agregadas são *extensionais*

**Diagnóstico do erro residual dominante.** A sub-marcação persiste depois da
D2.2 (1.059 contra 1.311 marcações do gabarito, ~19% a menos) e está
concentrada:

| Categoria | gabarito | p2 | faltando |
|---|---:|---:|---:|
| Politics | 245 | 177 | **68** |
| International | 83 | 44 | 39 |
| Anti-vaccine people | 129 | 95 | 34 |
| Information sources | 59 | 37 | 22 |
| COVID risks | 75 | 52 | 23 |
| Disadvantages of vaccines | 126 | 105 | 21 |

**Hipótese:** o problema não é limiar, é **natureza da categoria**. As colunas
agregadas do gabarito são `OR` de dezenas de subcategorias concretas —
`All_Category_1_Politics` dispara com menção a Bolsonaro, ao governo federal,
a senadores, a governos regionais, a Lula, ao PT, ao judiciário, à corrupção,
ao lobby, ao Ministério da Saúde, à Anvisa, ao SUS… O gabarito humano marca
**extensionalmente** ("cita algum destes?"), enquanto o modelo está julgando
**intensionalmente** ("este tweet *é sobre* política?"). Um tweet sobre
vacinação infantil que menciona a Anvisa de passagem é "Politics" para o
gabarito e não é para o modelo.

Se a hipótese estiver certa, mandar "marcar mais" não resolve — está pedindo
ao modelo que baixe o limiar do juízo errado.

**Proposta p3:** reescrever as categorias agregadas como **listas de gatilho
extensionais** ("marque se o tweet citar qualquer um: Bolsonaro, governo
federal, senadores/deputados, governos estaduais, Lula, PT, judiciário,
corrupção, lobby, Ministério da Saúde, Anvisa, SUS…"), em vez de nome de tema
+ lista de subcategorias em prosa. E **remover** a instrução global "na dúvida
MARQUE" (D2.2), cujo efeito colateral está documentado acima — a inclusão
passa a vir da definição de cada categoria, não de um empurrão global.

### Resultado no dev (n=506) — **melhor rodada até aqui**

**SHA-256 (12):** `380f49882a55` · Custo: US$ 0,094.

| Métrica | p1 | p2 | **p3** | Aceite |
|---|---:|---:|---:|---:|
| κ stance | 0,714 | 0,738 | 0,735 | 0,70 |
| mediana κ categorias | 0,599 | 0,602 | **0,621** | 0,60 |

As duas previsões declaradas **antes** de rodar se confirmaram:

- **Politics 0,593 → 0,677** e **International 0,636 → 0,690** — as duas
  categorias mais extensionais subiram, como previsto pela hipótese D3.
- **Religion voltou a 0,564** (exatamente o valor da p1) e **Other drugs foi a
  0,839** (de 0,527) — confirma que o dano nessas era da instrução global
  "na dúvida MARQUE", e não da definição.

Mas **7 categorias pioraram**, e o total de marcações *caiu* (900, contra 1.059
da p2 e 1.311 do gabarito). A mediana subiu porque a precisão compensou a
recall perdida — não porque a sub-marcação foi resolvida.

### Diagnóstico: as listas de gatilho não são todas legítimas

Teste direto no gabarito — a lista de gatilhos que **vai para o prompt** cobre
a coluna agregada? (sobre os 1.525 tweets):

| # | Categoria | agregado | **órfãos** | lista é |
|---|---|---:|---:|---|
| 4 | Disadvantages of vaccines | 378 | 0 (0%) | **exaustiva** |
| 7 | Advantages of vaccines | 242 | 0 (0%) | **exaustiva** |
| 10 | Information sources | 179 | 0 (0%) | **exaustiva** |
| 12 | Vaccines type or laboratories | 86 | 0 (0%) | **exaustiva** |
| 1 | Politics | 719 | 24 (3%) | parcial |
| 6 | International | 253 | 40 (16%) | parcial |
| 3 | Restrictive policies | 531 | 91 (17%) | parcial |
| 5 | Anti-vaccine people | 375 | 125 (33%) | parcial |
| **2** | **Children** | **592** | **573 (97%)** | **parcial** |
| 8, 9, 11, 13, 14 | COVID risks, Misinformation, Science, Religion, Other drugs | — | 100% | atômicas |

> **Erratum (registrado de propósito).** A primeira versão desta tabela
> reportava 7 órfãos em Politics, 5 em Restrictive e 4 em Anti-vaccine people.
> Estava errada: o `OR` fora calculado incluindo as colunas **agregadas**
> (`About_All_…`), que por construção cobrem quase tudo e **não entram no
> prompt**. Media-se a cobertura de uma lista diferente da que o modelo recebe.
> Os números acima excluem os agregados e correspondem à lista real. A direção
> da conclusão não mudou, mas o suporte era menor do que eu havia dito — e é
> consistente: Politics (3% de fora) ganhou 0,08 de κ com a lista, enquanto
> Anti-vaccine people (33% de fora) ficou parada (0,510 → 0,487).
>
> Correção estrutural: o diagnóstico agora roda **dentro** do
> `rotula_conteudo.py`, sobre exatamente a mesma lista que compõe o prompt
> (`diagnostico_cobertura()` reaproveita o mesmo filtro `_e_rollup`). Os dois
> não podem mais divergir.

**Children é o contraexemplo que explica a perda.** A coluna agregada é
`About_all_Children` — qualquer menção a crianças — mas as únicas
subcategorias listadas tratam de *prescrição médica para crianças*: cobrem
115 dos 592. A lista de gatilhos da p3 **estreitou** a categoria para 19% do
que ela é. κ caiu 0,889 → 0,786.

**Conclusão refinada da hipótese D3.** A reformulação extensional não é boa nem
ruim em si; ela é boa **quando a lista é exaustiva** e ruim **quando é parcial**:

- lista exaustiva + entidades concretas (Politics, International, labs) → **ganho**;
- lista parcial (Children) → **perda**, por estreitamento;
- categoria atômica sem lista (COVID risks, Misinformation, Science) → **perda**,
  porque perdeu o empurrão global da D2.2 e não ganhou nada no lugar;
- exceção instrutiva: **Other drugs** não tem subcategoria, mas o *nome da
  própria coluna* (`About_OtherDrugs_CloroquinaORIvermectna`) carrega as
  entidades — minerar o nome da coluna rendeu κ 0,839.

---

## D4. Proposta — tratamento por tipo de categoria (não executada)

O erro das p2 e p3 foi o mesmo em direções opostas: **aplicar uma política
única a 14 categorias de naturezas diferentes.** A p2 empurrou todas para
marcar mais; a p3 transformou todas em listas. Cada uma acertou o subconjunto
que casava com a sua política e errou o resto.

Proposta: escolher a política **por categoria**, segundo o diagnóstico de
exaustividade acima — que é derivado dos dados, não da minha intuição.

| Tipo | Categorias | Tratamento |
|---|---|---|
| Lista exaustiva ou quase | 1, 3, 4, 5, 7, 10, 12 | lista de gatilhos da p3 (funcionou) |
| Lista parcial | 2, 6 | lista **+** cláusula de abertura ("e qualquer outra menção a …"), para não estreitar |
| Atômica com entidade no nome | 14 | mineração do nome da coluna (funcionou: 0,839) |
| Atômica sem entidade | 8, 9, 11, 13 | enquadramento temático **+** empurrão de inclusividade *escopado nelas*, em vez de global |

### Resultado no dev (n=506) — **melhor em ambas as métricas**

**SHA-256 (12):** ver `dev_p4/execucao.json` · Custo: US$ 0,099.

| Métrica | p1 | p2 | p3 | **p4** | Aceite |
|---|---:|---:|---:|---:|---:|
| κ stance | 0,714 | 0,738 | 0,735 | **0,755** | 0,70 |
| mediana κ categorias | 0,599 | 0,602 | 0,621 | **0,646** | 0,60 |
| marcações totais (gabarito: 1.311) | 1.000 | 1.059 | 900 | **1.095** | — |

**Previsão minha que falhou:** eu havia registrado que, com quase toda
categoria recebendo cláusula de abertura, a p4 tenderia a "se aproximar da p2".
Não se aproximou — ficou 0,044 acima dela. A diferença entre uma cláusula de
abertura *ancorada em gatilhos concretos e escopada por categoria* e um
"na dúvida MARQUE" *global* é maior do que eu supunha. Fica o registro.

O tratamento por tipo recuperou exatamente o que cada política anterior havia
quebrado:

| Categoria | tipo | p3 → p4 | o que resolveu |
|---|---|---:|---|
| Children | parcial | 0,786 → **0,881** | cláusula de abertura desfez o estreitamento |
| COVID risks | atômica | 0,511 → **0,640** | empurrão escopado nas atômicas |
| Restrictive policies | parcial | 0,690 → **0,729** | cláusula de abertura |
| Anti-vaccine people | parcial | 0,487 → **0,528** | cláusula de abertura |
| Other drugs | atômica c/ entidade | 0,839 → **0,887** | mineração do nome da coluna |

### Duas categorias resistem a tudo

- **Advantages of vaccines** (7): κ 0,344 → 0,344 → 0,373 → **0,271**. Quatro
  versões, nenhuma melhora, e é uma categoria **exaustiva** — a lista de
  gatilhos cobre 100% dela. A causa provável é a colocação de "Misinformation
  on vaccine risks" dentro de Advantages pelos autores: um tweet que desmente
  boato sobre risco de vacina é *Advantages* no gabarito, o que contraria a
  leitura natural. **Reportar como limitação do rotulador**, não insistir.
- **Misinformation sources** (9): 0,259 → 0,378 → 0,332 → 0,370. Teto baixo,
  provavelmente pela mesma fronteira com a 7.

**Status:** executada. p4 é a candidata a congelar.

### Sobre iterar no dev: quanto é legítimo?

Calibrar no dev é o uso correto do dev. Mas iterar **indefinidamente** contra
ele também é overfitting, só que ao conjunto de calibração: o prompt vai
absorvendo o ruído amostral dos 506. Três iterações com hipóteses declaradas
*antes* de rodar (como aqui) é defensável e reportável. Quinze rodadas de
tentativa e erro não seriam. **Registrar o número de iterações no texto da
dissertação**, junto com o κ.

---

---

## D5. CONGELAMENTO DO ROTULADOR (26/jul/2026)

**A `p4` está congelada.** Registrado **antes** de qualquer chamada ao conjunto
de teste, com aval explícito da Mariana. A partir daqui, nenhum ajuste de
prompt é feito olhando o teste — se o critério de aceite reprovar, as saídas
possíveis estão listadas abaixo, e "mexer no prompt" não é uma delas.

| Item | Valor congelado |
|---|---|
| Prompt | `p4` — `_prompt_p4()` em `pipeline/rotula_conteudo.py` |
| SHA-256 do system prompt | `e61365e316011705c3c638094d624f0fd1f0d118e24b4f6c0b60c615035f22fe` |
| Modelo | `claude-haiku-4-5-20251001` (ID datado, não alias) |
| Temperatura | 0 |
| Tweets por chamada | 10 |
| Codebook | `codebook_v1.json` (14 categorias) |
| Split | `split_dev_teste.csv`, seed `20260726` |
| Iterações no dev até aqui | **4** (p1 → p4), cada uma com hipótese declarada antes de rodar |
| κ no dev (p4) | stance 0,755 · mediana categorias 0,646 |

**Critério de aceite** (de `PRE_REGISTRO_split.md`, registrado antes de medir):
κ do stance ≥ 0,70 **e** mediana dos κ das 14 categorias ≥ 0,60, no teste cego,
**uma única vez**.

**Se reprovar** — as três saídas legítimas, nenhuma delas envolvendo o prompt:
1. trocar para um modelo mais capaz (Sonnet) e **revalidar do zero**, incluindo
   nova calibração no dev — o κ do Haiku não transfere;
2. reportar a reprovação e limitar o eixo B ao estrato já rotulado à mão pelo
   paper (>500 RT), sem descer o limiar;
3. voltar ao dev com uma hipótese nova — mas então o teste de hoje está
   queimado, e a validação final exigiria um terceiro conjunto.

---

## D6. TESTE CEGO — resultado (26/jul/2026, rodada única)

**APROVADO.** `rotulos_llm/teste_p4/` · n = 1.018 · custo US$ 0,199.

| Métrica | dev (p4) | **teste cego** | Aceite | |
|---|---:|---:|---:|---|
| κ de Cohen — stance | 0,755 | **0,759** | 0,70 | passou |
| mediana dos κ — 14 categorias | 0,646 | **0,650** | 0,60 | passou |
| acurácia do stance | 0,874 | 0,876 | — | |

**O teste veio ligeiramente ACIMA do dev** — 0,650 contra 0,646. O esperado era
o contrário (o dev é onde o prompt foi calibrado). A diferença é pequena o
bastante para ser ruído amostral, mas descarta a hipótese preocupante: se as
quatro iterações tivessem ajustado ruído do dev, o teste teria caído
visivelmente. Ajustaram estrutura.

### κ por categoria no teste cego

| # | Categoria | n gabarito | n LLM | κ |
|---|---|---:|---:|---:|
| 2 | Children | 398 | 354 | 0,874 |
| 14 | Other drugs | 22 | 19 | 0,826 |
| 3 | Restrictive policies | 362 | 335 | 0,758 |
| 6 | International | 170 | 116 | 0,757 |
| 12 | Vaccines type or laboratories | 58 | 81 | 0,730 |
| 4 | Disadvantages of vaccines | 252 | 191 | 0,704 |
| 1 | Politics | 473 | 420 | 0,664 |
| 8 | COVID risks | 166 | 165 | 0,636 |
| 9 | Misinformation sources | 130 | 79 | 0,518 |
| 5 | Anti-vaccine people | 245 | 191 | 0,506 |
| 13 | Religion | 31 | 12 | 0,503 |
| 10 | Information sources | 119 | 51 | 0,469 |
| 11 | Science | 63 | 103 | 0,400 |
| 7 | Advantages of vaccines | 165 | 135 | 0,376 |

### Limitações a declarar na dissertação

1. **`Advantages of vaccines` (κ=0,376) e `Misinformation sources` (κ=0,518)**
   resistiram a quatro versões de prompt. A causa provável é do codebook do
   paper, não do rotulador: os autores classificam "desmentir desinformação
   sobre riscos da vacina" como *Advantages*, contrariando a leitura natural,
   o que embaralha a fronteira entre as duas categorias. Conclusões que
   dependam **apenas** dessas duas categorias devem ser reportadas com ressalva.
2. **Sub-marcação residual.** O rotulador ainda marca menos que os
   codificadores humanos em quase toda categoria. Isso **atenua** diferenças
   entre estratos em vez de inflá-las — o viés joga contra a hipótese do E1,
   não a favor, o que é o lado seguro.
3. **A aposta pré-registrada acertou em parte.** Previu-se que o stance
   passaria folgado (passou: 0,759) e que as categorias raras ficariam abaixo
   do corte. Religion (n=31) de fato ficou em 0,503 — mas **Other drugs
   (n=22) deu 0,826**, o segundo melhor κ de todos, contrariando a previsão.
   Raridade sozinha não determina o κ: `Other drugs` é rara **e** lexicalmente
   inequívoca (cloroquina, ivermectina), enquanto `Information sources`, com
   n=119, ficou em 0,469 por ser semanticamente difusa. **É a nitidez lexical,
   não a frequência, que prediz o desempenho.** Isso refina o argumento da
   tese: o que a análise composta exige não é só mais dados, é fronteira
   conceitual nítida.

### Falha operacional registrada

Um tweet (id `539`) ficou sem rótulo: o modelo devolveu o id `538` no lugar,
erro de **transcrição do identificador** ao ecoá-lo. Taxa medida: 1 em 1.019
(0,1%) — desprezível aqui, mas ~35 tweets no escopo de >10 RT.

**O número reportado acima é o medido (n=1.018), sem correção retroativa** —
recuperar o tweet depois de ver o resultado seria mexer no teste cego. A
correção foi feita **no pipeline, para as rodadas seguintes**: quando a
quantidade de rótulos devolvidos bate com a do lote, o alinhamento passa a ser
por **posição** (a ordem é preservada), e cada id corrigido é registrado em
`execucao.json` (`n_ids_corrigidos_por_posicao`). É correção mecânica, sem
juízo sobre o conteúdo do rótulo.

---

## D7. O gabarito não tem classe neutra — e o rotulador herdou isso

**Apurado em 27/jul/2026**, depois da validação no estrato baixo reprovar.
Detalhamento completo em `CALIBRAGEM_criterio.md`.

**O que se apurou.** O método do artigo (PDF, p. 3) prevê três classes de
stance: *pro-vaccine, anti-vaccine, non-relevant/ambiguous*. Os três tweets
que o gabarito atribui à terceira classe são usos da palavra "vacina" **fora
do tema** (meme, trocadilho com influenciadores, vacinação veterinária). A
classe operou como marcador de irrelevância tópica, não de ausência de posição.
Tweets sobre vacinação sem juízo avaliativo não tinham categoria e foram
resolvidos em `pro` ou `anti` — esquema **binário forçado**, desenho comum na
literatura, não uma particularidade deste artigo.

**Consequência para o nosso instrumento.** O rotulador reproduziu fielmente o
esquema do gabarito, inclusive a ausência da classe neutra (κ 0,759 no estrato
viral). Aplicado ao corpus amplo, onde ~1/3 dos tweets é topicamente relevante
mas não avaliativo, ele atribui lado a esses casos porque nunca viu exemplos do
contrário. **Não é defeito de redação do prompt: é propriedade do material de
calibração.**

**Direção do viés.** Na amostra manual, os neutros forçados dividiram-se de
forma aproximadamente simétrica (16 `pro` / 14 `anti`), o que **atenua** as
estimativas em direção a 50%. As proporções do rotulador no corpus amplo devem
ser lidas como **limite inferior** — a rotulagem humana dá 64,7% de `pro` entre
os decididos contra 62,6% do rotulador.

### Duas retratações minhas, registradas

1. **"A sub-coleta contaminou o instrumento por estrato"** — retirada. A taxa de
   `nenhum` da Mariana é praticamente igual nos dois estratos (33% viral, 32%
   baixo); os neutros não são propriedade do estrato. O mecanismo real é a
   ausência da classe no material de calibração, não a diferença de estrato.
2. **"A Tabela 1 do paper corrobora o achado"** — enfraquecida. A Tabela 1
   classifica por **comunidade do autor** na rede, não por conteúdo do tweet;
   seus 27,1% de *Unidentified* são autores fora das duas comunidades grandes,
   não tweets sem posição. Vale como indício independente de direção, não como
   corroboração.

Em ambos os casos o erro foi o mesmo: tomar proximidade numérica entre
grandezas de construtos diferentes como evidência de que mediam a mesma coisa.

---

## D8. `p6` (Padrão B) — **REPROVADA** por 0,003

Padrão B adotado por decisão da Mariana: o rotulador passa a codificar em três
classes, com exemplos tirados da partição de calibração da rotulagem humana.
Acrescentada a **regra de atribuição** formulada por ela em 27/jul/2026:

> O stance é propriedade do que o **tweet afirma** sobre a vacinação, não do
> que se infere sobre o **autor**. Reproduzir fala de terceiro sem comentário
> próprio não é tomar posição; posicionar-se sobre tema adjacente (passaporte,
> restrições, obrigatoriedade) marca a categoria temática e deixa o stance em
> `nenhum`. *"Não é um tweet pró-vacina, mas de alguém pró-vacina."*

### Resultado

| conjunto | p4 | p5 | **p6** | aceite |
|---|---:|---:|---:|---:|
| calibração (n=50) | 0,469 | 0,639 | 0,727 | — |
| **reservado (n=50)** | 0,477 | 0,544 | **0,697** | **0,70** |
| viral reservado (n=30) | 0,417 | — | **0,501** | 0,70 |

**Veredito: REPROVADO.** O critério pré-registrado era κ ≥ 0,70 na partição
reservada; deu 0,697. A diferença é irrelevante estatisticamente
(IC 90% = [0,544 ; 0,834]; P(κ real ≥ 0,70) ≈ 46%), **mas o critério foi
registrado como ponto e não como intervalo**. Arredondar para cima aqui
invalidaria todo o pré-registro. Fica reprovado.

A segunda checagem (30 virais, reservados desde o início) dá 0,501 — abaixo
também, e num estrato onde o material é retoricamente mais complexo. As
marginais batem bem (11/9/10 dela contra 9/10/11 do modelo), mas a atribuição
item a item erra em 1/3 dos casos.

Como previsto no pré-registro, a concordância com o **gabarito do paper** caiu
(0,759 → 0,463): adotar a classe neutra afasta o rotulador do esquema binário.
Isso é o desenho, não falha.

### O que está esgotado

Ambas as partições reservadas foram usadas. Iterar de novo contra elas seria
exatamente o vício que o pré-registro existe para impedir.

### O ponto de referência que falta

Não há estimativa de confiabilidade **humano × humano** para o esquema de três
classes. O artigo não reporta concordância entre seus próprios codificadores; a
única medida disponível é Mariana × gabarito = 0,350, que compara esquemas
diferentes e não serve de teto.

Sem esse número não se sabe se **0,70 era alcançável**. É um limite do desenho,
não desculpa para o resultado: o teto plausível de qualquer instrumento é a
concordância entre humanos na mesma tarefa, e essa não foi medida — nem por nós,
nem pelo artigo original.

---

## D9. O teto da tarefa — e o que isso faz com o critério

Reteste intra-codificador (30 tweets re-rotulados às cegas pela Mariana no
mesmo dia): `RETESTE_intracodificador.md`.

| Medida | κ | IC 90% |
|---|---:|---|
| **Mariana × Mariana** (teto da tarefa) | **0,746** | [0,56 ; 0,90] |
| `p6` × Mariana, mesmos 30 tweets | 0,648 | [0,44 ; 0,84] |
| `p6` × Mariana, partição reservada (n=50) | 0,697 | [0,54 ; 0,83] |
| Mariana × gabarito do paper (esquema binário) | 0,350 | [0,18 ; 0,52] |

Diferença teto − máquina: **+0,097** (IC 90% [−0,01 ; +0,22]);
P(máquina ≥ teto) ≈ 12%.

### O que isso estabelece

1. **O critério pré-registrado de 0,70 coincide praticamente com o teto da
   tarefa (0,746).** Sem saber disso, exigimos do rotulador desempenho
   equivalente ao de um humano contra si mesmo. É uma barra atipicamente alta,
   e não foi escolhida por essa razão — foi herdada da literatura.
2. **O teto de 0,746 é otimista.** O reteste foi no mesmo dia, e memória infla
   auto-concordância. O teto real é mais baixo; quanto, não se sabe. É
   plausível que esteja em torno de 0,70 — ou seja, **é possível que o critério
   fosse inatingível até para a codificadora humana.**
3. **A máquina fica abaixo do teto, mas pouco.** A diferença é +0,097 com IC
   cruzando quase o zero. A reprovação da `p6` por 0,003 permanece válida como
   fato pré-registrado; o que muda é o que ela significa.

### Conclusão registrada

A reprovação **não** deve ser lida como "o rotulador é inadequado". Deve ser
lida como: o rotulador opera perto do teto de consistência que a própria tarefa
admite, e o critério foi fixado num patamar que a tarefa mal comporta.

O `nenhum` é uma classe genuinamente difícil — **para a máquina e para a
humana**. Distinguir "não toma posição" de "toma posição indiretamente" é
julgamento fino, e a codificadora discorda de si mesma em 1 de cada 6 casos.

### Consequência para a tese

Este é o resultado mais forte do eixo B, e não estava previsto. A survey mostra
que a **coleta** é sub-problematizada. Aqui se acrescenta: a **anotação**
também é — e de forma auto-encobridora, porque sem medida de confiabilidade
não há como saber que o rótulo é instável. O artigo replicado teve dois
codificadores e um árbitro e não reportou κ; esta replicação mediu, e o número
é 0,746 contra a própria codificadora — um limite que qualquer conclusão
derivada daqueles rótulos herda, sem que ninguém tenha notado.

---

## Pendências de decisão

- [x] ~~Congelar o prompt e rodar o teste cego~~ — feito (D5, D6). **Aprovado.**
- [ ] **Rotular o escopo do E1** (>10 RT, 34.866 tweets, ~US$ 13 no pior caso)
      e seguir para a Fase 3. **Aguarda aval da Mariana** — é o maior gasto do
      caso, ainda que caiba no teto com folga.
- [ ] **`--por-chamada` 1 vs 10** (D0.5): decidir por κ, não por custo
      (~US$ 0,35). Agora só faria sentido **antes** da rodada grande, e mudaria
      o rotulador congelado — ou seja, exigiria revalidar. Provável descarte.
- [ ] Opção C (classificador como análise de robustez), se houver cronograma.

> **O rotulador está validado e congelado.** Qualquer mudança daqui em diante
> (modelo, prompt, agrupamento) invalida o κ de D6 e exige nova validação.
