# Pré-registro — expansão do corpus da survey

> **Escrito em 21/ago/2026, ANTES de extrair qualquer artigo novo.** O baseline
> está congelado ao lado, em [`baseline_agg.txt`](baseline_agg.txt) (saída literal
> de `agg_results.py`) e [`baseline_ids.json`](baseline_ids.json) (os 2.298 ids que
> já tinham PDF e os 2.139 que já tinham análise). Qualquer número deste documento
> é conferível contra esses dois arquivos.
>
> Vale para este trabalho a mesma regra dos casos de replicação (`CLAUDE.md` §7):
> **a aposta é registrada antes de medir, e se ela falhar, o que se reporta é a
> falha.**

---

## 1. A pergunta

A survey catalogou **13.395** artigos e extraiu **2.139**, porque **10.075**
estavam marcados como inacessíveis por *paywall*. Essa é a maior limitação
declarada do trabalho, e hoje ela é **admitida, não medida** (decisão em aberto
nº 1 do [STATUS.md](../STATUS.md)).

A dissertação propõe um protocolo — *tratar o trabalho como amostra sub-coletada,
coletar um superconjunto on-theme, e medir se a conclusão mudou e se já havia
convergido*. Este é o protocolo **aplicado à própria survey**.

A pergunta **não** é "a base fica maior?". É: **o viés de acesso alterava os
achados?** Uma base maior com os mesmos achados é o melhor desfecho possível —
converte a limitação declarada em limitação medida e fecha a decisão nº 1.

## 2. O que é a expansão

Em 21/ago/2026 apurou-se que a marcação de inacessibilidade está **desatualizada**:
numa sondagem de 70 DOIs do estrato pago, **18,6%** estavam em acesso aberto
(IC95% Wilson 11,2%–29,2%), em repositório ou na própria editora.

A expansão roda `scripts.retry_pdfs` sobre a **fila inteira** — os **11.093**
artigos com DOI e sem PDF — por Unpaywall, OpenAlex, Semantic Scholar e arXiv.
**Não usa o proxy institucional** (ver §7).

### 2.1 Limitação que já se sabe, e que nenhum resultado apaga

O estrato recuperado **não é uma amostra aleatória do estrato pago**: é o
**subconjunto dele que está em acesso aberto**. Autores que depositam em
repositório não são um sorteio dos que não depositam. Portanto:

- Um resultado "não mudou" **não** prova que o estrato pago inteiro concorda com
  a base extraída; prova que a parte dele **alcançável sem credencial** concorda.
- Um resultado "mudou" é conclusão mais forte, porque um viés medido num
  subconjunto enviesado **na direção da base atual** (ambos favorecem acesso
  aberto) é um piso, não um teto.

Isso vai ao texto como está escrito aqui, nos dois desfechos.

## 3. Semente, tamanho e regra de sorteio

| Item | Valor |
|---|---|
| Semente da **recuperação** (ordem da fila) | `20260821` — `retry_pdfs --shuffle 20260821` |
| Semente do **sorteio da amostra** | `20260929` (a data da defesa; número fixo, verificável e sem relação com os dados) |
| Tamanho da amostra | **n = 800** |
| Modelo de extração | **Gemini 2.5 Flash apenas** (`--models gemini`) |
| Teto de gasto | **~R$45** (800 × R$0,054/chamada, tarifa calibrada em [ORCAMENTO.md §1](../../../../redes-sociais-digitais-survey/documentacao/ORCAMENTO.md)) |

**Por que `--shuffle` na recuperação.** A ordem padrão da fila é por `id`, que
**não** é neutra: os ids baixos concentram artigos recentes (2025–26), justamente
os menos propensos a estar em repositório aberto. Com a semente, **qualquer
prefixo** da fila é uma amostra não enviesada dela — o que protege a medida caso a
recuperação precise ser interrompida.

**Por que só Gemini.** Os achados reportados no artigo têm base Gemini (cobre os
2.139; o Claude Haiku cobre 887, dos quais 732 sobrevivem ao filtro de descarte).
Gemini-novo contra Gemini-velho é a comparação limpa; misturar modelos
introduziria a diferença inter-modelo (≈85% de concordância) dentro do efeito que
se quer medir.

**Regra de sorteio** (determinística, em `sorteia_amostra.py`):

1. **População:** artigos cujo `pdf_path` era nulo no baseline congelado **e** que
   ganharam PDF nesta expansão **e** que não têm `analyses`.
