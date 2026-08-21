# MP/MC — o teste de link rot: CDX do Internet Archive e a via indireta

> Gerado em **07/ago/2026** por `analise/cdx_links_mortos.py` e
> `analise/proxy_link_rot.py`. Números em `cdx_mortos.json` e `proxy_link_rot.json`.
> Fecha o último candidato aberto de
> [RESULTADOS_FASE0_mp_mc_sensibilidade.md](RESULTADOS_FASE0_mp_mc_sensibilidade.md) §3.

**A hipótese.** 13% dos links não resolvem (`nao_resolvido`) e saem da base MP/MC.
Se os mortos fossem sistematicamente mais MC que os vivos, a base resolvida estaria
enviesada a favor de MP, e parte do gap **72,2% × 59%** se explicaria. O §6 de
[RESULTADOS_analise_midia_MV_MH.md](../../RESULTADOS_analise_midia_MV_MH.md) registrava
isso como **hipótese não testada** (depois de retratar uma versão mais forte dela).

---

## 1. Via direta: CDX do Internet Archive — **o instrumento não alcança**

Amostra de 150 links mortos (semente 20141026), consulta à API CDX pública:

| | n | % |
|---|--:|--:|
| amostrados | 150 | — |
| **erro de consulta** (rate limiting) | **72** | 48,0% |
| consultas válidas | 78 | — |
| **sem captura no Archive** | **74** | **94,9% das válidas** |
| snapshot sem destino legível | 3 | — |
| **alvo recuperado** | **1** | **1,3% das válidas** |

O único alvo recuperado classificou como `indefinido` — nem serve de dado.

**Por que falha:** o Internet Archive arquiva **páginas de destino**, não
**redirecionadores individuais**. Encurtadores como `zhora.co/1uM6FtT`, `abr.ai/…`
e `glo.bo/…` não são rastreados. Confirmado também em teste manual antes da corrida.

⚠ **Duas ressalvas de execução, ambas registradas:**

1. **Rate limiting severo.** Os erros cresceram ao longo da corrida
   (4 → 11 → 31 → 49 → 72), reduzindo a amostra efetiva de 150 para 78. Não se
   insistiu com mais requisições: o serviço é público e já estava estrangulando.
2. **Erro nunca foi contado como ausência.** A primeira versão do script usava a API
   `archive.org/wayback/available`, que respondeu **429**, e o código engolia a
   exceção — o que teria produzido um **falso 0% de arquivamento** apresentado como
   resultado. Corrigido para o CDX, com as duas contagens separadas.

**Veredito:** o teste foi executado e **a via não alcança**. A hipótese de link rot
fica **não testável pelo CDX** — o que é diferente de descartada.

---

## 2. Via indireta: encurtados-sobreviventes × links diretos

Se não dá para recuperar os mortos, dá para olhar quem se parece com eles. Janela
13–23/out (37.068 tweets):

| tipo do 1º link | MP | MC | **MP%** | **MC%** | n com mídia |
|---|--:|--:|--:|--:|--:|
| **direto** | 2.464 | 2.647 | **48,2%** | **51,8%** | 5.111 |
| **encurtado sobrevivente** | 8.680 | 3.240 | **72,8%** | **27,2%** | 11.920 |
| encurtado *branded* sem path (glo.bo, oesta.do…) | 4.708 | 209 | 95,7% | 4,3% | 4.917 |
| **encurtado morto** (sem classe) | — | — | — | — | **4.926** |

### 2.1 ⚠ O achado contraria a premissa da hipótese

O §6 do doc de mídia supunha que **encurtado carrega mais MC que direto**
(34,2% × 23,7%). **Medido aqui, é o inverso:** MC **27,2%** nos encurtados
sobreviventes contra **51,8%** nos diretos.

Faz sentido: encurtador é ferramenta de quem publica em volume — veículo grande,
agregador, bot de redação. Link direto colado à mão tende a vir de fonte menor.

**Consequência:** se os mortos se parecem com os encurtados que sobreviveram, eles
são **mais MP**, não mais MC — o que **afastaria** a réplica do paper, não a
aproximaria. A hipótese de link rot não só não se confirma: ela aponta ao contrário.

### 2.2 Projeção condicional

Redistribuindo os 4.926 mortos sob três suposições:

| suposição sobre os mortos | MP% resultante | explica do gap de 13,2 p.p. |
|---|--:|--:|
| **como os encurtados sobreviventes** (a natural) | **72,3%** | **−0,1 p.p. — nada** |
| como os links diretos | 67,8% | 4,4 p.p. (~33%) |
| **extremo: 100% MC** | **59,0%** | 13,2 p.p. (100%) |

O limite teórico bate **exatamente** com o valor publicado — mas exige que **todos os
4.926** links mortos fossem mídia complementar, o que nenhuma evidência sustenta e
que a §2.1 torna implausível.

⚠ **Viés de sobrevivência, declarado:** estimar os mortos pelos encurtados que
sobreviveram compara populações diferentes por construção. Isto é uma **projeção
condicional**, não uma medida. Serve para dimensionar, não para provar.

---

## 3. Veredito do eixo MP/MC

| candidato para o gap 72,2% × 59% | estado |
|---|---|
| convenção de lista MP (estrita × conceitual) | ❌ descartado — alargar MP **piora** |
| blog/coluna hospedado em portal | ❌ descartado — 97,6% dos paths visíveis, efeito ausente |
| resíduo `indefinido` não curado | ❌ descartado — move −1,3 p.p. |
| **link rot** | ❌ **descartado sob hipótese natural** (−0,1 p.p.); só fecharia no limite implausível de 100% MC |
| **coleta diferente / critério do artigo** | ⏳ **único que resta** |

**Todas as explicações que dependiam da nossa classificação foram eliminadas.** O que
sobra está do lado do artigo: ou o corpus dele difere do acervo preservado, ou a
codificação MP/MC dele segue um critério que o texto não explicita. Reforça isso o
fato de a nossa amostra reconstruída (70,3%) e o nosso universo (72,2%) darem
praticamente o mesmo — **a diferença não está do nosso lado**.

Como o artigo de 2018 não publica a lista de domínios por classe nem o gabarito dos
2.200 tweets sorteados, a divergência **não é resolúvel com o material publicado**.
Fica registrada como limite de reprodutibilidade do alvo.
