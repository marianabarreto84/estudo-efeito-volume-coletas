# Caso de replicação · Twitter/X · Verjovsky et al. (2023) — Vacinas 2021–2022

> Caso da dissertação da Mariana espelhado no fluxo dos casos Twitter/Ituassu e
> Heine. Alvo: **"Political quarrel overshadows vaccination advocacy"**
> (Verjovsky, **Porto Barreto**, Carmo, Coutinho, Thomer, **Lifschitz**, Jurberg;
> **_Vaccine_/Elsevier, 2023**, revisado por pares — preprint SSRN 4370287) — debate
> vacinal no Twitter brasileiro, **9/dez/2021–9/fev/2022**
> (consulta pública + início da vacinação infantil contra COVID-19). Análises:
> **rede/modularidade** (eixo A) + **análise de conteúdo/framing** (eixo B).
> Detalhe do alvo em [ARTIGO_VACINAS_alvo.md](ARTIGO_VACINAS_alvo.md).

**Valor deste caso no lineup.** Três coisas que os outros dois casos não têm:
(i) acrescenta **dois tipos de análise novos** — comunidades em rede e análise de
conteúdo manual (Bardin) — elevando a cobertura do lineup para 6 tipos sobre a mesma
rede; (ii) é a instância mais literal da tese da survey: a coleta foi larga (1 M
tweets), mas a **análise substantiva foi filtrada por critério** (só virais, >500 RTs)
— o caso mede o que o limiar esconde; (iii) fecha a linhagem no grau máximo: **a
Mariana é coautora e extraiu os dados** — a lente "coletar mais" aplicada ao próprio
trabalho, autocrítica pré-registrada em vez de crítica externa.

---

## 0. O que muda em relação aos casos irmãos

| Dimensão | Ituassu (compos2014) | Heine (heine2022) | **Vacinas (vacinas2022)** |
|---|---|---|---|
| Alvo | 2 papers (2015/2018) | 1 dissertação (2025) | 1 preprint (2023, SSRN) |
| Dados | Twitter 2014 | Twitter 2022 (eleições) | **Twitter dez/2021–mar/2022 (vacinas)** |
| Recorte de coleta | 1 hashtag-âncora | query ampla por candidato | **6 termos-índice + atividade de RT** |
| Análises replicadas | mídia + stance | tópicos + quantitativa | **modularidade (rede) + conteúdo/framing** |
| O gargalo da análise | rotulagem de stance | nomeação de tópicos | **rotulagem de conteúdo (Bardin, manual)** |
| Sub-coleta problematizada | volume+escopo da coleta | tamanho da amostra | **limiar de viralidade (>500 RT) na análise** |
| Rótulos originais disponíveis? | não | n/a | **sim (planilha suplementar)** — verificar acesso |

**Consequência de desenho:** aqui a "amostra sub-coletada" não é a coleta (que foi
larga), e sim o **estrato analisado**. O eixo-título é descer o limiar de viralidade
e medir se o framing (AV5/AV6) é propriedade do debate ou da elite viral. E, ao
contrário do stance do caso Ituassu (travado por falta de gabarito), aqui a rotulagem
automatizada tem **gabarito publicado** para validação.

---

## 1. Afirmações testáveis (a camada substantiva)

Do **eixo A — rede/modularidade**:

- **AV1 — pró ≈ anti ≈ 2/5 cada; juntos 78% dos posts** (Tabela 1).
- **AV2 — entre os virais, top pró recebeu 2× mais RTs que top anti** (Tabela 2).
- **AV3 — 602 influentes: 58,6% pró × 40,9% anti** (Tabela 3).
- **AV4 — concentração: top-10 autores = 15,7% dos RTs; 9 dos 10 mais retuitados são anti.**

Do **eixo B — conteúdo/framing** (Tabela 5, 11 categorias):

- **AV5 — ranking de categorias liderado pela agenda anti-vax:** Política > Crianças >
  Políticas restritivas > Desvantagens > Pessoas anti-vacina > … > Religião.
- **AV6 (conclusão-título) — os anti-vax impuseram o enquadramento**; o grupo pró
  reagiu (criticou anti-vax/políticas) em vez de promover a vacinação.

---

## 2. A ressalva metodológica honesta

