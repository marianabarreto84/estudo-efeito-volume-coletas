# Revisões da dissertação — o que cada rodada mudou

**Fluxo:** a Mariana comenta a última versão em PDF (destaques com balão, no
Acrobat ou em qualquer leitor); a rodada seguinte aplica os comentários no fonte
LaTeX e salva um `revisao-N+1.pdf` nesta pasta para a próxima leitura. Nunca
sobrescrever um `revisao-N.pdf` já comentado — ele é o registro do que ela viu.

O procedimento completo da rodada (extrair → ler tudo → planejar → aplicar →
recompilar → documentar), com as armadilhas já encontradas, está na skill
[`revisao-dissertacao`](../../../.claude/skills/revisao-dissertacao/SKILL.md).

Para extrair os comentários de um PDF anotado:

```bash
PYTHONUTF8=1 python extrai_comentarios.py revisao-N.pdf > coment.md
```

O script está aqui: [`extrai_comentarios.py`](extrai_comentarios.py). Ele lê os
balões (`/Contents`, via pypdf) e recorta o trecho destacado a partir dos
`/QuadPoints` (via pdfplumber). O `PYTHONUTF8=1` e o redirecionamento para arquivo
não são opcionais: o console do Windows é cp1252 e quebra em `τ`, `—` e afins.

---

## revisao-1.pdf → revisao-2.pdf (21/ago/2026)

- **Entrada:** `revisao-1.pdf`, 45 p., **32 destaques comentados**, pp. 6–27
  (do Resumo ao início do Cap. 4). Na numeração de agora, os Caps. 5 (Reddit),
  6 (YouTube), 7 (TikTok) e 8 (Conclusão) **não foram revisados nesta rodada**.
- **Saída:** `revisao-2.pdf`, **57 p.**, compila limpo (sem `undefined`).
- **Fonte alterado:** `dissertacao.tex` (resumo PT/EN, `\graphicspath`),
  `corpo.tex` (29 edições), `figuras/` (novo).

> ⚠️ **O `revisao-2.pdf` foi regerado no mesmo dia e cresceu de 47 para 57 páginas.**
> Duas coisas aconteceram entre uma coisa e outra: (a) outra frente de trabalho
> acrescentou o **capítulo de Reddit** (Buntain + Massachs), renumerou os capítulos
> seguintes e corrigiu o capítulo do YouTube; (b) essa sincronização **sobrescreveu** o
> `corpo.tex` e apagou as edições desta rodada, que foram **reaplicadas** por cima da
> versão nova. Nada da revisão se perdeu, e nada do capítulo novo foi desfeito — mas se
> você já tinha baixado um `revisao-2.pdf` de 47 páginas, **é o antigo**. Detalhes em
> `ESTADO.md` §4.17.

### Mapa comentário → mudança

| # | p. | O que você pediu | O que foi feito |
|---|----|------------------|-----------------|
| 1 | 6 | "análises mais praticadas" é pouco usado | → "análises mais **realizadas**" (resumo PT e EN) |
| 2 | 6 | "essa vírgula existe?" (`…de uma análise, e esta dissertação…`) | frase quebrada em duas; a vírgula sumiu |
| 3 | 6 | tirar a mediana | → "**menos da metade** dos artigos passa de 1 milhão de itens" |
| 4 | 6 | 1ª conclusão ("coletar muito não implica amostrar") fica sem sentido | removida do resumo; sobra só a 2ª |
| 5 | 6 | "seis casos, um por rede social (…)" mudou | → "um conjunto de **casos replicáveis, distribuídos por diferentes redes sociais e tipos de análise**". Corrigido também na Conclusão (mantendo a contagem em "cinco executados, e um sexto em parte") e na `tab:casos` |
| 6 | 6 | fecho genérico demais | → fecho agora diz a consequência prática (declarar o volume e a dependência da conclusão passa a integrar o relato) |
| 7 | 10 | adicionar figuras | **2 figuras novas**, geradas dos dados congelados: `Fig. 3.1` (curva do RTMV, Cap. 3) e `Fig. 4.1` (curva da rede do debate vacinal, 2 painéis, Cap. 4). Script em [figuras/gerar_figuras.py](../figuras/gerar_figuras.py) |
| 8 | 13 | não gostou de "fluxo reprodutível" | → "o levantamento partiu do índice DBLP… **em etapas documentadas e reexecutáveis**" |
| 9 | 13 | por que 13.395 → 2.139? | **parágrafo novo**: não é critério de inclusão, é *paywall* (10.230 fechados; 2.106 PDFs em acesso aberto + *proxy*), com a ressalva de que o subconjunto é enviesado por editora. ⚠️ *sua sugestão de coletar mais da survey ficou registrada como trabalho futuro, não foi executada* |
| 10 | 13 | o que importa é que a **maioria coleta pouco** | parágrafo reescrito: "metade dos artigos fica abaixo de ≈273 mil itens, e **seis em cada dez não chegam a 1 milhão**"; o achado "coletar muito não implica amostrar" virou observação secundária |
| 11 | 14 | refrasear a PP2 | → "…convergido ou ainda se movia? **No caso em que esse volume bastava**, …; no caso em que ainda se movia, a coleta foi interrompida cedo demais" |
| 12 | 14 | antes é preciso saber **se** varia por tipo de análise | PP3 agora começa por "**O efeito do volume é o mesmo para toda análise ou varia conforme o tipo?**" e só depois pergunta para quais |
| 13 | 14 | a ideia é o volume virar motivo de *disclaimer* | **contribuição nova** na lista: o volume e a dependência da conclusão deveriam constar do relato como ressalva explícita, e a dissertação diz *quando* ela é indispensável |
| 14 | 16 | não gostou de "O levantamento estabelece o quê." | → "O capítulo anterior estabeleceu o problema: …" |
| 15 | 16 | "banda bootstrap" solto | **definida** onde aparece pela primeira vez (repetir o sorteio, tomar os percentis 2,5 e 97,5 → o que o acaso sozinho já explicaria) |
| 16 | 16 | o que é `N_paper` e "a curva ainda se movia"? | ambos definidos explicitamente; parágrafo separado explicando a diferença entre **estreitar sem deslocar** (convergência) e **deslocar sistematicamente** (não convergiu) |
| 17 | 17 | nenhum caso viu centralidade de verdade | linha renomeada para **"Análise de rede e papéis sociais"**, com registro explícito de que *nenhum caso instancia centralidade em sentido estrito*; a `tab:casos` passou a dizer "Rede / papéis sociais" na linha do Buntain |
| 18 | 18 | contar o problema real com Meta e TikTok | **parágrafo novo**: MCL virou paga em jan/2026 e não deixa os dados saírem (incompatível com a Fase 1); a cota limita **ritmo**, não total; por isso a migração para a **Ad Library API**. No TikTok, credencial expirada → entrega o **eixo temporal** no lugar do de volume. Limitação correspondente também atualizada |
| 19 | 19 | tabela estourou a formatação | `tabularx` com largura fixa em `\textwidth` + `\footnotesize`; **a última coluna agora lê inteira**. De quebra, a tabela ganhou a linha do **caso vacinas**, que só existia na prosa (agora 7 linhas) e passou a ser **ordenada por capítulo**, com o único caso não executado (Instagram/Facebook) por último |
| 20 | 21 | "É o sexto caso e o único em Twitter/X" — **mentira** | removido; → "é **um dos dois** casos em Twitter/X do conjunto". A prosa da §2.5 também passou de "um sexto caso" para "dois casos cobrem o Twitter/X" |
| 21 | 21 | não entendeu 32.193 / 140.909 | explicado: 32.193 = tudo com `#Eleições2014` na janela (**46× os 700 do artigo**) = o `A_mais` do eixo E1; 140.909 = com todas as hashtags eleitorais = eixo E2. "O primeiro mede coletar mais do mesmo; o segundo, coletar o que estava ao lado" |
| 22 | 22 | estatística pesada demais | Wilson/`z`/`p` movidos para **nota de rodapé**; no corpo fica "5 para 1, sobre 79.603 tweets, margem inferior a meio ponto" |
| 23 | 22 | deixar claro que o problema é o **horário de pico**, não amostrar | trecho novo: "o problema não é ter amostrado; é ter amostrado **por horários de pico**", com o mecanismo e a afirmação de que uma amostra **aleatória** do mesmo tamanho teria acertado |
| 24 | 23 | explicar "intra-autor" | substituído por "comparar **cada autor consigo mesmo**", com o raciocínio contrafactual explícito; a estatística pareada foi para nota de rodapé |
| 25 | 23 | "Predição refutada" confuso | reescrito como "**Uma aposta registrada antes, e perdida**", dizendo o que é o pré-registro, qual era a aposta e por que ela se perdeu |
| 26 | 23 | o que é "escolástica"? | → "A distinção **tem consequência prática direta**" |
| 27 | 24 | o que é "o alvo já analisou a população"? | explicado: a pergunta só vale quando o alvo **amostrou**; se rodou sobre tudo o que coletou (como o eixo de rede do Cap. 4), não há esquema a avaliar |
| 28 | 24 | você não sabe de antemão como amostrar; na dúvida, colete tudo | **parágrafo novo** incorporando o argumento: saber o esquema não-viesado exige saber a quê a medida é sensível; APIs não oferecem quadro amostral; logo, **coletar amplo e sortear depois** — e é por isso que o protocolo mede volume mesmo quando a falha é de esquema |
| 29 | 25 | parágrafo da coautoria é desnecessário | removido do corpo; virou **nota de rodapé** de uma linha na primeira menção ao artigo (a divulgação de conflito de interesse é academicamente esperada, então foi encolhida, não apagada) |
| 30 | 26 | "estabilidade estrutural, não empírica" — não entendeu | reescrito em português direto: a afirmação compara os **dois tweets mais retuitados**, e o topo é o que qualquer coleta pega primeiro; descer o limiar acrescenta material **embaixo**, não em cima |
| 31 | 27 | (só marcação, sem texto) | coberto pela reescrita do item 30 — é a mesma frase |
| 32 | 27 | qual o propósito do parágrafo do "equilíbrio entre os polos"? | ganhou **abertura** (a simetria é o pano de fundo que dá força à conclusão-título do artigo) e **fecho** (o lado pró é ~1,5× o anti, então a premissa de simetria não se sustenta) |

