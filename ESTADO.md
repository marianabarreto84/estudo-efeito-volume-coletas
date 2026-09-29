# ESTADO — o que dá para avançar agora

> **Documento canônico de estado.** Responde a uma pergunta só: *sentando agora,
> o que dá para fazer sem depender de ninguém e sem esperar nada?*
> Última revisão: **28/set/2026** (preparação da defesa: artefatos publicáveis, contas de
> infraestrutura, errata em LaTeX e o `PERGUNTAS.md` auditado — ver §4.30). Antes: **15/set/2026** (extração completa dos 198 PDFs da revisão: base
> 2.322 → 2.472, survey e dissertação refeitas e alinhadas de novo no `revisao-12.pdf`).
> A rodada 9 da dissertação só tirou travessões (70 → 0), itálico de ênfase (145 → 39) e
> negrito de ênfase no texto (41 → 31, os que restam são de tabela), pelo critério da
> survey; mapa em [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md).
>
> ✅ **Extração completa (15/set/2026): os 198 PDFs que nunca tinham passado pelo modelo
> foram extraídos** (pedido da Mariana, comentário 4 da v3). Entraram 196 (6 da Tech
> Science Press com o texto lido pelo `pypdf`, desvio autorizado por ela e registrado na
> §3.4 da survey; 2 PDFs corrompidos ficaram de fora), 150 deles na base, que foi de
> **2.322 para 2.472**. Todos os números da survey e da dissertação foram refeitos pelo
> `aplica_numeros.py`. Nenhuma frase qualitativa deixou de valer e nenhuma conclusão
> mudou (filtragem 81,1% → 80,3%, amostragem 18,9% → 18,6%, Twitter 64,9% → 64,8%).
> Registro em [revisoes/README.md](escrita/survey/revisoes/README.md) §Extração completa e
> em [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md) §revisao-12; roteiro e
> scripts em [`extracao198/`](escrita/survey/revisoes/extracao198/LEIA.md). Backup do banco
> de antes: `research.db.antes_198_20260915`. ✅ **Decidido por ela (15/set/2026):** o
> volume de “100 bilhões de submissões” do art#873, que o próprio artigo declara (erro
> dos autores, e não da extração), **fica**, porque a revisão registra o volume que cada
> artigo declara.
>
> 📦 **Versão final para envio em [`versao_final/`](versao_final/)** (15/set/2026):
> `Dissertacao_MarianaBarreto.pdf` = `revisao-13.pdf` (80 p., md5 conferido) e
> `Survey_MarianaBarreto.pdf` = **rodada 6 da survey, v7** (15 p.): os 14 comentários da
> versão final anterior, mais 49 feitos na própria versão final (6 na v1, 2 na v2, 11 na
> v3, 8 na v4, 11 na v5, 11 na v6), e a base de 2.472 da extração completa. Desde a v5, o teste do
> viés de acesso usa os 811 recuperados (sem o sorteio de 800), e a §4.4 traz a
> interseção SGBD × arquivo (SGBD 130 → 133, por uma correção na regra). A v6 vai direto
> aos 3.107 PDFs com extração e não tem mais a tabela de percurso. O ciclo é disparado pela skill
> **`/versao-final`**. Por pedido dela,
> comentários na versão final contam como a **mesma rodada**: o arquivo é refeito no
> lugar, a versão comentada vai para `escrita/survey/revisoes/` (`survey-5.pdf`,
> `survey-6-v1.pdf`…), e o `Survey_MarianaBarreto_trechos_refeitos.pdf` é regerado por
> `revisoes/gera_trechos.py` sempre contra a survey de antes da rodada
> (`revisoes/base_rodada6.tex`). Ver [revisoes/README.md](escrita/survey/revisoes/README.md)
> §rodada 6. ✅ A dissertação foi **alinhada à survey no mesmo dia**, a pedido dela
> (`revisao-10.pdf`): 10.200 em paywall, sem a divisão 2.298 + 811 dos PDFs. Ver
> [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md) §revisao-10. Os PDFs não entram
> no git (`.gitignore` exclui `*.pdf`).
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
| ~~3~~ | ✅✅ **STANCE FECHADO em 9/set/2026 — é a 16ª linha da tabela mestre e está no `corpo.tex` (§4.5, `sec:stance`).** A Mariana rotulou os **210** do teste cego à mão, em três fases (portão → stance por texto, com propagação → desambiguação do NDA). Gabarito: **NDA 71,4% · EA 19,0% · ED 9,5%** — P1 e P2 do pré-registro confirmadas. ⚠ **O rotulador automático REPROVOU** o critério (κ 0,604 < 0,70; portão 0,781 < 0,90), e **o critério não foi revisto** — a Mariana havia apostado a reprovação, e acertou. ★ **O teto da tarefa explica a reprovação**: as duplicatas do dev dão κ **0,625** entre a anotadora e ela mesma (0,198 com a manchete ambígua da irmã de Lula, que gerou o caso-limite 13) — o rotulador está **no teto**, a dois centésimos. ★ **Estimativa corrigida** pela inversão da matriz de confusão sobre **5.000** tweets do universo: fatia sem lado **23,4% → 65,8%** (muda, converge em n≈2.000, plana desde n=100), mas a razão EA/ED fica **indecidível** (1,01; IC95% [0,36; 2,35], que contém o 0,80 do artigo). É **indeterminação de instrumento**, categoria nova no conjunto. ⚠ **O reteste de 40 não foi feito e não será**: 26 dos 40 vinham do teste rotulado no mesmo dia, e os ≥7 dias cairiam em 16/set, depois da entrega. Custo total US$ 1,47; livro-caixa em US$ 16,89 de US$ 25 | [VALIDACAO](casos/twitter-ituassu/data/repl/compos2014/stance/RESULTADOS_stance_validacao.md) · [UNIVERSO](casos/twitter-ituassu/data/repl/compos2014/stance/RESULTADOS_stance_universo.md) | Nada a fazer aqui. O que resta do caso é o **eixo de temas**, sem rotulagem |
| **4** | ✅ **Survey rodada 6 (15/set/2026): os 14 comentários da versão final aplicados**, e o PDF novo substitui o anterior em `versao_final/` (15 p., limpo). O modelo específico só é nomeado na metodologia; o funil ganhou a conta aberto × paywall (13.395 = 3.108 + 10.200 + 87; 3.109 PDFs ≠ 3.108 abertos); a §2 cita três trabalhos sobre LLM em revisões; a evolução anual abre pela API; a Fig. 7 separa 10⁷–10⁸ de ≥10⁸; a Fig. 5 **ficou em barras** (81,1 + 18,9 = 100 é coincidência). Nenhum número antigo mudou, mas o paywall passou de 10.230 para 10.200 (outra fonte) — ✅ a dissertação foi alinhada no mesmo dia (`revisao-10.pdf`, também em `versao_final/`). Mapa em [revisoes/README.md](escrita/survey/revisoes/README.md) §rodada 6. Antes: ✅ **Survey: [`revisoes/survey-5.pdf`](escrita/survey/revisoes/survey-5.pdf) publicado em 14/set/2026** (14 p., limpo) — os 12 comentários do `survey-4.pdf` + **reescrita do texto inteiro contra maneirismos de IA**, tomando como referência a proposta de dissertação dela, o SBBD 2023 do grupo e a dissertação da Salgueiro. O κ saiu do texto (fica a concordância bruta, que ela consegue explicar); o Claude Haiku virou só “tentativa de triangulação”; o “gabarito de um artigo” deixou de ser citado; as figuras ficam junto do texto; os grandes coletores viraram três pizzas. ⚠ Duas afirmações corrigidas de passagem. Nenhum número mudou. ⏳ **Decisão dela:** dar mais foco ao **banco de dados**? Hoje é resultado secundário (ver [revisoes/README.md](escrita/survey/revisoes/README.md) §rodada 5). Antes: ✅ **Survey: [`revisoes/survey-4.pdf`](escrita/survey/revisoes/survey-4.pdf) publicado em 14/set/2026** (15 p., limpo) — **primeira rodada com PDF comentado**: os 7 comentários da Mariana no `survey-3.pdf` (pp. 1–2) + pedidos de figura. O achado passou a ser **a onipresença da filtragem por critério** (e não o contraste com a amostragem, que ela já tinha corrigido antes); itálico só em inglês (89 → 46) e negrito só nos rótulos (26 de ênfase cortados); a dissertação foi conferida e já resume a revisão pela filtragem, sem mudança; plataformas e estratégia de coleta viraram **barras**, e a persistência ganhou uma **pizza** de onde os dados ficaram (SGBD 5,2% · só arquivos 6,5% · não menciona 87,9%); a Fig. temporal perdeu o eixo duplo; a §2 cita Tufekci, Ruths & Pfeffer e Olteanu. ⚠ De passagem, um **erro factual** corrigido: o estudo de ≈2,8 bi de tweets era dado como exemplo de *amostragem*, e é de *filtragem* (Jimeno-Yepes 2015). **Nenhum número mudou.** Mapa em [revisoes/README.md](escrita/survey/revisoes/README.md) §rodada 4. Antes: ✅ **Survey: [`revisoes/survey-3.pdf`](escrita/survey/revisoes/survey-3.pdf) publicado em 14/set/2026, à noite** (13 p., limpo) — auditoria de vieses: base **2.322** (com a expansão), **tudo só-Gemini**, série temporal com e sem arXiv, descarte sem DOI medido, validação 2023–26 declarada, a lacuna deixou de ser afirmada sem medida. ✅ A dissertação foi **realinhada a ele na mesma noite** (`revisao-8.pdf`, §4.28). Detalhe em [revisoes/README.md](escrita/survey/revisoes/README.md) §rodada 3. Antes: ✅ **Survey: [`revisoes/survey-2.pdf`](escrita/survey/revisoes/survey-2.pdf) publicado em 14/set/2026** (12 p., limpo) — “levantamento sistemático” → “revisão”, pedido do orientador; o título agora termina em *“uma Revisão da Literatura”*. Nenhum número mudou, e a divergência de base com a dissertação (§4.24) foi **resolvida** no mesmo dia. Autoria, afiliação e agradecimento à CAPES copiados da dissertação, e os e-mails dos dois autores informados por ela. O registro da rodada 1: ◐ **Survey: existe um PDF de rodada, [`revisoes/survey-1.pdf`](escrita/survey/revisoes/survey-1.pdf) (9/set/2026, 11 p.), escrito como artigo fechado.** O que falta é a **leitura dela** — o ciclo é o mesmo da dissertação (comenta o PDF → a rodada seguinte aplica). Nesta rodada o artigo ganhou **6 figuras** (funil, série anual com a queda do Twitter/X, κ por campo, amostragem × filtragem, volume, persistência corpus × grandes coletores) e **5 tabelas**, todas geradas por `figuras.py`/`validacao.py` a partir do `research.db` — nenhum número digitado à mão, e o dump fica em `numeros.json`. Três coisas que a leitura precisa decidir: (a) a **base subiu para 1.723** e o `corpo.tex` segue em 1.718 (§4.24); (b) a decisão em aberto nº 1 **deixou de ser "como reportar"** e virou ameaça à validade **medida** (12,4%, IC95% 11,3–13,6, ~830 artigos recuperáveis); (c) a recomendação nº 1 do diagnóstico de tipos de análise segue **declarada e não aplicada** | [survey-1.pdf](escrita/survey/revisoes/survey-1.pdf) · [STATUS.md](escrita/survey/STATUS.md) §Decisões em aberto | Redação pura; nenhuma pendência de dado. ◐ **a decisão nº 1 virou medição** — ver item 12 |
| **12** | ⭐ **Expansão do corpus da survey — a varredura ACABOU (23/ago/2026, 05:17) e ninguém tinha lido o desfecho até 9/set.** Fila **100% tentada**: 11.093 de 11.093. Recuperados **811 PDFs** sem credencial nenhuma — a base de PDFs foi de 2.298 para **3.109**. ⚠ **A taxa final é 7,7% no estrato pago** (772/10.039, IC95% 7,2–8,2), **não os 12,4%** da medição intermediária — os ICs **não se sobrepõem**, e a explicação provável é que aquele numerador incluía os 307 órfãos de disco de execuções em outra ordem (§4.25). ⛔ **A condição de parada pré-registrada DISPAROU** (piso de 11%; o IC inteiro está abaixo): pelo [PRE_REGISTRO](escrita/survey/expansao/PRE_REGISTRO_expansao.md) §8, a extrapolação não vale e o trabalho "vira uma nota de método". ⛔ **E a extração dos 800 NUNCA RODOU** — bug de shell (caminho do Windows interpolado dentro de `$(...)` do bash), com o laço reportando `codigo 0` por cima do erro; por isso passou 17 dias despercebido. **Nada foi gasto**, os **800 seguem sorteados** pela semente `20260929` e os PDFs estão em disco. **O que dá para avançar aqui é decisão dela, não trabalho** — ver §3, item 12 | [EXPANSAO_recuperacao.md §3c e §7](escrita/survey/EXPANSAO_recuperacao.md) · [expansao/README.md](escrita/survey/expansao/README.md) | A varredura não pede mais nada: acabou. O que resta é (a) decidir se a extração dos 800 acontece apesar do `PARAR`, e (b) conferir a hipótese dos 307 órfãos antes de o 7,7% virar número final em outro lugar |
| **5** | ✅ **ÚLTIMA VERSÃO: [`revisao-8.pdf`](escrita/dissertacao/revisoes/revisao-8.pdf) (14/set/2026, noite, 80 p., zero erros, zero indefinidas, zero `Overfull`) — alinhada ao `survey-3.pdf`**: base 2.322, Tab. 1.1 = Tab. 4 da survey (só Gemini), Twitter 64,9%, mediana ≈387 mil, e a revisão deixou de ser citada como prova de que “quase ninguém verifica” o recorte, que a extração não mede. ⚠ **O `revisao-7.pdf` ficou intocado, por ser a versão entregue: se ele já foi à banca, é o `revisao-8.pdf` que precisa ser reenviado** — decisão da Mariana. O registro anterior: ✅ **VERSÃO FINAL: [`revisao-7.pdf`](escrita/dissertacao/revisoes/revisao-7.pdf) (14/set/2026, 80 p., zero erros, zero indefinidas, zero `Overfull`).** O pedido do orientador (“levantamento sistemático” → “revisão”) foi aplicado, e a dissertação foi **alinhada à survey**: base 1.723, PDFs só por rota aberta, dois modelos retidos, Tab. 1.1 = Tab. 3 da survey, Twitter 63,7% da base e o falso “quarto tipo mais frequente” corrigido. Mapa em [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md). O registro anterior: ✅ **DISSERTAÇÃO PRONTA PARA A ENTREGA (9/set/2026). ⚠ A entrega é **14/set** e é a **VERSÃO FINAL PARA A BANCA**, não um depósito prévio; a defesa segue em 29/set.** **80 páginas**, zero erros, zero indefinidas, zero `Overfull`. O que mudou hoje: (a) **um capítulo por caso** — o Cap. 6 cobria dois casos de Reddit e virou **6 (Papéis Sociais)** e **7 (Homofilia)**; a numeração dos seguintes já os contava como dois (“Quinto Caso”, “Sexto”), então nada precisou de renome, e as 10 referências externas foram reapontadas uma a uma. Cada um ganhou conclusão própria, sem duplicar, com o contraste só no quarto caso (decisão dela); (b) o **Cap. 8 perdeu o “Parcial”** — nenhum capítulo quebra mais no sumário; (c) o **eixo de stance entrou** (§4.5) e a tabela mestre foi de 15 para **16 linhas**; (d) o **front-matter fechou**: dedicatória (texto dela, com uma correção de aposto), agradecimentos (+ banca, + família) e bio (2023/2024). ✅ **Nenhuma pendência bloqueia a entrega.** | [revisao-6.pdf](escrita/dissertacao/revisoes/revisao-6.pdf) · [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md) | O que resta é leitura dela. Os **Caps. 5 a 8** seguem sem comentário desde o `revisao-2.pdf` |
| ~~5 (rodada 1)~~ | ✅ **Rodada 1 aplicada em 21/ago/2026.** A Mariana comentou **pp. 6–27** do [`revisao-1.pdf`](escrita/dissertacao/revisoes/revisao-1.pdf) (Resumo → início do Cap. 4) e os **32 comentários foram todos aplicados**; mapa comentário→mudança em [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md). O [`revisao-2.pdf`](escrita/dissertacao/revisoes/revisao-2.pdf) espera a leitura dela | [revisoes/](escrita/dissertacao/revisoes/) | Fluxo fixado: ela comenta o último `revisao-N.pdf` → a rodada seguinte aplica e salva `revisao-N+1.pdf`. Corrigiu **3 erros factuais** que ela apontou: "o **único** em Twitter/X" (são dois), "seis casos, **um por rede**" (sete em cinco) e a linha *Centralidade* da `tab:casos` (é **papéis sociais**) |
| ~~5b~~ | ✅ **Resolvido em 21/ago/2026:** os quatro capítulos novos foram lidos e comentados pela Mariana na rodada 2, e os comentários foram aplicados (item 5). O registro original: 📌 **Revisar os capítulos novos no `corpo.tex`** — são **quatro**: caso **vacinas** (07/ago), caso **Reddit** (21/ago, cobre Buntain + Massachs), caso **YouTube** (19/ago, **reescrito em 21/ago**) e caso **TikTok/PoliTok** (19/ago), mais os trechos novos da conclusão (o **quarto eixo** — volume, largura, forma e momento — os **números que dependem de decisões não publicadas**, e o parágrafo novo sobre os dois casos de Reddit) | [corpo.tex](escrita/dissertacao/corpo.tex) | Nenhum foi lido pela Mariana. **É trabalho dela.** Compila limpo em **54 páginas** (eram 45 em 19/ago), zero referências indefinidas. ⚠ **A afirmação de circularidade do cap. do YouTube foi corrigida em 21/ago** — a conclusão ficou, o mecanismo mudou (§4.16). Os capítulos foram **renumerados**: Reddit é o 3º/4º, YouTube passou a 5º, TikTok a 6º |
| **6** | ✅✅ **`reddit-buntain` FECHADO (19/ago) e ESCRITO (21/ago).** Coleta completa (**43.479 submissions + 1.015.247 comentários**, 13 subreddits, sem corte) e **RB3 medido**: o artigo diz que **~3%** dos usuários participam de >1 comunidade; no universo, **sob o mesmo limiar de atividade**, são **57,6%** — **19×**. A localidade dos papéis sociais que o artigo relata é **artefato do recorte top-100 × top-200** | [RESULTADOS_RB3](casos/reddit-buntain/data/repl/buntain2013/RESULTADOS_RB3.md) · [corpo.tex §cap:caso-reddit](escrita/dissertacao/corpo.tex) | É o maior efeito de sub-coleta medido na dissertação. **Nada a fazer aqui** — o capítulo foi escrito em 21/ago, junto com o do Massachs, num capítulo só de Reddit |
| **7** | ◐ **`reddit-massachs`: Fases 1a e 2 feitas; Fase 3 FORA DE ESCOPO.** O ponto original **replica** (ordenação homofilia ≈ feedback ≫ influência, pontas a <0,25 p.p.). ⛔ A Fase 3 não foi sequer **dimensionável**: o endpoint de agregação do Arctic Shift falha nos subreddits grandes (2 rodadas, a 2ª mês a mês, 34/34 incompletos). Caminho real seria dump por subreddit no Academic Torrents — download pesado, não cabe até 31/ago | [FASE2 §6](casos/reddit-massachs/data/repl/massachs2016/FASE2_ponto_original.md) · [corpo.tex §cap:caso-reddit](escrita/dissertacao/corpo.tex) | ✅ **Capítulo escrito em 21/ago**, junto com o do Buntain. ⚠ **22/set/2026: o “fora de escopo” foi decidido por uma sessão, não pela Mariana, e o motivo caiu em 22/ago sem que o item fosse reaberto — ver §4.29.** ⚠ a 1ª sonda **imprimiu um total falso** (somava só quem respondia); corrigido — o script agora se recusa a totalizar com falhas e grava `COMPLETO: false` |
| **8** | ⚠ **`tab:casos` MUDOU em 21/ago/2026** — perdeu a linha de **Instagram/Facebook** (decisão da Mariana, §4.18) e a linha do **YouTube** deixou de dizer *Modelagem de tópicos*, que o caso não entrega, passando a *Sentimento + composição do corpus*. São hoje **6 casos em 4 redes**. O registro anterior: ✅ **`tab:casos` FECHADA em 18/ago/2026** — as três células que faltavam foram preenchidas: **YouTube** (#363 → **AGECovP**, agora *Modelagem de tópicos*), **TikTok** (#299 → **PoliTok-DE**, *Análise de conteúdo*) e **Instagram/Facebook** (**Capozzi 2021**, *Classificação*). A prosa que dizia "o caso de Instagram/Facebook ainda não tem artigo definido" foi corrigida. **Compila limpo em 35 páginas** | [corpo.tex](escrita/dissertacao/corpo.tex) §Conjunto de casos | Nada a fazer aqui |
| **9** | ✅ **Feito em 7/ago/2026** — full text do CHI 2021 lido e **CB2 desambiguado**. Nada a fazer aqui; o caso agora só espera a conta Meta (§2) | [DECISOES_CB2.md](casos/meta-ads-imigracao/data/repl/metaads2019/DECISOES_CB2.md) | Ver §4.14 |
| **10** | ⚠ **TikTok: a credencial do eTC está MORTA** — diagnosticado em 18/ago/2026. A Mariana importou a chave e o token deu `invalid_client`. **Não é erro nosso**: a chave do `.env` é a mesma dos dois deployments da vm031 (conferido por hash) e **funcionou em 19/jun/2025** (o log registra `Access token acquired` e uma coleta completa). A aprovação da Research API expirou/foi revogada desde então. **Nada a fazer no código** — ele está pronto e testado a seco | [casos/tiktok/README.md](casos/tiktok/README.md) §2b | Destrava com (a) **renovar a aprovação do eTC** (quem gerencia é o Tomaz, citado no `execute_tiktok.sh`) ou (b) **credencial própria** — o Brasil é região elegível, e credencial própria é o que torna a Fase 1 reproduzível por terceiros |
| **11** | ✅ **Caso YouTube (AGECovP) — FECHADO em 21/ago/2026** no eixo do filtro (nasceu em 18/ago; é a **quarta rede** do lineup). Fase 1 completa: **85/85 buscas, 3.446 vídeos**, mais os **2.165 canais** buscados pela API — cobertura de 100%, o que a Fase 3 parcial pedia. Fases 2 e 3 fechadas. ⏳ resta só AG1/AG2 nos **comentários** (~1 unidade por 100; cabe numa cota diária), que **não** bloqueia a linha 15 da tabela mestre | [README](casos/youtube-agecovp/README.md) · [FASE3 §7](casos/youtube-agecovp/data/repl/agecovp2020/FASE3_efeito_filtro.md) | ❌ **A predição P1 falhou**: o filtro remove **6,4 p.p. menos** conteúdo de usuário do que preserva (IC95% [−11,4; −1,4]), não mais. ★ Mas o **funil inteiro** seleciona muito: canais no corpus publicado 23,5% UGC × **61,7%** fora dele, Δ **+38,3 p.p.**, mediana de inscritos **199 mil × 1.070**. A circularidade do artigo **se confirma e sai reforçada**; o **mecanismo não foi isolado** |

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
> **Feito em 21/ago/2026:** (a) o **caso YouTube fechou** — Fase 1 completa (85/85 buscas,
> 3.446 vídeos) mais os 2.165 canais pela API, e a Fase 3 refeita sobre base íntegra;
> (b) ⚠ **a predição P1 do YouTube foi refutada e o capítulo teve de ser corrigido** — a
> circularidade fica e sai reforçada (+38,3 p.p. contra os 7,9 antigos), mas o mecanismo
> muda: **não é o filtro de palavra-chave** (§4.16); (c) o **capítulo de Reddit foi
> escrito**, cobrindo Buntain e Massachs num capítulo só, com as duas entradas novas no
> `referencias.bib`; (d) os capítulos foram **renumerados** (Reddit 3º/4º, YouTube 5º,
> TikTok 6º) e a conclusão ganhou o parágrafo dos dois casos de Reddit; (e) a **tabela
> mestre passou de 10 para 13 linhas fechadas**; (f) o `CLAUDE.md` da raiz ganhou as
> linhas de **YouTube e TikTok**, que faltavam no mapa e no lineup desde 18/ago. A
> dissertação compila limpo em **54 páginas**.
>
> ⚠ **Incidente da sessão:** um script de edição truncou este arquivo (abriu em modo `w`
> e falhou na codificação antes de escrever). Ele foi **reconstruído a partir do conteúdo
> em contexto** com todas as edições do dia reaplicadas. O conteúdo confere com a versão
> de 07/ago mais as mudanças de 18/ago, mas **se algo parecer faltando, é aqui que
> aconteceu**.

> **Feito em 21/ago/2026 (2ª rodada de revisão):** a Mariana leu o `revisao-2.pdf`
> **inteiro** e deixou **56 anotações**, as primeiras a alcançar os Caps. 5 (Reddit),
> 6 (YouTube) e 7 (TikTok). Todas foram tratadas, e o resultado é o `revisao-3.pdf`
> (64 p., compilação limpa, **zero `Overfull`** pela primeira vez). Além das reescritas,
> a rodada: (a) **tirou Instagram/Facebook da dissertação**, sem apagar o caso;
> (b) apurou que o caso do YouTube **não cobre modelagem de tópico**, abrindo uma lacuna
> declarada; (c) **rebaixou a "validação"** da atribuição de lado no caso vacinas, por
> uma dúvida da Mariana que reencontrou uma retratação já registrada no D7 do caso;
> (d) criou **2 figuras e 3 tabelas** novas e o `curva_rb3.json`; (e) preencheu **banca,
> data da defesa e bio**; (f) consertou um `\ref` quebrado que saía literal no PDF.
> Tudo em §4.18 e no mapa comentário→mudança de
> [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md). O **fluxo da revisão virou
> skill**: [`revisao-dissertacao`](.claude/skills/revisao-dissertacao/SKILL.md).

> **Feito em 21/ago/2026 (nota de atualidade no Cap. 4):** a Mariana trouxe a matéria
> da Folha/BBC sobre o levantamento Torabit do debate vacinal em ago/2026. Avaliou-se
> que **não** cabe como sétimo caso — plataforma comercial, sem lista de termos, sem
> gabarito e sem descrição do classificador, portanto **não reproduzível** — e sim como
> vinheta no Cap. 4, onde a dissertação já mediu o contrafactual: a razão pró/anti vai
> de 1,41 a 7,42 conforme o termo-índice, e o esquema binário forçado desloca a
> descrição em ~18 p.p. O levantamento publica **1,92** a partir de um termo só, o
> genérico, e descarta os 9,4% sem classificação. Aplicado em `corpo.tex`
> (`cap:caso-vacinas`, §largura do filtro) + entrada `bbc2026vacinas` no `.bib`.
> Compila em 64 p., zero `Overfull`, zero referência indefinida. Sobre a referência:
> a URL no `.bib` é a da Folha (republicação); trocar pela canônica da BBC News Brasil
> ✅ **resolvida no mesmo dia:** a entrada nasceu apontando para a republicação na
> Folha (o domínio `bbc.com` bloqueia acesso automatizado, então não dava para achar
> o original daqui), e a Mariana localizou a URL canônica da BBC News Brasil, que
> substituiu a anterior. O `xurl`, que só existia para a URL longa da Folha, foi
> removido.
> O `revisao-3.pdf` foi **republicado** com a nota, e o registro está em
> [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md), na seção *Fora do ciclo*.

> **Feito em 21/ago/2026 (1ª rodada de revisão):** a **primeira rodada de revisão da
> dissertação** foi aplicada. Os 32 comentários do `revisao-1.pdf` (pp. 6–27) viraram
> edições em `dissertacao.tex` e `corpo.tex`, e o resultado está em
> `revisoes/revisao-2.pdf`. Além das reescritas de texto, a rodada corrigiu **três erros
> factuais** apontados pela Mariana e criou as **duas primeiras figuras** da dissertação,
> a partir dos JSON congelados dos casos. ⚠ As edições foram **perdidas e reaplicadas**
> no mesmo dia, por uma sobrescrita vinda de outra sessão — ver §4.17. Mapa completo em
> [escrita/dissertacao/revisoes/REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md).

> **Feito em 22/ago/2026 (o sétimo caso, modelagem de tópico):** o caso
> [`reddit-topicos`](casos/reddit-topicos/README.md) nasceu e foi executado até o
> **Portão 1**, onde **parou**, como o prompt manda. Alvo: **Melton et al. 2021**
> (178 cit.), LDA + sentimento em 13 subreddits. (a) **Full text lido por inteiro** e
> afirmações numeradas — ⭐ o corpus analisado é **11.641** itens, não os ~18.000 do
> resumo, e o sentimento é **TextBlob**, não VADER; (b) ⭐ **os autores publicaram o
> modelo LDA ajustado** (7 saídas de pyLDAvis), congelado como gabarito e
> auto-conferido contra a Fig. 4 deles — o levantamento de alvos dava isso como
> inexistente; (c) ★ **T1 não é ranking, é afirmação de ausência**, e ela já está sob
> tensão no gabarito dos próprios autores (janeiro, k=15, traz `autism` e `microchip`):
> a ausência depende da **resolução do modelo**, o que obriga o caso a separar efeito
> de resolução de efeito de coleta; (d) **quatro divergências internas do artigo**
> registradas; (e) dimensionamento **6 de 13** — só os menores já dão **215.394 itens
> contra 11.641** (18,5×) —, travado no **rate limit** do Arctic Shift; (f) ⭐
> `NoNewNormal` **banido em 1º/set/2021**, depois da coleta do artigo. **Nada foi ao
> `corpo.tex`.** A decisão de seguir ou não é da Mariana (§3, item 9); o relatório do
> portão está em
> [PORTAO1_relatorio.md](casos/reddit-topicos/data/repl/melton2021/PORTAO1_relatorio.md).
> ⚠ De quebra, o diagnóstico do rate limit **toca o veredito do `reddit-massachs`** —
> §4.23.

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
| ⏳ **reddit-topicos, do Portão 2 em diante** | (a) **decisão da Mariana** (§3, item 9), e (b) o **dimensionamento incompleto**: 7 dos 13 subreddits — entre eles `conspiracy`, `COVID19` e `coronavirus`, os maiores — não foram medidos porque o Arctic Shift devolve `"Timeout. Maybe slow down a bit"` e exige **~5 min de silêncio** para se recuperar. O prompt do caso manda **parar, não contornar** | Pela ordem: **um teste de taxa sustentada do `posts/search` paginado** (10 min, decide entre Arctic Shift e Academic Torrents) → **consertar a sonda** para recuar em vez de dividir quando o erro for de estrangulamento → **refazer o dimensionamento** devagar → estimar disco e tempo → decisão de commit. ⭐ **medido em 22/ago, depois do relatório: COLETAR funciona onde AGREGAR falha** — `conspiracy` (o maior) entrega 5.050 comentários em 51 páginas sem falha, enquanto a agregação dele recusa até janela de 5,2 d. **A rota está aberta**; o que não vale mais a pena é dimensionar por agregação. 🔖 **onde retomar:** [RETOMAR.md](casos/reddit-topicos/RETOMAR.md) |
| ⏳ **Tabela mestre completa (Fase 4)** | Faltam as linhas do Heine (8, 9) e do stance do Ituassu (10); as do Meta Ads (13, 14) saíram do escopo em 21/ago (§4.18); a coluna *fração mínima que estabiliza* tem **3 de 10** células (4b f≈0,75; linha 1 n=100; linha 2 n≈200) | Os dados do Heine + o gabarito do stance + a coleta do Buntain (§1, item 6) + a Fase 3 do Massachs (§1, item 7) + a conta Meta (§2). ✅ Já feitos: a curva `A(volume)` do Ituassu (linhas 1–3), os full texts do Massachs e do Capozzi (07/ago) e o **ponto original do Massachs** (18/ago). A [versão parcial](casos/RESULTADOS_tabela_mestre.md), com **10 linhas fechadas**, **já existe** desde 07/ago/2026 |
| ⏳ **Stance do Ituassu (Fases 0.5→3)** | Falta **só o ato de rotular** — o kit ficou pronto em 18/ago/2026 | **320 tweets** rotulados à mão pela Mariana (~3–4 h) na planilha já sorteada e congelada; tudo o mais (validação κ, aplicação em escala, curva) é automático — §1, item 3 |
| ✅ **VPN Cloud-DI** — *destravada em 07/ago/2026; reconectada em 18/ago* | — | ⚠ **Como testar se está mesmo conectada:** o `openvpn-gui` rodando **não** significa túnel de pé (o ícone na bandeja engana). O teste certo é o adaptador **`OpenVPN TAP-Windows6`** aparecer `Up` **e** existir IP/rota `10.x`. Conectada, fica `10.8.0.68` + rota `10.50.0.0/16` via `10.8.0.1`, e as portas 22 da vm031/vm067 abrem. Subir exige **elevação**: `Start-Process ... openvpn.exe -Verb RunAs` + `vpn-fixed.ovpn` (o UAC precisa de clique). Surfshark e Fortinet, também instalados, **não** dão acesso à Cloud-DI e não interferem. **Nas consultas, use `conectar(vm="vm031")` para a coleta vacinas** — `conectar_auto` cai na vm067 |
| ◐ **meta-ads-imigracao, Fase 1** | ⚠ **A conta entrou em processo em 21/ago/2026** — a Mariana iniciou a verificação e a **Etapa 1 está em análise (~48 h)**. A tela pediu **identidade e localização, sem carta física**, o que fecha favoravelmente a incerteza que estava registrada em [FASE0 §5.1](casos/meta-ads-imigracao/data/repl/metaads2019/FASE0_descoberta.md) e mantém o cronograma. ❗ É a **Ad Library API**, não a Content Library — rota certa. | **Assim que o token existir, o primeiro comando é o teste de retenção** ([FASE0 §5.2](casos/meta-ads-imigracao/data/repl/metaads2019/FASE0_descoberta.md), comando pronto, minutos): ele decide se o corpus italiano de 2019 sobreviveu à regra de arquivamento da UE. ⛔ **O caso está fora do escopo da dissertação desde 21/ago** (§4.18) — se a retenção passar, a decisão de reabrir é da Mariana e implica reescrever o parágrafo da Meta na §2.4 do `corpo.tex`. Se falhar, a remoção fica e o sumiço do arquivo público vira achado de uma frase |
| ◐ **TikTok, Fase 1 (expansão)** | a credencial do eTC está morta — **mas a célula não depende mais disso**: a Fase 2 foi feita offline sobre o dataset publicado do PoliTok-DE | só o eixo "coletar mais" estrito segue travado; no lugar dele o caso entrega o **eixo temporal** (rechecagem em datas sucessivas), medido com o que está publicado. Ver [FASE2_politok.md](casos/tiktok/FASE2_politok.md) |
| ◐ **Front-matter da dissertação** | Falta só a **dedicatória** (hoje um texto genérico). A **epígrafe** deixou de ser pendência em 21/ago/2026: ela saiu na 3ª rodada de revisão, porque chamada vazia imprimia uma página em branco com `, .` (§4.20). Para pôr uma de volta, basta descomentar as três linhas no `dissertacao.tex` | ✅ Preenchidos em 21/ago/2026: **data da defesa** (29/set/2026), **banca** (Edward Hermann Haeusler — PUC-Rio; Ana Carolina Brito de Almeida — UERJ) e **bio**, todos vindos do *Formulário de Marcação de Defesa* em `Downloads/`. Ver [escrita/dissertacao/README.md](escrita/dissertacao/README.md) |

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
9. ⭐ **DECISÃO NOVA, DA MARIANA — o caso de modelagem de tópico continua ou vira
   próximo passo?** O caso foi **aberto e executado até o Portão 1 em 22/ago/2026**
   ([`casos/reddit-topicos/`](casos/reddit-topicos/README.md)), e **parou lá**, como o
   prompt manda. O relatório do portão, com a recomendação, está em
   [`PORTAO1_relatorio.md`](casos/reddit-topicos/data/repl/melton2021/PORTAO1_relatorio.md).
   Em uma linha: **o alvo se mostrou melhor do que o levantamento previa, e o custo
   real continua desconhecido** — o dimensionamento parou em 6 de 13 subreddits porque
   o Arctic Shift estrangula, e a bifurcação inteira do custo (Arctic Shift × Academic
   Torrents) depende de **um teste de 10 minutos** que ainda não foi feito. A
   recomendação é: rodar o teste, consertar a sonda, refazer o dimensionamento devagar,
   e **só então** trazer o commit para ela. ⚠ **Nada disso foi ao `corpo.tex`**, e
   nada vai antes da decisão. ✅ O registro anterior: **DECIDIDO pela Mariana em
   22/ago/2026: o caso vai ser aberto**, pelo prompt de
   [`casos/PROMPT_caso_topicos.md`](casos/PROMPT_caso_topicos.md). O registro de como o
   alvo foi escolhido: ⭐ **o alvo já
   estava escolhido desde 22/ago/2026**, a pedido dela na 4ª rodada (“abre a busca de
   alvo agora”): **Melton et al. 2021** (*J. Infection and Public Health* 14(10),
   **178 citações**), LDA + sentimento sobre ~18 mil posts de **13 subreddits**
   colhidos por **PRAW numa única passada** — sub-coleta do tipo “topo da listagem”,
   igual à do Buntain, e expansível por dump. A análise, as alternativas e a ressalva
   sobre o pedido “de preferência brasileiro” (não existe alvo BR que faça modelagem
   de tópico **e** tenha tração) estão em
   [`casos/ALVOS_modelagem_topicos.md`](casos/ALVOS_modelagem_topicos.md).
   **A decisão que resta é só abrir ou não, e cabe a ela.** O registro original,
   de 21/ago/2026, na 3ª rodada de revisão (comentário 16): *“acho então que a gente
   devia ir atrás de um caso com modelagem de tópico talvez reddit que é mais fácil de
   conseguir dados”*. Está em **18,8% dos artigos da revisão** (base 2.472 desde a extração completa de 15/set, só Gemini; eram 18,9% na base 2.322 e 23,0% na união; o “quarto tipo mais frequente” que se dizia aqui era falso; corrigido em 14/set) e é um dos mais frequentes sem
   caso executado — hoje declarado como limitação de cobertura e como próximo passo.
   **O instinto dela bate com o que o próprio `corpo.tex` argumenta:** o Reddit é a
   única plataforma do conjunto em que coletar mais não depende de credencial nem de
   acervo preservado (§2.4), e a infra de coleta já está montada pelos casos Buntain e
   Massachs. O próximo passo do `corpo.tex` foi reescrito nesta rodada para **nomear
   essa rota**. O que falta é decisão dela: (a) escolher um alvo publicado **com
   tração** — o critério que descartou o #207 vale aqui — que modele tópicos sobre um
   subreddit ou conjunto delimitado; e (b) decidir se cabe **antes de 29/set/2026** ou
   se fica como agenda pós-defesa.
10. **TikTok — a cota.** A credencial é do **app do eTC**, cuja cota é compartilhada com o
   crawler que roda em loop na vm031. Combinar com quem opera (o `execute_tiktok.sh` cita
   o Tomaz) ou pedir credencial própria — esta última é o que torna a Fase 1
   **reproduzível por terceiros**.
11. ⭐ **DUAS DECISÕES NOVAS, saídas da rodada 1 da survey (9/set/2026).** Nenhuma
   bloqueia a defesa; as duas mexem em número já impresso, e por isso não foram
   aplicadas sozinhas.
   ✅ **(a) FECHADA em 14/set/2026 — propagada**, na rodada 7, a pedido da Mariana
   (“vai ser a versão final então garante que tá tudo consistente nos dois arquivos”).
   O registro: **(a) Propagar a base 1.723 para o `corpo.tex`?** A survey recompilou com o banco
   atual (2.147 extraídos, 1.723 na base); o `corpo.tex` segue em 2.139/1.718. Nenhum
   achado muda — são casas decimais —, mas os dois documentos são lidos juntos e a
   `tab:analises-survey` cita a survey nominalmente. É uma passada de `grep` mais
   `audita_numeros.py`/`audita_contas.py` antes e depois. Ver §4.24.
   ✅ **(b) FECHADA em 14/set/2026, à noite — aplicada nos dois documentos:** o survey-3 passou todas as tabelas para só-Gemini e a dissertação acompanhou (rodada 8). O registro: **(b) Trocar a base da tabela de tipos de análise da união para só-Gemini?** ~~⏳ segue
   aberta; desde 14/set a dissertação também **declara** o defeito, na nota da Tab. 1.1.~~ É a
   recomendação nº 1 do
   [DIAGNOSTICO_tipos_de_analise.md](escrita/survey/expansao/DIAGNOSTICO_tipos_de_analise.md),
   nunca aplicada. Hoje o `survey-1.pdf` **declara** o defeito (ameaça nº 6, com o
   +87% medido e a tabela recomputada dentro da própria ameaça) e o `corpo.tex` não
   diz nada. Aplicar alinha os dois achados ao mesmo critério, mas mexe nas duas
   tabelas de uma vez e a 20 dias da defesa. ⛔ o mesmo diagnóstico proíbe mexer no
   `vocabulary` antes de a expansão extrair — isso **não** está em jogo aqui.
12. ⭐⛔ **A expansão do corpus: extrai os 800 ou não?** — apurado em 9/set/2026, e é
   a decisão mais consequente em aberto. Os fatos, todos conferidos:
   - a varredura **acabou** em 23/ago e recuperou **811 PDFs**; eles estão em disco;
   - os **800 sorteados** pela semente pré-registrada `20260929` **nunca foram
     extraídos** — bug de shell, não de método (§4.25). **Nada foi gasto**;
   - extrair custa **~R$43** e algumas horas, e levaria a base de **1.723 para
     ~2.360** (800 × os ~80% que de fato coletam RSD) — um **+37%**;
   - ⛔ **mas a condição de parada pré-registrada disparou**: o estrato pago fechou
     em **7,7%**, com o IC95% inteiro abaixo do piso de 11%. O
     [PRE_REGISTRO](escrita/survey/expansao/PRE_REGISTRO_expansao.md) §8 manda
     **parar** e transformar o trabalho numa nota de método.

   **A tensão é real e não se resolve sozinha:** a parada foi escrita contra a
   *extrapolação* (``vale a pena varrer 11 mil artigos?''), e a varredura já
   aconteceu — os 811 existem independentemente de a taxa ter frustrado. Extrair
   agora não viola a aposta sobre a taxa; viola a **letra** da condição de parada.
   Só a Mariana decide se o pré-registro se aplica a este passo, e a decisão precisa
   ficar **escrita** — um pré-registro contornado em silêncio vale menos que nenhum.
   ⚠ Seja qual for a decisão, ela **não** muda o `survey-1.pdf`, que já reporta a
   taxa final medida como ameaça à validade.
   ✅ **FECHADO em 9/set/2026.** A Mariana mandou levar os 800 adiante; o adendo de
   decisão foi escrito **antes** da execução
   ([PRE_REGISTRO §11](escrita/survey/expansao/PRE_REGISTRO_expansao.md)). A extração
   rodou 08:47→14:42, **761 OK / 28 falhas** (3,5%), ≈R$43 — dentro do teto. Conferido
   contra o banco, não contra o código de saída: **+764 persistidos**, base de
   caracterização **1.723 → 2.322**.
   ⭐ **Resultado, em [RESULTADOS_expansao.md](escrita/survey/expansao/RESULTADOS_expansao.md):**
   a aposta central **acertou** — amostragem (18,7→18,9%) e filtragem (80,3→81,1%)
   **não se movem**, e o estrato antes inacessível não difere neles. *O achado central
   da survey não era artefato de viés de acesso.*
   ❌ **As três apostas de direção falharam, todas ao contrário**: Twitter **sobe** 5
   p.p. no estrato novo (previa queda), mediana **2,8×** maior (previa queda), fração
   abaixo de 1 mi **cai** 8,6 p.p. (previa alta). A intuição sobre quem está atrás do
   paywall estava invertida; a explicação fica **em aberto**.
   ⭐ **Um número do artigo muda:** DOI persistente **8,3% → 6,8%** (único a disparar o
   critério 1; o estrato fechado publica 3× menos, 2,6%) — e na direção que **reforça**
   o argumento de reprodutibilidade.
13. ~~**Rodar o proxy institucional na Springer?**~~ — ❌ **RESPONDIDA E FECHADA em
   9/set/2026, e a resposta é não porque não dá.** A Mariana autorizou a rota lenta
   ("está OK expandir mais se for feito com cuidado"). O cuidado foi construído
   primeiro — [`proxy_springer.py`](escrita/survey/expansao/proxy_springer.py), com
   parada dura em bloqueio, sequencial, sem tocar no banco — e **foi ele que achou o
   problema no piloto de 10**: a Springer devolve **HTTP 200 com 3 KB de "Client
   Challenge"** no endpoint do PDF. Confirmado em 4 DOIs diversos (periódico e
   capítulo, 2015–2022), resposta byte a byte idêntica.
   **A rota do proxy está fechada por inteiro:** ACM, Elsevier, SAGE, T&F, Emerald e
   Wiley já bloqueavam; IEEE fechou entre mai e ago/2026; Springer, até set/2026. Os
   ~2.000 artigos que pareciam folga **não são alcançáveis**. Detalhe em
   [EXPANSAO_recuperacao.md §4b](escrita/survey/EXPANSAO_recuperacao.md).
   ⛔ O `curl_cffi`/Playwright previsto no `PROXIMAS_ETAPAS.md` do repo da survey
   **não foi implementado, por decisão**: forjar *fingerprint* de navegador é
   contornar um controle anti-automação, não usar uma assinatura — e a conta cairia
   sobre o acesso da PUC-Rio inteira.
   ✅ **O saldo é positivo mesmo assim:** virou achado do artigo. A ameaça à validade
   nº 2 passou a dizer que o estrato comercial é um **limite estrutural** para
   levantamentos em escala, e não um custo que uma instituição possa pagar.
   ⭐ **E abriu uma sonda que a Mariana executou no mesmo dia.** Com o PAC da DBD
   ativo no navegador — acesso por **IP**, não por login —, ela baixou **199 de 200**
   periódicos Springer à mão (~1 h), contra **7,7%** das rotas abertas. ⛔ Mas **0
   de 5 anais LNCS**: a PUC-Rio assina os periódicos e não os anais, o que deixa
   **1.492 artigos** do corpus inalcançáveis *mesmo pagando*. Ferramenta em
   [`sonda_springer.py`](escrita/survey/expansao/sonda_springer.py); retomada em
   [`expansao/RETOMAR.md`](escrita/survey/expansao/RETOMAR.md).

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