2. Ordenar por `id` (ordem canônica, independente de sistema de arquivos).
3. `random.Random(20260929).sample(populacao, 800)`.
4. **Se a população tiver ≤ 800**, extrai-se **toda ela** — vira censo do estrato,
   e o documento de resultados diz isso em vez de falar em amostra.
5. O mesmo **filtro de descarte** da base atual se aplica aos novos: artigos que o
   Gemini marca `suggested_discard` saem da base de análise (foi o que levou 2.139
   a 1.718).

## 4. Os achados testados

Valores de hoje, todos de [`baseline_agg.txt`](baseline_agg.txt), base **N=1.718**
(2.139 extraídos − 421 descartados).

### 4.1 Primários — os quatro que o artigo defende

| # | Achado | Hoje | Base |
|---|---|---:|---|
| **A1** | Mediana de itens coletados | **273.290** | 1.518 com quantidade legível |
| **A2** | Fração que **não** chega a 1 milhão | **60,5%** | 1.518 |
| **A3a** | Taxa de **amostragem** | **18,7%** (321) | 1.718, Gemini |
| **A3b** | Taxa de **filtragem** | **80,3%** (1.379) | 1.718, Gemini |
| **A4** | Fatia de **Twitter** | **63,7%** (1.095) | 1.718 |

> ⚠ **Sobre os "54,5% de Twitter".** Os 54,5% que aparecem no `CLAUDE.md` da raiz
> são do **catálogo DBLP** (13.395, por título/veículo) — outra base e outro
> instrumento. Esse número **não é movido por extração nenhuma** e por isso **não
> entra neste teste**. O que se testa é a fatia na base extraída, **63,7%**. A
> distinção vai ao texto: eram dois números diferentes tratados como um.

### 4.2 Secundários — registrados, reportados, mas não são a manchete

| # | Achado | Hoje |
|---|---|---:|
| B1 | Coleta via **API** | 69,7% |
| B2 | **Grandes coletores** (≥10 mi) | 22,3% dos 1.518 |
| B3 | **DOI persistente** (Zenodo/Figshare/OSF) | 8,3% |
| B4 | Análise mais frequente | Estatística descritiva, 46,9% |
| B5 | **Modelagem de tópico** | 22,9% (4ª mais frequente) |

### 4.3 O que explicitamente **não** se testa

O **funil** (13.395 → 2.139 → 1.718) muda por construção, já que o denominador do
meio cresce. Isso é aritmética da expansão, não achado. Os números novos do funil
serão reportados, sem serem submetidos a teste.

## 5. O que conta como "mudou"

Reporta-se **movido / não movido por achado**, nunca um veredito único.

**Critério 1 — deslocamento (a pergunta do leitor do artigo).** Recomputa-se cada
achado sobre a **base combinada** (1.718 antigos + os novos que sobrevivem ao
descarte). *Moveu* se o valor combinado cai **fora** do IC95% de bootstrap do valor
de hoje: 2.000 reamostragens com reposição da base de 1.718 (1.518 para A1/A2),
intervalo percentil.

**Critério 2 — viés de acesso (a pergunta desta expansão).** Compara-se o valor
medido **só no estrato novo** contra o valor de hoje. Proporções: teste de duas
proporções, α = 0,05. Mediana (A1): bootstrap da diferença de medianas, 2.000
reamostragens, IC95% percentil; *moveu* se o IC não contém zero.

Os dois critérios são reportados lado a lado. Eles respondem a coisas diferentes e
**podem discordar** — um efeito real no estrato novo pode não deslocar o combinado
se o estrato novo for pequeno em relação aos 1.718. Essa discordância, se
acontecer, é resultado e vai reportada como tal, com o tamanho relativo dos
estratos ao lado.

**Sem correção para múltiplos testes.** São 5 achados primários pré-registrados,
não uma varredura; os *p* saem crus e o leitor aplica o desconto que quiser. O que
não se fará é caçar significância em achado não registrado aqui.

## 6. A aposta

Registrada antes de medir. **A aposta global:**

> **Os dois achados centrais não se movem; a descrição do corpus se move.**

Ou seja: a survey acerta que *amostragem é rara e filtragem é a norma* — isso é
prática metodológica, não propriedade de veículo, e não tem por que mudar com o
acesso. Mas *quem* está no corpus e *quanto* ele coleta muda, porque o acesso
aberto seleciona veículo, e veículo seleciona plataforma e escala.

