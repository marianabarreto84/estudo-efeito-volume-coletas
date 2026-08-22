# STATUS — Artigo da Survey

> Controle de progresso da redação. Atualizado em 2026-07-02.
> Workspace de redação: `dissertacao-escrita/survey/` (esta pasta), que reúne o
> manuscrito e os PDFs de referência. Movida de `Downloads/survey-redacao/survey/`
> em 2026-07-08 para o lar único da escrita. O repositório do sistema
> (`Documents/GitHub/redes-sociais-digitais-survey`) **não é modificado** — serve
> só como fonte de dados (`research.db`) e scripts.

## Arquivos do manuscrito (nesta pasta `survey/`)

- `survey.tex` — manuscrito (classe `article`, PT-BR). Compila com
  `pdflatex survey && bibtex survey && pdflatex survey && pdflatex survey`.
- `referencias.bib` — bibliografia (11 refs, todas citadas, sem `[REF?]`).
- `survey.pdf` — última compilação (limpa, sem citações indefinidas).
- `Addressing_Database-Related_Issues_in_Digital_Soci.pdf` — Heine et al. 2025 (SBBD), PDF de referência.

## Decisões fechadas (2026-07-02)

- **Venue/idioma:** PT-BR, template SBC (mira SBBD/Brasnam).
- **Achado amostragem × filtragem:** reportado sobre **Gemini** (cobre os 2.139;
  Claude Haiku só 887), com Claude como validação.
- **Escopo do corpus:** DBLP 2010–2026, 6 plataformas.
- **Heine et al. 2025 (SBBD):** incorporado como precursor nacional / gancho da
  lacuna (Mariana é coautora). Não há dataset nacional separado a minerar.
- **Gao et al. (tipologia usuários/relacionamentos/conteúdo):** em stand-by —
  referência não localizada; não usar até surgir fonte verificável.

## Seções

| Seção | Estado | Observações |
|---|---|---|
| Resumo | rascunho revisado | números atualizados p/ dados atuais |
| 1. Introdução | rascunho revisado | polida; removida afirmação quantitativa não sustentada |
| 2. Trabalhos Relacionados | rascunho revisado | Heine incorporado como precursor nacional |
| 3. Metodologia | rascunho revisado | nºs de coleta ancorados a maio/2026; piloto e ≈85% verificados |
| 4. Resultados | rascunho revisado | tabelas + amostragem/filtragem + persistência conferidos vs `research.db`; **+ §4.3 Volume de coleta** (Fig. 1 + Tab. grandes coletores) |
| 5. Discussão | rascunho revisado | Heine incorporado |
| 6. Limitações | rascunho revisado | viés de editora com nºs reais; +subconjunto extraído; +concordância |
| 7. Conclusão | rascunho revisado | escala ancorada (13.395/2.139) |

## Feito nesta sessão

- Adicionado BibTeX de `heine2025database` (SBBD 2025, pp. 977–983) e citado na Discussão.
- Corrigidos os percentuais de amostragem/filtragem para a base do Gemini:
  amostragem **18%** (Claude 20%), filtragem **72%** (Claude 82%). Antes: 16–17% / 60–73%
  — eram os números do **piloto n=100**, não do bulk (origem confirmada no METODOLOGIA.md §7.6.2).
- Persistência reescrita na escala do bulk (união, n=2.139): tecnologia de BD **\~14%**;
  GitHub **\~400**, "mediante solicitação" **\~130**, DOI persistente (Zenodo/Figshare/OSF)
  **\~145 (<7% do corpus)**. Antes: 40/21/dezena — também escala-piloto.
- Ancorados os números de coleta (17.812 hits, 102 consultas, 13.365 candidatos, 10.230
  paywall, 2.106 PDFs, 43% proxy) ao **recorte de maio de 2026** via nota de rodapé, e
  reconciliado 13.365 (dedup DBLP) → 13.395 (catálogo corrente). Esses números vêm de
  logs/`METODOLOGIA.md`, não do banco, e formam um snapshot internamente consistente.
- Verificados contra METODOLOGIA.md §7.6.1: piloto (sentimento 28, centralidade 26,
  "nenhum filtro" 35) e concordância média ≈85% — **todos corretos, sem alteração**.
- Ajustada a nota de cobertura dos Resultados (Gemini em todos os 2.139; Claude em 887).
- **Limitações reforçadas:** viés de editora com números reais (10.230 paywall; proxy só
  recupera Springer/IEEE, ≈43%; ACM/Wiley/SAGE/T&F/Emerald/Elsevier bloqueadas); nova
  limitação sobre o subconjunto extraído (2.139 acessíveis ≠ amostra aleatória dos 13.395);
  concordância inter-modelo ≈85% explicitada.
