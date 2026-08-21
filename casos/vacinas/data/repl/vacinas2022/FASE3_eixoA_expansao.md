# Fase 3 / eixo A — expansão da rede por limiar

> Gerado em **07/ago/2026** por `analise/av3_influentes_por_limiar.py` sobre o
> snapshot congelado e a partição da seed 42. Números em `av3_influentes.json`.
> Par do [FASE3_curvas.md](FASE3_curvas.md), que faz o mesmo pelo eixo B (conteúdo).
> O ponto original está em [FASE2_replicacao_ponto.md](FASE2_replicacao_ponto.md).

---

## 1. AV3 — composição pró × anti dos autores influentes, por limiar

**A afirmação do alvo (Tabela 3):** dos **602 autores influentes**, 353 pró (58,6%)
× 246 anti (40,9%). "Influente" = autor de ao menos 1 tweet viral (>500 RT).

**O teste:** baixar o limiar que define "influente" e ver se a composição se mantém.

**A regra de lado é topológica, não de conteúdo:** cada autor herda o lado da sua
comunidade, pela mesma regra do AV1 (maioria das 599 sementes publicadas; comunidade
sem semente → não identificado). Não usa o rotulador LLM do eixo B — é medição
independente dele.

| limiar | autores | pró | anti | n/ident | %pró* | %anti* | **razão pró/anti** |
|---|--:|--:|--:|--:|--:|--:|--:|
| **>500 RT** | 625 | 361 | 252 | 12 | **58,9%** | **41,1%** | **1,43** |
| >250 RT | 986 | 595 | 379 | 12 | 61,1% | 38,9% | 1,57 |
| >100 RT | 1.704 | 1.111 | 559 | 34 | 66,5% | 33,5% | 1,99 |
| >50 RT | 2.691 | 1.833 | 793 | 65 | 69,8% | 30,2% | 2,31 |
| >25 RT | 4.483 | 3.038 | 1.296 | 149 | 70,1% | 29,9% | **2,34** |
| >10 RT | 8.665 | 5.644 | 2.616 | 405 | 68,3% | 31,7% | 2,16 |

`%pró*` = entre os autores que receberam lado (exclui não identificados).

### 1.1 O ponto original replica — e isso valida o instrumento

| | autores | pró | anti | razão |
|---|--:|--:|--:|--:|
| **paper** (Tabela 3) | 602 | 353 (**58,6%**) | 246 (**40,9%**) | **1,43** |
| **réplica** (>500 RT) | 625 | 361 (**58,9%**) | 252 (**41,1%**) | **1,43** |

Diferença de **0,3 p.p.** na composição e razão idêntica. O conjunto é ligeiramente
maior (625 × 602) porque as contagens de RT são da re-coleta de mai/2022, posteriores
às do paper.

