# Tabela mestre — "mudou? / convergiu?" (Fase 4, **parcial**)

> Consolidado em **07/ago/2026** a partir dos `FASE*/RESULTADOS_*` de cada caso.
> **Nenhum número nasce aqui**: cada célula cita o documento canônico que a produziu.
> Se um valor divergir da fonte, a fonte vence — corrija lá e propague para cá.
>
> ⚠ **Parcial de propósito.** Fecham as 9 linhas de `twitter-ituassu` (eixo mídia) e
> `vacinas` (eixos A e B). Em ⏳: `heine-xande` (aguarda os dados,
> ver [ESTADO.md](../ESTADO.md) §2), o eixo *stance* do Ituassu (aguarda gabarito humano),
> `reddit-buntain` (Fase 0 feita; aguarda a coleta), `reddit-massachs` (Fase 0 parcial;
> aguarda o full text) e `meta-ads-imigracao` (Fase 0 parcial; aguarda o full text do CHI
> 2021 e a conta Meta verificada). As 7 linhas ausentes estão listadas em §4, não omitidas.

---

## 1. As duas perguntas

Cada linha responde às perguntas do protocolo (`escrita/dissertacao/corpo.tex`,
§Lógica do protocolo):

- **Mudou?** (PP1) — coletar mais do que o alvo coletou inverte a afirmação dele?
  O critério decisivo é **substantivo** (a afirmação se inverte), não apenas
  estatístico (sair do IC).
- **Convergiu?** (PP2) — a conclusão já estava estabilizada no volume original,
  caso em que coletar menos teria bastado?

As duas combinadas dão quatro desfechos. Os observados até aqui são **NÃO/SIM**
(robusta, a coleta bastava) e **SIM/NÃO** (frágil, coletar mais era necessário).

---

## 2. A tabela

