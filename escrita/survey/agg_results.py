# =====================================================================
#  Agregações da Seção de Resultados do artigo da survey.
#  Reproduz a lógica canônica de scripts/survey_data_sources.py do
#  sistema (mesmos norm/ANALYSIS_BUCKETS/ACTIVE_MODELS, união de
#  modelos), acrescentando o FILTRO DE DESCARTE: exclui artigos que o
#  Gemini sinalizou como suggested_discard (não fizeram coleta de RSD).
#
#  Uso:
#    python agg_results.py            -> base sem descartados (artigo)
#    python agg_results.py --keep-all -> base 2.139 (valida vs números antigos)
# =====================================================================
import sqlite3, json, re, sys, unicodedata, statistics
from collections import Counter

DB = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\research.db"
ACTIVE_MODELS = ("gemini", "claude_haiku")
KEEP_ALL = "--keep-all" in sys.argv

def norm(s):
    if not isinstance(s, str): return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode("ascii")
    return re.sub(r"\s+", " ", s)

ANALYSIS_BUCKETS = [
    ("Detecção de comunidades", ["community detection","deteccao de comunidade","detecao de comunidade","comunidade","community"]),
    ("Centralidade", ["centrality","centralidade","pagerank","betweenness","closeness","eigenvector"]),
    ("Sentimento", ["sentiment","sentimento","opinion mining","emocao","polaridade"]),
    ("Modelagem de tópico", ["topic model","topico","lda","bertopic","modelagem de topico"]),
    ("Classificação", ["classificacao","classification","supervised","classifier"]),
    ("Clusterização", ["clusteriza","cluster","agrupamento"]),
    ("Análise de rede", ["analise de rede","social network analysis","sna","network analysis","analise de grafo","graph analysis"]),
    ("Predição de links", ["link prediction","predicao de link"]),
    ("Influência", ["influence","influencia","spreader","propagacao"]),
    ("Desinformação/bots", ["misinform","desinform","rumor","fake news","fact check"]),
    ("Temporal", ["temporal","time series","longitudinal","evolucao"]),
    ("Estatística descritiva", ["estatistica descritiv","descriptive statistic","frequenc"]),
    ("PLN (NER/embed.)", ["ner","named entity","embedding","lstm","bert","transformer","word2vec"]),
]
def bucketize(label):
    n = norm(label)
    if not n: return None
    for canon, keys in ANALYSIS_BUCKETS:
        if any(k in n for k in keys): return canon
    return None

VOL_BLOCK = re.compile(r"token|palavra|\bword|visualiza|\bview|impress|senten|sentence|requisi|http")
def max_collected(g):
    items = g.get("collection_items") if isinstance(g, dict) else None
    if not isinstance(items, list): return None
    best = None
    for it in items:
        if isinstance(it, dict):
            q, u = it.get("quantity"), (it.get("unit") or "").lower()
            if isinstance(q,(int,float)) and q>0 and not VOL_BLOCK.search(u):
                if best is None or q>best: best = q
    return best

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
rows = con.execute("select analyses from articles where analyses is not null "
                   "and trim(analyses) not in ('','null','[]','{}')").fetchall()

arts = []
disc = 0
for r in rows:
    try: a = json.loads(r["analyses"])
    except: continue
    if not any(isinstance(a.get(m), dict) for m in ACTIVE_MODELS): continue
    g = a.get("gemini")
    is_disc = isinstance(g, dict) and bool(g.get("suggested_discard"))
    if is_disc: disc += 1
    if is_disc and not KEEP_ALL: continue
    arts.append(a)

N = len(arts)
print(f"{'KEEP-ALL' if KEEP_ALL else 'SEM DESCARTADOS'} | N = {N}  (descartados pelo Gemini = {disc})\n")

def union_list(a, field):
    out = set()
    for m in ACTIVE_MODELS:
        v = a.get(m)
        if isinstance(v, dict):
            for x in (v.get(field) or []):
                if isinstance(x, str) and x.strip(): out.add(x.strip())
    return out
def union_bool(a, field):
    return any(isinstance(a.get(m), dict) and a[m].get(field) is True for m in ACTIVE_MODELS)
def gem(a): return a.get("gemini") if isinstance(a.get("gemini"), dict) else {}

# 1. Plataformas
plats = ["twitter","reddit","youtube","facebook","tiktok","instagram"]
print("## Plataformas")
for p in plats:
    c = sum(1 for a in arts if any(p in norm(s) for s in union_list(a,"social_networks")))
    print(f"  {p.capitalize():12s} {c:5d}  ({100*c/N:.1f}%)")

# 2. Estratégia de coleta
print("\n## Estratégia de coleta")
for field, lab in [("uses_api","API"),("uses_preexisting_dataset","Dataset pré-existente"),
                   ("uses_other_method","Outro método"),("uses_scraping","Scraping")]:
    c = sum(1 for a in arts if union_bool(a, field))
    print(f"  {lab:22s} {c:5d}  ({100*c/N:.1f}%)")

