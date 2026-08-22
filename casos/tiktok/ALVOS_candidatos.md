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

## 5. Decisão — **fechada em 21/ago/2026: nenhum dos dois entra**

> Sondagem feita a pedido da Mariana, que perguntou se não haveria um alvo de TikTok
> **reconstruível por um crawler próprio**. A resposta é não, e as razões são
> específicas de cada candidato. Nada foi coletado do TikTok para chegar a isto.

### 5.1 ❌ #14 (AI vs. Human Paintings) — **irreconstruível**

Três obstáculos independentes, e o terceiro basta sozinho:

1. **O `robots.txt` do TikTok proíbe a busca.** Em 21/ago/2026 ele traz, para
   `User-agent: *`, `Disallow: /search?`, `/search/video?` e `/search/user?q=`. A coleta
   do #14 foi *"pesquisar por tags … e raspar a web"* — o endpoint que a reconstrução
   exige é exatamente o bloqueado. (`/tag` segue permitido, mas é feed por recência, não
   a busca que o artigo usou.) O mesmo arquivo põe `ClaudeBot`, `anthropic-ai`,
   `Claude-User` e `Claude-SearchBot` sob `Disallow: /` — o assistente não coleta; a
   ferramenta, se houver, é rodada pela pesquisadora.
2. **O artigo não publica identificadores.** As três extrações do `research.db`
   concordam (`mentions_data_publication = false`). Os vídeos que os filtros excluíram
   — que **são** o objeto da expansão — não são identificáveis.
3. **A janela não é reconstruível.** A coleta é um *snapshot de 15/nov/2023*, um corte
   **sem data de início**; e a busca do TikTok ordena por recência, sem recorte de data
   confiável. Um crawler de 2026 devolve o presente, não o corpus de 2023 — que hoje tem
   quase três anos e sofreu deleção.

### 5.2 ❌ #369 (*Just Another Hour on TikTok*) — reconstruível, mas sem tração

[arXiv 2504.13279](https://doi.org/10.48550/arXiv.2504.13279), Steel, Schirmer, Ruths &
Pfeffer. **É o único alvo de TikTok cuja coleta é reconstruível**, porque não usa busca:
faz engenharia reversa dos IDs de post e **enumera o espaço de identificadores** de uma
fatia de tempo, o que torna o bloqueio de `/search?` irrelevante. Código público em
[`bendavidsteel/tiktok-slice`](https://github.com/bendavidsteel/tiktok-slice) (⚠ **sem
licença declarada** = todos os direitos reservados; dá para ler e reimplementar citando).

**Por que ficou de fora mesmo assim:** **1 citação**, preprint — o perfil exato que a
Mariana recusou duas vezes (#207, #299). E o custo não cabe: os autores levaram **cinco
meses** para uma hora de TikTok (5 M de vídeos), e a dissertação congela o texto em
meados de setembro.

### 5.3 ⭐ O que se aproveita do #369 **sem** abrir caso

Os autores publicaram no Zenodo, **CC-BY**, 27 MB
([15330828](https://zenodo.org/records/15330828)), as **mesmas oito distribuições
calculadas duas vezes**: em `hour/` (censo completo de uma hora, 5.148.076 vídeos,
17–18h UTC de 10/abr/2024) e em `day/` (um minuto de cada hora ao longo de 24 h,
1.876.255 vídeos). É uma **população e uma amostra dela, publicadas lado a lado** —
material raro para o que esta dissertação pergunta.

Comparação rodada em 21/ago/2026 sobre o arquivo baixado:

| quantidade | censo da hora | amostra do dia | razão |
|---|---:|---:|---:|
| média de visualizações | 2.533,1 | 2.243,9 | **0,886** |
| média de curtidas | 177,9 | 145,8 | **0,820** |
| média de comentários | 4,9 | 4,2 | **0,850** |
| média de compartilhamentos | 14,1 | 9,1 | **0,646** |
| p99 de visualizações | 20.100 | 14.800 | **0,736** |

Todas as quantidades de engajamento são **sistematicamente menores** na amostra do dia,
de 11% a 35%, sempre na mesma direção. A leitura que interessa: os autores tinham
**100% da hora** — não é sub-coleta por volume, é sub-coleta por **janela**. Ter o censo
completo de um recorte não compra representatividade do recorte maior que o contém.

⚠ **Ressalva que impede tratar isso como resultado fechado:** as duas fatias não são a
mesma população (17–18h UTC é um horário específico), de modo que a diferença mistura o
esquema de amostragem com efeito de horário — a mesma confusão do H1 do caso Ituassu.
Separar exigiria os dados brutos, que não estão publicados. Serve como **evidência de
apoio** à terceira pergunta do protocolo, não como caso.

⏳ **Pendente de decisão da Mariana:** se este trecho entra na dissertação (meia tarde,
sem coleta) ou fica só aqui.

### 5.4 O que fica registrado para não refazer

- ❌ #14 e ❌ #369 **avaliados e recusados** — não reabrir sem fato novo.
- O alvo vigente da célula segue sendo o **PoliTok-DE**, com o eixo temporal
  ([FASE2_politok.md](FASE2_politok.md)), e a célula segue **parcial por escolha
  declarada**, não por descuido.
- ❗ A §2.4 do `corpo.tex` justifica o TikTok fechado apenas pela **credencial
  revogada**. O `robots.txt` de 21/ago/2026 é um argumento mais forte e verificável, e
  fecha a rota de raspagem por tag independentemente de credencial — vale acrescentar.

