# Eixo B — Estatística quantitativa via SGBD: como o Heine fez e como replicamos

> Eixo **quantitativo** da replicação da dissertação do Heine (Cap. 5). É o eixo em que
> "coletar mais" é **viável e barato** — e a hipótese é que as conclusões **convergem
> cedo**. Contraste direto com o eixo tópicos. Plano em
> [REPLICACAO_CASO_HEINE.md](REPLICACAO_CASO_HEINE.md).

## 1. O que o Heine fez

Sobre os **57,9 M** de tweets (dois blocos de out/2022), no **PostgreSQL** com o esquema
conceitual TreeTech (Fig. 5.1). Duas análises, por consulta SQL:

- **B1 — postagens por faixa de engajamento.** Engajamento do tweet = combinação
  ponderada de `likes/retweets/quotes/replies`; pesos calibrados pelo **ETA**
  (Engajamento Total da Amostra). Pesos (Tab. 5.1): eta ≈ 2,894×10¹¹; like ≈ 40,90;
  retweet ≈ 0,252; quote ≈ 1847,8; reply ≈ 879,3. Conta tweets por faixa de engajamento.
  - **Achado:** quase long-tail; 3 primeiras faixas com contagens próximas; repique na
    última faixa; queda gradual abaixo de 10.000.
- **B2 — postagens ao longo do tempo.** Contagem por dia, um SQL por bloco (2–16/out e
  24–31/out).
  - **Achado:** picos nos dias de votação (2/out e 30/out); subida às vésperas do 2º turno.

**Conclusão (Cap. 6.2):** o SGBD rodou as 57,9 M de linhas com várias operações
encadeadas sem estourar memória/hardware.

## 2. O que replicamos (e o ângulo novo)

O Heine provou **viabilidade** (o banco aguenta). A nossa pergunta é a da dissertação:
**a que fração de N essas conclusões já estão estabilizadas?** Isto é, se o objetivo é
só a forma da distribuição de engajamento e a posição dos picos temporais, **quanto
dado é suficiente?** Duas frentes:

- **Reproduzir os agregados no universo** (sanity check): recalcular ETA + pesos e a
  contagem por faixa e por dia; conferir contra Tab. 5.1 e Figs. 5.4/5.8/5.10.
- **Curva de convergência (E1'):** amostrar frações crescentes de N e medir:
  - **JS-divergence** entre o histograma de faixas de engajamento da fração e o do todo;
  - **erro relativo** da série temporal por dia; **posição dos picos** (batem sempre?).
  Esperado: **platô cedo** (poucos %), porque são estatísticas agregadas de baixa
  dimensão — o oposto dos tópicos.

## 3. Por que isto é barato (e a ironia útil)

As agregações do eixo B são **SQL puro no servidor** (`GROUP BY`, `count`, `sum`) — não
precisam trazer as 57,9 M linhas para o local. Então "coletar mais" aqui **não tem
custo de análise**: o SGBD faz. A ironia útil para a dissertação: no eixo em que coletar
tudo é **barato** (quantitativo), a amostra provavelmente **bastava** (converge cedo);
no eixo em que coletar tudo é **caro** (tópicos, com embeddings), a amostra **não
bastava**. A dor e o ganho estão **desalinhados** — recomendação prática forte.

## 4. Decisões pendentes do eixo

1. Cortes exatos das faixas de engajamento do Heine (o PDF traz os gráficos, não a
   tabela de limites) — extrair da consulta da Fig. 5.3 ou reconstruir por quantis.
2. Definição de "engajamento total" (ETA) e da fórmula de pesos exata (ref. [34] do
   Heine) — reproduzir para bater a Tab. 5.1.
3. Como amostrar frações preservando a estrutura temporal (amostra aleatória simples vs
   estratificada por dia) para o teste de convergência do B2.
4. Fuso horário das datas (o caso Twitter usa America/Sao_Paulo) — fixar igual.

## 5. Predição pré-registrada

BH1 (forma long-tail) e BH2 (picos nos dias de votação) **estabilizam com poucos %** de
N (aposta: ≤5%). A amostra por proporção do Heine **bastaria** para estas conclusões —
ao contrário do eixo tópicos. Registrar antes de rodar.