# 3. Tipos de análise
print("\n## Tipos de análise (bucketizados)")
bc = Counter()
for a in arts:
    bs = set()
    for m in ACTIVE_MODELS:
        v = a.get(m)
        if isinstance(v, dict):
            for at in (v.get("analysis_types") or []):
                b = bucketize(at) if isinstance(at,str) else None
                if b: bs.add(b)
    for b in bs: bc[b]+=1
for b,c in bc.most_common():
    print(f"  {b:26s} {c:5d}  ({100*c/N:.1f}%)")

# 4. Amostragem vs filtragem (base Gemini)
gN = sum(1 for a in arts if gem(a))
samp = sum(1 for a in arts if gem(a).get("sampling_used") is True)
filt = sum(1 for a in arts if gem(a).get("mentions_filtering") or gem(a).get("filtering_info"))
print(f"\n## Amostragem vs filtragem (base Gemini, gN={gN})")
print(f"  amostragem: {samp} ({100*samp/gN:.1f}%) | filtragem: {filt} ({100*filt/gN:.1f}%)")

# 5. Persistência (união, substring em persistence_info)
def pinfo(a):
    parts = []
    for m in ACTIVE_MODELS:
        v = a.get(m)
        if isinstance(v, dict) and isinstance(v.get("persistence_info"), str):
            parts.append(v["persistence_info"])
    return " ; ".join(parts).lower()
dbtech = sum(1 for a in arts if union_bool(a,"mentions_database_tech") or any((a.get(m,{}) or {}).get("database_tech") for m in ACTIVE_MODELS if isinstance(a.get(m),dict)))
gh = sum(1 for a in arts if "github" in pinfo(a))
req = sum(1 for a in arts if re.search(r"solicit|request|mediante", pinfo(a)))
doi = sum(1 for a in arts if re.search(r"zenodo|figshare|osf|dryad|dataverse", pinfo(a)))
print(f"\n## Persistência")
print(f"  tec. BD (mentions/tech): {dbtech} ({100*dbtech/N:.1f}%)")
print(f"  GitHub: {gh} | sob solicitação: {req} | DOI persistente (zenodo/figshare/osf): {doi} ({100*doi/N:.1f}%)")

# 4b. Amostragem/filtragem no Claude Haiku (subconjunto, validação)
cl = lambda a: a.get("claude_haiku") if isinstance(a.get("claude_haiku"),dict) else None
clN = sum(1 for a in arts if cl(a))
csamp = sum(1 for a in arts if cl(a) and cl(a).get("sampling_used") is True)
cfilt = sum(1 for a in arts if cl(a) and (cl(a).get("mentions_filtering") or cl(a).get("filtering_info")))
print(f"  [Claude Haiku, subconj. clN={clN}] amostragem {csamp} ({100*csamp/clN:.1f}%) | filtragem {cfilt} ({100*cfilt/clN:.1f}%)")

# 6. Volume (base = artigos com quantidade legível, mesma limpeza da fig)
volrecs = [(max_collected(gem(a)), gem(a)) for a in arts]
volrecs = [(v,g) for v,g in volrecs if v]
vols = sorted(v for v,_ in volrecs)
nv = len(vols)
big = [(v,g) for v,g in volrecs if v>=1e7]
print(f"\n## Volume (N com quantidade legível = {nv})")
print(f"  mediana: {statistics.median(vols):,.0f}")
print(f"  %<10k: {100*sum(1 for v in vols if v<1e4)/nv:.1f} | %>=1M: {100*sum(1 for v in vols if v>=1e6)/nv:.1f}")
print(f"  grandes coletores >=10M: {len(big)} ({100*len(big)/nv:.1f}%)")

# 6b. Comportamento dos grandes coletores (>=10M)
nb = len(big)
bsamp = sum(1 for _,g in big if g.get("sampling_used") is True)
bfilt = sum(1 for _,g in big if g.get("mentions_filtering") or g.get("filtering_info"))
bdb   = sum(1 for _,g in big if g.get("database_tech") or g.get("mentions_database_tech"))
def pbucket(g):
    pl = (g.get("persistence_info") or "").lower()
    if re.search(r"zenodo|figshare|osf|dryad|dataverse", pl): return "doi"
    if "github" in pl: return "github"
    if re.search(r"solicit|request|mediante", pl): return "request"
    if (g.get("persistence_info") or "").strip(): return "outra"
    return "nenhuma"
pc = Counter(pbucket(g) for _,g in big)
print(f"  [grandes coletores n={nb}] amostram {bsamp} ({100*bsamp/nb:.0f}%) | "
      f"filtram {bfilt} ({100*bfilt/nb:.0f}%) | tec.BD {bdb} ({100*bdb/nb:.0f}%)")
print(f"  persistência: doi={pc['doi']} github={pc['github']} request={pc['request']} "
      f"outra={pc['outra']} nenhuma={pc['nenhuma']}")
# extremos
print("  top extremos:")
for v,g in sorted(big, key=lambda z:-z[0])[:5]:
    u = next((it.get('unit') for it in g.get('collection_items',[]) if isinstance(it,dict) and it.get('quantity')==v), "?")
    print(f"     {v:,.0f} {u}")
