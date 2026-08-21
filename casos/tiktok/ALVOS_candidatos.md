# Alvo do caso TikTok — candidatos medidos, e a escolha que sobra

> Levantado em **18/ago/2026**, a pedido da Mariana ("a coleta tem que resolver para
> algum caso que usa o TikTok"). A coleta local já está pronta ([README](README.md));
> o que falta é **o alvo**, e ele decide o que se coleta.
>
> Critérios do projeto (os mesmos que descartaram o #207): **publicado com tração** +
> **coleta reproduzível hoje** + **sub-coleta declarada** + tipo de análise que a
> `tab:casos` pede para a célula TikTok, que é **modelagem de tópicos**.

---

## 1. O achado estrutural: os dois critérios se contradizem no TikTok

Varridos os **55 artigos de TikTok** do `research.db` com tipo de análise codificado, e
buscado fora do corpus (OpenAlex; o Semantic Scholar recusou por limite de taxa):

| faixa | o que existe |
|---|---|
| **muito citados** (300–530 cit., 2020–21) | *Mapping Internet Celebrity on TikTok* (527), *Affective Publics... Climate Activism* (343) — **estudos culturais / análise de discurso multimodal**, feitos à mão sobre amostras pequenas. Não há afirmação computacional mensurável para o par *mudou?/convergiu?* |
| **computacionais com sub-coleta declarada** (2024–25) | **2 a 12 citações**. São os que servem ao protocolo, e não têm tração |

Isso não é acidente de busca: **o corpus da survey é uma varredura DBLP recente** — os 55
artigos de TikTok são todos de **2025–2026**, e o mais citado do conjunto tem **25**
citações. TikTok como objeto de análise computacional é recente demais para ter
acumulado citações.

**Consequência honesta:** para a célula TikTok, "publicado com tração" no padrão do
Buntain (133 cit.) ou do Massachs (29 cit.) **não está disponível**. A escolha real é
entre dois candidatos modestos — e é melhor declarar isso no capítulo do que fingir que
o lineup é homogêneo em tração.

---

## 2. Os dois finalistas, lado a lado

| | **#14 — AI vs. Human Paintings** | **#299 — EDTok** (o previsto na `tab:casos`) |
|---|---|---|
| veículo | **Int. Journal of Human-Computer Interaction** (Taylor & Francis, revisado por pares) | **arXiv** — preprint |
| citações | **7** (OpenAlex) / **12** (Semantic Scholar) | **2** |
| ano | 2025 | 2025 |
| análise | engajamento + sentimento + **modelagem de tópicos** | descritiva + **BERTopic** + sentimento + multimodal |
| afirmação-alvo | *"topic modeling revelou **sete** razões-chave para percepções negativas"* — hiper-realismo, reações ambivalentes, **roubo de arte** | caracterização do conteúdo de transtorno alimentar (56k vídeos) |
| **sub-coleta** | **declarada e brutal**: 4.396 vídeos → filtros (≥10.000 views, ≥5 comentários, ≤5 obras por autor) → 1.713 → **417 vídeos** analisados; 19.071 de 71.962 comentários | hashtags/palavras-chave **curadas à mão**; 56k vídeos |
| instrumento de coleta | **raspagem** com conta criada para o estudo | **TikTok Research API** — a mesma que temos |
| gabarito público | ❌ não | ✅ **sim** — 43.040 IDs (sem texto; hidratar exige a API) |
| carga ética | baixa (arte gerada por IA) | ⚠ **alta** — conteúdo pró-transtorno alimentar; coletar *mais* tem peso próprio |

---

## 3. Recomendação: **#14**, com uma ressalva

**Por que #14.** O critério que a Mariana já aplicou duas vezes — e que matou o #207 — é
*publicado com tração*. O #299 tem **exatamente o perfil do #207**: preprint arXiv, 2
citações. Trocar um por outro do mesmo perfil não resolve o problema que motivou o
descarte. O #14 está num periódico revisado por pares e tem 3–6× mais citações.

**E o alvo-teste é bom.** "Sete razões para percepções negativas, obtidas por modelagem
de tópicos" é uma afirmação **contável**: os sete tópicos sobrevivem quando se coleta o
que os filtros excluíram? Some algum? Aparece um oitavo? É a mesma pergunta que a linha 6
da tabela mestre (ranking de enquadramento do caso vacinas) já responde para outra rede —
o que dá **comparabilidade entre casos**, que é o que a leitura PP3 precisa.

**E o funil é o achado.** O filtro **≥10.000 visualizações** é literalmente o estrato
viral — a mesma sub-coleta que o caso vacinas problematiza (conteúdo só nos virais >500
RTs). Se o resultado convergir com o do vacinas em rede diferente, análise diferente e
plataforma diferente, é **evidência forte** para a tese. Se divergir, é igualmente
interessante.

**A ressalva.** O #14 coletou por **raspagem**, e nós expandiríamos pela **Research
API**. Os corpora não são idênticos por construção, e isso tem de ser declarado — mas
não invalida: a pergunta do caso é sobre o **estrato analisado** (417 de 4.396), não
sobre o instrumento. É o mesmo desenho do caso vacinas, onde a sub-coleta
problematizada também é o estrato, não a coleta.

**O que o #299 tinha de melhor, e se perde:** o gabarito público (43.040 IDs) e o mesmo
instrumento de coleta. Se a Mariana preferir esses dois, o #299 volta — mas então a
fraqueza de tração precisa entrar declarada no capítulo, como limitação do caso.

---

## 4. Se a escolha for #14, o que a coleta tem de buscar

Isto é o que torna a coleta **útil** em vez de exploratória:

| # | o que coletar | por quê |
|---|---|---|
| 1 | os mesmos termos do artigo — `Stable Diffusion`, `Midjourney`, `AI paintings`, `Procreate`, `SAI` — **sem** o corte de 10.000 views | reconstruir o funil 4.396 → 417 e medir cada degrau |
| 2 | comentários dos vídeos (não só metadados) | os tópicos do artigo saem dos **comentários** (19.071 analisados de 71.962) |
| 3 | a janela temporal do artigo, e depois além dela | separar efeito de **estrato** de efeito de **janela** |

⚠ **Falta implementar:** o cliente atual só busca **vídeos**
([core/tiktok_api.py](core/tiktok_api.py)). Os comentários usam outro endpoint
(`/v2/research/video/comment/list/`) e são **insumo obrigatório** para replicar a
modelagem de tópicos. É a próxima peça de código, e só faz sentido escrevê-la depois de
a Mariana fixar o alvo — se for o #299, o que se hidrata são IDs de vídeo, não
comentários.

---

## 5. Decisão pendente

- [ ] **#14** (recomendado) · **#299** (mantém o previsto na `tab:casos`) · **outro**
- [ ] se #14: a `tab:casos` precisa trocar a linha TikTok (hoje diz "#299 · hashtags ED
      curadas; 56k vídeos")
- [ ] em qualquer caso: declarar no capítulo que a célula TikTok tem **tração menor** que
      as demais, e por quê (§1)
