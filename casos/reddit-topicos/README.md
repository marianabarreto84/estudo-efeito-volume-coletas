# Caso `reddit-topicos` — modelagem de tópico (Melton et al. 2021)

> **Sétimo caso** do lineup, aberto em **22/ago/2026** por decisão da Mariana
> ([`ESTADO.md`](../../ESTADO.md) §3 item 9). Existe para fechar a única lacuna de
> **tipo de análise** que a dissertação declara: modelagem de tópico é o 4º tipo mais
> frequente do levantamento (408 artigos, 19,1%) e o único frequente **sem caso
> executado** — hoje escrito no `corpo.tex` como limitação (§9.3) e próximo passo (§9.4).
>
> Prompt de abertura: [`../PROMPT_caso_topicos.md`](../PROMPT_caso_topicos.md).
> Escolha do alvo: [`../ALVOS_modelagem_topicos.md`](../ALVOS_modelagem_topicos.md).
> Afirmações do alvo: [`ARTIGO_MELTON_alvo.md`](ARTIGO_MELTON_alvo.md).
>
> 🔖 **Retomando o trabalho? Comece por [`RETOMAR.md`](RETOMAR.md)** — ele diz o que
> está feito, o que estava no meio, e em que ordem seguir.

---

## 1. O alvo e a sub-coleta

