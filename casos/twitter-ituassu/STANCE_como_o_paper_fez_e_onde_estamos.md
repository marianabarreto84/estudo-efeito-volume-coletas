# Classificação de preferência eleitoral (*stance*): como o artigo fez e onde estamos

> Documento didático. Não pressupõe nenhum conhecimento prévio do tema. Se você
> nunca ouviu falar deste projeto, comece por aqui — em ~10 minutos você entende
> o que estamos replicando, o que já foi feito automaticamente, e qual é a única
> parte que **só um humano pode fazer**.

---

## 1. O contexto em uma página

O mesmo grupo da PUC-Rio (**Arthur Ituassu, Sérgio Lifschitz** e colegas) publicou
**dois artigos** sobre os mesmos dados das **eleições presidenciais de 2014**
(2º turno: **Dilma Rousseff × Aécio Neves**), analisando o público da hashtag
**#Eleições2014**:

- **2015** (E-Compós) — preliminar, **700 tweets** (100/dia × 7 dias), tipologia de
  mídia **MV/MH**.
- **2018** (Palabra Clave) — expandido e agora nosso **alvo primário**, **1.129
  tweets** (200/dia aleatórios), tipologia **MP/MC** (mídia principal/complementar)
  e um **teste estatístico** (Qui-quadrado). Detalhe em
  [PAPER2018_palabra_clave.md](PAPER2018_palabra_clave.md).

As perguntas do público continuam as mesmas:

1. **Quem é o público?** — cada pessoa parecia torcer por Dilma ou por Aécio?
2. **Que mídia esse público reproduz?** — quando põe um link, é de grande mídia
   (Globo, UOL, Folha…) ou de mídia complementar/nicho (blogs, redes sociais)?
3. **Sobre quais temas fala?** — *(o 2018 abandonou o eixo temas; fica só no 2015.)*

O detalhe importante: eles tinham **>200 mil** tweets, mas analisaram **só uma
amostra pequena** — 700 (2015) / 1.129 (2018) — e tudo **na mão**, lendo um por um.

**Nosso projeto** ("replicação por expansão") pergunta: *e se, em vez de 700/1.129,
a gente usar o universo inteiro de tweets que ainda está guardado no banco da PUC?
As conclusões se mantêm, ou eram artefato da amostra pequena?* Ganhamos um trunfo:
o **próprio grupo já expandiu uma vez** (700 → 1.129) e **uma conclusão virou** no
caminho (a hipótese de que os públicos diferiam no tipo de mídia — ver
[PAPER2018 §5](PAPER2018_palabra_clave.md)). Temos, então, **dois pontos reais da
curva** antes de chegar ao universo.

> **Onde os dados moram:** um banco PostgreSQL na VM `vm067` da PUC-Rio, tabela
> `ituassu_2014`, com **10,7 milhões** de tweets coletados em out/2014.

---

## 2. As três análises do artigo (e por que só uma trava)

O artigo tem três análises. Duas delas nós conseguimos refazer **automaticamente
com o computador**; uma **precisa de humano**. Veja por quê:

| Análise | O que é | Precisa de humano? |
|---|---|---|
| **Mídia (MP/MC)** | o link do tweet é de mídia principal ou complementar? | ❌ Não — dá pra decidir pelo **domínio do link** (g1.com = mídia principal). **Já feito sob MV/MH; migrando para MP/MC.** |
| **Temas** | sobre o que é o tweet? (pesquisa, corrupção…) | ⚠️ Só no 2015 — o 2018 abandonou este eixo. Automatizável com topic modeling, com ressalvas. |
| **Preferência eleitoral (*stance*)** | a pessoa torce por Dilma ou por Aécio? | ✅ **Sim** — depende de **interpretar o sentido** do texto. É o foco deste documento. |

**"Stance"** (palavra em inglês para "posicionamento") é o rótulo de preferência
eleitoral que o artigo atribuiu a cada tweet. São três valores:

