# STATUS — Artigo da Survey

> Controle de progresso da redação. Atualizado em **15/set/2026**.
> Workspace de redação: `dissertacao-escrita/survey/` (esta pasta), que reúne o
> manuscrito e os PDFs de referência. Movida de `Downloads/survey-redacao/survey/`
> em 2026-07-08 para o lar único da escrita. O repositório do sistema
> (`Documents/GitHub/redes-sociais-digitais-survey`) **não é modificado** — serve
> só como fonte de dados (`research.db`) e scripts.

## Arquivos do manuscrito (nesta pasta `survey/`)

- `survey.tex` — manuscrito (classe `article`, PT-BR). Compila com
  `pdflatex survey && bibtex survey && pdflatex survey && pdflatex survey`.
- `referencias.bib` — bibliografia (17 refs, todas citadas, sem `[REF?]`; as 4
  novas da rodada 4 foram copiadas da `.bib` da dissertação, onde já estavam conferidas).
- `survey.pdf` — última compilação (15 p., 15/set/2026, rodada 6 v6, base 2.472,
  limpa: zero erros, zero citações indefinidas, zero `Overfull`).
- `revisoes/survey-N.pdf` — o PDF de cada **rodada de revisão**, para a Mariana
  comentar. Mesmo ciclo da dissertação; ver [revisoes/README.md](revisoes/README.md).
- `figuras.py` / `validacao.py` — geram as **6 figuras** e o `numeros.json` a partir
  do `research.db`. `agg_results.py` continua sendo a referência das agregações.
- `Addressing_Database-Related_Issues_in_Digital_Soci.pdf` — Heine et al. 2025 (SBBD), PDF de referência.

## Extração completa dos 198 PDFs (15/set/2026, dentro da rodada 6)

Detalhe em [revisoes/README.md](revisoes/README.md) §Extração completa. Em uma linha:
**os 198 PDFs que nunca tinham passado pelo modelo foram extraídos (196; 2 corrompidos;
6 com o texto lido pelo `pypdf`), e a base foi de 2.322 para 2.472.** Todos os números
foram refeitos por `revisoes/extracao198/aplica_numeros.py`. Nenhuma conclusão mudou (a
filtragem fica em 80,3%, e era 81,1%). 14 p., limpo; `versao_final/` atualizado.

## Rodada 5 — `revisoes/survey-5.pdf` (14/set/2026): os comentários do survey-4

Detalhe em [revisoes/README.md](revisoes/README.md) §rodada 5. Em uma linha: **texto
reescrito para tirar maneirismos de IA** (referência: a proposta dela, o SBBD 2023 do
grupo e a dissertação da Salgueiro); κ fora do texto (fica a concordância bruta); Claude
Haiku só como tentativa de triangulação; figuras junto do texto que as cita; três
pizzas no lugar da tabela dos grandes coletores. Duas afirmações corrigidas (a de
“análise de conteúdo” ser o pior rótulo e uma que a revisão não mede). Nenhum número
mudou. 14 p., limpo. `figuras.py` gera **9 figuras** (saiu a de κ do artigo, entrou
`fig_grandes`); a `.bib` tem 17 entradas, 15 citadas (Cohen e Landis-Koch não são mais
citados).

- [ ] ⏳ Decisão dela: dar mais foco ao **banco de dados**? Hoje é resultado secundário.

## Rodada 4 — `revisoes/survey-4.pdf` (14/set/2026): os comentários do survey-3

Detalhe e tabela comentário→mudança em [revisoes/README.md](revisoes/README.md) §rodada 4.
Em uma linha: **o achado passa a ser a onipresença da filtragem por critério** (não o
contraste com a amostragem); itálico só em inglês (89 → 46); plataformas e estratégia
viram barras (Figs. 3–4), BD vira pizza (Fig. 7), a temporal perde o eixo duplo; §2 com
Tufekci, Ruths & Pfeffer e Olteanu; o exemplo dos ≈2,8 bi de tweets passa de amostragem
a filtragem (Jimeno-Yepes 2015). Nenhum número mudou. 15 p., limpo. `figuras.py` gera
agora **9 figuras**.

- [x] Negrito no meio das frases — **cortado** a pedido dela (26 fora; ficam o título,
      “Palavras-chave” e os rótulos das 8 ameaças). `survey-4.pdf` republicado.
- [x] Dissertação conferida: já resume a revisão pela filtragem; nada a mudar.

## Rodada 3 — `revisoes/survey-3.pdf` (14/set/2026, noite): auditoria de vieses

