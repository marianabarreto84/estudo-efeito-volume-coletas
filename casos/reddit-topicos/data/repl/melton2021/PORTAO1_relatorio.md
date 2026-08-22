# Portão 1 — relatório e pedido de decisão

> Caso [`reddit-topicos`](../../../README.md) (Melton et al. 2021), aberto em
> **22/ago/2026**. Este é o item (d) do Portão 1 do
> [`PROMPT_caso_topicos.md`](../../../../PROMPT_caso_topicos.md): *relatar tamanho da
> população, rota viável, disco e tempo, e **parar** se a estimativa passar de ~24 h
> ou exigir Academic Torrents.*
>
> **Veredito: PARADO, esperando decisão da Mariana.** O motivo não é o que o prompt
> antecipava (custo alto demais). É que **o dimensionamento não pôde ser concluído**:
> o Arctic Shift aplica um rate limit agressivo, e o prompt manda **parar, não
> contornar**.

---

## 1. O que o Portão 1 fechou

| item | estado |
|---|---|
| **(a)** full text lido, afirmações numeradas | ✅ **feito** — [`ARTIGO_MELTON_alvo.md`](../../../ARTIGO_MELTON_alvo.md) |
| **(b)** dimensionamento da população | ◐ **6 de 13** subreddits; os 3 maiores ficaram de fora |
| **(c)** banimentos | ✅ **feito** (§4) |
| **(d)** relatório e decisão | ✅ este arquivo |

---

## 2. ★ O que já se sabe é suficiente para dizer que a sub-coleta é grande

Os **6 subreddits menores** — medidos duas vezes, em rodadas independentes que
concordam item a item ([`volume_portao1_parcial.json`](volume_portao1_parcial.json)) —
já contêm, na janela do artigo:

| subreddit | submissões | comentários |
|---|--:|--:|
| Vaccines | 1.148 | 4.216 |
| CovidVaccine | 2.432 | 18.641 |
| CovidVaccinated | 12.385 | 100.316 |
| AntiVaxxers | 1.380 | 15.643 |
| vaxxhappened | 2.788 | 55.927 |
| antivaccine | 222 | 296 |
| **parcial (6/13)** | **20.355** | **195.039** |

**215.394 itens**, contra os **11.641** que o artigo analisou (M4) — **18,5×**, e isso
**sem** os sete subreddits restantes, entre eles `conspiracy`, `COVID19` e
`coronavirus`, que são os grandes. Só em submissões são **20.355 × 1.401 = 14,5×**.

⚠ **Ressalva honesta de comparabilidade.** O corpus do alvo é *pós-filtro de termo*
(os 22 termos de M3) e o nosso parcial é a população bruta. Filtrar por termo vai
reduzir o nosso lado, e por quanto é justamente o que a Fase 2 mediria. Portanto
**18,5× é o teto do fator, não o fator**. Mesmo assim a ordem de grandeza é a do caso
[`reddit-buntain`](../../../../reddit-buntain/README.md), e a direção não está em dúvida:
`CovidVaccinated` **sozinho** tem 112.701 itens, quase 10× o corpus inteiro do artigo.

---

## 3. ⚠ Por que o dimensionamento parou: o rate limit, e o que ele é de fato

A **primeira** sonda usava o endpoint de agregação com **divisão adaptativa**: tenta a
janela inteira e, se falhar, parte ao meio, recursivamente. Foi desenhada para vencer o
problema que travou o [`reddit-massachs`](../../../../reddit-massachs/README.md).

Ela venceu nos 6 menores e travou depois. O diagnóstico, feito com sondas espaçadas:

- o erro é sempre `{"data":null,"error":"Timeout. Maybe slow down a bit"}`;
- ⭐ **o mesmo erro aparece por dois motivos diferentes**, e a mensagem não os
  distingue:
  1. **Estrangulamento.** `antivaccine` (222 submissões — trivial) **falhou** durante
     o uso intenso e **respondeu normalmente após ~5 min de silêncio**. Não tem
     nada a ver com o tamanho da consulta.
  2. **Tamanho real.** `conspiracy` na janela inteira **falhou em 14 s mesmo depois
     de 5 min de silêncio total**. Aí a agregação não cabe mesmo.
- o limiar de recuperação medido: 30 s e 120 s de silêncio **não** bastam; **300 s**
  bastam.

**Consequência para a sonda:** a divisão adaptativa interpreta *todo* erro como
"consulta grande demais" e responde **fazendo mais chamadas** — que é exatamente o
que agrava o estrangulamento. Dá para ver nos [`logs/`](logs/): na 2ª rodada, `Vaccines`
custou **16 chamadas** e granularidade de 5 dias para chegar ao **mesmo número** que na
1ª rodada custara **4 chamadas** a 83 dias. A sonda entrava em espiral.