| # | Caso · rede | Tipo de análise | Afirmação do alvo | **Mudou?** | **Convergiu?** | Fonte |
|---|---|---|---|---|---|---|
| 1 | ituassu · Twitter 2014 | Análise de conteúdo (classificação de fonte) | Entre conteúdo com mídia identificável, a vertical domina a horizontal | **NÃO** | **SIM — já em n = 100** (banda 74,5–92,0%, contém 83,4%) | [MV_MH §1](twitter-ituassu/RESULTADOS_analise_midia_MV_MH.md) · [curva](twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE3_curva_midia.md) |
| 2 | ituassu · Twitter 2014 | Estatística descritiva / temporal | **H1** — RTMV supera 50% em quase toda a semana | **SIM** (inverte) | **SIM — em n ≈ 200** ⚠ a falha do alvo é **viés do esquema**, não volume | [MV_MH §2](twitter-ituassu/RESULTADOS_analise_midia_MV_MH.md) · [curva](twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE3_curva_midia.md) |
| 3 | ituassu · Twitter 2014 | Estatística descritiva / temporal | **H2** — a MH rivaliza com a MV em ao menos um dia | **SIM** (não reproduz) | *não se aplica* — ⚠ não reproduz **em nenhum recorte**, nem no do próprio artigo | [MV_MH §8](twitter-ituassu/RESULTADOS_analise_midia_MV_MH.md) · [curva §3b](twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE3_curva_midia.md) |
| 3b | ituassu · Twitter 2014 (alvo **2018**) | Análise de conteúdo (classificação de fonte) | **Tab. 2 de 2018** — entre quem compartilha mídia, MP 59% × MC 41% | **NÃO** ao volume (amostra 70,3% ≈ universo 72,2%) · ⚠ **não reproduz o valor publicado**; as 4 explicações de classificação foram **testadas e descartadas** | **SIM** | [sensibilidade](twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md) · [link rot](twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE0_mp_mc_cdx.md) |
| 4a | vacinas · Twitter 2021–22 | Detecção de comunidades | **AV1a** — os dois lados juntos são 78% dos posts | ◐ **inconclusivo** (76,7–90,6% conforme a base de contagem) | *não se aplica* (o alvo já rodou no corpus completo) | [FASE2 §AV1](vacinas/data/repl/vacinas2022/FASE2_replicacao_ponto.md) |
| 4b | vacinas · Twitter 2021–22 | Detecção de comunidades | **AV1b** — os dois lados têm volumes semelhantes, ~2/5 cada | **SIM** (razão pró/anti 1,50–1,56 × 1,02 do paper) | **NÃO** — estabiliza só em **f ≈ 0,75** da coleta | idem · [curva](vacinas/data/repl/vacinas2022/FASE3_eixoA_expansao.md) |
| 4c | vacinas · Twitter 2021–22 | Detecção de comunidades / influência | **AV3** — dos 602 influentes, 58,6% pró × 40,9% anti | **SIM** (razão 1,43 → 2,16–2,34 ao descer o limiar) | **NÃO** (ainda subia em >10 RT) | [FASE3 eixo A §1](vacinas/data/repl/vacinas2022/FASE3_eixoA_expansao.md) |
| 5 | vacinas · Twitter 2021–22 | Centralidade / influência | **AV4** — top-10 autores concentram 15,7% dos RTs | **NÃO** na conclusão · ⚠ o **valor** é do corte (15,3% → 9,7%) | **SIM** | [FASE2 §AV4](vacinas/data/repl/vacinas2022/FASE2_replicacao_ponto.md) · [curva](vacinas/data/repl/vacinas2022/FASE3_eixoA_expansao.md) |
| 5b | vacinas · Twitter 2021–22 | Centralidade / influência | **AV2** — os tweets pró mais populares receberam 2× mais RTs que os anti | **NÃO** (topo-1 = 2,33× em todos os limiares) | **SIM** — mas *por construção*: o topo está em todo estrato | [FASE3 eixo A §1d](vacinas/data/repl/vacinas2022/FASE3_eixoA_expansao.md) |
| 6 | vacinas · Twitter 2021–22 | Análise de conteúdo (enquadramento) | **AV5** — ranking das categorias de enquadramento | **NÃO** ao volume · **SIM** à largura do filtro (E3) | **SIM** (no volume) | [FASE3 §2 e §5](vacinas/data/repl/vacinas2022/FASE3_curvas.md) |
| 7 | vacinas · Twitter 2021–22 | Análise de conteúdo (stance) | **AV6** — os anti-vacina impuseram o enquadramento; os polos se equivalem | **SIM** (inverte) | **NÃO** | [FASE3 §1, §3](vacinas/data/repl/vacinas2022/FASE3_curvas.md) |
| 8 | heine-xande · Twitter 2022 | Modelagem de tópicos (BERTopic) | ⏳ | ⏳ | ⏳ | [FASE0](heine-xande/data/repl/heine2022/FASE0_descoberta.md) |
| 9 | heine-xande · Twitter 2022 | Estatística quantitativa (SGBD) | ⏳ | ⏳ | ⏳ | idem |
| 10 | ituassu · Twitter 2014 | Sentimento / stance (EA/ED) | **H3** — os públicos diferem | ⏳ | ⏳ | [STANCE](twitter-ituassu/STANCE_como_o_paper_fez_e_onde_estamos.md) |
| 11 | reddit-buntain · Reddit 2013 | SNA / papéis sociais (rede) | **RB3** — só ~3% dos usuários (7/279) participam de >1 comunidade | ★ **SIM, por uma ordem de grandeza**: sob o **mesmo limiar de atividade** do artigo (≥20), o universo dá **57,6%** (3.450 de 5.991) — **19×** o publicado. Sem corte: 15,2% de 217.386 usuários | **SIM, em k≈10–20** (55,0% → 57,6% → 56,1%) — mas o valor do artigo não é recuperável em limiar nenhum: a limitação estava na **coleta** (top-100 × top-200), não no corte | [RESULTADOS_RB3](reddit-buntain/data/repl/buntain2013/RESULTADOS_RB3.md) |
| 12 | reddit-massachs · Reddit 2012–16 | Homofilia | **MH1** — homofilia e feedback social preveem apoio a Trump; influência social não. ✅ **o ponto original replica** (18/ago/2026): F1 **34,6% × 34,8%** na homofilia e **26,8% × 26,7%** na influência, sobre o gabarito dos autores | ⏳ (falta a Fase 3) | ⏳ | [FASE2](reddit-massachs/data/repl/massachs2016/FASE2_ponto_original.md) · [FASE0](reddit-massachs/data/repl/massachs2016/FASE0_descoberta.md) |
| 15 | youtube-agecovp · YouTube 2020–22 | Modelagem de tópicos / sentimento | **AG2** — os comentários são mais negativos que os vídeos (e AG4, categorias de canal; AG1, sentimento) | ⏳ (Fase 3 em coleta) | ⏳ | [FASE2](youtube-agecovp/data/repl/agecovp2020/FASE2_ponto_original.md) |
| 16 | tiktok-politok · TikTok 2024–26 | Análise de conteúdo / persistência | **PT2/PT3** — 18,7% e 39,7% dos posts deletados; **PT5** — deleção pela plataforma em 13,0% de todos os posts | ★ **SIM, no eixo TEMPORAL**: 3,3% → 9,5% → 18,7% em três checagens do mesmo conjunto (fator **5,7×**) | *não se aplica ao volume* — o denominador é idêntico nas três datas | [FASE2](tiktok/FASE2_politok.md) |
| 13 | meta-ads-imigracao · Instagram/Facebook 2019–20 | **Classificação** (pró/anti-imigração) | **CB2** — os anúncios anti capturam atenção acima do seu peso. Medido pela **razão de desproporção** R = fatia de impressões ÷ fatia de anúncios: **R = 1,72** entre os com posição (37,8% dos anúncios × 65,2% das impressões) · **1,46** entre todos. ⚠ o resumo do alvo contrasta populações diferentes | ⏳ | ⏳ | [DECISOES_CB2](meta-ads-imigracao/data/repl/metaads2019/DECISOES_CB2.md) · [ARTIGO §5.1](meta-ads-imigracao/ARTIGO_CAPOZZI_alvo.md) |
| 14 | meta-ads-imigracao · Instagram/Facebook 2019–20 | Centralidade / concentração | **CA2** — impressões muito desiguais (Gini 0,465 por página, 0,800 por anúncio) | ⏳ | ⏳ | idem |