Detalhe e tabela achado→correção em [revisoes/README.md](revisoes/README.md) §rodada 3.
Em uma linha: **base 2.322 + critério único Gemini + composição arXiv + descarte sem
DOI + validação 2023–26 declarada + a lacuna deixou de ser afirmada sem medida.**
13 p., zero erros, zero indefinidas, zero `Overfull`. `figuras.py` reescrito (só-Gemini,
série com/sem arXiv, reponderação por ano, releitura dos dumps do DBLP).

- [x] Recomendação nº 1 do DIAGNOSTICO (tipos de análise só-Gemini) — **aplicada**, e
      estendida a todas as tabelas.
- [x] Base da expansão (2.322) no artigo; o resultado dela virou a nova §3.5.
- [x] ~~⚠ **`corpo.tex` diverge de novo** (segue na base 1.723 e na união)~~ ✅
      **alinhado na mesma noite** (rodada 8 da dissertação, `revisao-8.pdf`), a pedido
      da Mariana: base 2.322, Tab. 1.1 = Tab. 4 (só Gemini), Twitter 64,9%, e a lacuna
      citada sem afirmar o que a extração não mede. Ver
      [REVISOES.md](../dissertacao/revisoes/REVISOES.md).
- [ ] Prompt novo (“avaliou o efeito da redução?”, redução pré × pós-coleta, sem
      “conveniência” como amostragem) + gabarito humano sorteado (≈30 dev + 50 teste,
      estratificado por ano) — só Gemini, ~6–26 h de máquina, ~R$200.
- [ ] Reimportar os 2.915 títulos sem DOI (ICWSM, HICSS, AIS, CLEF) pelo `ee` do DBLP.

## Rodada 2 — `revisoes/survey-2.pdf` (14/set/2026): "levantamento sistemático" → "revisão"

- Pedido do orientador, confirmado pela Mariana: **"revisão"**, e não "revisão
  sistemática". O artigo passa a se chamar *"Coleta, Filtragem e Volume em Análises
  de Redes Sociais Digitais: uma Revisão da Literatura"*; toda autorreferência ("o
  levantamento", "levantamento sistemático e reprodutível") virou "a revisão", com a
  concordância no feminino; a palavra-chave "revisão sistemática" virou "revisão da
  literatura".
- **Mantidos de propósito**, porque falam de outros trabalhos: "levantamento manual"
  para o trabalho do Heine (§2 e §5) e "revisões sistemáticas tradicionais" (§2).
- **Nenhum número mudou.** 12 p., zero erros, zero indefinidas, zero `Overfull`.
- ✅ A dissertação foi alinhada no mesmo dia (`revisao-7.pdf`): mesma terminologia,
  título novo no `.bib` dela, e os números de abertura trazidos para a base deste
  artigo (1.723). A divergência da rodada 1 (abaixo) **deixou de existir**. Mapa em
  [../dissertacao/revisoes/REVISOES.md](../dissertacao/revisoes/REVISOES.md).
- ✅ Autoria e afiliação copiadas do front-matter da dissertação (Departamento de
  Informática, PUC-Rio, Rio de Janeiro), e agradecimento à CAPES (Código de
  Financiamento 001) com o texto da dissertação. E-mails informados pela Mariana:
  `mbarreto@inf.puc-rio.br` e `sergio@inf.puc-rio.br`.

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
| Resumo | revisado 9/set | reescrito na base 1.723; lidera pelo achado e já traz os 339 grandes coletores |
| 1. Introdução | rascunho revisado | polida; removida afirmação quantitativa não sustentada |
| 2. Trabalhos Relacionados | rascunho revisado | Heine incorporado como precursor nacional |
| 3. Metodologia | revisada 9/set | + Fig. 1 (funil) e + Fig. 2 (κ por campo); o "≈85%" único saiu e virou κ campo a campo |
| 4. Resultados | revisada 9/set | reorganizada em 5 subseções; **+§4.1 plataformas e série anual** (Fig. 3), +Tab. de famílias de API, +Fig. 4 (amostragem×filtragem), +Fig. 6 (persistência); todos os números regerados na base 1.723 |
| 5. Discussão | revisada 9/set | Heine incorporado; + parágrafo sobre os dois achados laterais (série temporal e persistência) |
| 6. Ameaças à validade | revisada 9/set (2×) | de 4 para **6** itens: + viés de acesso **medido por censo** (7,7%, 811/11.093) e + cobertura desigual dos modelos (+87%) |
| 7. Conclusão | rascunho revisado | escala ancorada (13.395/1.723); reescrita em 9/set p/ liderar pelo achado |

> ⚠ A coluna "Estado" acima descreve o **fonte**. O que foi publicado em
> `revisoes/survey-1.pdf` está escrito **como artigo fechado**, de propósito: o que
> ainda está em aberto aparece lá como *ameaça à validade medida*, não como pendência.
> As pendências reais continuam listadas neste arquivo, e só aqui.