- **Prosa polida:** Trabalhos Relacionados cita Heine como precursor nacional; Introdução
  e Conclusão revisadas (escala 13.395/2.139 ancorada na Conclusão).
- **Alinhamento das LLMs (leitura de coerência):** removida a alegação de "três LLMs" como
  base dos resultados. Resumo/Intro/Metodologia agora refletem o real: piloto de 3 modelos
  → 2 retidos; **GPT-4o-mini descartado por qualidade** (o mais barato, mas inventava
  análises); **Claude Haiku 3–5× mais caro** que o Gemini → esquema de dois níveis (Gemini
  em todo o corpus e base dos resultados; Claude em 887 = ≈41%, triangulação). IDs exatos
  em nota de rodapé (`gemini-2.5-flash`, `gpt-4o-mini`, `claude-haiku-4-5-20251001`) + custos.
  Gabarito precisado como **1 artigo**; "PDFs acessíveis" (cobre proxy); "estrutura de rede".

## Volume de coleta — §4.3 estendida ao corpus completo (2026-07-03)

- **§4.3 "Volume de coleta e os grandes coletores"** + **Figura 1**
  (`fig_volume.pdf`, gerada por `fig_volume.py` — script reprodutível que lê
  `research.db`). Gráfico de barras da distribuição por ordem de grandeza.
- **DESCOBERTA-CHAVE:** o volume estruturado NÃO precisava ser re-extraído. O
  campo `collection_items` (pares quantidade/unidade) **já existia dentro do
  JSON `articles.analyses['gemini']` para todo o corpus** — só tinha sido
  "promovido" à coluna top-level `collection_items` nos 210 recentes. Custo de
  extensão: **zero** (sem LLM, sem PDF).
- **Escopo agora:** todo o corpus. **1.798 dos 2.139** têm ao menos uma
  quantidade legível (mesma base do resto dos Resultados). `fig_volume.py`
  reescrito p/ ler o JSON.
- **Regra de limpeza (nova):** o volume por artigo = maior quantidade entre os
  `collection_items`, **excluídas unidades que não são itens coletados**
  (`tokens`, `visualiza*`, `palavra*`/`word`, `senten*`, `requisi*`/`http`).
  Motivo: sem isso, a métrica "maior quantidade" pegava artefatos — ex. 1 trilhão
  de *tokens* de embeddings (id 9254) e 17 bi de *views* (id 530), que não são
  coleta. Documentado em nota de rodapé da §4.3.
- **Números novos:** mediana ≈115 mil; 27% <10 mil; **35% ≥1 mi**;
  **348 (19%) ≥10 mi** (antes 10%). Extremos reais: 118 bi tweets (decahose
  Twitter, década), 30,9 bi arestas (grafo interno Twitter), 13 bi comentários
  (dump Reddit).
- **Grandes coletores (≥10 mi, n=348):** amostram 81 (23%); filtram 302 (87%);
  tecnologia de BD 27 (8%); persistência — DOI/repo 40, GitHub 64, sob
  solicitação 21, outra menção 65, **nenhuma 158 (45%)**. Tabela `tab:grandes`.
  Exemplos de recorte: 2,8 bi→28 mi (1%); 500 mi→28 mil (0,01%). Conferidos vs
  `research.db`.
- **RESOLVIDO:** a decisão de escopo (210 vs corpus) foi fechada — estendido ao
  corpus. O denominador da §4.3 agora é consistente com o resto (base 2.139).

## Reenquadramento de tom — foco em resultados (2026-07-03)

- **Título trocado** para *"Coleta, Filtragem e Volume em Análises de Redes
  Sociais Digitais: um Levantamento Sistemático da Literatura"* — o LLM sai da
  manchete e vira detalhe de metodologia.
- **Resumo reescrito** liderando pelo problema e pelos achados (amostragem rara
  × filtragem norma; grandes coletores); LLM citado ao final como escolha
  metodológica, não como contribuição.
- **Introdução:** contribuições reordenadas — a caracterização empírica passa a
  ser a contribuição central; pipeline e extração multi-modelo viram
  instrumentos de apoio. Removido "O método é reutilizável...".
- **Conclusão:** removida a frase que vendia o método multi-modelo como
  contribuição reutilizável.
- **Resultados reescritos em tom "resultado primeiro"**: preâmbulo abre pelo que
  a seção mostra (base 2.139 vira fecho); achado central (18%/72%) lidera o
  parágrafo, mecânica de concordância vai ao fim; §4.3 abre pela cauda longa
  antes de explicar o recorte de 210.