✅ **Consertado em 22/ago/2026.** A sonda velha foi aposentada e substituída por
[`pipeline/dimensiona.py`](../../../pipeline/dimensiona.py), sobre
[`core/agregacao.py`](../../../core/agregacao.py), que faz **ladrilho adaptativo com
descanso**: em vez de dividir na primeira falha, ele **descansa 300 s e repete a mesma
janela** — se passar, era estrangulamento e o ladrilho fica; se falhar de novo, era
tamanho e só então o ladrilho encolhe. O descanso é o **discriminador** entre as duas
causas, e por isso ele só é pago quando há estrangulamento de fato. O script é
retomável (grava progresso a cada janela fechada), roda sem dependência externa e
serve também à reconferência do Massachs (`--caso massachs`).

> ⚠ **Isto tem efeito colateral sobre o caso `reddit-massachs`**, e é preciso dizê-lo
> com cuidado. Lá, a Fase 3 foi declarada *não dimensionável* porque "34/34
> agregações voltaram incompletas" — **com esta mesma mensagem de erro**. O que se
> aprendeu aqui é que a mensagem **também** significa estrangulamento, e uma sonda
> que insiste rápido produz falhas que parecem de tamanho. Isso **não** derruba o
> veredito de lá: os subreddits do Massachs (`politics`, `news`, `worldnews`) são
> grandes, e para grandes a falha é real, como `conspiracy` mostrou. Mas o
> "34/34" pode estar inflado por estrangulamento, e **o veredito merece uma
> reconferência paciente** antes de virar afirmação definitiva na dissertação.

---

## 4. Portão 1(c) — os banimentos

A API oficial do Reddit devolveu **403 nos 13** (acesso automatizado bloqueado), então
"perguntar ao Reddit" não serve de teste. O que se pôde estabelecer:

