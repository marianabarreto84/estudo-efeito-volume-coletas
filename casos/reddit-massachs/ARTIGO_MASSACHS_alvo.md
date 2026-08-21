# O alvo — Massachs et al. (2020): "Roots of Trumpism: Homophily and Social Feedback…"

> Leitura instrumental **completa** (full text lido em 7/ago/2026 — arXiv 2005.01790, versão
> aberta do WebSci'20). Plano em [REPLICACAO_CASO_MASSACHS.md](REPLICACAO_CASO_MASSACHS.md);
> viabilidade em [data/repl/massachs2016/FASE0_descoberta.md](data/repl/massachs2016/FASE0_descoberta.md).

**Ficha.** Joan Massachs, Corrado Monti, Gianmarco De Francisci Morales, Francesco Bonchi
(UPC / ISI Foundation / Eurecat). *Roots of Trumpism: Homophily and Social Feedback in
Donald Trump Support on Reddit.* **WebSci'20** (12th ACM Conf. on Web Science). DOI
10.1145/3394231.3397894. **29 citações** (Semantic Scholar, 7/ago/2026). Análise:
**homofilia** — tipo novo no lineup. ✅ **Dataset publicado** (`reddit-politics-12-16`,
`github.com/JoanMG/reddit-data`) — há gabarito, diferente do #207.

---

## 1. O que o artigo fez

### 1.1 Coleta e o estrato sub-coletado (o que o caso problematiza)

- **Fonte:** Reddit via **Pushshift** (Baumgartner et al.). Posts + comentários públicos.
- **Focus group (o filtro-chave):** usuários com **≥10 comentários em 2012 E ≥10 em 2016**
  em subreddits políticos (semente **r/politics** + os **50 mais similares** por LSA/cosseno).
  → **44.924 usuários** ("computational focus group"). **É a sub-coleta:** um estrato de
  usuários **persistentemente ativos em política**, ínfimo perto dos dezenas de milhões do
  Reddit.
- **Rótulo (apoiador de Trump):** participação em **r/The_Donald** em 2016 —
  operacionalizada como **≥4 comentários a mais** em r/The_Donald que em r/hillaryclinton
  **e** soma de scores ≥4 maior. → **7.083 (15,8%)** apoiadores × 37.841 (84,2%) não.
- **Tarefa:** prever, a partir **só de features de 2012**, quem participará de r/The_Donald
  em 2016.

### 1.2 As três hipóteses (features por usuário) e o método

- **Homofilia** = participação (binária) nos **top-1000 subreddits** populares.
- **Feedback social** = média dos scores positivos/negativos recebidos em subreddits políticos.
- **Influência direta** = interações (responder mensagens de quem postou no subreddit r) +
  interações conflituosas (uma msg ≥10, outra ≤−10).
- Baselines: **sentimento** (TextBlob) e **bag-of-words** (tf-idf dos títulos).
- Modelos: regressão logística, árvore, random forest; 5-fold CV; seleção de features
  (remove esparsas <500 usuários, Pearson p<0,05, VIF).

---

## 2. Resultados que viram afirmações testáveis

| # | Afirmação | Número | Onde |
|---|---|---|---|
| **MH1** | **Homofilia e feedback social preveem** apoio a Trump; **influência direta não** (é a **ordenação** entre as três) | Participação (homofilia) **F1 34,8%** ≈ Score (feedback) **33,7%** ≫ Interação (influência) **26,7%**; baseline aleatório 15,2% | §5.1, Tab. 1–2 |
| **MH1b** | O melhor modelo combina participação+score | **F1 35,3%, AUC 0,70** (prec. 0,27, rec. 0,56) | §5.1, Tab. 2 |
| **MH2** | **Persona** do apoiador: conservador/libertário, conspiração, PI, armas, empreendedorismo, interesses masculinos; anticorrelacionado com ateísmo, LGBT, culinária, tech | r/Conservative, r/Libertarian, r/conspiracy, r/4chan, r/guns, r/MensRights… (Tab. 5) | §5.2 |

**Conclusão-título:** homofilia (grupos sociais compartilhados) e conformidade/feedback
são as raízes do apoio a Trump no Reddit; influência direta importa pouco.

---

## 3. Por que este alvo serve à dissertação

Traz **homofilia** — tipo de análise ausente do lineup — num paper publicado (WebSci) e
com **dataset aberto**. O ângulo "coletar mais" ficou claro no full text: a conclusão vem
de um **estrato filtrado** — o focus group de usuários **persistentemente ativos em
política** (≥10 comentários em 2012 **e** 2016). É filtragem por critério clássica. A
pergunta do caso: *a ordenação "homofilia > influência" sobrevive quando se incluem os
usuários menos ativos* (que o filtro corta), cuja participação é mais esparsa? Eixos e
predições em [REPLICACAO_CASO_MASSACHS.md](REPLICACAO_CASO_MASSACHS.md).

⚠ **Ressalva de dado:** r/The_Donald foi **banido (jun/2020)**; mas as features são de
**2012** e o rótulo de **2016** — ambos no histórico do Pushshift/Arctic Shift/Academic
Torrents (r/The_Donald é dos banidos mais arquivados). Ver
[FASE0](data/repl/massachs2016/FASE0_descoberta.md).