### 4.17 ⚠ Duas sessões escreveram no mesmo `corpo.tex` — **resolvido em 21/ago/2026**

Registro para não repetir. Em 21/ago, uma sessão que trabalhava na cópia
`Documents/dissertacao/` sincronizou seu `escrita/dissertacao/corpo.tex` **por cima**
do versionado em `Documents/GitHub/dissertacao-mestrado/`, apagando as **29 edições**
que a rodada de revisão-1 tinha acabado de aplicar (as 32 anotações da Mariana),
inclusive os dois `\includegraphics` das figuras novas. Não havia backup pós-revisão.

- **Resolução:** as 29 edições foram **reaplicadas** sobre o `corpo.tex` novo, em vez de
  restaurar a versão antiga — assim o capítulo de Reddit e a correção do cap. do YouTube
  se preservaram. Colisões resolvidas: a contagem da Conclusão ficou em "**Cinco** deles
  já foram executados" (deles) com a formulação da revisão ("casos replicáveis,
  distribuídos por cinco redes"); a `tab:casos` foi reordenada por capítulo, já que
  Reddit passou a ser caso executado; a métrica de papéis sociais passou a apontar para
  `cap:caso-reddit`.
- **De passagem:** a cópia sobrescrita veio com **CRLF**; o arquivo foi renormalizado
  para **LF**, que é a convenção do repositório.