- ⭐ **`NoNewNormal` foi banido em 1º/set/2021**, por *brigading* — não por
  desinformação. Reddit também colocou em quarentena outros 54 subreddits negacionistas
  na mesma data ([Forbes](https://www.forbes.com/sites/carlieporterfield/2021/09/01/reddit-bans-controversial-covid-subreddit-after-users-protest-disinformation/),
  [CNN](https://www.cnn.com/2021/09/01/tech/reddit-covid-misinformation-ban/index.html),
  [Vice](https://www.vice.com/en/article/reddit-just-banned-one-of-the-biggest-subreddits-for-covid-19-misinformation/)).
- O banimento é **posterior** à coleta do artigo (16/mai/2021), então os autores
  alcançaram o subreddit. **Quem tentasse replicar o artigo hoje por PRAW não
  alcança** — é achado da tese, e do tipo que ela já coleciona: a rota oficial não
  reproduz nem o passado recente.
- ⏳ **`antivaccine` ficou indeterminado.** O script
  [`pipeline/checa_bans.py`](../../../pipeline/checa_bans.py) está pronto — ele decide
  por *atividade no arquivo* em três janelas (a do artigo, pós-banimentos de 2021, e
  2026) — mas **não foi rodado**, porque roda no mesmo endpoint estrangulado. Nota:
  `antivaccine` tem só **222 submissões** em 5,5 meses, ou seja, é praticamente
  inativo já na janela do artigo, o que por si só é dado interessante sobre a
  composição dos 13.

---

> ⭐ **ATUALIZAÇÃO de 22/ago/2026, posterior a este relatório — leia antes das §5 e §6.**
> A pergunta que as §5 e §6 tratam como aberta ("coletar é viável, mesmo com agregar
> impossível?") **foi medida, e a resposta é sim.** `conspiracy`, o maior dos 13,
> **coleta normalmente** pelo `/search` paginado: 684 submissões em 7 páginas/13 s, e
> **5.050 comentários em 51 páginas/97 s, sem uma falha** — enquanto a *agregação* do
> mesmo subreddit falha até em janela de 5,2 dias. São endpoints com custo diferente:
> agregar varre e conta, paginar entrega 100 por vez.
>
> **A rota está aberta, e a recomendação da §6 fica mais otimista do que está escrita
> ali.** Medido: 0,29 kB/item (comentário) e 0,46 kB/item (submissão); ~3,35 M
> comentários de `conspiracy` na janela, ~1 GB. Evidência em
> [`teste_coleta.json`](teste_coleta.json); estado e próximos passos em
> [`RETOMAR.md`](../../../RETOMAR.md).
>
> ⚠ E o **dimensionamento por agregação deixou de valer a pena**: amostrar janelas de
> 24 h por paginação e extrapolar é mais barato e funciona nos grandes. Ainda não
> implementado.

## 5. Rota, disco e tempo — o que dá e o que não dá para afirmar

**Não dá para dar a estimativa que o item (d) pede.** Faltam 7 subreddits, entre eles
os três maiores, e são eles que dominam o total. Qualquer número agora seria chute.

O que dá para dizer:

- **A ordem de grandeza provável** da população dos 13 é de **milhões** de itens
  (`conspiracy` e `coronavirus` em pleno pico da pandemia). Para comparação, o
  [`reddit-buntain`](../../../../reddit-buntain/README.md) coletou **1,06 milhão** de
  itens pelo Arctic Shift, a **95 itens/s medidos**, e fechou. A 95 itens/s, 5 milhões
  de itens dariam **~15 h** — dentro do teto de 24 h do prompt.
- ⚠ **Mas o caso do Melton precisa do TEXTO**, e o Buntain não precisava (RB3 é
  estrutural, coletou só `author`+`subreddit`+`created_utc`). Com corpo de post e de
  comentário, o item fica muito maior: a 1–2 kB/item úteis, 5 milhões de itens são
  **5–10 GB** em disco e uma taxa efetiva menor que 95 itens/s.
- ⭐ **A pergunta que decide a rota ainda não foi respondida, e é barata de
  responder:** o endpoint que estrangulou é o de **agregação**, que varre e conta o
  período inteiro numa chamada. A **coleta** do Buntain usa outro caminho —
  `posts/search` paginado em `limit=100` —, que é barato por chamada e **funcionou por
  horas em ago/2026**. É perfeitamente possível que **coletar seja viável mesmo com
  agregar impossível**. Um teste de 10 minutos resolve: paginar `conspiracy` por
  algumas horas de janela e medir a taxa sustentada.
- **A rota alternativa é o Academic Torrents** (dump por subreddit), que o prompt
  marca explicitamente como gatilho de decisão da Mariana.

---

## 6. O que eu recomendo

**Não abandonar o caso, e não commitá-lo ainda.** O alvo se mostrou melhor do que o
levantamento previa, e o custo real continua desconhecido por um motivo que se
conserta. Na ordem:

1. **Rodar o teste de taxa sustentada do `posts/search` paginado** (10 min de trabalho,
   depois de deixar o limitador descansar). Ele decide entre "Arctic Shift serve" e
   "só Academic Torrents serve", que é a bifurcação inteira do custo.
2. **Consertar a sonda** para recuar em vez de dividir quando a mensagem for de
   estrangulamento, e **refazer o dimensionamento** dos 7 que faltam, devagar.
3. Só então **estimar disco e tempo** e trazer a decisão de commit para a Mariana.

⚠ **O que NÃO recomendo:** contornar o rate limit (paralelizar, trocar User-Agent,
distribuir requisições). O prompt proíbe, e com razão — o Arctic Shift é
infraestrutura pública mantida por voluntários, e os outros dois casos de Reddit da
dissertação dependem dela.

### Se a decisão for não seguir

O caso **já rende** como próximo passo, e mais do que o `ALVOS_modelagem_topicos.md`
previa: alvo escolhido e lido, afirmações numeradas, **gabarito do modelo ajustado dos
autores congelado**, quatro divergências internas do artigo documentadas, a sub-coleta
medida em ≥18,5× no *pior* recorte, e a rota de coleta diagnosticada. A §9.4 do
`corpo.tex` passaria a apontar para um caso instruído, não para uma rota genérica.

---

## 7. Achados do Portão 1 que valem por si

1. ⭐ **O corpus analisado é 11.641, não ~18.000** (M4) — o resumo do artigo, e o
   nosso próprio levantamento de alvos, propagavam o número errado.
2. ⭐ **Os autores publicaram o modelo LDA ajustado** (7 saídas de pyLDAvis), o que o
   `ALVOS_modelagem_topicos.md` dava como inexistente. Congelado e auto-conferido
   contra a Fig. 4 do artigo.
3. ★ **T1 não é um ranking, é uma afirmação de ausência** — e ela **já está sob
   tensão no gabarito dos próprios autores**: o modelo de janeiro (k=15) tem tópicos
   com `autism` e `microchip`. A ausência de conspiração depende da **resolução** do
   modelo. O caso, se seguir, tem de separar efeito de resolução de efeito de coleta.
4. ⚠ **Quatro divergências internas do artigo** (M6, A2, A3, A7), entre elas os
   modelos mensais publicados terem k = 3, **15**, 2, **6**, **8**, 2 contra o "≤ 3"
   que o texto afirma.
5. ⚠ **O sentimento é TextBlob, não VADER** — correção ao levantamento de alvos.
6. ⭐ **`NoNewNormal` está banido desde 1º/set/2021**: a rota oficial de hoje não
   alcança parte do corpus do artigo.
7. ⚠ **A mensagem de erro do Arctic Shift conflaciona estrangulamento e tamanho** —
   com consequência para a leitura do `reddit-massachs` (§3).
