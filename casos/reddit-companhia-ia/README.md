# ❌ CASO DESCARTADO — Reddit / #207 "My Boyfriend is AI"

> **Descartado em 07/ago/2026 por decisão da Mariana.** Motivo: o alvo (#207,
> Pataranutaporn et al. 2025, arXiv 2509.11391) é um **preprint sem tração** —
> publicação informal no CoRR/arXiv, sem aceitação registrada e ainda pouco citada. O
> critério do lineup passou a ser **relevância** (artigo "da casa" ou **bastante
> referenciado**), e o #207 não atende. **Não é falha de método** — a Fase 0 documental
> chegou a ser feita; foi decisão de escopo.

**Substituído por dois casos de Reddit revisados/influentes**, escolhidos do corpus da
survey (fatia 2011–2024, que tem os papers já referenciados):

- [`../reddit-buntain/`](../reddit-buntain/) — Buntain & Golbeck 2014 (WWW, 133 citações),
  **SNA / papéis sociais** (answer-person por estrutura de rede).
- [`../reddit-massachs/`](../reddit-massachs/) — Massachs et al. 2020 (WebSci, 29 citações),
  **homofilia** (apoio a Trump no Reddit).

## Conhecimento reaproveitável (não se perde)

A Fase 0 do #207 produziu dois achados que **valem para os casos novos** (também Reddit):

1. **Rota de coleta Reddit: Arctic Shift** (`arctic-shift.photon-reddit.com`) — dumps
   pós-Pushshift com posts **e comentários**, por subreddit/janela. A API oficial **não
   serve** (teto ~1.000 itens/listagem). Academic Torrents como fallback. Cobertura ampla
   confirmada por consulta à API em 7/ago/2026.
2. **Reconstrução de gabarito:** quando o dataset original do paper não está publicado,
   reconstrói-se o ponto original de dentro da coleta completa (por `score`/critério do
   paper) — sem efeito-de-escopo.

Detalhe da decisão em `ESTADO.md` §3.7/§4.7.
