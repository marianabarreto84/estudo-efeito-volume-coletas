# MP/MC — o resíduo curado e a sensibilidade da divergência 70,3% × 59%

> Gerado em **07/ago/2026** por `analise/cura_indefinidos.py` e
> `analise/sensibilidade_mp_mc.py` sobre `snapshot_hashtag.sqlite`.
> Números em `sensibilidade_mp_mc.json`; curadoria auditável em
> `indefinidos_curados.csv`. Complementa [RESULTADOS_FASE0_mp_mc.md](RESULTADOS_FASE0_mp_mc.md).

**A pergunta.** A Fase 0 mediu MP **70,3%** na amostra e **72,2%** no universo, contra
os **59%** da Tabela 2 do paper de 2018. A divergência estava registrada como
**sem causa estabelecida**. Este documento testa as alavancas de classificação, uma a
uma, e mede quanto cada uma move o número.

---

## 1. Curadoria do resíduo `indefinido`

**2.082 tweets · 692 hosts** no snapshot inteiro (515 tweets na janela do paper).
Classificados por regra auditável — cada host com seu motivo em
`indefinidos_curados.csv`:

> 📋 Isto substitui a planilha
> [INDEFINIDOS_candidatos_MC.md](INDEFINIDOS_candidatos_MC.md), que listava os
> domínios com uma coluna "MC? (marcar)" para preenchimento à mão e nunca foi
> preenchida. A curadoria por regra cobre os 692 hosts (a planilha listava os da
> janela) e registra o **motivo** de cada um, o que a marcação manual não daria.

| destino | hosts | tweets | % |
|---|--:|--:|--:|
| **MC** — veículo fora da lista fechada das 26 | 552 | 1.631 | 78,3% |
| **não_mídia** — plataforma, institucional, ONG, domínio à venda | 108 | 284 | 13,6% |
| **não_resolvido** — encurtador que não expandiu | 32 | 167 | 8,0% |

**Por que quase tudo vira MC:** sob a convenção **estrita** do paper, MP é uma lista
**fechada** de 26 marcas. Nada fora dela pode virar MP — nem mainstream nacional
(Gazeta do Povo 61, Zero Hora 19, Correio Braziliense 9, Estado de Minas 9) nem
internacional (Guardian 34, ABC.es 14, DW 7, AP 7).

⚠ **Exceção registrada:** a regra "`.org` → ONG" erra com jornalismo hospedado em
`.org`. Abriu-se lista explícita para **Ponte Jornalismo, Portal Vermelho,
RioOnWatch, Diário Liberdade e Esquerda Diário**. O resíduo dessa regra é pequeno
(~160 tweets no total), mas fica declarado.

---

## 2. Sensibilidade — as três alavancas

Janela 13–23/out (37.068 tweets), base = tweets com mídia:

| cenário | MP | MC | **MP%** | gap p/ 59% |
|---|--:|--:|--:|--:|
| base (estrita, sem curadoria) | 15.852 | 6.096 | 72,2% | +13,2 |
| **A** · + curadoria do `indefinido` | 15.852 | 6.503 | **70,9%** | +11,9 |
| **B** · convenção **conceitual** | 16.954 | 5.401 | 75,8% | +16,8 |
| **C** · + regra de coluna ampliada | 15.825 | 6.530 | **70,8%** | +11,8 |
| A+B+C (tudo junto) | 16.922 | 5.433 | 75,7% | +16,7 |

**O que cada alavanca faz:**

- **(A) Curar o `indefinido`: −1,3 p.p.** O resíduo é 1,5% do corpus; não tinha como
  mover muito.
- **(B) Convenção conceitual: +4,9 p.p., na direção ERRADA.** Alargar MP para incluir
  mainstream fora das 26 (Valor, CartaCapital, BBC, WSJ, Gazeta do Povo, Guardian…)
  só **aumenta** MP%. Isso é decisivo: **a convenção estrita já é o mínimo possível
  de MP**, e mesmo assim estamos 12 pontos acima do paper. A divergência **não pode**
  ser explicada por escolha de lista.