### Pendências que esta rodada **não** resolveu

1. **[9]** "coletar mais da survey" para reduzir o funil 13.395 → 2.139 — é trabalho
   na survey, não na dissertação. Registrado no texto como limitação.
2. ~~Os resultados de **reddit-buntain** e **reddit-massachs** não têm capítulo~~ —
   **resolvido em 21/ago/2026 por outra frente**: o Cap. 5 (`cap:caso-reddit`) cobre os
   dois. Ele **não foi revisado pela Mariana**, como os Caps. 6 (YouTube), 7 (TikTok) e
   8 (Conclusão).
3. ~~A lista de **"Próximos passos"** da Conclusão está desatualizada~~ —
   **resolvida em 21/ago/2026 pela outra frente**: foi reescrita em cinco itens novos
   (Instagram/Facebook como único caso pendente; retomada da expansão do Massachs;
   isolar o passo do funil no YouTube; completar as curvas e a coluna de fração
   mínima; solução genérica agora "com seis casos e seis tipos de análise"). O rótulo
   "centralidade" saiu de lá.
4. Front-matter (`% TODO`): data da defesa, banca, bio, dedicatória, epígrafe.

---

## revisao-2.pdf → revisao-3.pdf (21/ago/2026)

- **Entrada:** `revisao-2.pdf`, 57 p., **56 anotações**, das quais **51 com
  comentário**, cobrindo o documento **inteiro** desta vez (front-matter →
  Cap. 7). É a primeira rodada em que os Caps. 5 (Reddit), 6 (YouTube) e
  7 (TikTok) foram lidos.
- **Saída:** `revisao-3.pdf`, **64 p.**, compila limpo: zero erros, zero
  referências indefinidas e **zero `Overfull \hbox`**.
- **Fonte alterado:** `dissertacao.tex` (banca, data, bio, resumo PT/EN),
  `corpo.tex` (uma reescrita estrutural + ~40 edições), `figuras/gerar_figuras.py`
  (2 figuras novas), `casos/reddit-buntain/analise/rb3.py` (saída JSON).
- **Fluxo:** virou skill — [`.claude/skills/revisao-dissertacao/SKILL.md`](../../../.claude/skills/revisao-dissertacao/SKILL.md).
  O extrator de comentários passou a viver aqui:
  [`extrai_comentarios.py`](extrai_comentarios.py).

### As três decisões estruturais desta rodada

1. **Instagram/Facebook saiu da dissertação** (comentários 24 e 25). O conjunto
   passou de sete casos em cinco redes para **seis casos em quatro redes**, todos
   executados (cinco por inteiro, o de TikTok em parte). A `tab:casos` perdeu uma
   linha; a §2.4 ganhou um parágrafo dizendo **por que** a Meta ficou de fora
   (CrowdTangle desligado, Content Library paga e sem exportação, Ad Library só
   alcança publicidade); e todas as listas que citavam "os anúncios de imigração"
   foram refeitas com o TikTok no lugar. ⚠️ **O caso não foi apagado**: `casos/meta-ads-imigracao/`
   segue documentado e a `RESULTADOS_tabela_mestre.md` mantém as linhas 13–14
   marcadas como fora do escopo. Os "Próximos passos" ganharam o item de reabrir
   a célula se uma rota de coleta compatível voltar a existir.
2. **O caso do YouTube não cobre modelagem de tópico** — foi o que a reescrita da
   §2.3 (comentários 19 e 20) tornou visível, e o texto afirmava o contrário. A
   `tab:casos` passou a dizer *Sentimento + composição do corpus*, que é o que o
   caso de fato entrega, e a ausência de modelagem de tópico virou **limitação de
   cobertura declarada** e item de próximos passos. É o tipo mais frequente do
   levantamento sem caso executado.
3. **A "validação" da regra de atribuição de lado no caso vacinal foi rebaixada**
   (comentário 35). A Mariana, coautora do artigo replicado, duvidou de que ele
   tivesse rotulado os 602 autores influentes lendo texto. Ela tem razão, e a
   dúvida reencontrou uma **retratação que já estava escrita** em
   `casos/vacinas/.../DECISOES_ROTULADOR.md` (D7): a Tabela 1 do artigo classifica
   por comunidade do autor, não por conteúdo. Os dois caminhos não são
   independentes, então a coincidência de 0,3 p.p. deixou de ser "validação" e
   passou a ser consistência de convenção; o peso do argumento migrou para a
   triangulação com o eixo de conteúdo, que é instrumento de fato independente.

### Mapa comentário → mudança