---

## 3. Detalhe por linha (os números e a ressalva de cada uma)

### 1 · Dominância da mídia vertical — robusta ao volume

| | ponto original | ponto expandido |
|---|---|---|
| n | 700 (amostra 100/dia por pico) | 79.603 (base com mídia classificável) |
| MV entre classificáveis | 84,4% (384 / 455) | **83,4%** (IC95% Wilson 83,1–83,6) |

Contra o acaso, z = 188,3, p ≈ 0. A amostra de 700 já dava praticamente o mesmo
valor do universo: **coletar mais não teria alterado a conclusão, e a coleta
original bastava**.

⚠ **Ressalva, com a direção corrigida em 07/ago/2026:** 13,1% dos tweets têm link
morto e ficam fora da base. A versão anterior dizia que encurtados carregam **mais**
MH, e que os 83,4% seriam um **teto**. **Medido, é o inverso** — MH 11,3% nos
encurtados sobreviventes contra 37,4% nos diretos. Se os mortos se parecem com eles,
incluí-los subiria a MV: os 83,4% são um **piso**. A conclusão fica mais segura, não
menos. Ver [MV_MH §1](twitter-ituassu/RESULTADOS_analise_midia_MV_MH.md).

### 2 · H1 (RTMV > 50%) — artefato da amostragem por pico

| | RTMV | IC95% Wilson |
|---|---:|---|
| amostra reconstruída (n=700) | 48,3% | 44,6–52,0 (contém 50%; p = 0,36) |
| universo da mesma janela (n=32.193) | **36,1%** | 35,6–36,6 (z = −49,9, p ≈ 0) |

Queda de **−12,2 p.p. com ICs disjuntos** — viés sistemático, não flutuação. A
subamostra do artigo não reconstrói nem as proporções do universo de onde saiu.

**Curva `A(volume)`** (300 réplicas/ponto, subamostra aleatória sem reposição —
`curva_midia.json`):

| n aleatório | média | IC95% | poder de refutar H1 |
|---|--:|--:|--:|
| 100 | 35,7% | 28,0–45,0 | 87,0% |
| **200** | 36,0% | 30,0–42,5 | **99,7%** |
| **700** | **36,1%** | **32,6–39,9** | 100% |
| 2.800 | 36,1% | 34,5–37,8 | 100% |

