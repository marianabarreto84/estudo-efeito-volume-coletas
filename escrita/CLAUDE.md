# CLAUDE.md — Escrita da Dissertação

> 📍 Esta pasta agora é `escrita/` dentro de `Documents/dissertacao/`. O mapa geral
> (escrita + casos de replicação) está no **`../CLAUDE.md`** (pasta-mãe). Este arquivo
> cobre só a **redação**.

> Lar **único da escrita** da dissertação de mestrado da Mariana (PUC-Rio,
> Informática; orientador Prof. Sérgio Lifschitz; grupo eTC/TriTech).
> Aqui fica **só a redação** — dissertação + survey + material de referência.
> O **desenvolvimento** (sistema de levantamento, coleta, experimentos) mora
> em outros repositórios e **não é modificado** a partir daqui.

---

## 1. O que é a dissertação

**Título de trabalho:** *O Efeito da Estratégia de Coleta em Análises de Redes
Sociais Digitais: um Desenho Experimental sobre Coletar Mais.*

Análises computacionais sobre Redes Sociais Digitais (RSD) — de SNA a modelagem
de tópicos — dependem de uma etapa de **coleta de dados** raramente
problematizada. A dissertação:

- parte do achado da **survey** (companion) de que a **amostragem estatística é
  rara** e a **filtragem por critério é a norma** — a literatura recorta o
  objeto de coleta sem verificar se o recorte preserva as conclusões;
- propõe um **desenho experimental** que trata cada artigo como uma amostra
  sub-coletada do seu tema, coleta um **superconjunto _on-theme_** (mais dados,
  mesmo assunto) e mede, por tipo de análise, se a conclusão **muda** e se já
  havia **convergido** no volume original;
- fixa um **_lineup_ de 5 casos** (Reddit, YouTube, TikTok, Instagram/Facebook),
  um por análise e por rede, com coleta ainda acessível hoje.

Perguntas de pesquisa e desenho completo estão em `dissertacao/dissertacao.tex`.

## 2. Estrutura desta pasta

```
dissertacao-escrita/
├── dissertacao/        Fonte da dissertação — classe OFICIAL PUC-Rio (thesispuc/ABNT). Ver dissertacao/README.md
│   ├── dissertacao.tex   arquivo principal (front-matter)
│   ├── corpo.tex         capítulos
│   ├── referencias.bib
│   ├── thesispuc.cls + .bst/.sty + puc.pdf   classe/estilos do template
│   └── dissertacao.pdf   última compilação (20 p.)
├── survey/             Artigo da survey (companion). Ver survey/CLAUDE.md e survey/STATUS.md
│   ├── survey.tex, referencias.bib, survey.pdf
│   ├── agg_results.py, fig_volume.py   scripts que reproduzem números/figuras a partir do research.db
│   └── ...
├── referencias/        Documentação de apoio (CÓPIAS; originais preservados na origem)
│   ├── proposta/         propostas de dissertação (várias versões), cronograma,
│   │                     apresentação/defesa de proposta, template PUC-Rio,
│   │                     proposta de colega (Rodrigo Motta) como referência de formato
│   ├── artigos/          artigos de referência (lineage eTC/Heine, casos do lineup, etc.)
│   └── salgueiro/        trabalho anterior (Salgueiro) que a dissertação assume como ponto de partida
└── INVENTARIO.md       índice do que há aqui, origem de cada item e relevância
```

`dissertacao/` e `survey/` foram **movidos** para cá; `referencias/` são
**cópias** (os originais seguem em `Downloads/Acadêmico/` e no `Downloads/`).

## 3. Relação com o desenvolvimento (fora daqui)

- **Sistema da survey** (`Documents/GitHub/redes-sociais-digitais-survey`):
  FastAPI + SQLite que cataloga a literatura; fonte de `research.db` e dos
  scripts. Os números da survey saem **dos dados** desse sistema, nunca de
  memória. Se um número no texto divergir dos dados, **os dados vencem** —
  sinalizar à Mariana.
- **Experimentos da dissertação** (coleta expandida, reprodução de análises):
  ainda a executar; ficam nos seus próprios repositórios. Esta pasta só
  **escreve** sobre eles.

## 4. Princípios de escrita

- **Rastreabilidade total.** Toda estatística deve ser reproduzível por um
  script/query. Nada de números soltos; marcar a origem em rascunho.
- **Não inventar referências.** Toda citação existe no corpus/`.bib` ou é
  confirmada pela Mariana. Em dúvida, marcar `[REF?]`.
- **Tom acadêmico, não de manifesto.** A lacuna emerge dos dados.
- **Terminologia fixa:** "redução de volume pré-coleta", "sub-coleta",
  "superconjunto/universo _on-theme_", "mudou? / convergiu?".
- **Figuras antes de prosa** na seção de resultados.
- **Não sobrescrever rascunhos** existentes sem confirmar; commits pequenos.
- Regras específicas da survey: ver `survey/CLAUDE.md`.

## 5. Nomenclatura (regra global da Mariana)

Nunca usar a palavra "claude" em nomes de branches, arquivos, projetos,
comentários, commits ou PRs. Branches descritivas (`feature/...`, `fix/...`).
