# RB3 — o recorte do artigo reconstruído sobre o nosso dado

> Medido em **25/set/2026**, a partir de uma pergunta da Mariana: *"não teria como
> chegar no que seria os 3% de forma equivalente? Tipo ver o quanto seria essa
> porcentagem só entre os posts top 100 de cada comunidade?"*
> Script: [`analise/rb3_recorte_artigo.py`](../../../analise/rb3_recorte_artigo.py) ·
> snapshot: `snapshot_buntain.sqlite` · JSON: `rb3_recorte_artigo.json`.
>
> ⚠ **A dissertação já está com a banca e não foi alterada.** Este documento existe
> para a preparação da defesa. Ver [ESTADO.md §4.31](../../../../../ESTADO.md).

---

## 1. A pergunta

[RESULTADOS_RB3.md](RESULTADOS_RB3.md) e a `tab:reddit-rb3` do `corpo.tex` contrastam
**3% (artigo)** com **57,6% (universo, ≥20 mensagens)**. Nessa comparação **duas coisas
variam ao mesmo tempo**: o recorte da coleta *e* a fonte do dado. Como a Fase 1 coletou
tudo, o recorte do artigo é um **subconjunto** do nosso snapshot e pode ser
reconstruído por cima dele — o que fixa o dado e deixa variar só o recorte.

## 2. Como o corte do artigo tem de ser lido

A [ficha do alvo](../../../ARTIGO_BUNTAIN_alvo.md) §1.1–1.2 registra que o grafo é
**dirigido e por subreddit**, e que o corte é de **≥20 arestas de saída**, restando
**279 usuários em 10 dos 13 subreddits** — três caíram *"por não ter usuário acima do
limiar"*. Esse detalhe é decisivo: um subreddit só pode cair por essa razão se o corte
for avaliado **dentro de cada rede**, e não sobre um grafo único. A réplica original
aplicou um corte **global**, de ≥20 **mensagens publicadas** — diferença já declarada
como ressalva em [RESULTADOS_RB3.md §6](RESULTADOS_RB3.md) e no `corpo.tex`, mas nunca
quantificada.

## 3. A reconstrução bate com o artigo

Top-100 submissões por subreddit (por score) × 200 comentários de cada (por score),
arestas de resposta, grau de **saída** ≥20 **por rede**:

| | artigo | reconstrução |
|---|--:|--:|
| participantes | 279 | **259** |
| subreddits com alguém acima do limiar | 10 de 13 | **11 de 13** |
| em >1 comunidade | 7 = **2,5%** | 2 = **0,8%** |

259 contra 279, com o mesmo punhado de subreddits esvaziando: o pipeline do artigo é
reproduzível a partir do nosso dado. **A resposta à pergunta é sim** — os ~3% são
recuperáveis, e o que os produz é o recorte combinado ao corte por rede.

## 4. O que isso faz com os 57,6%

Mantendo o corte do artigo (saída ≥20 por rede) e soltando só a coleta:

| recorte | participantes | em >1 rede | % |
|---|--:|--:|--:|
| artigo: top-100 × 200 | 259 | 2 | 0,8% |
| top-100 × todos os comentários | 761 | 30 | 3,9% |
| todas as submissões × 200 | 2.777 | 93 | 3,3% |
| **universo** | **3.889** | **163** | **4,2%** |

Sob a operacionalização do próprio artigo, **coletar tudo leva de ~1% a ~4%, não a
57,6%**. O fator 19× registrado no `corpo.tex` vem em boa parte da **troca de
definição** de "participar de mais de uma comunidade" — de *ter ≥20 arestas de saída em
cada rede* para *ter ≥20 mensagens no total e ter postado em mais de um subreddit* —, e
não apenas de coletar mais.

Com o corte **global** (o da réplica) aplicado ao recorte do artigo, o valor é **29,0%**
(1.190 participantes, 345 multi), e a faixa vai de 23,6% a 29,0% conforme a convenção
adotada para "20 arestas" e para a ordenação dos 200 comentários. Ou seja: o recorte
responde por metade da distância; a outra metade é definição.

## 5. A comparação que segura população e definição

Fixando a população nos **259** participantes que o recorte do artigo identifica, e
mudando **apenas o que a coleta deixa ver**:

| os mesmos 259 participantes | em >1 subreddit |
|---|--:|
| qualificados em >1 rede — *o que o artigo conta* | 2 = **0,8%** |
| presentes em >1 subreddit, dentro do recorte | 70 = 27,0% |
| **presentes em >1 subreddit, no universo** | **107 = 41,3%** |

Distribuição real dessas 259 pessoas nos 13 subreddits: **152** em um só, 58 em dois,
31 em três, 14 em quatro, 4 em cinco.

Esta é a formulação mais defensável do achado. A população é a do artigo, o tema é o do
artigo, a pergunta é a do artigo, e a única coisa que muda é a coleta: dos participantes
que o próprio artigo analisou, **41,3% estavam ativos em mais de uma das treze
comunidades**, contra os 2,5% que a coleta dele permitia enxergar. A conclusão
substantiva — a de que os papéis são locais — continua não sobrevivendo; o que muda é a
magnitude que se pode reivindicar e o enunciado que a sustenta.

## 6. Consequência para o par *mudou? / convergiu?*

- **mudou?** — **sim**, em qualquer das leituras: 0,8% → 4,2% com a definição do artigo
  fixa; 2,5% → 41,3% com a população do artigo fixa. A direção nunca se inverte.
- **convergiu?** — a leitura de [RESULTADOS_RB3.md §4](RESULTADOS_RB3.md) (estabiliza em
  k≈10–20) vale para a curva do corte **global**. Sob o corte por rede a curva é outra e
  não foi levantada.
- ⚠ **A afirmação de que "nenhum limiar aplicado ao universo devolve os 3%"**
  (`corpo.tex` §sec:rb3-curva e legenda da `fig:curva-rb3`) vale para o corte global,
  mas **não** para o corte por rede: sob ele o universo dá 4,2%, e o recorte do artigo
  dá 0,8%. Os 3% são recuperáveis — pelo recorte, que é justamente o que o caso
  argumenta.

## 7. O que não muda

Nada nos números publicados está errado: 3%, 15,2% e 57,6% são o que sempre foram, e
cada um mede o que sua linha declara. O que este documento acrescenta é que a **linha do
artigo e a linha do universo não compartilham a operacionalização**, e que a magnitude
do efeito depende de qual delas se adota.