- **Combinado:** `Documents/GitHub/dissertacao-mestrado/escrita/` é território de quem
  edita a redação; a outra frente sincroniza apenas `casos/`. **Nunca copiar arquivo
  inteiro por cima** — editar no lugar ou avisar antes.

### 4.16 ⚠ Circularidade do caso YouTube: a conclusão fica, **o mecanismo muda** (21/ago/2026)

O `corpo.tex` afirmava, como *"a afirmação mais forte que este capítulo faz sobre o
trabalho replicado"*, que o filtro de palavra-chave do AGECovP institucionaliza o corpus,
apoiando-se em **+7,9 p.p.** de conteúdo de usuário entre os descartados. Esse número
vinha da coleta parcial (50/85 buscas) e da caracterização de canais limitada ao gabarito
dos autores.

Com a **coleta completa** (85/85) e os **2.165 canais buscados pela API** (cobertura de
100%, o que a própria [FASE3 §6.4](casos/youtube-agecovp/data/repl/agecovp2020/FASE3_efeito_filtro.md)
pedia), o sinal **se inverte com significância**: −6,4 p.p., IC95% [−11,4; −1,4]. A
predição P1 **falha**.

⚠ **A causa da inversão não é a que a §6.4 supunha.** A hipótese registrada era viés de
cobertura do gabarito; medida, ela não se sustenta (64,3% × 64,7%, razão 0,99×). Também
não é a fonte dos inscritos (27,0% × 24,5% na mesma subamostra). É **quais canais entram
na base**: os 36% que o gabarito não tem são muito mais de usuário comum.

