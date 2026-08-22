# CLAUDE.md — Dissertação da Mariana (mestrado PUC-Rio, Informática)

> **Pasta-mãe** que reúne, num só lugar navegável, a **escrita** da dissertação e os
> **casos de replicação** que a alimentam. Orientador: Prof. Sérgio Lifschitz
> (grupo eTC/TriTech/TreeTech).

> ⚠ **ONDE TRABALHAR — leia antes de editar qualquer coisa.** Existem **duas** cópias
> desta pasta, e elas **não** são intercambiáveis:
>
> | Cópia | O que tem | O que fazer nela |
> |---|---|---|
> | `Documents/GitHub/dissertacao-mestrado/` | repositório **git**; os `.md`, `.tex` e scripts. **Não** tem os dados (`*.sqlite`, gabaritos — ver `.gitignore`) | **é a cópia canônica.** Toda edição de texto e documentação acontece aqui |
> | `Documents/dissertacao/` | mesma árvore **mais os ~105 arquivos de dado** (snapshots, gabaritos, CSVs) | rodar scripts que precisam dos dados. Depois, copiar **de volta só os arquivos que você mudou**, nunca a árvore inteira |
>
> **Nunca sincronize uma pasta inteira por cima da outra.** Em 21/ago/2026 uma cópia
> de `escrita/` destruiu as **29 edições** que uma sessão paralela havia aplicado no
> `corpo.tex` (registro no [`ESTADO.md`](ESTADO.md) §4.17). Antes de copiar, rode `git status` e confira se
> outra sessão está escrevendo. **`escrita/dissertacao/revisoes/` não se sincroniza em
> direção nenhuma** — o ciclo de revisão da Mariana (comentar o PDF, aplicar no fonte)
> só existe no repositório, e um PDF duplicado gera comentário órfão.
>
> Os originais anteriores à consolidação seguem em `Downloads/`
> (`dissertacao-escrita`, `pesquisa-twitter-refeita`, `replicacao-caso-xande`) e estão
> **desatualizados** — não são fonte para nada.

---

## 1. A tese em uma frase

Análises computacionais sobre Redes Sociais Digitais (SNA, modelagem de tópicos,
sentimento, estatística) dependem de uma etapa de **coleta** raramente problematizada.
A survey (companion) mostra que **amostragem estatística é rara** e **filtragem por
critério é a norma**. A dissertação propõe um **desenho experimental "coletar mais"**:
tratar cada trabalho como uma amostra sub-coletada do seu tema, coletar um
**superconjunto _on-theme_** e medir, por tipo de análise, se a conclusão **mudou** e
se já havia **convergido** no volume original.

## 2. Mapa da pasta

> ⚡ **Antes de qualquer coisa, leia o [`ESTADO.md`](ESTADO.md)** — ele responde
> "o que dá para avançar agora" (desbloqueado / travado / decisões / divergências).
> Este `CLAUDE.md` é o mapa **estável**; o `ESTADO.md` é o **agora**, e toda sessão
> que muda o estado do projeto termina atualizando-o.

