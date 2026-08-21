# Fase 2 — Replicação do ponto original (eixo A: rede/modularidade)

> Executado em **23/jul/2026** por `analise/rede_modularidade.py` sobre o snapshot
> congelado (busca 178). Números-chave em `fase2_rede.json`; log em `fase2_rede.log`.
> Cruzamentos com o gabarito do paper (`suplementar_rotulos.xlsx`) feitos ao vivo e
> reproduzíveis (código no doc do log desta fase).

## Setup (decisões registradas)

- Grafo **nível-autor** (retuitador → autor original), não-direcionado, peso = nº de
  RTs no par; 879.189 nós, 3.343.405 arestas (de 3.350.803 pares / 4.507.889 RTs).
- **Sem filtro de idioma** (o paper rodou a rede no corpus todo).
- Louvain (igraph `community_multilevel`), seeds 42/43/44 →
  modularidade 0,648 nas três; **NMI par-a-par 0,957–0,966** (estável).
  Run de referência: seed 42.
- "Posts" = originais + RTs do autor, **mesma definição** da Tabela 1 do paper
  (tweets + retweets). ⚠ **As magnitudes não são iguais**: a Tabela 1 soma
  1.107.224 tweets + 4.042.050 RTs = **5.149.274 posts**; a nossa re-coleta de
  mai/2022 dá **6.554.705** (27% maior, sobretudo em originais: 2,05 M × 1,11 M).
  *(Corrigido em 07/ago/2026 — a versão anterior desta linha afirmava que os dois
  totais eram o mesmo número.)*

## Resultados × afirmações do paper

### AV1 — "duas comunidades ~2/5 cada; juntas 78%" → **cobertura SIM, equilíbrio NÃO**

**Primeira leitura (23/jul/2026), depois descartada como mal pareada:**

| | nossa réplica | paper |
|---|---|---|
| Duas comunidades dominantes e ~equilibradas? | **sim** — com 3: 30,6% dos posts; com 2: 30,0% | ~2/5 cada |
| Juntas | **60,6%** dos posts (68,4% excluindo os 11,3% de posts de autores fora do grafo de RTs) | 78% |

Isso comparava as **duas maiores comunidades isoladas** com a **união dos grupos** do
paper — ver abaixo. Mantido só como registro; **não use estes 60,6%**.

### ✅ Causa da divergência — **estabelecida em 07/ago/2026** (era o numerador, não o denominador)

A comparação estava **mal pareada**, e a Tabela 1 do paper — que não está no PDF, só
no suplemento (aba `Table tweets and retweets`) — mostra por quê.

**O 78% do paper reproduz-se assim:**

| Tabela 1 do paper | tweets | retweets |
|---|--:|--:|
| Pro-vaccine | 461.265 (41,7%) | 1.561.005 (38,6%) |
| Against-vaccine | 345.688 (31,2%) | 1.632.738 (40,4%) |
| **Unidentified** | 300.271 (27,1%) | 848.307 (21,0%) |
| Total | 1.107.224 | 4.042.050 |

→ (461.265 + 345.688 + 1.561.005 + 1.632.738) / 5.149.274 = **77,7% ≈ 78%**, com
**22% de "Unidentified"**. O denominador do paper é **todos os posts do período** —
o mesmo conceito que usamos. Não era ali o problema.

**O erro estava do outro lado da fração.** O "pró" e o "anti" da Tabela 1 **não são
duas comunidades**: são a **união dos grupos de modularidade mapeados a cada lado**.
A aba `Spreadsheet 1` (coluna `Group eTC`) tem **7 grupos** entre os 1.525 virais
(g1 567 · g2 782 · g3 125 · g4 28 · g5 14 · g6 8 · g7 1), e o cruzamento desta mesma
fase já mostrava que **g2 = anti**, enquanto o lado **pró é g1 + g3 + menores**. Nós
comparávamos isso com as **duas maiores comunidades isoladas** da nossa partição.

### Atribuição formal de lado — a medida (07/ago/2026)

> Gerado por `analise/atribui_lado_comunidades.py` sobre a **partição já congelada**
> (`comunidades_autores`, seed 42 — não re-roda Louvain, para o número ser comparável
> ao da Fase 2). Números em `av1_lados.json`.

**Regra**, análoga à do paper (que rotulou cada *grupo* por seus membros influentes e
fez todo usuário herdar o lado do grupo): as **599 sementes** com lado publicado
(aba `Authors` = Tabela 3 do paper, 353 pró / 246 anti, conferido em execução) são
localizadas na partição; cada comunidade recebe o lado da **maioria** das sementes que
contém; comunidade sem semente, ou com empate, fica **não identificada**; autores fora
do grafo de RT (11,3% dos posts) idem.

