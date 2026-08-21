# Resultados da análise de mídia — MV × MH (#Eleições2014)

> Eixo **mídia** do paper de 2015 (Ituassu & Lifschitz), taxonomia **MV/MH** —
> hoje o **par** com o eixo MP/MC do paper de 2018. Cada tweet é classificado pelo
> domínio do **1º link** como **Mídia Vertical (MV)** — grande mídia, fluxo "de cima
> para baixo" — ou **Mídia Horizontal (MH)** — nicho/individual/blogs/redes sociais.
> Tweets **sem link nenhum** são **NDA**. Eixo 100% determinístico (não depende de stance).
>
> Scripts: `analise/analisa_midia.py`, `analise/stats_midia.py`, `analise/intra_autor.py`,
> `analise/compara_escopo.py`; dicionário `core/midia_dominios.py`; 1º link efetivo
> `core/extrai_links.py`. Ver também [PAPER2018_palabra_clave.md](PAPER2018_palabra_clave.md)
> e [REPLICACAO_CASO_COMPOS2014.md](REPLICACAO_CASO_COMPOS2014.md).
>
> ⚠ **Leia junto:** a curva `A(volume)` de 07/ago/2026
> ([RESULTADOS_FASE3_curva_midia.md](data/repl/compos2014/RESULTADOS_FASE3_curva_midia.md))
> **corrige o diagnóstico de H1**: a conclusão já havia convergido em n≈200, e a
> falha do artigo é **viés do esquema de amostragem**, não volume insuficiente.
>
> **Consumidores destes números** (propagar ao mudar qualquer valor abaixo):
> as linhas 1–3 da [tabela mestre](../RESULTADOS_tabela_mestre.md) e o capítulo
> `cap:caso-twitter` de `escrita/dissertacao/corpo.tex` — alinhado ao canônico em
> **07/ago/2026**.

---

## 0. ⚠ Correção desta versão (jul/2026) — leia antes dos números

A versão anterior deste relatório tinha um **defeito de pipeline**: ela lia só o campo
estruturado `links` e ignorava URLs embutidas **no texto** do tweet. Em ~9% dos tweets
(retweets nativos de 2014) o `t.co` só existe no texto — e eles eram contados como
**NDA ("opinião pura, sem link")** quando na verdade **compartilharam um link** (hoje,
em geral, morto). O pipeline agora usa o **1º link efetivo** (campo `links`; se vazio,
1ª URL do texto) e expande esses encurtadores (`pipeline/expandir_links_texto.py`).

**O que mudou:**

| medida (universo on-hashtag, N=140.909) | antes | **corrigido** |
|---|--:|--:|
| NDA (sem link nenhum) | 34,3% | **26,9%** |
| não_resolvido (link morto) | 5,7% | **13,1%** |
| MV | 47,1% | 47,1% |
| MH | 9,3% | 9,4% |
| cobertura (classe definida) | 94,3% | **86,9%** |

**O que sobreviveu intacto:** a dominância MV (§1), **H1** (§2) e o colapso da MV no
escopo amplo (§3) — nenhum número desses mudou. **O que encolheu:** tudo que se apoia
no NDA — a tese "as pessoas comentam em vez de compartilhar" e a prova intra-autor
(OR **4,47 → 2,91**). O efeito continua real e altamente significativo, mas era
**superestimado em ~35%**. Detalhe em §3.

> **Leitura de fundo:** o resíduo de **13,1% de link morto** não é ruído — é o limite
> de reprodutibilidade. Esses tweets compartilharam mídia que **não dá mais para
> classificar** (o `t.co` de 2014 morreu). Toda proporção MV/MH abaixo é calculada
> sobre a **base resolvida**, e por isso é um **limite**, não um ponto — ver §6.

---

## 1. Resultado principal — a mídia vertical domina, ~5 para 1

