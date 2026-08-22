# Dissertação — versão oficial PUC-Rio

Manuscrito na classe oficial **`thesispuc`** (template PUC-Rio), com bibliografia
**ABNT** via `abntex2cite`. Compila limpo (**76 p.**, sem citações indefinidas e
**sem `Overfull \hbox`**) — última compilação em **22/ago/2026**, após a 4ª rodada
de revisão.

```
pdflatex dissertacao && bibtex dissertacao && pdflatex dissertacao && pdflatex dissertacao
```

## Arquivos

- `dissertacao.tex` — arquivo principal / front-matter (autoria, título PT/EN,
  resumo/abstract, palavras-chave, agradecimentos — **inclui CAPES**, banca,
  dedicatória, epígrafe). Campos a confirmar marcados com `% TODO`.
- `corpo.tex` — capítulos (Contexto/Objetivos; Metodologia; caso \#Eleições2014;
  caso do debate vacinal; casos de Reddit; caso do YouTube; caso do TikTok;
  Conclusão parcial).
- `referencias.bib` — bibliografia.
- `figuras/` — figuras da dissertação **e o script que as gera**
  (`gerar_figuras.py`), que lê os JSON congelados dos casos. Nenhum número é
  digitado à mão: para refazer as figuras, `python gerar_figuras.py` a partir
  dessa pasta. O `.tex` acha os arquivos via `\graphicspath`.
- `audita_numeros.py` — **o número bate com o dado?** Confere os números do
  `corpo.tex` contra os JSON congelados dos casos. Rode `python audita_numeros.py`
  a partir desta pasta sempre que o texto ou um caso mudar de número. Cada linha
  diz de onde o valor sai; `AUSENTE` não é necessariamente erro (o número pode ter
  sido omitido de propósito ou escrito por extenso), mas pede olho humano. Em
  21/ago/2026: **72 conferidos, 69 encontrados, 3 ausentes** — e as três ausências
  são o AV4 do caso vacinas, divergência real registrada no
  [ESTADO.md](../../ESTADO.md) §4.19.
- `audita_contas.py` — **a conta fecha?** Não conhece os dados: audita o texto
  contra ele mesmo. Quatro camadas — (1) automática, que varre o `.tex` e testa
  todo delta em pontos percentuais, par que deveria somar 100, IC que deveria
  conter a estimativa, fração "X de Y" e linha de tabela contra o `N` da legenda;
  (2) declarada, uma tabela de relações que só um humano enxerga na prosa (razões,
  números por extenso, contas que atravessam parágrafos) e que vira teste de
  regressão; (3) sanidade (% fora de faixa, IC invertido, κ ou *p* impossíveis); e
  (4) **procedência**, que lista todo número do texto sem correspondência em JSON
  de caso. Em 21/ago/2026: **99 checagens, 0 erro**; 271 números distintos, 17 sem
  fonte no repositório e 12 só em `.md` de caso.
  ```
  python audita_contas.py               # só o que precisa de olho
  python audita_contas.py --tudo        # inclui o que passou
  python audita_contas.py --procedencia # só a camada de procedência
  ```
  **Ao mexer num número do texto, acrescente a relação correspondente na tabela
  `RELACOES`** — é ela que impede que uma edição altere um valor e deixe o outro
  lado da conta para trás.
- `revisoes/` — o ciclo de revisão da Mariana. Ver
  [revisoes/REVISOES.md](revisoes/REVISOES.md).
- `thesispuc.cls`, `abnt-alf.bst`, `abnt-num.bst`, `abntex2cite.sty`,
  `atbeginend.sty`, `subimages.sty`, `puc.pdf` — classe/estilos/recursos do template.
- `dissertacao.pdf` — última compilação.

## Ciclo de revisão

A Mariana comenta o PDF (destaques com balão) e salva em `revisoes/`. A rodada
seguinte aplica os comentários no fonte e salva um `revisao-N+1.pdf` na mesma
pasta, com o mapa comentário→mudança em
[revisoes/REVISOES.md](revisoes/REVISOES.md). **Nunca sobrescrever um
`revisao-N.pdf` já comentado.** O procedimento completo está na skill
[`revisao-dissertacao`](../../.claude/skills/revisao-dissertacao/SKILL.md).

Estado atual: `revisao-1.pdf` (comentado, pp. 6–27) → `revisao-2.pdf` (comentado
por inteiro, 56 anotações) → `revisao-3.pdf` (comentado até a p. 21, 20 anotações)
→ `revisao-4.pdf` (comentado, 17 anotações, pp. 9–56) → **`revisao-5.pdf`**,
aplicado em 22/ago/2026 e aguardando leitura. ⚠ A 4ª rodada saltou da p. 26 para a
p. 56, então **os capítulos do debate vacinal, do Reddit e do YouTube seguem sem
comentário desde o `revisao-2.pdf`** — é por aí que a próxima leitura rende mais.

## Pendências do front-matter

- ✅ **Data da defesa** — 29/set/2026, do *Formulário de Marcação de Defesa*.
- ✅ **Banca** — Edward Hermann Haeusler (PUC-Rio) e Ana Carolina Brito de Almeida
  (UERJ), além do orientador. O suplente (Marcos Vianna Villas) não entra na folha
  de aprovação.
- ✅ **Resumo pessoal / bio** — Engenharia da Computação, PUC-Rio.
- ⏳ **Dedicatória** — ainda um texto genérico.
- ✅ **Epígrafe** — deixou de ser pendência em 21/ago/2026: a chamada vazia imprimia
  uma página em branco com `, .`, e as três linhas foram **comentadas** no
  `dissertacao.tex`. Para pôr uma epígrafe de verdade, descomente-as.
- Agradecimentos: ampliar se desejar (a menção à CAPES já está incluída).

## Notas da classe `thesispuc` (para não reintroduzir bugs)

- ⚠ **A classe tem um `\fi` faltando, e a cópia deste repositório está corrigida.**
  Em `\puc@showfrontmatter` (linha 1587), o `\if@pucepigraph` não era fechado. Com a
  epígrafe ligada o `\if` fica pendente sem dano visível; **desligada**, o TeX sai
  pulando à procura do fecho e engole `\puc@setmargins@text`, `\onehalfspacing`,
  `\rmfamily`, `\puc@setpagestyle` e o próprio `\begin{document}` — daí o erro
  "Can be used only in preamble" e o documento encolhendo para 56 p. sem espaçamento
  um e meio. Era isto que a nota antiga desta lista descrevia como "a classe exige
  `\dedication` e `\epigraph` definidos": o sintoma, não a causa. Corrigido em
  21/ago/2026. **Se a versão final precisar da classe intocada**, reverta a linha e
  volte a chamar `\epigraph` (com conteúdo, ou a página em branco volta).
- Seções opcionais desativadas via `\abreviationsmode{none}`, `\codesmode{none}`,
  `\algorithmsmode{none}` (macro é `algorithms`, com "h").
- `puc.pdf` (logo da capa) precisa estar na pasta.
- Citações em ABNT: `\cite{...}` (parentético) e `\citeonline{...}` (autor no texto).
- URLs **muito** longas na bibliografia estouram a caixa (`Overfull \hbox`). O
  `url`/`hyperref` da classe quebra nas barras, o que basta para URLs curtas; para
  uma URL longa demais, carregar `\usepackage{xurl}` **depois** do `abntex2cite`.
  Aconteceu em 21/ago/2026 com a entrada `bbc2026vacinas` enquanto ela apontava para
  a republicação na Folha; com a URL curta da BBC o pacote deixou de ser necessário
  e foi removido.
