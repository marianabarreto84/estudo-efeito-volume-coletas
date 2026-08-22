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

**Título (como está no `dissertacao.tex`):** *O Efeito do Volume de Coleta sobre os
Resultados de Análises: Redes Sociais Digitais como Caso de Estudo.*

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
- fixa um **conjunto de 6 casos em 4 redes** (Twitter ×2, Reddit ×2, YouTube,
  TikTok), cobrindo seis tipos de análise, com coleta ainda acessível hoje. Todos
  estão escritos (Caps. 3 a 7): cinco executados por inteiro e o de TikTok em
  parte. ⚠ **Instagram/Facebook saiu do conjunto em 21/ago/2026**, por decisão da
  Mariana na 2ª rodada de revisão — a §2.4 do `corpo.tex` explica por quê (Meta
  sem rota de coleta compatível), e o material de trabalho segue documentado em
  `casos/meta-ads-imigracao/` para poder voltar. **Modelagem de tópico** é hoje o
  tipo de análise mais frequente do levantamento **sem caso executado**, e está
  declarada como limitação de cobertura. Ver a `tab:casos` no `corpo.tex` e o
  `ESTADO.md` da raiz.

Perguntas de pesquisa e desenho completo estão em `dissertacao/dissertacao.tex`.

⚠ **Desde a 4ª rodada de revisão (22/ago/2026)** o `corpo.tex` tem **nove**
capítulos, e não oito: entrou um **Cap. 2 de Trabalhos Relacionados**, e os casos
passaram a ser os Caps. 4 a 8. A **tabela mestre** (`tab:mestre`), que era anunciada
e não existia, agora é a Tabela 9.1, na §9.1; e a §9.2 é a seção nova sobre o papel
do banco de dados. O `.bib` foi de 27 para **43 entradas**.

## 2. Estrutura desta pasta

```
dissertacao-escrita/
├── dissertacao/        Fonte da dissertação — classe OFICIAL PUC-Rio (thesispuc/ABNT). Ver dissertacao/README.md
│   ├── dissertacao.tex   arquivo principal (front-matter)
│   ├── corpo.tex         capítulos
│   ├── referencias.bib
│   ├── thesispuc.cls + .bst/.sty + puc.pdf   classe/estilos do template
│   ├── figuras/          4 figuras + gerar_figuras.py (lê os JSON congelados dos casos)
│   ├── revisoes/         ciclo de revisão da Mariana — ver revisoes/REVISOES.md
│   │                     e a skill .claude/skills/revisao-dissertacao/
│   └── dissertacao.pdf   última compilação (76 p., 22/ago/2026, rodada 5)
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
