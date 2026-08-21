# Fase 0 — caso YouTube (AGECovP): alvo, gabarito e viabilidade

> Fechada em **18/ago/2026**, inteiramente **offline + API pública** (sem VPN, sem conta
> verificada, sem credencial de terceiro). É a célula **YouTube** da `tab:casos`.

---

## 1. O alvo

**Ghenai, Amira; Nath, Keshav; Satsangi, Aarat.** *AGECovP: identifying ageism and
analyzing COVID-19 discourse on older adults in YouTube.* **EPJ Data Science** 14:65,
publicado em **27/ago/2025**. DOI [10.1140/epjds/s13688-025-00582-6](https://doi.org/10.1140/epjds/s13688-025-00582-6).
Acesso aberto. **2.161 acessos**, **0 citações** (OpenAlex, 18/ago/2026).

⚠ **Tração declarada como fraca, e de propósito.** Nenhum alvo de YouTube do corpus da
survey tem citações relevantes — os 18 com amostragem declarada são todos de 2025–2026, e
o mais citado tem **3**. O critério que sobra é o **veículo**: a EPJ Data Science é
periódico revisado por pares de ciência de dados social, e é o único dos candidatos que
não é preprint. Isso tem de ser dito no capítulo, como se disse do Meta Ads.

---

## 2. Por que este alvo é executável quando os outros não são

A comparação entre as rotas de coleta, medida nesta mesma sessão, é o que decidiu:

| rede | rota | estado em ago/2026 |
|---|---|---|
| Instagram/Facebook | Ad Library API | exige **conta com documento verificado** (1–3 dias úteis) |
| TikTok | Research API | credencial do eTC **morta**; aprovação nova leva semanas |
| **YouTube** | **Data API v3** | **chave em ~5 min, grátis, sem verificação** ✅ |

E o dado do YouTube **persiste**: vídeos e comentários de 2020 continuam buscáveis hoje —
verificado com uma consulta real. É o que separa este alvo do #363 (Taiwan), cujo objeto
é o **grafo de recomendações**, volátil por construção porque o instrumento é o próprio
algoritmo.

---

## 3. O gabarito publicado — baixado e **conferido**

Os autores publicaram o dataset completo em
[zenodo.org/records/15800324](https://zenodo.org/records/15800324) (03/jul/2025).
Baixado para [`gabarito_zenodo/`](gabarito_zenodo/):

| arquivo | linhas | confere com o artigo? |
|---|--:|---|
| `videos.csv` | **3.782** | ✅ exato |
| `channels.csv` | **2.243** | ✅ exato |
| `comments.csv` | **69.425** | ✅ exato |
| `labelled_comments.csv` | **4.389** | ◐ o artigo diz 4.390 (diferença de 1, provavelmente contagem de cabeçalho) |

Cobertura temporal medida nos dados: vídeos de **28/jan/2020 a 21/ago/2022**
(1.805 em 2020, 1.683 em 2021, 294 em 2022); comentários de **12/fev/2020 a 28/nov/2023**.
Rótulos de ageísmo: **810 `TRUE` (18,5%)** × 3.579 `FALSE`.

`videos.csv` traz texto (título, descrição, tags), métricas e **toxicidade**;
`comments.csv` traz toxicidade, profanidade, insulto e sentimento por **VADER** e
**TextBlob**. Ou seja: as análises do artigo são reproduzíveis **sem gastar API**.

---

## 4. A sub-coleta — que é o objeto do caso

O funil está declarado no §2 do artigo, passo a passo:

```
17 termos de "older adults" × 5 de "Covid-19"  =  85 combinações de busca
   (cada uma: todos os resultados ou as 12 primeiras páginas = 600, o que vier antes)
        ↓
   6.997 vídeos iniciais
        ↓  filtro de regex: a palavra-chave tem de aparecer no TÍTULO ou na DESCRIÇÃO
        ↓  (+ remoção de vídeos deletados)
   3.353 vídeos                                    ← descarta 52,1%
        ↓
   + "Suggested Videos" de cada um: 104.172 vídeos
        ↓  mesmo filtro de palavra-chave
   1.025 vídeos                                    ← descarta 99,0%  ★
        ↓
   4.378 vídeos  →  filtro de idioma (não-inglês)  →  3.782 finais
```

★ **É aqui que mora o caso.** O filtro de palavra-chave descarta **99% do que o próprio
YouTube apontou como vizinhança temática** dos vídeos já coletados. Exigir que a palavra
de busca reapareça no título ou na descrição é um critério de **forma**, não de assunto —
e quem escreve título com palavra-chave é, tipicamente, **veículo de imprensa**, não
usuário comum. É filtragem por critério no estado puro: a norma que a survey documenta.

### Os termos (Tabela 1 do artigo)

**Older adults (N=17):** `ageism, ageist, elderly, older, boomer, senior, aging, ageing,
later life, age-related, retiree, retired, elders, geriatric, grandparent, grandmother,
grandfather`

**Covid-19 (N=5):** extraídos do PDF como `coronavirus, covid19, covid-19, covid19,
coronavirus` — ⚠ **com duplicatas aparentes**. Quase certamente é artefato da extração
(o PDF perde espaços: `corona virus`→`coronavirus`, `covid 19`→`covid19`).
**Não reportar como achado sem conferir na tabela renderizada.** A hipótese de trabalho é
que a lista real seja `coronavirus, corona virus, covid19, covid 19, covid-19`.

### A lista do filtro

O filtro de palavra-chave dos vídeos sugeridos usa uma lista **muito maior** (~88 termos),
publicada em nota de rodapé — de `elderly` e `nursing home` a `old geezer` e
`can't teach an old dog new tricks`. Está transcrita em
[`termos_agecovp.json`](termos_agecovp.json).

---

## 5. Alvos-teste (o que a replicação vai medir)

| # | afirmação | número | família |
|---|---|---|---|
| **AG1** | distribuição de sentimento dos comentários | TextBlob **39% neutro / 39% positivo / 22% negativo**; VADER 39/39/22 (positivo/negativo/neutro) | descritiva |
| **AG2** | **os comentários são mais negativos que os vídeos** | comparação de distribuições | **comparativa** |
| **AG3** | o conteúdo é dirigido por **veículos de imprensa**, não por usuários | **UGC < 7%** | descritiva |
| **AG4** | composição por categoria de canal | Society **56,4%**, Lifestyle 13,6%, Knowledge 12,1%, Politics 4,1%, Health 3,7% | descritiva |

**AG2 é o alvo central**, por ser comparativo — a família que, nos casos já fechados,
sobrevive à expansão (vacinas, linha 6). **AG3 é o alvo mais exposto**: é exatamente a
quantidade que o filtro deveria enviesar.

---

## 6. Predições pré-registradas (18/ago/2026, antes de coletar)

Registradas antes de qualquer coleta, conforme o princípio §7 do `CLAUDE.md`.

| # | aposta | raciocínio |
|---|---|---|
| **P1** | **AG3 muda muito** — a fatia de UGC **sobe** ao soltar o filtro (aposta: mais que dobra) | o filtro exige palavra-chave no título/descrição, e isso é prática editorial de imprensa; canal pessoal titula "my grandma got covid", sem os termos da lista |
| **P2** | **AG1 muda** — a distribuição de sentimento fica **mais negativa** | conteúdo institucional é mais neutro/positivo; ao entrar UGC, entra reclamação |
| **P3** | **AG2 não muda** — comentários seguem mais negativos que vídeos | é comparação entre dois níveis do mesmo corpus, e o viés do filtro atinge os dois |
| **P4** | AG4 muda: a fatia "Society" (56,4%) **cai** | é a categoria dos canais institucionais |

Se P1–P2 falharem e P3 sobreviver, o caso **converge** com o padrão dos casos anteriores
(comparativo robusto, descritivo frágil) numa **quarta rede** e num tipo de análise novo.

---

## 7. O que dá e o que **não** dá para expandir

| ramo do funil | recoletável hoje? |
|---|---|
| busca (85 combinações → 6.997 → 3.353) | ✅ **sim** — `search.list` funciona e alcança vídeos de 2020 |
| **vídeos sugeridos** (→ 104.172 → 1.025) | ❌ **não** — o parâmetro `relatedToVideoId` foi **removido da API em ago/2023** |

⚠ Consequência de método, a declarar: o ramo **★** (o mais espetacular, 99% de descarte)
**não é reproduzível**. O que se testa é o **mesmo filtro de regex** aplicado ao ramo da
busca, onde ele descarta 52% — e a comparação com o gabarito diz se a nossa reconstrução
do ramo da busca é fiel.

Isto é, por si, um segundo achado sobre perecibilidade: **um trabalho de 2025 já tem uma
etapa de coleta irreproduzível**, porque a API mudou entre a coleta e a publicação.

---

## 8. Custo de API (cota de 10.000 unidades/dia, grátis)

| operação | custo | volume do caso |
|---|--:|---|
| `search.list` | **100** un. / 50 resultados | 85 combinações × 12 páginas = 1.020 chamadas = **102.000 un.** → ~10 dias de cota |
| `search.list`, 2 páginas | 100 un. | 170 chamadas = **17.000 un.** → ~2 dias |
| `videos.list` | 1 un. / 50 ids | desprezível |
| `commentThreads.list` | 1 un. / 100 comentários | desprezível |

**Decisão de escopo (prazo de 31/ago):** rodar **2 páginas por combinação** (100 vídeos),
não 12. Cobre a mesma população com profundidade menor, cabe em ~2 dias de cota, e a
comparação filtro × sem-filtro — que é o alvo — não depende da profundidade. Declarar.

A cota zera à **meia-noite do Pacífico** (4h–5h no Brasil).

---

## 9. Estado

- ✅ artigo lido; funil, termos e lista de filtro extraídos
- ✅ gabarito baixado e **conferido linha a linha** contra o artigo
- ✅ chave da API criada e **testada** (retorna vídeos de 2020)
- ✅ alvos-teste e predições pré-registrados
- ⏳ Fase 1 — coleta (2 páginas × 85 combinações)
- ⏳ Fase 2 — reproduzir AG1–AG4 sobre o gabarito
- ⏳ Fase 3 — aplicar/soltar o filtro na nossa coleta e medir a mudança
