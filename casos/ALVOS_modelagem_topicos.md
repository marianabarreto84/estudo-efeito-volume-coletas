# Alvos candidatos — o caso que falta: **modelagem de tópico**

> Levantado em **22/ago/2026**, a pedido da Mariana, na rodada de revisão 4 → 5
> (comentários 5 e 10 do `revisao-4.pdf`).
>
> ✅ **A Mariana decidiu abrir o caso em 22/ago/2026.** O prompt de abertura está
> em [`PROMPT_caso_topicos.md`](PROMPT_caso_topicos.md), e o caso nasceu em
> [`reddit-topicos/`](reddit-topicos/README.md) no mesmo dia.
>
> ⚠ **A leitura do full text (22/ago/2026) corrigiu três coisas deste levantamento.**
> Elas estão detalhadas em [`reddit-topicos/ARTIGO_MELTON_alvo.md`](reddit-topicos/ARTIGO_MELTON_alvo.md);
> o resumo, para quem só ler esta página:
>
> 1. **O corpus analisado é 11.641 itens** ("1401 posts and 10,240 comments"), **não
>    ~18.000**. Os ~18.000 são a colheita bruta, antes de um **filtro por 22 termos**.
>    São **submissões e comentários**, não só posts.
> 2. **O sentimento é TextBlob, não VADER** — o mesmo instrumento do caso do YouTube.
> 3. **A afirmação de tópicos não é um ranking**, é uma afirmação de **ausência**
>    ("conspiracy theories were **not detectable** by the LDA models"). Continua
>    invertível — mais nitidamente que um ranking, aliás —, mas o pré-registro tem de
>    ser escrito contra ausência, não contra ordem.
>
> ⭐ E acrescentou uma coisa boa que este levantamento dava como inexistente: **os
> autores publicaram o modelo LDA ajustado** (sete saídas de pyLDAvis no repositório
> que o artigo cita), o que dá gabarito termo a termo para T1.
>
> ⚠ **Isto não está na dissertação, e não entra até o caso produzir resultado.** É o
> *norte* de escolha do alvo, não um caso executado. O `corpo.tex` continua
> declarando a modelagem de tópico como **limitação de cobertura** (§9.3) e como
> **próximo passo**, e a rota Reddit já está nomeada lá.

---

## 1. Por que este caso, e por que Reddit

**Modelagem de tópico é o 4º tipo de análise mais frequente do levantamento**
(408 artigos, 19,1% dos 2.139 extraídos — `tab:analises-survey`) e é o único
tipo frequente **sem caso executado**. O caso do YouTube, que ocupava essa
célula no plano antigo, acabou entregando composição de corpus e sentimento.

A Mariana pediu **Reddit**, e a razão está escrita na própria §3.4 do
`corpo.tex`: é a **única plataforma do conjunto em que "coletar mais" é
literal** — os arquivos históricos (Pushshift e sucessores, via Academic
Torrents; Arctic Shift para janelas menores) contêm a população completa de um
subreddit numa janela, enquanto a interface oficial devolve ~1.000 itens por
listagem. Expandir não depende de credencial, de acervo institucional nem de
acordo com a plataforma. E a infraestrutura de coleta **já está montada** pelos
dois casos executados lá (`reddit-buntain`, `reddit-massachs`).

---

## 2. ⭐ Recomendação: **Melton, Olusanya, Ammar & Shaban-Nejad (2021)**