**O que substitui P1 é maior.** Entre os 1.615 vídeos no tema que as mesmas buscas
devolvem, os canais que terminaram no corpus publicado são **23,5%** UGC contra **61,7%**
dos que ficaram de fora — Δ **+38,3 p.p.**, IC95% [+33,5; +43,0], com mediana de inscritos
de **199.000 × 1.070**. A conclusão do capítulo (a explicação do artigo é parcialmente
circular) **sai reforçada**; o que cai é a **atribuição do mecanismo**, porque dentro de
cada estrato o filtro quase não age e age ao contrário (−3,5 e −11,1 p.p.).

**Corrigido na mesma sessão** no `corpo.tex` (capítulo do YouTube e conclusão), na
[FASE3 §7](casos/youtube-agecovp/data/repl/agecovp2020/FASE3_efeito_filtro.md), no
[README do caso](casos/youtube-agecovp/README.md) e na linha 15 da
[tabela mestre](casos/RESULTADOS_tabela_mestre.md). **Nenhum número antigo sobrou** —
conferido por `grep` em `.md` e `.tex`.

⚠ **Fica uma pendência de leitura para a Mariana:** o capítulo agora afirma que o efeito
de seleção existe e é grande, mas que **o passo do funil responsável não foi isolado**.
É uma afirmação mais honesta e mais fraca em atribuição causal do que a anterior, e vale
conferir se ela sustenta o peso que o capítulo lhe dá.

---

### 4.18 ✅ A 2ª rodada de revisão mudou o escopo do trabalho (21/ago/2026)

A Mariana comentou o `revisao-2.pdf` inteiro (**56 anotações**). A maior parte virou
reescrita de texto, mapeada em
[REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md); três comentários, porém,
mudaram **o que a dissertação é**, e não só como ela está escrita.

**(a) Instagram/Facebook saiu do conjunto de casos.** Comentários 24 e 25: *"acho que a
gente vai acabar não usando instagram e facebook, trate a dissertação sem incluir isso"*
e *"vê se tudo isso está bem documentado antes de tirar (…) caso seja decidido que vai
voltar então vai voltar"*. O conjunto passou de **7 casos em 5 redes** para **6 casos em
4 redes**. No `corpo.tex`, a §2.4 passou a tratar a Meta como **rota fechada** (uma linha
argumentativa: CrowdTangle desligado, Content Library paga e sem exportação, Ad Library
restrita a publicidade e portanto não comparável), e não como caso pendente. **Nada foi
apagado**: `casos/meta-ads-imigracao/` ganhou aviso de escopo no topo do README, as
linhas 13 e 14 da tabela mestre estão marcadas ⛔ em vez de ⏳, e os *próximos passos*
preveem reabrir a célula se a rota voltar.

**(b) A `tab:casos` afirmava que o caso do YouTube cobre modelagem de tópico. Não
cobre.** A reescrita da §2.3 (comentários 19 e 20, que pediam uma seção de métricas menos
técnica e ligada ao que foi de fato feito) obrigou a listar caso a caso o que se comparou,
e aí a divergência apareceu: o caso entrega **sentimento (AG1/AG2) e composição do
corpus**, e não modelagem de tópico. A linha foi corrigida. Consequência: **modelagem de
tópico é hoje o tipo mais frequente do levantamento sem caso executado** (4º lugar, 19,1%),
e a lacuna virou limitação de cobertura declarada + item de próximos passos. O caso
`heine-xande`, se destravar, a preenche.

**(c) A "validação" da atribuição de lado no caso vacinas foi rebaixada.** Comentário 35,
sobre a frase *"o artigo rotulou esses autores lendo o que escreveram"*: *"será? porque eu
acho que a comunidade importou para essa classificação"*. Ela é **coautora do artigo**, e
tem razão — e a dúvida reencontrou uma **retratação que já estava escrita** em
[DECISOES_ROTULADOR.md](casos/vacinas/data/repl/vacinas2022/DECISOES_ROTULADOR.md) §D7:
a Tabela 1 do artigo classifica **por comunidade do autor**, não por conteúdo. Os dois
caminhos não são independentes, então a coincidência de 0,3 p.p. deixou de ser
"validação da regra" e passou a ser **consistência de convenção**; o peso do argumento
migrou para a triangulação com o eixo de conteúdo, que é instrumento de fato independente.
⚠ **Lição transferível, e já registrada no D7:** proximidade numérica entre grandezas de
construtos diferentes não é evidência de que medem a mesma coisa. O `corpo.tex` tinha
reintroduzido o erro que o `.md` do caso já havia corrigido.

**Correção de erro achada de passagem:** um `\ref` da conclusão tinha perdido a
contrabarra numa sessão anterior e saía literal no PDF (`Capítulo ef{cap:caso-reddit}`).
A causa provável — substituir LaTeX por `sed`/heredoc — está registrada na skill
[`revisao-dissertacao`](.claude/skills/revisao-dissertacao/SKILL.md), junto com o
padrão seguro (script Python com `assert` de ocorrência única).

### 4.19 ⚠ Auditoria automática das estatísticas do `corpo.tex` (21/ago/2026)

Toda estatística da dissertação passou por uma auditoria mecânica, agora versionada em
dois scripts complementares em `escrita/dissertacao/` (ver o
[README](escrita/dissertacao/README.md) da pasta):

- **`audita_contas.py`** (novo) — *a conta fecha?* Não conhece os dados: confere o texto
  contra ele mesmo (deltas, pares que somam 100, ICs que contêm a estimativa, razões,
  linhas de tabela contra o `N` da legenda, sanidade de %/κ/p) e, na camada de
  **procedência**, diz quais números do texto não se ligam a nenhum JSON congelado.
  **99 checagens: 0 erro aritmético.**
- **`audita_numeros.py`** (ampliado de 49 para **72** checagens) — *o número bate com o
  dado?* Passou a cobrir AV1, AV4, a rede do caso vacinas, o stance por limiar e o ponto
  original do Massachs. **69 encontrados, 3 ausentes** — e as 3 ausências são o achado (a).

**(a) ⚠ AV4 do caso vacinas: a dissertação e a tabela mestre contam histórias
diferentes.** O `corpo.tex` diz que a concentração do top-10 *"se reproduz ao decimal"* e
que no corpus completo *"cai para 9,3%… um em cada onze retuítes de um corpus de 4,5
milhões"*. Esses valores vêm da **Fase 2**, medida sobre o suplemento do próprio artigo
([FASE2_replicacao_ponto.md](casos/vacinas/data/repl/vacinas2022/FASE2_replicacao_ponto.md)
§AV4: 374.531/2.383.643 e 9,3% sobre 4.507.889 RTs). Mas a medição **congelada em JSON** é
a da Fase 3, sobre o nosso instantâneo
([av4_lorenz.json](casos/vacinas/data/repl/vacinas2022/av4_lorenz.json)): **15,3%** no
corte >500 RT (0,4 p.p. do artigo) e **9,7%** sobre **4.599.451** RTs. A
[tabela mestre](casos/RESULTADOS_tabela_mestre.md) (linha 5) já usa o par **15,3% → 9,7%**.
São duas medições legítimas de bases diferentes, nunca reconciliadas; pela regra do
[CLAUDE.md](CLAUDE.md) §6 (os dados vencem) o texto deveria usar a série congelada — e aí
*"um em cada onze"* vira **um em cada dez** e *"4,5 milhões"* vira **4,6 milhões**.
📌 **Espera decisão da Mariana**, porque a frase *"reproduz ao decimal"* só é verdadeira na
base do artigo.

