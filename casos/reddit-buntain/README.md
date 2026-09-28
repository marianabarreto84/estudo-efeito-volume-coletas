# Caso de replicação · Reddit · Buntain & Golbeck (2014) — papéis sociais / SNA

**Leia primeiro:** o plano em [REPLICACAO_CASO_BUNTAIN.md](REPLICACAO_CASO_BUNTAIN.md) e o
alvo em [ARTIGO_BUNTAIN_alvo.md](ARTIGO_BUNTAIN_alvo.md).

Caso Reddit do lineup (substitui o #207 descartado — ver
[`../reddit-companhia-ia/`](../reddit-companhia-ia/)). Alvo: **Buntain & Golbeck 2014**
(WWW, **133 citações**), que identificou o papel *answer-person* por **estrutura de rede**
num estrato de topo de 13 subreddits. Traz a análise de **rede/SNA** que faltava no lineup.

## Estado atual (7/ago/2026)

- ✅ **Fase 0 documental** — alvo caracterizado (paper lido na íntegra), eixos e predições
  pré-registrados, rota de coleta decidida. Ver
  [data/repl/buntain2013/FASE0_descoberta.md](data/repl/buntain2013/FASE0_descoberta.md).
- ✅ **Alvo relevante** — publicado (WWW'14) e bastante referenciado (133 cit.), atende ao
  critério novo do lineup.
- ✅ **Rota: Arctic Shift** — rede confirmada daqui (User-Agent de navegador). Volume do
  universo sondado: **43.479 submissions + ~943 mil comentários** nos 13 subreddits
  (jul/2013). Ver [FASE1_coleta.md](data/repl/buntain2013/FASE1_coleta.md).
- ⏳ **Fase 1 EM ANDAMENTO** (7/ago/2026) — pipeline validado; coleta dos 9 subreddits
  grandes rodando em background → `snapshot_buntain.sqlite` (resumível). Depois:
  [`analise/rb3.py`](analise/rb3.py) para o teste RB3.

**Alvo-teste central (RB3):** o paper afirma que só **~3% dos usuários** participam de >1
comunidade (7/279) — provável artefato da sub-coleta. É um teste mudou?/convergiu? limpo e
**sem gabarito humano**.

## Estrutura

```
reddit-buntain/
├── README.md                    <- este arquivo
├── REPLICACAO_CASO_BUNTAIN.md   <- plano de fases (4 eixos de expansão)
├── ARTIGO_BUNTAIN_alvo.md       <- o artigo destrinchado
├── core/arctic.py               <- cliente Arctic Shift (paginação)
├── pipeline/
│   ├── probe_volume.py          <- sonda de volume (jul/2013)
│   └── collect.py               <- coletor resumível -> snapshot_buntain.sqlite
├── analise/rb3.py               <- teste RB3 (multi-comunidade); grava curva_rb3.json
└── data/repl/buntain2013/
    ├── FASE0_descoberta.md      <- viabilidade + predições
    ├── FASE1_coleta.md          <- volume do universo + estado da coleta
    ├── RESULTADOS_RB3.md        <- o resultado: 3% -> 57,6% sob o mesmo limiar
    ├── RB3_recorte_reconstruido.md <- 25/set: o recorte do artigo refeito no nosso
    │                               dado (259 x 279). Qualifica o 19x; ver ESTADO §4.31
    ├── curva_rb3.json           <- (gerado) curva por limiar; alimenta a Fig. 5.1
    │                               da dissertação via figuras/gerar_figuras.py
    └── snapshot_buntain.sqlite  <- (gerado) submissions + comentários
```

> ⚠ `rb3.py` só roda onde o `snapshot_buntain.sqlite` existe, isto é, na cópia com
> dados (`Documents/dissertacao/`) — o `.sqlite` é `.gitignore`. O `curva_rb3.json`,
> por ser pequeno, **é** versionado, para que a figura da dissertação seja
> reproduzível a partir do repositório.