**As 599 sementes caem em apenas 8 das 11.664 comunidades:**

| comunidade | lado | sementes | % dos posts |
|---|---|---|--:|
| com 3 | **anti** | 244 anti · 1 pró | 30,63% |
| com 2 | pró | 183 pró | 30,00% |
| com 0 | pró | 158 pró | 14,90% |
| com 13 | pró | 5 pró · 2 anti | 1,12% |
| com 17 · 9 · 8 · 19 | pró | 1 · 1 · 3 · 1 pró | 1,78% (somadas) |

#### Qual base de contagem? — duas, de propósito

O corpus da réplica é maior que o da Tabela 1 (6,55 M × 5,15 M posts) **sem ser uma
janela maior**: as datas do snapshot vão de `2021-12-08T23:00` a `2022-02-08T22:59`
(−03:00), ou seja, **exatamente** a janela 9/dez–9/fev do artigo. Não há material da
coleta de repercussões de 8/mar/2022 aqui dentro. A diferença é de **convenção de
contagem**, e ela é identificável:

| "Tweets" (coluna 1 da Tabela 1) | n | vs paper |
|---|--:|--:|
| paper | 1.107.224 | — |
| todos os originais da réplica | 2.046.816 | +85% |
| só `idioma='pt'` | 1.713.885 | +55% |
| só autores no grafo de RT | 1.304.267 | +18% |
| **pt E no grafo de RT** | **1.129.126** | **+2%** |

