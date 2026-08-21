# vacinas — Caso Verjovsky et al. (2023) do lineup da dissertação

Replicação por expansão do artigo **"Political quarrel overshadows vaccination
advocacy"** (Verjovsky, Porto Barreto, Carmo, Coutinho, Thomer, Lifschitz, Jurberg;
**_Vaccine_/Elsevier, 2023**, revisado por pares — preprint SSRN 4370287) — debate
vacinal no Twitter brasileiro, dez/2021–mar/2022 — aplicando o
**mesmo fluxo** dos casos irmãos (`../twitter-ituassu`, `../heine-xande`).
**A Mariana é coautora do alvo e extraiu os dados originais.**

## Leia primeiro
- [REPLICACAO_CASO_VACINAS.md](REPLICACAO_CASO_VACINAS.md) — plano de fases (o mapa).
- [ARTIGO_VACINAS_alvo.md](ARTIGO_VACINAS_alvo.md) — o alvo detalhado (AV1–AV6).
- [political_quarrel.pdf](political_quarrel.pdf) — o preprint em si.

## Estrutura (espelha os casos irmãos)
```
vacinas/
├── political_quarrel.pdf        alvo (preprint SSRN 4370287)
├── REPLICACAO_CASO_VACINAS.md / ARTIGO_VACINAS_alvo.md
├── core/         db.py (Postgres via túnel SSH) · llm.py (cliente Anthropic)
│                 orcamento.py (TETO RÍGIDO de US$ 25 — leia o cabeçalho)
├── diagnostico/  lista_tabelas.py, explora_vacinas.py — Fase 0 (achar/caracterizar a coleta)
│                 checa_colunas_vazias_na_fonte.py — ✅ respondeu: vazias na FONTE
│                 (só leitura; usar vm="vm031", não conectar_auto)
├── pipeline/     extrai_snapshot_vacinas.py  (Fase 1: snapshot local)
│                 extrai_codebook.py          (eixo B: codebook ← suplemento)
│                 congela_split.py            (eixo B: split dev/teste pré-registrado)
│                 rotula_conteudo.py          (eixo B: rotulador LLM, com teto de gasto)
├── analise/      rede_modularidade.py        (eixo A)
│                 valida_rotulador.py         (κ contra o gabarito)
│                 curvas_por_limiar.py        (Fase 3: "mudou? / convergiu?")
│                 amostra_validacao_humana.py + gera_guia_rotulagem.py
│                 valida_estrato_baixo.py     (κ humano × modelo no estrato baixo)
│                 atribui_lado_comunidades.py (AV1 formal: lado das 11.664 comunidades)
│                 av3_influentes_por_limiar.py (AV3: composição dos influentes por limiar)
│                 av4_lorenz_por_limiar.py    (AV4: Lorenz/Gini/top-k por limiar)
│                 curva_rede_por_fracao.py    (AV1: curva A(volume) da rede, ~29 min)
│                 av2_rts_por_lado.py         (AV2: RTs por lado, agregado e topo)
│                 e3_por_termo.py             (E3: conclusões por termo-índice)
├── data/repl/vacinas2022/   snapshots + FASE*/RESULTADOS_*.md (nunca versionar dados crus)
└── documentos/   cópias de apoio
```

## Pré-requisitos para rodar
1. **VPN Cloud-DI (PUC-Rio) conectada** — exige elevação/admin (OpenVPN adiciona
   rotas). Teste: `ping 10.50.0.68` responde.
2. **`.env`** na raiz com credenciais SSH/Postgres (mesmo formato dos casos irmãos;
   nunca versionar). O `core/db.py` reaproveita o `.env` de `../twitter-ituassu` ou
   `../heine-xande` se este aqui não existir.
3. `pip install -r requirements.txt` (conexão + eixo B).
4. **Eixo B (rotulador):** `ANTHROPIC_VACINAS_API_KEY=sk-ant-...` no `.env` da
   raiz de `dissertacao/` ou deste caso. **Teto de gasto de US$ 25** aplicado em
   `core/orcamento.py`; o livro-caixa vive em `data/repl/vacinas2022/gastos_llm.json`.
   Use `--dry-run` para estimar sem gastar.

## Estado atual
- ✅ Documentação da replicação (plano + alvo) — caso criado em jul/2026.
- ✅ Infra de conexão (`core/db.py`) + scripts de descoberta (`diagnostico/`).
- ✅ **Fase 0 concluída** — ver `data/repl/vacinas2022/FASE0_descoberta.md`. A coleta
  **está acessível**: vm031 / eTC_Producao, **busca id=178** (termos e janela idênticos
  ao paper; 6,55 M registros = 4,5 M RTs + 2,0 M originais — bate com ">1 M + 4 M").
  Re-coletada em mai/2022 → contagens de RT pós-paper (730 autores >500 RT vs 602).