> *Public sentiment analysis and topic modeling regarding COVID-19 vaccines on
> the Reddit social media platform: A call to action for strengthening vaccine
> confidence.* **Journal of Infection and Public Health** 14(10):1505–1512.
> Preprint aberto: [arXiv:2108.13293](https://arxiv.org/abs/2108.13293) ·
> **178 citações** (Semantic Scholar, 22/ago/2026).

### Por que este

| Critério do lineup | Como este alvo se sai |
|---|---|
| **Tipo de análise que falta** | ✅ **LDA** é uma das duas análises centrais do artigo (a outra é sentimento por **TextBlob** — este levantamento dizia VADER, ver a correção no topo) |
| **Tração** | ✅ 178 citações, periódico revisado — passa folgado no critério que descartou o #207 |
| **Sub-coleta declarada e expansível** | ★ **o ponto forte.** ~**18.000 posts** de **13 subreddits**, colhidos com **PRAW** (a API oficial) numa **única passada, em 16/mai/2021**, cobrindo **01/dez/2020 a 15/mai/2021** — dos quais **11.641 chegaram à análise** (ver correção no topo). A API oficial devolve ~1.000 itens por listagem: 18 mil posts em 13 comunidades ao longo de 5,5 meses é uma **fatia do topo das listagens**, não a população. É a mesma falha estrutural do caso Buntain (top-100 × top-200), e igualmente medível |
| **Coleta reproduzível hoje** | ✅ os 13 subreddits são nomeados no artigo (`Vaccines`, `CovidVaccine`, `CovidVaccinated`, `AntiVaxxers`, `vaxxhappened`, `antivaccine`, `conspiracy`, `conspiracytheories`, `NoNewNormal`, `conspiracy_commons`, `COVID19`, `COVID`, `coronavirus`) e a janela é fechada. Dumps históricos cobrem dez/2020–mai/2021 |
| **Afirmação inversível** | ✅ duas, e das boas: (i) ~~o **ranking dos tópicos**~~ → é **afirmação de ausência** (ver correção no topo): as comunidades falam de **efeitos colaterais**, e conspiração **não é detectável** pelo LDA; (ii) o **balanço de sentimento** — "mais positivo que negativo, e estático ao longo do tempo" |
| **Custo** | baixo: sem credencial, sem rotulagem humana, sem LLM. O gasto é transferência e disco |

### O que torna este alvo especialmente bom para a tese

1. **Duas análises sobre o mesmo corpus.** LDA e sentimento rodam sobre os
   *mesmos* 11.641 itens. Isso repete, numa rede nova, o desenho que o caso
   `vacinas` usou para responder à PP3: duas quantidades medidas sobre o mesmo
   dado podem convergir em ritmos diferentes. E acrescenta um par que a tabela
   mestre ainda não tem — **modelagem de tópico × sentimento**.
2. **Continuidade temática com o caso `vacinas`.** Mesmo assunto (debate
   vacinal), outra plataforma, outro idioma, outro método. Dá uma comparação
   entre redes que hoje não existe no conjunto.
3. **A sub-coleta é do tipo que este trabalho já sabe medir.** "O topo da
   listagem" é um esquema de amostragem enviesado, não uma amostra aleatória —
   exatamente o diagnóstico da §4.4 (curva de mídia) e do caso Buntain. Dá para
   perguntar de novo, e com dado novo, se a falha é **de volume** ou **de
   esquema**.
4. **Aposta pré-registrável e não óbvia.** Modelos de tópico são notoriamente
   instáveis à composição do corpus, mas o *ranking grosseiro* de temas pode
   muito bem sobreviver. A predição a registrar antes de rodar: **o ranking dos
   tópicos principais não se inverte, mas o balanço de sentimento sim**, porque
   o topo da listagem é engajamento e engajamento seleciona polaridade. Se der
   errado, dá errado por escrito.

### O que a Fase 0 tem de checar antes de comprometer

- [x] ✅ **Ler o full text** — feito em 22/ago/2026. Não é ranking: é afirmação de
      **ausência**. $k=5$ no modelo combinado (coerência 0,5641), Gensim LDAModel,
      pré-processamento = regex + remoção de *stop words* + lematização.
- [x] ✅ **Confirmar o número exato de posts** — são **1.401 submissões + 10.240
      comentários = 11.641**, e não ~18.000. São os dois tipos.
- [◐] **Dimensionar a população** — **6 de 13** medidos em 22/ago/2026; os 7
      restantes (entre eles os 3 maiores) travaram no **rate limit** do Arctic Shift.
      ⚠ o mesmo problema do `reddit-massachs`, e a sonda daqui descobriu que a
      mensagem de erro dele **conflaciona estrangulamento e tamanho de consulta**.
      Só o parcial já dá **215.394 itens contra 11.641** do artigo (18,5×).
      Ver [PORTAO1_relatorio.md](reddit-topicos/data/repl/melton2021/PORTAO1_relatorio.md).
- [◐] **Banimentos** — ✅ **`NoNewNormal` foi banido em 1º/set/2021** (por *brigading*),
      depois da coleta do artigo: os autores alcançaram, quem replicasse hoje por PRAW
      não alcança. ⏳ `antivaccine` segue indeterminado (script pronto, endpoint
      estrangulado); nota-se que ele tem só **222 submissões** em 5,5 meses.
- [ ] Decidir o que fixar: o artigo usa LDA. **Fixar LDA**, pelo princípio de
      não confundir efeito de coleta com efeito de método — BERTopic entra, se
      entrar, como análise de sensibilidade separada.

---

## 3. Alternativas consideradas

| Alvo | Rede / análise | Por que **não** ficou em primeiro |
|---|---|---|
| **Low et al. 2020**, *NLP Reveals Vulnerable Mental Health Support Groups…*, JMIR 22(10):e22635 — **321 citações** | Reddit / NLP sobre 28 subreddits, 826.961 usuários, 2018–2020 | Tração ainda maior, e os dados estão publicados no Zenodo (Fase 0 barata). Mas **a modelagem de tópico não é a análise-título** — o artigo se apoia em regressão sobre ~90 atributos textuais — e a coleta **não é obviamente sub-coletada**: eles já levam a janela inteira dos subreddits. Sem sub-coleta expansível, não há o que expandir |
| **"Caracterizando Polarização em Redes Sociais: … Reddit … Eleições Brasileiras de 2018 e 2022"**, WebMedia 2024 (SBC) | Reddit **brasileiro** / *stance detection* + polarização em grafo | ✅ é brasileiro e é Reddit — foi o que mais perto chegou do pedido. ❌ mas a análise é **stance/polarização**, que os casos `vacinas` e `reddit-massachs` já cobrem: não fecharia a lacuna que motivou a busca. E a tração é ~nula (2024, anais nacionais), o que reprova pelo critério que descartou o #207 |
| **"Caracterização e Comportamento de Usuários Tóxicos em Subreddits Brasileiros"**, BraSNAM (SBC) | Reddit brasileiro / toxicidade | mesma objeção: tipo de análise já coberto por classificação, sem tração |
| **"Análise de sentimentos … comunidades brasileiras do Reddit"**, WebMedia 2025 (SBC) | Reddit brasileiro / sentimento | sentimento já está coberto (linha 15 da tabela mestre); sem tração |
| **Gomes, Attux & Cruz 2025**, *Enhancing Contributions to Brazilian Social Media Analysis Based on Topic Modeling with Native BERT Models*, JIDM 16(1):181–191 | **X/Twitter** brasileiro / modelagem de tópico | é modelagem de tópico e é brasileiro, mas (a) é **Twitter**, cuja coleta nova está fechada; (b) é um **artigo de comparação de métodos**, não uma afirmação sobre o mundo — não há conclusão a inverter, que é o que o protocolo mede |

### ⚠ Sobre o pedido "de preferência brasileiro"

**Não achei alvo brasileiro que satisfizesse as duas condições ao mesmo tempo.**
Existe pesquisa brasileira sobre Reddit — nos anais da SBC (WebMedia, BraSNAM,
JIDM), listada acima —, mas o cruzamento *Reddit brasileiro × modelagem de
tópico × tração* está vazio no que esta busca alcançou. Os brasileiros que
existem fazem stance, toxicidade ou sentimento, que são tipos **já cobertos**
pelo conjunto de casos.

Como as duas preferências entram em conflito, a recomendação privilegia **fechar
a lacuna de tipo de análise**, que é a limitação declarada no texto e o motivo de
existir de um sétimo caso. Um caso brasileiro que repetisse um tipo já coberto
não removeria a limitação.

> Se a preferência por Brasil for a decisiva, o caminho honesto é outro: não um
> sétimo caso, e sim um **braço brasileiro** de um caso existente — e aí o
> WebMedia 2024 serve, com a ressalva de tração declarada, do mesmo jeito que a
> tração do alvo de TikTok está declarada no `ALVOS_candidatos.md` daquele caso.

---

## 4. Se a decisão for abrir

Ordem sugerida, espelhando `reddit-buntain`:

1. `casos/reddit-topicos/` com `README.md` + `ARTIGO_MELTON_alvo.md` (as
   afirmações numeradas, extraídas do full text).
2. **Fase 0** — reproduzir o ponto original. Aqui há um obstáculo real: o artigo
   **não publica o corpus**. Reconstruí-lo pelos dumps na mesma janela e nos
   mesmos subreddits é o que mais se aproxima, e a diferença entre o corpus
   reconstruído e os **11.641** deles **é ela própria a medida da sub-coleta**.
3. **Fase 1** — população completa dos 13 subreddits na janela, congelada em
   SQLite.
4. **Fases 2–3** — LDA em frações crescentes, com réplicas por ponto; ranking de
   tópicos comparado por similaridade de partição, e o sentimento medido em
   paralelo sobre o mesmo corpus.
5. **Fase 4** — duas linhas novas na tabela mestre (`tab:mestre` do `corpo.tex`),
   e a lacuna da §9.3 deixa de ser lacuna.

⚠ **Custo de tempo.** É o mesmo perfil do `reddit-buntain`, que levou a coleta
completa a 43.479 submissões + 1.015.247 comentários. Treze subreddits grandes
(`coronavirus`, `conspiracy`, `COVID19`) em 5,5 meses é **bem maior** que isso.
Dimensionar antes de baixar não é formalidade — foi o que travou o
`reddit-massachs`.
