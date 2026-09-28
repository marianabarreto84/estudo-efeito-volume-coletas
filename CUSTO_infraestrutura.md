# O custo de infraestrutura do protocolo

A §10.2 da dissertação argumenta que medir o efeito do volume é carga de trabalho de banco de
dados, e não de planilha, mas não publica números. Este documento traz os números, medidos sobre
os instantâneos congelados de cada caso e sobre os arquivos de saída das curvas. Nada aqui é
recalculado: as contagens de reexecução saem dos próprios JSON que geraram as figuras.

## 1. O que foi preciso guardar para testar cada conclusão

| Caso | Itens que o artigo analisou | O que a réplica teve de guardar | Instantâneo | Reexecuções da análise |
|---|---|---|---|---|
| #Eleições2014, mídia (Twitter) | 700 tweets rotulados à mão | 32.193 tweets na hashtag-âncora; 140.909 no escopo eleitoral | **124 MB** | **15.301** subamostras |
| Debate vacinal (Twitter) | 1.525 tweets no eixo de conteúdo | 29.978 tweets rotulados; rede de 6,55 M posts, 879 mil autores, 3,34 M arestas | **1.744 MB** | **32** execuções de Louvain |
| Papéis sociais (Reddit) | 279 participantes | 43.479 submissões e 1.015.247 comentários, dos quais 217.386 participantes | **120 MB** | 6 limiares, determinísticos |
| Apoio a Trump (Reddit) | 44.924 usuários | a matriz de atributos publicada pelos autores | **19 MB** | validação cruzada de 5 partes × 4 famílias |
| Idosos e pandemia (YouTube) | 3.782 vídeos | 3.446 vídeos e 2.165 canais de coleta própria, mais o gabarito dos autores | **64 MB** | 5 limiares de sensibilidade |
| Deleção política (TikTok) | 938.961 publicações | as mesmas, com o estado em 3 datas | **12 MB** | 3 datas × 3 bases de contagem |
| **Total** | | | **2.086 MB** | **≈ 15,3 mil** |

Leitura em uma linha: para pôr à prova uma conclusão que um artigo tirou de 1.525 tweets, foi
preciso guardar 1,7 GB e refazer a partição de comunidades 32 vezes; para uma que saiu de 700
tweets, quinze mil reexecuções da mesma agregação.

## 2. De onde vem a contagem de reexecuções

| Curva | Pontos | Réplicas por ponto | Total | Arquivo |
|---|---|---|---|---|
| H1, retuíte de mídia vertical por volume | 10 (de 100 a 32.193) | 300, e 1 no universo | **2.701** | `casos/twitter-ituassu/data/repl/compos2014/curva_midia.json` |
| H2, rivalidade entre mídias por dia | 7 dias × 6 tamanhos (25 a 800) | 300 | **12.600** | `.../curva_h2.json` |
| Rede do debate vacinal por fração | 8 (de 1% a 100%) | 5 até f=0,25; 3 em 0,50 e 0,75; 1 em 1,0 | **32** | `casos/vacinas/data/repl/vacinas2022/curva_rede.json` |
| Participação multicomunidade por limiar | 6 (k = 1 a 50) | determinístico | **6** | `casos/reddit-buntain/data/repl/buntain2013/curva_rb3.json` |

As 32 execuções de Louvain são o número que explica por que a Figura 5.1 usa de 3 a 5 réplicas por
ponto, e não as 30 que o protocolo pede: o ponto mais caro roda sobre 6,55 milhões de posts. A
legenda da figura declara essa redução.

## 3. Os dois papéis do banco de dados, com o que cada um sustenta

**O banco que preserva.** Os dois casos de Twitter existem porque o laboratório mantém acervos
históricos em PostgreSQL e MongoDB, consultáveis por hashtag e por janela. A rota de coleta da
plataforma está fechada desde 2023, de modo que, sem o acervo, a plataforma fechada seria o fim do
caso. O acervo de 2014 tem 10,7 milhões de tweets, e o que o caso usa é uma janela de sete dias
dele.

**O banco que congela.** Cada caso reduz a sua coleta a um instantâneo local versionado, em SQLite
ou CSV, e todas as análises rodam sobre ele, sem rede. É esse segundo papel que torna o resultado
reproduzível por terceiros, e ele não exige servidor: um arquivo único basta. Nenhum script de
análise deste trabalho abre conexão de rede; só os de extração o fazem.

## 4. O que não foi medido

O tempo de execução não foi cronometrado durante o trabalho, e não foi refeito na véspera da
defesa para não arriscar os resultados. O que se sabe indiretamente é que o custo do Louvain foi
alto o suficiente para reduzir as réplicas de 30 para 3, e isso está declarado no texto.

---

*Contas de 28/set/2026, sobre a cópia local dos instantâneos. Tamanhos por `du -sm` em
`casos/<caso>/data`; contagens de réplica lidas dos JSON citados na seção 2.*