Como nos casos irmãos, o que está no eTC hoje não é necessariamente o dataset
congelado do artigo:

- A coleta eTC é **contínua** — a tabela pode conter mais período/termos do que a
  janela do paper. Reproduzir a janela exata (9/dez–9/fev + update 8/mar) é o
  primeiro sanity check (o volume bate ~1 M tweets / ~4 M RTs?).
- As **contagens de RT mudam com o tempo** (o artigo fez coleta de atualização em
  8/mar/2022): o conjunto ">500 RT" pode não ser idêntico ao deles. Reportar o delta.
- Se houver divergência, separar **efeito-de-volume** (descer o limiar no mesmo
  universo) de **efeito-de-escopo** (universo diferente do deles), como no caso
  Ituassu.

A Fase 0 (`diagnostico/`) resolve isso empiricamente — com um atalho que os outros
casos não tinham: **perguntar à Mariana**, que extraiu os dados originais e pode
apontar tabela/queries de época.

---

## 3. Os eixos de expansão (separáveis)

| Eixo | Restrição (artigo) | Expansão | Isola a pergunta |
|---|---|---|---|
| **E1 · Limiar de viralidade** (o eixo-título) | conteúdo analisado só em >500 RT | limiares decrescentes: 500 → 250 → 100 → 50 → 10 → corpus todo | "o framing anti-vax é do debate ou da elite viral?" |
| **E2 · Extensão temporal** | 9/dez/2021–9/fev/2022 | antes (anúncio da consulta) e depois (mar/2022+), se a coleta contínua cobrir | "a janela da consulta pública representa o debate vacinal?" |
| **E3 · Escopo de termos** | 6 termos-índice | termos ausentes: imunizante, imunização, CoronaVac, Pfizer, "passaporte sanitário/da vacina" | "o recorte lexical muda a composição pró×anti?" |
| **E1' · Volume (rede)** | — (modularidade rodou no todo) | frações crescentes de N | "a estrutura de 2 comunidades e o 78% convergem cedo?" |

**Pré-requisito do E1:** análise de conteúdo manual não escala para limiares baixos.
O desbloqueio é um **rotulador automatizado** (pró/anti + 11 categorias; classificador
supervisionado ou LLM documentado) **validado contra os rótulos originais** da planilha
suplementar (acurácia/κ reportados antes de qualquer uso substantivo). Só depois de
validado ele desce o limiar.

**Contraste-chave do caso:** a hipótese é que as **estatísticas agregadas (AV1, AV4)
convergem cedo** e são robustas ao limiar, mas o **framing (AV5/AV6) é sensível ao
estrato**: a elite viral superrepresenta a campanha anti-vax articulada (políticos,
religiosos, jornalistas), enquanto abaixo do limiar a maioria pró "desarticulada"
pode recompor o ranking. Mesmo objeto ("coletar/analisar mais"), respostas opostas
por **tipo de análise** — exatamente a tese da dissertação.

---

## 4. Pipeline por fase

### Fase 0 — Localizar e caracterizar a coleta vacinas no eTC (sanity check)
`diagnostico/lista_tabelas.py` procura a coleta no eTC_Producao (vm067; se nada,
varrer as outras VMs como na Fase 0 do Heine); `explora_vacinas.py` caracteriza a
candidata: schema, range de datas, contagem por dia na janela do paper, distribuição
de RTs. **Checar:** a janela 9/dez–9/fev tem ~1 M tweets e ~4 M RTs? Quantos tweets
têm >500 RT (ordem de grandeza compatível com 602 autores influentes)? **Atalho:**
confirmar com a Mariana o nome da tabela/coleção usada em 2022.

### Fase 1 — Snapshot congelado
`pipeline/extrai_snapshot_vacinas.py` extrai para SQLite local:
- **snapshot_vacinas.sqlite** — tweets da janela do paper com texto, autor, timestamp
  e contagens de engajamento (1 M linhas cabe em SQLite local);
- **grafo de RTs** (arestas retuitador→autor) — para reproduzir a modularidade;
- agregações por dia/limiar via SQL no servidor quando o bruto não compensar trazer.

### Fase 2 — Replicar o ponto original
- **Eixo A:** modularidade (python-louvain/igraph sobre o grafo de RTs; Gephi só p/
  conferência visual) → reproduz 2 comunidades, ≈2/5 + ≈2/5 = 78% (AV1), Tabelas 2–4.