- **EA** = **E**leitor de **A**écio
- **ED** = **E**leitor de **D**ilma
- **NDA** = **N**ão-**D**eterminado/**A**mbíguo (não deu pra saber a preferência)

---

## 3. Como o artigo decidiu o *stance* (o método manual, passo a passo)

Foi **100% manual**: os pesquisadores **leram os 700 tweets, um por um**, e
seguiram três camadas de decisão.

### Camada 0 — "Isto é um cidadão comum?"
Antes de tudo, eles **jogavam fora** contas que não eram de pessoas comuns:
empresas, veículos de imprensa, órgãos do governo, partidos. Só sobravam os
**"perfis individuais"** (cidadãos).
→ Dos 700 tweets, **666 eram de cidadãos**.

### Camada 1 — Sinais explícitos de torcida
Procuravam pistas óbvias no perfil ou no texto — por exemplo, **hashtags que já
declaram lado**. O artigo cita duas, **sem dizer de que lado cada uma está**:

- `#ForaDilma` → contra Dilma → **EA**
- `#Aécionever` → "nunca Aécio", ou seja, **contra Aécio** → **ED**

> ⚠ **Correção de 18/ago/2026.** Este trecho dizia que as **duas** eram "contra
> Dilma → EA". É falso para `#AecioNever`. Medido nos dados (`analise/lean_hashtags.py`):
> nas 157 ocorrências da janela ela co-ocorre **84×** com hashtags declaradamente
> pró-Dilma e **0×** com pró-Aécio. A lista completa, com o lado medido de cada
> hashtag frequente, está no [CODEBOOK_stance.md](CODEBOOK_stance.md) §7.

### Camada 2 — O "tom" da mensagem (a regra central)
Quando não havia sinal óbvio, liam o **tom** do tweet e aplicavam esta regra
(a chave de tudo):

> - Falou/linkou algo **negativo contra um candidato** → é eleitor do **adversário**.
> - Falou/linkou algo **positivo a favor de um candidato** → é eleitor **dele**.
> - Não deu pra decidir / é apolítico → **NDA**.

A lógica: quem ataca Dilma provavelmente vota em Aécio, e vice-versa.

### Camada 3 — Revisão em grupo
Como "ler o tom" é **subjetivo**, **cinco pesquisadores juniores** conferiam as
classificações e apontavam divergências. (Guarde este detalhe — ele volta na
Seção 6: é a origem da ideia de "mais de um anotador".)

---

## 4. Os exemplos reais do artigo (com os tweets originais)

Estes são os casos que os próprios autores usaram para ilustrar a regra. Servem
como "gabarito" de como pensar cada rótulo.

### Exemplo → **ED** (eleitor de Dilma)
> Um usuário publica, em 8/out/2014, um tweet com link e a mensagem:
> **"32 capas de jornal que vão te lembrar do Brasil dos anos 90 e governo FHC"**

Por quê ED: o conteúdo é **negativo ao governo FHC (PSDB, o partido de Aécio)**.
Atacar o lado do Aécio ⇒ classificado como eleitor de **Dilma**.

### Exemplo → **EA** (eleitor de Aécio)
> Um usuário publica um link para uma página no Facebook com um pequeno vídeo de
> um cachorro que **late e avança quando a dona fala "Dilma"**, e **brinca quando
> ela fala "Aécio"**.

Por quê EA: a "piada" é **negativa a Dilma** e simpática a Aécio ⇒ eleitor de
**Aécio**.

### Exemplo → **EA** (sinal explícito + tom em CAIXA ALTA)
> A usuária "E", às 16h51, **retuíta** um post do perfil @BR_indignado e afirma
> em letras garrafais:
> **"DILMA JÁ FOI ENQUADRADA. ELA SABIA DE TUDO SIM"**
> (com link para o conteúdo da capa da revista *Veja* que acusava Dilma).

Por quê EA: ataque direto a Dilma, capitalizando a denúncia da *Veja* ⇒ **Aécio**.

### Exemplo → **NDA** (não-determinado)
> O usuário "C" posta:
> **"Vc aí falando de Aécio e Dilma... Ruim mesmo é o Chico Buarque!!! Chatinho
> e canta maaaal pra dedé!"**

Por quê NDA: **não toma lado** entre os candidatos — é uma mensagem apolítica
(ou "praga a nos dois"). Não dá pra inferir preferência ⇒ **NDA**.

### Outro caso de **NDA** (cansaço/apolítico)
> O usuário "D", às 21h47:
> **"Cansado dessa ladainha entre DILMA x AECIO! que passe logo esse domingo"**

Reclama dos dois igualmente ⇒ sem preferência ⇒ **NDA**.

---

## 5. O que o artigo encontrou (os números-alvo da replicação)

**No 2015** (após rotular os 666 cidadãos):

| Rótulo | Quantidade | O que significa |
|---|--:|---|
| **ED** (Dilma) | **284** | maioria |
| **EA** (Aécio) | **226** | |
| **NDA** | **156** | não deu pra decidir |

**No 2018** (Amostra D = 1.129, quem tinha mídia **e** preferência identificável):

| Rótulo | Quantidade | O que significa |
|---|--:|---|
| **EA** (Aécio) | **581** | maioria |
| **ED** (Dilma) | **548** | |

> 🔀 **A maioria inverteu entre os dois papers** — 2015 dava Dilma (ED), 2018 dá
> Aécio (EA). As amostras são definidas de formas diferentes (a de 2018 é
> condicionada a ter compartilhado mídia), então não é comparação limpa — mas já é
> um sinal de que a composição fina é **instável**. São esses números que vamos
> tentar reproduzir no universo para ver o que sobrevive.

---

## 6. Onde estamos AGORA

Pense no projeto como três trilhos. Este é o mapa:

```
[✅ FEITO - automático]  Eixo MÍDIA (MV/MH, convenção 2015)
     → descobrimos que a conclusão (retweet de grande mídia > 50%) SÓ vale
       na amostra pequena; no universo cai de 48% para 36%, e no escopo amplo
       para 20%. A amostra exagerava o efeito. (relatórios já gerados)

[🔧 A REFAZER - automático]  Eixo MÍDIA sob MP/MC (convenção 2018)
     → migrar o dicionário para as 26 marcas MP do 2018 e retestar; medir
       também o "efeito-de-taxonomia" (quanto muda só por trocar MV/MH→MP/MC).

[🟡 PRÓXIMO - precisa de humano]  Eixo STANCE (EA/ED/NDA)  ← VOCÊ ESTÁ AQUI
     → travado. Não dá pra ler 32 mil+ tweets à mão, e o computador só pode
       automatizar DEPOIS que humanos criarem um "gabarito" para ele aprender
       e ser testado.

[⬜ DEPOIS]  Eixo TEMAS + curva de volume/tempo (Fases 2-3)
     → fazem mais sentido depois do stance.
```

### Por que o stance trava tudo
As perguntas mais interessantes do artigo (havia mais eleitores de Dilma?
os dois públicos falam de temas diferentes?) **dependem do rótulo EA/ED/NDA**.
E esse rótulo depende de **interpretar o sentido** de cada tweet — algo que:

- **à mão** é inviável no universo (32 mil a 58 mil+ tweets);
- **por computador** só funciona se antes existir um **"gabarito humano"** para
  (a) ensinar/ajustar o classificador e (b) **medir se ele acerta**.

---

## 7. O que nós humanos precisamos fazer (a única parte irredutível)

A tarefa humana chama-se **criar um *gold set*** ("conjunto-ouro" = gabarito):

> **Rotular à mão uma amostra de tweets** (marcar EA / ED / NDA em cada um,
> seguindo a regra da Seção 3), para servir de verdade-fundamental.

Esse gabarito serve para duas coisas:
1. **Validar** o classificador automático — comparar máquina × humano e medir o
   grau de acerto (uma métrica chamada **κ / "kappa"**, ver glossário).
2. **Medir a concordância entre anotadores** — replicando os "5 pesquisadores"
   do artigo (se duas pessoas discordam muito, o próprio rótulo é frágil).

### O que exatamente você decide/faz

| Item | Decisão de vocês |
|---|---|
| **Quantos tweets rotular** | ~400–500 (como o paper) ou ~200 só para validar |
| **Quantas pessoas rotulam** | idealmente **≥2** (para medir concordância) |
| **Seguindo qual regra** | a codebook da Seção 3 (eu formalizo num guia) |
| **A ação em si** | ler cada tweet e marcar **EA / ED / NDA** (e cidadão: sim/não) |

**Todo o resto é automático e por minha conta:** eu sorteio a amostra do banco,
monto a planilha já com o texto e os links de cada tweet e as colunas de rótulo,
calculo a concordância, e — se o resultado for bom — aplico o classificador no
universo inteiro e refaço as tabelas do artigo em escala.

### Quem/o quê será o classificador automático?
Depois do gabarito pronto, o "robô" que rotula os 32 mil+ pode ser um **LLM**
(uma IA de linguagem, como a que escreve este texto) ou um **modelo de PT-BR
treinado**. Mas isso é decisão da fase seguinte — **nada avança sem o gabarito
humano primeiro**.

---

## 8. Glossário (para quem caiu de paraquedas)

- **Tweet / retweet (RT):** post no Twitter; retweet = repostar o de outra pessoa.
- **Hashtag:** palavra com `#`, ex. `#Eleições2014`, usada para agrupar assuntos.
- **Stance / preferência eleitoral:** o lado político do tweet — aqui **EA**
  (Aécio), **ED** (Dilma) ou **NDA** (indefinido).
- **MV / MH (mídia vertical/horizontal, 2015):** MV = grande mídia (Globo, UOL…);
  MH = mídia de nicho/alternativa/redes sociais. Critério = *fluxo* da informação.
- **MP / MC (mídia principal/complementar, 2018):** MP = lista fechada de 26 grandes
  marcas (PBM 2014); MC = todo o resto, incl. redes sociais. Critério = *proeminência
  da marca*. É a convenção primária agora — ver [PAPER2018 §2](PAPER2018_palabra_clave.md).
- **RTMV:** retweet de conteúdo de mídia vertical — a métrica central da 1ª
  hipótese (H1) do paper de 2015.
- **Universo × amostra:** universo = todos os tweets; amostra = o pedacinho
  (700) que o artigo analisou.
- **Snapshot:** uma cópia congelada dos dados que baixamos do banco para o
  computador local, para a análise ser reproduzível e não depender da rede.
- **Gold set / gabarito:** tweets rotulados à mão que servem de verdade-de-referência.
- **κ (kappa de Cohen):** número de 0 a 1 que mede o quanto duas classificações
  concordam além do acaso (quanto mais perto de 1, melhor). Serve para dizer se o
  classificador automático é confiável.

---

## 9. Próximo passo concreto — ◐ **dev fechado, falta o teste cego** (22/ago/2026)

O kit existe e está congelado desde 18/ago. Em **22/ago/2026** a rotulagem começou: o
**dev (110)** fechou em duas rodadas — `v1` cego e `v2` revisto contra uma pré-anotação
automática declarada — e as três lacunas de regra que ele revelou já viraram os
casos-limite 13 e 14 do codebook. **Falta o teste cego de 210**, que é o conjunto de onde
sai o κ do critério de aceite. Números, desenho e decisões em
[DECISOES_ROTULADOR.md](data/repl/compos2014/stance/DECISOES_ROTULADOR.md).

| artefato | onde |
|---|---|
| **Codebook** (guia operacional, com os casos-limite decididos) | [CODEBOOK_stance.md](CODEBOOK_stance.md) |
| **Planilha para preencher** (320 tweets, já com texto, host do link e metadados) | `data/repl/compos2014/stance/gold_stance_para_rotular.csv` |
| **Planilha do reteste** (40 itens, ≥7 dias depois) | `.../stance/gold_stance_RETESTE.csv` |
| **Pré-registro** (split congelado, apostas, critério de aceite) | [.../stance/PRE_REGISTRO_stance.md](data/repl/compos2014/stance/PRE_REGISTRO_stance.md) |
| Sorteador (reprodutível, seed `20260818`) | `analise/amostra_stance_humana.py` |

**Como usar (atualizado em 22/ago/2026):** o caminho recomendado deixou de ser o Excel.
Abra `data/repl/compos2014/stance/rotulagem_dev.html` no navegador — um tweet por tela,
atalhos de teclado, o codebook resumido ao lado, salvamento automático e exportação no
formato exato do gold set. Comece pelas **110 do dev**, em lotes de 20: ao fechar cada
lote, a página mostra a **pré-anotação automática** e as divergências, para afinar o
codebook antes do que conta. As **210 do teste** são rotuladas **sem** pré-anotação —
é delas que sai o κ. O desenho e o porquê estão em
[DECISOES_ROTULADOR.md](data/repl/compos2014/stance/DECISOES_ROTULADOR.md).
O CSV no Excel continua valendo como alternativa (preencher `cidadao`, `stance`,
`confianca`, `notas`). Se houver uma segunda pessoa, ela preenche uma **cópia** do mesmo
arquivo (aí sai o κ humano×humano). Depois disso a validação e a aplicação em escala são
automáticas.

*(Este documento cobre só o eixo stance. O plano completo das fases está em
`REPLICACAO_CASO_COMPOS2014.md`; os resultados do eixo mídia em
`data/repl/compos2014/RESULTADOS_FASE0_midia.md` e `RESULTADOS_E2_escopo_midia.md`.)*
