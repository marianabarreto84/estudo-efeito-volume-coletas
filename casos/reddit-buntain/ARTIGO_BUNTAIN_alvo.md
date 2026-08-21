# O alvo — Buntain & Golbeck (2014): "Identifying Social Roles in reddit Using Network Structure"

> Leitura instrumental para a replicação por expansão. Fonte: PDF oficial WWW'14
> ([archives.iw3c2.org/www2014/proceedings/companion/p615.pdf](https://archives.iw3c2.org/www2014/proceedings/companion/p615.pdf)).
> Plano do caso em [REPLICACAO_CASO_BUNTAIN.md](REPLICACAO_CASO_BUNTAIN.md).

**Ficha.** Cody Buntain & Jennifer Golbeck (University of Maryland). *Identifying Social
Roles in reddit Using Network Structure.* **WWW'14 Companion** (23rd Int. World Wide Web
Conference), Seul. DOI 10.1145/2567948.2579231. **133 citações** (Semantic Scholar,
7/ago/2026; 10 influentes). Venue de primeira linha; artigo **bastante referenciado** —
por isso substitui o #207. Código do crawler: `github.com/cbuntain/redditResponseExtractor`.

---

## 1. O que o artigo fez

### 1.1 Coleta (a parte que o caso problematiza) — sub-coleta em 4 camadas

Reconstrói **redes de interação** entre usuários por subreddit. Por limite da API do
Reddit (explícito no paper: "reddit imposes strict limitations… no more than two requests
per second… limits the number of objects… between 100–1500"), coletou um **estrato de
topo**:

1. **Top 100 submissions** de **um único mês (julho/2013)** — não todas as submissions.
2. **~top 200 comentários** por submission (média) — não todos os comentários.
3. **1 mês** — não a história dos subreddits.
4. **Corte de grau:** descartou todo nó com **< 20 arestas de saída** ("to ensure
   statistical significance") → sobraram **279 usuários** em **10 subreddits** (dos 13
   iniciais; 3 foram descartados por não ter usuário acima do limiar).

**13 subreddits-alvo** (o "tema" do caso): AskScienceDiscussion, AskMen, AskScience,
AskWomen, CompSci, DesMoines, IAmA, MachineLearning, Movies, MyLittlePony,
PersonalFinance, TalesFromTechSupport, WashingtonDC.

⚠ A sub-coleta é a **mesma assinatura do #207** (recorte imposto por limite de API, não
por amostragem), mas num paper de 133 citações e com **análise de rede** — o que faltava
no lineup.

### 1.2 Rede e análise

- **Grafo dirigido por subreddit:** nós = usuários (que postaram submission ou
  comentário); arestas = **respostas** (autor→destinatário), com peso = nº de respostas.
- **Papéis (roles):** rotulagem **manual** de cada nó de alto grau como *answer-person* ×
  *non-answer-person*, inspecionando a **assinatura estrutural da ego-rede 1,5-grau**
  (Welser 2007): answer-person = "hub-and-spoke" esparso (estrela), com muitos vizinhos de
  grau baixo e poucos triângulos. ~150 answer × ~130 non-answer.
- **Features estruturais da ego-rede:** densidade, distribuição de grau baixo, proporção
  de vizinhos de grau baixo, proporção de "intense ties" (peso >1), coeficiente de
  clustering, densidade de triângulos, + comunidade de origem.
- **Classificador:** 100 árvores de decisão (Scikit), split 85/15.

---

## 2. Resultados que viram afirmações testáveis

| # | Afirmação (como está no artigo) | Onde |
|---|---|---|
| **RB1** | O papel **answer-person existe** no Reddit (RQ1 = "definitive yes") | §4.1, §5.1 |
| **RB2** | O papel é **identificável só pela estrutura de rede** (~80% de acerto médio; 0,66–0,92), e a **estrutura (80%) supera a filiação ao subreddit (69%)** — a estrutura importa mais que a comunidade de origem | §4.2, §5.2 |
| **RB3** | **Usuários quase não participam de múltiplas comunidades:** só **7 de 279 (~3%)** apareceram em >1 subreddit; ligado à "regra do 1%" (≈1% do 1%) | §4.1, §5.3, §6 |

**Conclusão-título:** roles bem definidos existem e são detectáveis por estrutura em
ambientes multi-comunidade; a participação cruzada entre comunidades é **rara**.

---

## 3. Por que este alvo serve à dissertação

Exemplar de sub-coleta por critério **agravada por limite de ferramenta**, num paper
influente. E tem um **alvo-teste ideal para "coletar mais": a afirmação RB3 (3%
multi-comunidade)**. Esse número é quase por construção um **artefato da sub-coleta**: se
você só olha quem comentou nos **top-100 submissions de 1 mês** e ainda **corta quem tem
<20 arestas**, você **não consegue ver** a atividade cruzada de um usuário — ela está nos
posts/subreddits que você não coletou. Coletar todos os posts e comentários dos mesmos 13
subreddits (sem o corte de grau) é expandir **sem sair do tema** e testar se os 3% sobem.

Bônus de desenho:
- **RB3 não precisa de gabarito humano** (é contagem estrutural: quantos usuários em >1
  subreddit) → re-testável de forma limpa, diferente do stance/rotulador.
- Dados de **julho/2013** estão **plenamente disponíveis** (Arctic Shift / dumps / Academic
  Torrents cobrem 2013 com folga) — ver [FASE0](data/repl/buntain2013/FASE0_descoberta.md).
- Análise = **SNA a nível de nó** (ego-redes, densidade, clustering) — **tipo novo** no
  lineup, que antes nenhum caso cobria.