- **Eixo B:** validar o rotulador automatizado contra a planilha suplementar no
  estrato >500 RT; reproduzir a Tabela 5 (AV5) com rótulos automáticos ANTES de
  expandir — se não reproduzir, parar e reportar.

### Fase 3 — Expansão e divergência (métricas)

| Análise | Métrica | Afirmação que pode inverter/confirmar |
|---|---|---|
| **Rede** | proporção pró/anti e % coberto pelas 2 comunidades × fração de N; estabilidade (NMI entre partições) | AV1 converge a que fração? |
| **Concentração** | curva de Lorenz/top-k dos RTs por limiar | AV4 é estrutural (long-tail) ou artefato do corte? |
| **Framing** | ranking das 11 categorias por limiar (RBO entre rankings; JS entre distribuições); composição pró×anti por categoria | AV5/AV6 sobrevivem a limiar 100? 10? corpus todo? |
| **Temporal/lexical** | AV1/AV5 recomputados por janela (E2) e por termo (E3) | a conclusão é da janela/recorte ou do fenômeno? |

### Fase 4 — Tabela mestre + recomendação
Linha do caso: *o limiar bastava? × a conclusão mudou? × limiar/fração mínima que
estabiliza cada conclusão* — com o contraste **agregados (robustos) × framing
(sensível ao estrato)** como resultado candidato a título, e a nota reflexiva (o caso
é autocrítica de trabalho da própria autora) como fecho.

---

## 4.1 Auditoria plano × execução (07/ago/2026)

> Levantamento do que o plano acima promete e o que de fato existe em
> `data/repl/vacinas2022/`. **Nada aqui está travado em terceiros nem precisa de VPN**,
> exceto o último item. Registrado para não se perder entre as fases já concluídas.

| Item do plano | Estado | Custo |
|---|---|---|
| **AV1** (§1) | ✅ medido — cobertura inconclusiva, equilíbrio **não replica** ([FASE2 §AV1](data/repl/vacinas2022/FASE2_replicacao_ponto.md)) | feito |
| **AV2** — top pró recebeu 2× mais RTs que top anti | ✅ **medido em 07/ago/2026** ([FASE3 eixo A §1d](data/repl/vacinas2022/FASE3_eixoA_expansao.md)). A leitura que o artigo quis é a do **topo-1** (2,33× ≈ "2×"); a agregada dá 1,50 × 1,68 dele. **Não muda** entre limiares — e não muda **por construção**, porque a cauda está em todo estrato | feito |
| **AV3** — 602 influentes: 58,6% pró × 40,9% anti | ✅ **medido em 07/ago/2026** ([FASE3 eixo A](data/repl/vacinas2022/FASE3_eixoA_expansao.md)). Replica no ponto original a **0,3 p.p.** (58,9% × 41,1%) — o que **valida a atribuição de lado por topologia** usada no AV1 — e **muda ao expandir**: razão pró/anti de 1,43 (>500 RT) a 2,34 (>25 RT) | feito |
| **AV4** | ✅ replica exato no denominador do paper | feito |
| **AV5 / AV6** | ✅ Fase 3 (categorias convergem; stance inverte) | feito |
| **E2 — recomputar por janela** (Fase 3) | ✅ **respondido em 07/ago/2026, e negativamente**: o snapshot já tem exatamente a janela do artigo (`2021-12-08T23:00` a `2022-02-08T22:59`). Não há material da coleta de 8/mar/2022 aqui. A diferença de tamanho é de **convenção de contagem**, não de janela | feito |
| **E3 — recomputar por termo** (Fase 3) | ✅ **feito em 07/ago/2026** ([FASE3 §5](data/repl/vacinas2022/FASE3_curvas.md)). O balanço pró/anti **não inverte em nenhum** dos 6 termos (razão 1,41–7,42); a composição temática **muda muito**. Dois achados: os termos "anti-*" capturam **gente pró falando sobre anti-vaxxers** (75,5% pró em `anti-vax`), e `anti-vacinação` traz **7 tweets** em 29.978 — um dos seis termos é inerte | feito |
| **Curva `A(volume)` da rede** (Fase 3) | ✅ **feita em 07/ago/2026** ([FASE3 eixo A §1c](data/repl/vacinas2022/FASE3_eixoA_expansao.md), 29 min). Resposta: **AV1 estabiliza em f ≈ 0,75** — primeira célula preenchida da coluna *fração mínima* da tabela mestre. E a curva **corrigiu a leitura de AV1b**: a distância para o artigo não é de volume (com 1% dos dados a razão já é 1,31 × 1,02 dele) | feito |
| **Curva de Lorenz / top-k por limiar** (AV4, Fase 3) | ✅ **feita em 07/ago/2026** ([FASE3 eixo A §1b](data/repl/vacinas2022/FASE3_eixoA_expansao.md)). O ponto publicado replica (15,3% × 15,7%) e o valor cai monotonicamente até 9,7%: **15,7% é propriedade do corte**. A conclusão substantiva sobrevive em todos os cortes | feito |
| **Validar o rotulador fora do estrato viral** | ⏳ **travado em rotulagem humana**. ⚠ O teste tem de seguir a **convenção do artigo** (binária forçada; terceira classe só para irrelevância tópica) — a rodada de n=100 mediu divergência entre dois critérios humanos, não transferência entre estratos (ver [CALIBRAGEM_criterio.md](data/repl/vacinas2022/CALIBRAGEM_criterio.md)) | ~100–200 tweets |
| **RTs 12% acima do paper na janela idêntica** | ❌ resíduo da re-coleta **sem explicação** | baixo |

