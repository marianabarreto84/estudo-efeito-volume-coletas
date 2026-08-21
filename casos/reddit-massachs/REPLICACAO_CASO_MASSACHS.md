# Caso de replicação · Reddit · Massachs et al. (2020) — homofilia no apoio a Trump

> Caso Reddit do lineup (irmão do [`../reddit-buntain/`](../reddit-buntain/)). Alvo:
> **Massachs et al. 2020** (WebSci, 29 cit.), **homofilia**. Full text lido (7/ago/2026).
> Alvo em [ARTIGO_MASSACHS_alvo.md](ARTIGO_MASSACHS_alvo.md); viabilidade em
> [data/repl/massachs2016/FASE0_descoberta.md](data/repl/massachs2016/FASE0_descoberta.md).

**Valor no lineup.** Traz **homofilia** (tipo de análise ausente), com **dataset aberto**
(gabarito) e um estrato sub-coletado nítido: o *focus group* de **44.924 usuários
persistentemente ativos em política** (≥10 comentários em 2012 **e** 2016). A conclusão
"homofilia > influência" é, formalmente, uma afirmação **sobre esse estrato** — o caso
pergunta se ela sobrevive nos usuários menos ativos que o filtro descartou.

---

## 1. Afirmações testáveis

- **MH1** — ordenação: **homofilia (F1 34,8%) ≈ feedback (33,7%) ≫ influência (26,7%)**.
- **MH1b** — melhor modelo participação+score: **F1 35,3%, AUC 0,70**.
- **MH2** — persona (r/Conservative, r/Libertarian, r/conspiracy, r/4chan, r/guns…).

---

## 2. Os eixos de expansão (separáveis)

O paper ocupa **um ponto**: focus group ≥10 comentários/ano, semente r/politics+50,
2012→2016. Cada restrição é um eixo.

| Eixo | Restrição (paper) | Expansão | Isola a pergunta |
|---|---|---|---|
| **E1 · Limiar de atividade** | ≥10 comentários em 2012 **e** 2016 | ≥5, ≥1 comentário | "a conclusão vale fora do estrato hiperativo?" |
| **E2 · Semente política** | r/politics + 50 similares | semente mais larga / entradas não-políticas | "o recorte de subreddits define o resultado?" |
| **E3 · Cobertura de features** | corta subreddits <250–500 usuários | sem corte | "features raras mudam o ranking?" |

**Contraste-chave:** a hipótese é que **MH1 (a ordem) sobreviva**, mas que o **F1 da
homofilia caia** ao incluir usuários menos ativos (participação fica esparsa), podendo
encostar no do feedback/influência — testando se a vantagem da homofilia era do estrato.

---

## 3. Pipeline por fase

### Fase 0 ✅ (documental, completa)
Alvo caracterizado (full text), eixos e predições pré-registrados, gabarito localizado
(dataset dos autores), rota de coleta definida. Ver [FASE0](data/repl/massachs2016/FASE0_descoberta.md).

### Fase 1 — Ponto original + snapshot ⏳
Baixar o dataset dos autores (`reddit-politics-12-16`) = ponto original reproduzível; e dos
**dumps 2012+2016** (Arctic Shift/Academic Torrents) reconstruir o focus group com **limiar
de atividade menor** (E1). Congelar `snapshot_massachs.sqlite` (features por usuário +
rótulo r/The_Donald 2016).

### Fase 2 — Curva A(volume)
Re-treinar os classificadores (LR/RF, 5-fold) em focus groups de tamanho crescente (do
≥10 do paper ao ≥1), medindo por ponto o **F1 de cada família** (homofilia, feedback,
influência) e a **ordem** entre elas. ≥30 réplicas/ponto.

### Fase 3 — Divergência
- **MH1:** a ordem homofilia>influência inverte/comprime em algum limiar? A que fração?
- **MH2:** os subreddits-âncora da persona mudam?

### Fase 4 — Linha da tabela mestre
Preencher a linha 12 (*Reddit / homofilia*) com o veredito de MH1.

---

## 4. Onde apostar (predições pré-registradas — antes de rodar)

- **Provável CONFIRMA:** a **ordenação** homofilia/feedback > influência (efeito forte, é ordem).
- **Provável MUDA (interessante):** o **F1 da homofilia cai** ao incluir usuários menos
  ativos (participação esparsa) — se a vantagem some, a conclusão era do estrato hiperativo.
- **Persona:** âncoras robustas; cauda reordena.
- Segue o padrão cross-case (comparativo robusto, magnitude não) — a confirmar. Registrar
  humildade se a ordem cair.

---

## 5. Decisões pendentes

1. **Limiar(es) de atividade** a testar em E1 (≥5, ≥3, ≥1?) e passo da curva.
2. Reproduzir com o **mesmo pipeline** do paper (LR/RF + seleção de features) ou documentar
   trocas.
3. Escala: reconstruir features de milhões de usuários dos dumps 2012/2016 — confirmar que
   os agregados por usuário cabem local.

---

*Docs irmãos: [ARTIGO_MASSACHS_alvo.md](ARTIGO_MASSACHS_alvo.md) ·
[FASE0_descoberta.md](data/repl/massachs2016/FASE0_descoberta.md).*
