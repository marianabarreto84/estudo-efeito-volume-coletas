# Caso de replicação · Reddit · Buntain & Golbeck (2014) — papéis sociais por estrutura de rede

> Caso Reddit do lineup (substitui o #207 descartado). Alvo: **Buntain & Golbeck 2014**
> (WWW, 133 citações), que identificou o papel *answer-person* por **estrutura de rede**
> num estrato de topo de 13 subreddits. Análise: **SNA / papéis sociais** — tipo novo no
> lineup. Alvo destrinchado em [ARTIGO_BUNTAIN_alvo.md](ARTIGO_BUNTAIN_alvo.md);
> viabilidade em [data/repl/buntain2013/FASE0_descoberta.md](data/repl/buntain2013/FASE0_descoberta.md).

**Valor no lineup.** Traz a **análise de rede/centralidade** que faltava, com um paper
**influente** (133 cit.), e tem um **alvo-teste de manual**: a afirmação de que só **3%
dos usuários participam de múltiplas comunidades** (7 de 279) — quase certamente artefato
da sub-coleta. É o par mudou?/convergiu? no seu formato mais limpo, e **sem precisar de
gabarito humano**.

---

## 1. Afirmações testáveis

Transcritas do alvo (ver [ARTIGO_BUNTAIN_alvo.md](ARTIGO_BUNTAIN_alvo.md) §2):

- **RB1** — o papel *answer-person* existe (qualitativo).
- **RB2** — identificável só por estrutura (~80%); estrutura (80%) > filiação (69%).
- **RB3** — só **~3%** dos usuários (7/279) participam de >1 comunidade. **← o alvo central.**

**Ressalva de reprodutibilidade:** RB1 e RB2 dependem da **rotulagem manual** de
answer-person (assinatura de ego-rede) — é uma etapa humana, como no stance. **RB3 não**:
é contagem estrutural pura. Por isso RB3 é o eixo primário; RB1/RB2 entram se/quando
houver esforço de rotulagem (reaproveitável do fluxo do caso vacinas).

---

## 2. Os eixos de expansão (separáveis)

O paper ocupa **um ponto**: top-100 submissions × top-200 comentários × 1 mês × corte
≥20 arestas. Cada camada é um eixo.

| Eixo | Restrição (paper) | Expansão | Isola a pergunta |
|---|---|---|---|
| **E1 · Profundidade de submissions** | top-100 do mês | todas as submissions | "o topo representava a rede?" |
| **E2 · Profundidade de comentários** | top-200/submission | todos os comentários | "a rede de interação muda com o volume?" |
| **E3 · Corte de grau** | descarta <20 arestas | sem corte (todos os nós) | "o corte fabricou a estrutura?" |
| **E4 · Janela temporal** | julho/2013 | janela maior (meses/anos) | "1 mês representa a comunidade?" |

**Contraste-chave:** a hipótese é que **RB1 sobreviva** (o papel existe de qualquer jeito),
**RB2 fique instável** (a assinatura "estrela esparsa" do answer-person pode borrar quando
os comentários não são mais cortados em 200 — mais arestas, ego-redes mais densas), e
**RB3 mude forte** (os 3% sobem muito) — o mesmo objeto ("coletar mais") com respostas
diferentes por tipo de afirmação.

---

## 3. Pipeline por fase

### Fase 0 — Alvo + viabilidade ✅ (documental)
Feita: alvo caracterizado, eixos e predições pré-registrados, rota de coleta levantada.
Ver [FASE0_descoberta.md](data/repl/buntain2013/FASE0_descoberta.md).

### Fase 1 — Coletar o universo + snapshot ⏳
Baixar, via **Arctic Shift / dumps**, **todas** as submissions e comentários dos **13
subreddits** em julho/2013 (e, para E4, uma janela maior). Materializar
`snapshot_buntain.sqlite` com `submissions` e `comments` (com `author`, `parent_id`,
`link_id`, `subreddit`, `created_utc`, `score`). Reconstruir o **ponto original** aplicando
os filtros do paper (top-100 subs × top-200 comentários × ≥20 arestas) → o n=279 é um
**subconjunto materializado** do universo (sem efeito-de-escopo).

### Fase 2 — Curva A(volume) (o coração)
Reconstruir os grafos de interação em frações crescentes (do estrato do paper ao universo),
medindo por fração:
- **RB3 (primário):** fração de usuários ativos em >1 dos 13 subreddits. Curva do "3%" ×
  volume. **≥30 réplicas** (subamostras) por ponto p/ banda bootstrap.
- **RB2 (se rotular):** acurácia do classificador estrutural e o gap estrutura×filiação,
  por fração; estabilidade das assinaturas de ego-rede.
- Métricas de rede auxiliares: grau, densidade, coef. de clustering por fração.

### Fase 3 — Divergência (métricas)

| Afirmação | Métrica | Pode inverter/confirmar |
|---|---|---|
| **RB3** (3% multi-comunidade) | % de usuários em >1 subreddit por fração; IC bootstrap | a que volume os 3% deixam de valer? |
| **RB2** (estrutura>filiação) | acurácia por fração; estabilidade da assinatura answer-person | a assinatura sobrevive sem o corte de comentários? |
| **RB1** (papel existe) | presença de nós com assinatura answer-person | robusto (esperado) |

### Fase 4 — Linha da tabela mestre
Preencher a linha *Reddit / SNA (papéis)* em [`../RESULTADOS_tabela_mestre.md`](../RESULTADOS_tabela_mestre.md)
com o veredito de RB3 (e RB1/RB2 se rotulados), *a coleta bastava? × a conclusão mudou? ×
fração mínima que estabiliza*.

---

## 4. Onde apostar (predições pré-registradas — antes de rodar)

- **Provável MUDA (forte):** RB3 — os 3% **sobem muito**. A sub-coleta (top-submissions +
  corte ≥20 arestas + 1 mês) esconde a atividade cruzada por construção. É a aposta
  central e a mais falsificável.
- **Provável CONFIRMA:** RB1 — o papel answer-person existe (não some com mais dados).
- **Incerto / interessante:** RB2 — a assinatura estrutural "estrela esparsa" pode
  **borrar** ao não cortar comentários em 200; o gap estrutura(80%)×filiação(69%) pode
  encolher. Se a assinatura depende do corte, é achado forte ("a estrutura era do recorte").
- **Provável NÃO CONVERGIU:** n=279 (7 multi-comunidade) é minúsculo — a estimativa de RB3
  não havia estabilizado.
- **Registrar humildade:** se RB3 **não** subir (os 3% forem robustos), é um resultado
  igualmente publicável e honesto — anotar.

---

## 5. Decisões pendentes (específicas)

1. **Rotular ou não** answer-person (para RB1/RB2)? RB3 anda sem isso. Se sim, reusar o
   fluxo de rotulagem do caso vacinas (`core/orcamento.py`, teto de gasto).
2. **Janela do E4:** só julho/2013 (fiel) ou janela maior (separa efeito-temporal do
   efeito-volume)?
3. **Definição de "participar de uma comunidade"** ao medir RB3: ≥1 comentário? ≥k? Fixar
   o limiar e reportar sensibilidade (o paper usou o corte de ≥20 arestas, que é parte do
   que problematizamos).

---

*Docs irmãos: [ARTIGO_BUNTAIN_alvo.md](ARTIGO_BUNTAIN_alvo.md) ·
[FASE0_descoberta.md](data/repl/buntain2013/FASE0_descoberta.md). Caso-irmão de Reddit:
[`../reddit-massachs/`](../reddit-massachs/) (homofilia).*
