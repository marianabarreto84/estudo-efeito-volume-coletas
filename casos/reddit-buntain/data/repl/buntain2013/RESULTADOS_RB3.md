# Fase 2/3 — RB3: participação multi-comunidade no universo

> Medido em **19/ago/2026**, ao fim da coleta completa. Script:
> [`analise/rb3.py`](../../../analise/rb3.py) · snapshot:
> `snapshot_buntain.sqlite` (**43.479 submissions + 1.015.247 comentários**, 13
> subreddits, julho/2013, sem corte algum).

---

## 1. A afirmação do alvo

Buntain e Golbeck (2014, §5.3) relatam que **apenas ~3% dos usuários (7 de 279)**
participam de **mais de uma** das comunidades analisadas. A leitura substantiva que o
artigo extrai disso é a de que os papéis sociais no Reddit são **locais**: quem responde
perguntas numa comunidade raramente é o mesmo que responde em outra.

## 2. A sub-coleta que produziu esse número

O artigo coletou, de cada um dos 13 subreddits em julho de 2013, as **100 submissões
mais votadas** e cerca de **200 comentários** de cada uma; depois **descartou usuários
com menos de 20 arestas** na rede de interação. Restaram **279 usuários**.

Nossa coleta recolheu **tudo**: 43.479 submissões e 1.015.247 comentários dos mesmos 13
subreddits, na mesma janela. São **217.386 usuários** não-bot — 779 vezes o conjunto
analisado pelo artigo.

## 3. Resultado: **a conclusão muda, e por uma ordem de grandeza**

| recorte | usuários | em >1 subreddit | % |
|---|--:|--:|--:|
| **artigo** (top-100 × ~200 coment., corte ≥20 arestas) | 279 | 7 | **~3%** |
| **universo**, sem corte nenhum | 217.386 | 33.115 | **15,2%** |
| **universo, no limiar do artigo** (≥20 mensagens) | 5.991 | 3.450 | **57,6%** |

A comparação que importa é a última linha, porque é a que aplica **o mesmo corte de
atividade** do artigo ao universo. Sob esse corte, a participação multi-comunidade não é
de 3%: é de **57,6%** — **dezenove vezes** o valor publicado. A maioria dos usuários
ativos circula por mais de uma comunidade, e não a minoria.

**A predição pré-registrada se confirma**, e com folga muito maior que a apostada. O que
o artigo mediu não foi a localidade dos papéis sociais no Reddit; foi a localidade
induzida por olhar só os 100 posts mais votados de cada comunidade. Ao restringir a
coleta ao topo de cada subreddit, a chance de reencontrar o mesmo usuário em dois topos
distintos torna-se pequena **por construção**, e o resultado mede o desenho da coleta,
não o comportamento da população.

## 4. A curva por limiar de atividade

| ≥ k mensagens | usuários | multi | % multi |
|--:|--:|--:|--:|
| 1 | 217.386 | 33.115 | 15,2% |
| 2 | 101.270 | 33.115 | 32,7% |
| 5 | 34.566 | 16.875 | 48,8% |
| 10 | 14.622 | 8.047 | 55,0% |
| **20** | **5.991** | **3.450** | **57,6%** |
| 50 | 1.709 | 959 | 56,1% |

A quantidade **cresce com o limiar e depois assenta**: sobe de 15,2% a 57,6% entre k=1 e
k=20 e recua levemente em k=50. Isso tem consequência para o par *mudou? / convergiu?*:

- **mudou?** — **SIM**, drasticamente (3% → 57,6% no mesmo limiar).
- **convergiu?** — a medida **estabiliza a partir de k≈10–20**; o problema do artigo não
  foi o limiar de atividade, que é razoável, e sim **o que havia disponível para ser
  contado** depois do recorte top-100 × top-200.

É o mesmo diagnóstico do H1 do caso Twitter, mas com sinal invertido: lá o esquema de
amostragem enviesava uma estimativa que já convergira; aqui o esquema **remove a
evidência** de que a quantidade de interesse é grande.

## 5. Distribuição

| subreddits por usuário | usuários |
|--:|--:|
| 1 | 184.271 |
| 2 | 28.624 |
| 3 | 3.767 |
| 4 | 615 |
| 5 | 95 |
| 6 a 9 | 14 |

## 6. Ressalvas

- O artigo corta por **arestas na rede de interação** (≥20); nós cortamos por
  **mensagens publicadas** (≥20). São grandezas próximas mas não idênticas: um usuário
  com 20 mensagens pode ter menos de 20 arestas. A direção do achado não depende disso
  — em k=10 o valor já é 55,0% —, mas a equivalência exata do limiar não está
  estabelecida.
- Bots e `[deleted]` foram excluídos.
- A coleta cobre julho/2013 nos 13 subreddits do artigo, que é a janela declarada.

## 7. Linha na tabela mestre

Preenche a **linha 11** (reddit-buntain / SNA / papéis sociais):
**mudou? SIM** (3% → 57,6% sob o mesmo limiar) · **convergiu? SIM, em k≈10–20** — com a
observação de que a convergência é da nossa curva; o valor do artigo não é recuperável
em limiar nenhum, porque a limitação estava na coleta e não no corte.