Universo `A_mais_hashtag` (#Eleições2014), **140.909 tweets**, pós-classificação:

| classe | tweets | % |
|---|--:|--:|
| **MV** (mídia vertical) | 66.370 | 47,1% |
| **NDA** (sem link) | 37.921 | 26,9% |
| **nao_resolvido** (link morto) | 18.480 | 13,1% |
| **MH** (mídia horizontal) | 13.233 | 9,4% |
| indefinido (domínio não mapeado) | 4.905 | 3,5% |

Olhando **só o conteúdo que aponta para mídia identificável** (MV ou MH):

> **MV 66.370 × MH 13.233 → 83,4% MV contra 16,6% MH.**
> Entre os tweets com link de mídia classificável, a **vertical supera a horizontal em
> ~5 para 1**. É a espinha dorsal da tese do paper.

**Estatística:** P(MV | há mídia) = **83,4%** (IC95% Wilson 83,1–83,6; n = 79.603). Contra o
acaso (H₀: P = 50%): **z = 188,3, p ≈ 0**.

⚠ **Ressalva de viés — DIREÇÃO CORRIGIDA em 07/ago/2026.** Os 13,1% de link morto saem
dessa base. A versão anterior afirmava que links **encurtados** carregam **mais MH**
que os diretos, e concluía que os 83,4% seriam um **teto**. **Medido, é o inverso:**

| tipo do 1º link | MV% | MH% | n com mídia |
|---|--:|--:|--:|
| direto | 62,6% | **37,4%** | 16.123 |
| encurtado sobrevivente | 88,7% | **11,3%** | 63.480 |
| encurtado morto (fora da base) | — | — | 18.480 |

Encurtador é ferramenta de quem publica em volume (veículo grande, agregador), logo
carrega **menos** MH, não mais. Se os mortos se parecem com os encurtados vivos, incluí-los
**subiria** a MV — os 83,4% são então um **piso**, não um teto. A conclusão substantiva
(MV domina ~5:1) fica **mais** segura, não menos.
*(Mesmo padrão medido no eixo MP/MC: MC 27,2% nos encurtados × 51,8% nos diretos —
ver [link rot](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_cdx.md) §2.1.)*

---

## 2. H1 — "retweet de mídia vertical > 50%" se sustenta? **Não.**

O paper afirma **H1: RTMV (retweets cujo 1º link é MV) passa de 50%** em quase toda a
semana. Testamos em dois níveis. **Nenhum número desta seção mudou com a correção.**

### Amostra reconstruída (100 tweets/dia nos horários de pico, 19–25/out)

| dia | n | MV | MH | NDA | RTMV% | MV% | MH% |
|---|--:|--:|--:|--:|--:|--:|--:|
| **TOTAL** | **700** | 384 | 71 | 111 | **48,3%** | **54,9%** | 10,1% |

→ RTMV agregado **48,3%** (IC95% Wilson 44,6–52,0; n = 700). O intervalo **contém 50%** e o
teste não rejeita H₀ = 50% (z = −0,9, p = 0,36 bicaudal); no unicaudal "RTMV > 50%",
p = 0,82. Ou seja: **mesmo na amostra não há evidência de que ultrapasse 50%**.

### Universo completo on-hashtag (mesma janela)

| | n | MV | MH | NDA | RTMV% | MV% | MH% |
|---|--:|--:|--:|--:|--:|--:|--:|
| **TOTAL 19–25/out** | **32.193** | 13.954 | 3.365 | 9.922 | **36,1%** | **43,3%** | 10,5% |

→ RTMV agregado **36,1%** (IC95% Wilson 35,6–36,6; n = 32.193). Decisivamente **abaixo** de
50% (z = −49,9, p ≈ 0). **H1 não se sustenta em escala.**

### Achado central — o efeito-de-volume

A amostra de 100/dia nos horários de pico **superestima** a dominância de RT de mídia
vertical: RTMV cai de **48,3% → 36,1%** (**−12,2 p.p.**), com **ICs disjuntos**
(44,6–52,0 vs 35,6–36,6). Não é flutuação amostral — é diferença real entre o recorte
por pico e o universo. **A conclusão do paper é artefato da amostragem por pico.**

---

## 3. Efeito do escopo temático (E2) — alargar hashtags dilui a MV

Comparando a janela 19–25/out sob dois escopos (volume e janela fixos no máximo):

| escopo | n | MV% | MH% | NDA% | RTMV% |
|---|--:|--:|--:|--:|--:|
| **A_mais_hashtag** (só #Eleições2014) | 32.193 | 43,3% | 10,5% | 30,8% | 36,1% |
| **A_mais_full** (todas hashtags eleitorais) | 57.610 | 24,9% | 10,0% | 47,1% | 20,4% |

→ ao abrir o escopo, a **MV cai 18,4 p.p.** e o **NDA sobe para 47,1%**. A MH quase não
muda. **Quanto mais amplo o recorte, menos compartilhamento de grande mídia.**

### Decomposição NÚCLEO × COMPLEMENTO

- **NÚCLEO** — tweets com #Eleições2014 (n=32.193);
- **COMPLEMENTO** — só hashtag partidária, **sem** #Eleições2014 (n=25.417).

| grupo (19–25/out) | MV% | MH% | NDA% |
|---|--:|--:|--:|
| **NÚCLEO** | **43,3%** | 10,5% | 30,8% |
| **COMPLEMENTO** | **1,5%** | 9,5% | **67,7%** |

- **ΔMV = 41,9 p.p.** (43,3% → 1,5%; IC95% 41,3–42,4; z = 115,5; p ≈ 0; **Cohen's h = 1,20**, *enorme*). ✔ *não mudou com a correção*
- **ΔNDA = 36,9 p.p.** (30,8% → 67,7%; IC95% 36,2–37,7; z = −88,2; p ≈ 0; **h = 0,76**, *grande*). ↓ *antes: 40,0 p.p., h=0,83*
- **ΔMH = 1,0 p.p.** (10,5% → 9,5%; z = 3,9; p = 7,9×10⁻⁵; **h = 0,03**, *trivial*).
- Distribuição das 5 classes: **χ²(4) = 14.623, p ≈ 0, Cramér's V = 0,50**.

Alargar o escopo **desloca conteúdo de MV para NDA**, sem mexer na MH.

### Prova intra-autor — o mesmo autor, nos dois grupos ⚠ *revisada*

Desenho pareado: os **mesmos indivíduos** que tuitaram no NÚCLEO **e** no COMPLEMENTO
(script `analise/intra_autor.py`). Cada autor é seu próprio controle → composição de
autores 100% removida.

- Na janela há **28.588 autores**; **1.752 (6,1%)** aparecem nos **dois** grupos, e
  respondem por **18,4%** dos tweets.
- **Esses mesmos autores** têm NDA de **25,9%** nos tweets com #Eleições2014 e **53,3%**
  nos tweets só-partidária. *(antes: 31,6% → 68,0%)*
- **OR de Mantel-Haenszel estratificado por autor = 2,91** (IC95% 2,63–3,23).
  *(antes: 4,47 [4,01–4,98] — **superestimado em ~35%**)*
- Autor a autor (≥3 tweets em cada grupo, n = 257): **174 aumentam** o NDA no
  COMPLEMENTO, **51 diminuem**, 32 empatam; mediana por autor **20% → 50%**.
  **Wilcoxon: p = 3,0×10⁻¹⁸**; teste de sinais: p = 3,3×10⁻¹⁷.

**Conclusão (mantida, com magnitude menor):** não são autores diferentes usando tags
diferentes — **é o mesmo autor trocando de registro**. Com #Eleições2014 ele compartilha
matéria; com hashtag partidária, opina sem link. O efeito é **real e altamente
significativo**, mas ~35% menor do que reportamos antes: parte do que parecia
"opinião sem link" era **link compartilhado que morreu**.

### Controle por tipo de autor (proxy `status_verificado`)

- **Verificados:** NDA núcleo 21,5% × complemento 78,9% → **OR = 13,7** (IC95% 10,7–17,5)
- **Não-verificados:** NDA núcleo 31,4% × complemento 67,5% → **OR = 4,5** (IC95% 4,4–4,7)
  *(antes 5,5)*
- **OR comum de Mantel-Haenszel = 4,7** *(antes 5,6)*

O efeito da hashtag sobre o NDA persiste forte **dentro de cada estrato** → a diluição é
**função da hashtag**, não composição de autores.

---

## 4. Nota metodológica — recuperação de links (duas etapas)

1. **Encurtadores no campo `links`** (`pipeline/expandir_links.py`): links de 2014 vinham
   encurtados (`bit.ly`, `goo.gl`, `ow.ly`…); sem expandir, todo 1º link curto ficaria
   sem classe. A expansão via HTTP precede a classificação.
2. **URLs só no texto** (`pipeline/expandir_links_texto.py`, **novo**): ~9% dos tweets têm
   `t.co` apenas no texto (retweet nativo). Antes viravam NDA por engano.

**Teto de recuperação:** dos ~5,4 mil `t.co` distintos achados no texto, **a grande maioria
está morta** (`goo.gl` foi descontinuado em ago/2025; tweets de 2014 apagados). Cache atual:
**11,3 mil URLs** — `ok` 2.184 · `morto` 7.448 · `erro` 1.123. Daí o resíduo de **13,1%**
`nao_resolvido`, que **não é recuperável**.

---

## 5. Síntese

- **MV domina MH ~5:1** entre conteúdo com link classificável — 83,4% (IC95% 83,1–83,6);
  z = 188,3. ✔ tese central do paper **sobrevive** (e o resíduo joga a favor dela,
  não contra — ver a ressalva de direção em §1).
- **H1 (RTMV > 50%)** ✘ **não se sustenta**: amostra 48,3% (IC 44,6–52,0), não difere de
  50% (p = 0,36); universo 36,1% (IC 35,6–36,6), decisivamente abaixo. ICs disjuntos.
- **Alargar o escopo** (E2) desloca MV→NDA: ΔMV = 41,9 p.p. (h = 1,20), sem mexer na MH
  (h = 0,03). A diluição é **função da hashtag**, comprovada **intra-autor** (OR 2,91).
- **NDA é menor do que pensávamos** (26,9%, não 34,3%): parte do "comentário sem link"
  era link morto. A tese "as pessoas comentam em vez de compartilhar" **continua de pé,
  porém mais fraca**.

---

## 6. O resíduo de 13,1% — o que sabemos e o que **não** sabemos

**13,1% dos tweets compartilharam um link que hoje não resolve** (`t.co` morto). Como
esses tweets ficam fora da base MV/MH, toda proporção acima é calculada sobre a **base
resolvida** — e a pergunta é se essa base é enviesada.

**O que está medido:**
- ~~Link **encurtado-resolvido** carrega mais mídia horizontal que link **direto**
  (no eixo MP/MC: MC 34,2% vs 23,7%). Encurtado é o que morre.~~
  ⚠ **REVOGADO em 07/ago/2026.** Medido de novo sobre o pipeline corrigido
  ([proxy_link_rot](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_cdx.md) §2), o
  resultado é o **inverso**: MC **27,2%** nos encurtados sobreviventes contra
  **51,8%** nos links diretos. Encurtador é ferramenta de quem publica em volume
  (veículo grande, agregador), então carrega **mais MP**, não mais MC.
- Entre os encurtados-resolvidos classificados MP, **5,6%** têm path de blog/coluna
  (Reinaldo Azevedo/*Veja*, Fausto Macedo/*Estadão*, Mônica Bergamo/*Folha*) — que o
  paper de 2018 codifica como **complementar**, e nossa regra de domínio chama de MP.
  Nos links diretos essa taxa é 1,4%. *(E o regex subconta: "Miriam Leitão" é
  `oglobo.globo.com/economia/miriam-leitao/`, sem `/blog` no path.)*

> ### ⚠ O que NÃO está estabelecido — retratação
> Uma versão anterior desta seção afirmava que **o link rot destrói o sinal
> horizontal/complementar** e que por isso o lado frágil não reproduz. **Isso foi
> superafirmado.** O raciocínio tem dois furos:
> 1. **Viés de sobrevivência:** estimar os links *mortos* a partir dos encurtados que
>    *sobreviveram* compara populações diferentes por construção.
> 2. **A magnitude não fecha:** aplicando o próprio proxy (morto ≈ 34% MC), a MC do
>    universo iria de 22% para **24,5%** — ~2 p.p. de um gap de ~16 p.p. Só o cenário
>    extremo "os mortos são quase todos MC" reconciliaria, e **não há evidência disso**.
>
> **Estado real:** a divergência entre a nossa medição e a do paper de 2018 está
> **em aberto**. Candidatos, em ordem de promessa: (a) **blogs hospedados em portal**
> classificados MP por nós e MC por eles (medido ≥5,6% nos encurtados, subcontado);
> (b) diferença entre a coleta do eTC e a coleta deles; (c) link rot — **hipótese não
> testada**, hoje explicando ~2 p.p.
>
> **Teste de (c): ✅ FEITO em 07/ago/2026 — e (c) está descartado.** A CDX do
> Internet Archive **não alcança** (1 alvo recuperado em 78 consultas válidas: o
> Archive guarda páginas de destino, não redirecionadores). A via indireta
> (encurtados sobreviventes × diretos) mostrou que a **premissa estava invertida** e
> que, sob a suposição natural, o link rot explica **−0,1 p.p.** do gap. Detalhe em
> [RESULTADOS_FASE0_mp_mc_cdx.md](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_cdx.md).
>
> Com (a) e (c) descartados — e (a) também foi, por medição direta, ver
> [sensibilidade](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md) —
> **resta apenas (b): a coleta/critério do artigo**.

**Implicação prática (independente de qual candidato vença):**
- **Robustas** (não dependem do resíduo): H1 refutada; o colapso da MV no escopo amplo;
  a dominância *qualitativa* da MV.
- **Limite, não ponto**: os **83,4%** de MV (§1) são calculados sobre a base resolvida.
  ⚠ **Corrigido em 07/ago/2026:** medido o resíduo por tipo de link, ele empurra a MV
  **para cima**, não para baixo (encurtado tem 11,3% de MH contra 37,4% do direto) —
  logo os 83,4% são um **piso**, não um teto. O efeito dos blogs-de-portal, que
  puxaria no sentido oposto, foi medido e é desprezível (§2.1 da
  [sensibilidade](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md)).

---

## 7. Nota estatística (métodos)

- **Proporções:** IC 95% por **Wilson**. **Valor fixo** (RTMV vs 50%): **z de uma
  proporção** (unicaudal para H1, fiel à direção do paper). **Dois grupos**: **z de duas
  proporções** + IC da diferença; efeito por **Cohen's h** (0,2 peq · 0,5 méd · 0,8 gr).
- **Distribuição de classes** (2×5): **qui-quadrado** + **Cramér's V**.
- **Efeito ajustado pelo autor:** **OR** por estrato + **OR comum de Mantel-Haenszel**.
- **Desenho intra-autor (pareado):** OR de **MH estratificado por autor** (IC por
  Robins-Breslow-Greenland) + **Wilcoxon** pareado e **teste de sinais**.
- p reportado como "≈ 0" abaixo do limite de ponto flutuante (|z| ≳ 40).

---

## 8. Confronto com o paper de 2015

> **Escopo:** apenas o eixo **mídia** (MV/MH/RTMV), determinístico. **Stance (EA/ED),
> composição dos públicos (226/284/156) e temas dependem da Fase 0.5 (rotulagem manual)
> e NÃO são avaliados aqui.**

| Afirmação do paper | O que A_mais mostra | Veredito |
|---|---|---|
| **H1 — RTMV > 50% em quase toda a semana** | Universo: RTMV **36,1%**; só 1 dia passa de 50%. Amostra: 48,3% — não difere de 50% (p=0,36). | ✘ **não se sustenta** |
| **H2 — MH rivaliza com MV em ≥1 dia** (qui-23, capa da *Veja*) | Em **nenhum dia** a MH chega perto da MV; o 23/out é o **mais vertical**. | ✘ **não reproduz** ⚠ *(a MH é subcontada pelo link morto — §6; veredito é um limite)* |
| **#Eleições2014 representa o "debate eleitoral"** | No escopo amplo a MV cai 43,3% → 24,9% e o NDA sobe a 47,1%. | ↔ **depende do escopo** |
| **A amostra de 100/dia por pico capta o padrão** | O pico **superestima** a MV: 48,3% × 36,1%, ICs disjuntos. Viés sistemático. | ✘ **a amostra não representa seu próprio universo** |
| **(implícito) reproduzir MV é traço do público** | É do **contexto**: o mesmo autor vai de **25,9% → 53,3%** de NDA ao trocar a hashtag (OR intra-autor 2,91). | ⚠ **traço da hashtag, não do ator** |

**Em uma frase:** sobrevive o **qualitativo** — entre conteúdo com link classificável, a
vertical domina a horizontal (~5:1). Não sobrevive o **quantitativo**: o limiar RTMV > 50%
(H1), o pico horizontal de qui-23 (H2), a representatividade da hashtag única e a
suficiência da amostra por pico.

> **Nota de honestidade (dupla).**
> 1. A predição **pré-registrada deste projeto** (`REPLICACAO_CASO_COMPOS2014.md` §5:
>    "*H1 — predomínio agregado de MV… provavelmente robusto; provável NÃO MUDA*") foi
>    **refutada**. Apostamos errado, e registrar isso é o ponto do desenho pré-registrado.
> 2. **Este relatório também errou** na primeira versão: contava link morto como
>    "opinião sem link", inflando o NDA em ~7 p.p. e o efeito intra-autor em ~35%. As
>    conclusões sobreviveram, a magnitude não. Fica o registro.
