# Dissertação — versão oficial PUC-Rio

Manuscrito na classe oficial **`thesispuc`** (template PUC-Rio), com bibliografia
**ABNT** via `abntex2cite`. Compila limpo (30 p., sem citações indefinidas)
— última compilação em **07/ago/2026**.

```
pdflatex dissertacao && bibtex dissertacao && pdflatex dissertacao && pdflatex dissertacao
```

## Arquivos

- `dissertacao.tex` — arquivo principal / front-matter (autoria, título PT/EN,
  resumo/abstract, palavras-chave, agradecimentos — **inclui CAPES**, banca,
  dedicatória, epígrafe). Campos a confirmar marcados com `% TODO`.
- `corpo.tex` — capítulos (Contexto/Objetivos, Metodologia, caso \#Eleições2014,
  caso do debate vacinal, Conclusão parcial).
- `referencias.bib` — bibliografia.
- `thesispuc.cls`, `abnt-alf.bst`, `abnt-num.bst`, `abntex2cite.sty`,
  `atbeginend.sty`, `subimages.sty`, `puc.pdf` — classe/estilos/recursos do template.
- `dissertacao.pdf` — última compilação.

## Pendências (`% TODO` no `dissertacao.tex`)

- **Data da defesa** (`\day`/`\month`/`\year`).
- **Banca** (`\jury` — hoje com um membro placeholder).
- **Resumo pessoal / bio** (`\resume`).
- **Dedicatória** e **epígrafe** (placeholders).
- Agradecimentos: ampliar se desejar (a menção à CAPES já está incluída).

## Notas da classe `thesispuc` (para não reintroduzir bugs)

- Exige `\dedication` e `\epigraph` **definidos** (mesmo placeholder), senão dá
  erro "Can be used only in preamble".
- Seções opcionais desativadas via `\abreviationsmode{none}`, `\codesmode{none}`,
  `\algorithmsmode{none}` (macro é `algorithms`, com "h").
- `puc.pdf` (logo da capa) precisa estar na pasta.
- Citações em ABNT: `\cite{...}` (parentético) e `\citeonline{...}` (autor no texto).
