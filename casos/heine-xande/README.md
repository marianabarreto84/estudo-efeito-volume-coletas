# replicacao-caso-xande — Caso Heine (2025) do lineup da dissertação

Replicação por expansão da **dissertação do Alexandre "Xande" Heine (2025)**,
*Um Estudo sobre Amostragem em Grandes Volumes de Dados em RSD* (PUC-Rio, orient.
Lifschitz), aplicando o **mesmo fluxo** do caso Twitter/Ituassu
(`../pesquisa-twitter-refeita`) à dissertação da Mariana (`../dissertacao-escrita`).

## Leia primeiro
- [REPLICACAO_CASO_HEINE.md](REPLICACAO_CASO_HEINE.md) — plano de fases (o mapa).
- [DISSERTACAO_HEINE_alvo.md](DISSERTACAO_HEINE_alvo.md) — o alvo detalhado.
- [EIXO_TOPICOS.md](EIXO_TOPICOS.md) · [EIXO_QUANTITATIVO.md](EIXO_QUANTITATIVO.md) — os dois eixos.

## Estrutura (espelha o caso Twitter)
```
replicacao-caso-xande/
├── Dissertação_..._Alexandre Heine_...pdf   alvo (51 p.)
├── REPLICACAO_CASO_HEINE.md / DISSERTACAO_HEINE_alvo.md / EIXO_*.md
├── core/         db.py (conexao Postgres via tunel SSH — mesma infra do caso Twitter)
├── diagnostico/  lista_tabelas.py, explora_heine.py — Fase 0 (achar/caracterizar a tabela 2022)
├── pipeline/     extrai_snapshot_heine.py — Fase 1 (snapshot local)
├── analise/      (Fase 2-3: curva de convergencia tópicos + quantitativa)
├── data/repl/heine2022/   snapshots + RESULTADOS_*.md
└── documentos/   cópias de apoio
```

## Pré-requisitos para rodar
1. **VPN Cloud-DI (PUC-Rio) conectada** — exige elevação/admin (OpenVPN adiciona rotas).
   Teste: `ping 10.50.0.68` responde.
2. **`.env`** na raiz com credenciais SSH/Postgres (mesmo formato do caso Twitter;
   nunca versionar). Ver `../pesquisa-twitter-refeita/.env` como modelo.
3. `pip install paramiko sshtunnel psycopg2-binary` (conexão) e, para tópicos,
   `sentence-transformers bertopic umap-learn hdbscan scikit-learn`.

## Estado atual
- ✅ Documentação da replicação (fluxo do caso Twitter aplicado ao Heine).
- ✅ Infra de conexão (`core/db.py`) + scripts de descoberta (`diagnostico/`).
- ✅ **Fase 0 concluída** — ver `data/repl/heine2022/FASE0_descoberta.md`. Achado: o
  **Twitter 57,9 M do Heine não está nos bancos acessíveis** (3 VMs, 29 Postgres, 3 Mongo
  varridos). Acessível: **Instagram** dele (`xande_search`, 628 k) + **Reddit** no Mongo
  da vm031. O Twitter está no **SharePoint do BioBD** (conta `mbarreto@inf.puc-rio.br`).
- ⏳ **Fases 1–4 — em espera**: aguardando a Mariana baixar do SharePoint os CSVs
  (`1st_turn_day.csv`, `1st_turn_day_random_sample.csv`) ou o dump do Mongo Twitter.
  O pipeline (`pipeline/`, `analise/`) já aceita CSV (`content_text`) e SQLite.