> ⚠ **Correção de 07/ago/2026: esta linha dizia "convergiu? NÃO".** A curva mostra o
> contrário — a média é **36,1% em todo `n`**, e bastariam **200 tweets aleatórios**
> para refutar H1 com 99,7% de poder. O artigo coletou **700**, 3,5× o suficiente.
>
> **A falha do alvo não é de volume, é de esquema.** Os 48,3% dele **não cabem** na
> banda de n=700 aleatório (32,6–39,9%), o que exclui erro amostral. Dizer que
> "coletar mais era necessário para chegar à conclusão correta" é **falso** aqui:
> coletar mais *revelou* o erro, mas uma amostra aleatória 3,5× **menor** já o teria
> evitado. Ver [a curva](twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE3_curva_midia.md) §4.

### 3 · H2 (MH rivaliza com MV) — não reproduz em recorte nenhum

Em nenhum dia a MH se aproxima da MV; o dia que o artigo aponta como exceção
(23/out) é, no universo, o **mais vertical** (MV 59,0% × MH 10,1%).

**Curva por dia** (300 réplicas/ponto; rivalidade = MH% ≥ MV% no dia —
`curva_h2.json`):

- **Taxa de rivalidade = 0%** em todos os dias a partir de n=50, e **0% já em n=25**
  no 23/out. Ali o gap médio é 48,8 p.p. e o **pior caso** em 300 réplicas ainda
  deixa a MV 31 pontos à frente.
- **A amostra do próprio artigo, reconstruída, também não mostra rivalidade em
  23/out** (MV 62,0% × MH 13,0%).
- Sob a leitura alternativa ("MH atinge o pico da semana"), 23/out também não é o
  dia: o pico é **21/out** no universo (15,3%) e **20/out** na amostra (16,0%).

→ H2 não falha por volume **nem** por viés de esquema: **não se reproduz nem sob o
recorte que o artigo usou**. Fica em aberto se a divergência vem de outra
operacionalização de "rivalizar" ou da amostra específica dos autores.

⚠ **Ressalvas:** (i) ~~a MH é subcontada pelo link morto, logo o veredito é um
limite~~ — **medido em 07/ago/2026, a direção é a oposta**: encurtados (os que morrem)
têm MH **11,3%** contra **37,4%** dos diretos. Recuperar os mortos tenderia a subir a
MV, não a MH, o que **reforça** o veredito em vez de o limitar; (ii) a reconstrução da
amostra do artigo é aproximada — ele não detalha o procedimento, e a hora de pico de
22/out é ambígua no próprio texto.

### 4 · AV1 — comunidades: a cobertura replica, o equilíbrio não

Grafo nível-autor, 879.189 nós e 3.343.405 arestas; Louvain (seeds 42/43/44),
modularidade 0,648 nas três, NMI par-a-par 0,957–0,966. Lado atribuído a **todas
as 11.664 comunidades** pela regra do paper (maioria das 599 sementes publicadas;
`analise/atribui_lado_comunidades.py`).

| | base ampla | conv. do paper | paper (Tabela 1) |
|---|--:|--:|--:|
| pró | 47,8% | 55,2% | 39,3% |
| anti | 30,6% | 35,4% | 38,4% |
| não identificados | 21,6% | 9,4% | 22,3% |
| **cobertura (pró+anti)** | 78,4% | 90,6% | 77,7% |
| **razão pró/anti** | **1,56** | **1,56** | **1,02** |

Duas bases porque o corpus da réplica é maior que o da Tabela 1 **sem ser uma janela
maior** (as datas são exatamente as do artigo): a diferença é de convenção de
contagem. A convenção "originais em pt de autores no grafo de RT" reproduz a coluna
de tweets do artigo a **+2%** (1.129.126 × 1.107.224) e corresponde ao critério de
inclusão declarado no PDF.

Em **8 cenários** (2 bases × mínimo de 1, 2, 3 ou 5 sementes por comunidade):

- **AV1a, "juntos 78%": inconclusivo** — a cobertura varia de **76,7% a 90,6%**.
  Não é medida estável o bastante para servir de teste.
- **AV1b, "semelhantes, ~2/5 cada": não replica, e isso é robusto** — a razão
  pró/anti fica entre **1,50 e 1,56** nos oito, contra **1,02** do artigo.

As 599 sementes caem em **8 das 11.664 comunidades**. O lado **anti é uma única
comunidade coesa** (244 sementes anti contra 1 pró); o **pró se espalha por sete** —
a tese do alvo ("anti articulado, pró desarticulado") aparece na topologia.

**Em números absolutos, o desequilíbrio tem origem localizada** (base ampla):