- **(C) Regra de coluna/blog ampliada: −0,1 p.p.** Praticamente nada — 27 tweets.

### 2.1 O (C) falha por efeito ausente, não por falta de dado

Era o candidato mais promissor: o §6 de
[RESULTADOS_analise_midia_MV_MH.md](../../RESULTADOS_analise_midia_MV_MH.md)
levantava que blogs hospedados em portal seriam MP para nós e MC para eles, e notava
que o regex subconta ("Miriam Leitão" mora em `oglobo.globo.com/economia/miriam-leitao/`,
sem `/blog` no path). Ampliamos o regex com nomes de colunistas conhecidos.

Mediu-se também se a regra **poderia** agir:

| | n | % |
|---|--:|--:|
| MP com path inspecionável | 15.472 | **97,6%** |
| MP só por host (encurtador *branded* não resolvido, path invisível) | 380 | 2,4% |

→ **97,6% dos links MP têm path visível.** A regra tinha onde agir e não achou.

Testou-se também a outra forma de blog-em-portal, que a regra de *path* não pega:
**blog em subdomínio** (`josiasdesouza.blogosfera.uol.com.br`, `blogdojuca.uol.com.br`).
São **29 tweets em 15.852 MP — 0,18%**. Também desprezível.

O candidato "blog-em-portal" fica **descartado** como explicação da divergência, pelas
duas vias (path e host).

> 📋 Isto substitui a planilha de curadoria manual
> [BLOGS_EM_PORTAL_candidatos.md](BLOGS_EM_PORTAL_candidatos.md), que listava prefixos
> de seção para marcação à mão e nunca foi preenchida. A pergunta que ela existia para
> responder está respondida por medição.

---

## 3. Veredito

**Nenhuma alavanca de classificação fecha o gap.** O melhor cenário dá **70,8%**,
ainda **+11,8 p.p.** dos 59% do paper — e o cenário que mais mexe (B) piora.

Isso **elimina a família inteira de explicações "é convenção de classificação"** e
empurra a causa para fora do nosso dicionário. Restam:

| candidato | estado |
|---|---|
| ~~lista MP / convenção estrita × conceitual~~ | ❌ **descartado** (§2, alavanca B) |
| ~~blog/coluna hospedado em portal~~ | ❌ **descartado** (§2.1) |
| ~~resíduo `indefinido` não curado~~ | ❌ **descartado** (§2, alavanca A: −1,3 p.p.) |
| **link rot** — os 13% de mortos saem da base e podem ser mais MC | ❌ **descartado** — ver [RESULTADOS_FASE0_mp_mc_cdx.md](RESULTADOS_FASE0_mp_mc_cdx.md). Sob a hipótese natural explica **−0,1 p.p.**; e a premissa está invertida (encurtado tem **menos** MC que direto, não mais) |
| **coleta diferente / critério do artigo** | ⏳ **único que resta** — não resolúvel com o material publicado |

O último merece atenção: o nosso **72,2%** é do universo e o **70,3%** é da nossa
amostra reconstruída — os dois praticamente iguais, o que indica que a diferença
**não** é de amostragem do nosso lado. Ou o corpus é outro, ou a classificação deles
diverge da nossa por um critério que o artigo não explicita.

---

## 4. Ressalvas

1. A curadoria do `indefinido` é por **regra**, não por inspeção host a host. Os 692
   hosts estão em `indefinidos_curados.csv` com o motivo de cada um, para auditoria.
2. A lista `CONCEITUAL_EXTRA_MP` do cenário (B) é uma **construção nossa** — o paper
   não define convenção conceitual. Ela serve para medir a direção do efeito, não
   para propor uma classificação alternativa.
3. A regra de coluna ampliada cobre colunistas brasileiros conhecidos; colunista fora
   dessa lista e sem `/blog` no path continua invisível. O teto disso é pequeno
   (§2.1), mas não é zero.
