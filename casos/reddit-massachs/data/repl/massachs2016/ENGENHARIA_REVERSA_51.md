# Engenharia reversa da lista dos 51 subreddits (22/set/2026)

Feito **depois da entrega da dissertação**, a pedido da Mariana, para a defesa. Nada disto
está no `corpo.tex`.

## Pergunta

O grupo focal do artigo é formado por quem tem ≥10 comentários em 2012 **e** ≥10 em 2016
em "r/politics + os 50 subreddits mais similares". A lista dos 51 não foi publicada, e o
dataset só deixa ver 34 nomes. Mas o dataset traz o **nome de usuário** dos 44.924. Dá
para descobrir a lista contando, no acervo do Reddit, os comentários desses usuários?

## O que foi feito

- `pipeline/contagem_por_usuario.py`: 500 usuários **do grupo**, sorteados com a semente
  20260922, com os comentários por subreddit em 2012 e em 2016. A fonte é o endpoint de
  agregação por autor do Arctic Shift. Foram 500 de 500, com 10 erros pontuais (HTTP 422).
- `pipeline/amostra_fora_do_grupo.py`: 500 usuários **fora do grupo**, tirados de
  comentários de r/politics em instantes sorteados de 2012, com a mesma contagem.
- `analise/infere_51.py` e `analise/infere_51_discrimina.py`.

Dados, na cópia com dados: `contagem_por_usuario.jsonl` e `contagem_fora_do_grupo.jsonl`.

## Resultado

**1. Quem está dentro do grupo não revela a lista.** Com só os 34 conhecidos, 478 dos 500
membros (95,6%) já passam do limiar. As 34 incluem subreddits enormes (`todayilearned`,
`worldnews`, `atheism`), e quase todo usuário ativo atinge 10 comentários só com elas.

**2. A regra declarada não reproduz o grupo, com qualquer lista.**
- Dos 500 de fora, **37 (7,4%; IC95% ≈ 5–10%)** têm ≥10 comentários em **r/politics
  sozinho** em 2012 **e** em 2016. Exemplos: 2.453 e 3.071 comentários; 697 e 126.
- Como r/politics é a semente da lista, pela regra do artigo esses usuários teriam de
  estar no grupo, e não estão. Nenhuma escolha dos outros 50 conserta isso.
- Com os 34 conhecidos, 60 dos 186 não-membros ativos em 2016 entrariam, e 22 membros
  ficariam de fora.
- A busca gulosa não converge para uma lista plausível. Ela reduz os membros perdidos
  acrescentando subreddits como `tf2`, `hearthstone` e `edmproduction`, e nunca reduz os
  não-membros incluídos. É sobreajuste a ruído.

## Leitura

A lista dos 51 não é identificável por esta via, porque o grupo publicado **não segue a
regra publicada** quando conferido contra o acervo atual. Há duas explicações possíveis,
que esta sondagem não separa:

- **Lacunas no acervo que os autores usaram.** O Pushshift de ~2019 tinha falhas
  documentadas: Gaffney e Matias (2018), citados na dissertação (p. 16), acharam cerca de
  36 milhões de comentários faltando.
- **Um critério adicional não declarado** na formação do grupo, como exclusões, um recorte
  de período ou uma deduplicação.

Nas duas hipóteses, reconstruir o grupo a partir do dado bruto **não devolve os 44.924**.
Isso reforça o argumento da defesa: a expansão não era só baixar mais dado, porque o ponto
de partida publicado não é reconstruível pela regra declarada.

## Limites

- É uma amostra de 500 de cada lado. Os não-membros vieram de comentários em r/politics,
  o que favorece quem comenta muito.
- O Arctic Shift é o acervo de hoje. Comentários apagados entre ~2019 e 2026 contam para
  menos, e não para mais, então não explicam não-membros que **passam** do limiar.
- A contagem por autor do Arctic Shift não foi conferida contra uma coleta paginada.