## Rodada 1 de revisão — `revisoes/survey-1.pdf` (9/set/2026)

Primeira compilação publicada para leitura da Mariana. **11 páginas**, zero erros,
zero referências indefinidas, zero `Overfull`.

### Números recomputados: a base foi de 1.718 para **1.723**

O `research.db` mudou desde jul/2026 porque o **piloto de 5 artigos** da expansão
entrou no banco. Todo o `.tex` foi regerado contra o banco atual:

| | antes (jul) | agora (9/set) |
|---|---:|---:|
| extraídos | 2.139 | **2.147** |
| descartados (`suggested_discard`) | 421 | **424** |
| base de caracterização | 1.718 | **1.723** |
| com volume legível | 1.518 | **1.522** |
| Twitter / API / rótulo ``conteúdo'' | 1.095 / 1.198 / 1.040 | **1.097 / 1.200 / 1.045** |

**Nenhum achado se move**: amostragem 18,7%, filtragem 80,3%, mediana 273 mil, 339
grandes coletores (24% amostram, 88% filtram) — todos idênticos.
~~⚠ O `corpo.tex` da dissertação **não** foi atualizado e segue em 2.139/1.718;
divergência registrada no [ESTADO.md](../../ESTADO.md) §4.24.~~ ✅ Alinhado em
14/set/2026 (rodada 2).

### O que o artigo ganhou

- **6 figuras**, todas reprodutíveis (`figuras.py` + `validacao.py` → `numeros.json`):
  funil do levantamento; série anual com a fatia do Twitter/X; κ por campo;
  amostragem × filtragem; distribuição de volume; persistência corpus × grandes
  coletores. Paleta única, verificada para daltonismo em OKLab.
- **§4.1 nova — "Plataformas, e a dependência de uma só"**: a fatia do Twitter/X vai
  de **95% em 2014 a 14% em 2026**, com inflexão em 2023. É a demonstração mais
  concreta de que a composição da literatura segue a **disponibilidade de coleta**, e
  não o interesse de pesquisa. Vira também um parágrafo da Discussão.
- **Tabela nova de famílias de API** efetivamente nomeadas (Twitter/X 749, YouTube
  143, Reddit 140, Facebook/Instagram 76, TikTok 46).
- **§3.4 reescrita**: a concordância inter-modelo deixou de ser o número único de
  ``≈85%'' e passou a ser reportada **campo a campo** (κ de Cohen sobre os 732
  duplamente lidos). O padrão é o argumento: **coleta e plataforma 0,64–0,99**
  (Reddit 0,99, Twitter 0,98, API 0,74), **tipos de análise** mediana **0,40**. O
  instrumento é sólido para o que o artigo afirma e frágil para o que ele usa como
  contexto. Entradas novas no `.bib`: `cohen1960kappa`, `landis1977measurement`.
- **§4.4 "Escala não traz infraestrutura" corrigida**: a versão antiga dizia que a
  precariedade ``persiste'' no topo do volume. Medido, o quadro é mais fino — os
  grandes coletores publicam **um pouco mais** (11% × 8% em repositório com DOI; 44%
  × 53% sem indicação nenhuma) e mencionam **menos** tecnologia de armazenamento
  (7% × 12%). O texto passou a dizer isso.
- **Ameaças à validade de 4 para 6 itens** — ver abaixo.

### As duas ameaças novas (e por que elas fecham decisões antigas)

1. **Viés de acesso, agora medido por censo** (item 3). ⚠ **Corrigido no mesmo dia,
   algumas horas depois da primeira publicação** — ver abaixo. A varredura de acesso
   aberto **terminou** em 23/ago/2026 com a fila **100% tentada** (11.093 artigos) e
   recuperou **811** deles: **7,3%** da fila (IC95% de Wilson 6,8–7,8) e **7,7%** do
   estrato pago (772/10.039; IC95% 7,2–8,2). Por editora, de 8,9% (ACM) a menos de 4%
   (Emerald, T&F). Isto **fecha a decisão em aberto nº 1** de forma mais forte do que o
   previsto: não é projeção, é **censo** — a rota aberta foi esgotada, e o que ela
   alcança é pouco mais de um artigo em treze.
   ⚠ **O `survey-1.pdf` foi publicado citando 12,4% e uma projeção de ~830**, números
   da medição intermediária (34% da fila). O censo os desmente e **os ICs nem se
   sobrepõem**; o `.tex` foi corrigido e o PDF republicado no mesmo dia. A hipótese
   para a diferença — os 307 órfãos de disco no numerador intermediário — está em
   [EXPANSAO_recuperacao.md §3c](EXPANSAO_recuperacao.md) e **ainda precisa ser
   conferida**.