**(b) ⚠ Erro de objeto no Cap. 6 (YouTube).** A `tab:youtube-ponto` do `corpo.tex` chama a
linha de *"Distribuição de sentimento **dos vídeos**"*. A medição é de **comentários**: o
`analise/fase2_ponto_original.py` lê `comments.csv`, a
[FASE0](casos/youtube-agecovp/data/repl/agecovp2020/FASE0_descoberta.md) e a
[FASE2](casos/youtube-agecovp/data/repl/agecovp2020/FASE2_ponto_original.md) chamam AG1 de
*"sentimento dos comentários"*, e o próprio script registra a ressalva de que **o gabarito
não traz sentimento de vídeo nenhum** — logo essa distribuição não teria como ser
reproduzida. Os 59%/72% que o texto atribui aos vídeos são a afirmação **do artigo**, e
são outro objeto que os 39/39/22 do AG1. **É correção de uma palavra, e vale a pena.**

**(c) Contagem menor, no mesmo capítulo:** o texto diz que *"as outras **duas** convenções
plausíveis erram de 27 a 75 p.p."*; a FASE2 testou **quatro** convenções, das quais **três**
erram (26,8 · 70,8 · 74,5 p.p.).

**(d) Números sem fonte reexecutável** (não são erros; são o princípio de rastreabilidade
do [CLAUDE.md](CLAUDE.md) §7 ainda não fechado). Em 271 números distintos do `corpo.tex`,
**17 não têm fonte nenhuma neste repositório** e **12 só existem em `.md` de caso**:
  - ~~a **`tab:tiktok-temporal`** publica a série 6,3% → 17,3% → 18,7%, mas o
    `fase2_politok.json` só congela a *outra* série (3,3/9,5/18,7)~~ — ✅ **resolvido
    em 22/ago/2026, e era pior do que parecia:** a série publicada **misturava bases**
    (dois pontos dos rechecados, um da coleção inteira). O `fase2_politok.py` ganhou o
    bloco `painel_temporal`, que congela **as três** séries, e o `corpo.tex` passou a
    publicar a do **painel** (6,3 → 17,4 → 20,9). Ver §4.22;
  - os testes do Cap. 3 (79.603 tweets, *z*=188,3, IC de Wilson 83,1–83,6 e 35,6–36,6,
    *z*=−49,9, 1.752 autores, OR 2,91 com IC 2,63–3,23) só existem em `.md`; o
    `curva_midia.json` não os guarda;
  - os números da **revisão** (13.395 · 3.107 · 635 · 2.472 · 3.109 · 2.179 · 1.376 · 64,8 · 18,8 · 80,3 · ≈340 mil, na base da extração completa de 15/set, e a
    `tab:analises-survey` inteira) vêm do `research.db`, que mora em outro repositório —
    limitação conhecida, não defeito;
  - ⚠ os do **levantamento da Torabit/BBC** (65,8% · 34,2% · razão 1,92 e sobretudo os
    **9,4% sem classificação**) não têm fonte aqui, e o próprio `.bib` só registra as
    93.755 publicações e o período. O **9,4%** coincide exatamente com a fatia sem-lado da
    réplica no mesmo capítulo — **conferir na matéria** antes da defesa.

**O que passou.** As demais contas fecham, inclusive as que valia a pena duvidar: a
`tab:analises-survey` inteira contra *N*=2.139; o funil do YouTube (3.353+1.025=4.378, e
os descartes de 52/99/14%); os três recortes da `tab:reddit-rb3`; os deltas de −6,4 e
+38,3 p.p. e seus ICs; a razão 62,6% = 58,8/(58,8+35,1) e a de 61,7% no esquema de três
classes; as 14 categorias de enquadramento; as pontas do Massachs (34,6/26,8 e o fator de
quatro sem reponderação); e as datas do TikTok (31, 100 e 134 dias após 01/set/2024).

### 4.20 ⚠ O `thesispuc.cls` tem um `\fi` faltando — **corrigido em 21/ago/2026**

Descoberto na 3ª rodada de revisão, ao atender o pedido de tirar a página de epígrafe
vazia (a p. 12 do `revisao-3.pdf` saía com o conteúdo literal `, .`).

Em `\puc@showfrontmatter` (linha 1587 da classe), o `\if@pucepigraph` **não tem
`\fi`**. O único `\fi` ali perto pertence ao `\if@puctight` que vem depois.
Consequência, conforme a epígrafe esteja ligada ou não:

- **ligada** (como estava até o `revisao-3.pdf`): o `\if` fica pendente e é absorvido
  adiante sem dano visível. Foi por isso que ninguém viu o bug em três rodadas;
- **desligada**: o TeX sai **pulando** à procura do fecho que falta e engole
  `\puc@setmargins@text`, `\onehalfspacing`, `\rmfamily`, `\puc@setpagestyle`
  e o próprio `\begin{document}` — erro *“Can be used only in preamble”* e o
  documento caindo para **56 p.** sem espaçamento um e meio.

O `\fi` foi acrescentado, com comentário no lugar. ⚠ **A cópia deste repositório
passou a diferir da classe oficial da PUC-Rio em uma linha.** Se a versão final tiver
de sair com a classe intocada, o caminho é reverter essa linha **e** voltar a chamar
`\epigraph` — com uma epígrafe de verdade, ou a página em branco volta. ❗ **Decisão
da Mariana**, sem urgência.

### 4.21 ⚠ O medidor da expansão apagava a variável que media (22/ago/2026)

O `escrita/survey/expansao/taxa_recuperacao.py` imprimiu, com todas as letras,
`!! PARAR: estrato pago em 0.0%, abaixo do piso de 11%` — a condição de parada
pré-registrada da expansão, disparada por um número que não existe. Duas causas,
as duas corrigidas no mesmo dia:

1. **O estrato vinha da coluna `pdf_inaccessible`**, que o `retry_pdfs` e o
   `reconcilia_pdfs` reescrevem a cada sucesso (`True` → `False`). Um artigo pago
   recuperado **saía do estrato pago no instante em que era recuperado**, então a
   taxa daquele estrato só podia dar 0,0%. O `expansao/README.md` já documentava a
   armadilha ("o ato de medir apaga a variável pela qual se mede") — o medidor era
   anterior ao `estratos.json` e ficou para trás. Agora lê o rótulo congelado.
2. **O denominador era a fila inteira**, mas a varredura cobriu 34% dela. Isso
   mede **cobertura**, não taxa. Agora o denominador é o conjunto **tentado**,
   lido dos logs, e a fila inteira aparece rotulada como cobertura.

Corrigido, o estrato pago mede **12,4%** (412/3.321, IC95% 11,3–13,6) — coerente
com os 13,25% do lote pré-registrado de 400 e acima do piso. Nada havia parado; o
que quase parou foi um artefato de leitura.

⚠ **Vale como lição de método, não só como bug:** é a terceira vez que este
projeto encontra a mesma classe de erro — o instrumento de medida interferindo na
grandeza medida (as outras duas estão em [EXPANSAO_recuperacao.md](escrita/survey/EXPANSAO_recuperacao.md)
§5 e §5b, ambas sobre a ordem da fila).

---

### 4.22 ★ O Cap. do TikTok reivindicava um achado que é do artigo-alvo (22/ago/2026)

Descoberto ao atender o comentário 17 da 4ª rodada de revisão — *“mas aí o que a gente
está fazendo de diferente do que o próprio artigo já mostra?”*. A dúvida estava certa, e
cobrar a resposta obrigou a ler o full text do PoliTok-DE, que até então só tinha sido
lido pelo resumo e pelos dados.

**O que se achou.** O artigo traz, no **Apêndice C, Tabela 5**, um **painel dos mesmos
102.953 posts** da Saxônia rechecados a 1, 3 e 4,5 meses — 6,3% / 17,4% / 20,5% — e
afirma no corpo que *the deleted share grows the longer we wait*. O eixo temporal, que o
capítulo apresentava como “o achado próprio deste caso”, **está no alvo**.

**Duas consequências piores que a primeira.**

1. **A série publicada misturava bases.** A `tab:tiktok-temporal` trazia
   6,3% → 17,3% → 18,7%: os dois primeiros pontos vinham dos posts efetivamente
   rechecados naquela data, e o terceiro, da coleção inteira (195.373). Denominador
   diferente em cada ponto não é curva. O painel estrito (estado válido nas três datas,
   **n = 100.926**) dá **6,3% → 17,4% → 20,9%** e reproduz o do artigo a 0,4 p.p. no
   último ponto — diferença atribuível ao tratamento dos `UNKNOWN_ERROR`, que o artigo
   não declara (mais uma convenção não publicada, a terceira só neste caso).
2. **“Sobe rápido e assenta” não se sustenta.** A coleta federal do mesmo artigo,
   verificada uma única vez aos **16 meses**, marca **39,7%** — quase o dobro dos 20,9%
   da estadual aos 4,5 meses. Ou as duas não são comparáveis (e o artigo avisa que não
   as compara diretamente, por terem horizontes distintos), ou a curva temporal não havia
   assentado. **Convergência no eixo temporal: em aberto**, na tabela mestre e no texto.

**O que ficou.** O caso continua no conjunto, e a §8.3 foi reescrita para reivindicar
apenas o que é dele: (i) a verificação independente do painel; (ii) o diagnóstico da base
misturada, que é uma armadilha do próprio protocolo aplicada a ele mesmo; (iii) a
**incorporação do eixo ao protocolo**, com as perguntas mudou?/convergiu? aplicadas ao
tempo — que é o que de fato é novo. O `fase2_politok.py` ganhou o bloco
`painel_temporal` com as três séries; `FASE2_politok.md`, `RESULTADOS_tabela_mestre.md`
e o `CLAUDE.md` da raiz foram corrigidos.

**Lição de processo, e ela dói:** o caso foi fechado em 19/ago sobre os *dados*
publicados sem que o *texto* do alvo tivesse sido lido por inteiro. É exatamente a falha
que a Fase 0 do protocolo existe para impedir, e ela passou porque os dados estavam
disponíveis e o artigo parecia dispensável.

### 4.23 ⚠ A mensagem de erro do Arctic Shift conflaciona duas causas — e isso toca o `reddit-massachs` (22/ago/2026)

Descoberto ao dimensionar o caso novo [`reddit-topicos`](casos/reddit-topicos/README.md).
O endpoint de agregação do Arctic Shift responde `{"data":null,"error":"Timeout. Maybe
slow down a bit"}` em **dois** casos que a mensagem não distingue:

1. **Estrangulamento por taxa.** `antivaccine` (222 submissões em 5,5 meses — consulta
   trivial) **falhou** durante uso intenso e **respondeu normalmente após ~5 min de
   silêncio**. Medido: 30 s e 120 s de silêncio não bastam; 300 s bastam.
2. **Tamanho real da consulta.** `conspiracy` na janela de 166 dias **falhou em 14 s
   mesmo após 5 min de silêncio total**.

**Por que importa além do caso novo.** A Fase 3 do
[`reddit-massachs`](casos/reddit-massachs/README.md) foi declarada *não dimensionável*
porque "34/34 agregações voltaram incompletas" — **com esta mesma mensagem**. Uma sonda
que insiste rápido produz falhas de estrangulamento que **parecem** falhas de tamanho, e
a sonda de lá consultava mês a mês em sequência, sem recuo.

⚠ **Isto não derruba o veredito do Massachs.** Os subreddits de lá (`politics`, `news`,
`worldnews`) são grandes, e para grandes a falha é real — foi o que `conspiracy` mostrou.
Mas o "34/34" pode estar **inflado** por estrangulamento, e o veredito merece uma
**reconferência paciente** antes de virar afirmação definitiva na dissertação. Hoje o
`corpo.tex` diz que a expansão do Massachs não é dimensionável pela API; se a
reconferência mudar isso, o texto muda junto.

**Efeito colateral no desenho de sonda:** dividir o intervalo ao meio quando a causa é
estrangulamento **agrava** o problema (mais chamadas). Visível nos logs do caso novo: a
mesma contagem de `Vaccines` custou 4 chamadas numa rodada e **16** na seguinte. O
conserto é recuar-e-repetir quando a mensagem for de taxa, e só dividir quando o
intervalo grande falhar **depois** de um recuo longo.

### 4.24 ✅ ~~A survey recompilou na base **1.723**; o `corpo.tex` segue em **1.718**~~ (9/set/2026) — resolvida em 14/set/2026

> ✅ **Resolvida na rodada 7 (14/set/2026).** O `corpo.tex` passou a 2.147/424/1.723, e
> a `tab:analises-survey` virou a Tab. 3 da survey. De passagem apareceram, e foram
> corrigidas, quatro divergências que esta seção não listava: o **acesso** (a
> dissertação dizia que o *proxy* institucional contribuiu PDFs; a survey diz que não
> foi usado em escala), a **extração** (“três modelos” × dois retidos), o **Twitter**
> (“54,5% do levantamento” é o catálogo DBLP; a base dá 63,7%) e a **modelagem de
> tópico** (“quarto tipo mais frequente”, falso nas duas tabelas). A segunda
> divergência abaixo (recomendação nº 1) segue de pé, mas os dois documentos agora a
> declaram. Mapa em
> [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md). O texto abaixo é o registro.

O `survey.tex` foi recomputado contra o `research.db` atual e todos os seus números
subiram um degrau, porque o **piloto de 5 artigos** da expansão (§item 12 da §1)
entrou no banco: **2.139 → 2.147** extraídos, **421 → 424** descartados,
**1.718 → 1.723** na base de caracterização. Os deslocamentos são de casas decimais
(Twitter 1.095 → 1.097; API 1.198 → 1.200; volume legível 1.518 → 1.522; ``análise de
conteúdo'' 1.040 → 1.045), e **nenhum achado se move**: amostragem 18,7%, filtragem
80,3% e os 339 grandes coletores são idênticos.

