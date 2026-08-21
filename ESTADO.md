# ESTADO — o que dá para avançar agora

> **Documento canônico de estado.** Responde a uma pergunta só: *sentando agora,
> o que dá para fazer sem depender de ninguém e sem esperar nada?*
> Última revisão: **18/ago/2026**.
>
> Regra: **toda sessão nesta pasta termina atualizando este arquivo** — ver
> [.claude/skills/docs-em-dia/SKILL.md](.claude/skills/docs-em-dia/SKILL.md).
> Ele não guarda números nem método (isso vive nos `FASE*/RESULTADOS_*` dos casos);
> guarda **o que está desbloqueado, o que está travado e em quê, e o que espera decisão**.

---

## 1. Desbloqueado agora (não depende de VPN, de banco, do SharePoint nem de terceiros)

Ordenado por urgência. Os snapshots de todos os casos executáveis já estão **congelados
em disco** — é o próprio desenho do protocolo (Fase 1 → análise offline).

| # | O que fazer | Onde | Por que agora |
|---|---|---|---|
| **3** | ✅ **Kit de rotulagem do stance — FEITO em 18/ago/2026.** O que resta é **da Mariana**: abrir `gold_stance_para_rotular.csv` no Excel e marcar `cidadao`/`stance`/`confianca`/`notas` em **320 linhas** (~3–4 h), seguindo o [CODEBOOK_stance.md](casos/twitter-ituassu/CODEBOOK_stance.md). Depois, `gold_stance_RETESTE.csv` (40 itens, ≥7 dias depois) | [STANCE_...md](casos/twitter-ituassu/STANCE_como_o_paper_fez_e_onde_estamos.md) §9 · [PRE_REGISTRO](casos/twitter-ituassu/data/repl/compos2014/stance/PRE_REGISTRO_stance.md) | Amostra congelada (seed `20260818`, sha `dc8ee39ff69b`), split 110 dev / 210 teste, apostas e critério de aceite (κ ≥ 0,70) registrados **antes** de medir. Saldo de LLM: **US$ 9,58** de US$ 25 — o universo da janela (32.193) cabe folgado |
| **4** | **Survey**: fechar as 2 decisões em aberto e reler o `.tex` | [escrita/survey/STATUS.md](escrita/survey/STATUS.md) §Decisões em aberto | Redação pura; nenhuma pendência de dado |
| **5** | 📌 **Revisar os capítulos novos no `corpo.tex`** — são **três**: caso **vacinas** (07/ago), caso **YouTube** (19/ago) e caso **TikTok/PoliTok** (19/ago), mais dois trechos novos da conclusão (o **quarto eixo** — volume, largura, forma e momento — e os **números que dependem de decisões não publicadas**) | [corpo.tex](escrita/dissertacao/corpo.tex) | Nenhum foi lido pela Mariana. **É trabalho dela.** Compila limpo em **45 páginas** (eram 34 em 07/ago). A afirmação mais forte a conferir é a de **circularidade** no cap. do YouTube |
| **6** | ✅ **`reddit-buntain` FECHADO em 19/ago/2026.** Coleta completa (**43.479 submissions + 1.015.247 comentários**, 13 subreddits, sem corte) e **RB3 medido**: o artigo diz que **~3%** dos usuários participam de >1 comunidade; no universo, **sob o mesmo limiar de atividade**, são **57,6%** — **19×**. A localidade dos papéis sociais que o artigo relata é **artefato do recorte top-100 × top-200** | [RESULTADOS_RB3](casos/reddit-buntain/data/repl/buntain2013/RESULTADOS_RB3.md) | É o maior efeito de sub-coleta medido até aqui na dissertação. Falta **escrever o capítulo** |
| **7** | ◐ **`reddit-massachs`: Fases 1a e 2 feitas; Fase 3 FORA DE ESCOPO.** O ponto original **replica** (ordenação homofilia ≈ feedback ≫ influência, pontas a <0,25 p.p.). ⛔ A Fase 3 não foi sequer **dimensionável**: o endpoint de agregação do Arctic Shift falha nos subreddits grandes (2 rodadas, a 2ª mês a mês, 34/34 incompletos). Caminho real seria dump por subreddit no Academic Torrents — download pesado, não cabe até 31/ago | [FASE2 §7](casos/reddit-massachs/data/repl/massachs2016/FASE2_ponto_original.md) | ⚠ a 1ª sonda **imprimiu um total falso** (somava só quem respondia); corrigido — o script agora se recusa a totalizar com falhas e grava `COMPLETO: false` |
| **8** | ✅ **`tab:casos` FECHADA em 18/ago/2026** — as três células que faltavam foram preenchidas: **YouTube** (#363 → **AGECovP**, agora *Modelagem de tópicos*), **TikTok** (#299 → **PoliTok-DE**, *Análise de conteúdo*) e **Instagram/Facebook** (**Capozzi 2021**, *Classificação*). A prosa que dizia "o caso de Instagram/Facebook ainda não tem artigo definido" foi corrigida. **Compila limpo em 35 páginas** | [corpo.tex](escrita/dissertacao/corpo.tex) §Conjunto de casos | Nada a fazer aqui |
| **9** | ✅ **Feito em 7/ago/2026** — full text do CHI 2021 lido e **CB2 desambiguado**. Nada a fazer aqui; o caso agora só espera a conta Meta (§2) | [DECISOES_CB2.md](casos/meta-ads-imigracao/data/repl/metaads2019/DECISOES_CB2.md) | Ver §4.14 |
| **10** | ⚠ **TikTok: a credencial do eTC está MORTA** — diagnosticado em 18/ago/2026. A Mariana importou a chave e o token deu `invalid_client`. **Não é erro nosso**: a chave do `.env` é a mesma dos dois deployments da vm031 (conferido por hash) e **funcionou em 19/jun/2025** (o log registra `Access token acquired` e uma coleta completa). A aprovação da Research API expirou/foi revogada desde então. **Nada a fazer no código** — ele está pronto e testado a seco | [casos/tiktok/README.md](casos/tiktok/README.md) §2b | Destrava com (a) **renovar a aprovação do eTC** (quem gerencia é o Tomaz, citado no `execute_tiktok.sh`) ou (b) **credencial própria** — o Brasil é região elegível, e credencial própria é o que torna a Fase 1 reproduzível por terceiros |
| **11** | 🆕 **Caso YouTube (AGECovP) — CRIADO e COLETANDO em 18/ago/2026.** É a **quarta rede** do lineup, e a única rede nova viável no prazo: chave de API em 5 min, sem verificação. **Fase 0 fechada** (artigo lido, funil e termos extraídos, alvos-teste e predições pré-registrados) e **gabarito dos autores baixado e conferido** (Zenodo: 3.782 vídeos, 2.243 canais, 69.425 comentários, 4.389 rotulados — todos batem). **Fase 1 rodando** | [casos/youtube-agecovp/README.md](casos/youtube-agecovp/README.md) · [FASE0](casos/youtube-agecovp/data/repl/agecovp2020/FASE0_descoberta.md) | O alvo aplica um filtro de regex que descarta **52% da busca** e **99% dos sugeridos** — filtragem por critério no estado puro. Coletamos sem filtrar e gravamos o filtro como **coluna**, então o mesmo snapshot serve aos dois lados |

> **Feito em 07/ago/2026:** (a) os números do eixo mídia no `corpo.tex` foram
> corrigidos para o canônico (§4.1); (b) o **capítulo do caso vacinas** foi escrito
> (`\label{cap:caso-vacinas}`); (c) a **tabela mestre parcial** nasceu em
> [casos/RESULTADOS_tabela_mestre.md](casos/RESULTADOS_tabela_mestre.md) — hoje com
> **10 linhas fechadas** e 7 em ⏳; (d) o **caso vacinas foi fechado**: AV1–AV6 e
> E1/E2/E3 todos medidos (§4.4 a §4.8), incluindo duas correções de leitura feitas
> dentro da própria sessão — a cobertura de AV1 passou de "replica" a **inconclusiva**
> (varia com a base) e a causa de AV1b passou de "efeito de volume" a **diferença de
> convenção**; (e) a VPN foi diagnosticada e destravada (§2). A dissertação compila
> limpo em **34 páginas** (eram 20). (f) A **última rede vaga do lineup foi preenchida**:
> nasceu o caso [`meta-ads-imigracao`](casos/meta-ads-imigracao/README.md) (Capozzi et al.,
> CHI 2021 + SocInfo 2020), com Fase 0 parcial e o **gabarito dos autores baixado e
> conferido** — ver §4.13.
>
> O relato completo do dia, sessão por sessão, está em
> [BALANCO_2026-08-07.md](BALANCO_2026-08-07.md) — histórico, não estado.

> **Feito em 18/ago/2026:** (a) o **kit de rotulagem do stance** do Ituassu ficou pronto
> e congelado (§1, item 3), e de passagem corrigiu um erro nosso sobre `#AecioNever`
> (§4.15); (b) a coleta do **Buntain foi retomada** (§1, item 6); (c) o **ponto original
> do Massachs foi replicado** — MH1 reproduz (§1, item 7); (d) descobriu-se o **coletor
> de TikTok do eTC** na vm031 e escreveu-se a infra de coleta local — que **não pôde coletar**: a credencial
> do eTC está morta (§1, item 10); (e) levantou-se o **alvo de TikTok** e não há candidato com tração
> ([ALVOS_candidatos.md](casos/tiktok/ALVOS_candidatos.md)); (f) **nasceu o caso YouTube** — a quarta
> rede do lineup, do zero à coleta rodando na mesma sessão (§1, item 11).
>
> ⚠ **Incidente da sessão:** um script de edição truncou este arquivo (abriu em modo `w`
> e falhou na codificação antes de escrever). Ele foi **reconstruído a partir do conteúdo
> em contexto** com todas as edições do dia reaplicadas. O conteúdo confere com a versão
> de 07/ago mais as mudanças de 18/ago, mas **se algo parecer faltando, é aqui que
> aconteceu**.

### O caso vacinas destravou o stance do Ituassu

Vale registrar porque não está escrito em lugar nenhum: o eixo stance está parado
esperando "rotulagem humana", mas o caso vacinas **executou e validou** exatamente esse
fluxo — codebook → split pré-registrado → rotulador LLM com teto rígido de gasto → κ
contra gabarito → aplicação em escala (29.978 tweets), inclusive medindo o **teto da
tarefa** por reteste intracodificador. A parte irredutivelmente humana do stance encolheu
de "ler 400–500 tweets" para "ler ~200–300 para servir de gabarito", e o resto é
transponível. Ver [DECISOES_ROTULADOR.md](casos/vacinas/data/repl/vacinas2022/DECISOES_ROTULADOR.md).

---

## 2. Travado — e o que exatamente destrava

| O quê | Travado em | Destrava com |
|---|---|---|
| ⏳ **heine-xande, Fases 1–4** | O Twitter 57,9 M do Heine **não existe em nada acessível** (varridos 3 VMs, 29 Postgres, 3 Mongo, filesystem, repo) | A Mariana baixar `1st_turn_day.csv` / `1st_turn_day_random_sample.csv` do **SharePoint do BioBD** (conta `mbarreto@inf.puc-rio.br`), **ou** decidir pivotar para o Instagram (`xande_search`, 628 k) / Reddit que estão acessíveis. Ver [FASE0_descoberta.md](casos/heine-xande/data/repl/heine2022/FASE0_descoberta.md) |
| ⏳ **Tabela mestre completa (Fase 4)** | Faltam as linhas do Heine (8, 9), do stance do Ituassu (10), do Reddit (11, 12) e do Meta Ads (13, 14); a coluna *fração mínima que estabiliza* tem **3 de 10** células (4b f≈0,75; linha 1 n=100; linha 2 n≈200) | Os dados do Heine + o gabarito do stance + a coleta do Buntain (§1, item 6) + a Fase 3 do Massachs (§1, item 7) + a conta Meta (§2). ✅ Já feitos: a curva `A(volume)` do Ituassu (linhas 1–3), os full texts do Massachs e do Capozzi (07/ago) e o **ponto original do Massachs** (18/ago). A [versão parcial](casos/RESULTADOS_tabela_mestre.md), com **10 linhas fechadas**, **já existe** desde 07/ago/2026 |
| ⏳ **Stance do Ituassu (Fases 0.5→3)** | Falta **só o ato de rotular** — o kit ficou pronto em 18/ago/2026 | **320 tweets** rotulados à mão pela Mariana (~3–4 h) na planilha já sorteada e congelada; tudo o mais (validação κ, aplicação em escala, curva) é automático — §1, item 3 |
| ✅ **VPN Cloud-DI** — *destravada em 07/ago/2026; reconectada em 18/ago* | — | ⚠ **Como testar se está mesmo conectada:** o `openvpn-gui` rodando **não** significa túnel de pé (o ícone na bandeja engana). O teste certo é o adaptador **`OpenVPN TAP-Windows6`** aparecer `Up` **e** existir IP/rota `10.x`. Conectada, fica `10.8.0.68` + rota `10.50.0.0/16` via `10.8.0.1`, e as portas 22 da vm031/vm067 abrem. Subir exige **elevação**: `Start-Process ... openvpn.exe -Verb RunAs` + `vpn-fixed.ovpn` (o UAC precisa de clique). Surfshark e Fortinet, também instalados, **não** dão acesso à Cloud-DI e não interferem. **Nas consultas, use `conectar(vm="vm031")` para a coleta vacinas** — `conectar_auto` cai na vm067 |
| ⏳ **meta-ads-imigracao, Fase 1** | Acesso à **Ad Library API** | 📌 **AÇÃO DA MARIANA — abrir a conta Meta verificada.** Adiada em 07/ago/2026 ("não consigo fazer isso agora"). **Passo a passo pronto**, levantado das páginas oficiais, em [FASE0 §5.1](casos/meta-ads-imigracao/data/repl/metaads2019/FASE0_descoberta.md) — 4 passos, só o 1º espera (documento oficial em `facebook.com/ID`, **1-3 dias úteis**). Grátis, sem App Review, sem tier pago. Destrava junto o **teste de retenção** ([§5.2](casos/meta-ads-imigracao/data/repl/metaads2019/FASE0_descoberta.md), comando pronto), que decide se o corpus italiano de 2019 ainda existe. ⚠ se a tela pedir **endereço postal**, avisar — muda o cronograma e promove o braço Brasil |
| ◐ **TikTok, Fase 1 (expansão)** | a credencial do eTC está morta — **mas a célula não depende mais disso**: a Fase 2 foi feita offline sobre o dataset publicado do PoliTok-DE | só o eixo "coletar mais" estrito segue travado; no lugar dele o caso entrega o **eixo temporal** (rechecagem em datas sucessivas), medido com o que está publicado. Ver [FASE2_politok.md](casos/tiktok/FASE2_politok.md) |
| ⏳ **Front-matter da dissertação** | Dados que só a Mariana tem | Data da defesa, banca, resumo/bio, dedicatória, epígrafe. Ver [escrita/dissertacao/README.md](escrita/dissertacao/README.md) §Pendências |

---

## 3. Decisões esperando a Mariana

Nenhuma delas bloqueia os itens do §1, mas todas mudam trabalho futuro.

1. ~~**O lineup é de 6 casos ou de 3?**~~ — **resolvido em 07/ago/2026 pela Mariana:**
   ela **segue trabalhando em mais casos**, logo o conjunto de 6 do `corpo.tex` é o
   **plano vigente** e os 3 do `CLAUDE.md` são apenas os **executados até aqui**. O que
   resta em aberto é mais estreito e não urgente: quais redes/artigos ocupam as linhas
   ainda vazias da Tab. `tab:casos`. ~~O caso de Instagram/Facebook segue sem artigo
   definido~~ — **resolvido em 07/ago/2026**: é o **Capozzi et al.** (CHI 2021 + SocInfo
   2020), caso [`meta-ads-imigracao`](casos/meta-ads-imigracao/README.md). Ver §4.2 e §4.13.
2. **Heine:** apontar o Twitter (SharePoint), pivotar para Instagram/Reddit, ou pedir os
   CSVs direto ao Heine.
3. **Stance:** ~~rotular à mão? quantos tweets~~ — **fixado em 18/ago/2026: 320 tweets**,
   com o kit pronto. **Resta:** quantas pessoas rotulam (1 dá só o teto intracodificador;
   2 dão o κ humano×humano) e quando.
4. **Ituassu:** ~~fechar a lista MP (convenção estrita × conceitual)~~ ✅ **resolvido
   por medição em 07/ago/2026** — não era decisão a tomar: a estrita é a certa (é o
   mínimo de MP) e a divergência não vem daí (§4.11). **Resta** decidir como
   reproduzir a cascata A→B→C→D. Ver
   [REPLICACAO_CASO_COMPOS2014.md](casos/twitter-ituassu/REPLICACAO_CASO_COMPOS2014.md) §7.
5. **Survey:** como reportar a fração inacessível do corpus; resgatar ou não a tipologia
   de Gao.
6. **Defesa:** os `% TODO` do front-matter.
7. ~~**Rótulo do caso Reddit**~~ — **superado em 07/ago/2026:** o #207 foi **descartado**
   (preprint sem tração) e substituído por **Buntain 2014** (SNA de verdade) + **Massachs
   2020** (homofilia). Toda a discussão de "reetiquetar a centralidade via comentários"
   virou pó — o slot de centralidade da `tab:casos` agora é preenchido por um paper que
   **de fato faz SNA**. Ver §4.12. Resta a edição da `tab:casos` (§1, item 8).
8. **TikTok — o alvo.** A coleta está resolvida (§1, item 10), mas a célula não tem
   artigo. **Levantamento feito em 18/ago/2026** ([ALVOS_candidatos.md](casos/tiktok/ALVOS_candidatos.md)):
   varridos os 55 artigos de TikTok do `research.db` + busca fora do corpus. **Achado
   estrutural:** os muito citados (300–530 cit.) são estudos culturais/discurso, sem
   afirmação computacional mensurável; os computacionais com sub-coleta declarada têm
   **2–12 citações**. Tração no padrão do Buntain (133) **não existe** para TikTok.
   **Recomendação: trocar o #299 (arXiv, 2 cit.) pelo #14** — *AI vs. Human Paintings*
   (Int. J. Human-Computer Interaction, revisado, 7–12 cit.), cujo alvo-teste é contável
   ("7 razões por modelagem de tópicos") e cujo funil declarado (**4.396 → 1.713 → 417**
   vídeos, filtro de **≥10.000 views**) é o mesmo estrato viral do caso vacinas.
   ⚠ o #299 perde o **gabarito público** (43.040 IDs) e o mesmo instrumento de coleta.
9. **TikTok — a cota.** A credencial é do **app do eTC**, cuja cota é compartilhada com o
   crawler que roda em loop na vm031. Combinar com quem opera (o `execute_tiktok.sh` cita
   o Tomaz) ou pedir credencial própria — esta última é o que torna a Fase 1
   **reproduzível por terceiros**.

---

## 4. Divergências detectadas entre documentos

Registradas aqui até serem corrigidas. **Os dados vencem** (princípio §7 do `CLAUDE.md`).

### 4.1 ✅ Números do eixo mídia — **corrigido em 07/ago/2026**

O eixo MV/MH foi refeito e corrigido em jul/2026 (os scripts liam só o campo `links` e
contavam como NDA tweets que tinham `t.co` só no texto), e o `corpo.tex` ficou citando
os valores antigos. **Os seis valores foram alinhados ao canônico**
([RESULTADOS_analise_midia_MV_MH.md](casos/twitter-ituassu/RESULTADOS_analise_midia_MV_MH.md)
§0, §1, §3): a proporção MV/MH e seu IC/n/z; o NDA do escopo amplo (53,9% → **47,1%**);
o par intra-autor (31,6→68,0% → **25,9→53,3%**); a razão de chances (4,47 → **2,91**,
que era superestimada em ~35%); e o Wilcoxon (10⁻²⁵ → **3,0×10⁻¹⁸**). Um sétimo valor,
não listado na versão anterior deste documento, também dependia do NDA e foi corrigido:
"NDA, um terço do universo e mais de 40% nos dias da votação" → **30,8% da janela,
chegando a 48,8% em 24/out**.

Conferidos e **corretos**, não foram mexidos: H1 (48,3% → 36,1%, ICs disjuntos), ΔMV do
escopo (43,3% → 24,9%), 32.193 / 140.909.

### 4.2 ✅ O lineup: 6 casos multiplataforma × 3 casos, todos Twitter — **resolvido**

> **Resolução (07/ago/2026, pela Mariana):** *"eu ainda quero fazer mais casos, estou
> trabalhando nisso"*. Os dois documentos **não** eram contraditórios, e sim de níveis
> diferentes: o `corpo.tex` descreve o **plano** (6 casos, um por rede) e o `CLAUDE.md`
> descreve o **executado** (3 casos, todos Twitter, porque são os que têm acervo
> disponível hoje). Nada a reescrever na Tab. `tab:casos`; a acomodação feita no
> `corpo.tex` (parágrafo do 2º caso em Twitter) está correta como está.
>
> ~~Fica só o resíduo, que **não é divergência**: a linha de Instagram/Facebook segue sem
> artigo definido, e o texto já a marca como tal.~~ — **resíduo fechado em 07/ago/2026**
> (§4.13): a linha tem alvo, e o `.tex` precisa ser editado (§1, item 8).

O registro original, mantido para histórico:

- [escrita/dissertacao/corpo.tex](escrita/dissertacao/corpo.tex) §*Conjunto de casos*
  (Tab. `tab:casos`) descreve **seis** casos, um por rede: Reddit ×2, YouTube, TikTok,
  Instagram/Facebook e Twitter como exceção — e afirma que **um** foi executado.
- [CLAUDE.md](CLAUDE.md) §3 descreve **três** casos, **todos Twitter**, com uma
  justificativa própria e explícita ("por que todos são Twitter e complementares":
  6 tipos de análise sobre a mesma rede).

Ao entrar o capítulo do caso vacinas, o texto passou a descrever **dois** casos
executados, ambos em Twitter, dentro de um conjunto que a `tab:casos` apresenta como
**seis casos, um por rede**. A `tab:casos` **não foi tocada**: o caso vacinas entra por
um parágrafo em §*Conjunto de casos* que o justifica pela mesma exceção do Twitter
(acervo eTC) e explicita que ele acrescenta **tipos de análise**, não uma rede.

### 4.3 ✅ O caso vacinas no texto — **escrito em 07/ago/2026**

O capítulo existe (`\label{cap:caso-vacinas}` no `corpo.tex`), cobre os eixos A e B e as
pendências declaradas, e a referência ao alvo entrou no `referencias.bib`
(`verjovsky2023quarrel`). ⚠ **Ainda não foi lido pela Mariana** — ver §1, item 5.

### 4.4 ✅ AV1 do caso vacinas: 60,6% × 78% — **resolvido e medido em 07/ago/2026**

O gap não era de denominador (esse sempre foi o mesmo: todos os posts do período).
Era **numerador**: o "pró"/"anti" do artigo é a **união dos grupos de modularidade
mapeados a cada lado** — são **7 grupos**, não 2 — e a réplica comparava com as **duas
maiores comunidades isoladas**.

Medido com atribuição formal de lado às **11.664 comunidades**
(`analise/atribui_lado_comunidades.py`, sementes = os 599 autores com lado publicado),
em **8 cenários** (2 bases de contagem × 4 exigências mínimas de sementes):

| parte de AV1 | resultado | veredito |
|---|---|---|
| "juntos, 78% dos posts" | cobertura varia **76,7%–90,6%** conforme a base | ◐ **inconclusivo** |
| "volumes semelhantes, ~2/5 cada" | razão pró/anti **1,50–1,56** × **1,02** do paper | ✘ **não replica** |

⚠ **Correção dentro da própria sessão:** a primeira rodada usou só a base ampla, deu
cobertura 78,4% × 77,7% e foi registrada como "a cobertura replica". A segunda base
derrubou — os 0,7 p.p. eram coincidência de diferenças que se cancelam. O que é
robusto é a **razão**, não a cobertura. Detalhe e ressalvas no
[FASE2 §AV1](casos/vacinas/data/repl/vacinas2022/FASE2_replicacao_ponto.md).

O desequilíbrio converge, por caminhos independentes, com o achado do eixo B: ao sair
do estrato viral, a fatia pró cresce. Confirmado depois pelo **AV3** (§4.6).

### 4.6 ✅ AV3 do caso vacinas — **medido em 07/ago/2026**, e valida o AV1

Composição pró × anti dos autores influentes, por limiar, com lado atribuído **por
topologia** (`analise/av3_influentes_por_limiar.py`). Dois resultados:

1. **Replica o ponto publicado a 0,3 p.p.** — 58,9% × 41,1% contra 58,6% × 40,9% do
   artigo. Como o artigo rotulou esses autores **lendo o conteúdo** e a réplica os
   rotula **pela comunidade de retuítes**, isso **valida a regra de atribuição de
   lado** — que era a peça mais frágil do AV1.
2. **Muda ao expandir** — a razão pró/anti vai de **1,43** (>500 RT) a **2,34**
   (>25 RT), sem convergir na faixa observada.

Detalhe e ressalvas em
[FASE3_eixoA_expansao.md](casos/vacinas/data/repl/vacinas2022/FASE3_eixoA_expansao.md).

### 4.7 ⚠ AV1b: o veredito fica, a **causa** muda (curva `A(volume)`, 07/ago/2026)

A curva da rede por fração de N mostrou que **em nenhuma fração** da coleta a razão
pró/anti se aproxima do 1,02 do artigo — com **1% dos dados** a réplica já mede
**1,31**. Logo a distância para o artigo **não é efeito de volume**: se fosse,
coletar menos aproximaria. É diferença de **convenção de atribuição de lado** (o
artigo deixa 22,3% dos posts sem lado; a réplica, sob a convenção dele, 9,4%).

Isso **corrige** a leitura registrada mais cedo hoje, que apresentava o "+54,9% no
pró × +1,5% no anti" como se fosse explicação de sub-coleta. Corrigido no
`FASE2 §AV1`, na tabela mestre e no `corpo.tex`.

**O que a curva entregou de positivo:** a resposta a "AV1 converge a que fração?" —
**f ≈ 0,75**. É a **primeira célula preenchida** da coluna *fração mínima que
estabiliza* da tabela mestre.

### 4.9 ⚠ H1 do Ituassu: **convergiu, sim** — a falha é de esquema, não de volume

A curva `A(volume)` do eixo mídia (07/ago/2026, 300 réplicas/ponto,
[RESULTADOS_FASE3_curva_midia.md](casos/twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE3_curva_midia.md))
derrubou o veredito que a tabela mestre registrava para H1:

- a média do RTMV é **36,1% em todo n**, de 100 ao universo — o estimador não deriva;
- os **48,3% do artigo não cabem** na banda de n=700 **aleatório** (32,6–39,9%),
  o que **exclui erro amostral**;
- bastariam **200 tweets aleatórios** para refutar H1 com **99,7% de poder**; o
  artigo coletou **700**.

**Correção:** a linha 2 passa de *convergiu? NÃO* para ***SIM, em n≈200***, e a causa
da falha do alvo passa de "volume insuficiente" para **viés do esquema de
amostragem**. Dizer que "coletar mais era necessário para chegar à conclusão correta"
é falso para H1 — coletar mais *revelou* o erro, mas uma amostra aleatória 3,5×
**menor** já o teria evitado.

**Consequência para o protocolo (já no `corpo.tex`, §*A curva de volume*):** o par
mudou?/convergiu? pode atribuir a volume uma falha de desenho amostral. Proposta de
**terceira pergunta**, para todo alvo que amostrou: *o esquema é não-viesado para a
quantidade de interesse?* — operacionalizada como "a estimativa publicada cabe na
banda de subamostras aleatórias do mesmo tamanho?".

### 4.11 ✅ MP/MC do Ituassu — divergência **fechada como irresolúvel** (07/ago/2026)

A divergência MP **72,2% × 59%** do paper de 2018 estava "sem causa estabelecida".
Testadas as quatro explicações que dependiam da **nossa** classificação, todas
descartadas
([sensibilidade](casos/twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md)
· [link rot](casos/twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE0_mp_mc_cdx.md)):

| candidato | resultado |
|---|---|
| convenção de lista MP (estrita × conceitual) | ❌ alargar MP **piora** (+4,9 p.p.) — a estrita já é o mínimo |
| blog/coluna em portal | ❌ efeito ausente (−0,1 p.p.), e **97,6% dos paths são visíveis** |
| resíduo `indefinido` (2.082 tweets, 692 hosts, curados) | ❌ −1,3 p.p. |
| link rot | ❌ −0,1 p.p. sob hipótese natural; CDX não alcança (1 recuperado em 78) |

⚠ **Duas revogações que isso produziu:**
1. O §6 de `RESULTADOS_analise_midia_MV_MH.md` afirmava que encurtado carrega **mais**
   MC que direto (34,2% × 23,7%). **É o inverso**: 27,2% × 51,8%. Encurtador é
   ferramenta de quem publica em volume, logo carrega **mais MP**.
2. O "teste pendente do CDX" registrado lá foi **feito** e fecha (c) negativamente.

**Resta só a explicação do lado do artigo** — corpus diferente ou critério não
explicitado. Como o alvo não publica a lista de domínios por classe nem o gabarito
dos 2.200 sorteados, **não é resolúvel com o material publicado**. Fica registrada
como limite de reprodutibilidade do alvo, não como pendência de trabalho.

### 4.10 ⚠ H2 do Ituassu — não reproduz em recorte nenhum (07/ago/2026)

A curva **por dia** (H2 é afirmação sobre *um dia*) mostrou que a rivalidade MH ≥ MV
tem taxa **0%** em todos os dias a partir de n=50 — e **0% já em n=25** no 23/out,
o dia que o artigo aponta. Ali o pior caso em 300 réplicas ainda deixa a MV **31
pontos à frente**.

O ponto novo: **a amostra do próprio artigo, reconstruída, também não mostra
rivalidade em 23/out** (MV 62,0% × MH 13,0%). E sob a leitura alternativa ("MH atinge
o pico da semana"), o dia seria 21/out no universo ou 20/out na amostra — nunca 23.

**Logo H2 não falha por volume nem por viés de esquema.** A divergência fica **sem
causa atribuída**: ou o artigo usou outra operacionalização de "rivalizar", ou a
amostra dele difere da nossa reconstrução (que é aproximada — ele não detalha o
procedimento, e a hora de pico de 22/out é ambígua no próprio texto).

### 4.8 ✅ AV2 e E3 — caso vacinas fechado em 07/ago/2026

- **AV2:** a leitura que o artigo quis é a do **topo-1** (2,33× ≈ o "2×" declarado);
  a agregada dá 1,50 contra 1,68 dele. Não muda entre limiares — e **não muda por
  construção**: afirmação sobre a cauda extrema é imune à sub-coleta.
- **E3 (largura do filtro):** o balanço pró/anti **não inverte em nenhum** dos 6
  termos-índice (razão 1,41–7,42), mas a **composição temática muda muito**. Achados
  de passagem: os termos "anti-*" capturam **gente pró falando sobre anti-vaxxers**
  (75,5% pró em `anti-vax`) e `anti-vacinação` traz **7 tweets** em 29.978 — a lista
  efetiva do artigo tem 4 termos, não 6.

**A leitura que isso consolida:** volume e largura de filtro são **eixos
independentes que podem responder ao contrário**. O enquadramento é robusto ao
volume e frágil ao filtro; o balanço entre polos, o inverso. Está no `corpo.tex`
como seção própria e na §5 da tabela mestre.

### 4.5 ✅ E2 (janela) do caso vacinas — **respondido negativamente em 07/ago/2026**

Suspeitava-se que o corpus 27% maior que o da Tabela 1 viesse da coleta de
repercussões de 8/mar/2022. **Não vem:** o snapshot cobre exatamente
`2021-12-08T23:00` a `2022-02-08T22:59`, a janela do artigo. A diferença é de
**convenção de contagem** — "originais em pt de autores no grafo de RT" reproduz a
coluna de tweets do artigo a **+2%** (1.129.126 × 1.107.224), batendo com o critério
de inclusão declarado no PDF. Fica sem explicação o excesso de **12% nos RTs** dentro
da janela idêntica.

Corrigido de passagem no [FASE2](casos/vacinas/data/repl/vacinas2022/FASE2_replicacao_ponto.md):
o doc afirmava que os 6.554.705 posts da réplica eram "= Tabela 1 do paper", e não são
(a Tabela 1 soma 5.149.274; a re-coleta de mai/2022 é 27% maior).

### 4.12 ✅ Caso Reddit: #207 descartado, substituído por Buntain + Massachs — **`tab:casos` editada em 07/ago/2026**

Histórico: em 7/ago/2026 a Fase 0 do #207 detectou que a `tab:casos` o rotulava como
**Centralidade**, mas o paper ("My Boyfriend is AI") faz clustering + classificação, não
SNA. A Mariana **descartou o #207** (preprint sem tração) e o substituiu por dois alvos de
Reddit relevantes — **Buntain & Golbeck 2014** (WWW, 133 cit., **SNA de verdade**) e
**Massachs 2020** (WebSci, homofilia/polarização).

**Resolvido:** a `tab:casos` foi editada (compila, 34 p.): a linha #207 virou **Buntain**
(Centralidade), a linha #117 (aborto) foi **removida** — "do Reddit só Buntain e Massachs",
decisão da Mariana — e no lugar entrou **Massachs**. A prosa "exemplar" e a legenda foram
ajustadas (não é mais "um por rede social", pois Reddit tem 2).

**Decisão de rótulo (dados da survey):** o Massachs foi rotulado **"Polarização"**, não
"Homofilia". Motivo: nas 244 fichas com tipo de análise codificado no `research.db`,
**homofilia aparece 0×**, mas **polarização é top-8 (25×)** — a legenda promete "tipos de
análise mais recorrentes", então o rótulo tem de ser recorrente. Homofilia é o *mecanismo*,
descrito no capítulo. Se a Mariana preferir o termo preciso, é só trocar de volta.

Docs dos casos: [reddit-buntain](casos/reddit-buntain/REPLICACAO_CASO_BUNTAIN.md),
[reddit-massachs](casos/reddit-massachs/REPLICACAO_CASO_MASSACHS.md).

### 4.13 ◐ Instagram/Facebook: a célula tem alvo — **decidido em 07/ago/2026**

A última rede sem artigo definido foi preenchida: **Capozzi et al.**, *Clandestino or
Rifugiato?* (**CHI 2021**, 29 cit.) + *Facebook Ads: Politics of Migration in Italy*
(SocInfo 2020, 16 cit.), sobre anúncios de imigração na Itália na **Meta Ad Library**.
Análise: **classificação** pró/anti (F1 = 0,85) — o tipo que a `tab:casos` pede.

**O que decidiu a escolha não foi a citação, foi a coleta.** Varridas as rotas Meta
existentes em ago/2026: a API do Instagram está morta desde 2018-2020, o CrowdTangle foi
desligado em ago/2024, e a **Meta Content Library** virou paga em jan/2026 (US$ 371/mês +
US$ 1.000) **e não deixa os dados saírem do ambiente seguro** — o que quebra a Fase 1 do
protocolo (snapshot congelado local). Sobra **uma** rota: a **Ad Library API**, grátis e
exportável. Consequência a declarar no capítulo: a célula Instagram/Facebook será sobre
**anúncio pago**, não post orgânico.

O alvo tem duas qualidades que nenhum caso anterior teve: **a sub-coleta é declarada pelos
próprios autores** (*"we search for ads appearing only on Facebook (**not Instagram**)"*,
SocInfo §3) e o **gabarito está publicado** — CSV com 2.312 anúncios, baixado e conferido
contra o paper (bate exatamente; 731 × 733 páginas é a única divergência).

**Decisão da Mariana no mesmo dia:** o **Brasil entra como segundo braço** do caso, não
como caso próprio — o candidato brasileiro (WebMedia 2022) é descritivo, não classifica e
não está indexado no Semantic Scholar. O braço BR **não gera linha** na `tab:casos` nem na
tabela mestre; serve de teste de robustez entre polities e de mitigação do risco de
retenção do arquivo europeu. Ver [REPLICACAO §3](casos/meta-ads-imigracao/REPLICACAO_CASO_META_ADS.md).

**Atualização do mesmo dia — o full text do CHI 2021 foi lido, e mudou duas coisas:**

1. ⚠ **O alvo-teste CB2 está ambíguo no próprio artigo.** O resumo diz "47,6% de *todos* os
   anúncios de migração"; o corpo (§5.2) mostra que, entre os 2.312, os anti são **677 =
   29,3%** — os 47,6% são **368/773**, só os de **grandes partidos**. E os 65,2% das
   impressões têm um **terceiro** denominador. ✅ **Fixado no mesmo dia** — ver §4.14.
2. ✅ **Existe um segundo dataset público** (nota de rodapé 10 do CHI): **200 anúncios × 3
   anotadores, com o texto dos anúncios**. Isso (a) dá o **gabarito pró/anti** de graça,
   encolhendo a decisão de rotulagem, e (b) libera parte do insumo do classificador **sem
   depender da retenção**. Com ele, o **α de Krippendorff foi reproduzido** — 0,763 × 0,76
   nos 5 rótulos (n=174, exato) e 0,924 × 0,92 nas 2 polaridades, esta sobre **141**
   anúncios contra os 150 declarados (divergência registrada, não explicada).

**O que falta:** editar a `tab:casos` (§1, item 8) e abrir a conta Meta verificada (§2).

### 4.14 ✅ CB2 desambiguado, e as impressões do alvo não reproduzem (07/ago/2026)

Decisão de método registrada em
[DECISOES_CB2.md](casos/meta-ads-imigracao/data/repl/metaads2019/DECISOES_CB2.md).

A afirmação substantiva de CB2 é de **desproporção** ("os anúncios anti capturam atenção
acima do seu peso"), e quem a carrega é a **razão** R = fatia de impressões ÷ fatia de
anúncios — não qualquer das porcentagens isoladas, que se movem mecanicamente quando a
população do denominador muda. **Base primária: os anúncios com posição** (R = **1,72**),
com a base de **todos** sempre ao lado (R = **1,46**); a dos grandes partidos fica
reportada, não testada.

Três razões: é a única base em que **as duas metades da afirmação usam a mesma população**;
casa com o **instrumento** (o classificador tem duas etapas, e "ter posição" é o domínio de
saída da segunda); e mantém a **comparabilidade com a linha 7** da tabela mestre, que usa a
mesma convenção — necessária porque a leitura PP3 nº 3 se constrói comparando casos.

⚠ **Achado colateral, e é sério:** o total de impressões do artigo **não reproduz** a partir
do CSV que ele publica. O CHI reporta ~35 M; o CSV dá **49,8 M** pela regra que o SocInfo
§3 **declara** usar (média dos extremos do intervalo), 36,5 M somando os mínimos e 63,1 M
somando os máximos. Confirmado por caminho independente (somar as 14 colunas demográficas
dá 49,65 M). A hipótese "são só as impressões localizadas na Itália" foi **testada e
descartada**. Como os 65,2% são uma fatia de impressões, herdam a ambiguidade — a Fase 2
roda as **duas** convenções e reporta a sensibilidade.

### 4.15 ⚠ `#AecioNever` estava do lado errado no nosso próprio doc — **corrigido em 18/ago/2026**

O `STANCE_como_o_paper_fez_e_onde_estamos.md` §3 dizia que `#ForaDilma` e `#Aécionever`
eram, as duas, "claramente contra Dilma → tende a **EA**". O artigo cita as duas como
exemplo de sinal explícito **sem dizer de que lado cada uma está** — a glosa foi nossa, e
está errada: *"Aécio never"* = **nunca Aécio**, logo **pró-Dilma (ED)**.

Medido, sem circularidade (`analise/lean_hashtags.py`, sementes de lado auto-evidente,
`#aecionever` **fora** das sementes): nas **157** ocorrências da janela, ela co-ocorre
**84×** com hashtags declaradamente pró-Dilma e **0×** com pró-Aécio.

**Por que importa:** essa linha ia direto para o prompt do rotulador automático e para o
codebook do gabarito humano — os dois lados da medida de κ teriam herdado o mesmo erro,
que **não apareceria** na concordância. Corrigido no doc de origem e registrado no
[CODEBOOK_stance.md](casos/twitter-ituassu/CODEBOOK_stance.md) §2 e §7.

**Achado de passagem:** o mesmo script mede o lado das demais hashtags frequentes —
`#desesperodaveja` é ED 100%; `#VemPraRua25deOutubro`, `#MudaBrasil`, `#AcordaBrasil` e
`#corrupcao` são EA 100%; e as temáticas (`#G1`, `#DebateNaGlobo`, `#Dilma`) têm lean
**EA 61–85%**, o que é composição do público e **não** pode virar regra de rotulagem.

---

## 5. Estado por frente (uma linha cada)

| Frente | Estado |
|---|---|
| **casos/twitter-ituassu** | **Eixo mídia completo** ✅ — curvas `A(volume)` de H1, da dominância MV e de H2 por dia (07/ago). H1 convergiu em n≈200 e a falha do alvo é **de esquema** (§4.9); H2 **não reproduz em recorte nenhum** (§4.10) · **MP/MC fechado** ✅ — resíduo curado e as 4 explicações de classificação descartadas; divergência é do lado do artigo e **irresolúvel com o publicado** (§4.11) · **stance ◐ kit de rotulagem pronto** (18/ago/2026): codebook, amostra congelada de 320 (seed `20260818`), split 110/210, reteste de 40 e pré-registro com κ ≥ 0,70 — falta **só a Mariana rotular**. De passagem, corrigido o lado de `#AecioNever` (§4.15) |
| **casos/heine-xande** | Docs + pipeline ✅ · Fase 0 ✅ (dado não localizado) · Fases 1–4 ⏳ SharePoint |
| **casos/vacinas** | **AV1–AV6 e E1/E2/E3 todos medidos** (07/ago/2026) — auditoria do [plano §4.1](casos/vacinas/REPLICACAO_CASO_VACINAS.md) zerada · eixo B validado (κ 0,759 / 0,697) · colunas vazias explicadas (vazias na fonte) · ⏳ **único item aberto:** validar o rotulador no estrato baixo sob a convenção do artigo (precisa de rotulagem humana) · saldo LLM US$ 9,58 |
| **casos/reddit-buntain** | ✅ **CASO FECHADO** (19/ago/2026). Alvo **Buntain & Golbeck 2014** (WWW, 133 cit.). Coleta completa: **43.479 submissions + 1.015.247 comentários**. **RB3: 3% → 57,6%** sob o mesmo limiar (**19×**); sem corte, 15,2% de 217.386 usuários. Converge em k≈10–20. ⏳ falta só o **capítulo** |
| **casos/reddit-massachs** | Alvo **Massachs 2020** (WebSci, 29 cit.), **homofilia** (tipo novo). **Fase 0** ✅ · **Fase 1a** ✅ gabarito baixado e conferido (44.924 usuários / 7.083 apoiadores, **exato**) · **Fase 2** ✅ **MH1 REPRODUZ** (18/ago/2026): 34,6% × 34,8% na homofilia e 26,8% × 26,7% na influência — ordenação idêntica, e o baseline aleatório também bate (15,6% × 15,2%) · **Fase 3** ⏳ dumps 2012/2016 para baixar o limiar do focus group |
| **casos/reddit-companhia-ia** | ❌ **DESCARTADO** (07/ago/2026): #207 "My Boyfriend is AI" era preprint sem tração. Tombstone no README; substituído pelos dois acima |
| **casos/meta-ads-imigracao** | **Novo** (7/ago/2026) — fecha a **última rede vaga** do lineup. Alvo **Capozzi et al.** (CHI 2021, 29 cit. + SocInfo 2020, 16 cit.), **classificação** pró/anti em anúncios da Meta Ad Library. **Fase 0 ◐ quase fechada**: **os dois papers lidos na íntegra**, **dois gabaritos públicos** baixados e conferidos (2.312 anúncios de metadados + 200 anúncios × 3 anotadores **com texto**), 26 keywords transcritas, rota decidida (Ad Library API — a única coleta Meta viva), predições pré-registradas, e o **α de Krippendorff reproduzido** (0,763 × 0,76; 0,924 × 0,92 — ⚠ n 141 × 150). ✅ **CB2 desambiguado** — mede-se a razão R (§4.14). ⏳ só falta a **conta Meta verificada** (§2). Braço **Brasil** como mitigação de risco, sem alvo próprio |
| **casos/tiktok** | **A célula ressuscitou em 18/ago/2026.** A rota de coleta segue morta (credencial do eTC revogada), mas o alvo mudou de #299 para **PoliTok-DE** (arXiv 2509.15860), que publica dados no Hugging Face sob CC-BY **sem gate** — 939 mil posts de duas eleições alemãs com **status de disponibilidade por data** + 935 anotações humanas. **Fase 2 feita, offline**: **6 das 7** afirmações replicam (18,7% e 39,7% de deleção **exatos**; 2/3 de retirada pelo autor; 1-em-5 de intolerância; maioria com humor). A 7ª (deleção pela plataforma, 13,0%) replica a **1,4 p.p.** sob convenção não publicada. ★ **achado novo:** a taxa de deleção vai de **3,3% → 9,5% → 18,7%** em três checagens do **mesmo** conjunto — um **eixo temporal** independente do volume. Infra de coleta pronta, esperando chave viva |
| **casos/youtube-agecovp** | A **quarta rede**. Alvo **AGECovP** (*EPJ Data Science* 14:65, 2025). **Fase 0** ✅ · **gabarito conferido** ✅ · **Fase 2** ✅ o ponto original replica (AG4 a **1,9 p.p.** sob convenção não declarada; AG2 com folga — comentários **74×** mais tóxicos; AG1 só no VADER) · **Fase 3 ◐ parcial** (50/85 buscas): o filtro descarta **60,2%** (artigo: 52,1%), e os vídeos que ele mantém têm **5,3×** mais chance de estar no corpus do artigo (33,0% × 6,2%) — **a reconstrução é fiel e o filtro é o mecanismo**. ❌ **a predição P4 falhou**: 'Society' **sobe** entre os descartados, e aparece conteúdo **fora do tema** (Sport, Baseball, 7,9%) — o filtro também remove ruído legítimo, o que exige restringir a comparação aos descartados no tema antes de concluir · ⏳ 35 buscas restantes (cota das 4h)  · ★ **AG3 é irreproduzível porque o artigo se contradiz** (19/ago): ele diz *"less than 7% of the videos were **UCC** and not UGC"* (→ >93% UGC) e, no parágrafo seguinte e de novo na seção de sentimento, *"UGC accounts for less than 7%"* (→ ~7% UGC). A leitura "imprensa dominante" é **carregadora**: explica o sentimento positivo e a toxicidade baixa. Os rótulos UGC/UCC foram manuais e **não estão publicados**. Nossa medição independente dá **32,0%** — nenhum dos dois extremos. Calibragem **recusada** de propósito ([DECISOES_regras.md](casos/youtube-agecovp/data/repl/agecovp2020/DECISOES_regras.md)) · ✅ a regra `no_tema` validou: aprova **99,9%** do corpus do próprio artigo |
| **casos/ (Fase 4)** | [Tabela mestre](casos/RESULTADOS_tabela_mestre.md) ✅ **parcial** — 10 linhas fechadas, **7 ⏳** (Heine ×2, stance, Reddit ×2: Buntain + Massachs, Meta Ads ×2) · a linha 12 (Massachs) já tem o **ponto original replicado** · coluna *fração mínima* com **3 de 10** células · ⚠ ganhou uma **leitura nova de PP3**: o par mudou?/convergiu? pode confundir viés de esquema com falta de volume (§4.9) |
| **escrita/dissertacao** | Compila limpo (**45 p.**) · números do eixo mídia ✅ · **três capítulos de caso escritos e não revisados** (vacinas, YouTube, TikTok) · `tab:casos` ✅ fechada · conclusão ✅ reescrita (4 casos, quatro eixos de decisão de coleta, achado de reprodutibilidade) · front-matter ⏳ |
| **escrita/survey** | Todas as seções em rascunho revisado · 2 decisões em aberto · sem pendência de dado |
