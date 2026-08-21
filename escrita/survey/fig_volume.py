# =====================================================================
#  Gera a Figura de volume de coleta (Seção de Resultados).
#  Fonte: research.db do sistema. O volume estruturado (pares
#  quantidade/unidade) vive DENTRO do JSON `articles.analyses` sob a
#  chave do modelo Gemini (cobertura total do corpus extraído), e não
#  na coluna top-level `collection_items` (que só foi promovida para a
#  coorte 2025-2026). Por isso lemos de analyses['gemini'].
#  Uso: python fig_volume.py  ->  fig_volume.pdf
#
#  Volume principal por artigo = maior quantidade entre os
#  collection_items, EXCLUÍDAS unidades que não são itens coletados
#  (tokens de corpus de embeddings, visualizações/engajamento, palavras,
#  sentenças de snippets, requisições HTTP) — ver BLOCK. Buckets por
#  ordem de grandeza (base 10). Corte de "grande coletor" = 10^7.
# =====================================================================
import sqlite3, json, os, re, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DB = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\research.db"

# unidades que NÃO são itens de coleta (evita inflar o volume com
# tokens de embeddings, contadores de views, etc.)
BLOCK = re.compile(r"token|palavra|\bword|visualiza|\bview|impress|"
                   r"senten|sentence|requisi|http")

def max_collected(gemini):
    """Maior quantidade coletada de um bloco de extração do Gemini,
    ignorando unidades fora de escopo (BLOCK)."""
    if not isinstance(gemini, dict):
        return None
    items = gemini.get("collection_items")
    if not isinstance(items, list):
        return None
    best = None
    for it in items:
        if not isinstance(it, dict):
            continue
        q = it.get("quantity")
        u = (it.get("unit") or "").lower()
        if isinstance(q, (int, float)) and q > 0 and not BLOCK.search(u):
            if best is None or q > best:
                best = q
    return best

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
rows = con.execute(
    "select analyses from articles "
    "where analyses is not null "
    "and trim(analyses) not in ('','null','[]','{}')"
).fetchall()

vols = []
for r in rows:
    try:
        gem = json.loads(r["analyses"]).get("gemini")
    except Exception:
        continue
    # exclui artigos sinalizados pelo Gemini como não-coleta de RSD
    # (suggested_discard), coerentes com a base 1.718 dos Resultados
    if isinstance(gem, dict) and gem.get("suggested_discard"):
        continue
    v = max_collected(gem)
    if v:
        vols.append(v)

labels = [r"$<10^{3}$", r"$10^{3}$–$10^{4}$", r"$10^{4}$–$10^{5}$",
          r"$10^{5}$–$10^{6}$", r"$10^{6}$–$10^{7}$", r"$\geq 10^{7}$"]
edges = [1e3, 1e4, 1e5, 1e6, 1e7]

def bucket(v):
    for i, e in enumerate(edges):
        if v < e:
            return i
    return len(edges)

counts = [0] * len(labels)
for v in vols:
    counts[bucket(v)] += 1

n = len(vols)
big = counts[-1]
print("N =", n, "  counts =", counts)
print("mediana = %.0f" % statistics.median(vols))
print("%% <10k = %.1f | %% >=1M = %.1f | grandes coletores (>=10M) = %d (%.1f%%)"
      % (100*sum(1 for v in vols if v < 1e4)/n,
         100*sum(1 for v in vols if v >= 1e6)/n, big, 100*big/n))

# ---- figura ---------------------------------------------------------
BASE = "#4C6E91"   # azul acinzentado, sóbrio para impressão
HILITE = "#B4462F" # terracota para destacar os grandes coletores
colors = [BASE] * (len(labels) - 1) + [HILITE]

fig, ax = plt.subplots(figsize=(6.4, 3.1))
bars = ax.bar(range(len(labels)), counts, color=colors, width=0.72,
              edgecolor="white", linewidth=0.5)

for x, c in zip(range(len(labels)), counts):
    ax.text(x, c + max(counts) * 0.02, str(c), ha="center", va="bottom",
            fontsize=10, color="#222222")

ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("Nº de artigos", fontsize=10)
ax.set_xlabel("Volume coletado (itens, ordem de grandeza)", fontsize=10)
ax.set_ylim(0, max(counts) * 1.18)

# anotação dos grandes coletores
ax.annotate("%d grandes coletores\n($\\geq$10 milhões)" % big,
            xy=(len(labels) - 1, counts[-1]),
            xytext=(len(labels) - 1.9, max(counts) * 0.92),
            fontsize=8.5, color=HILITE, ha="center",
            arrowprops=dict(arrowstyle="->", color=HILITE, lw=0.8))

for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(length=0)
ax.yaxis.grid(True, color="#DDDDDD", lw=0.6)
ax.set_axisbelow(True)

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig_volume.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=160, bbox_inches="tight")
print("salvo em", out)