O `corpo.tex` **não** foi tocado e continua citando 2.139/1.718, inclusive na
`tab:analises-survey`. Como os dois documentos são hoje lidos juntos, a divergência
fica registrada aqui. **Corrigir é uma passada de `grep`**, mas mexe em números de
abertura da dissertação a 20 dias da defesa — é decisão da Mariana (§3).

⚠ Uma segunda divergência, mais antiga, **continua de pé nos dois documentos**: a
recomendação nº 1 do
[DIAGNOSTICO_tipos_de_analise.md](escrita/survey/expansao/DIAGNOSTICO_tipos_de_analise.md)
— reportar tipos de análise só pelo Gemini — **não foi aplicada em lugar nenhum**. O
`survey-1.pdf` passou a **declarar** o problema como ameaça à validade, com a medida
(+87% de rótulos por artigo entre os 732 duplamente lidos) e com a tabela recomputada
só pelo Gemini dentro da própria ameaça; o `corpo.tex` ainda não diz nada. Aplicar a
recomendação mudaria as duas tabelas de uma vez.

### 4.25 ⚠ A taxa de recuperação da expansão caiu de 12,4% para **7,7%** no censo completo (9/set/2026)

Terceiro artefato de medição da mesma frente, e o primeiro que empurra o número
**para cima** — o que é pior, porque otimismo não dispara desconfiança.

A varredura fechou em 23/ago com a fila **100% tentada** (11.093). O resultado
final, por `taxa_recuperacao.py` sobre o `estratos.json`: **7,7%** no estrato pago
(772/10.039, IC95% 7,2–8,2) e 7,3% no total (811/11.093). A medição intermediária,
feita a 34% da fila, dizia **12,4%** (IC95% 11,3–13,6). **Os dois intervalos não se
sobrepõem**, então não é flutuação amostral — e, com `--shuffle`, qualquer prefixo
da fila deveria ser amostra não enviesada dela.

**Hipótese**, ainda por conferir: a contagem intermediária foi feita logo depois de
o `reconcilia_pdfs` trazer **307 PDFs órfãos do disco**, recuperados por execuções
anteriores em **outra ordem** — inclusive a primeira, em `order_by(id)`. Eles
entraram no numerador sem que seus denominadores estivessem no conjunto tentado
daquela medição. ⚠ **Confirmar antes de o 7,7% virar número final em outro lugar.**

**Onde o número velho já estava impresso, e o que foi feito:** o
`revisoes/survey-1.pdf` foi publicado horas antes, na mesma sessão, citando os
12,4% e uma projeção de ~830 artigos. **Corrigido e republicado no mesmo dia** — a
ameaça à validade nº 3 do artigo passou a ser um **censo** (11.093 tentados, 811
recuperados) em vez de uma projeção, o que a deixa mais forte, e a medição
intermediária virou nota de rodapé. Fora do `survey.tex`, o número velho ainda
aparece em `EXPANSAO_recuperacao.md` §3b e no `expansao/README.md`, **de propósito**:
lá ele é o registro histórico da execução, e §3c o supera explicitamente.

### 4.26 ⛔ A extração da expansão falhou em silêncio por 17 dias (9/set/2026)

O `extrai_apos_varredura.sh` esperou a varredura, sorteou os 800 e **não extraiu
nenhum**: o script interpola o caminho da amostra em formato Windows
(`C:\Users\...`) dentro de um `$(python -c ...)` executado pelo **bash**, que o
entrega como `/c/Users/...`; o Python do Windows não abre, `--ids` fica vazio e o
`analyze_pdfs` aborta.

⚠ **O laço registrou `codigo 0`** — sucesso — porque leu o `$?` do último comando
do bloco, e não o do `analyze_pdfs`. O log termina com uma linha de sucesso sobre
um fracasso, que é a razão de ninguém ter percebido.

**Consequência:** nada foi gasto, os 800 seguem sorteados e válidos, e **962 PDFs
estão em disco sem extração**. O conserto do comando está em
[EXPANSAO_recuperacao.md §7](escrita/survey/EXPANSAO_recuperacao.md); rodar ou não
é decisão da Mariana (§3, item 12).

### 4.27 ⭐ O proxy institucional NUNCA foi usado em escala — e os "43%" são capacidade, não coleta (9/set/2026)

Apurado a pedido da Mariana, que lembrava de o proxy ter sido usado. **A memória
está meio certa: a capacidade foi construída, a coleta não aconteceu.**

O que de fato existe, por `documentacao/METODOLOGIA.md` §5.6 e
`PROXIMAS_ETAPAS.md`: em **26/mai/2026** foram implementados
`fetch_pdf_via_proxy()`, a flag `--via-proxy` e o `--doi-prefix`, mais um **teste
de fumaça em 10 DOIs** (1 por editora). O item aparece como **"Concluído"** — e é,
mas o que concluiu foi a *implementação*.

⚠ **Os "≈43% do paywall" são o conjunto endereçável, não o recuperado**: Springer
2.245 + IEEE 2.117 = 4.362 dos 10.229 pagos são as editoras que o proxy consegue
tecnicamente alcançar. Nenhuma varredura em massa foi rodada sobre elas.

**Medido no banco em 9/set/2026**, sobre os 4.356 artigos pagos dessas duas
editoras: apenas **157 (3,6%)** tinham PDF antes da expansão — e mesmo esses são
compatíveis com rota aberta (preprint em arXiv de artigo Springer, etc.), não com
colheita via proxy. Se a varredura tivesse rodado, o número estaria perto de 4.356.

**Onde o número errado estava impresso, e o que foi feito:** o `survey.tex` dizia
que *"um acesso institucional via proxy recupera adicionalmente parte de Springer e
IEEE (≈43% do paywall alcançável), totalizando 2.298 PDFs obtidos"* — o que dá a
entender uma contribuição que não houve. **Corrigido e republicado no mesmo dia**
(3ª republicação do `survey-1.pdf`): a Metodologia passou a dizer que **todos os
3.109 PDFs vêm de rotas abertas e gratuitas** e que o proxy foi implementado,
testado e **deliberadamente não usado em escala**; a ameaça à validade nº 2 passou a
descrever o viés por **política de depósito da editora** (Emerald, T&F e Wiley
abaixo de 5%; ACM 8,9%) em vez de por catálogo de assinaturas. O artigo fica mais
forte: o viés de cobertura é nítido, e não misturado a licença comercial.

⚠ **A folga que isso parecia abrir NÃO existe** — apurado horas depois, no mesmo dia
(§3, item 13). Os ~2.000 artigos da Springer não são alcançáveis: ela devolve HTTP
**200 com 3 KB de "Client Challenge"** no endpoint do PDF, e a linha "Springer 200"
do diagnóstico de agosto media a *landing page*, não o PDF. Com IEEE (202 vazio
desde ago) e as demais já bloqueadas, **não sobrou editora colhível por automação**.
O proxy nunca foi usado em escala e agora não pode mais ser.

---

### 4.28 ✅ ~~A survey foi para a base 2.322 e só-Gemini; a dissertação ficou em 1.723 e união~~ (14/set/2026, noite) — resolvida na mesma noite

> ✅ **Resolvida na rodada 8 (`revisao-8.pdf`), a pedido da Mariana** (“garante que a última
> versão da dissertação tá batendo com a última versão da survey”). Tudo o que está listado
> abaixo foi alinhado, e conferido contra o `numeros.json` do survey-3. Apareceu ainda uma
> divergência de **afirmação**, que esta seção não listava: a dissertação citava a revisão
> como prova de que “quase nunca se avalia” o efeito do volume (Resumo, §1.1, §1.2 e
> Conclusão), e o survey-3 deixou de afirmar isso por nenhum campo da extração o medir
> (ameaça nº 8). A dissertação passou a atribuir à revisão só o que ela mede (o recorte:
> 81,1% filtram, 18,9% amostram) e a apresentar a verificação como o que o protocolo mede.
> A “inflexão em 2023” **não aparece** no `corpo.tex`. Mapa em
> [REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md). O texto abaixo é o registro.


A rodada 3 da survey ([`survey-3.pdf`](escrita/survey/revisoes/survey-3.pdf)) trocou a
base (1.723 → 2.322, com a expansão) e o critério das tabelas (união → só-Gemini). A
dissertação tinha sido alinhada à rodada 2 **no mesmo dia** (`revisao-7.pdf`), e por isso
diverge de novo: a Tab. 1.1 (= Tab. 3 antiga da survey), Twitter 63,7% → **64,9%**,
amostragem/filtragem 18,7/80,3 → **18,9/81,1**, 339 → **469** grandes coletores, e a
ordem dos tipos de análise (sentimento cai de 2º para 3º). **Nenhum achado muda de
direção.** O `corpo.tex` não foi tocado — decisão da Mariana se e quando alinhar. A
série do Twitter também muda de leitura: sem os preprints do arXiv, a inflexão é em
**2025**, e não em 2023; se o `corpo.tex` repete a “inflexão em 2023”, vale conferir.

## 5. Estado por frente (uma linha cada)

