# =====================================================================
#  Concordancia inter-modelo (kappa de Cohen) por familia de campo,
#  + o efeito da cobertura desigual dos modelos sobre a tabela de
#  tipos de analise. Gera fig_kappa.pdf e imprime os numeros.
#
#  Base: os artigos lidos pelos DOIS modelos (Gemini e Claude Haiku),
#  dentro da base de analise (pos-descarte). Reaproveita a logica de
#  agg_results.py / figuras.py sem redefini-la.
#
#  Uso:  python validacao.py
# =====================================================================
import sqlite3, json, re, os, unicodedata
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import figuras as F  # reusa norm/bucketize/carga? nao: reimporta so as regras

DB = F.DB
OUT = os.path.dirname(os.path.abspath(__file__))
AZUL, CLARO, TERRA = F.AZUL, F.CLARO, F.TERRA
TINTA = F.TINTA
norm, bucketize = F.norm, F.bucketize
ANALYSIS_BUCKETS = F.ANALYSIS_BUCKETS

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
rows = con.execute(
    "select analyses from articles where analyses is not null "
    "and trim(analyses) not in ('','null','[]','{}')").fetchall()

todos, arts = [], []
for r in rows:
    try:
        a = json.loads(r["analyses"])
    except Exception:
        continue
    if not any(isinstance(a.get(m), dict) for m in ("gemini", "claude_haiku")):
        continue
    todos.append(a)
    g = a.get("gemini")
    if isinstance(g, dict) and g.get("suggested_discard"):
        continue
    arts.append(a)

dois = [a for a in arts if isinstance(a.get("gemini"), dict)
        and isinstance(a.get("claude_haiku"), dict)]
so_gem = [a for a in arts if isinstance(a.get("gemini"), dict)
          and not isinstance(a.get("claude_haiku"), dict)]
print(f"base = {len(arts)} | lidos pelos dois = {len(dois)} | so Gemini = {len(so_gem)}")


def kappa(pares):
    n = len(pares)
    if not n:
        return None
    a = sum(1 for x, y in pares if x and y)
    b = sum(1 for x, y in pares if x and not y)
    c = sum(1 for x, y in pares if not x and y)
    d = n - a - b - c
    po = (a + d) / n
    pe = ((a + b) * (a + c) + (c + d) * (b + d)) / (n * n)
    k = (po - pe) / (1 - pe) if pe != 1 else 1.0
    return k, po


def plat(m, p):
    return any(p in norm(s) for s in (m.get("social_networks") or []) if isinstance(s, str))


def buckets(m):
    out = set()
    for at in (m.get("analysis_types") or []):
        if isinstance(at, str):
            b = bucketize(at)
            if b:
                out.add(b)
    return out


CAMPOS = [
    ("Reddit (plataforma)", "coleta", lambda m: plat(m, "reddit")),
    ("Twitter (plataforma)", "coleta", lambda m: plat(m, "twitter")),
    ("YouTube (plataforma)", "coleta", lambda m: plat(m, "youtube")),
    ("Dataset pré-existente", "coleta", lambda m: m.get("uses_preexisting_dataset") is True),
    ("Uso de API", "coleta", lambda m: m.get("uses_api") is True),
    ("Scraping", "coleta", lambda m: m.get("uses_scraping") is True),
    ("Tecnologia de BD", "coleta", lambda m: bool(m.get("mentions_database_tech") or m.get("database_tech"))),
    ("Amostragem estatística", "reducao", lambda m: m.get("sampling_used") is True),
    ("Filtragem por critério", "reducao", lambda m: bool(m.get("mentions_filtering") or m.get("filtering_info"))),
]
for b, _ in ANALYSIS_BUCKETS:
    CAMPOS.append((b, "analise", (lambda bb: (lambda m: bb in buckets(m)))(b)))
CAMPOS.append(("[rótulo] análise de conteúdo", "analise",
               lambda m: any("analise de conteudo" in norm(x) or "content analysis" in norm(x)
                             for x in (m.get("analysis_types") or []) if isinstance(x, str))))

res = []
for nome, fam, fn in CAMPOS:
    pares = [(fn(a["gemini"]), fn(a["claude_haiku"])) for a in dois]
    prev = sum(1 for x, y in pares if x or y)
    if prev < 20:          # campo raro demais para um kappa estavel
        continue
    k, po = kappa(pares)
    res.append((nome, fam, k, prev, po))

res.sort(key=lambda r: -r[2])
print("\n## kappa de Cohen (n = %d artigos lidos pelos dois modelos)" % len(dois))
for nome, fam, k, prev, po in res:
    print(f"  {nome:32s} {fam:8s} k={k:.3f}  bruta={100*po:.1f}%  (prev.uniao {prev})")

