# Fase 2 — o ponto original do PoliTok-DE, reproduzido (célula TikTok)

> Medido em **18/ago/2026**, **inteiramente offline**: sem API, sem cota, sem credencial.
> Script: [`analise/fase2_politok.py`](analise/fase2_politok.py) · saída:
> `data/politok_de/fase2_politok.json`.

---

## 1. Como a célula TikTok ressuscitou

A rota de coleta morreu (a credencial da Research API do eTC está revogada —
[README §2b](README.md)). O que destravou a célula foi **trocar a pergunta**: em vez de
"como coletar TikTok?", *"que alvo de TikTok publica dados suficientes para replicar sem
coletar?"*.

**Alvo:** Ruiz et al., *PoliTok-DE: A Multimodal Dataset of Political TikToks and
Deletions From Germany*, arXiv 2509.15860 (2025). Dados em
[huggingface.co/datasets/tomasruiz/PoliTok-DE](https://huggingface.co/datasets/tomasruiz/PoliTok-DE),
**CC-BY-4.0, sem gate**.

Os autores **não** liberam mídia nem texto (só mediante pedido avaliado). Mas liberam o
que sustenta as afirmações centrais: o **status de disponibilidade de cada post em várias
datas de checagem**, e as **anotações humanas**. Isso basta.

| arquivo | conteúdo |
|---|--:|
| `saxony_2024/post_ids.parquet` | **195.373** posts × disponibilidade em **3 datas** |
| `federal_2025/post_ids.parquet` | **743.588** posts × disponibilidade em 1 data |
| `saxony_2024/annotations.parquet` | **935** anotações sobre **360** posts, 5 anotadores |

---

## 2. Resultado: **6 das 7 afirmações replicam exatamente**

| # | afirmação do artigo | alvo | medido | veredito |
|---|---|--:|--:|---|
| **PT1** | "over 930,000 posts" | >930.000 | **938.961** | ✅ replica |
| **PT2** | deletados na Saxônia | 18,7% | **18,7%** | ✅ exato |
| **PT3** | deletados na federal | 39,7% | **39,7%** | ✅ exato |
| **PT4** | ~2/3 das deleções são retirada do autor | 66,7% | **65,9%** | ✅ replica |
| **PT5** | deleção **pela plataforma** | 13,0% | **11,6%** | ◐ aprox. (1,4 p.p.) |
| **PT6** | "~1 em 5 posts com intolerância" | 20% | **20,5%** | ✅ replica |
| **PT7** | "maioria com humor" | >50% | **63,0%** | ✅ replica |

### PT5 — a única que não fecha, e por quê

O artigo não publica **quais códigos de status** conta como deleção da plataforma. Os
posts deletados trazem tokens como `status_audit_not_pass`, `cross_border_violation`,
`status_reviewing`, `content_classification`, `author_secret`, `status_deleted`.
Convenções testadas:

| regra | % de todos os posts | erro |
|---|--:|--:|
| A: `audit_not_pass` + `violation` | 4,1% | 8,9 p.p. |
| B: A + `status_reviewing` | 10,3% | 2,7 p.p. |
| D: A + `reviewing` + `content_classification` | 11,5% | 1,5 p.p. |
| **F: D + `copyright`** | **11,6%** | **1,4 p.p.** ✅ mais próxima |

Nenhuma chega aos 13,0%. Fica como **replicação aproximada com convenção não publicada** —
o mesmo padrão do caso YouTube (categorias de canal) e do vacinas (AV1).

### PT6 — replica na convenção *por anotação*, não *por post*

São 935 anotações sobre 360 posts (300 anotados por mais de uma pessoa). Contando **por
anotação**, intolerância dá 20,5% — o "1 em 5" do artigo. Contando **por post, com voto
majoritário**, dá **16,1%**. O artigo não diz qual usa. O mesmo vale para o humor (63,0%
por anotação × 59,2% por post; a conclusão "maioria" sobrevive nas duas).

---

## 3. O eixo temporal — ⚠ **o alvo já o reporta**

> ⚠ **Corrigido em 22/ago/2026, na rodada de revisão 4 → 5.** A primeira leitura
> deste caso tratou o eixo temporal como achado próprio. **Não é.** O full text do
> PoliTok-DE traz, no **Apêndice C, Tabela 5**, um **painel dos mesmos 102.953
> posts** rechecados a 1, 3 e 4,5 meses — 6,3% / 17,4% / 20,5% — e a frase
> explícita de que a fatia deletada cresce quanto mais se espera. O que é nosso:
> (a) a **verificação independente** desse painel, que reproduz 6,3 e 17,4 exatos e
> difere 0,4 p.p. no último ponto; (b) o diagnóstico da **base misturada** (abaixo);
> (c) a **incorporação do eixo ao protocolo** da dissertação, com as duas perguntas
> mudou?/convergiu? aplicadas a ele.

> ⚠ **E a série mudou.** O painel estrito (estado válido nas três datas, n=100.926)
> dá **6,3% → 17,4% → 20,9%**. A série 6,3 / 17,3 / 18,7 que este documento
> reportava **mistura bases**: os dois primeiros pontos são dos rechecados naquela
> data, o terceiro é da coleção inteira. Só o painel é curva. Bloco
> `painel_temporal` em `fase2_politok.json`.

> ⚠ **E “assenta” caiu.** A coleta federal do mesmo artigo, verificada aos 16
> meses, marca 39,7% — quase o dobro dos 20,9% da estadual aos 4,5 meses. Ou as
> duas não são comparáveis (o artigo avisa que não as compara diretamente), ou a
> curva não havia assentado. **Convergência no eixo temporal: em aberto.**

### 3.1 A série, como estava

A Saxônia tem **três datas de checagem**, e a taxa de deleção muda assim:

| data da checagem | dias após a eleição | deletados (todos) | deletados (**só os rechecados**) |
|---|--:|--:|--:|
| 02/out/2024 | 31 | 3,3% | **6,3%** |
| 10/dez/2024 | 100 | 9,5% | **17,3%** |
| 13/jan/2025 | 134 | 18,7% | **18,7%** |

⚠ **A coluna certa é a última.** Nas duas primeiras datas, cerca de 46% dos posts
constam como `NOT_RESCRAPED` — não foram verificados. Calcular sobre o total inclui
esses posts no denominador como se fossem "não deletados", o que **subestima** a taxa.
Sobre a base efetivamente rechecada, a série é **6,3% → 17,3% → 18,7%**.

**A taxa triplica em pouco mais de três meses sobre o mesmo conjunto de posts** — não é
efeito de coletar mais, já que o denominador é o mesmo; é efeito de **coletar depois**.

**E ela estabiliza.** O salto está entre outubro e dezembro (6,3% → 17,3%); de dezembro
a janeiro o movimento é de 1,4 ponto. Isto é: o eixo temporal tem **curva de
convergência própria**, com a mesma forma da curva de volume — sobe rápido e assenta.
A pergunta "a partir de quando a medida estabiliza?" é irmã de "a partir de que volume
estabiliza?", e o protocolo da dissertação hoje só faz a segunda.

**Por que isso importa para a tese.** O desenho da dissertação pergunta *mudou?* e
*convergiu?* ao longo do **volume**. Este caso mostra um segundo eixo, independente e de
magnitude comparável: o **momento** da coleta. Um trabalho que medisse deleção em out/2024
publicaria **6,3%** e outro, em jan/2025, publicaria **18,7%** — ambos corretos, ambos
sobre o mesmo corpus, com um fator **3,0×** entre eles. Nenhuma quantidade de dados
resolve isso; só a data resolve.

Isso soma à leitura já consolidada de que **volume e largura de filtro são eixos
independentes** (§4.8 do `ESTADO.md`, caso vacinas). Agora são **três** eixos: volume,
filtro e **momento**. Proposta: entrar no `corpo.tex` junto da "terceira pergunta" (§4.9),
como quarta.

⚠ A ressalva do `NOT_RESCRAPED` foi incorporada acima, na coluna da base rechecada.
Registrada aqui a correção: a primeira leitura deste documento reportou 3,3% → 18,7%
(fator 5,7×) sobre o total; o correto é **6,3% → 18,7% (fator 3,0×)** sobre a base
comparável.

---

## 4. O que isto entrega, e o que não entrega

**Entrega:** a célula TikTok deixa de estar vazia. Há alvo, há gabarito público, há ponto
original replicado (6/7), e há um achado próprio (o eixo temporal).

**Não entrega:** o eixo "coletar mais" no sentido estrito. A expansão exigiria a Research
API — que está morta para nós. O que este caso oferece no lugar é o **eixo temporal**,
que é medível com o que está publicado.

**Ressalva de tração, declarada:** arXiv, 2025, poucas citações — como todos os alvos de
TikTok e YouTube disponíveis. Ver [ALVOS_candidatos.md](ALVOS_candidatos.md) §1 para o
achado estrutural de que tração e análise computacional com sub-coleta declarada não
coexistem nessas duas redes.
