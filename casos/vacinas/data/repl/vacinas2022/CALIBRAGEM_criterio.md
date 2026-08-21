# Teste de calibragem — o criterio da Mariana × o dos codificadores do paper

**CRITERIOS DIVERGENTES** — n = 30 tweets do estrato viral, rotulados as
cegas; o gabarito publicado so entrou na hora de medir.

| Metrica | Valor |
|---|---:|
| κ de Cohen (Mariana × gabarito) | **0.350** |
| acuracia | 0.567 |
| `nenhum` da Mariana | 10 de 30 (33%) |
| `nenhum` no gabarito, nesta amostra | 0 |

## O numero decisivo

| `nenhum` da Mariana | taxa |
|---|---:|
| estrato **viral** (aqui, n=30) | **33%** |
| estrato **baixo** (rodada anterior, n=100) | **32%** |
| gabarito do paper (1.525 virais) | 0,2% |

As duas taxas dela sao praticamente iguais nos dois estratos. Ou seja:
os ~32% de `nenhum` medidos no estrato baixo **nao sao propriedade do
estrato** — sao propriedade do criterio. A hipotese de que o rotulador
'nao transfere entre estratos' **nao se sustenta**: o que muda entre a
Mariana e o modelo e o padrao de codificacao, nao o material.

Quando ela atribui lado, a concordancia e boa: no subconjunto
`pro` x `anti` (n=20), κ = **0.700**. Toda a divergencia
esta na existencia mesma da classe `nenhum`.

## Quem reproduz melhor o gabarito do paper?

| | κ contra o gabarito | n |
|---|---:|---:|
| rotulador `p4` (teste cego) | **0,759** | 1.018 |
| Mariana (coautora do paper) | **0.350** | 30 |

O rotulador automatico reproduz a codificacao publicada **melhor que
uma coautora do proprio artigo**. Ele nao aprendeu a tarefa: aprendeu
a convencao de codificacao daquela equipe, que e o que o gabarito
registra.

## Origem da divergencia (apurada no PDF e no suplemento)

A diferenca de taxa nao decorre de erro de codificacao de nenhuma das
partes: as duas classes chamadas de "terceira opcao" nao designam a
mesma coisa.

O metodo do artigo (p. 3) registra que o material foi rotulado como
*pro-vaccine, anti-vaccine, or non-relevant/ambiguous*. Os tres tweets
que o gabarito publicado classifica nessa terceira classe sao:

| ID | tweet |
|---|---|
| 1471 | *portugueses com medo da vacina tipo que este nao e o seu pequeno-almoco* |
| 1516 | *vacina contra a influencia????? mds vao acabar com o instagram* |
| 1386 | *hoje levei minha cachorra pra tomar vacina e a veterinaria disse (...)* |

Os tres sao usos da palavra *vacina* **fora do tema** — meme, trocadilho
com influenciadores, vacinacao veterinaria. A classe operou, portanto,
como marcador de **irrelevancia topica**, e nao de ausencia de posicao.
Tweets sobre vacinacao que nao emitem juizo (noticia relatada, fala
citada, dado factual) nao tinham categoria propria e foram resolvidos
em `pro` ou `anti`.

Trata-se de um esquema **binario forcado** para stance — desenho comum
na literatura de analise de conteudo, e nao uma particularidade deste
artigo. A numeracao das linhas do suplemento e contigua (1 a 1.525, sem
lacunas), o que e compativel com ausencia de descarte; a evidencia nao
e conclusiva quanto a isso, porque uma exportacao pode renumerar.

## Consequencia para esta replicacao

A consequencia principal recai sobre **o nosso instrumento**, nao sobre
o artigo. O rotulador automatico foi calibrado contra este gabarito e
reproduziu fielmente o esquema nele registrado, inclusive a ausencia de
uma classe neutra: kappa 0,759 no estrato viral. Ao aplica-lo a um
corpus mais amplo, em que cerca de um terco dos tweets e topicamente
relevante mas nao avaliativo, o instrumento atribui lado a esses casos
porque nunca viu exemplos do contrario.

Na amostra rotulada a mao, esses casos se distribuiram de forma
aproximadamente simetrica entre `pro` e `anti` (16 e 14). O efeito
esperado e, portanto, de **atenuacao** em direcao a 50%: as estimativas
de predominancia produzidas pelo rotulador no corpus amplo devem ser
lidas como **limite inferior**. A rotulagem manual no estrato baixo da
64,7% de `pro` entre os tweets com posicao, contra 62,6% do rotulador —
consistente com essa direcao.

## Implicacao para a leitura do trabalho replicado

Os percentuais de stance do estrato viral (48,4% x 51,4%) sao computados
sobre uma binaria que nao admite ausencia de posicao. Isso nao invalida
a descricao do material viral, mas **limita a generalizacao** dessas
proporcoes ao debate como um todo: parte do que aparece como adesao a
um dos polos pode ser conteudo sem posicao alocado por necessidade do
esquema. A comparacao entre estratos exige um esquema com classe neutra
nos dois lados — que e o que esta replicacao passa a adotar.

> Registrado como limitacao metodologica identificada na replicacao. O
> artigo nao reporta concordancia entre codificadores, o que impede
> estimar quanto da variacao aqui observada ja existia na codificacao
> original.

## Leitura

A Mariana aplica um criterio diferente do dos codificadores do paper **no mesmo material**. Consequencia: o kappa do estrato baixo mede divergencia entre dois padroes humanos, e nao transferencia do instrumento — os dois diagnosticos sao incompativeis e o segundo nao se sustenta como estava escrito.

Se o criterio da Mariana for o mais defensavel (so conta juizo explicito sobre a vacinacao), entao o proprio gabarito do paper atribui lado a conteudo neutro, o que **infla a polarizacao relatada pelo alvo**. Isso deixa de ser problema do nosso rotulador e vira uma critica ao trabalho replicado — mais forte, e diretamente no espirito da dissertacao.

## Os 13 desacordos

| ID | Mariana | gabarito |
|---|---|---|
| 1256 | nenhum | anti |
| 918 | nenhum | anti |
| 696 | nenhum | anti |
| 1333 | nenhum | pro |
| 357 | nenhum | pro |
| 643 | nenhum | pro |
| 611 | nenhum | pro |
| 1072 | nenhum | anti |
| 1240 | pro | anti |
| 1082 | nenhum | anti |
| 1354 | anti | pro |
| 829 | nenhum | pro |
| 1300 | pro | anti |