| | paper | réplica | Δ |
|---|--:|--:|--:|
| posts anti | 1.978.426 | 2.007.838 | **+1,5%** |
| posts pró | 2.022.270 | 3.132.218 | **+54,9%** |

O lado anti é praticamente o mesmo nas duas contagens; a diferença toda está do lado
pró. Converge, por um caminho independente (topologia, não conteúdo), com a linha 7:
sair do estrato viral aumenta a fatia pró.

> ⚠ **Correção interna (07/ago/2026).** A primeira rodada usou só a base ampla, deu
> cobertura 78,4% × 77,7% e registrou "AV1a replica". A segunda base derrubou isso:
> os 0,7 p.p. eram coincidência de duas diferenças que se cancelam. Fica o registro
> de que a cobertura foi lida como confirmação antes de se testar a sensibilidade.

⚠ **Ressalvas:** (i) a regra manda a **com 0** inteira (349 k autores, difusa) para o
pró — convenção do artigo aplicada com fidelidade, mas generosa **nos dois
trabalhos**; sem ela o pró cai a 32,9% e a cobertura a 63,5% na base ampla; (ii) a
fatia não identificada da réplica sob a convenção do artigo (9,4%) é bem menor que a
dele (22,3%), porque a nossa regra rotula comunidade com uma semente só; (iii) o
artigo não publica posts por grupo; (iv) os RTs da réplica são 12% mais que os dele
na janela idêntica, resíduo da re-coleta ainda não explicado.

> **Esta linha não é um teste de volume.** O alvo rodou a rede sobre o corpus
> completo; aqui há **reprodução**, não expansão. Fica na tabela porque a
> identificação das comunidades é o que valida os eixos seguintes.

### 4c · AV3 — autores influentes: replica no ponto, muda na expansão

Unidade = **autor**, lado atribuído por **topologia** (comunidade), sem ler texto.

| | autores | pró | anti | razão |
|---|--:|--:|--:|--:|
| **paper** (Tabela 3) | 602 | 353 (58,6%) | 246 (40,9%) | **1,43** |
| **réplica** em >500 RT | 625 | 361 (58,9%) | 252 (41,1%) | **1,43** |

Depois, ao descer o limiar que define "influente": razão **1,57** (>250) · **1,99**
(>100) · **2,31** (>50) · **2,34** (>25) · **2,16** (>10). A fatia pró entre os
autores com lado vai de 58,9% a 70,1% no pico.

**Curva `A(volume)` da rede** (`curva_rede.json`, 5 réplicas até f=0,25 · 3 acima ·
bandas min–max, **não** IC bootstrap — abaixo das ≥30 do protocolo, por custo):

| fração | posts | razão pró/anti | cobertura | NMI vs cheio |
|---|--:|--:|--:|--:|
| 0,010 | 65.506 | 1,31 | 60,5% | 0,420 |
| 0,100 | 655.457 | 1,46 | 70,5% | 0,561 |
| 0,500 | 3.277.480 | 1,52 | 76,0% | 0,774 |
| **0,750** | 4.916.952 | **1,55** | 77,5% | 0,851 |
| 1,000 | 6.554.705 | 1,55 | 78,0% | 0,972 (teto: só seed) |

→ **fração mínima que estabiliza ≈ 0,75.** Em f=0,50 a banda (1,51–1,53) ainda não
contém o valor final. A **estrutura** converge ainda mais devagar: em 75% da coleta
o NMI está a 0,12 do teto.

> ⚠ **O que a curva corrige.** Em nenhuma fração a razão chega perto do 1,02 do
> artigo — com **1% da coleta** a réplica já mede **1,31**. Logo a distância entre a
> réplica e o artigo **não é efeito de volume**: se fosse, coletar menos aproximaria,
> e não aproxima. É diferença de **convenção de atribuição** (a fatia não
> identificada do artigo, 22,3%, é muito maior que a nossa sob a convenção dele,
> 9,4%, o que empurra o número dele para o equilíbrio). O veredito de 4b não muda;
> a **causa** não é sub-coleta.

> **A linha 4c valida o instrumento das linhas 4a/4b.** O lado aqui vem da
> comunidade de retuítes; o do paper veio da leitura do conteúdo desses mesmos
> autores. Os dois concordam a **0,3 p.p.** no estrato viral. A objeção mais óbvia ao
> resultado de AV1b — "a atribuição de lado por comunidade está errada" — fica
> respondida pelo gabarito publicado do próprio artigo.