| # | p. | O que você pediu | O que foi feito |
|---|----|------------------|-----------------|
| 1 | 2 | é aqui que vai a banca? | **Sim, é a folha de aprovação.** Preenchida com o *Formulário de Marcação de Defesa* que estava em `Downloads/`: **Edward Hermann Haeusler** (PUC-Rio) e **Ana Carolina Brito de Almeida** (UERJ). O suplente (Marcos Vianna Villas) não entra na folha |
| 2 | 2 | atualizar a data | Usei a **data da defesa**, que o formulário traz e é o que o campo pede: **29 de Setembro de 2026** (não "hoje") |
| 3 | 3 | Engenharia da Computação pela PUC-Rio | bio preenchida com o nome extenso |
| 4 | 6 | "agudo" não ajuda; "mensurável" basta | → "um domínio em que esse efeito é **mensurável**" (PT e EN) |
| 5 | 6 | falta conectivo de oposição | → "varia enormemente, **mas** que menos da metade…" (PT); "enormously, **yet** that fewer than half…" (EN) |
| 6 | 10 | isso é legenda e não figura, né? | **Sim, é legenda** (`\caption`). Encurtei as duas para o que a figura não diz sozinha, e a linha de rastreabilidade virou "Dados em X; figura gerada por Y" |
| 7 | 13 | "empiricamente" sobra | removido |
| 8 | 13 | não sei se cabe "a ironia" num texto acadêmico | concordo — o registro ficou, o tom saiu: "O próprio levantamento é, portanto, uma coleta parcial do seu tema, e a §8.1 o retoma como limitação declarada" |
| 9 | 13 | o que é "item"? | **definido** na primeira ocorrência: a unidade que o próprio trabalho declara ter recolhido (publicação, comentário, vídeo, anúncio, conta), com a ressalva de que se comparam ordens de grandeza e não objetos idênticos |
| 10 | 13 | "conveniência" não é preguiça, é o que dava para coletar | **parágrafo novo**: o volume é dimensionado pelo que a coleta *alcançou* (o que a interface devolveu, o que a cota permitiu, o que o acervo já tinha), que é a condição normal de quem coleta de RSD; o vão não é esse, é o volume não ser declarado nem tratado como condição da conclusão |
| 11 | 14 | (só marcação, sobre a Tabela 1.1) | era **formatação**: a tabela estourava a margem em 7,9 pt. Corrigido; o documento hoje tem **zero** `Overfull` |
| 12 | 14 | a PP2 deixa de ser pergunta no meio | PP2 virou só a pergunta; a leitura ("quando bastava… quando foi interrompida cedo") saiu para uma frase depois da lista |
| 13 | 15 | a PP3 pode ser resumida | → "E, se varia, quais tipos são sensíveis ao volume e quais não são?" |
| 14 | 15 | esse teste existe para todos os casos? | **Não** — só para os alvos que amostraram. A contribuição passou a dizer isso: "é executado em parte dos casos, e não em todos" |
| 15 | 16 | pode tirar esse trecho | removido |
| 16 | 16 | prefiro voz passiva a "reproduz-se" | o parágrafo inteiro da lógica do protocolo foi para a voz passiva |
| 17 | 16 | não sei se precisa de "bootstrap" | a palavra saiu de todas as ocorrências; ficou "banda", definida uma vez, com o nome técnico (reamostragem) mencionado só de passagem |
| 18 | 16 | gosto do parágrafo, mas só se ele descrever o que foi feito | descreve, e agora **diz onde**: o parágrafo aponta as duas inversões de afirmação que a camada substantiva decidiu (H1 no Cap. 3, papéis locais no Cap. 5). O detalhe que não se usava saiu |
| 19 | 17 | técnico demais; diga o que a dissertação abordou e por que a métrica muda por tipo | **§2.3 reescrita do zero.** Sai a lista de NMI/ARI/Kendall-τ/RBO/atribuição húngara; entra a explicação de que a quantidade a comparar é ditada pela **forma da afirmação do alvo** (proporção, partição, ordenação) e a **Tabela 2.2**, que liga cada tipo de análise ao capítulo, à forma da afirmação e ao que se comparou de fato |
| 20 | 18 | (continuação do 19) | idem. As citações de algoritmo viraram uma linha na legenda da tabela |
| 21 | 18 | um parágrafo por plataforma, dizendo o que dava e o que não dava para coletar | **§2.4 reescrita**: abertura sobre por que a rota de coleta decide o volume publicado, e depois **um parágrafo por plataforma** — Reddit (aberta), YouTube (aberta, com teto e com prazo), Twitter/X (fechada, contornada por acervo), TikTok (fechada por credencial), Instagram e Facebook (fechadas, e por isso fora) |
| 22 | 18 | "Fase 1" aparece antes de ser explicada | referência removida; ficou "o instantâneo congelado localmente de que este protocolo depende" |
| 23 | 19 | Ad Library não é coleta normal | concordo, e o comentário 24 tornou o ponto moot: a Ad Library sai como rota adotada e passa a ser mencionada só como a rota que **sobra** e não serve, por alcançar apenas publicidade |
| 24 | 19 | trate a dissertação sem Instagram e Facebook | **feito** — ver decisão estrutural 1 acima |
| 25 | 20 | confere se está documentado antes de tirar | conferido: `casos/meta-ads-imigracao/` tem README, plano de replicação, `ARTIGO_CAPOZZI_alvo.md` e a Fase 0 com os gabaritos baixados e o α de Krippendorff reproduzido. A tabela mestre marca as linhas como fora do escopo em vez de apagá-las |
| 26 | 24 | "36,1% em todos os tamanhos" está certo? | **Não estava.** O `curva_midia.json` dá de **35,7% a 36,1%**. Corrigido, e o texto passou a explicar que a constância é **esperada por construção** (subamostras aleatórias do mesmo conjunto estimam a mesma proporção) e que o valor da curva é servir de **régua** contra a qual medir a estimativa publicada |
| 27 | 24 | não dá para pedir 200 tweets aleatórios a uma API | **certíssimo**, e o texto dizia isso mal. Parágrafo novo: nenhuma API atende a esse pedido; o sorteio só existe *depois*, de dentro do que se coletou. Os 200 não economizam **coleta**, economizam a etapa cara deste caso, que é a **rotulagem manual** — 700 lidos à mão para o número errado, 200 bastariam para o certo |
| 28 | 25 | (só marcação) | coberto pelo 27 |
| 29 | 25 | a parte de cima contradiz esta explicação | a recomendação "sortear é barato" foi refeita para não prometer o que a ressalva de baixo desmente, e agora **aponta para ela**: as duas recomendações são complementares, não alternativas |
| 30 | 26 | (só marcação) | coberto pelo 29 |
| 31 | 28 | parágrafo vago e genérico | **concretizado**: as três categorias mais frequentes, com os dois valores cada (política 39,6→38,2; crianças 31,8→30,6; políticas restritivas 31,8→23,4), o maior deslocamento nomeado, e as trocas de posição da 4ª à 6ª colocada declaradas em vez de escondidas atrás de "não reordena" |
| 32 | 29 | não dá para entender nada, extremamente vago | reescrito como "**As apostas registradas antes, e o que elas erraram**", dizendo qual era cada aposta, o que ela acertou, o que errou, e que o achado do caso não foi o que se tinha ido procurar |
| 33 | 29 | 1,50 para um é exatamente o quê? | → "o lado pró reúne entre **1,50 e 1,56 post para cada post** do lado anti. A tabela do artigo reporta 1,02 post por post, isto é, um **empate**" |
| 34 | 29 | não sei o que "monotônica" significa | as duas ocorrências saíram: "sobe **sem recuar em nenhum ponto**" e "cresce **a cada passo** em que o limiar cai" |
| 35 | 30 | será? acho que a comunidade importou para a classificação do artigo | **você tem razão** — ver decisão estrutural 3 acima. "Valida a regra" virou "não se deve ler como validação externa"; a confirmação independente passou a ser atribuída ao eixo de conteúdo |
| 36 | 31 | quais são "os dois trabalhos"? | nomeados no texto (o artigo replicado e esta réplica), com os dois números lado a lado: ele deixa 22,3% dos posts sem lado, ela 9,4% |
| 37 | 31 | argumento forte, escrito de forma confusa; enriquecer com exemplos | reescrito com **a tese na primeira frase** ("no material que viralizou os dois lados aparecem empatados, e no debate de onde ele saiu não aparecem"), com o mecanismo dito em razão simples ("um em cada quatro tweets virais não toma partido, contra um em cada três no debate inteiro") e com exemplos concretos do que é um tweet sem posição |
| 38 | 32 | (só marcação) | coberto pelo 37 |
| 39 | 33 | esse termo precisa estar em inglês? | precisa **porque é do artigo**, e o texto agora diz isso: "que ele nomeia em inglês como *non-relevant/ambiguous*". Ganhou também os três casos reais do gabarito (um meme, um trocadilho, vacinação veterinária) |
| 40 | 33 | "Duas consequências." — queria uma oração completa | → "Disso decorrem duas consequências, uma sobre o artigo replicado e outra sobre o método em geral", e cada uma virou parágrafo próprio |
| 41 | 33 | genérico e confuso: o que exatamente aconteceu? | reescrito em três tempos: a **evidência** (κ 0,759 do classificador contra 0,350 da coautora recodificando), a **causa** (ele nunca viu um tweet neutro porque a convenção do gabarito não tinha essa classe) e o **problema** (o gabarito só existe no estrato sub-coletado, então o instrumento importa as propriedades dele). A direção do viés saiu para um parágrafo à parte |
| 42 | 34 | essa conclusão está ótima — queria o resto assim | é o que os itens 31, 37 e 41 fizeram: a frase-conclusão do capítulo agora tem, acima dela, as três medições ditas na mesma clareza |
| 43 | 34 | esse parágrafo é necessário? o que ele não explica está vago também | ficou, mas **reformulado como limite do que se afirma**: o resultado é que o equilíbrio não se reproduz, e não saber por que o artigo chegou a 1,02 — com as três razões nomeadas, todas do lado do material publicado |
| 44 | 35 | falta o $A_{paper}$, o $A_{máx}$ e a aplicação procedimental do protocolo | **parágrafo novo** amarrando o caso à notação: $N_{paper}$=279, $A_{paper}$=3%, $N_{máx}$=217.386, e a explicação de **por que a curva aqui percorre o limiar de atividade** em vez de frações sorteadas (a quantidade não é média sobre itens, é contagem de quem sobrevive a um corte) |
| 45 | 36 | formata essa tabela | `tabularx` em `\textwidth` + `\footnotesize`; a primeira coluna agora lê inteira, e a legenda diz qual linha decide a questão |
| 46 | 37 | não seria legal ter a imagem da curva? | **Figura 5.1 nova**, com a curva por limiar e a linha dos 3% publicados. Para gerá-la sem digitar número, `analise/rb3.py` ganhou saída JSON (`curva_rb3.json`), foi rodado sobre o snapshot e o JSON entrou no repositório |
| 47 | 37 | "Três, e a primeira…" pede oração completa | → "São três as ressalvas, e a primeira é a que mais pesa" |
| 48 | 38 | técnico demais, não entendi | reescrito: o artigo não publica quem recebeu cada papel, então não se testou a **atribuição de papéis**, e sim a afirmação estrutural de que cada um atua numa comunidade só — que é a base da conclusão do artigo e, ao contrário dos papéis, se conta direto do que se coletou |
| 49 | 41 | "continuação deste protocolo"? "custo de transferência"? | explicado: os arquivos existem, são públicos e o que faltou foi **tempo de download** (arquivos volumosos por torrent), o que é diferente de porta fechada por credencial (TikTok) ou por decisão comercial (Meta). "Uma pendência de tempo se resolve esperando; uma de acesso, não" |
| 50 | 42 | esse não é o lugar de falar disso | **removido** do Cap. 6 — o diagnóstico de Meta e TikTok já vive na §2.4, e o capítulo agora só aponta para lá |
| 51 | 42 | a ressalva de tração não precisa constar | **removida** do Cap. 6 e, pelo mesmo critério, do Cap. 7 (comentário 56). A nota de rodapé com a origem dos números foi preservada |
| 52 | 44 | é erro do artigo ou dá para entender o que ele quis dizer? | **relido o registro do caso** (`DECISOES_regras.md`, D2b, com as quatro frases literais). É contradição real: as duas leituras opostas aparecem **duas vezes cada** e sustentam partes distintas do argumento. Mas o parágrafo foi reenquadrado para dizer que, isolada, a frase se leria como lapso e não valeria registro — o que a torna relevante é o artigo **usá-la como explicação** de dois resultados seus, e não publicar os rótulos que decidiriam |
| 53 | 44 | parece um ataque grande demais aos artigos | **parágrafo removido** do Cap. 6. A observação sobrevive só na Conclusão, onde é sobre reprodutibilidade e não sobre os autores, e lá ganhou a frase que faltava: "Nada disso é acusação aos autores… o que se encontrou foi uma prática de relato em que decisões de operação não são consideradas parte do que se publica" |
| 54 | 44 | capítulo com muito texto corrido; quebrar com gráficos e tabelas | **três objetos novos**: `tab:youtube-funil` (o funil de coleta, etapa a etapa), `tab:youtube-ponto` (as quatro afirmações e sob que condição reproduzem) e a **Figura 6.1**, que põe lado a lado o filtro (−6,4 p.p.) e o funil inteiro (+38,3 p.p.). Mais três subseções quebrando a seção do filtro |
| 55 | 48 | não entendi: como isso foi feito sem coletar mais? | **não foi** — o texto agora diz isso na hora, e não só quatro páginas depois: "Não houve expansão… este caso **não** responde à pergunta 'coletar mais muda a conclusão?'", com o ponteiro para o que ele faz no lugar |
| 56 | 50 | vale manter o caso? não dá para coletar nem com crawler? | **vale, e o capítulo agora argumenta por quê** em vez de se desculpar. Sobre o crawler: três razões, e a terceira é decisiva — a quantidade que o caso mede é **o que desapareceu**, e um raspador de 2026 só alcança o que sobreviveu, de modo que "coletar depois é coletar menos". As outras duas: raspar contraria os termos de uso (a Fase 1 deixaria de ser repetível por terceiros) e o corpus de 2024–25 não é comparável a uma coleta de hoje |