2. **Cobertura desigual dos modelos** (item 6). A tabela de tipos de análise agrega
   pela união, mas só **732 dos 1.723** foram lidos por dois modelos, e quem foi lido
   por dois acumula **4,23 rótulos contra 2,26** (+87%). O artigo passou a declarar
   isso, com a tabela recomputada só pelo Gemini dentro da própria ameaça (top-3
   sobrevive; magnitudes caem até 17 p.p.; 4ª e 5ª trocam).
   ⛔ **A recomendação nº 1 do [DIAGNOSTICO_tipos_de_analise.md](expansao/DIAGNOSTICO_tipos_de_analise.md)
   NÃO foi aplicada** — a Tab. 3 continua pela união, como no `corpo.tex`. Trocar a
   base é decisão da Mariana e mexe nos dois documentos de uma vez.

## Feito na sessão de 2026-07-02

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

- [x] **Como reportar a fração inacessível do corpus** (limitação vs. trabalho futuro).
      ✅ **Resolvida na rodada 1 (9/set/2026), pela terceira via**: nem "limitação"
      nem "trabalho futuro", e sim **limitação quantificada**. A medição virou o
      item 3 das Ameaças à validade do artigo, com a taxa final medida por censo
      (**7,7%** no estrato pago, 772/10.039, IC95% 7,2–8,2; **811** recuperados de
      **11.093** tentados) e a leitura de que a rota aberta não compensa o *paywall*.
      A decisão deixou de
      depender do fim da varredura: o artigo declara o tamanho do estrato que falta,
      e a extração da amostra pré-registrada, quando ocorrer, **testa** o achado em
      vez de destravar a redação. O histórico da medida fica abaixo.
      Registro anterior: parcialmente endereçado; Limitações §2 já quantificava o
      viés de editora.
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
- [ ] ⭐⛔ **Extrair os 800 da expansão, ou não?** Apurado em 9/set/2026: a varredura
      **acabou** em 23/ago (fila 100% tentada), recuperou **811 PDFs**, e a extração
      dos 800 sorteados **nunca rodou** — bug de shell, com o laço reportando
      `codigo 0` por cima do erro. **Nada foi gasto.** Extrair custa **~R$43** e
      levaria a base de **1.723 para ~2.360** (+37%).
      ⛔ **Mas a condição de parada pré-registrada disparou**: 7,7% no estrato pago,
      IC95% inteiro abaixo do piso de 11%, e o
      [PRE_REGISTRO](expansao/PRE_REGISTRO_expansao.md) §8 manda parar.
      A tensão: a parada foi escrita contra a **extrapolação**, e a varredura já
      aconteceu — os 811 existem de qualquer jeito. Extrair não desmente a aposta
      sobre a taxa, mas contraria a **letra** da condição. **A decisão precisa ficar
      escrita**; pré-registro contornado em silêncio vale menos que nenhum.
      Detalhe em [EXPANSAO_recuperacao.md §3c e §7](EXPANSAO_recuperacao.md).
- [ ] ⚠ **Conferir a hipótese dos 307 órfãos** antes de o 7,7% virar número final em
      qualquer outro lugar — é o que explicaria a queda de 12,4% para 7,7% com ICs
      que não se sobrepõem. Só o `survey.tex` depende disso hoje, e lá o valor está
      reportado como censo, que não muda.
- [ ] Gao/tipologia — resgatar se surgir fonte (ver memória do projeto).
- [x] **Propagar a base 1.723 para o `corpo.tex`?** ✅ **Feito em 14/set/2026**
      (rodada 7 da dissertação). Os dois documentos divergiam
      desde 9/set (2.139/1.718 lá, 2.147/1.723 aqui). É uma passada de `grep`, mas
      mexe em números de abertura da dissertação a 20 dias da defesa —
      [ESTADO.md](../../ESTADO.md) §4.24.
- [ ] **Aplicar a recomendação nº 1 do
      [DIAGNOSTICO_tipos_de_analise.md](expansao/DIAGNOSTICO_tipos_de_analise.md)?**
      Trocar a base da tabela de tipos de análise da união para só-Gemini alinha os
      dois achados ao mesmo critério e remove a dependência de qual artigo a cota
      alcançou. Hoje o problema está **declarado** no artigo (ameaça nº 6) mas
      **não corrigido**, e a mesma troca teria de acontecer na `tab:analises-survey`
      do `corpo.tex`. ⛔ o diagnóstico também alerta: **não** mexer no `vocabulary`
      antes de a expansão extrair, ou o `compara.py` passa a medir mudança de
      *prompt* em vez de viés de acesso.