| Frente | Estado |
|---|---|
| **casos/twitter-ituassu** | **Eixo mídia completo** ✅ — curvas `A(volume)` de H1, da dominância MV e de H2 por dia (07/ago). H1 convergiu em n≈200 e a falha do alvo é **de esquema** (§4.9); H2 **não reproduz em recorte nenhum** (§4.10) · **MP/MC fechado** ✅ — resíduo curado e as 4 explicações de classificação descartadas; divergência é do lado do artigo e **irresolúvel com o publicado** (§4.11) · **stance ◐ kit de rotulagem pronto** (18/ago/2026): codebook, amostra congelada de 320 (seed `20260818`), split 110/210, reteste de 40 e pré-registro com κ ≥ 0,70 — falta **só a Mariana rotular**. De passagem, corrigido o lado de `#AecioNever` (§4.15) |
| **casos/heine-xande** | Docs + pipeline ✅ · Fase 0 ✅ (dado não localizado) · Fases 1–4 ⏳ SharePoint |
| **casos/vacinas** | **AV1–AV6 e E1/E2/E3 todos medidos** (07/ago/2026) — auditoria do [plano §4.1](casos/vacinas/REPLICACAO_CASO_VACINAS.md) zerada · eixo B validado (κ 0,759 / 0,697) · colunas vazias explicadas (vazias na fonte) · ⏳ **único item aberto:** validar o rotulador no estrato baixo sob a convenção do artigo (precisa de rotulagem humana) · saldo LLM US$ 9,58 |
| **casos/reddit-buntain** | ✅ **CASO FECHADO E ESCRITO** (19 e 21/ago/2026). Alvo **Buntain & Golbeck 2014** (WWW, 133 cit.). Coleta completa: **43.479 submissions + 1.015.247 comentários**. **RB3: 3% → 57,6%** sob o mesmo limiar (**19×**); sem corte, 15,2% de 217.386 usuários. Converge em k≈10–20. Capítulo em `corpo.tex` (`cap:caso-reddit`), junto com o Massachs. Em 21/ago o `analise/rb3.py` ganhou **saída JSON** (`curva_rb3.json`, versionado) para alimentar a **Fig. 5.1** da dissertação — os números reproduziram exatamente. Nada pendente |
| **casos/reddit-massachs** | ✅ **FECHADO no que era viável, e ESCRITO** (21/ago/2026). Alvo **Massachs 2020** (WebSci, 29 cit.), **homofilia** (tipo novo). **Fase 2** ✅ **MH1 REPRODUZ**: 34,6% × 34,8% na homofilia e 26,8% × 26,7% na influência; baseline 15,6% × 15,2%. ⚠ **achado lateral:** sem reponderação de classes o mesmo modelo cai a **F1 8,2%** — decisão não declarada que domina o resultado publicado. ⛔ **Fase 3 fora de escopo** (não dimensionável pela API; caminho = Academic Torrents, depois da defesa), com predição pré-registrada guardada · ⚠ **o "não dimensionável" merece reconferência paciente**: o caso `reddit-topicos` mostrou que a mensagem de erro do Arctic Shift conflaciona estrangulamento e tamanho de consulta (§4.23) |
| **casos/reddit-companhia-ia** | ❌ **DESCARTADO** (07/ago/2026): #207 "My Boyfriend is AI" era preprint sem tração. Tombstone no README; substituído pelos dois acima |
| **casos/meta-ads-imigracao** | ⛔ **FORA DO ESCOPO DA DISSERTAÇÃO desde 21/ago/2026** (§4.18) — preservado por inteiro, volta se a rota Meta reabrir. O que estava feito, e continua válido: **Novo** (7/ago/2026) — fechava a **última rede vaga** do lineup. Alvo **Capozzi et al.** (CHI 2021, 29 cit. + SocInfo 2020, 16 cit.), **classificação** pró/anti em anúncios da Meta Ad Library. **Fase 0 ◐ quase fechada**: **os dois papers lidos na íntegra**, **dois gabaritos públicos** baixados e conferidos (2.312 anúncios de metadados + 200 anúncios × 3 anotadores **com texto**), 26 keywords transcritas, rota decidida (Ad Library API — a única coleta Meta viva), predições pré-registradas, e o **α de Krippendorff reproduzido** (0,763 × 0,76; 0,924 × 0,92 — ⚠ n 141 × 150). ✅ **CB2 desambiguado** — mede-se a razão R (§4.14). ⏳ só falta a **conta Meta verificada** (§2). Braço **Brasil** como mitigação de risco, sem alvo próprio |
| **casos/tiktok** | **A célula ressuscitou em 18/ago/2026.** A rota de coleta segue morta (credencial do eTC revogada), mas o alvo mudou de #299 para **PoliTok-DE** (arXiv 2509.15860), que publica dados no Hugging Face sob CC-BY **sem gate** — 939 mil posts de duas eleições alemãs com **status de disponibilidade por data** + 935 anotações humanas. **Fase 2 feita, offline**: **6 das 7** afirmações replicam (18,7% e 39,7% de deleção **exatos**; 2/3 de retirada pelo autor; 1-em-5 de intolerância; maioria com humor). A 7ª (deleção pela plataforma, 13,0%) replica a **1,4 p.p.** sob convenção não publicada. ★ **achado novo:** a taxa de deleção vai de **3,3% → 9,5% → 18,7%** em três checagens do **mesmo** conjunto — um **eixo temporal** independente do volume. Infra de coleta pronta, esperando chave viva |
| **casos/youtube-agecovp** | ✅ **FECHADO no eixo do filtro e ESCRITO** (21/ago/2026). A **quarta rede**; alvo **AGECovP** (*EPJ Data Science* 14:65, 2025). **Fase 1 completa**: 85/85 buscas, **3.446 vídeos** + **2.165 canais** pela API (cobertura 100%). **Fase 2** ✅ o ponto original replica, mas **só sob convenções não declaradas** (1ª categoria do canal → 1,9 p.p.; limiar de neutralidade do TextBlob). AG2 com folga (comentários **74×** mais tóxicos). **Fase 3** ✅ ❌ **P1 refutada**: o filtro remove **−6,4 p.p.** de UGC (IC95% [−11,4; −1,4]) — *menos*, não mais; robusto a 5 limiares e à mediana de inscritos (28 mil × 61,5 mil). ★ **o efeito de seleção está no funil inteiro**: canais no corpus 23,5% UGC × **61,7%** fora, Δ **+38,3 p.p.** (IC95% [+33,5; +43,0]), mediana **199 mil × 1.070**. Circularidade **confirmada e reforçada**, mecanismo **não isolado** (o ramo dos sugeridos saiu da API em ago/2023). ★ **AG3 segue irreproduzível porque o artigo se contradiz** (>93% UGC × ~7% UGC no mesmo texto; rótulos manuais não publicados; nossa medição dá **32,0%**, nenhum dos extremos). ⏳ resta só AG1/AG2 nos comentários |
| **casos/reddit-topicos** | ⏳ **NOVO em 22/ago/2026, e PARADO no Portão 1 esperando decisão da Mariana.** Sétimo caso; existe para fechar a única lacuna de **tipo de análise** (modelagem de tópico). Alvo **Melton et al. 2021** (*J. Infection and Public Health* 14(10), **178 cit.**), LDA + sentimento sobre 13 subreddits, dez/2020–mai/2021. **Fase 0 ✅**: full text lido e afirmações numeradas em [ARTIGO_MELTON_alvo.md](casos/reddit-topicos/ARTIGO_MELTON_alvo.md). ⭐ o corpus analisado é **11.641** (1.401 submissões + 10.240 comentários), **não os ~18.000** do resumo — **dois** filtros empilhados. ⭐ os autores **publicaram o modelo LDA ajustado** (7 pyLDAvis), congelado como gabarito e auto-conferido contra a Fig. 4 deles. ★ **T1 não é ranking, é ausência**, e já está sob tensão no gabarito deles (janeiro, k=15, tem `autism` e `microchip`): a ausência depende da **resolução**, não só da coleta. ◐ dimensionamento **6/13** — só os menores dão **215.394 × 11.641** (18,5×, teto do fator); os 7 restantes travaram no **rate limit**. ⭐ `NoNewNormal` **banido em 1º/set/2021**. ⭐ **e a rota de coleta está aberta**: paginar funciona no maior subreddit (5.050 comentários, 51 páginas, zero falhas) onde agregar falha — 0,29 kB/item, ~3,35 M comentários de `conspiracy` na janela, ~1 GB. **Nada foi ao `corpo.tex`.** 🔖 [RETOMAR.md](casos/reddit-topicos/RETOMAR.md) |
| **casos/ (Fase 4)** | [Tabela mestre](casos/RESULTADOS_tabela_mestre.md) ✅ **13 linhas fechadas**, **3 ⏳** (Heine ×2, stance) e **2 ⛔ fora do escopo** (Meta Ads ×2, §4.18) · *fração mínima* anotada em **4** células (AV1 f≈0,75; linha 1 n=100; linha 2 n≈200; linha 11 k≈10–20) · ⚠ **duas leituras novas**: PP3 pode confundir viés de esquema com falta de volume (§4.9), e a linha 15 inaugura um desfecho **não previsto** — efeito grande, mas *causa indeterminada* porque o passo do funil não é isolável (§4.16) |
| **escrita/dissertacao** | ✅ **Última versão: [`revisoes/revisao-8.pdf`](escrita/dissertacao/revisoes/revisao-8.pdf)** (14/set/2026, noite, **80 p.**, limpo): alinhada ao survey-3 (§4.28 resolvida). Antes, o [`revisao-7.pdf`](escrita/dissertacao/revisoes/revisao-7.pdf), o entregue: terminologia “revisão” e alinhamento ao survey-2 (§4.24 resolvida). Histórico: Compila limpo (**76 p.**), **zero referências indefinidas** e **zero `Overfull`** · ✅ **4ª rodada de revisão aplicada em 22/ago/2026** (17 anotações, pp. 9–56) → [`revisoes/revisao-5.pdf`](escrita/dissertacao/revisoes/revisao-5.pdf) · **capítulo novo de Trabalhos Relacionados** (Cap. 2) e **`.bib` de 27 → 43 entradas** · a **tabela mestre** entrou no texto (Tab. 9.1, §9.1, quinze linhas) e a **§9.2** passou a tratar do papel do banco de dados · ★ o Cap. do TikTok foi corrigido: o eixo temporal **já está no artigo-alvo** e a série publicada misturava bases (§4.22) · ✅ **3ª rodada de revisão aplicada em 21/ago/2026** (20 comentários, pp. 1–21) → [`revisoes/revisao-4.pdf`](escrita/dissertacao/revisoes/revisao-4.pdf), esperando a leitura da Mariana **do Cap. 3 em diante** · **passiva sintética 46 → 21** ocorrências no `corpo.tex` · **legendas curtas** nas 4 figuras e nas 8 tabelas, o que reduziu a Lista de figuras de duas páginas de texto corrido para 4 linhas · **4 entradas novas** no `.bib`: Jimeno-Yepes 2015 (o estudo dos 2,8 bi, que estava sem referência), Efron 1979, Efron e Tibshirani 1993 e Wilson 1927 · as 5 fases do protocolo viraram lista, e PP1/PP2 foram reescritas para deixarem de parecer a mesma pergunta · **epígrafe removida** (era uma página em branco com `, .`), o que destravou o bug do `thesispuc.cls` (§4.20) · ✳ **Nota de atualidade acrescentada ao Cap. 4** em 21/ago/2026 (fora do ciclo de revisão): o levantamento Torabit/BBC de ago/2026 (93.755 posts, termo único “vacina”, 65,8% × 34,2%) entra como ilustração pública dos dois eixos que o capítulo mediu — largura do filtro e esquema binário forçado. Entrada `bbc2026vacinas` no `.bib`, apontando para o original da BBC News Brasil. ✅ o **`revisao-3.pdf` foi republicado** com a nota (o PDF ainda estava com **0 anotações**, então nada comentado foi sobrescrito) · ✅ **2ª rodada de revisão aplicada em 21/ago/2026** (56 comentários, documento inteiro, primeira vez que os Caps. 5–7 foram lidos) → [`revisoes/revisao-3.pdf`](escrita/dissertacao/revisoes/revisao-3.pdf), esperando a leitura da Mariana · conjunto reduzido a **6 casos / 4 redes** e `tab:casos` corrigida em duas linhas (§4.18) · §2.3 (métricas) e §2.4 (coleta por plataforma) **reescritas** · **4 figuras** e **5 tabelas**: novas nesta rodada a `tab:metricas`, a `tab:youtube-funil`, a `tab:youtube-ponto`, a **Fig. 5.1** (curva por limiar do Buntain, de `curva_rb3.json`) e a **Fig. 6.1** (filtro × funil do YouTube) · front-matter ◐ — banca, data da defesa e bio preenchidas; faltam dedicatória e epígrafe · fluxo de revisão virou [skill](.claude/skills/revisao-dissertacao/SKILL.md), com o extrator em `revisoes/extrai_comentarios.py` · ⚠ histórico que segue valendo: os capítulos foram renumerados em 21/ago (Reddit 3º/4º, YouTube 5º, TikTok 6º) e o cap. do YouTube teve o **mecanismo** da circularidade corrigido (§4.16) |
| **escrita/survey** | ✅ **3ª rodada publicada em 14/set/2026, à noite** — [`revisoes/survey-3.pdf`](escrita/survey/revisoes/survey-3.pdf), 13 p., limpo: base 2.322 e só Gemini; a dissertação foi realinhada a ela na mesma noite (§4.28). ✅ **2ª rodada publicada em 14/set/2026** — [`revisoes/survey-2.pdf`](escrita/survey/revisoes/survey-2.pdf), 12 p., limpo: “levantamento sistemático” → “revisão” (pedido do orientador), nenhum número mudou. ⚠ o trecho abaixo sobre a extração dos 800 está superado: ela rodou em 9/set (base 2.322, §3 item 12), e o artigo segue, de propósito, na base 1.723. ✅ **1ª rodada de revisão publicada em 9/set/2026** — [`revisoes/survey-1.pdf`](escrita/survey/revisoes/survey-1.pdf), **11 p.**, zero erros, zero referências indefinidas, zero `Overfull`, escrito como artigo **fechado**. Base recomputada em **1.723** (§4.24). **6 figuras + 5 tabelas**, todas reprodutíveis por [`figuras.py`](escrita/survey/figuras.py) e [`validacao.py`](escrita/survey/validacao.py) sobre o `research.db`, com dump em `numeros.json` · seções novas: **§4.1** (a dependência do Twitter/X e sua data de vencimento — a fatia cai de 95% em 2014 para 14% em 2026, com inflexão em 2023), **§3.4** (κ por campo: coleta e plataforma 0,64–0,99, tipos de análise mediana 0,40) e a **tabela de famílias de API** · a §Ameaças à validade passou de 4 para **6 itens**, com o viés de acesso agora **medido** e a cobertura desigual dos modelos declarada · `.bib` de 11 → **13** entradas (Cohen 1960, Landis e Koch 1977) · Todas as seções em rascunho revisado · 2 decisões em aberto · sem pendência de dado · ⭐ **expansão: a varredura ACABOU** (23/ago, fila 100% tentada) e o desfecho só foi lido em **9/set**: **811 PDFs** recuperados sem credencial nenhuma (2.298 → **3.109**), taxa final **7,7%** no estrato pago (IC95% 7,2–8,2) — **não** os 12,4% intermediários, cujos ICs nem se sobrepõem (§4.25). ⛔ **condição de parada pré-registrada disparada** (piso 11%) e ⛔ **extração dos 800 nunca rodou** (bug de shell com `codigo 0` por cima do erro, §4.26). **Nada gasto**; 962 PDFs em disco sem extração; os 800 seguem sorteados. Extrair levaria a base de 1.723 a **~2.360** — decisão dela (§3, item 12). A decisão em aberto nº 1 (como reportar a fração inacessível) **fechou**: virou censo, e está no artigo como ameaça à validade medida |

### 4.30 📋 Roteiro de defesa em [`ROTEIRO.md`](ROTEIRO.md) (22/set/2026)

Justificativas prontas (homofilia, TikTok, Meta, modelagem de tópico, Heine), perguntas
previsíveis e **todas as fraquezas conhecidas**, cada uma com a pergunta da banca, a
resposta e a gravidade. ✅ **Decidido pela Mariana (22/set/2026): a dissertação foi
entregue e NÃO MUDA MAIS** — nem o `corpo.tex`. Tudo o que precisar de correção vai para os
`.md` de defesa:
- [`ROTEIRO.md`](ROTEIRO.md): justificativas prontas, **errata de 21 frases** do PDF
  entregue (com página) e ajustes na fala dos slides;
- [`PERGUNTAS.md`](PERGUNTAS.md): perguntas previsíveis e todas as fraquezas conhecidas,
  cada uma com a pergunta da banca, a resposta e a gravidade.
A edição que uma sessão tinha feito na Seção 3.3 foi **desfeita** (ver
[REVISOES.md](escrita/dissertacao/revisoes/REVISOES.md) §Depois do revisao-13).

### 4.31 ★ O 19× do caso Buntain mistura coletar mais com trocar de definição (25/set/2026)

A Mariana perguntou se não daria para chegar aos 3% do artigo "de forma equivalente",
olhando só os top-100 posts de cada comunidade. **Dá — e a conta muda a magnitude que o
Cap. 6 reivindica.** Medição em
[RB3_recorte_reconstruido.md](casos/reddit-buntain/data/repl/buntain2013/RB3_recorte_reconstruido.md);
script `casos/reddit-buntain/analise/rb3_recorte_artigo.py`; JSON `rb3_recorte_artigo.json`.

1. **A ficha do alvo fixa a leitura do corte.** O grafo do artigo é dirigido e **por
   subreddit**, o corte é de ≥20 arestas **de saída**, e três subreddits caem *"por não ter
   usuário acima do limiar"* — o que só é possível se o corte valer **dentro de cada rede**.
   A réplica aplicou um corte **global**, de ≥20 mensagens.
2. **O recorte do artigo é reproduzível pelo nosso dado:** **259** participantes em **11**
   de 13 subreddits, contra 279 em 10. Isso responde à fraqueza 2.6.2 do
   [PERGUNTAS.md](PERGUNTAS.md), que dizia que o ponto original não fora reconstruído.
3. ⚠ **Com a definição do artigo fixa, coletar tudo leva de 0,8% a 4,2%** — e não a 57,6%.
   O fator **19×** do `corpo.tex` vem em boa parte da troca de definição de "participar de
   mais de uma comunidade" (≥20 arestas de saída em cada rede → ≥20 mensagens no total mais
   presença em dois subreddits), e não só de coletar mais. Com o corte global aplicado ao
   recorte do artigo o valor é 29,0%, ou seja: o recorte responde por metade da distância e
   a definição pela outra metade.
4. ★ **A formulação que se sustenta segura população e definição:** dos **mesmos 259**
   participantes que o recorte do artigo identifica, **41,3%** estavam ativos em mais de uma
   das treze comunidades (152 em um só, 58 em dois, 31 em três, 14 em quatro, 4 em cinco),
   contra os 2,5% que a coleta deles deixava ver. **≈16×, na população do artigo.**