### Correções de erro que a rodada fez de passagem

- Um `\ref` tinha **perdido a contrabarra** numa sessão anterior e saía literal no
  PDF: `Capítulo ef{cap:caso-reddit}`, na Conclusão. Corrigido, e a causa
  provável (substituição por heredoc/`sed`) está registrada na skill.
- A Tabela 1.1 estourava a margem em 7,9 pt — era o que o comentário 11 marcava
  sem texto.
- A dissertação passou a compilar com **zero** `Overfull \hbox` (era 1).

### Pendências que esta rodada **não** resolveu

1. **Front-matter:** faltam **dedicatória** e **epígrafe** (a banca, a data da
   defesa e a bio foram preenchidas nesta rodada).
2. **Modelagem de tópico sem caso executado** — declarado como limitação de
   cobertura e como próximo passo, mas é um buraco real no conjunto de casos.
3. **Instagram/Facebook** — fora da dissertação por decisão sua; o material de
   trabalho segue em `casos/meta-ads-imigracao/` para poder voltar.
4. **[9, rodada 1]** "coletar mais da survey" para reduzir o funil 13.395 → 2.139
   continua sendo trabalho na survey, não na dissertação.

---

## Fora do ciclo: `revisao-3.pdf` republicado (21/ago/2026)

Não é uma rodada de revisão — o `revisao-3.pdf` **ainda não tinha anotação nenhuma**
(verificado com `extrai_comentarios.py`: 0 anotações) quando a Mariana autorizou
republicá-lo com uma inclusão nova. A regra de ouro fica intacta: nenhum PDF já
comentado foi sobrescrito.

**O que entrou:** um `\paragraph{Nota de atualidade.}` fechando a seção *Volume e
largura do filtro respondem ao contrário* do Cap. 4 (caso vacinas). Ele traz o
levantamento da plataforma Torabit divulgado pela BBC News Brasil / Folha em
13/ago/2026 — 93.755 publicações em X, Facebook, Instagram e Bluesky, recolhidas por
um único termo ("vacina") em oito dias, com 65,8% pró contra 34,2% anti entre as
posicionadas.

**Por que ele cabe ali, e não como sétimo caso.** Não é replicável: plataforma
comercial, sem lista de termos, sem gabarito e sem descrição do classificador. Cabe
como ilustração pública porque a seção onde entra já mediu o contrafactual — no mesmo
debate e no mesmo país, a razão pró/anti vai de **1,41 a 7,42** conforme o
termo-índice, e o esquema binário forçado desloca a descrição em **~18 p.p.** O
levantamento publica **1,92** a partir do termo genérico e descarta os 9,4% sem
classificação: são exatamente as duas decisões que o capítulo mostrou serem decisivas.

**Mudanças de arquivo:**

| Arquivo | O quê |
|---|---|
| `corpo.tex` | o parágrafo novo, em `cap:caso-vacinas` |
| `referencias.bib` | entrada `bbc2026vacinas` (`@misc`), com o método do levantamento na `note` |
| `dissertacao.tex` | nenhuma, no fim das contas — o `xurl` entrou e saiu (ver abaixo) |

Compila em **64 páginas**, zero `Overfull`, zero referência indefinida.

✅ **URL canônica resolvida no mesmo dia.** A entrada apontava primeiro para a
republicação na Folha, única URL disponível na hora. A Mariana localizou o original
da BBC News Brasil (`bbc.com/portuguese/articles/c36d27g1d62o`) e a entrada foi
trocada. Efeito colateral: a URL da Folha era longa a ponto de estourar a caixa na
bibliografia e exigiu `\usepackage{xurl}`; com a URL curta da BBC o pacote
virou desnecessário e foi **removido**, e a quebra voltou a cair na barra, que é o
ponto convencional. O `dissertacao.tex` terminou o dia sem alteração.

---

## revisao-3.pdf → revisao-4.pdf (21/ago/2026)

- **Entrada:** `revisao-3.pdf`, 64 p., **20 anotações, todas com comentário**,
  cobrindo **pp. 1–21** (front-matter → meio do Cap. 2). Os Caps. 3 a 8 **não
  foram lidos nesta rodada** — a leitura parou no *Conjunto de casos*.
- **Saída:** `revisao-4.pdf`, **65 p.**, compila limpo: zero erros, zero
  referências indefinidas, zero `Overfull \hbox`.
- **Fonte alterado:** `dissertacao.tex` (resumo PT/EN, epígrafe),
  `corpo.tex` (~30 edições), `referencias.bib` (**4 entradas novas**),
  `thesispuc.cls` (**1 correção de bug** — ver abaixo).

### O que atravessou o documento inteiro

Dois comentários não eram sobre um ponto e sim sobre o texto todo:

