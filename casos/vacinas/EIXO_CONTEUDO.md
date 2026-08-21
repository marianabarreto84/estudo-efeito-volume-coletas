# Eixo B — Rotulador de conteúdo (pró/anti + 14 categorias)

> Proposta de desenho para o rotulador automatizado do caso vacinas. O eixo E1
> (descer o limiar de viralidade) só existe se a análise de conteúdo escalar além
> da rotulagem manual do paper (1.525 tweets). Documento de decisão — a escolha
> final é da Mariana. Preços da API Anthropic em 23/jul/2026.

## 0. A tarefa e o gabarito

- **Tarefa por tweet:** (a) stance: pró-vacina / anti-vacina / não-relevante;
  (b) **14** categorias temáticas binárias — ver `data/repl/vacinas2022/CODEBOOK.md`.
  ⚠️ Este documento dizia **11** (número do corpo do preprint). O material
  suplementar numera **14**, e os 14 totais batem exatamente com a Tabela 5.
  Os dados vencem; o pipeline usa 14.
- **Gabarito:** `suplementar_rotulos.xlsx` / aba `Spreadsheet 1` — **1.525 tweets
  virais** com texto + rótulos humanos (2 codificadores + árbitro, Bardin).
- **Protocolo de validação (qualquer opção):** dividir o gabarito em
  ~500 de desenvolvimento (ajustar prompt/features) + ~1.000 de teste cego;
  reportar **κ de Cohen** (stance) e κ/F1 por categoria no teste cego.
  Critério de aceite proposto: κ ≥ 0,70 no stance e κ ≥ 0,60 na mediana das
  categorias (comparável a concordância humana típica em análise de conteúdo;
  o paper não reporta o κ entre os codificadores — citar como limitação).
  **Só depois de aprovado** o rotulador desce o limiar (Fase 3).

## 1. Volumes a rotular (originais, contagens da Fase 0)

> ⚠️ Contagens **sem filtro de idioma**. O corpus tem ~14% de tweets em
> francês e inglês (os termos provax/antivax pegaram o debate internacional),
> que foram **excluídos** da rodada real — ver §7. Escopo efetivo do E1:
> **29.983** tweets em português, não 34.866.

| Escopo | Tweets |
|---|---|
| >500 RT (validação; já tem gabarito p/ 1.525) | 1.686 |
| >250 RT | 3.384 |
| >100 RT | 6.836 |
| >50 RT | 11.207 |
| **>10 RT (alvo do E1)** | **34.866** |
| Corpus completo (se um dia precisar) | 2.046.816 |

## 2. Opção A — LLM documentado (recomendada)

**Como:** Claude **Haiku 4.5** via **Batch API** (assíncrona, −50% no preço),
prompt fixo versionado no repo com as definições das 11 categorias (traduzidas
do codebook do paper) + exemplos do conjunto de desenvolvimento; saída JSON
estruturada; `temperature=0`.

**Custo estimado** (Haiku 4.5: $1/M entrada, $5/M saída; batch −50%; system
prompt de ~2,5 k tokens com cache):
≈ **US$ 0,0005/tweet** →

| Volume | Custo aprox. |
|---|---|
| Validação (1.686) | < US$ 1 |
| Até >10 RT (34.866) | ≈ US$ 15–20 → **real: US$ 6,33** (29.983 pt) |
| Amostra de 100 k do corpus | ≈ US$ 50 |
| Corpus completo (2 M) — não recomendado | ≈ US$ 1.000 |

(Com Sonnet no lugar do Haiku: ×2–3 nos valores. Só se o κ do Haiku reprovar.)

**Prós:** melhor qualidade esperada em tarefa nuançada (ironia, contexto político);
cobre bem categorias raras (Religião = 46 casos no gabarito, impossível de
aprender por classificador); custo irrisório no escopo do E1.
**Contras:** reprodutibilidade exige disciplina — mitigada por: modelo pinado
(`claude-haiku-4-5-20251001`), prompt versionado, `temperature=0`, requests e
respostas brutas salvas em `data/repl/vacinas2022/`, e os **rótulos congelados
no snapshot** (quem replicar a dissertação usa os rótulos publicados; re-rodar o
LLM é verificação extra, não requisito). Mesma discussão do EIXO_TOPICOS do Heine.

## 3. Opção B — Classificador supervisionado

**Como:** embeddings multilíngues (`paraphrase-multilingual-MiniLM-L12-v2`, o
mesmo do caso Heine) + regressão logística por rótulo, treinado nos 1.525.

**Prós:** custo zero, 100% offline, reprodutível por seed.
**Contras:** 1.525 exemplos para 12 rótulos é pouco; as categorias raras
(Religião 46, Internacional ~200) não têm massa de treino — recall baixo
esperado; o κ de stance talvez passe, o das categorias provavelmente não.
Risco real de reprovar no critério de aceite e voltar pra opção A.