```
dissertacao/
├── CLAUDE.md            <- este arquivo (o mapa)
├── ESTADO.md            <- O AGORA: o que dá para avançar, o que trava, o que espera decisão
├── escrita/             A REDAÇÃO (dissertação + survey + referências). Ver escrita/CLAUDE.md
│   ├── dissertacao/       fonte LaTeX (classe oficial PUC-Rio thesispuc/ABNT)
│   ├── survey/            artigo companion + scripts reprodutíveis (research.db)
│   ├── referencias/       propostas, artigos de referência, trabalho do Salgueiro
│   └── INVENTARIO.md      índice do material de escrita
└── casos/               OS CASOS DE REPLICAÇÃO (geram evidência p/ a escrita)
    ├── RESULTADOS_tabela_mestre.md   FASE 4: o entregável central — "mudou? / convergiu?"
    │                      por análise e rede. PARCIAL (10 linhas fechadas, 7 em ⏳).
    ├── twitter-ituassu/   caso #Eleições2014 (Ituassu 2015/2018). Ver REPLICACAO_CASO_COMPOS2014.md
    │                      Análises: mídia (MV/MH→MP/MC) + stance. Snapshots em data/repl/compos2014/.
    ├── heine-xande/       caso Heine 2025 (amostragem 2022). Ver REPLICACAO_CASO_HEINE.md
    │                      Análises: tópicos (BERTopic) + quantitativa. Espelha o fluxo do twitter-ituassu.
    ├── vacinas/           caso Verjovsky et al. 2023 (debate vacinal 2021-22). Ver REPLICACAO_CASO_VACINAS.md
    │                      Análises: rede (modularidade) + conteúdo/framing. A Mariana é coautora do alvo.
    ├── reddit-buntain/    caso Buntain & Golbeck 2014 (WWW, 133 cit.). Ver REPLICACAO_CASO_BUNTAIN.md
    │                      Análise: SNA / papéis sociais (answer-person). 1º caso fora do Twitter. Fase 0 feita (paper lido).
    ├── reddit-massachs/   caso Massachs et al. 2020 (WebSci, 29 cit.). Ver REPLICACAO_CASO_MASSACHS.md
    │                      Análise: homofilia/polarização (apoio a Trump). Fase 0 completa (full text lido).
    ├── youtube-agecovp/   caso Ghenai et al. 2025 (AGECovP, EPJ Data Science). Ver README.md
    │                      Análise: composição do corpus / filtro de forma. 4ª rede. FECHADO 21/ago/2026.
    ├── reddit-topicos/    ⏳ caso Melton et al. 2021 (J. Infection and Public Health, 178 cit.).
    │                      Ver README.md e ARTIGO_MELTON_alvo.md. Analise: MODELAGEM DE TOPICO
    │                      (LDA) + sentimento. Aberto 22/ago/2026; PARADO no Portao 1.
    ├── tiktok/            caso Ruiz et al. 2025 (PoliTok-DE). Ver README.md e FASE2_politok.md
    │                      Análise: deleção de conteúdo — eixo TEMPORAL, sem coleta. Parcial.
    ├── meta-ads-imigracao/ ⛔ FORA DO ESCOPO DA DISSERTAÇÃO desde 21/ago/2026 (mas preservado).
    │                      Capozzi et al. 2021/2020 (CHI, 29 cit.). Ver REPLICACAO_CASO_META_ADS.md
    │                      Análise: classificação pró/anti em anúncios de imigração (Meta Ad Library, Itália).
    │                      Gabarito dos autores em data/repl/metaads2019/. Volta se a rota Meta reabrir.
    └── reddit-companhia-ia/  ❌ DESCARTADO (#207 "My Boyfriend is AI", preprint sem tração). Tombstone no README.
```

## 3. Os casos de replicação (lineup)

Cada caso = um trabalho publicado tratado como amostra sub-coletada + a expansão
_on-theme_ + a medição "mudou? / convergiu?".