O último bate com o **critério de inclusão declarado no PDF** ("*all tweets from users
who retweeted or retweeted someone in the period*") somado ao idioma dos termos-índice.
Os RTs ficam em 4.507.889 × 4.042.050 (+12%). Por isso o script roda **duas bases**:
a **ampla** (tudo) e a **convenção do paper** (pt + no grafo).

#### Resultado

| | base ampla | conv. do paper | paper (Tabela 1) |
|---|--:|--:|--:|
| posts | 6.554.690 | 5.637.000 | 5.149.274 |
| pró | 47,8% | 55,2% | 39,3% |
| anti | 30,6% | 35,4% | 38,4% |
| não identificados | 21,6% | 9,4% | 22,3% |
| **cobertura (pró+anti)** | **78,4%** | **90,6%** | **77,7%** |
| **razão pró/anti** | **1,56** | **1,56** | **1,02** |

**Sensibilidade** (mínimo de sementes por comunidade: 1, 2, 3, 5), nas duas bases —
**8 cenários**:

- **cobertura: 76,7% – 90,6%.** Varia com a base. **Não é uma medida estável.**
- **razão pró/anti: 1,50 – 1,56.** Praticamente constante nos 8 cenários, contra
  **1,02** do paper.

### ✅ Veredito de AV1 — as duas partes, e **só uma** é conclusiva

| parte de AV1 | réplica | veredito |
|---|---|---|
| "juntos, **78%** dos posts" | 76,7%–90,6% conforme a base | ◐ **inconclusivo** |
| "pró e anti têm volumes **semelhantes**, ~2/5 cada" | razão 1,50–1,56 × 1,02 | ✘ **não replica** |

> ⚠ **Correção de uma leitura anterior desta mesma sessão (07/ago/2026).** A primeira
> rodada da atribuição formal usou só a base ampla e deu cobertura 78,4% contra 77,7%
> — registrou-se então que "a cobertura replica". Ao rodar a segunda base isso caiu:
> a coincidência de 0,7 p.p. na base ampla resulta de duas diferenças que se cancelam
> (o corpus é maior, mas a fatia não identificada também). Sob a convenção que
> reproduz a contagem do paper, a cobertura vai a 90,6%. **A cobertura não é um teste
> informativo aqui**; a razão entre os polos é.

**O que sustenta o veredito de AV1b.** Em números absolutos, na base ampla:

| | paper | réplica | Δ |
|---|--:|--:|--:|
| posts anti | 1.978.426 | 2.007.838 | **+1,5%** |
| posts pró | 2.022.270 | 3.132.218 | **+54,9%** |

O lado **anti é praticamente o mesmo nas duas contagens**; a diferença toda está no
lado pró. E a razão pró/anti resiste às 8 combinações de base e regra, o que é o
oposto do comportamento da cobertura. Consistente, por um caminho independente
(topologia da rede, sem ler texto), com o achado do eixo B: ao sair do estrato viral,
a fatia pró cresce.

> ⚠ **Não leia a tabela acima como explicação de volume.** A curva `A(volume)` da
> rede ([FASE3 eixo A §1c.2](FASE3_eixoA_expansao.md)) mostra que **em nenhuma
> fração** da coleta a razão se aproxima do 1,02 do artigo: com **1% dos dados** a
> réplica já mede **1,31**. Se a divergência fosse de tamanho de coleta, coletar
> menos aproximaria — e não aproxima. A distância para o artigo é de **convenção de
> atribuição de lado**, não de sub-coleta. O veredito de AV1b não muda; a causa, sim.

⚠ **Ressalvas que permanecem:**
1. A regra manda a **com 0** inteira (349 k autores, difusa, 14,9% dos posts na base
   ampla) para o lado pró, com base em 158 sementes. É a convenção do paper aplicada
   com fidelidade — comunidade herda lado por inteiro —, mas é generosa **nos dois
   trabalhos**. Sem a com 0, o pró cai a 32,9% e a cobertura a 63,5% na base ampla.
2. A fatia "não identificada" da réplica sob a convenção do paper (9,4%) é bem menor
   que a dele (22,3%): a nossa regra rotula uma comunidade com **uma** semente, e a
   dele provavelmente só rotulou os grupos bem definidos. É outra razão para não ler
   a cobertura como medida comparável.
3. O paper não publica posts por grupo, só o agregado da Tabela 1, então a
   decomposição dele não é verificável.
4. Os RTs da réplica são 12% mais que os do paper mesmo na janela idêntica — resíduo
   da re-coleta de mai/2022 ainda **não explicado**.

### Identificação das comunidades — **cruzamento perfeito com o gabarito do paper**

Matching (case-insensitive) dos **602 autores influentes** da aba MAXQDA
("Grupo eTC") com as nossas comunidades: **602/602 achados**.

| Grupo do paper | n | cai na nossa… |
|---|---|---|
| grupo 2 (**anti**) | 244 | **com 3: 244/244 (100%)** |
| grupo 1 (**pró**, principal) | 224 | com 2: 175 · com 0: 49 |
| grupo 3 (pró, secundário) | 102 | com 0: 97 |
| grupos 4–7 (menores) | 32 | dispersos (com 0/2/13/…) |

→ **nossa com 3 = comunidade anti** (confirma também pelos autores-top: Fiuza,
Constantino, Osmar Terra, Bia Kicis, Zambelli…); **com 2 = pró** (autor-top:
@oatila). E um achado substantivo de graça: **o lado anti é UMA comunidade coesa
nas duas partições (100% de acordo); o lado pró se fragmenta** (o "pró" do paper é
a união dos grupos 1+3+4+5…, e no nosso Louvain parte dele cai na com 0 difusa) —
exatamente a tese do paper ("anti articulado, pró desarticulado"), agora visível
na topologia.

### AV4 — "top-10 autores = 15,7% dos RTs" → **REPLICA EXATO (com o denominador certo)**

- O 15,7% do paper é **dentro da amostra viral**: pela aba `Authors` do suplemento,
  top-10 = 374.531 de 2.383.643 RTs da amostra → **15,7%** reproduzido ao decimal.
- No **corpus completo** (4.507.889 RTs), o nosso top-10 = **9,3%** — número novo do
  caso: mesmo no universo, 10 contas concentram ~1 em cada 11 RTs.
- Top-10 nosso: 8 anti (com 3) + 2 pró (com 2: @oatila 1º, @ThiagoResiste 8º);
  paper: 9/10 anti. Diferença compatível com a época das contagens.

## Veredito da Fase 2 (eixo A)

O ponto original **replica em parte**: anti coesa × pró fragmentada e a concentração
do top-10 (exata com o denominador do paper).

A divergência 60,6% × 78% **foi resolvida em 07/ago/2026** — era comparação mal
pareada (duas comunidades × união de grupos). A atribuição formal trouxe duas coisas:
(a) **a cobertura de AV1 não é teste informativo** — varia de 76,7% a 90,6% conforme a
base de contagem; (b) **o equilíbrio entre os polos não replica**, e isso **é** robusto
— razão pró/anti de 1,50–1,56 nos 8 cenários, contra 1,02 do paper. Ver §AV1.

## Próximo (Fase 2 / eixo B)

Validar o rotulador automatizado contra os 1.525 tweets rotulados do gabarito
(κ no estrato >500 RT) e reproduzir a Tabela 5 (AV5) — só então descer o limiar
(Fase 3, teste das apostas do §5 do plano).