fam_rng = {}
for nome, fam, k, _, _ in res:
    fam_rng.setdefault(fam, []).append(k)
print("\n## faixa por família")
for fam, ks in fam_rng.items():
    print(f"  {fam:8s} {min(ks):.2f} – {max(ks):.2f}   (mediana {sorted(ks)[len(ks)//2]:.2f})")

# --- direcao da discordancia nos tipos de analise (rodada 6) --------
# Quem marcou o rotulo sozinho. Sustenta a frase da Seção 3.4: a
# discordância se concentra em rótulos amplos e vem, sobretudo, de um
# modelo que atribui mais rótulos por artigo.
print("\n## tipos de analise: quem marcou sozinho (n = %d)" % len(dois))
for nome, fam, fn in CAMPOS:
    if fam != "analise":
        continue
    so_g = sum(1 for a in dois if fn(a["gemini"]) and not fn(a["claude_haiku"]))
    so_h = sum(1 for a in dois if fn(a["claude_haiku"]) and not fn(a["gemini"]))
    if so_g + so_h + sum(1 for a in dois if fn(a["gemini"]) and fn(a["claude_haiku"])) < 20:
        continue
    print(f"  {nome:32s} so Gemini {so_g:4d} | so Haiku {so_h:4d} | "
          f"bruta {100*(len(dois)-so_g-so_h)/len(dois):.1f}%")
print("  rotulos/artigo: Gemini %.2f | Haiku %.2f" % (
    sum(len(buckets(a["gemini"])) for a in dois) / len(dois),
    sum(len(buckets(a["claude_haiku"])) for a in dois) / len(dois)))

# --- cobertura desigual: buckets por artigo -------------------------
def nb(a):
    s = set()
    for m in ("gemini", "claude_haiku"):
        if isinstance(a.get(m), dict):
            s |= buckets(a[m])
    return len(s)


m_dois = sum(nb(a) for a in dois) / len(dois)
m_gem = sum(nb(a) for a in so_gem) / len(so_gem)
print(f"\n## cobertura desigual (base {len(arts)})")
print(f"  buckets/artigo — lidos pelos dois: {m_dois:.2f} | só Gemini: {m_gem:.2f} "
      f"(+{100*(m_dois/m_gem-1):.0f}%)")

# --- tabela de analises: uniao x so-Gemini --------------------------
uni, gemonly = Counter(), Counter()
for a in arts:
    s = set()
    for m in ("gemini", "claude_haiku"):
        if isinstance(a.get(m), dict):
            s |= buckets(a[m])
    for b in s:
        uni[b] += 1
    for b in buckets(a.get("gemini") or {}):
        gemonly[b] += 1
NB_ = len(arts)
print("\n## tipos de analise: uniao x so-Gemini (base %d)" % NB_)
for b, c in uni.most_common(12):
    print(f"  {b:26s} uniao {100*c/NB_:5.1f}%   so Gemini {100*gemonly[b]/NB_:5.1f}%   "
          f"delta {100*(gemonly[b]-c)/NB_:+5.1f}")

# --- figura kappa ---------------------------------------------------
COR = {"coleta": AZUL, "reducao": TERRA, "analise": CLARO}
ROT = {"coleta": "Coleta e plataforma", "reducao": "Redução de volume",
       "analise": "Tipo de análise"}
r2 = list(reversed(res))
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.barh(range(len(r2)), [k for _, _, k, _, _ in r2],
        color=[COR[f] for _, f, _, _, _ in r2], height=0.68,
        edgecolor="white", lw=0.5)
for i, (_, _, k, _, _) in enumerate(r2):
    ax.text(k + 0.012, i, "%.2f" % k, va="center", fontsize=7.5, color=TINTA)
ax.set_yticks(range(len(r2)))
ax.set_yticklabels([n for n, _, _, _, _ in r2], fontsize=8)
ax.set_xlim(0, 1.08)
ax.set_xlabel("κ de Cohen entre Gemini Flash e Claude Haiku")
for x, lab in ((0.40, "moderada"), (0.60, "substancial"), (0.80, "quase perfeita")):
    ax.axvline(x, color="#BBBBBB", lw=0.7, ls=(0, (3, 3)), zorder=0)
    ax.text(x, len(r2) - 0.1, lab, fontsize=6.8, color="#777777",
            ha="center", va="bottom")
handles = [plt.Rectangle((0, 0), 1, 1, color=COR[f]) for f in ("coleta", "reducao", "analise")]
ax.legend(handles, [ROT[f] for f in ("coleta", "reducao", "analise")],
          frameon=False, loc="lower right", fontsize=8, handlelength=1.2)
F.limpa(ax, "x")
F.salva(fig, "fig_kappa")