**Melton, Olusanya, Ammar & Shaban-Nejad (2021)**, *Public sentiment analysis and topic
modeling regarding COVID-19 vaccines on the Reddit social media platform*, **J. Infection
and Public Health** 14(10):1505–1512 · **178 citações** · CC BY ·
[arXiv:2108.13293](https://arxiv.org/abs/2108.13293).

A sub-coleta é **declarada e datada**: ~18.000 posts de **13 subreddits**, colhidos pela
**API oficial do Reddit numa única passada, em 16/mai/2021**, cobrindo 01/dez/2020 a
15/mai/2021. A API devolve ~1.000 itens por listagem — logo aquilo é o **topo das
listagens**, não a população. É a mesma falha estrutural do caso
[`reddit-buntain`](../reddit-buntain/README.md), que deu o maior efeito de sub-coleta da
dissertação.

⭐ **O corpus analisado não é 18.000, é 11.641** — "1401 posts and 10,240 comments" (M4).
Os 18.000 são a colheita bruta; entre uma coisa e outra há um **filtro por 22 termos**
(M3). São, portanto, **dois** filtros empilhados sobre a população: o topo da listagem e
o termo.

## 2. As duas afirmações a testar

| | afirmação | como está no artigo |
|---|---|---|
| **T1** | modelagem de tópico | ⚠ **não é ranking, é ausência**: "community members mainly focused on **side effects rather than outlandish conspiracy theories**", e "the majority of conspiracy theories were **not detectable** by the LDA models" |
| **T2** | sentimento | 56,68% positivo × 27,69% negativo × 15,63% neutro, e "**have not meaningfully changed** since December 2020" |

As duas rodam sobre o **mesmo corpus** — o desenho que respondeu à PP3 no caso vacinal —
e acrescentam à tabela mestre um par que ela não tem: **modelagem de tópico × sentimento**.

Detalhe e verbatim de cada uma em [`ARTIGO_MELTON_alvo.md`](ARTIGO_MELTON_alvo.md) §4 e §5.

## 3. Estado atual — ⏳ **PARADO no Portão 1, esperando decisão da Mariana**

Relatório completo do portão, com a recomendação:
[`data/repl/melton2021/PORTAO1_relatorio.md`](data/repl/melton2021/PORTAO1_relatorio.md).

| Fase | Estado |
|---|---|
| **Portão 1(a)** — full text lido, afirmações numeradas | ✅ **feito** em 22/ago/2026 |
| **Portão 1(b)** — dimensionamento da população | ◐ **6 de 13** subreddits; ⏳ os 7 restantes (entre eles os 3 maiores) esperam o rate limit do Arctic Shift |
| **Portão 1(c)** — banimentos | ◐ `NoNewNormal` **banido em 1º/set/2021** (confirmado fora da API); ⏳ `antivaccine` indeterminado — o script está pronto e roda no mesmo endpoint estrangulado |
| **Portão 1(d)** — relatório e decisão | ✅ relatório escrito; ⏳ **decisão é da Mariana** |
| Portão 2 — pré-registro | ⛔ só depois da decisão |
| Fases 1–4 | ⛔ |

★ **Mesmo o parcial já mostra a sub-coleta:** os **6 subreddits menores** somam
**215.394 itens** na janela, contra os **11.641** do corpus do artigo — **18,5×** sem
os grandes. (Teto do fator, não o fator: o corpus do alvo é pós-filtro de termo e o
nosso parcial é população bruta — ver o relatório §2.)

⚠ **Por que parou:** o Arctic Shift devolve `"Timeout. Maybe slow down a bit"` e exige
**~5 min de silêncio** para se recuperar. O prompt do caso manda **parar, não
contornar**. A mensagem, descobriu-se, **conflaciona estrangulamento e tamanho de
consulta** — o que tem consequência para a leitura do caso
[`reddit-massachs`](../reddit-massachs/README.md) (relatório §3).

## 4. O que o Portão 1(a) já produziu

1. ⭐ **Um gabarito que não se esperava ter.** O artigo não publica o corpus, mas o
   repositório que ele manda consultar (`github.com/Cheltone/NLP_Reddit`) contém **sete
   saídas de pyLDAvis** — o **modelo LDA ajustado** dos autores, com matriz tópico-termo
   e fração de tokens por tópico. Congelado por script em
   [`data/repl/melton2021/gabarito_lda_autores.json`](data/repl/melton2021/gabarito_lda_autores.json)
   ([`pipeline/baixa_gabarito_lda.py`](pipeline/baixa_gabarito_lda.py)). Confere sozinho
   contra a legenda da Fig. 4 do artigo (13,38% × "13.4% of tokens"). Isso permite
   comparar os nossos tópicos com os deles **termo a termo (RBO)**, em vez de comparar
   prosa.
2. ⚠ **Quatro divergências dentro do próprio artigo**, todas registradas: a janela dos
   gráficos começa 3 meses antes da janela declarada (M6); as faixas de subjetividade
   dos *Methods* e dos *Results* são diferentes (A2); o limiar de polaridade não é
   declarado (A3); e os modelos mensais publicados têm **k = 3, 15, 2, 6, 8, 2**, não o
   "≤ 3" que o texto afirma (A7).
3. ⚠ **Correção ao levantamento de alvos:** o sentimento é **TextBlob**, não VADER.
4. ★ **T1b já está sob tensão no gabarito dos autores.** No modelo de janeiro (k=15)
   deles há um tópico com **`autism`** e outro com **`microchip`** — vocabulário
   conspiratório que a prosa diz não ser detectável. A ausência depende da **resolução
   do modelo**, e o caso vai ter de separar *efeito de resolução* de *efeito de coleta*
   (ver `ARTIGO_MELTON_alvo.md` §4).

## 5. Mapa da pasta

```
reddit-topicos/
├── README.md                  <- este arquivo
├── ARTIGO_MELTON_alvo.md      <- as afirmações numeradas, do full text
├── core/
│   ├── arctic.py              <- cliente de coleta paginada (herdado do reddit-buntain)
│   └── agregacao.py           <- cliente de AGREGAÇÃO, paciente com o rate limit
├── pipeline/
│   ├── dimensiona.py          <- ⭐ Portão 1(b): mede a população. Retomável, sem dependência
│   ├── checa_bans.py          <- Portão 1(c): quais subreddits só existem no arquivo
│   ├── consolida_sonda.py     <- funde as 2 rodadas da 1ª sonda num JSON congelado
│   └── baixa_gabarito_lda.py  <- congela o modelo ajustado dos autores
├── analise/                   <- (vazio até a Fase 2)
└── data/repl/melton2021/
    ├── PORTAO1_relatorio.md          <- o relatório do portão e o pedido de decisão
    ├── gabarito_lda_autores.json     <- o modelo LDA ajustado dos autores
    ├── volume_portao1_parcial.json   <- dimensionamento da 1ª sonda (6/13, PARCIAL)
    ├── volume_portao1.json           <- dimensionamento do `dimensiona.py`
    ├── volume_portao1_progresso.json <- estado retomável (não apagar no meio)
    ├── volume_portao1.log            <- log da medição, com data e hora
    └── logs/                         <- stdout das 2 rodadas da 1ª sonda
```

### Como medir a população (o passo lento)

```bash
cd casos/reddit-topicos
python pipeline/dimensiona.py --listar     # o que já foi medido e o que falta
python pipeline/dimensiona.py              # mede o que falta (caso Melton)
python pipeline/dimensiona.py --caso massachs   # a reconferência do reddit-massachs
```

Só precisa de `python` — nenhuma dependência externa, nenhuma credencial, nenhum gasto
de LLM. **É lento de propósito**: 15 s entre consultas e **300 s** quando o Arctic Shift
recusa, porque foi essa a folga medida que cura o estrangulamento (§ do relatório e
[ESTADO.md §4.23](../../ESTADO.md)). Nos subreddits grandes isso dá horas. Pode fechar e
rodar de novo depois: o progresso é gravado a cada janela fechada e **nada se perde**.

⚠ **Não paralelize e não troque o User-Agent para contornar o limite.** O Arctic Shift é
infraestrutura pública mantida por voluntários, e os outros dois casos de Reddit da
dissertação dependem dela.

## 6. Travas herdadas do prompt

- **Não usar a API oficial do Reddit para volume** — a rota é Arctic Shift / dumps.
- **Nenhum gasto de LLM.** LDA e TextBlob são locais; o `ANTHROPIC_VACINAS_API_KEY` é do
  rotulador do stance e não se toca.
- **Fixar LDA** (o algoritmo do alvo). BERTopic, se entrar, entra como análise de
  sensibilidade separada — trocar o método confundiria efeito de coleta com efeito de
  método.
- **Não mexer no `corpo.tex`** enquanto a Mariana não tiver lido o `revisao-5.pdf`.