| Caso | Alvo | Rede / ano | Análises | Estado |
|---|---|---|---|---|
| **twitter-ituassu** | Ituassu & Lifschitz 2015; Ituassu et al. 2018 | Twitter / 2014 | mídia (determinística, **feita**) + stance (kit de rotulagem pronto) | **Eixo mídia fechado** (07/ago/2026): curvas `A(volume)` de H1, dominância MV e H2 por dia — H1 convergiu em n≈200 e a falha do alvo é **de esquema de amostragem, não de volume**; H2 não reproduz em recorte nenhum. **MP/MC fechado**: resíduo curado e as 4 explicações do nosso lado descartadas — a divergência 72,2% × 59% é do lado do artigo e irresolúvel com o publicado. **Stance ◐ kit de rotulagem pronto em 18/ago/2026** (codebook + 320 tweets sorteados e congelados + pré-registro); falta **só a rotulagem humana** |
| **heine-xande** | Heine & Lifschitz 2025 (dissertação) | Twitter / 2022 | tópicos (BERTopic) + quantitativa (SGBD) | **docs + pipeline prontos**; execução **aguarda os dados** (ver §5) |
| **vacinas** | Verjovsky et al. 2023 (_Vaccine_/Elsevier, revisado; preprint SSRN 4370287) | Twitter / 2021–22 | rede (modularidade) + conteúdo/framing (Bardin) | **Fases 0–3 concluídas.** Eixo A: AV4 exato; AV1 medido com atribuição formal de lado às 11.664 comunidades — **cobertura inconclusiva** (76,7–90,6% conforme a base), **equilíbrio entre polos não replica** (razão pró/anti 1,50–1,56 × 1,02). AV3 replica a 0,3 p.p. no ponto original (validando a atribuição de lado) e **muda na expansão** (razão 1,43→2,34). AV2 não muda (topo-1 = 2,33×), mas por construção. Curvas de volume feitas: **AV1 estabiliza só em f≈0,75**. **E3**: o balanço pró/anti não inverte em nenhum dos 6 termos, mas o enquadramento muda muito — volume e largura de filtro respondem ao contrário. Eixo B: rotulador LLM validado (κ 0,759 no esquema do artigo; 0,697 num esquema de 3 classes, com teto da tarefa em 0,746) e 29.978 tweets rotulados nos dois esquemas. Fase 3: conclusão **comparativa robusta** ao esquema de anotação, **descrição do corpus não** (~18 pontos de diferença); categorias convergem. Linhas 4–7 da tabela mestre fechadas |
| **reddit-buntain** | Buntain & Golbeck 2014 (WWW, **133 cit.**) | Reddit / 2013 | **SNA / papéis sociais** (answer-person por estrutura de rede) | ★ **FECHADO em 19/ago/2026 — o maior efeito de sub-coleta da dissertação.** Coleta completa (**43.479 submissões + 1.015.247 comentários**, 13 subreddits, sem corte) contra os **279 usuários** do artigo (top-100 subs × ~200 coment. × 1 mês × corte ≥20 arestas). **RB3 inverte**: o artigo diz ~3% em >1 comunidade (7/279); no universo, **sob o mesmo limiar de atividade**, são **57,6%** (3.450/5.991) — **19×**. A localidade dos papéis sociais é artefato do recorte top-100 × top-200, não propriedade do Reddit. Curva por limiar assenta em k≈10–20. **Capítulo escrito** em 21/ago. 1º caso fora do Twitter |
| **reddit-massachs** | Massachs et al. 2020 (WebSci, 29 cit.) | Reddit / 2012–16 | **homofilia** (apoio a Trump, r/The_Donald) | **Fases 0–2 feitas; Fase 3 declarada FORA DE ESCOPO.** **MH1 REPRODUZ** (18/ago/2026): F1 34,6% × 34,8% na homofilia e 26,8% × 26,7% na influência — as duas pontas a <0,25 p.p. Traz homofilia (tipo novo). Estrato sub-coletado = focus group de 44.924 usuários (≥10 comentários em 2012 **e** 2016); **gabarito publicado** (`github.com/JoanMassachs/reddit-data`). ⚠ **Achado lateral:** sem reponderação de classes o mesmo modelo cai de F1 34,6% para **8,2%** — decisão que o artigo não declara e que domina o resultado. ⛔ A expansão não é dimensionável pela API do Arctic Shift (34/34 incompletos); caminho real = dumps no Academic Torrents, depois da defesa. **Capítulo escrito** em 21/ago |
| ~~**meta-ads-imigracao**~~ ⛔ | Capozzi et al. 2021 (**CHI**, 29 cit.) + 2020 (SocInfo, 16 cit.) | **Instagram/Facebook** (Meta Ad Library) / 2019–20 | **classificação** (pró/anti-imigração, F1 = 0,85) + caracterização | ⛔ **FORA DO ESCOPO DA DISSERTAÇÃO desde 21/ago/2026** — decisão da Mariana na 2ª rodada de revisão; a §2.4 do `corpo.tex` trata a Meta como rota fechada, não como caso pendente. **Nada foi apagado**, e o caso volta se a rota reabrir. O que estava feito: **Fase 0 ◐ parcial** (7/ago/2026). Fecha a **última rede vaga** do lineup. A sub-coleta é **declarada pelos autores**: *"we search for ads appearing only on Facebook (not Instagram)"* — a expansão **é** a plataforma que nomeia a célula. **Dois gabaritos publicados, baixados e conferidos**: metadados dos 2.312 anúncios (bate com o paper; 731 × 733 páginas) e as **anotações do CHI 2021** (200 anúncios × 3 anotadores, **com o texto**). **α de Krippendorff reproduzido** (0,763 × 0,76 nos 5 rótulos, n=174 exato; 0,924 × 0,92 nas 2 polaridades, ⚠ n 141 × 150). ⚠ **o alvo-teste CB2 é ambíguo no próprio artigo** (o resumo contrasta proporções de populações diferentes) — **desambiguado em 7/ago/2026**: mede-se a **razão de desproporção** R = fatia de impressões ÷ fatia de anúncios na base dos anúncios **com posição** (R = 1,72), com a base de todos ao lado (R = 1,46). ⚠ **as impressões do alvo não reproduzem**: 35 M reportados × **49,8 M** pela regra que ele declara usar. ⏳ só falta a **conta Meta verificada**. Braço **Brasil** sem alvo próprio, como mitigação de risco |
| **reddit-topicos** ⏳ | Melton et al. 2021 (*J. Infection and Public Health* 14(10), **178 cit.**) | Reddit / 2020–21 | **modelagem de tópico (LDA)** + sentimento | ⏳ **Aberto em 22/ago/2026, PARADO no Portão 1 esperando decisão da Mariana.** Existe para fechar a única lacuna de **tipo de análise** da dissertação. Fase 0 **feita**: full text lido e afirmações numeradas. ⭐ O corpus analisado é **11.641** itens (1.401 submissões + 10.240 comentários), **não os ~18.000** do resumo — há **dois** filtros empilhados (topo da listagem + 22 termos). ⭐ Os autores **publicaram o modelo LDA ajustado** (7 saídas de pyLDAvis), congelado como gabarito. ★ **T1 não é ranking, é ausência** ("conspiracy theories were *not detectable*") — e já está sob tensão no gabarito deles: no modelo de janeiro (k=15) há tópicos com `autism` e `microchip`, ou seja a ausência depende da **resolução**, não só da coleta. ◐ Dimensionamento **6/13**: só os menores já dão **215.394 itens × 11.641** (18,5×); os 7 restantes travaram no **rate limit** do Arctic Shift, e o prompt manda parar, não contornar. ⭐ `NoNewNormal` **banido em 1º/set/2021** — a rota oficial de hoje não alcança parte do corpus do artigo |
| **youtube-agecovp** | Ghenai et al. 2025 (AGECovP, *EPJ Data Science* 14:65) | **YouTube** / 2020–22 | **composição do corpus** (filtro de *forma*) + sentimento/tópicos | **FECHADO em 21/ago/2026** no eixo do filtro. 4ª rede do lineup. Fase 1 completa (**85/85 buscas, 3.446 vídeos + 2.165 canais** pela API). Fase 2: o ponto original reproduz, mas **só sob convenções não declaradas** (contar a 1ª categoria do canal; limiar de neutralidade do TextBlob). Fase 3: ❌ **a predição P1 falhou** — o filtro remove **6,4 p.p. menos** UGC do que preserva (IC95% [−11,4; −1,4]). ★ Mas o funil inteiro seleciona **muito**: canais no corpus 23,5% UGC × **61,7%** fora, Δ **+38,3 p.p.**, mediana de inscritos 199 mil × 1.070. Circularidade confirmada, **mecanismo não isolado** (o ramo dos sugeridos saiu da API em ago/2023). ⏳ resta só AG1/AG2 nos comentários |
| **tiktok** (PoliTok) | Ruiz et al. 2025 (PoliTok-DE) | **TikTok** / 2024–26 | análise de conteúdo / **persistência** | **Parcial, fechado em 19/ago/2026 pelo eixo TEMPORAL.** A credencial de Research API do eTC está morta (`invalid_client`), então **não há expansão por volume**; no lugar, o caso mede a **rechecagem em datas sucessivas** sobre o dataset publicado: o *mesmo* painel de 100.926 posts vai de 6,3% → 17,4% → **20,9%** de deleção em 4,5 meses, sem que um post seja acrescentado. Acrescenta o **quarto eixo** (momento) ao protocolo. ⚠ **corrigido em 22/ago/2026:** a série antiga (6,3/17,3/18,7) misturava bases, e o eixo temporal **já está no artigo-alvo** (Apêndice C) — o que é nosso é a verificação e a incorporação ao protocolo. ⚠ o alvo tem 2 citações — ver [ALVOS_candidatos.md](casos/tiktok/ALVOS_candidatos.md) |
| ~~reddit-companhia-ia~~ | ❌ **DESCARTADO** (#207 "My Boyfriend is AI", preprint sem tração) | — | — | Substituído por reddit-buntain + reddit-massachs em 07/ago/2026. Tombstone no README; método de coleta Reddit (Arctic Shift) reaproveitado |

**Fase 4 (o entregável central):** a tabela mestre existe em **parcial** desde
07/ago/2026 — [`casos/RESULTADOS_tabela_mestre.md`](casos/RESULTADOS_tabela_mestre.md).
Em **21/ago/2026** são **13 linhas fechadas** (ituassu eixo mídia + vacinas eixos A e B
+ Buntain + Massachs + YouTube + TikTok), **3 em ⏳** (Heine ×2 e stance do Ituassu) e
**2 fora do escopo da dissertação** (Meta Ads ×2 — ver abaixo). A *fração mínima que estabiliza a conclusão* está anotada em **4** células
(AV1 em f≈0,75; linha 1 em n=100; linha 2 em n≈200; linha 11 em k≈10–20).

⚠ A linha 15 (YouTube) inaugurou uma **categoria de desfecho não prevista** no
protocolo: o efeito de seleção é grande e medido, mas a pergunta "convergiu?" não é
respondível porque o **passo do funil que o produz não pôde ser isolado** — o maior
suspeito saiu da API em ago/2023. Não é ⏳ nem um número: é *indeterminação de causa*.

**Por que os três primeiros são Twitter, e por que o lineup deixou de ser só Twitter.**
O Twitter é 54,5% do levantamento DBLP da survey, e é onde há acervo preservado (eTC) —
por isso os casos executados primeiro são todos dele, e complementares entre si: o
Ituassu ataca **mídia + sentimento**; o Heine, **tópicos + estatística quantitativa**,
fechando a linhagem por dentro (mesmo orientador; ele **já mediu** amostra × completo);
o vacinas acrescenta **rede + análise de conteúdo** e leva a linhagem ao grau máximo (a
**própria Mariana é coautora** e extraiu os dados — a lente "coletar mais" vira
autocrítica). Juntos, 6 tipos de análise sobre a mesma rede. No vacinas, a sub-coleta
problematizada não é a coleta (larga, 1 M tweets) e sim o **estrato analisado**
(conteúdo só nos virais >500 RTs).

A partir de 07/ago/2026 o lineup cobre **outras redes**, como o `corpo.tex` sempre
previu: **Reddit** (`reddit-buntain`, SNA; `reddit-massachs`, homofilia), **YouTube**
(`youtube-agecovp`) e **TikTok** (`tiktok`). O critério de escolha endureceu no caminho
— alvo tem de ser **publicado e com tração** (foi o que descartou o #207) e a **coleta
tem de ser reproduzível hoje**.

⛔ **Instagram/Facebook saiu do conjunto de casos da dissertação em 21/ago/2026**, por
decisão da Mariana na 2ª rodada de revisão. O `corpo.tex` passou a tratar as
plataformas da Meta na §2.4 como **rota fechada**, e não como caso pendente: o
CrowdTangle foi desligado, a Content Library é paga e não deixa os dados saírem, e a
Ad Library alcança apenas conteúdo publicitário, que não é comparável ao conteúdo
orgânico dos demais casos. O conjunto ficou em **6 casos / 4 redes**. O caso
`meta-ads-imigracao` **não foi descartado** — a Fase 0 e os gabaritos conferidos
seguem em [casos/meta-ads-imigracao/](casos/meta-ads-imigracao/README.md), e os
“próximos passos” da dissertação preveem reabrir a célula se uma rota compatível
voltar a existir.

⚠ **Modelagem de tópico ficou sem caso executado, e desde 22/ago/2026 tem um caso
aberto para fechá-la.** A rodada de revisão apurou que o caso do YouTube entrega
**sentimento + composição do corpus**, e não modelagem de tópico como a `tab:casos`
afirmava. É o quarto tipo mais frequente do levantamento, e a lacuna segue declarada
no `corpo.tex` como limitação de cobertura (§9.3) e como próximo passo (§9.4).

O **sétimo caso**, [`reddit-topicos`](casos/reddit-topicos/README.md) (Melton et al.
2021), nasceu para converter essa limitação em duas linhas da tabela mestre. Ele está
⏳ **parado no Portão 1**, que é o portão que decide se o caso entra na dissertação ou
fica como *próximo passo bem instruído*: a defesa é em 29/set/2026 e o dimensionamento
da população não pôde ser concluído (rate limit do Arctic Shift). **Nada dele foi ao
`corpo.tex`**, e nada vai antes de a Mariana decidir — ver
[PORTAO1_relatorio.md](casos/reddit-topicos/data/repl/melton2021/PORTAO1_relatorio.md).

## 4. Infra compartilhada dos casos

- **Dados:** PostgreSQL + MongoDB nas VMs da Cloud-DI PUC-Rio, via **túnel SSH sobre a
  VPN Cloud-DI** (usuário `cloud-di`). VMs: **vm031** (10.50.0.32), **vm037** (10.50.0.38,
  servidor de disciplinas), **vm067** (10.50.0.68).
  - Postgres `eTC_Producao`: `ituassu_2014` (caso 2014, vm067) e coleta contínua eTC.
  - Mongo (só na **vm031**): `xande_search_2022-10-*` (Instagram do Heine, 628k) + `reddit`.
- **Conexão:** `core/db.py` (em cada caso) lê credenciais do `.env` local (nunca
  versionado). Requer a **VPN conectada** — adicionar rotas exige **elevação/admin**:
  subir o OpenVPN como administrador (`Start-Process ... openvpn.exe -Verb RunAs` +
  `vpn-fixed.ovpn`). Teste: `ping 10.50.0.68` ou porta 22 das VMs.
- **API de LLM (rotuladores):** chave `ANTHROPIC_VACINAS_API_KEY` no `.env` da raiz
  desta pasta (nunca versionado). Nome dedicado de propósito: uma `ANTHROPIC_API_KEY`
  solta seria capturada por outras ferramentas. **Todo gasto passa por um teto rígido**
  (`casos/vacinas/core/orcamento.py`: US$ 25, reserva-antes-de-enviar pelo pior caso,
  livro-caixa persistente). Nenhum script gasta sem `--dry-run` disponível.
- **Coleta pública (casos fora do acervo eTC):** **Reddit** via *Arctic Shift* / dumps
  históricos (sem VPN). **Instagram/Facebook** via **Meta Ad Library API** — grátis e
  exportável, exige só conta Meta pessoal com documento verificado (1-3 dias úteis), e é a
  **única** rota Meta viva em ago/2026. Descartadas, com motivo: API pública do Instagram
  (morta desde 2018-20), CrowdTangle (desligado em ago/2024) e **Meta Content Library**
  (paga desde jan/2026 — US$ 371/mês + US$ 1.000 — e os dados **não saem do ambiente
  seguro**, o que quebra a Fase 1). Ver
  [FASE0 do caso](casos/meta-ads-imigracao/data/repl/metaads2019/FASE0_descoberta.md) §3.
- **Padrão de trabalho:** Fase 0 (diagnóstico do banco) → Fase 1 (snapshot congelado em
  SQLite/CSV local) → Fases 2-3 (análises reprodutíveis **sobre o snapshot**, sem rede) →
  Fase 4 (tabela mestre "mudou?/convergiu?").

## 5. Estado do caso Heine (importante)

A Fase 0 (ver `casos/heine-xande/data/repl/heine2022/FASE0_descoberta.md`) mostrou que o
**Twitter 57,9 M / 1,29 M-do-dia-2 do Heine NÃO está nos bancos acessíveis** (varridos 3
VMs, 29 Postgres, 3 Mongo, filesystem, repo GitHub). O que existe acessível é a coleta
**Instagram** dele (`xande_search`, 628 k) + **Reddit**. O dado de Twitter que a
dissertação usa está no **SharePoint do BioBD PUC-Rio** (acesso pela conta institucional
`mbarreto@inf.puc-rio.br`) — a Mariana vai baixar os **CSVs** (`1st_turn_day.csv`,
`1st_turn_day_random_sample.csv`) ou o **dump do Mongo Twitter**. O pipeline já aceita os
dois formatos; assim que o arquivo estiver local, roda-se Fase 1–4.

## 6. Relação escrita × casos

- A **escrita** (`escrita/`) só **redige**; não modifica o desenvolvimento.
- Os **casos** (`casos/`) geram **evidência reprodutível**; todo número no texto deve ter
  origem num script/query de um caso ou no `research.db` da survey. **Se um número no
  texto divergir dos dados, os dados vencem** — sinalizar à Mariana.
- O **sistema da survey** (FastAPI+SQLite que cataloga a literatura) mora em
  `Documents/GitHub/redes-sociais-digitais-survey` (fora daqui) — fonte do `research.db`.

## 7. Princípios (valem para tudo aqui)

- **Rastreabilidade total.** Nada de número solto; toda estatística reproduzível por
  script/query. Marcar origem em rascunho.
- **Não inventar referências.** Toda citação existe no `.bib`/corpus ou é confirmada.
- **Predições pré-registradas.** Antes de rodar um caso no universo, registrar a aposta
  (mudou/não mudou); reportar honestamente quando a aposta falha.
- **Tom acadêmico, não de manifesto.** A lacuna emerge dos dados.
- **Não sobrescrever rascunhos** sem confirmar; commits pequenos.
- **Nomenclatura (regra global da Mariana):** nunca usar a palavra "claude" em nomes de
  branches/arquivos/projetos/commits. Branches descritivas (`feature/...`, `fix/...`).

## 8. Ponteiros rápidos

- **O que fazer agora** → [`ESTADO.md`](ESTADO.md) (desbloqueado / travado / decisões /
  divergências). Atualizado a cada sessão; é a primeira e a última leitura.
- **O resultado consolidado** → [`casos/RESULTADOS_tabela_mestre.md`](casos/RESULTADOS_tabela_mestre.md)
  (Fase 4, parcial): a tabela "mudou? / convergiu?" por tipo de análise, com a leitura
  provisória de PP3 e o registro das predições pré-registradas que falharam.
- Regras da redação → `escrita/CLAUDE.md`. Regras da survey → `escrita/survey/CLAUDE.md`.
- Plano do caso Twitter → `casos/twitter-ituassu/REPLICACAO_CASO_COMPOS2014.md`.
- Plano do caso Heine → `casos/heine-xande/REPLICACAO_CASO_HEINE.md`; descoberta de dados
  → `casos/heine-xande/data/repl/heine2022/FASE0_descoberta.md`.
- Plano do caso vacinas → `casos/vacinas/REPLICACAO_CASO_VACINAS.md`; alvo detalhado
  → `casos/vacinas/ARTIGO_VACINAS_alvo.md` (PDF: `casos/vacinas/political_quarrel.pdf`).
  Decisões de método do rotulador (eixo B) →
  `casos/vacinas/data/repl/vacinas2022/DECISOES_ROTULADOR.md`; resultado da Fase 3
  → `.../FASE3_curvas.md`.
- Plano do caso Instagram/Facebook → `casos/meta-ads-imigracao/REPLICACAO_CASO_META_ADS.md`;
  alvo detalhado → `casos/meta-ads-imigracao/ARTIGO_CAPOZZI_alvo.md`; viabilidade e rotas de
  coleta Meta descartadas → `.../data/repl/metaads2019/FASE0_descoberta.md`.
- **Contrato de documentação** (quais `.md` atualizar a cada mudança de estado, e como)
  → `.claude/skills/docs-em-dia/SKILL.md`. Vale para toda sessão: trabalho só termina
  quando o `.md` correspondente reflete a realidade.