## 4. Opção C — Híbrida (A + B como robustez)

LLM rotula (opção A); o classificador é treinado **nos rótulos do LLM + gabarito**
e reportado como análise de robustez (as conclusões da Fase 3 se sustentam com os
dois rotuladores?). Custo = opção A + tempo de implementação do B. É o desenho
mais defensável na banca, mas só vale se o cronograma permitir.

## 5. Recomendação

**Opção A** (Haiku 4.5 + batch + validação cega por κ), com a opção C como
extensão se sobrar tempo. Justificativa: o gargalo científico do eixo é o
**κ contra o gabarito humano** — é ele que legitima qualquer rotulador; dado o
custo (~US$ 20 no escopo todo do E1), a qualidade esperada do LLM domina.
A inadequação da opção B pelas categorias raras é, aliás, um dado que reforça a
tese (análises compostas exigem mais dados do que parece — eco do achado do Heine
sobre a fórmula de amostragem).

## 6. Pendências antes de rodar

1. **Decisão da Mariana** entre A / B / C.
2. Extrair o codebook (definições exatas das 11 categorias + subcategorias) das
   abas `Table broad/subcategories` para dentro do prompt — com citação do paper.
3. Chave da API Anthropic disponível (opções A/C) — custo estimado ≈ US$ 20.
4. Pré-registrar no plano: split dev/teste do gabarito ANTES de qualquer ajuste
   de prompt (evitar overfitting ao teste).

## 7. Estado atual (27/jul/2026 — EIXO B CONCLUÍDO)

**Decisão da Mariana: opção A**, com teto rígido de US$ 25.
**Gasto final: US$ 15,42 de 25.**

### Resultado

Duas versões do rotulador foram levadas até o fim, de propósito:

| | esquema | κ contra referência | uso |
|---|---|---:|---|
| `p4` | binário forçado (o do artigo) | **0,759** vs gabarito (teste cego, n=1.018) | reproduz o artigo |
| `p6` | três classes, com `nenhum` | **0,697** vs codificação humana (n=50) | comparação entre estratos |

Teto da tarefa medido: **0,746** (concordância intra-codificador, n=30). O
critério pré-registrado de 0,70 coincide praticamente com esse teto — a `p6`
reprovou por 0,003 num patamar que a própria tarefa mal comporta.

### Os quatro achados

1. **A conclusão comparativa é robusta ao esquema de anotação.** A fatia
   pró-vacina entre os decididos sobe ao descer o limiar nos dois esquemas
   (+14,2 pontos no binário, +11,7 nas três classes).
2. **A descrição do corpus não é.** Em >10 RT o esquema do artigo lê 58,8% pró
   × 35,1% anti; o de três classes lê 41,1% × 25,5% × **33,4% sem posição**.
   Mesmo corpus, mesmo modelo — ~18 pontos de diferença vindos de uma escolha
   que normalmente não é reportada.
3. **A viralidade seleciona conteúdo que toma partido:** a fatia neutra cai de
   33,4% (>10 RT) para 24,6% (>500 RT). Só visível sob esquema com classe neutra.
4. **As 14 categorias temáticas convergem** entre estratos (maior deslocamento:
   −8,4 pontos). Análises de composição temática aguentam o estrato viral;
   afirmações sobre equilíbrio de forças, não.

### Limitações declaradas

- `Advantages of vaccines` (κ 0,376) e `Misinformation sources` (0,518)
  resistiram a todas as versões de prompt — causa provável no codebook do
  artigo, que classifica "desmentir desinformação sobre riscos" como *Advantages*.
- O esquema do artigo não previa classe para o tweet on-topic sem posição (a
  terceira classe marcava irrelevância tópica: memes, vacinação veterinária).
  Ver `CALIBRAGEM_criterio.md`.
- Confiabilidade da anotação: nem o artigo (2 codificadores + árbitro) nem esta
  replicação dispõem de κ inter-codificador. O teto de 0,746 é intra-codificador
  medido no mesmo dia, portanto otimista.
- Contagens de RT vêm da re-coleta de mai/2022, posteriores às do artigo.

### Mapa dos artefatos

| Documento | O quê |
|---|---|
| `DECISOES_ROTULADOR.md` | diário de decisões D0–D9, com retratações |
| `CODEBOOK.md` | as 14 categorias e 121 subcategorias |
| `PRE_REGISTRO_split.md` | split do gabarito, critério e aposta |
| `PRE_REGISTRO_split_humano.md` | split da rotulagem humana, com contaminação declarada |
| `CALIBRAGEM_criterio.md` | por que os dois esquemas divergem |
| `RETESTE_intracodificador.md` | o teto da tarefa |
| `FASE3_curvas.md` | as curvas por limiar, nos dois esquemas |

Rotulagem humana produzida pela Mariana nesta rodada: **160 tweets**
(100 estrato baixo + 30 viral cego + 30 reteste).