- ✅ **Fase 1 concluída** — `snapshot_vacinas.sqlite` (1,78 GB; 2,05 M originais +
  4,5 M arestas de RT) extraído e validado. Ver `data/repl/vacinas2022/FASE1_snapshot.md`
  (inclui 2 ressalvas: grafo de RT é nível-autor; ~16% dos originais não são pt).
- ✅ **Planilha suplementar baixada** (`data/repl/vacinas2022/suplementar_rotulos.xlsx`):
  1.525 tweets virais rotulados (gabarito do eixo B), os 602 autores, as tabelas do
  paper e o mapa comunidade→pró/anti ("Grupo eTC"). Ver `SUPLEMENTAR_gabarito.md`.
- ✅ **Fase 2 / eixo A concluída** — ver `data/repl/vacinas2022/FASE2_replicacao_ponto.md`.
  AV4 replica exato (15,7% no denominador do paper); anti = 1 comunidade coesa
  (244/244 batem com o gabarito), pró = fragmentado. *(O 60,6% × 78% de AV1 registrado
  nesta fase foi depois identificado como comparação mal pareada — ver o item de AV1
  abaixo.)*
- ✅ **Fase 2 / eixo B concluída.** Rotulador LLM (Haiku 4.5 pinado, teto rígido
  de US$ 25 — gasto final **US$ 15,42**). Codebook extraído do suplemento
  (**14** categorias, não 11) → split pré-registrado → 6 versões de prompt, cada
  uma com hipótese declarada antes de rodar → teste cego.
  **Duas versões mantidas de propósito:** `p4` reproduz o esquema binário do
  artigo (κ **0,759** contra o gabarito) e `p6` usa três classes com `nenhum`
  (κ **0,697** contra codificação humana, com teto da tarefa em **0,746**).
- ✅ **E1 rodado nos dois esquemas** — 29.978 tweets (>10 RT, `idioma='pt'`).
- ✅ **Fase 3 concluída** — ver [FASE3_curvas.md](data/repl/vacinas2022/FASE3_curvas.md):
  1. **conclusão comparativa robusta ao esquema**: a fatia pró-vacina entre os
     decididos sobe ao descer o limiar nos dois (+14,2 e +11,7 pontos);
  2. **descrição do corpus não é robusta**: em >10 RT o esquema do artigo lê
     58,8% pró × 35,1% anti, o de três classes lê 41,1% × 25,5% × **33,4% sem
     posição** — ~18 pontos vindos de uma escolha de anotação, não do dado;
  3. **a viralidade seleciona quem toma partido**: fatia neutra cai de 33,4%
     (>10 RT) para 24,6% (>500 RT);
  4. **as 14 categorias temáticas convergem** (maior deslocamento −8,4 pontos).
- ✅ **Fase 4 — as linhas deste caso entraram** na tabela mestre parcial
  ([`casos/RESULTADOS_tabela_mestre.md`](../RESULTADOS_tabela_mestre.md), 07/ago/2026):
  linhas 4 (AV1, comunidades), 5 (AV4, concentração), 6 (AV5, enquadramento —
  **convergiu**) e 7 (AV6/stance — **mudou e inverteu**). A tabela segue ⏳ incompleta
  enquanto o `heine-xande` aguarda os dados do SharePoint.
- ✅ **No texto da dissertação** — o caso virou capítulo próprio em
  `escrita/dissertacao/corpo.tex` (`\label{cap:caso-vacinas}`), 07/ago/2026.
- ✅ **AV1 medido (07/ago/2026)** por `analise/atribui_lado_comunidades.py`, que atribui
  lado às **11.664 comunidades** pela regra do paper (sementes = os 599 autores com lado
  publicado), em 8 cenários. O gap 60,6% × 78% era **comparação mal pareada** — o
  "pró"/"anti" do paper é a união dos 7 grupos de modularidade, não 2 comunidades.
  Resultado: **a cobertura é inconclusiva** (76,7%–90,6% conforme a base de contagem) e
  **o equilíbrio entre os polos não replica** — razão pró/anti **1,50–1,56** contra
  **1,02** do paper, estável nos 8 cenários. Números em `av1_lados.json`; ver
  [FASE2_replicacao_ponto.md](data/repl/vacinas2022/FASE2_replicacao_ponto.md) §AV1.
- ✅ **E2 (janela) respondido negativamente:** o snapshot tem exatamente a janela do
  artigo; o corpus maior é convenção de contagem, não janela.