⚠ A curva não é monotônica na cauda (2,34 em >25 RT, 2,16 em >10 RT) e os não
identificados sobem de 12 para 405 autores, o que pode afetar o último ponto. Não há
convergência dentro da faixa observada.

### 5 · AV4 — concentração: a conclusão sobrevive, o número não é transportável

| denominador | top-10 |
|---|---:|
| amostra viral (o do paper) | **15,7%** — reproduzido ao decimal |
| corpus completo (4.507.889 RTs) | **9,3%** |

Curva completa por limiar (`av4_lorenz.json`), com o `top-10` calculado dentro de
cada estrato:

| limiar | autores | top-10 | Gini | top 10% dos autores |
|---|--:|--:|--:|--:|
| >500 RT | 625 | **15,3%** | 0,609 | 47,9% |
| >100 RT | 1.704 | 12,5% | 0,753 | 64,5% |
| >10 RT | 8.665 | 10,6% | 0,895 | 87,7% |
| todos | 75.082 | **9,7%** | 0,957 | 95,2% |

O ponto publicado **replica** (15,3% × 15,7%). Depois, o valor cai de forma
monotônica: **15,7% é propriedade do corte >500 RT, não do debate**. A conclusão
substantiva, essa sim, sobrevive em todos os cortes — no universo inteiro, 10 contas
em 75.082 detêm 9,7% dos retuítes.

⚠ **Ressalva que impede uma leitura mais forte:** tanto a queda do `top-k` quanto a
subida do Gini são **em parte mecânicas** (mais autores diluem o top-k; incluir a
cauda acrescenta desigualdade). Nenhuma das duas medidas é comparável entre recortes
sem esse desconto, então **não** se conclui daqui que "a concentração é estrutural" —
só que o número publicado não sai do estrato onde foi medido.

### 6 · AV5 — enquadramento temático: **convergiu**

14 categorias, do estrato viral (>500 RT, n=1.559) ao corpus 19× maior
(>10 RT, n=29.978):

- maior deslocamento: **−8,4 p.p.** (*Restrictive policies*, 31,8% → 23,4%);
- a maioria das categorias fica dentro de **±2 p.p.**;
- **os temas não se reordenam.**

O estrato viral já representava bem a distribuição de enquadramentos do corpus
amplo: para esta análise, **o limiar do artigo bastava**.

### 7 · AV6 / stance — **mudou e inverteu o sinal**

Fatia pró-vacina **entre os tweets a que se atribui lado**:

| limiar | n | esquema do artigo (binário) | esquema com classe neutra |
|---|---:|---:|---:|
| >500 RT | 1.559 | 48,4% | 50,0% |
| >100 RT | 6.090 | 56,0% | 57,5% |
| >10 RT | 29.978 | **62,6%** | **61,7%** |

- Deslocamento de **+14,2 p.p.** (binário) e **+11,7 p.p.** (três classes): a
  conclusão **comparativa é robusta ao esquema de anotação**.
- **Aferição:** em >500 RT o instrumento dá 48,4%; o gabarito **humano** do paper
  dá 48,4%. A divergência não vem do classificador.
- **A curva ainda sobe em >10 RT** — não há evidência de convergência nem no
  maior corpus disponível. Não se pode, portanto, nomear a fração mínima que
  estabiliza esta conclusão; só afirmar que **o estrato viral não a estabilizava**.
- **Achado próprio:** a fatia sem posição cresce de 24,6% (>500 RT) para 33,4%
  (>10 RT) — **a viralidade seleciona quem toma partido**, o que explica o
  mecanismo do viés.

⚠ **Ressalvas (as três que limitam esta linha):**
1. O classificador foi validado contra gabarito **apenas no estrato viral**, que
   é onde o gabarito existe.
2. Rotulagem manual cega no estrato baixo indica que os neutros forçados a um
   polo se dividem quase simetricamente, o que **atenua** a estimativa: os 62,6%
   são um **piso**, não um teto (a rotulagem humana da amostra dá 64,7%).
   Ver [CALIBRAGEM_criterio.md](vacinas/data/repl/vacinas2022/CALIBRAGEM_criterio.md).
3. O corpus é a re-coleta de mai/2022, com contagens de RT posteriores às do
   paper: os limiares não selecionam exatamente os mesmos objetos.

---

## 4. O que falta para a tabela fechar