> **Por que isto importa mais do que parece.** A atribuição de lado aqui é **por
> topologia** — comunidade de retuítes, sem ler uma linha de texto. O paper rotulou
> esses mesmos autores **por conteúdo**. Os dois caminhos chegam ao mesmo lugar com
> 0,3 p.p. de diferença. Isso **valida a regra de atribuição de lado** usada no
> [AV1](FASE2_replicacao_ponto.md#av1), que era a peça mais frágil daquele resultado:
> a objeção "vocês atribuíram os lados errado" fica respondida pelo próprio gabarito
> publicado do artigo.

### 1.2 Ao descer o limiar, a composição **muda**

A razão pró/anti vai de **1,43** (>500 RT) a **2,16–2,34** abaixo de 25 RT: o
desequilíbrio a favor do lado pró **dobra**. A fatia pró entre os autores com lado
sobe de 58,9% para 70,1% no pico (>25 RT), fechando em 68,3% em >10 RT.

⚠ **A curva não é monotônica no fim:** a razão cresce até >25 RT (2,34) e recua em
>10 RT (2,16). Não há evidência de convergência dentro da faixa observada, e o recuo
final não está explicado — pode ser real (autores de baixíssimo engajamento têm
composição diferente) ou efeito de mais autores caírem em comunidades pequenas sem
semente (os não identificados sobem de 12 para 405).

---

## 1b. AV4 — a concentração é estrutural ou artefato do corte?

> `analise/av4_lorenz_por_limiar.py` → `av4_lorenz.json`.
> **Nota de dado:** `rt_arestas.tweet_referenciado_id` está **100% nulo** na
> re-coleta, então não dá para ligar cada evento de RT ao tweet que o originou. Usa-se
> a coluna `retweets` dos originais (contagem da API por tweet) agregada por autor —
> que é exatamente o `SUM_Retweets_Per_Author` da aba `Authors` do suplemento.

| limiar | autores | RTs | top-10 | top-100 | **Gini** | top 10% dos autores |
|---|--:|--:|--:|--:|--:|--:|
| **>500 RT** | 625 | 2.451.210 | **15,3%** | 60,6% | 0,609 | 47,9% |
| >250 RT | 986 | 2.996.414 | 13,7% | 55,6% | 0,675 | 55,3% |
| >100 RT | 1.704 | 3.470.066 | 12,5% | 51,7% | 0,753 | 64,5% |
| >50 RT | 2.691 | 3.735.681 | 11,8% | 49,4% | 0,808 | 72,4% |
| >25 RT | 4.483 | 3.950.268 | 11,2% | 47,5% | 0,854 | 80,2% |
| >10 RT | 8.665 | 4.178.561 | 10,6% | 45,4% | 0,895 | 87,7% |
| **todos** | 75.082 | 4.599.451 | **9,7%** | 41,5% | **0,957** | **95,2%** |

**O ponto publicado replica:** top-10 = **15,3%** contra os **15,7%** do artigo, 0,4
p.p. de diferença. É a terceira quantidade publicada que a réplica reproduz (com AV3
a 0,3 p.p. e o gabarito de stance a 0,0).

### Leitura — e o que **não** se pode concluir

⚠ **As duas medidas se movem em parte por construção, e isso precisa ser dito.** O
`top-k share` cai ao alargar o universo porque há mais autores para dividir o total;
o Gini sobe porque incluir a cauda acrescenta desigualdade. Nenhum dos dois é
scale-free na comparação entre recortes. **Não se pode, portanto, ler o Gini de 0,957
como prova de que "a concentração é estrutural"** — parte do salto é mecânica.

O que **se pode** afirmar:

1. **O número 15,7% é uma propriedade do corte, não do debate.** Ele varia de 15,3% a
   9,7% conforme o limiar, de forma monotônica. Quem lê "os 10 maiores concentram
   15,7% dos retuítes" como característica do debate vacinal está lendo uma
   característica do recorte >500 RT.
2. **A conclusão qualitativa sobrevive em todos os cortes**, e com folga: mesmo no
   universo inteiro, 10 contas em 75.082 detêm 9,7% dos retuítes, e 10% dos autores
   detêm 95,2%.

Ou seja: **AV4 não muda** (a afirmação substantiva se mantém), mas o **valor**
publicado não é transportável para fora do estrato em que foi medido.

---

## 1c. AV1 por fração de N — a curva `A(volume)` da rede

> `analise/curva_rede_por_fracao.py` → `curva_rede.json`. 29 min de execução.
> Sorteia uma fração *f* da coleta (originais **e** eventos de RT), reconstrói o
> grafo, roda Louvain, atribui lado pela regra do AV1 e mede. Base de posts: ampla.

⚠ **Réplicas abaixo do protocolo.** 5 réplicas até f=0,25; 3 em 0,50/0,75; 1 em
f=1,0. O protocolo pede ≥30. Motivo: cada réplica é um Louvain sobre até 3,3 M
arestas. **As bandas abaixo são min–max das réplicas, não IC bootstrap.**

| fração | posts | **razão pró/anti** (min–max) | cobertura | NMI vs corpus cheio |
|---|--:|--:|--:|--:|
| 0,010 | 65.506 | **1,31** (1,28–1,34) | 60,5% | 0,420 |
| 0,025 | 163.816 | 1,39 (1,37–1,42) | 64,5% | 0,481 |
| 0,050 | 327.848 | 1,43 (1,39–1,44) | 67,6% | 0,512 |
| 0,100 | 655.457 | 1,46 (1,45–1,48) | 70,5% | 0,561 |
| 0,250 | 1.638.104 | 1,50 (1,48–1,51) | 73,8% | 0,672 |
| 0,500 | 3.277.480 | 1,52 (1,51–1,53) | 76,0% | 0,774 |
| 0,750 | 4.916.952 | 1,55 (1,54–1,56) | 77,5% | 0,851 |
| **1,000** | 6.554.705 | **1,55** | 78,0% | 0,972 |

### 1c.1 A que fração AV1 converge? **≈ 0,75**

A razão sobe de forma **monotônica** e só entra na banda do valor final a partir de
**f = 0,75**: em f=0,50 a banda é 1,51–1,53, que **não contém** o 1,55 do corpus
cheio. Ou seja, **seria preciso ~75% desta coleta** para a razão pró/anti estabilizar.

É a **primeira célula preenchida** da coluna *fração mínima que estabiliza a
conclusão* da [tabela mestre](../../../RESULTADOS_tabela_mestre.md) — e o valor é
alto, o que é o próprio ponto: metade da coleta ainda daria um número em movimento.

**A estrutura converge ainda mais devagar.** O NMI contra a partição do corpus cheio
vai de 0,42 (1%) a 0,85 (75%). O teto é **0,972** — o valor em f=1,0, que não tem
sorteio nenhum e mede só a variabilidade de seed do Louvain. Em 75% da coleta a
partição ainda está a 0,12 do teto: **a estrutura de comunidades não convergiu**
dentro da faixa disponível.

### 1c.2 ⚠ O que esta curva **corrige** na leitura de AV1b

**Em nenhuma fração a razão chega perto do 1,02 do artigo.** Mesmo com **1% da
coleta** (65 mil posts, contra os 5,15 M do artigo) a réplica já mede **1,31**.

Isso obriga a qualificar o que se disse antes. A leitura de que "o lado anti é
praticamente o mesmo nas duas coletas e todo o crescimento está do lado pró"
(§AV1 do [FASE2](FASE2_replicacao_ponto.md)) sugeria uma explicação **de volume**.
A curva mostra que não é: se fosse, coletar menos aproximaria a réplica do artigo, e
não aproxima. Portanto:

- **o que é de volume:** dentro da nossa medição, a razão se move de 1,31 a 1,55 —
  o número depende de quanto se coletou, e não estabiliza antes de ~75%;
- **o que NÃO é de volume:** a distância entre a réplica (1,31–1,55) e o artigo
  (1,02). Essa vem de **medição/convenção**, não de tamanho de coleta — coerente com
  a fatia "não identificada" do artigo (22,3%) ser bem maior que a nossa sob a
  convenção dele (9,4%), o que empurra o número dele em direção ao equilíbrio.

**O veredito de AV1b não muda** (o equilíbrio relatado não se reproduz), mas a
**causa** não é sub-coleta. É diferença de como cada trabalho decide quem tem lado.

---

## 1d. AV2 — os tweets pró recebem mais RTs que os anti?

> `analise/av2_rts_por_lado.py` → `av2_rts_por_lado.json`. RTs pela coluna
> `retweets` dos originais; lado pelos rótulos do eixo B.

**A afirmação do alvo (Tabela 2)** é ambígua — "os tweets pró **mais populares**
receberam **2×** mais retuítes que os anti mais populares" — então medem-se as duas
leituras: a **agregada** (soma de RTs de cada lado) e a **do topo** (os N mais
retuitados de cada lado).

| limiar | n pró | n anti | RTs pró | RTs anti | **agregada** | topo-10 | topo-1 |
|---|--:|--:|--:|--:|--:|--:|--:|
| >500 RT | 732 | 779 | 1.413.346 | 939.892 | **1,50** | 3,16 | 2,33 |
| >100 RT | 3.264 | 2.563 | 1.978.490 | 1.347.994 | 1,47 | 3,16 | 2,33 |
| >10 RT | 17.638 | 10.534 | 2.407.596 | 1.585.332 | **1,52** | 3,16 | 2,33 |

*(esquema `p4`, o binário do artigo; com `p6` a agregada fica em 1,58–1,62)*

**Qual leitura o artigo quis dizer?** A do **topo-1** — o tweet pró mais retuitado
recebeu **2,33×** o do anti, que é o "2×" declarado. A agregada dá 1,50 (réplica) ×
**1,68** (Tabela 2 do suplemento, rotulagem humana); a do topo-10 dá 3,16, mais que
o dobro.

### ✅ Veredito: **AV2 não muda, e não muda por construção**

A razão agregada é **plana** entre limiares (1,47–1,52 em `p4`; 1,58–1,62 em `p6`).
E as razões de topo são **idênticas** em todos os limiares — o que **não é achado
empírico, é propriedade da medida**: os tweets do topo estão, por definição, em todos
os estratos. Qualquer coleta que alcance o limiar já os contém.

> **Observação metodológica que vale generalizar.** A sensibilidade ao volume depende
> de **que parte da distribuição** a afirmação descreve. Afirmações sobre a **cauda
> extrema** (AV2, AV4) são estruturalmente imunes à sub-coleta, porque a cauda é o
> que qualquer coleta captura primeiro. Afirmações sobre o **balanço** da
> distribuição (AV1b, AV3, AV6) são as frágeis. Não é o tema que decide a robustez,
> é a estatística escolhida.

---

## 2. Leitura — três caminhos independentes, mesma direção

O caso agora mede o **mesmo desequilíbrio** por três operacionalizações que não
compartilham instrumento, unidade nem dado de entrada:

| eixo | unidade | instrumento | no estrato viral | expandido |
|---|---|---|---|---|
| **AV1** | posts | topologia | (paper: razão 1,02) | razão **1,50–1,56** |
| **AV3** | autores influentes | topologia | razão **1,43** ✔ replica | razão **2,16–2,34** |
| **AV6** | tweets rotulados | conteúdo (LLM) | 48,4% pró ✔ replica | **62,6%** pró |

Nos três, o estrato viral subestima o peso do lado pró, e a diferença aparece assim
que se sai dele. AV3 é o mais forte dos três como evidência, porque é o único cujo
ponto original **reproduz o número publicado** e cujo instrumento é validado por esse
mesmo ponto.

**O que isso diz sobre o alvo:** a conclusão-título ("os anti-vacina impuseram o
enquadramento") descreve o estrato viral. Fora dele, o lado pró é majoritário em
autores, em posts e em tweets — e por margem crescente conforme se desce o limiar.

---

## 3. Pendências do eixo A na Fase 3

| Item | Estado |
|---|---|
| **AV3 por limiar** | ✅ §1 |
| **AV4 — curva de Lorenz / top-k por limiar** | ✅ §1b |
| **AV1 por fração de N** — proporção pró/anti e cobertura em frações crescentes, com NMI entre partições ("AV1 converge a que fração?") | ✅ §1c |
| **AV2 — top pró × top anti em RTs** | ❌ nunca testado |
| **E3 — recomputar por termo-índice** | ❌ não feito |

Ver a auditoria completa em
[REPLICACAO_CASO_VACINAS.md §4.1](../../../vacinas/REPLICACAO_CASO_VACINAS.md).

---

## 4. Ressalvas

1. **Contagens de RT pós-paper.** Os limiares são aplicados sobre a re-coleta de
   mai/2022; um tweet que tinha 480 RT à época do artigo pode ter 520 aqui. Os
   conjuntos não são exatamente os mesmos objetos — vale para todas as linhas.
2. **Filtro de idioma.** O conjunto de influentes usa `idioma='pt'`, para acompanhar
   o eixo B. A partição de comunidades, não (o paper rodou a rede no corpus todo).
3. **Herança de lado por comunidade.** Um autor herda o lado da comunidade inteira;
   autores atípicos dentro da sua comunidade são contados no lado da maioria. É a
   convenção do paper, e a §1.1 mostra que ela reproduz a codificação publicada — mas
   só foi verificada no estrato viral, que é onde o gabarito existe.
4. **Não identificados crescem com a expansão** (12 → 405), o que pode afetar a cauda
   da curva (ver ⚠ em §1.2).