- ✅ **AV3 medido (07/ago/2026)** por `analise/av3_influentes_por_limiar.py` — ver
  [FASE3_eixoA_expansao.md](data/repl/vacinas2022/FASE3_eixoA_expansao.md). Replica o
  ponto do artigo a **0,3 p.p.** (58,9% × 41,1% contra 58,6% × 40,9%), o que **valida
  a atribuição de lado por topologia** do AV1, e **muda ao expandir**: razão pró/anti
  de **1,43** (>500 RT) a **2,34** (>25 RT), sem convergir na faixa observada.
- ✅ **Curvas da Fase 3 / eixo A (07/ago/2026)** — ver
  [FASE3_eixoA_expansao.md](data/repl/vacinas2022/FASE3_eixoA_expansao.md):
  **Lorenz do AV4** (`av4_lorenz_por_limiar.py`) — o ponto publicado replica
  (15,3% × 15,7%) e o valor cai a 9,7%: **15,7% é propriedade do corte**;
  **curva `A(volume)` da rede** (`curva_rede_por_fracao.py`) — **AV1 estabiliza só em
  f ≈ 0,75** da coleta, e a estrutura (NMI) nem isso. A curva também **corrigiu a
  causa** de AV1b: a distância para o artigo **não é de volume** (com 1% dos dados a
  razão já é 1,31, contra 1,02 dele), e sim de convenção de atribuição de lado.
- ✅ **Colunas vazias do snapshot explicadas (07/ago/2026)**, com a VPN de pé e
  contagem completa na vm031: as 10 colunas estão **vazias na fonte** para a busca
  178 — a extração foi fiel, não há bug. E o custo é menor do que se registrou:
  `texto` está 100% preenchido, então **hashtags/menções saem por regex** sobre o
  snapshot local (E3 desbloqueado, sem VPN). Ver
  [FASE1_snapshot.md](data/repl/vacinas2022/FASE1_snapshot.md) Achado 1.
- ✅ **AV2 e E3 fechados (07/ago/2026)** — com eles, a auditoria de plano × execução
  ([REPLICACAO_CASO_VACINAS.md §4.1](REPLICACAO_CASO_VACINAS.md)) fica **zerada**,
  exceto a validação humana no estrato baixo.
  **AV2** (`av2_rts_por_lado.py`): a leitura que o artigo quis é a do topo-1
  (2,33× ≈ "2×"); não muda entre limiares — e não muda **por construção**, porque a
  cauda está em todo estrato.
  **E3** (`e3_por_termo.py`): o balanço pró/anti **não inverte em nenhum** dos 6
  termos (razão 1,41–7,42), mas a composição temática **muda muito**. Os termos
  "anti-*" capturam **gente pró falando sobre anti-vaxxers** (75,5% pró em
  `anti-vax`), e `anti-vacinação` traz **7 tweets** em 29.978.
- ⏳ **Único item aberto do caso:** validar o rotulador no estrato baixo **sob a
  convenção do artigo** (binária forçada). Depende de rotulagem humana.

### Documentos do eixo B
- [EIXO_CONTEUDO.md](EIXO_CONTEUDO.md) §7 — estado, custos medidos, teto de gasto.
- [DECISOES_ROTULADOR.md](data/repl/vacinas2022/DECISOES_ROTULADOR.md) — **diário de
  decisões de método**: o que foi decidido, com que evidência, e o que foi rejeitado
  (inclui um *erratum* de um diagnóstico calculado errado). Nenhuma mudança de prompt
  sem uma linha lá.
- [PRE_REGISTRO_split.md](data/repl/vacinas2022/PRE_REGISTRO_split.md) e
  [PRE_REGISTRO_split_humano.md](data/repl/vacinas2022/PRE_REGISTRO_split_humano.md)
  — splits, critérios e apostas registrados **antes** de medir (o segundo declara
  a contaminação por leitura prévia).
- [CALIBRAGEM_criterio.md](data/repl/vacinas2022/CALIBRAGEM_criterio.md) — por que
  o esquema do artigo e o da codificação humana divergem (κ 0,350 entre eles).
- [RETESTE_intracodificador.md](data/repl/vacinas2022/RETESTE_intracodificador.md)
  — o teto da tarefa (κ 0,746), que nem o artigo original mediu.
- [CODEBOOK.md](data/repl/vacinas2022/CODEBOOK.md) — as 14 categorias e 121 subcategorias.
- [FASE3_curvas.md](data/repl/vacinas2022/FASE3_curvas.md) — as curvas por limiar e as
  5 limitações declaradas.