**Estado em 07/ago/2026:** ~~AV3~~ ~~curvas (rede + Lorenz)~~ ~~AV2~~ ~~E3~~ — todos
feitos. **Resta apenas a validação humana no estrato baixo**, sob a convenção do
artigo (ver linha correspondente). Saldo de LLM intacto: US$ 9,58 de US$ 25.

---

## 5. Onde apostar (predições pré-registradas — antes de rodar)

- **Provável CONFIRMA (não muda):** AV1 e AV4 — proporção agregada das comunidades e
  concentração long-tail são estatísticas de baixa dimensão; devem ser estáveis cedo.
  (Humildade: no caso Ituassu uma aposta "robusta" caiu — registrar e reportar.)
- **Provável MUDA (a aposta interessante):** AV5 — o ranking de categorias abaixo do
  limiar deve se recompor (Vantagens/Crianças subindo entre os pró desarticulados),
  enfraquecendo a generalização de AV6 de "elite viral" para "o debate".
- **Incerto / mais informativo:** *em que limiar exato* o framing vira — é o número
  que transforma a crítica ("filtragem por critério") em recomendação operacional
  ("abaixo de X RTs a conclusão inverte / acima converge").

---

## 6. Decisões pendentes (específicas deste caso)

1. **Fase 0:** nome exato da tabela/coleção da coleta vacinas no eTC (perguntar à
   Mariana; senão, varredura como no Heine). Confirmar se a coleta contínua cobre a
   janela e se as contagens de RT são de época ou atuais.
2. **Planilha suplementar:** confirmar acesso ao Google Sheets do Apêndice A (link no
   PDF) e se contém os rótulos por tweet (gabarito do rotulador). Sem ela, o eixo B
   exige re-rotulagem manual de um estrato de validação.
3. **Rotulador:** classificador supervisionado × LLM documentado (custo/reprodutibilidade
   — mesma discussão do EIXO_TOPICOS do Heine). Critério de aceite: κ contra o gabarito
   no estrato >500 RT antes de descer o limiar.
4. **Modularidade reprodutível:** Louvain tem aleatoriedade — fixar seed, reportar
   estabilidade entre execuções (NMI), e conferir contra o Gephi 0.9.2 do artigo.
5. **Direitos/ética:** dados de Twitter de 2021–22 via eTC; snapshot local segue o
   padrão dos outros casos (IDs + campos mínimos, nunca versionado).

---

*Docs irmãos: [ARTIGO_VACINAS_alvo.md](ARTIGO_VACINAS_alvo.md) (alvo detalhado) ·
[README.md](README.md). Protocolo geral nos casos irmãos:
`../twitter-ituassu/REPLICACAO_CASO_COMPOS2014.md` e
`../heine-xande/REPLICACAO_CASO_HEINE.md`.*