- Recompilado limpo (sem citações indefinidas).

## Base de análise: 2.139 → 1.718 (exclusão dos descartados, 2026-07-03)

- **Decisão da Mariana:** excluir os artigos que o Gemini marcou
  `suggested_discard` (não coletam dados de RSD — entrevistas, estudos
  qualitativos). São **421 dos 2.139**. Nova base de análise = **1.718**.
- **Funil no artigo:** 13.395 catalogados → 2.139 extraídos → 1.718 coletam RSD.
  Documentado na Metodologia (§Validação) e propagado a TODAS as tabelas.
- **Reprodutibilidade:** criado `survey/agg_results.py`, que replica a lógica
  canônica de `scripts/survey_data_sources.py` (mesmos `norm`/`bucketize`/união
  de modelos) + filtro de descarte. **Validado**: com `--keep-all` reproduz
  exatamente os números antigos de 2.139 (API 1215/56,8%, os 12 buckets, 18,3%/
  71,9%, GitHub 402, DOI 149…). Sem flag → base 1.718.
- **A exclusão FORTALECE o achado** (descartados quase não coletavam via API):
  API 56,8→**69,7%**; filtragem 72→**80,3%**; Twitter 56,8→**63,7%**; amostragem
  ~igual (18,7%). No volume, mediana **115 mil→273 mil** (descartados eram
  coletas minúsculas).
- **Números atualizados no `.tex`** (todos conferidos): plataformas, estratégia,
  12 tipos de análise, amostragem/filtragem (Gemini 18,7/80,3; Claude 21/91),
  persistência, "análise de conteúdo" 1.396→1.040, abstract/intro/limitações/
  conclusão, e a §4.3 inteira (N=1.518; grandes coletores 348→**339**; tabela
  `tab:grandes` recomputada; fig regenerada com filtro de descarte).
- Recompilado limpo.

## Pendências de dados (rastreabilidade)

Rastreabilidade fechada nesta sessão. Observações remanescentes:

- Números de coleta/`download` são snapshot de maio/2026 (ancorado por nota de rodapé).
  Se for regerar tudo na versão corrente do banco, os números de log (17.812 hits, 102
  consultas, 43% proxy) precisam vir do `fetch_refs_gemini.log`, não do `research.db`.
- Os `\~400/\~130/\~145` de persistência saem de contagem por substring em `persistence_info`
  (união dos modelos); reprodutível, mas aproximado — por isso reportados com `\approx`.

## Decisões fechadas (2026-07-02, cont.)

- [x] **Fonte de verdade do manuscrito:** `survey-redacao/survey/` é a fonte única. A
      cópia antiga em `redes-sociais-digitais-survey/survey/` foi **deletada** (conferido
      antes que nada útil se perdia — só continha os números defasados que corrigimos). A
      deleção aparece no `git status` do repo do sistema; commit a critério da Mariana.
- [x] **Coautoria/ordem:** manter **Mariana Barreto** (1ª) e **Sérgio Lifschitz**. Sem mudança no `\author`.

## Decisões em aberto

- [ ] Como reportar a fração inacessível do corpus (limitação vs. trabalho futuro).
      Parcialmente endereçado: Limitações §2 já quantifica o viés de editora.
      ◐ **Em andamento desde 21/ago/2026** — a decisão pode deixar de ser
      "como reportar" e virar "o que a medição mostrou". Apurou-se que a marcação
      `pdf_inaccessible` está desatualizada: **13,25%** do estrato pago (IC95%
      10,3–16,9%) baixa por acesso aberto, o que projeta **~1.334 artigos** e
      levaria a base de 2.139 para **~3.473 (+62%)**.
      **Atualizado em 22/ago/2026:** a varredura já tentou **3.742** artigos e
      recuperou **443** — no estrato pago, **12,4%** (412/3.321, IC95% 11,3–13,6),
      dentro do IC do lote de 400 e **acima** do piso de 11% da condição de
      parada. Projeção para os 6.718 pagos ainda não tentados: **+833** (IC95%
      +761 a +912). A varredura foi retomada às 17:02 de 22/ago e a extração
      **ainda não começou**.
      Ver [EXPANSAO_recuperacao.md](EXPANSAO_recuperacao.md); o passo seguinte é
      pré-registrar a amostra e medir se os achados se movem, não extrair tudo.
      ⚠ O proxy institucional **não** foi usado: as editoras bloqueiam automação
      e o risco recai sobre o acesso da PUC-Rio inteira (§4 daquele documento).
- [ ] Gao/tipologia — resgatar se surgir fonte (ver memória do projeto).
