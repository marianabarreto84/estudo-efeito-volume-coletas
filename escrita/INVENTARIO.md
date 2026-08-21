# INVENTÁRIO — material de escrita reunido

> Montado em 2026-07-08. Mapeia cada item desta pasta, sua origem e por que é
> relevante para a escrita da dissertação. `dissertacao/` e `survey/` foram
> **movidos** para cá; tudo em `referencias/` são **cópias** (originais
> preservados na origem indicada).

## dissertacao/  (MOVIDO — era `Documents/GitHub/redes-sociais-digitais-survey/dissertacao/`)

| Arquivo | O que é |
|---|---|
| `dissertacao.tex` | Arquivo principal, **classe oficial PUC-Rio `thesispuc`** (front-matter). Núcleo = desenho experimental "coletar mais". |
| `corpo.tex` | Capítulos (Introdução, Desenho Experimental, Conclusão). |
| `referencias.bib` | Bibliografia da dissertação (ABNT). |
| `dissertacao.pdf` | Última compilação (20 p., limpa). |
| `thesispuc.cls` + `.bst`/`.sty` + `puc.pdf` | Classe/estilos/recursos do template PUC-Rio. |
| `README.md` | Como compilar, pendências `% TODO` e notas da classe. |

> Migrado em 2026-07-08 do rascunho em classe `report` para a classe oficial
> `thesispuc` (ABNT via `abntex2cite`); a versão `report` antiga foi removida.

## resumo-dissertacao.tex (raiz) — visão geral (classe `article`, NÃO o template PUC)

Documento autônomo que percorre cada capítulo/seção da dissertação atual (1–2
parágrafos por seção) e descreve o que ainda entra na versão final (os 5 casos
restantes do conjunto + o fechamento do caso do Twitter). Compila sozinho
(`pdflatex resumo-dissertacao`, 6 p.). A introdução é apresentada como a redigir
ao final.

> A pasta saiu do repositório git do sistema. No `git status` do repo ela
> aparecerá como removida — commit a critério da Mariana. A referência
> relativa `../survey/` dentro do `.tex` continua válida (survey/ está ao lado).

## survey/  (MOVIDO — era `Downloads/survey-redacao/survey/`)

Artigo companion da survey + PDF de referência (Heine et al. 2025) + scripts
reprodutíveis (`agg_results.py`, `fig_volume.py`) e `survey.tex`/`.pdf`/`.bib`.
Estado detalhado em `survey/STATUS.md`; regras de escrita em `survey/CLAUDE.md`.
As configurações `.claude/` (permissões da redação) também vieram para a raiz.

## referencias/proposta/  (CÓPIA — de `Downloads/Acadêmico/Dissertação/` + soltos no Downloads)

| Arquivo | O que é |
|---|---|
| `PropostaDissertacao_MarianaBarreto_20251217.pdf` | Proposta mais recente (17/12/2025). |
| `PropostaDissertacao_MarianaBarreto vSL.pdf` | Versão com marcações do orientador (SL). |
| `PropostaDissertacao_MarianaBarreto.pdf`, `-1.pdf` | Versões anteriores da proposta. |
| `ApresentacaoProposta_MarianaBarreto.pdf` | Slides da apresentação de proposta. |
| `defesa_proposta_mestrado.pdf`, `-1.pdf`, `-2.pdf` | Documentos da defesa de proposta. |
| `CronogramaMestradoAssinado_MarianaBarreto.pdf`, `cronograma_mestrado.pdf` | Cronograma do mestrado. |
| `Modelo_de_tese_e_dissertação_PUC_Rio.zip` | **Template oficial PUC-Rio** (classe puc-tese) para a versão final. |
| `Defesa_de_Proposta_Mariana_2023.zip` | Pacote da defesa de proposta (2023). |
| `PropostaDissertacao_RodrigoMotta_PUC_rio.pdf` | Proposta de colega — referência de **formato/estrutura**. |

## referencias/artigos/  (CÓPIA — de `Downloads/Acadêmico/Artigos/` + soltos no Downloads)

Artigos de referência (lineage do grupo e trabalhos relacionados). Destaques
identificados:

| Arquivo | O que é |
|---|---|
| `Barreto-etal-SBBD2023-Gerenciamento-Dados-RSD.pdf` | SBBD 2023, **co-autoria da Mariana** (Carmo, Rêgo, Barreto, Schuler, Heine, Villas, Lifschitz). Ferramenta eTC; análise de redes + tópicos. Precursor direto. |
| `Ituassu-Lifschitz-Eleicoes2014-Twitter.pdf` | Ituassu & **Lifschitz** — #Eleições2014 no Twitter (opinião pública, sentimento, mídia). |
| `Analysis-and-Prediction-of-Users-Emotional-Tone-in-Reddit-Me.bib` (+ PDFs correlatos) | Tom emocional de usuários no Reddit — relacionado aos casos de sentimento/Reddit. |
| `related-work-busca.pdf` | Busca por trabalho anterior semelhante ("já foi feito?") — material de trabalhos relacionados. |
| demais PDFs/`.bib`/`.enw` | Artigos de referência e exports de busca (EACL, Frontiers, EPJ Data Science, GNN/Twitter, TikTok etc.) — **não classificados individualmente**; triar ao redigir trabalhos relacionados. |

## referencias/salgueiro/  (CÓPIA — solto no Downloads)

| Arquivo | O que é |
|---|---|
| `Manuscrito Defesa Mestrado - Mariana Salgueiro.pdf` | Dissertação anterior (Salgueiro) — **ponto de partida** que a dissertação assume: especificação conceitual de RSD e esquema genérico. Citada como `salgueiro2023`/`salgueiro2022dbmodels`. |
| `Addressing_Database-Related_Issues_in_Digital_Soci.pdf` | Heine et al. 2025 (SBBD) — precursor nacional/gancho da lacuna. (Também presente em `survey/` como PDF de referência.) |

## O que ficou de fora (desenvolvimento/pessoal — permanece na origem)

- `Downloads/Projetos/` — app de séries (fiscal-de-series etc.), não relacionado.
- `Downloads/Exports Pessoais/`, faturas/IRPF/DAS-MEI, `proposta-modelagem-fisica.*`
  ("Sistema Financeiro Pessoal") — pessoais/fiscais, não relacionados.
- Interno do repo `redes-sociais-digitais-survey` (DBLP dumps, `database.py`,
  pipelines) — é o **sistema** (dados/scripts), não escrita.