| Linha | Falta | Destrava com |
|---|---|---|
| 8, 9 (heine-xande) | os dados: o Twitter 57,9 M não está em nada acessível | baixar os CSVs do SharePoint do BioBD **ou** decidir pivotar para Instagram/Reddit |
| 10 (stance do Ituassu) | gabarito humano | ~200–300 tweets rotulados à mão (fluxo já validado no caso vacinas) |
| 11 (reddit-buntain) | a coleta dos 13 subreddits de jul/2013 (todas as submissions + comentários, sem o corte de grau) | rodar a Fase 1 — rota **Arctic Shift** (2013 coberto), offline, sem VPN. RB3 não precisa de gabarito humano. Ver [FASE0](reddit-buntain/data/repl/buntain2013/FASE0_descoberta.md) |
| 12 (reddit-massachs) | ~~ler o full text~~ ✅ · ~~o ponto original~~ ✅ **replicado em 18/ago/2026** · **resta** refazer o focus group com limiar de atividade menor (≥5, ≥3, ≥1) | baixar os dumps 2012/2016 (Arctic Shift/Academic Torrents), sem VPN. Ver [FASE2](reddit-massachs/data/repl/massachs2016/FASE2_ponto_original.md) |
| 13, 14 (meta-ads-imigracao) | só a **conta Meta verificada**, que destrava a Ad Library API **e** o teste de retenção | Só a Mariana (documento, 1-3 dias úteis). ✅ Já feitos em 7/ago/2026: full text do CHI 2021 lido, **α publicado reproduzido** (0,763 × 0,76) e **CB2 desambiguado** ([DECISOES_CB2](meta-ads-imigracao/data/repl/metaads2019/DECISOES_CB2.md)). ⚠ **Duas ressalvas já registradas:** as impressões do alvo **não reproduzem** (35 M × 49,8 M pela regra declarada), e anúncios políticos da UE pararam em out/2025 com retenção de 7 anos — o corpus de mar/2019 está no limite. Mitigação = braço Brasil |
| 1, 2 (curva do Ituassu) | ✅ **feita em 07/ago/2026** (300 réplicas/ponto) — e corrigiu o veredito da linha 2 | — |
| 3 (H2 do Ituassu) | ✅ **feita em 07/ago/2026** — e mostrou que H2 não reproduz nem no recorte do próprio artigo | — |
| 4a, 4b, 4c | ✅ nada — medidos em 07/ago/2026 | — |
| *(eixo A do caso vacinas, fora da tabela)* | AV1 por fração de N (com NMI), curva de Lorenz do AV4, AV2 e E3 — nunca rodados | nada; dado local. Ver [auditoria](vacinas/REPLICACAO_CASO_VACINAS.md) §4.1 |

Sem esses itens, **a coluna "fração mínima que estabiliza a conclusão"** — prevista
no protocolo — não pode ser preenchida em nenhuma linha, e por isso não figura na
tabela. O que existe hoje é o par mudou?/convergiu?.

---

## 5. Leitura por tipo de análise (PP3, provisória)

Com 10 linhas fechadas, o padrão que emerge é **um contraste dentro de cada caso**,
não entre casos — e, no caso vacinas, **dentro da mesma afirmação**:

| Comportamento | Análises observadas |
|---|---|
| **Robustas ao volume** (a coleta bastava) | dominância qualitativa de uma classe de fonte (1); concentração/centralidade (5, 5b); composição temática / enquadramento (6) |
| **Sensíveis ao volume** (coletar mais era necessário) | limiares e proporções com corte declarado (2, 3); **peso relativo dos polos** — em posts (4b), em autores influentes (4c) e em conteúdo (7) |
| **Sensíveis à largura do filtro**, ainda que robustas ao volume | composição temática / enquadramento (6), via E3 |
| **Sem veredito** (a medida não é estável o bastante) | cobertura agregada das comunidades (4a) |

Seis leituras provisórias, a confirmar com os casos restantes:

0. **O par mudou?/convergiu? pode atribuir a volume uma falha que é de desenho
   amostral.** É o achado de 07/ago/2026 na linha 2: a conclusão do Ituassu **havia
   convergido** no volume que o artigo coletou (bastariam 200 tweets aleatórios;
   ele coletou 700) e ainda assim o artigo errou, porque amostrou por horário de
   pico. **Proposta de terceira pergunta no protocolo**, aplicável a todo alvo que
   amostrou em vez de analisar o universo: *o esquema de amostragem é não-viesado
   para a quantidade de interesse?* — operacionalizada como "a estimativa publicada
   cabe na banda de subamostras **aleatórias** do mesmo tamanho?". Se não cabe,
   coletar mais é remédio caro para o problema errado.