Isso é a **mesma forma de desfecho do caso vacinas** (`CLAUDE.md` §3): conclusão
comparativa robusta ao instrumento, descrição do corpus não. Se ela se repetir
aqui, num objeto completamente diferente, é achado transversal da dissertação — e
é por isso que a aposta está escrita antes.

Achado a achado:

| # | Achado | Aposta | Direção | Por quê |
|---|---|---|---|---|
| **A3a** | Amostragem 18,7% | **não move** | — | Prática metodológica; não se vê por que dependeria de o PDF ser gratuito. Faixa apostada: 16–22% |
| **A3b** | Filtragem 80,3% | **não move** | — | Idem. Faixa apostada: 77–84% |
| **A4** | Twitter 63,7% | **move** | ⬇ **cai** 2–6 p.p. | A base extraída foi montada com o que era grátis na hora do download, e isso é dominado por arXiv — a fatia mais concentrada em Twitter que existe. O estrato pago tem mais periódico de comunicação e ciências sociais, onde Facebook e YouTube pesam mais |
| **A1** | Mediana 273.290 | **move** | ⬇ **cai**, possivelmente abaixo de 200 mil | Mesmo mecanismo: o arXiv/CS é onde moram as coletas de escala (decahose, dumps). O trabalho de periódico tende a corpus menor e curado à mão |
| **A2** | 60,5% abaixo de 1 mi | **move** | ⬆ **sobe** 2–5 p.p. | É o espelho aritmético de A1 |

**Se A3a ou A3b se moverem**, a aposta falhou no ponto que mais importa, e o
resultado é maior do que se ela acertasse: significaria que o achado central da
survey era artefato de acesso. Esse desfecho seria reportado como tal, na primeira
linha do documento de resultados, sem atenuação.

## 7. Travas — nenhuma se contorna sem falar com a Mariana

- ⛔ **Proxy institucional (`PUCRIO_PROXY*`) não se usa para volume.** Ele
  autentica e funciona, mas as editoras bloqueiam automação: ACM 403, IEEE 202 com
  corpo vazio, Elsevier 403 na ScienceDirect, SAGE 403, T&F 403 — só a Springer
  devolveu 200. O risco de rodar volume por ali **não é da Mariana, é do acesso da
  PUC-Rio inteira**. A expansão usa exclusivamente as rotas abertas
  (Unpaywall/OpenAlex/Semantic Scholar/arXiv).
- 💰 **O teto de US$ 25 do `ANTHROPIC_VACINAS_API_KEY` é do rotulador do stance e
  está em US$ 9,58 — não se toca nele.** A extração usa a `GEMINI_API_KEY` do
  `.env` do repositório da survey, que é outra chave e outro orçamento.
- 📏 **A amostra é dimensionada pelo orçamento, não o contrário.** n = 800 dá
  IC95% de ±2,7 p.p. numa proporção de 20% — folga suficiente para os
  deslocamentos apostados em §6, e o ponto a partir do qual precisão para de
  comprar informação.

## 8. Condições de parada

Registradas antes, para que parar não seja decisão tomada no calor do resultado.

| Condição | Ação |
|---|---|
| Taxa de recuperação final **< 11%** (o piso do IC da sondagem) | **Parar.** A sondagem de 70 era otimista e a extrapolação de 1.127–2.944 artigos não vale. Reporta-se a taxa real e o trabalho vira uma nota de método |
| Qualquer sinal de **bloqueio ou captcha** | **Parar**, não contornar, reportar qual fonte bloqueou |
| Custo por artigo **> 2× o calibrado** (R$0,108) | **Parar** e reportar o custo por artigo antes de continuar |
| População recuperada **< 100** artigos | Não há amostra a sortear; reporta-se só a taxa de recuperação |

## 9. Encadeamento com a dissertação

Se algum número **se mover**, ele se move também no resumo, no Cap. 1 e na
conclusão da dissertação. A propagação é **verificada, não manual**: roda-se
`escrita/dissertacao/audita_numeros.py` e `audita_contas.py` **antes e depois**, e
a diferença entre as duas saídas é o que se edita.

⛔ **O `corpo.tex` não se toca enquanto a Mariana não tiver lido o
`revisao-3.pdf`** — o PDF que ela comenta tem de bater com a fonte. Se houver
número a propagar antes disso, ele fica registrado no documento de resultados e
espera.
