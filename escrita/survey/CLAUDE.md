# CLAUDE.md — Artigo da Survey

> Instruções para o Claude ao redigir o artigo da survey. O manuscrito vive
> agora em `Downloads/dissertacao-escrita/survey/` (lar único da escrita). Os
> **dados e scripts** continuam no repositório do sistema
> (`C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey`), que serve
> só como fonte (`research.db`) e **não é modificado** pela redação.
> Objetivo atual da frente: **fechar o artigo da survey**, que servirá de
> referência formal para a dissertação de mestrado.

---

## 1. Contexto do projeto

- Autora: Mariana, mestranda na PUC-Rio, orientada pelo Prof. Sérgio Lifschitz,
  no grupo de pesquisa eTC (TriTech).
- A dissertação investiga como **reduções de volume anteriores à coleta**
  (filtragem por palavra-chave, perfil, janela temporal, métricas de
  relevância) afetam análises de redes sociais digitais, expandindo
  Heine et al. (SBBD 2025) para múltiplas plataformas e tipos de análise.
- A **lacuna central** que o artigo deve evidenciar: os trabalhos da área
  descrevem *como* coletam, mas raramente avaliam *como as reduções de volume
  alteram os resultados* das análises.
- Enquadramento teórico: tipologia de Gao et al. (usuários / relacionamentos /
  conteúdo) para organizar os tipos de análise; Morstatter et al. (2013) como
  referência clássica do problema de amostragem (Streaming API vs Firehose).

## 2. O que este repositório contém

Este repo abriga o sistema de revisão da literatura que alimenta a survey:

- Backend **FastAPI + SQLite** que cataloga artigos sobre coleta de dados em
  redes sociais.
- Ingestão por **DOI/DBLP**, extração automática de metadados/conteúdo via
  **Gemini 2.5 Flash**, e **grafo de referências** entre artigos.
- Corpus de ~10 mil artigos (parte obtida via proxy institucional PUC-Rio;
  uma fração ainda inacessível por anti-bot/Cloudflare).
- Levantamento DBLP: **24.754 publicações (2000–2024)**, com predominância do
  Twitter (**54,5%**). Há também o mapeamento nacional (SBBD, Brasnam).

**Antes de escrever qualquer texto, explore o repositório**: leia o README,
os `.md` de protocolo existentes, os scripts de análise e os dados agregados
(tabelas/CSVs/queries) disponíveis. Os números do artigo devem sair **dos
dados do próprio sistema**, nunca de memória ou estimativa. Se um número
citado nestas instruções divergir do que os dados mostram, **os dados vencem**
— sinalize a divergência para a Mariana.

## 3. Objetivo e papel do artigo

O artigo da survey tem dupla função:

1. **Publicável por si só**: mapear sistematicamente como a literatura de
   análise de redes sociais digitais realiza (e reporta) a coleta de dados,
   com foco nas estratégias de redução de volume pré-coleta.
2. **Referência da dissertação**: fundamentar a lacuna que a parte
   experimental (protocolo de replicação por expansão) vai atacar. A survey
   *demonstra* que a lacuna existe; o experimento a *operacionaliza*.

O texto deve construir o argumento nessa ordem: (a) coleta é etapa decisiva e
onipresente; (b) reduções de volume são a norma, não a exceção; (c) quase
ninguém avalia o efeito dessas reduções sobre as conclusões; (d) logo, há uma
lacuna sistemática — que motiva a dissertação.

## 4. Estrutura sugerida do artigo

Ajuste conforme o venue-alvo, mas parta deste esqueleto:

1. **Introdução** — motivação, pergunta da survey, contribuições.
2. **Fundamentação** — tipologia de Gao et al.; conceitos de coleta
   (APIs, scraping, datasets públicos); tipos de redução de volume
   (palavra-chave, perfil/conta, janela temporal, relevância/engajamento,
   amostragem).
3. **Metodologia do levantamento** — fontes (DBLP, SBBD, Brasnam), critérios
   de inclusão/exclusão, pipeline de extração automática (incluindo validação
   da extração via LLM — reportar como foi verificada), grafo de referências.
4. **Resultados** — panorama quantitativo (plataformas, tipos de análise,
   evolução temporal 2000–2024), caracterização das estratégias de coleta e
   redução reportadas.
5. **Discussão / Lacuna** — quantos trabalhos avaliam o efeito das reduções?
   Confronto com Morstatter et al. (2013) e Heine et al. (2025).
6. **Ameaças à validade** — cobertura do corpus (fração inacessível),
   dependência do DBLP, extração automática, viés de idioma/venue.
7. **Conclusão e agenda** — apontar para avaliação sistemática do efeito de
   volume (ponte para a dissertação, sem antecipar resultados dela).

## 5. Princípios de escrita

- **Rastreabilidade total**: toda estatística no texto deve ser reproduzível
  por um script/query do repo. Ao escrever um número, indique em comentário ou
  nota de rodapé de rascunho a origem (`script/tabela`). Nada de números soltos.
- **Tom de survey, não de manifesto**: descrever a literatura com justiça antes
  de apontar a lacuna. A lacuna deve emergir dos dados, não de retórica.
- **Terminologia consistente**: fixar cedo os termos (ex.: "redução de volume
  pré-coleta", "sub-coleta", "universo on-theme") e usá-los uniformemente.
- **Transparência metodológica**: a extração via LLM e a fração inacessível do
  corpus são limitações a declarar explicitamente, não a esconder.
- **Figuras antes de prosa**: para a Seção de Resultados, gere primeiro as
  tabelas/figuras a partir dos dados, depois escreva o texto em torno delas.
- Não inventar referências. Toda citação deve existir no corpus do sistema ou
  ser fornecida/confirmada pela Mariana. Em caso de dúvida, marcar `[REF?]`.

## 6. Fluxo de trabalho esperado

1. Explorar o repo e inventariar o que já existe de texto do artigo
   (rascunhos, LaTeX, notas) e de dados agregados prontos.
2. Propor/confirmar o esqueleto de seções com a Mariana antes de redigir.
3. Escrever seção por seção, sempre gerando primeiro os artefatos
   quantitativos (tabelas, figuras) da seção correspondente.
4. Manter um `STATUS.md` (ou seção no README) com: seções concluídas,
   pendências de dados, decisões em aberto.
5. Commits pequenos e descritivos; não sobrescrever rascunhos existentes sem
   confirmar.

## 7. Decisões em aberto (perguntar à Mariana antes de assumir)

- [ ] **Venue-alvo** (e com isso: idioma PT/EN, template, limite de páginas).
- [ ] Formato do manuscrito no repo (LaTeX? Markdown? diretório dedicado?).
- [ ] Escopo temporal e de plataformas final do corpus reportado no artigo.
- [ ] Como reportar a fração inaccessível do corpus (limitação vs trabalho
      futuro de desbloqueio).
- [ ] Coautoria e ordem de autores.

## 8. O que NÃO fazer

- Não antecipar resultados da parte experimental da dissertação (protocolo de
  replicação); o artigo pode citá-la como agenda, no máximo.
- Não citar números do corpus sem regenerá-los a partir dos dados atuais.
- Não alterar o schema do banco ou os pipelines de ingestão como efeito
  colateral da escrita — se precisar de uma agregação nova, criar script novo
  em vez de modificar os existentes.