1. **Afirmações qualitativas e de composição convergem cedo; afirmações sobre
   limiar e equilíbrio de forças, não.** Em ambos os casos executados, o que
   sobreviveu foi a ordenação (quem domina, quais temas prevalecem) e o que caiu
   foi a magnitude que sustentava uma afirmação numérica ("supera 50%", "os polos
   se equivalem").
2. **A sensibilidade é propriedade do tipo de análise, não do trabalho.** O caso
   vacinas mostra os dois desfechos dentro do **mesmo** artigo-alvo e sobre o
   **mesmo** corpus — o que enfraquece a leitura de que um trabalho está ou não
   sub-coletado, e reforça a de que cada análise tem seu próprio limiar.
3. **A robustez depende de que parte da distribuição a afirmação descreve.** No caso
   vacinas, as afirmações sobre a **cauda extrema** (AV2, o topo dos retuítes; AV4, a
   concentração) são estruturalmente imunes à sub-coleta — a cauda é o que qualquer
   coleta captura primeiro. As frágeis são as sobre o **balanço** da distribuição
   (4b, 4c, 7). Não é o tema que decide, é a estatística escolhida.
4. **Volume e largura de filtro são eixos independentes, e podem responder ao
   contrário.** No caso vacinas, o ranking de enquadramentos (6) **converge** ao
   descer o limiar de volume, mas **muda muito** ao trocar o termo-índice
   (E3: *Politics* 32,8% no termo genérico × *Anti-vaccine people* 83,9% em
   "anti-vax"). O balanço pró/anti (7) faz o oposto: **muda** com o volume e **não
   inverte** em nenhum termo. Uma conclusão robusta a um eixo pode ser frágil ao
   outro, e reportar só um deles dá falsa segurança.
5. **Análises independentes podem falhar do mesmo jeito.** No caso vacinas, o
   peso relativo dos polos se move em **três** operacionalizações que não
   compartilham instrumento nem unidade: posts pela topologia (4b), autores
   influentes pela topologia (4c) e tweets pela rotulagem de conteúdo (7).
   Convergência independente é evidência mais forte do que qualquer uma isolada — e
   é o tipo de checagem que o protocolo deveria buscar de propósito nos próximos
   casos. Vale também o inverso: quando uma dessas operacionalizações **reproduz** o
   número publicado (4c no estrato viral, a 0,3 p.p.), ela valida o instrumento das
   outras.

> **Achado transversal, fora do par mudou?/convergiu?:** no caso vacinas, o
> **esquema de anotação** produz ~18 pontos de diferença na descrição do mesmo
> corpus pelo mesmo modelo (58,8% × 35,1% no esquema do artigo; 41,1% × 25,5% ×
> 33,4% sem posição no de três classes), embora a comparação **entre** estratos
> permaneça robusta. E um classificador calibrado contra gabarito aprende a
> **convenção** daquele gabarito — que, por construção, só existe no estrato
> sub-coletado. Ver
> [CALIBRAGEM_criterio.md](vacinas/data/repl/vacinas2022/CALIBRAGEM_criterio.md).

---

## 6. Predições pré-registradas × resultado

Registro honesto das apostas feitas **antes** de rodar (princípio §7 do
[CLAUDE.md](../CLAUDE.md)):

| Caso | Aposta registrada | Resultado | |
|---|---|---|---|
| ituassu | H1, por ser efeito agregado, "provavelmente NÃO MUDA" | **mudou e inverteu** | ✘ refutada |
| vacinas | AV1 e AV4 (agregados de baixa dimensão) "provável CONFIRMA" | AV4 confirmou; de AV1, a cobertura ficou **inconclusiva** e o **equilíbrio não replica** (razão 1,5 × 1,02) | ◐ parcial |
| vacinas | AV5 (ranking de enquadramentos) "provável MUDA" — era *a aposta interessante* | **convergiu**; o que se moveu foi o stance, que não estava na aposta | ✘ refutada |

Duas das três apostas substantivas falharam, e em direções opostas. O desenho
pré-registrado serve exatamente para isso ficar visível.
