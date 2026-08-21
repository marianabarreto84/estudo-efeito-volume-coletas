# Dissertação de Mestrado — Mariana Barreto (PUC-Rio, Informática)

Orientador: Prof. Sérgio Lifschitz (grupo eTC/TriTech/TreeTech).

Este repositório reúne, num só lugar, a **escrita** da dissertação e os **casos de
replicação** que a alimentam.

## A tese em uma frase

Análises computacionais sobre Redes Sociais Digitais (SNA, modelagem de tópicos,
sentimento, estatística) dependem de uma etapa de **coleta** raramente problematizada.
A survey companion mostra que **amostragem estatística é rara** e **filtragem por
critério é a norma**. A dissertação propõe um desenho experimental **"coletar mais"**:
tratar cada trabalho publicado como uma amostra sub-coletada do seu tema, coletar um
**superconjunto _on-theme_** e medir, por tipo de análise, se a conclusão **mudou** e se
já havia **convergido** no volume original.

## Por onde começar

| Arquivo | O que é |
|---|---|
| [`ESTADO.md`](ESTADO.md) | **O agora**: o que está desbloqueado, o que está travado e em quê, o que espera decisão. Primeira e última leitura de toda sessão. |
| [`CLAUDE.md`](CLAUDE.md) | **O mapa estável**: estrutura das pastas, infra compartilhada, princípios de trabalho. |
| [`casos/RESULTADOS_tabela_mestre.md`](casos/RESULTADOS_tabela_mestre.md) | **O entregável central** (Fase 4): a tabela "mudou? / convergiu?" por tipo de análise e por rede. |
| [`BALANCO_2026-08-07.md`](BALANCO_2026-08-07.md) | Histórico de uma jornada de trabalho — não é estado. |

## Estrutura

```
escrita/            A REDAÇÃO
├── dissertacao/      fonte LaTeX (classe oficial PUC-Rio / ABNT)
├── survey/           artigo companion + scripts reprodutíveis
└── referencias/      propostas, template PUC-Rio, material de referência

casos/              OS CASOS DE REPLICAÇÃO (geram a evidência)
├── twitter-ituassu/    Ituassu & Lifschitz 2015/2018 — mídia + stance
├── heine-xande/        Heine & Lifschitz 2025 — tópicos (BERTopic) + quantitativa
├── vacinas/            Verjovsky et al. 2023 — rede (modularidade) + conteúdo/framing
├── reddit-buntain/     Buntain & Golbeck 2014 (WWW) — SNA / papéis sociais
├── reddit-massachs/    Massachs et al. 2020 (WebSci) — homofilia / polarização
├── meta-ads-imigracao/ Capozzi et al. 2021 (CHI) — classificação pró/anti-imigração
├── youtube-agecovp/    AGECovP — modelagem de tópicos
├── tiktok/             PoliTok-DE — análise de conteúdo
└── reddit-companhia-ia/ ❌ descartado (tombstone no README)
```

Cada caso segue o mesmo protocolo, e cada etapa deixa um `.md` rastreável:

**Fase 0** diagnóstico da fonte → **Fase 1** snapshot congelado em SQLite/CSV local →
**Fases 2–3** análises reprodutíveis *sobre o snapshot*, sem rede →
**Fase 4** tabela mestre "mudou? / convergiu?".

Dentro de um caso: `core/` (conexão e utilidades), `diagnostico/` (exploração da fonte),
`pipeline/` (extração e coleta), `analise/` (as medições) e `data/repl/<caso>/`
(snapshot + resultados + documentação de fase).

## Reprodução

```bash
pip install -r casos/<caso>/requirements.txt
cp .env.example .env      # preencher credenciais (ver CLAUDE.md §4)
python casos/<caso>/pipeline/extrai_snapshot_*.py    # Fase 1: gera o snapshot
python casos/<caso>/analise/<script>.py              # Fases 2-3: sobre o snapshot
```

As Fases 2–3 rodam **offline**, sobre o snapshot congelado — é o próprio desenho do
protocolo. Só a Fase 1 precisa de rede (VPN da Cloud-DI PUC-Rio, ou API pública, conforme
o caso).

## O que **não** está versionado

Ver [`.gitignore`](.gitignore). Em resumo:

- **Credenciais** — `.env`, certificados e perfis de VPN. Nunca entram.
- **Snapshots** (`*.sqlite`) — de 49 MB a 1,7 GB. São regeráveis pelos scripts de
  `pipeline/`, e cada um tem um `MANIFEST`/`FASE1_*.md` que registra como foi extraído.
- **Gabaritos externos volumosos** — dados publicados pelos autores dos artigos-alvo
  (Zenodo, dumps do Reddit, parquets do PoliTok). Baixáveis da fonte original; o `.md` da
  fase de cada caso diz de onde.
- **PDFs** — artigos de terceiros, documentos administrativos e saídas de compilação
  LaTeX. Única exceção: `puc.pdf`, o brasão exigido pela classe `thesispuc.cls`.
- **Artefatos de build** — LaTeX (`.aux`, `.bbl`, `.fls`, …), `__pycache__/`, logs.

## Princípios

- **Rastreabilidade total.** Nada de número solto: toda estatística sai de um script ou
  query versionado aqui.
- **Predições pré-registradas.** A aposta (mudou / não mudou) é registrada *antes* de
  medir, e o resultado é reportado mesmo quando a aposta falha.
- **Se um número no texto divergir dos dados, os dados vencem.**
- **Não inventar referências.** Toda citação existe no `.bib` ou foi confirmada.
