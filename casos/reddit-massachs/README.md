# Caso de replicação · Reddit · Massachs et al. (2020) — homofilia

**Leia primeiro:** [REPLICACAO_CASO_MASSACHS.md](REPLICACAO_CASO_MASSACHS.md) e
[ARTIGO_MASSACHS_alvo.md](ARTIGO_MASSACHS_alvo.md).

Caso Reddit do lineup (irmão do [`../reddit-buntain/`](../reddit-buntain/)). Alvo:
**Massachs et al. 2020** (WebSci, 29 cit.), *homofilia* no apoio a Trump (r/The_Donald).
Traz um **tipo de análise novo** (homofilia/polarização).

## Estado atual (18/ago/2026)

- ✅ **Fase 0 completa** — full text lido (arXiv 2005.01790), alvo caracterizado, eixos e
  predições pré-registrados. Estrato sub-coletado = focus group de 44.924 usuários (≥10
  comentários em 2012 **e** 2016). Alvo-teste **MH1**: homofilia (F1 34,8%) ≈ feedback
  (33,7%) ≫ influência (26,7%).
- ✅ **Fase 1a feita (18/ago/2026)** — dataset dos autores **baixado e conferido**:
  44.924 usuários e 7.083 apoiadores (15,77%) batem **exatamente** com o artigo.
  ⚠ o repositório real é `github.com/JoanMassachs/reddit-data` (o `JoanMG` da Fase 0
  redireciona). `sha256` registrado na [Fase 2](data/repl/massachs2016/FASE2_ponto_original.md).
- ✅ **Fase 2 feita (18/ago/2026) — MH1 REPRODUZ.** A ordenação homofilia ≈ feedback ≫
  influência sai idêntica, com as duas pontas a **<0,25 p.p.** do publicado
  (34,6% × 34,8% e 26,8% × 26,7%). Ver
  [FASE2_ponto_original.md](data/repl/massachs2016/FASE2_ponto_original.md).
- ⏳ **Fase 3 (o "coletar mais")** — baixar dumps 2012/2016 e refazer o focus group com
  limiar de atividade menor (≥5, ≥3, ≥1). **Único passo pesado que resta; sem VPN.**
- ⚠ r/The_Donald banido (2020) — histórico em dumps (Arctic Shift/Academic Torrents).

## Estrutura

```
reddit-massachs/
├── README.md
├── REPLICACAO_CASO_MASSACHS.md   <- plano preliminar (⏳ depende do full text)
├── ARTIGO_MASSACHS_alvo.md       <- alvo do abstract (⏳ full text pendente)
├── analise/
│   └── mh1_ponto_original.py     <- reproduz MH1 sobre o gabarito dos autores
└── data/repl/massachs2016/
    ├── FASE0_descoberta.md       <- viabilidade + o que falta
    ├── FASE2_ponto_original.md   <- MH1 reproduzido (18/ago/2026)
    ├── mh1_ponto_original.json   <- números da Fase 2
    ├── reddit-politics-12-16.csv.bz2  <- gabarito dos autores (17,7 MB)
    └── README_autores.md         <- dicionário de features, dos autores
```