1. **Passiva sintética** (comentário 7, declarado por ela como *"crítica para o
   texto geral"*). O `corpo.tex` tinha **46** construções `verbo-se`; ficou com
   **21**. Cortadas primeiro as dos Caps. 1–2, que é o que ela leu, e depois os
   abre-parágrafo mais amaneirados e repetidos do resto: `Registre-se` (×5),
   `Some-se` (×4), `Acrescente-se`, `Comece-se`, `Note-se`, `Segue-se`. Em dois
   trechos o conserto melhorou o sentido além do estilo — *"tomaram-se as cem
   submissões mais votadas"* virou *"o artigo tomou as cem submissões mais
   votadas"*, que diz **quem** fez o recorte. Ficaram as ocorrências em que o
   impessoal é natural e não se repete (`Trata-se de`, `torna-se`, `obtêm-se`).
2. **Legendas inteiras na lista de figuras** (comentário 4). Causa: nenhuma
   figura ou tabela tinha legenda curta, então a lista imprimia o parágrafo de
   legenda completo — a Figura 4.1 ocupava treze linhas. As **4 figuras e as 8
   tabelas** ganharam `\caption[curta]{longa}`. A Lista de figuras passou de
   duas páginas de texto corrido para quatro linhas.

### ⚠ Um bug da classe `thesispuc` apareceu, e foi corrigido

Tirar a página de epígrafe vazia (comentário 1) **quebrou a compilação**, e o
motivo não era a edição: em `\puc@showfrontmatter` (linha 1587 da classe), o
`\if@pucepigraph` **não tem `\fi`**. Com a epígrafe ligada o `\if` fica pendente
e é absorvido adiante sem dano visível — foi assim que as rodadas 1 a 3
compilaram. Com a epígrafe **desligada**, o TeX sai pulando à procura do fecho
que falta e engole `\puc@setmargins@text`, `\onehalfspacing`, `\rmfamily`,
`\puc@setpagestyle` e o próprio `\begin{document}`: erro *"Can be used only in
preamble"* e o documento caindo para 56 páginas sem espaçamento um e meio.

O `\fi` foi acrescentado à classe, com comentário no lugar. **Vale você saber
disso**: o `thesispuc.cls` é o arquivo oficial da PUC-Rio, e a cópia deste
repositório agora tem uma linha a mais que a original. Se a versão final tiver
de sair com a classe intocada, o caminho é reverter essa linha **e** voltar a
chamar `\epigraph` (com uma epígrafe de verdade, ou a página vazia volta).

### Mapa comentário → mudança

| # | p. | O que você pediu | O que foi feito |
|---|----|------------------|-----------------|
| 1 | 1 | tem umas páginas vazias que não precisavam | A p.12 saía com o conteúdo literal `, .` — é a **página de epígrafe**, chamada vazia. As três linhas `\epigraph`/`\epigraphauthor`/`\epigraphbook` foram comentadas e a página sumiu. A dedicatória (p.4) tem texto e ficou. Destravou o bug da classe descrito acima |
| 2 | 6 | a gente não fez nenhum de centralidade né? | **Você tem razão** — nem centralidade nem modelagem de tópico. A frase listava os tipos *mais frequentes do campo*, mas lê-se como o que a dissertação fez. A lista do resumo passou a ser dos tipos **efetivamente instanciados**: detecção de comunidades, análise de conteúdo, sentimento e classificação (PT e EN). A `tab:analises-survey` mantém *Centralidade*: ali é frequência medida no levantamento, e está certo |
| 3 | 6 | "itens" confunde; "publicações" se encaixa | → "1 milhão de **publicações coletadas**" (PT) e "one million **collected posts**" (EN). O termo *item* continua definido na §1.1, onde há espaço para explicar que a unidade muda de plataforma para plataforma |
| 4 | 10 | o título da figura está incluindo a legenda também? mal formatado | **Sim, e era isso mesmo.** Legendas curtas em todas as figuras e tabelas — ver acima |
| 5 | 14 | os ≈2,8 bilhões merecem referência | **Achado e citado.** É Jimeno-Yepes, MacKinlay e Han (2015), *Investigating Public Health Surveillance using Twitter*, BioNLP@ACL-IJCNLP, pp. 164–170. A Tabela 2 do próprio artigo fecha a conta: Decahose 12.000×10⁶ → pré-filtrado 2.800×10⁶ → com entidade médica 28×10⁶, que o artigo rotula "1%". A frase agora diz também **o que** era esse 1%: os tweets com alguma entidade médica |
| 6 | 14 | "o vão" é muito informal | → "a **lacuna**", nas duas ocorrências da passagem |
| 7 | 14 | muita passiva sintética (crítica geral) | 46 → 21 ocorrências. Ver acima |
| 8 | 14 | "O levantamento é o objetivo instrumental que fundamenta este" — engessada | Reescrita dizendo o que ele **faz**: "O levantamento (§1.1) serve a esse objetivo: é ele que mostra que o volume varia por ordens de grandeza e que quase ninguém testa se ele importa, que é o que há para medir" |
| 9 | 14 | ou troca a segunda pergunta da PP1, ou nem bota | **Cortada** — a PP2 já a absorve, e era ela que gerava a confusão do comentário 10 |
| 10 | 15 | PP1 e PP2 não ficam distintas | A confusão vinha da PP1 terminar em "coletar mais era necessário?", que soa igual à PP2. A PP1 ficou só com "muda a conclusão?"; a PP2 ganhou o contraste explícito ("**mude ela ou não**, já havia convergido…"); e o parágrafo seguinte foi reescrito para nomear a diferença: **a PP1 olha os dois extremos da curva, a PP2 olha o caminho entre eles**. Com um exemplo de cada lado — uma conclusão pode mudar sem nunca ter convergido, e pode não mudar por já estar assentada muito antes |
| 11 | 15 | dá pra tirar a subpergunta da PP3 | **Cortada** |
| 12 | 15 | não falta um verbo? | Sim: → "isto é, **para saber** se coletar mais era necessário e se coletar menos teria bastado" |
| 13 | 16 | faltam referências pra reamostragem não parecer invenção | Entraram **Efron (1979)** (o *bootstrap*) e **Efron e Tibshirani (1993)** (o intervalo por percentis, que é exatamente o que o texto descreve). Acrescentei também a frase que diz *por que* é o teste certo aqui: os estimadores em jogo (uma modularidade, uma similaridade entre partições, um $F_1$) não têm distribuição amostral de forma fechada. E, um parágrafo adiante, o **intervalo de Wilson** também era nomeado sem referência — entrou **Wilson (1927)** |
| 14 | 17 | põe entre parênteses a qual capítulo se refere | Os três exemplos ganharam ponteiro: mídia vertical → Cap. 3, dois polos → Cap. 4, homofilia → Cap. 5 |
| 15 | 18 | "no caso do debate vacinal, que será dissecado no capítulo X" | → "no caso do debate vacinal, **dissecado no Capítulo 4**" |
| 16 | 18 | a gente devia ir atrás de um caso com modelagem de tópico, talvez Reddit | **Concordo, e o texto já apontava para lá sem dizer.** O próximo passo era genérico ("sobre um alvo cuja coleta ainda seja acessível") e passou a nomear a rota, com o argumento que a própria §2.4 faz: o Reddit é a **única** plataforma em que coletar mais não depende de credencial nem de acervo preservado, e a infraestrutura já está montada pelos dois casos executados lá. Falta escolher um alvo publicado que modele tópicos sobre um subreddit delimitado. ⚠ **Executar ou não um sétimo caso antes da defesa é decisão sua** — está registrada no `ESTADO.md` §3 |
| 17 | 20 | nunca fale de tempo em semanas | Adotei a sua redação: "obter uma nova **não foi possível dentro do tempo desta pesquisa**". Havia **duas** ocorrências, a da §2.4 e a do Cap. 7; as duas foram trocadas. Ficou uma menção a "semanas" no parágrafo da Meta, mas ela é sobre **o ritmo que a plataforma impõe** ("a cota limita o ritmo… montar um superconjunto exigiria semanas consecutivas de coleta"), e não sobre o seu tempo de trabalho |
| 18 | 20 | não falar do documento verificado | **Cortado.** O argumento não dependia disso: o que fecha a rota da Ad Library é ela alcançar só conteúdo publicitário, que não é comparável ao orgânico dos demais casos |
| 19 | 21 | separar melhor os dois casos de Twitter; ficou estranho | Virou **três parágrafos**: o da exceção que vale para os dois, o do caso de 2014 e o do debate vacinal. De passagem, o segundo ganhou o que faltava para justificar a linha própria — o número da coleta larga (1 milhão) ao lado do estrato analisado (1.525 itens), que é o contraste que define a sub-coleta desse caso |
| 20 | 21 | uma linha por fase | As cinco fases viraram lista `description`. A Tabela 2.3 flutuava para o meio dela e separava a Fase 4 das outras quatro; a lista foi fechada em `samepage` |

### Correções que a rodada fez de passagem

- O `\fi` que faltava no `thesispuc.cls` (ver acima).
- A legenda curta da Figura 5.1 saía justificada apertada na lista de figuras e
  foi encurtada mais uma vez.

### Pendências que esta rodada **não** resolveu

1. **Caps. 3 a 8 não foram lidos nesta rodada** — a leitura parou na p. 21. As
   edições de estilo (passiva) alcançaram esses capítulos, mas o conteúdo deles
   não passou por você desde o `revisao-2.pdf`.
2. **Front-matter:** faltam **dedicatória** (hoje um texto genérico) e
   **epígrafe** (agora ausente por decisão, não por esquecimento).
3. **Modelagem de tópico sem caso executado** — comentário 16. Continua sendo
   trabalho de caso, não de redação, e a decisão de executá-lo é sua.
4. **A classe está patchada.** Se a versão final exigir o `thesispuc.cls`
   original, ver as instruções na seção do bug, acima.

---

## revisao-4.pdf → revisao-5.pdf (22/ago/2026)

- **Entrada:** `revisao-4.pdf`, 65 p., **17 anotações**, 15 delas com comentário,
  pp. 9–56. Primeira rodada em que você passou do Cap. 2 desde o `revisao-2.pdf`.
- **Saída:** `revisao-5.pdf`, **76 p.**, zero erros, zero referências indefinidas,
  zero `Overfull`.
- **Fonte alterado:** `corpo.tex` (capítulo novo + 14 edições), `referencias.bib`
  (**16 entradas novas**), `casos/tiktok/analise/fase2_politok.py` e o JSON dele.

### O que esta rodada mudou de estrutura

**1. Capítulo novo: Trabalhos Relacionados (agora o Cap. 2).** Feita a busca de
literatura que você pediu. O capítulo organiza o campo em quatro linhas — amostra
contra todo, crítica metodológica, replicação e sensibilidade de método — e fecha com
uma tabela de posicionamento. **Resposta à sua pergunta sobre trabalhos parecidos:**
o mais próximo é **Liang e Fu (2015)**, que tirou dez proposições de estudos de Twitter
e testou numa amostra própria de 34.006 contas — **seis das dez não se reproduziram**,
e eles atribuem à variação de coleta e de medida. A diferença de desenho é real e está
escrita: a replicação deles é **independente** (outra população, dois pontos), a nossa
é **pareada** (mesmo tema, coleta do alvo contida na expansão) e percorre o caminho
entre os dois pontos. Nada idêntico ao que você faz apareceu, e o capítulo diz
explicitamente que isso vale para o que a busca alcançou, e não é prova de
inexistência.

**2. A tabela mestre passa a existir no texto.** Você tinha razão: ela era anunciada
como “entregável central” e não aparecia em lugar nenhum — só existia no
`casos/RESULTADOS_tabela_mestre.md`. Agora é a **Tabela 9.1**, numa seção própria da
conclusão (§9.1), com as **quinze linhas fechadas** dos seis casos, e a §3.6 aponta
para lá explicando por que ela não cabe em capítulo de caso nenhum (a unidade dela é o
conjunto).

**3. Seção nova sobre banco de dados (§9.2).** A que você pediu. Ela não entra em
detalhe técnico; faz o argumento em três passos: (a) o levantamento mostra que metade
do campo fica abaixo de ~273 mil itens, volume que cabe em memória — e é provavelmente
por isso que armazenamento nunca aparece como problema nesses trabalhos; (b) mas
**onde a conclusão dependeu do volume, o superconjunto saiu três ordens de grandeza
acima** (279 usuários → 1.015.247 comentários, 700 tweets → acervo de 10,7 M), e o
protocolo não faz uma consulta e sim centenas, porque cada ponto da curva refaz a
mesma agregação sobre um sorteio; (c) a infra usada separa **o banco que preserva**
(Postgres/Mongo do eTC, sem o qual os dois casos de Twitter não existiriam) do
**banco que congela** (os instantâneos SQLite, que tornam o resultado reproduzível e
não exigem servidor). Cita o `salgueiro2022dbmodels`, que estava no `.bib` sem uso.

### ★ O comentário 17 achou um erro de verdade

Você perguntou, sobre o Cap. do TikTok: *“o que a gente está fazendo de diferente do
que o próprio artigo já mostra?”*. Fui ler o full text do alvo, e **você estava
certa**: o PoliTok-DE **já analisa** o crescimento da deleção ao longo do tempo —
Apêndice C, Tabela 5, um painel dos mesmos 102.953 posts rechecados a 1, 3 e 4,5
meses, com a frase explícita de que a fatia deletada cresce quanto mais se espera. O
capítulo apresentava isso como “o achado próprio deste caso”, e isso não se sustentava.

Ao conferir, apareceram mais duas coisas:

- **A série que estávamos publicando misturava bases.** 6,3% → 17,3% → 18,7%: os dois
  primeiros pontos vinham dos posts rechecados naquelas datas, e o terceiro, da
  coleção inteira. Refeito o painel estrito (posts com estado válido nas três datas,
  n = 100.926), a série é **6,3% → 17,4% → 20,9%**, e reproduz a do artigo (6,3 / 17,4
  / 20,5) a 0,4 p.p. no último ponto.
- **A frase “sobe rápido e assenta” não se sustenta.** A outra coleta do mesmo artigo,
  verificada aos 16 meses, marca 39,7% — quase o dobro do que a estadual marca aos 4,5
  meses. Ou as duas não são comparáveis (e o artigo avisa que não as compara), ou a
  curva não tinha assentado. A convergência no eixo temporal **ficou declarada em
  aberto**, na tabela mestre e no texto.

A §8.3 foi reescrita: atribui o fato ao alvo, mantém como contribuição (i) a
verificação independente do painel, (ii) o diagnóstico da base misturada e (iii) a
incorporação do eixo ao protocolo, que é o que de fato é novo. O
`fase2_politok.py` ganhou o bloco `painel_temporal`, e o
[`FASE2_politok.md`](../../../casos/tiktok/FASE2_politok.md) e a
[tabela mestre](../../../casos/RESULTADOS_tabela_mestre.md) foram corrigidos.

### Mapa comentário → mudança

| # | p. | O que você pediu | O que foi feito |
|---|----|------------------|-----------------|
| 1 | 9 | um mestrado em banco de dados e nada fala de banco de dados | **Seção nova §9.2**, descrita acima. Ficou na conclusão, e não na metodologia, porque o argumento depende dos volumes que os casos **de fato** exigiram — antes de ter os casos, ele seria especulação |
| 2 | 12 | “redes sociais digitais” vem do Salgueiro, precisa aludir | Parágrafo de abertura da §1.1 creditando \citeonline{salgueiro2023}, com o que o termo carrega (estrutura conceitual comum a plataformas diferentes) e por que isso autoriza tratar as quatro redes como um objeto só |
| 3 | 12 | cabe um capítulo de trabalhos relacionados | **Capítulo 2 novo**, descrito acima. **16 referências novas** no `.bib` |
| 4 | 14 | PP2 não está clara; a curva é o meio, não a pergunta | Você tem razão e a formulação estava invertida. A PP2 passou a perguntar em termos substantivos (“o volume que o artigo coletou já bastava… ou ela ainda mudaria se ele tivesse coletado um pouco mais?”), e o parágrafo seguinte diz, com essas palavras, que a curva é o **instrumento** que responde à PP2, e não a pergunta |
| 5 | 14 | não gosto do “um em parte”, não sei de qual você fala | Nomeado nos **três** lugares onde aparecia (contribuições, legenda da `tab:casos`, conclusão): é o de TikTok, e “em parte” quer dizer que o ponto original do alvo é reproduzido mas a expansão não ocorre, por credencial revogada |
| 5b | 14 | tem que ser incluído algum trabalho de modelagem de tópico | Busca feita, **fora da dissertação**, como você pediu: [`casos/ALVOS_modelagem_topicos.md`](../../../casos/ALVOS_modelagem_topicos.md). Recomendação e ressalva sobre o pedido “brasileiro” estão lá |
| 6 | 18 | a legenda da Tab. 2.2 parece texto do corpo | A legenda ficou com **uma frase**; a nota sobre algoritmos virou **nota sob a tabela**, em corpo menor e recuada. Mesmo padrão aplicado às tabelas novas |
| 7 | 18 | “Classificação de mídia” na survey é estatística descritiva | Resolvido junto com o 8: cada linha da tabela ganhou uma **segunda linha** dizendo o rótulo correspondente na taxonomia do levantamento. Esta virou *Classificação e Estatística descritiva* |
| 8 | 18 | “Rede e papéis sociais” seria análise de rede? | Sim — *Análise de rede*. A nota da tabela avisa que o rótulo do levantamento nem sempre é o nome que o artigo-alvo dá à própria análise, que é a razão de os dois conviverem |
| 9 | 18 | “no caso do debate vacinal, **por exemplo**” | Adotado literalmente |
| 10 | 18 | devia ir atrás de incluir o caso de modelagem de tópico | Mesmo item do 5b. **O texto não mudou**: a lacuna segue declarada na §3.3 e na §9.3, e o próximo passo já nomeia o Reddit como rota |
| 11 | 19 | *(destaque sem comentário)* | Continuação do destaque do 10, na quebra de página. Sem `Overfull` na região — nada a corrigir |
| 12 | 19 | mencionar que coletar do passado no YouTube perde muito | **Achado e citado**, em parágrafo novo da §3.4: Kurdi, Albadi e Mishra (ASONAM 2020) acompanharam 73 mil vídeos por uma semana e **17,3% já estavam indisponíveis**; Elmas (WebSci 2023) generaliza e mostra que o que some antes da coleta **não some ao acaso**. O parágrafo liga isso ao caso de TikTok, que mede o efeito |
| 13 | 22 | existe essa tabela mestre? por capítulo ela não aparece | **Não existia.** Agora é a Tabela 9.1, na §9.1. Descrito acima |
| 14 | 23 | *(destaque sem comentário)* | Continuação do destaque do 13. Coberto por ele |
| 15 | 26 | não entendi; o que seriam ICs disjuntos? | Explicado **na primeira ocorrência** do termo, com os dois intervalos escritos por extenso (44,6–52,0 e 35,6–36,6) e a frase do que isso quer dizer: não há um único número que sirva de resposta para as duas medições, e como cada intervalo já acomoda o acaso do sorteio, sobra viés de esquema. O terceiro item da lista deixou de repetir a sigla |
| 16 | 26 | não entendo nada desse conceito, não sei se deixa | **Ficou, mas explicado.** A razão de chances é o teste certo aqui porque a comparação é **pareada** (cada autor contra ele mesmo), e é justamente o pareamento que sustenta o argumento do parágrafo. A nota agora diz o que o número significa em português (“para um mesmo autor, a chance é cerca de três vezes maior…”) e o que o Wilcoxon compara. Se ainda assim você preferir tirar, dá — mas aí o parágrafo perde a prova e vira afirmação |
| 17 | 56 | não ficou claro o que a gente faz de diferente do artigo | ★ **Você achou um erro.** Ver a seção acima. Além da reescrita da §8.3, a §8.1 ganhou o parágrafo que faltava dizendo **o que o alvo se propõe a fazer** (é um artigo de conjunto de dados, e a afirmação de maior peso dele é sobre quanto do corpus desaparece) |

### Pendências que esta rodada **não** resolveu

1. **Caps. 4 a 7 quase não foram lidos** — a leitura passou da p. 26 direto para a
   p. 56. Os capítulos do debate vacinal, do Reddit e do YouTube seguem sem comentário
   desde o `revisao-2.pdf`.
2. **Modelagem de tópico continua sem caso executado.** O alvo está escolhido e
   documentado; **abrir ou não o sétimo caso é decisão sua**, e o prazo é apertado.
3. **Front-matter:** falta a dedicatória (hoje genérica).
4. **A classe segue com o `\fi` acrescentado** (ver a rodada 3 → 4).

---

## revisao-5.pdf → revisao-6.pdf (24/ago/2026)

- **Entrada:** `revisao-5.pdf`, 76 p., **23 anotações**, pp. 12–72. A leitura
  alcançou o fim do documento pela primeira vez desde o `revisao-2.pdf` — os
  comentários das pp. 62–72 são os primeiros sobre o Cap. 8 (TikTok) e a conclusão.
- **Saída:** `revisao-6.pdf`, **77 p.**, zero erros, zero referências indefinidas,
  zero `Overfull`.
- **Fonte alterado:** `corpo.tex` (~30 edições), `dissertacao.tex` (preâmbulo:
  legendas + colocação de floats) e `referencias.bib` (entrada nova
  `heine2025amostragem`).
- ⚠ **A rodada foi executada em duas sessões.** A primeira (22/ago) gravou o
  preâmbulo e o `.bib` e abortou num `assert` antes de tocar no `corpo.tex`; a
  gravação é atômica, então nada se perdeu. A retomada (24/ago) está descrita em
  [`rodada-6/RETOMAR.md`](rodada-6/RETOMAR.md), que fica como registro do
  incidente e do procedimento.

### O que atravessou o documento inteiro

**1. A legenda de tabela — a terceira vez que você pede (comentários 2 e 14).**
Desta vez foi tratada na raiz, e não tabela a tabela. No preâmbulo:
`\captionsetup{font=footnotesize, labelfont=bf, labelsep=endash,
justification=raggedright, margin=14pt, skip=6pt}` — a legenda passa a ser
**menor que o corpo do texto**, com o rótulo em **negrito** e separado por
travessão (`Tabela 1.1 – …`, que é o padrão ABNT), recuada das margens. Nenhuma
legenda pode mais ser confundida com parágrafo. Além disso, cada legenda foi
reduzida a **uma frase**, e a explicação desceu para uma *nota sob a tabela* em
corpo menor — padrão que a `tab:tiktok-temporal` e a `tab:mestre` já usavam, agora
estendido a `tab:analises-survey`, `tab:casos`, `tab:reddit-rb3`,
`tab:youtube-funil` e `tab:youtube-ponto`.

**2. A colocação das tabelas (comentário 14).** A queixa de que as tabelas caem em
páginas desconexas do texto que as discute era de posicionamento, e não de
legenda. As tabelas passaram de `[t]` para `[htbp]`, e o preâmbulo afrouxou
`\topfraction`, `\textfraction` e `\floatpagefraction`, que eram o que empurrava
tabela grande para página própria.

**3. O capítulo do TikTok (comentário 18).** *“Esse caso parece forçação, e o
desenrolar é muito técnico.”* A ideia e o capítulo ficam — o problema era a
execução. A §8.3 foi reescrita para (i) mandar as três séries de denominador para
a **nota da tabela**, deixando no corpo uma frase só; (ii) encurtar o parágrafo da
“assimetria” entre as duas perguntas, que era o trecho mais técnico de todo o
capítulo; e (iii) **fechar pelo argumento**, e não pela mecânica — dizer quanto se
coletou sem dizer quando se verificou é publicar um número sem sentido definido.

**4. A dissertação do Alexandre Heine entra (comentário 12).** Você acertou o
enquadramento: ela vai na linha de **amostragem** (§2.1), e não na de replicação.
É o **antecedente mais direto** que este trabalho tem — mesmo orientador, e ele já
mediu amostra contra completo: extraiu amostras de 57,9 M de tweets já coletados e
os tópicos não reproduziram. A diferença de desenho está escrita (ele amostra
*para baixo* a partir de um acervo; esta dissertação coleta *para cima* a partir do
recorte publicado), e o parágrafo amarra na linha em aberto da tabela mestre.

### Mapa comentário → mudança

| # | p. | O que você pediu | O que foi feito |
|---|----|------------------|-----------------|
| 1 | 12 | o parágrafo do Salgueiro é estranho para abrir; virar parêntese no de baixo | Parágrafo removido; o crédito virou **parêntese** dentro da 1ª frase do levantamento, preservando a justificativa de tratar as quatro redes como um objeto só |
| 2 | 13 | legenda × texto corrido, “já não é a primeira vez que eu peço” | Tratada na raiz — ver item 1 acima |
| 3 | 14 | o que é “evidência transferível” | Termo **eliminado** e explicado por extenso: a evidência descreve o *tipo de análise*, não a plataforma, e por isso vale onde essas análises forem feitas |
| 4 | 16 | a abertura do Cap. 2 soa defensiva | “encosta em quatro linhas … e não se confundem com ela” → “apoia-se em quatro linhas já estabelecidas”. O fecho agora **localiza** o trabalho, em vez de defendê-lo |
| 5 | 16 | cada subcapítulo do Cap. 2 devia ter o autor no título; Morstatter é o “original” | Os **4 títulos** ganharam o autor de referência (Morstatter / boyd e Crawford / Liang e Fu / Kossinets), com título curto para o sumário. E o texto passou a dizer que a linha **começa** em Morstatter |
| 6 | 17 | “boyd” com minúscula? | **Nota de rodapé** na 1ª ocorrência: é a grafia que a própria autora adota e registra nas suas publicações, não é erro tipográfico |
| 7 | 17 | o trecho do erro total está artificial | Reescrito **sem o jargão**: decompõem o percurso do dado — quem está na plataforma → o que ela registra → o que a interface devolve → o que o pesquisador filtra — e localizam o erro de cada etapa |
| 8 | 17 | Ruths e Pfeffer ficaram genéricos; falam de rede social? | **Sim.** Trocado pelos três pontos concretos deles: cada plataforma tem população própria; filtro por palavra-chave ou API não é amostra de nada bem definido; contas automatizadas. Mais a recomendação de relato |
| 9 | 17 | o que é “dado social”? | Definido **na primeira menção** (gloss na abertura do capítulo) e por extenso na abertura da §2.2: é a tradução de *social data*, e o traço que importa é que **ninguém o produziu para pesquisar** |
| 10 | 17 | “conclusões ficam ao alcance” não se entende | Reescrito: os conjuntos diferem em tamanho, composição e contas centrais, e por isso a escolha do método de coleta **já delimita que perguntas** o material poderá responder |
| 11 | 17 | “insumo empírico” é rebuscado | → “a evidência” |
| 12 | 17 | a dissertação do Heine tem que entrar; provavelmente em amostragem | Parágrafo novo na §2.1 + entrada `heine2025amostragem` no `.bib` — ver item 4 acima |
| 13 | 19 | as duas ressalvas finais do Cap. 2 não são necessárias | A **primeira** (a busca não achar não prova inexistência) foi **cortada**; a segunda ficou, encurtada. E o parágrafo anterior virou fechamento de verdade |
| 14 | 25 | tabelas em páginas desconexas; a crítica é a **legenda** | Ver itens 1 e 2 acima |
| 15 | 62 | dois “Convém dizer” seguidos; cuidado com repetição no resto | Varredura do texto inteiro: de **11** ocorrências de “convém” sobraram **5**, e as 6 trocadas ganharam formas distintas (*Vale localizar / é preciso dizer / Cabe precisar / é preciso identificar / Note-se / Vale dizer*) |
| 16 | 62 | “códigos de estado”? não se entende | Explicado: o que os autores publicam não é o **motivo** do sumiço, é o **rótulo que a interface devolveu** (`status_deleted`, `status_reviewing`, `status_audit_not_pass`, `author_secret`…) — e o artigo não diz quais deles conta como remoção da plataforma |
| 17 | 62 | isso não é detalhe técnico demais? | Comprimido de 4 frases para **2**, liderando **pelo ponto** (é a mesma classe de achado dos outros alvos) em vez de pela mecânica do voto majoritário |
| 18 | 64 | o caso do TikTok parece forçação e é técnico demais | Ver item 3 acima |
| 19 | 66 | “companion” em inglês; parágrafo longo demais | As **6** ocorrências de *companion* viraram “projeto de replicação” / “reportado em … como parte do mesmo projeto” (hoje **zero** no texto); a abertura do Cap. 9 foi quebrada em **4 parágrafos** |
| 20 | 71 | me perdi nas duas últimas frases da §9.2 | Reescritas em linguagem direta: declarar quanto se coletou é **como se escreve o artigo**; poder coletar mais para verificar é **que infraestrutura se tem** — e sem a segunda o número não é verificável nem pelo próprio autor |
| 21 | 72 | “modelo/ algoritmo” → “modelo e/ou algoritmo” | Adotado literalmente |
| 22 | 72 | limitação do “porquê”: não entendi | Reescrita com **exemplo concreto dos próprios casos** (a partição do debate vacinal ainda se movia; a proporção de mídia de 2014 já estava assentada em 100 tweets), e dizendo que explicar isso exigiria estudar **o método**, e não a coleta |
| 23 | 72 | a limitação de teoria de amostragem pode subir | Movida de **7ª para 2ª** na lista, com “sampling” traduzido e uma frase nova: o trabalho não diz **quanto se deveria coletar**, diz **se o que se coletou bastou** |

### Correção que a rodada fez de passagem

⚠ **O título corrente estourava o cabeçalho em dois capítulos.** Ao conferir as
páginas de tabela — que era o objeto desta rodada — apareceu um defeito que
nenhum comentário tinha apontado e que o `Overfull` não acusa: no **Cap. 8** o
título corrente **encavalava no número da página** (“…Político no TikTok**62**”) e
no **Cap. 6** ele quebrava em duas linhas. Os cinco capítulos de caso ganharam um
`\chaptermark` com título curto (“Sexto Caso, Parcial: o TikTok”, “Terceiro e
Quarto Casos: o Reddit” etc.). O `\chaptermark` mexe **só no cabeçalho** — o
sumário e a abertura de cada capítulo seguem com o título por extenso. Script em
[`rodada-6/ajusta_cabecalho.py`](rodada-6/ajusta_cabecalho.py).

### Pendências que esta rodada **não** resolveu

Herdadas e ainda de pé:

1. **Caps. 4 a 7 seguem quase sem leitura.** A revisão 5 saltou da p. 26 para a
   p. 56; a revisão 6 acrescentou comentários nas pp. 62–72, mas os capítulos do
   debate vacinal, do Reddit e do YouTube continuam sem comentário desde o
   `revisao-2.pdf`. **É o que mais rende na próxima leitura.**
2. **Modelagem de tópico continua sem caso executado.** O sétimo caso
   (`casos/reddit-topicos`, Melton et al. 2021) está **parado no Portão 1**
   esperando decisão sua — ver
   [`PORTAO1_relatorio.md`](../../../casos/reddit-topicos/data/repl/melton2021/PORTAO1_relatorio.md).
3. **Front-matter:** falta a dedicatória (hoje genérica).
4. **A classe segue com o `\fi` acrescentado** (ver a rodada 3 → 4).

Novas desta rodada:

5. **A entrada `heine2025amostragem` usa as iniciais `A. A. P.`**, que é o que o
   material do caso registra. Se você tiver o nome por extenso, vale completar
   antes da versão final.
6. **`labelsep=endash`** mudou o rótulo de `Tabela 1.1:` para `Tabela 1.1 –` em
   **todas** as legendas do documento. É o padrão ABNT e ajuda a separar legenda de
   texto, mas é uma mudança visível em todo o documento — se você não gostar, é
   uma linha só no preâmbulo.

---

## Fora do ciclo: acabamento de entrega (9/set/2026)

Pedido da Mariana: *“quero entregar por agora, e gostaria que ela tivesse com a
maior cara de finalizada possível”*. Auditoria do documento inteiro, mais duas
mudanças de acabamento. **Não é rodada de revisão** — nenhum comentário novo dela
foi consumido, e o `revisao-6.pdf` foi **republicado** no mesmo arquivo (ele ainda
estava com zero anotações, então nada comentado foi sobrescrito).

**[A] O capítulo final deixou de se chamar “Conclusão Parcial e Próximos Passos”
e passou a “Conclusão”.** Era o único lugar do sumário em que o documento
anunciava-se incompleto, e o corpo do capítulo **não se diz parcial em lugar
nenhum**: ele apresenta a tabela mestre com 15 linhas fechadas, a seção de banco de
dados, sete limitações e oito próximos passos — que é exatamente o conteúdo
esperado de uma conclusão. “Próximos passos” continua sendo a §9.4, como é padrão.
O rótulo “Parcial” era autoavaliação de uma fase com menos casos fechados.

**[B] Títulos curtos de sumário nas §2.2 e §2.4.** As duas quebravam em duas linhas
no sumário. A forma curta preserva o autor de referência — que foi o pedido dela no
comentário [5] desta mesma rodada, e que na aplicação tinha ficado com a forma curta
idêntica à longa, sem efeito. O título por extenso segue na abertura da seção.

Script: [`rodada-6/acabamento.py`](rodada-6/acabamento.py). Compila limpo em
**77 p.**, zero erros, zero indefinidas, zero `Overfull`.

### O que a auditoria encontrou de pendente

Não há nada quebrado: bibliografia íntegra (45 entradas, **nenhuma citação órfã**,
nenhuma chave citada e ausente), front-matter com banca, data, ficha catalográfica,
resumo e *abstract* nos dois idiomas, 4 figuras e 10 tabelas. O que falta é:

1. **Dedicatória** — hoje `A todos que apoiaram este trabalho.`, que imprime uma
   página inteira e lê-se como texto de preenchimento. **Só a Mariana pode escrever.**
2. **Agradecimentos** — duas frases (orientador + CAPES). Marcado `TODO` no fonte.
   **Só ela pode escrever.**
3. **Bio (`\resume`)** — uma linha; costuma trazer também o ano de formação.
4. **Cap. 8 ainda se chama “Um Sexto Caso, Parcial”** — é o último “parcial” do
   sumário, e quebra em duas linhas nele. Tirar “Um” e “, Parcial” resolve as duas
   coisas, e a ressalva **não se perde**: a §8.4 (“O que este caso não entrega, e por
   que ainda assim entra”) e a lista de contribuições já a fazem por extenso.
   **Decisão dela** — é moldura científica, não acabamento.
5. **Cap. 6** tem 72 caracteres e também quebra no sumário.
6. **`barreto2026survey` é `@unpublished` / “Manuscrito”**, e é a fonte dos números
   de abertura (Tab. 1.1, o “menos da metade passa de 1 milhão”). Se for submetido
   antes da defesa, trocar a `note` por “submetido a …” fortalece a base do Cap. 1.

---

## Fora do ciclo: mudanças estruturais e fechamento do *stance* (9/set/2026)

Sessão longa, com três frentes. **Não é rodada de revisão** — nenhum comentário novo
foi consumido; o `revisao-6.pdf` foi republicado no mesmo arquivo (segue com zero
anotações). ⚠ **A entrega mudou de data e de natureza:** é **14/set/2026**, e é a
**versão final para a banca** — não um depósito prévio. A defesa segue em 29/set.

### 1. Um capítulo por caso

O Cap. 6 cobria **dois** casos (papéis sociais e homofilia, ambos no Reddit), e era o
único assim. Foi dividido em **6 · Terceiro Caso: Papéis Sociais no Reddit** e
**7 · Quarto Caso: Homofilia no Reddit**.

O argumento que decidiu não foi estético: **os títulos dos capítulos seguintes já
contavam os dois como casos separados** — o YouTube era “Quinto Caso” e o TikTok o
sexto, o que só fecha se o Reddit for o terceiro *e* o quarto. A numeração estava
certa; a estrutura é que não acompanhava. Por isso a divisão **não exigiu renomear**
nenhum capítulo posterior.

Decisão da Mariana sobre a antiga §6.3 (“O que os dois casos acrescentam ao
conjunto”): ela deixa de existir como seção conjunta. **Cada capítulo ganhou a sua
própria conclusão**, sem duplicar, seguindo o padrão “Leitura em termos de volume”
dos Caps. 4 e 5; o **contraste entre os dois** aparece só no quarto caso.

As **10 referências externas** ao antigo `cap:caso-reddit` foram reapontadas uma a
uma — 3 para `cap:caso-papeis`, 4 para `cap:caso-homofilia` e 3 que falavam dos dois
viraram “Capítulos 6 e 7”. Script em [`rodada-6/divide_reddit.py`](rodada-6/divide_reddit.py).

### 2. Cap. 8 perde o “Parcial”

“Um Sexto Caso, Parcial: Deleção…” → **“Sexto Caso: Deleção de Conteúdo Político no
TikTok”**. Era o último “parcial” do sumário e quebrava em duas linhas nele. A
ressalva não se perde: a §8.4 (“O que este caso não entrega…”) e a lista de
contribuições continuam dizendo por extenso que a expansão não ocorreu. **Nenhum
capítulo quebra mais em duas linhas no sumário.**

### 3. O eixo de *stance* fechou, e entrou no texto

Era uma das três linhas em aberto da tabela mestre e estava declarado como pendente em
**quatro** lugares do `corpo.tex`. Agora é a **Seção 4.5** (`sec:stance`), e a tabela
mestre passou de **15 para 16 linhas**.

O desfecho é de dois sinais, e está escrito assim: a fatia sem lado vai de **23,4%
para 65,8%** (muda, e converge em n≈2.000), mas a razão entre os lados fica
**indecidível** (1,01; IC95% [0,36; 2,35], que contém o 0,80 do artigo). ★ O que impede
a conclusão **não é o volume** — a curva é plana desde n=100 — e sim o **teto da
tarefa de rotulagem**. É uma *indeterminação de instrumento*, categoria distinta da
*indeterminação de causa* que o caso do YouTube trouxe.

⚠ **O rotulador automático reprovou o critério pré-registrado** (κ 0,604 < 0,70), e o
texto diz isso com essas palavras. O critério **não foi revisto** depois de conhecido o
resultado — mover a trave depois de ver o número é exatamente a prática que esta
dissertação documenta nos seis casos. A estimativa corrigida entra como leitura
declaradamente *post hoc*, e assim está rotulada em nota de rodapé.

Detalhe completo em
[`RESULTADOS_tabela_mestre.md`](../../../casos/RESULTADOS_tabela_mestre.md) §10.

### 4. Front-matter fechado

As três pendências que só a Mariana podia resolver saíram:

- **Dedicatória** — “Aos meus pais, Mauro e Regina, e ao meu irmão Marcelo, que
  estiveram do meu lado em todas as minhas jornadas.” Texto dela, com **uma correção
  gramatical**: vírgula após “Regina”, para fechar o aposto — sem ela, “Regina e ao
  meu irmão” se lê como um par, e não como pai, mãe e irmão;
- **Agradecimentos** — acrescentados a **banca** (nominalmente) e a **família**, na
  ordem convencional: orientador → banca → família → CAPES;
- **Bio** — graduação em **2023**, ingresso no mestrado em **2024**, mais a área de
  pesquisa.

Os dois `TODO` que restavam no `dissertacao.tex` foram removidos.

### Estado do documento

**80 páginas**, zero erros, zero referências indefinidas, zero `Overfull`.
**10 capítulos, um caso por capítulo.** Nada mais bloqueia a entrega.

### Pendências que esta sessão **não** resolveu

1. **Modelagem de tópico** segue sem caso executado — declarada como limitação (§9.3)
   e próximo passo (§9.4). Com 5 dias, fica assim.
2. **O reteste intracodificador de 40 itens não foi feito**, e não será: 26 dos 40
   vinham do teste rotulado no mesmo dia, e os ≥7 dias exigidos cairiam em 16/set,
   depois da entrega. O teto foi estimado pelas **duplicatas do dev** — medida mais
   frágil (15 pares), e o texto a reporta como tal.
3. **A classe segue com o `\fi` acrescentado** (ver a rodada 3 → 4).
4. `barreto2026survey` segue `@unpublished`/“Manuscrito”.