5. ⚠ A afirmação do `corpo.tex` de que *"nenhum limiar aplicado ao universo devolve os 3%"*
   (§sec:rb3-curva e legenda da `fig:curva-rb3`) vale para o corte global, mas **não** para o
   corte por rede.

**Nada disso mudou a dissertação**, pela decisão de 22/set (§4.30): as respostas foram para
o [PERGUNTAS.md](PERGUNTAS.md) §2.6.1, §2.6.2 e §2.6.7, e a orientação lá é **não defender o
19×** — conceder a unidade e ir direto aos 2,5% × 41,3%. **Resta decisão dela:** se a frase
do §sec:rb3-curva entra na errata do [ROTEIRO.md](ROTEIRO.md), e se
[RESULTADOS_RB3.md](casos/reddit-buntain/data/repl/buntain2013/RESULTADOS_RB3.md) §7 e a
linha 11 da [tabela mestre](casos/RESULTADOS_tabela_mestre.md) passam a registrar as duas
operacionalizações lado a lado.

### 4.29 ⚠ A expansão do Massachs foi fechada por uma sessão, não pela Mariana, e nunca reaberta (22/set/2026)

A Mariana perguntou, preparando a defesa, por que o caso de homofilia não foi executado
por inteiro, se ela perguntou várias vezes o que faltava. A reconstrução pelos documentos:

1. **19/ago:** a sonda de dimensionamento (`pipeline/probe_volume.py`) usou só o endpoint
   de **agregação** do Arctic Shift, que falhou (20/34, depois 34/34 incompletos). A mesma
   sessão escreveu em [FASE2 §6](casos/reddit-massachs/data/repl/massachs2016/FASE2_ponto_original.md)
   “**Decisão:** a Fase 3 fica fora do escopo da versão de 31/ago”. Nenhum documento
   atribui essa decisão à Mariana, ao contrário das outras decisões de escopo (Meta, #207).
2. **A decisão foi escrita como “não é pendência”** (FASE2 §5, tabela mestre, §1 item 7:
   “Nada a fazer aqui até a defesa”). Por isso nenhuma resposta a “o que falta” a listou.
3. **22/ago:** o caso `reddit-topicos` mediu que a mensagem de erro mistura
   estrangulamento com tamanho (§4.23) e que **coletar pela paginação funciona onde
   agregar falha** (§2). Isso tirava o motivo da decisão, mas a §4.23 concluiu que
   “não derruba o veredito” e a descoberta não voltou ao item 7.
4. **O prazo mudou e o escopo não foi revisto:** a decisão valia para “a versão de
   31/ago”; a entrega foi 14/set e a defesa é 29/set.

O Buntain coletou 1.015.247 comentários pela mesma rota paginada, então a expansão era
tentável. Não se sabe o tamanho: `politics`, `news`, `worldnews` e `todayilearned` em
2012 e 2016 somam provavelmente dezenas de milhões de comentários, o que pela API leva
semanas e pelos dumps do Academic Torrents leva dias de download e processamento.
⚠ O `corpo.tex` diz ainda “Cinco são executados por inteiro” (§1.3 e nota da `tab:casos`),
o que contradiz o Cap. 7. ✅ **Resolvido em 22/set:** as frases não serão
corrigidas (a dissertação não muda mais); entram na errata do [`ROTEIRO.md`](ROTEIRO.md).
**Resta decisão dela:** se a expansão entra depois da defesa.

⭐ **Achado da mesma conversa (22/set):** a sonda de 19/ago media a coisa errada. Ela
contava comentários dos **34** subreddits políticos, mas o arquivo dos autores traz
`participation_12`, `pos_scores_12` e `neg_scores_12` sobre **766** subreddits (e
`participation_16` sobre 985); só as interações (`dist_int_12`, `pos_int_12`) são sobre os
34. Recalcular os atributos de usuários novos exige o histórico de 2012 deles no Reddit
inteiro, não só na política. E a lista dos 51 subreddits que definem o grupo focal não é
publicada, de modo que a expansão precisa antes reconstruir os 44.924 a partir do dado
bruto e medir a sobreposição. Nenhum dos dois pontos está no Cap. 7 nem nos `.md` do caso.
Consulta à tabela dos autores (22/set): os usuários vêm com o **nome de usuário real**, então
o grupo dos 44.924 é conferível contra o dado bruto. Das 34 comunidades políticas, só 17
aparecem nas colunas de participação (que cobrem as ~1.000 mais populares). Em 2016, **305
usuários** do grupo não comentaram em nenhuma política visível; 47,5% deles comentaram em
`r/The_Donald` e 23% em `r/SandersForPresident`, pista de que as 51 incluíam comunidades de
campanha. Registrado em [PERGUNTAS.md](PERGUNTAS.md) 2.7.1b.
⭐ **Engenharia reversa da lista dos 51 (22/set, depois da entrega):** 500 membros e 500
não-membros ativos em r/politics em 2012, com as contagens do Arctic Shift por autor.
**37 dos 500 não-membros (7,4%) têm ≥10 comentários só em r/politics nos dois anos**: pela
regra publicada teriam de estar no grupo. **O grupo não segue a regra declarada**, e a lista
não é identificável. Hipóteses não separadas: lacunas do Pushshift de ~2019, ou critério
adicional não declarado. Ver
[ENGENHARIA_REVERSA_51.md](casos/reddit-massachs/data/repl/massachs2016/ENGENHARIA_REVERSA_51.md).

---

### 4.30 ⚠ O que o texto entregue promete e não existia fora dele (28/set/2026)

Defesa em 29/set. A dissertação e a survey estão **congeladas** em `versao_final/`, então tudo o
que segue é correção por fora. Uma leitura dos dois PDFs entregues, cruzada com o repositório,
achou três coisas que o texto afirma e que não tinham lastro público, e uma conta que existia e não
estava no lugar certo.

**1. O texto promete reprodutibilidade e não dá endereço.** Os **18 artefatos** citados por nome
nas notas de rodapé e legendas (scripts, `curva_*.json`, `fase3_ugc_completo.json`,
`fase2_politok.json`, `PRE_REGISTRO_stance.md`) **existem e estão todos versionados**. O que
faltava era o endereço, e o repositório está **privado** (verificado: o endereço devolve 404 de
fora). Feito: [`REPRODUCAO.md`](REPRODUCAO.md) na raiz, ligando cada figura e cada número ao
script, à saída e ao dado de entrada, com a declaração do que não é redistribuído e por quê
(tweets e gabarito de stance são dado pessoal; metadados do YouTube são termos da API; gabaritos de
terceiros apontam para a fonte). ⏳ **Só a Mariana pode fechar:** tornar o repositório público e
criar o release ligado ao Zenodo para o DOI. Enquanto isso não acontece, a resposta 2.10.1 do
`PERGUNTAS.md` traz a versão honesta, que não afirma publicação.

**2. A §10.2 argumenta infraestrutura e não mede nada.** Feito:
[`CUSTO_infraestrutura.md`](CUSTO_infraestrutura.md), com os números que o texto não traz —
**2.086 MB** de instantâneo congelado nos seis casos e cerca de **15,3 mil** reexecuções de
análise (2.701 subamostras no H1, 12.600 no H2, **32 execuções de Louvain** sobre grafos de 65 mil
a 6,55 M de posts, que é o que explica as 3 réplicas da Figura 5.1). Contra os itens que os artigos
analisaram: 1,74 GB guardados para testar uma conclusão tirada de 1.525 tweets; 124 MB para uma
tirada de 700.

**3. O H1 do Ituassu é enunciado por dia e testado no agregado.** A conta por dia **já existia** em
[RESULTADOS_FASE0_midia.md](casos/twitter-ituassu/data/repl/compos2014/RESULTADOS_FASE0_midia.md) e
não está no PDF: no universo, **1 dos 7 dias** passa de 50% (23/out, 51,2%; os outros entre 24,9% e
43,2%); na amostra reconstruída, 3 dos 7. A refutação por dia é **mais forte** que a agregada, de
modo que o texto relata a versão conservadora. Registrado como pergunta 2.3.7 e errata 22.

**4. A errata virou documento.** [`errata/errata.tex`](errata/errata.tex) → `errata.pdf`, 3 páginas,
`article` autônomo que não toca em `escrita/`. Reúne **25 itens** em duas seções, correções de
afirmação e precisões, cada uma com a fonte da correção. **Decisão da Mariana: não será entregue à
banca**; existe pronto para o caso de ser pedido ou de a decisão mudar. A Parte B do
[ROTEIRO.md](ROTEIRO.md) remete a ele e mantém a coluna do que dizer.

**5. O `PERGUNTAS.md` foi auditado e ampliado.** De 88 para **104** entradas, com **índice por
gravidade** no topo e uma seção nova (**2.10**, artefatos e infraestrutura). Dezessete entradas novas,
entre elas a tensão entre a PP3 prometida por tipo de análise e a resposta que desloca a unidade
para a afirmação (2.1.10), as apostas pré-registradas que erraram (2.1.12), o alvo de 2018 que tem
linha na tabela mestre e quase nada de texto (2.3.8) e o teto de 0,972 do NMI (2.5.14). Os números
marcados como conta fora do texto foram **reconferidos contra os arquivos dos casos**, e onde a
resposta só afirmava o resultado agora traz a derivação (a razão de 1,07 sem a comunidade difusa; a
concordância esperada por acaso de 0,77 na validação da survey).

✅ **Decidido pela Mariana em 28/set/2026: o dado no histórico não é impedimento**, e o
repositório pode ser aberto como está. O levantamento que motivou a pergunta fica registrado
abaixo, porque ele é o que sustenta a ressalva do `REPRODUCAO.md` e o que justifica o depósito
curado ser diferente do repositório. ⏳ Falta só a ação na conta dela: tornar público e criar o
release ligado ao Zenodo.

⚠ **O levantamento, de 28/set/2026.** Os seis
`casos/twitter-ituassu/data/repl/compos2014/stance/gold_stance_*.csv` **estão versionados**, e
somam **1.005 linhas com texto de tweet, identificador de autor e contagem de seguidores** de
pessoas reais. Entraram no commit `1243bc8` (9/set), de modo que estão também no histórico.
Consequências: (a) **não torne o repositório público como ele está**; (b) `git rm --cached` resolve
a árvore e **não** resolve o histórico; (c) reescrever histórico na véspera da defesa é risco alto,
e o GitHub pode manter objetos alcançáveis por um tempo depois. Com a decisão tomada, o que
fica valendo é: o **repositório** carrega esses arquivos e a ressalva correspondente, e o
**depósito com DOI** não os carrega. O pacote do depósito está em `deposito/` (fora do git):
289 arquivos, 0,95 MB, os 19 artefatos que o PDF cita por nome, auditado por conteúdo (zero
identificadores de autor, zero chaves) e com `MANIFESTO.md` listando os 9 arquivos excluídos.

**6. Três comentários novos na versão final, lidos em 28/set/2026.** A Mariana anotou o PDF
entregue depois da entrega, e os três viraram resposta pronta, não errata, porque em nenhum deles o
texto está errado: ele está comprimido.
- p. 12, *"3.107 + 10.200 não é 13.395"*. Não são complementares: **932** dos 10.200 em paywall
  entraram no corpus (tinham cópia gratuita) e **948** dos abertos não entraram (sem endereço de PDF
  nas quatro fontes, ou arquivo reprovado na validação). Por licença, 13.395 = 3.108 + 10.200 + **87
  sem rótulo no DBLP**, que são os 88 que pareciam faltar; por PDF, 13.395 = 3.107 + 10.288.
  Números em `escrita/survey/numeros.json`, chave `funil_acesso`. → PERGUNTAS 2.2.16.
- p. 12, *"que segunda busca?"*. É a varredura dos **11.093** artigos que tinham ficado sem PDF,
  tentados todos de novo pelas rotas abertas, que recuperou **811** (7,3% no total, 7,7% no estrato
  pago) e serviu de teste do viés de acesso. → PERGUNTAS 2.2.17.
- p. 18, *"a conclusão é quase a mesma de Ruths e Pfeffer; o que esta dissertação entrega que aquele
  artigo não?"*. É a pergunta de fundo da defesa, e a resposta em uma linha é que eles recomendam e
  ela mede: prevalência, teste da afirmação publicada, e a conclusão de que a sensibilidade é
  propriedade da afirmação, o que permite dizer **quando** a ressalva importa. → PERGUNTAS 2.1.16.

**7. A taxonomia de tipos de análise foi auditada (28/set/2026).** A pergunta da Mariana era como
garantir que o prompt não enviesou a detecção das análises. A resposta tem três camadas, todas
declaradas: as regras 1 e 5 do prompt (evidência direta, e só o que foi executado), o campo ser
**aberto** com um vocabulário de 22 termos passado como sugestão em vez de lista fechada, e o
agrupamento posterior em doze categorias por um mapeamento de palavras-chave no `figuras.py`.
⭐ O que não existia era o tamanho do limite, e agora existe:
[`audita_rotulos_analise.py`](escrita/survey/audita_rotulos_analise.py) mede **14.237 rótulos** nos
2.472 artigos, 5,8 por artigo, dos quais **52,9% não caem em nenhuma das doze categorias** (43,5%
descontado o guarda-chuva da análise de conteúdo), e **143 artigos, 5,8% da base, não entram em
categoria alguma**. O script **reproduz as doze linhas publicadas** antes de medir o que sobra, o
que dá lastro à nota da Tabela 1.1 de que ela é ordenação e não estimativa de prevalência. Achados
de passagem: "análise descritiva" (63 ocorrências) não casa com as chaves de estatística
descritiva, e "identificação de bots" mais "detecção de spam/bots" (216) não casam com as de
desinformação, de modo que essas duas linhas da tabela são subcontagem. → PERGUNTAS 2.2.15.

⚠ **Nada disso alterou os PDFs entregues nem os fontes de `escrita/dissertacao`.** O `.gitignore`
passou a excluir `PERGUNTAS.md`, `ROTEIRO.md`, `errata/`, o rascunho de fala e o gabarito humano de
stance (traz texto de tweet e perfil de autor), para que abrir o repositório não publique nem a
preparação da defesa nem dado pessoal.
