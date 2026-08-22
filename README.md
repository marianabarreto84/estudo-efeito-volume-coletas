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
| [`.claude/skills/`](.claude/skills/) | Os dois fluxos fixados da pasta: [`docs-em-dia`](.claude/skills/docs-em-dia/SKILL.md) (contrato de documentação — qual `.md` atualizar a cada mudança de estado) e [`revisao-dissertacao`](.claude/skills/revisao-dissertacao/SKILL.md) (ciclo de revisão do PDF). |
| [`BALANCO_2026-08-07.md`](BALANCO_2026-08-07.md) | Histórico de uma jornada de trabalho — não é estado. |

## Estrutura

```
escrita/            A REDAÇÃO
├── dissertacao/      fonte LaTeX (classe oficial PUC-Rio / ABNT)
│   ├── revisoes/       ciclo de revisão: revisao-N.pdf comentado → aplicado no fonte
│   │                   → revisao-N+1.pdf. Mapa comentário→mudança em REVISOES.md.
│   │                   NÃO se sincroniza com Documents/dissertacao/ (ver CLAUDE.md)
│   └── figuras/        figuras geradas pelos casos
├── survey/           artigo companion + scripts reprodutíveis (research.db)
└── referencias/      propostas, artigos de referência, trabalho do Salgueiro

casos/              OS CASOS DE REPLICAÇÃO (geram a evidência)
├── RESULTADOS_tabela_mestre.md   Fase 4: o entregável central, "mudou? / convergiu?"
├── twitter-ituassu/    Ituassu & Lifschitz 2015/2018 — mídia ✅ + stance ⏳
├── vacinas/            Verjovsky et al. 2023 — rede (modularidade) + conteúdo/framing ✅
├── reddit-buntain/     Buntain & Golbeck 2014 (WWW) — SNA / papéis sociais ✅
├── reddit-massachs/    Massachs et al. 2020 (WebSci) — homofilia / polarização ✅ (parcial)
├── youtube-agecovp/    Ghenai et al. 2025 (AGECovP) — sentimento + composição do corpus ✅
├── tiktok/             Ruiz et al. 2025 (PoliTok-DE) — conteúdo / persistência ✅ (eixo temporal)
├── heine-xande/        Heine & Lifschitz 2025 — tópicos (BERTopic) + quantitativa ⏳ aguarda os dados
├── meta-ads-imigracao/ ⛔ fora do escopo desde 21/ago/2026 — material preservado
└── reddit-companhia-ia/ ❌ descartado (tombstone no README)
```

O conjunto de casos da dissertação são **6, em 4 redes** (Twitter/X, Reddit, YouTube,
TikTok) — é o que a `tab:casos` do `corpo.tex` relata. Dois casos estão fora dele:
`heine-xande`, com documentação e pipeline prontos mas sem os dados (ver
[`CLAUDE.md`](CLAUDE.md) §5), e `meta-ads-imigracao`, que saiu do escopo em 21/ago/2026
por decisão da Mariana — Instagram/Facebook passou a ser tratado como **rota de coleta
fechada**, e não como caso pendente. Nada foi apagado: a Fase 0 e os gabaritos conferidos
seguem no lugar, e a célula reabre se uma rota compatível voltar a existir.

⚠ **Modelagem de tópico ficou sem caso executado.** O caso do YouTube entrega
sentimento e composição do corpus, não modelagem de tópico; é o quarto tipo mais
frequente do levantamento, e a lacuna está declarada no texto como limitação de
cobertura e como próximo passo.

Cada caso segue o mesmo protocolo, e cada etapa deixa um `.md` rastreável:

**Fase 0** diagnóstico da fonte → **Fase 1** snapshot congelado em SQLite/CSV local →
**Fases 2–3** análises reprodutíveis *sobre o snapshot*, sem rede →
**Fase 4** tabela mestre "mudou? / convergiu?".

Dentro de um caso: `core/` (conexão e utilidades), `diagnostico/` (exploração da fonte),
`pipeline/` (extração e coleta), `analise/` (as medições) e `data/repl/<caso>/`
(snapshot + resultados + documentação de fase).

## Reprodução

```bash
cp .env.example .env      # preencher credenciais (ver CLAUDE.md §4)
pip install -r casos/<caso>/requirements.txt         # onde houver: heine-xande,
                                                     # vacinas, youtube-agecovp
python casos/<caso>/pipeline/extrai_snapshot_*.py    # Fase 1: gera o snapshot
python casos/<caso>/analise/<script>.py              # Fases 2-3: sobre o snapshot
```

Os casos sem `requirements.txt` rodam sobre a mesma base (`pandas`, `networkx`,
`python-dotenv`, mais o driver do banco do caso); o `.md` de fase de cada um diz o que
usa. As Fases 2–3 rodam **offline**, sobre o snapshot congelado — é o próprio desenho do
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
- **PDFs** — artigos de terceiros, documentos administrativos, saídas de compilação
  LaTeX e os `revisoes/revisao-N.pdf` do ciclo de revisão (existem só na cópia local;
  o que fica versionado é o `REVISOES.md`, o mapa comentário→mudança). Única exceção:
  `puc.pdf`, o brasão exigido pela classe `thesispuc.cls`.
- **Artefatos de build** — LaTeX (`.aux`, `.bbl`, `.fls`, …), `__pycache__/`, logs.

## Princípios

- **Rastreabilidade total.** Nada de número solto: toda estatística sai de um script ou
  query versionado aqui.
- **Predições pré-registradas.** A aposta (mudou / não mudou) é registrada *antes* de
  medir, e o resultado é reportado mesmo quando a aposta falha.
- **Se um número no texto divergir dos dados, os dados vencem.**
- **Não inventar referências.** Toda citação existe no `.bib` ou foi confirmada.
- **Documentação é estado, não registro pós-fato.** Toda mudança de estado termina com o
  `.md` correspondente atualizado, na mesma sessão — ver
  [`docs-em-dia`](.claude/skills/docs-em-dia/SKILL.md).
