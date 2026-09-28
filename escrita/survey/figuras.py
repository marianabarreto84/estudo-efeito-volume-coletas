# =====================================================================
#  Gera TODAS as figuras da survey + o dump de numeros (numeros.json).
#  Fonte unica: research.db do sistema (+ os dumps XML do DBLP, para
#  medir o que a importacao descartou).
#
#  CRITERIO UNICO (rodada 3, 14/set/2026): todo resultado sai da extracao
#  do Gemini, que cobre a base inteira. O Claude Haiku entra apenas como
#  validacao (fig_amostragem e validacao.py). Antes, plataformas,
#  estrategia, tipos de analise e persistencia usavam a UNIAO dos dois
#  modelos, e so 732 artigos tinham sido lidos pelos dois — ver
#  expansao/DIAGNOSTICO_tipos_de_analise.md §4.
#
#  Uso:  python figuras.py   ->  fig_*.pdf/.png + numeros.json
#
#  Paleta (impressao, verificada para CVD em OKLab; todos os pares
#  efetivamente adjacentes ficam com dE >= 15 em visao normal e >= 14
#  sob deuteranopia/protanopia):
#     AZUL   #4C6E91  serie principal
#     CLARO  #B8C4CE  serie de contexto / validacao
#     TERRA  #B4462F  destaque (grandes coletores)
# =====================================================================
import sqlite3, json, re, os, glob, unicodedata, statistics, math
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DB = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\research.db"
DUMPS = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\dblp_dumps"
OUT = os.path.dirname(os.path.abspath(__file__))
ACTIVE_MODELS = ("gemini", "claude_haiku")

AZUL, CLARO, TERRA = "#4C6E91", "#B8C4CE", "#B4462F"
TINTA, TINTA2 = "#222222", "#555555"
plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5, "legend.fontsize": 8.5, "figure.dpi": 160,
})


def norm(s):
    if not isinstance(s, str):
        return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s)


ANALYSIS_BUCKETS = [
    ("Detecção de comunidades", ["community detection", "deteccao de comunidade", "detecao de comunidade", "comunidade", "community"]),
    ("Centralidade", ["centrality", "centralidade", "pagerank", "betweenness", "closeness", "eigenvector"]),
    ("Sentimento", ["sentiment", "sentimento", "opinion mining", "emocao", "polaridade"]),
    ("Modelagem de tópico", ["topic model", "topico", "lda", "bertopic", "modelagem de topico"]),
    ("Classificação", ["classificacao", "classification", "supervised", "classifier"]),
    ("Clusterização", ["clusteriza", "cluster", "agrupamento"]),
    ("Análise de rede", ["analise de rede", "social network analysis", "sna", "network analysis", "analise de grafo", "graph analysis"]),
    ("Predição de links", ["link prediction", "predicao de link"]),
    ("Influência", ["influence", "influencia", "spreader", "propagacao"]),
    ("Desinformação/bots", ["misinform", "desinform", "rumor", "fake news", "fact check"]),
    ("Temporal", ["temporal", "time series", "longitudinal", "evolucao"]),
    ("Estatística descritiva", ["estatistica descritiv", "descriptive statistic", "frequenc"]),
    ("PLN (NER/embed.)", ["ner", "named entity", "embedding", "lstm", "bert", "transformer", "word2vec"]),
]


def bucketize(label):
    n = norm(label)
    if not n:
        return None
    for canon, keys in ANALYSIS_BUCKETS:
        if any(k in n for k in keys):
            return canon
    return None


VOL_BLOCK = re.compile(r"token|palavra|\bword|visualiza|\bview|impress|senten|sentence|requisi|http")


def max_collected(g):
    items = g.get("collection_items") if isinstance(g, dict) else None
    if not isinstance(items, list):
        return None
    best = None
    for it in items:
        if isinstance(it, dict):
            q, u = it.get("quantity"), (it.get("unit") or "").lower()
            if isinstance(q, (int, float)) and q > 0 and not VOL_BLOCK.search(u):
                if best is None or q > best:
                    best = q
    return best


def ano(y):
    try:
        return int(y)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- carga
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
N_CATALOGO = con.execute("select count(*) from articles").fetchone()[0]
CAT_ANO = Counter(ano(r[0]) for r in con.execute("select year from articles"))
rows = con.execute(
    "select id, year, doi, analyses from articles where analyses is not null "
    "and trim(analyses) not in ('','null','[]','{}')").fetchall()

arts, disc = [], 0
for r in rows:
    try:
        a = json.loads(r["analyses"])
    except Exception:
        continue
    if not isinstance(a.get("gemini"), dict):      # criterio unico: Gemini
        continue
    if a["gemini"].get("suggested_discard"):
        disc += 1
        continue
    a["_year"] = ano(r["year"])
    a["_arx"] = bool(r["doi"] and r["doi"].lower().startswith("10.48550"))
    arts.append(a)

N = len(arts)
N_EXTRAIDOS = N + disc


def gem(a):
    return a.get("gemini") if isinstance(a.get("gemini"), dict) else {}


def cla(a):
    return a.get("claude_haiku") if isinstance(a.get("claude_haiku"), dict) else {}


def glist(a, field):
    return [x.strip() for x in (gem(a).get(field) or []) if isinstance(x, str) and x.strip()]


def plat(a, p):
    return any(p in norm(s) for s in glist(a, "social_networks"))


def samp(a):
    return gem(a).get("sampling_used") is True


def filt(a):
    g = gem(a)
    return bool(g.get("mentions_filtering") or g.get("filtering_info"))


def api(a):
    return gem(a).get("uses_api") is True


def pct(k, n):
    return 100 * k / n if n else float("nan")


NUM = {"n_catalogo": N_CATALOGO, "n_extraidos": N_EXTRAIDOS,
       "n_descartados": disc, "N": N}

# --------------------------------------------------------- 1. plataformas
plats = ["twitter", "reddit", "youtube", "facebook", "tiktok", "instagram"]
NUM["plataformas"] = {p: sum(1 for a in arts if plat(a, p)) for p in plats}

# --------------------------------------------------------- 2. estrategia
NUM["estrategia"] = {lab: sum(1 for a in arts if gem(a).get(f) is True)
                     for f, lab in [("uses_api", "API"),
                                    ("uses_preexisting_dataset", "Dataset pre-existente"),
                                    ("uses_other_method", "Outro metodo"),
                                    ("uses_scraping", "Scraping")]}

# --------------------------------------------------------- 3. analises
bc = Counter()
for a in arts:
    for b in {bucketize(at) for at in glist(a, "analysis_types")} - {None}:
        bc[b] += 1
NUM["analises"] = dict(bc.most_common())
NUM["rotulo_analise_de_conteudo"] = sum(
    1 for a in arts if any("analise de conteudo" in norm(x) or "content analysis" in norm(x)
                           for x in glist(a, "analysis_types")))

# --------------------------------------------------- 4. amostragem/filtragem
gN = N
clN = sum(1 for a in arts if cla(a))
g_samp = sum(1 for a in arts if samp(a))
g_filt = sum(1 for a in arts if filt(a))
c_samp = sum(1 for a in arts if cla(a) and cla(a).get("sampling_used") is True)
c_filt = sum(1 for a in arts if cla(a) and (cla(a).get("mentions_filtering") or cla(a).get("filtering_info")))
NUM["amostragem_filtragem"] = {"gemini_N": gN, "gemini_amostragem": g_samp,
                               "gemini_filtragem": g_filt, "claude_N": clN,
                               "claude_amostragem": c_samp, "claude_filtragem": c_filt}
dual = [a for a in arts if cla(a)]
NUM["validacao"] = {"n": clN,
                    "ano_min": min(a["_year"] for a in dual) if dual else None,
                    "ano_max": max(a["_year"] for a in dual) if dual else None,
                    "n_ate_2022": sum(1 for a in dual if a["_year"] and a["_year"] <= 2022),
                    "pct_arxiv": pct(sum(a["_arx"] for a in dual), clN),
                    "pct_twitter": pct(sum(plat(a, "twitter") for a in dual), clN),
                    "pct_twitter_resto": pct(sum(plat(a, "twitter") for a in arts if not cla(a)),
                                             N - clN)}


# ------------------------------------------------------- 5. persistencia
def pbucket(g):
    pl = (g.get("persistence_info") or "").lower()
    if re.search(r"zenodo|figshare|osf|dryad|dataverse", pl):
        return "doi"
    if "github" in pl:
        return "github"
    if re.search(r"solicit|request|mediante", pl):
        return "request"
    if (g.get("persistence_info") or "").strip():
        return "outra"
    return "nenhuma"


pc_all = Counter(pbucket(gem(a)) for a in arts)
db_all = sum(1 for a in arts if gem(a).get("database_tech") or gem(a).get("mentions_database_tech"))
NUM["persistencia_corpus"] = dict(pc_all)
NUM["db_tech_corpus"] = db_all


def pinfo(a):
    v = gem(a).get("persistence_info")
    return v.lower() if isinstance(v, str) else ""


# contagens NAO exclusivas (um artigo pode citar GitHub e Zenodo)
NUM["persistencia_gemini"] = {
    "github": sum(1 for a in arts if "github" in pinfo(a)),
    "request": sum(1 for a in arts if re.search(r"solicit|request|mediante", pinfo(a))),
    "doi": sum(1 for a in arts if re.search(r"zenodo|figshare|osf|dryad|dataverse", pinfo(a)))}

# ------------------------------------------------------------ 6. volume
volrecs = [(max_collected(gem(a)), gem(a)) for a in arts]
volrecs = [(v, g) for v, g in volrecs if v]
vols = sorted(v for v, _ in volrecs)
NV = len(vols)
big = [(v, g) for v, g in volrecs if v >= 1e7]
NB = len(big)
pc_big = Counter(pbucket(g) for _, g in big)
NUM["volume"] = {"N": NV, "mediana": statistics.median(vols),
                 "pct_lt_10k": 100 * sum(1 for v in vols if v < 1e4) / NV,
                 "pct_ge_1M": 100 * sum(1 for v in vols if v >= 1e6) / NV,
                 "grandes": NB, "pct_grandes": 100 * NB / NV}
NUM["grandes"] = {"n": NB,
                  "amostram": sum(1 for _, g in big if g.get("sampling_used") is True),
                  "filtram": sum(1 for _, g in big if g.get("mentions_filtering") or g.get("filtering_info")),
                  "db_tech": sum(1 for _, g in big if g.get("database_tech") or g.get("mentions_database_tech")),
                  "persistencia": dict(pc_big)}
NUM["extremos"] = [
    {"q": v, "u": next((it.get("unit") for it in g.get("collection_items", [])
                        if isinstance(it, dict) and it.get("quantity") == v), "?")}
    for v, g in sorted(big, key=lambda z: -z[0])[:6]]

# ------------------------------------------------------------- 7. APIs
FAM = [("Twitter/X", r"twitter|tweepy|\bx api"), ("YouTube", r"youtube"),
       ("Reddit", r"reddit|praw|pushshift"), ("TikTok", r"tiktok"),
       ("Facebook/Instagram", r"facebook|instagram|graph api|crowdtangle")]
famc = Counter()
for a in arts:
    txt = norm(gem(a).get("api_used")) if isinstance(gem(a).get("api_used"), str) else ""
    for lab, rx in FAM:
        if re.search(rx, txt):
            famc[lab] += 1
NUM["api_familias"] = dict(famc.most_common())

# ---------------------------------------------------------- 8. temporal
anos = list(range(2010, 2027))
tot_ano, tw_ano, arx_ano, tw_na_ano = Counter(), Counter(), Counter(), Counter()
for a in arts:
    y = a["_year"]
    if y not in anos:
        continue
    tot_ano[y] += 1
    tw = plat(a, "twitter")
    tw_ano[y] += tw
    if a["_arx"]:
        arx_ano[y] += 1
    else:
        tw_na_ano[y] += tw
NUM["temporal"] = {"anos": anos, "total": [tot_ano[y] for y in anos],
                   "twitter": [tw_ano[y] for y in anos],
                   "arxiv": [arx_ano[y] for y in anos],
                   "twitter_sem_arxiv": [tw_na_ano[y] for y in anos]}

# ------------------------------------- 8b. composicao: arXiv, periodo, repeso
# O DBLP so atribui DOI a preprints do arXiv a partir de 2022, e a importacao
# exige DOI: ate 2021 o arXiv nao entra; depois, domina a base.
def resumo(L):
    n = len(L)
    return {"n": n, "amostragem": pct(sum(map(samp, L)), n), "filtragem": pct(sum(map(filt, L)), n),
            "twitter": pct(sum(plat(a, "twitter") for a in L), n), "api": pct(sum(map(api, L)), n)}


ate21 = [a for a in arts if a["_year"] and a["_year"] <= 2021]
de22 = [a for a in arts if a["_year"] and a["_year"] >= 2022]
cat21 = sum(c for y, c in CAT_ANO.items() if y and 2010 <= y <= 2021)
cat22 = sum(c for y, c in CAT_ANO.items() if y and y >= 2022)
NUM["composicao"] = {
    "arxiv": resumo([a for a in arts if a["_arx"]]),
    "nao_arxiv": resumo([a for a in arts if not a["_arx"]]),
    "ate_2021": dict(resumo(ate21), pct_base=pct(len(ate21), N), pct_catalogo=pct(cat21, cat21 + cat22)),
    "de_2022": dict(resumo(de22), pct_base=pct(len(de22), N), pct_catalogo=pct(cat22, cat21 + cat22)),
    "arxiv_ate_2021": sum(1 for a in ate21 if a["_arx"]),
    "pct_arxiv_de_2022": pct(sum(1 for a in de22 if a["_arx"]), len(de22)),
}

por_ano = defaultdict(list)
for a in arts:
    if a["_year"] in anos:
        por_ano[a["_year"]].append(a)


def repondera(fn):
    """Reescala cada ano para o seu peso no CATALOGO (pos-estratificacao)."""
    num = den = 0.0
    for y, L in por_ano.items():
        w = CAT_ANO.get(y, 0) / len(L)
        num += w * sum(1 for a in L if fn(a))
        den += w * len(L)
    return 100 * num / den


NUM["reponderado"] = {"twitter": repondera(lambda a: plat(a, "twitter")),
                      "amostragem": repondera(samp), "filtragem": repondera(filt),
                      "api": repondera(api)}
NUM["bruto"] = resumo(arts)

# ------------------------------------------- 9. o que a importacao descartou
# A importacao (import_dblp.py) so aceita registros com DOI. Relemos os
# dumps para medir o que ficou de fora e se havia outra versao com DOI.
hits, sem_doi, doi_t, tit_plat, icwsm = 0, [], set(), 0, Counter()
for f in glob.glob(os.path.join(DUMPS, "*.xml")):
    p = os.path.basename(f).split("_")[0]
    for hit in ET.parse(f).getroot().iter("hit"):
        info = hit.find("info")
        if info is None:
            continue
        hits += 1
        tit = norm(info.findtext("title") or "")
        tit_plat += p in tit
        venue = info.findtext("venue") or "?"
        t = re.sub(r"[^a-z0-9 ]", "", tit).strip()
        if "ICWSM" in venue:
            icwsm["com_doi" if info.findtext("doi") else "sem_doi"] += 1
        if info.findtext("doi"):
            doi_t.add(t)
        else:
            sem_doi.append((t, venue))
perdidos = {t: v for t, v in sem_doi if t not in doi_t}
pv = Counter(perdidos.values())
AIS = ("AMCIS", "ICIS", "PACIS", "ECIS", "ACIS")
NUM["importacao"] = {"hits_releitura": hits, "sem_doi": len(sem_doi),
                     "pct_sem_doi": pct(len(sem_doi), hits),
                     "perda_real": len(perdidos),
                     "perda_real_corr": pv["CoRR"],
                     "perda_real_sem_corr": len(perdidos) - pv["CoRR"],
                     "perda_icwsm": pv["ICWSM"], "icwsm_hits": dict(icwsm),
                     "perda_hicss": pv["HICSS"], "perda_clef": pv["CLEF"],
                     "perda_ais": sum(pv[v] for v in AIS),
                     "top_venues": pv.most_common(12),
                     "pct_plataforma_no_titulo": pct(tit_plat, hits)}

# ------------------------------ 9b. datasets pre-existentes (rodada 6)
# Familias de fonte citadas em preexisting_dataset_source (texto livre); um
# artigo conta uma vez por familia. Mais a relacao com a classificacao, que
# ajuda a explicar por que o reuso de datasets e tao frequente.
PRE = [a for a in arts if gem(a).get("uses_preexisting_dataset") is True]
DSFAM = [("Pushshift", r"pushshift"), ("SemEval", r"semeval"),
         ("COVID-19", r"covid|coronav|sars-cov"), ("Kaggle", r"kaggle"),
         ("Deteccao de bots", r"cresci|twibot|botometer|gilani|bot ?repository|bot detection")]


def eh_classif(a):
    return "Classificação" in {bucketize(x) for x in glist(a, "analysis_types")}


def dsrc(a):
    v = gem(a).get("preexisting_dataset_source")
    return v.lower() if isinstance(v, str) else ""


NUM["datasets"] = {
    "n": len(PRE),
    "familias": {lab: sum(1 for a in PRE if re.search(rx, dsrc(a))) for lab, rx in DSFAM},
    "so_dataset": sum(1 for a in PRE if gem(a).get("uses_api") is not True
                      and gem(a).get("uses_scraping") is not True),
    "pct_classif_reusa": pct(sum(map(eh_classif, PRE)), len(PRE)),
    "pct_classif_nao_reusa": pct(sum(eh_classif(a) for a in arts
                                     if gem(a).get("uses_preexisting_dataset") is not True),
                                 N - len(PRE)),
}

# ------------------------- 9c. filtragem x amostragem, exclusivas (rodada 6)
# 81,1% + 18,9% somam 100,0% por coincidencia: um artigo pode filtrar e
# amostrar, ou nenhum dos dois. O texto da Sec. 4.3 cita as combinacoes; a
# Fig. 5 fica em barras (pedido da Mariana: se a soma e coincidencia, nao e pizza).
fa = Counter((filt(a), samp(a)) for a in arts)
NUM["filtra_amostra"] = {"so_filtra": fa[(True, False)], "filtra_e_amostra": fa[(True, True)],
                         "so_amostra": fa[(False, True)], "nenhum": fa[(False, False)]}

# ---------------------------------------------------------- 10. funil
PDFS = 2298 + 811   # coleta primaria + varredura aberta (os 199 da sonda
                    # Springer ficam fora: nao foram extraidos)

# Acesso (rodada 6): aberto x paywall no catalogo e nos PDFs obtidos. O rotulo
# vem do estratos.json (campo <access> dos dumps do DBLP), e nao da coluna
# pdf_inaccessible, que a varredura reescreve (ver expansao/README.md).
ESTR = json.load(open(os.path.join(OUT, "expansao", "estratos.json"), encoding="utf-8"))["acesso"]
SONDA = {it["id"] for it in json.load(open(os.path.join(OUT, "expansao", "sonda_springer.json"),
                                            encoding="utf-8"))["itens"]}


def rot_acesso(doi):
    r = ESTR.get((doi or "").lower())
    return r if r in ("open", "closed") else "outro"


cat_rows = con.execute("select id, doi, pdf_path, analyses from articles").fetchall()
com_pdf = [r for r in cat_rows if r["pdf_path"] and r["pdf_path"].strip() and r["id"] not in SONDA]
assert len(com_pdf) == PDFS, (len(com_pdf), PDFS)
NUM["funil_acesso"] = {
    "catalogo": dict(Counter(rot_acesso(r["doi"]) for r in cat_rows)),
    "pdfs": dict(Counter(rot_acesso(r["doi"]) for r in com_pdf)),
    "pdfs_sem_extracao": sum(1 for r in com_pdf
                             if not (r["analyses"] and '"gemini"' in r["analyses"])),
    # rodada 6, v5 (15/set/2026): o texto vai direto aos PDFs com extração
    # (os 2 corrompidos saem do texto), e a divisão por acesso é desses.
    "extraidos": dict(Counter(rot_acesso(r["doi"]) for r in com_pdf
                              if r["analyses"] and '"gemini"' in r["analyses"])),
}
assert sum(NUM["funil_acesso"]["extraidos"].values()) == N_EXTRAIDOS

# rodada 6, v5: "PDFs obtidos" e "Com extracao estruturada" viram uma etapa só
NUM["funil"] = [("Registros retornados pelo DBLP", 17812),
                ("Artigos unicos catalogados", N_CATALOGO),
                ("PDFs obtidos, com extracao estruturada", N_EXTRAIDOS),
                ("Coletam dados de RSD (base)", N)]


# =====================================================================
#  FIGURAS
# =====================================================================
def limpa(ax, eixo="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    getattr(ax, eixo + "axis").grid(True, color="#DDDDDD", lw=0.6)
    ax.set_axisbelow(True)


def salva(fig, nome):
    p = os.path.join(OUT, nome)
    fig.savefig(p + ".pdf", bbox_inches="tight")
    fig.savefig(p + ".png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("  ->", nome)


def milhar(v):
    return f"{v:,}".replace(",", ".")


if __name__ == "__main__":
    # --- Fig. funil ---------------------------------------------------
    vals = [v for _, v in NUM["funil"]][::-1]
    labs = ["Registros retornados\npelo DBLP", "Artigos \u00fanicos\ncatalogados",
            "PDFs obtidos, com\nextra\u00e7\u00e3o estruturada",
            "Coletam dados de RSD\n(base de an\u00e1lise)"][::-1]
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    cols = [AZUL] + [CLARO] * 3
    ax.barh(range(len(vals)), vals, color=cols, height=0.62, edgecolor="white", lw=0.8)
    for i, v in enumerate(vals):
        ax.text(v + max(vals) * 0.012, i, milhar(v), va="center", fontsize=9, color=TINTA)
    ax.set_yticks(range(len(labs)))
    ax.set_yticklabels(labs, fontsize=8.5)
    ax.set_xlim(0, max(vals) * 1.16)
    ax.set_xlabel("N\u00ba de artigos")
    limpa(ax, "x")
    salva(fig, "fig_funil")

    # --- Fig. temporal: composicao da base (acima) + fatia do Twitter (abaixo)
    # Dois paineis com o mesmo eixo x, e nao um grafico de dois eixos y: a
    # escala de artigos e a de % nao tem alinhamento natural entre si.
    T = NUM["temporal"]
    tot, tw, arx, twna = T["total"], T["twitter"], T["arxiv"], T["twitter_sem_arxiv"]
    nao = [t - x for t, x in zip(tot, arx)]
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6.4, 4.4), sharex=True,
                                  gridspec_kw={"height_ratios": [1.25, 1], "hspace": 0.12})
    ax.bar(anos, nao, color=AZUL, width=0.74, label="Peri\u00f3dicos e anais",
           edgecolor="white", lw=0.7)
    ax.bar(anos, arx, bottom=nao, color=CLARO, width=0.74,
           label="Preprints do arXiv", edgecolor="white", lw=0.7)
    ax.set_ylabel("N\u00ba de artigos")
    ax.set_ylim(0, max(tot) * 1.12)
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    limpa(ax, "y")
    sh = [100 * w / t if t >= 20 else math.nan for w, t in zip(tw, tot)]
    shna = [100 * w / n if n >= 20 else math.nan for w, n in zip(twna, nao)]
    ax2.plot(anos, sh, color=TINTA, lw=1.6, marker="o", ms=3.5,
             label="Toda a base")
    ax2.plot(anos, shna, color=TERRA, lw=1.6, ls=(0, (4, 2)), marker="o", ms=3.5,
             label="Só periódicos e anais")
    ax2.set_ylim(0, 100)
    # Rodada 6: a leitura principal e a da API, entao 2023 fica marcado.
    ax2.axvline(2023, color=TINTA2, lw=0.9, ls=(0, (2, 2)), zorder=0)
    ax2.text(2023.2, 97, "fim do acesso acadêmico\ngratuito à API (2023)",
             ha="left", va="top", fontsize=7.5, color=TINTA2, linespacing=1.25)
    ax2.set_ylabel("Fatia do Twitter/X (%)")
    ax2.legend(frameon=False, loc="lower left", fontsize=8)
    limpa(ax2, "y")
    ax2.set_xticks(anos)
    ax2.set_xticklabels([str(a) for a in anos], rotation=45, ha="right", fontsize=7.5)
    salva(fig, "fig_temporal")

    # --- Fig. plataformas (barras; um artigo pode estudar mais de uma) ----
    def pt(v, casas=1):
        return ("%.*f" % (casas, v)).replace(".", ",")

    def barras_h(itens, nome, rotulos_it=()):
        """Barras horizontais de uma serie so, rotulo '% (n)' na ponta."""
        labs = [l for l, _ in itens][::-1]
        vals = [100 * n / gN for _, n in itens][::-1]
        ns = [n for _, n in itens][::-1]
        # altura fixa: as duas figuras de barras ficam lado a lado no artigo
        fig, ax = plt.subplots(figsize=(3.3, 2.5))
        ax.barh(range(len(vals)), vals, color=AZUL, height=0.66,
                edgecolor="white", lw=0.8)
        for i, (v, n) in enumerate(zip(vals, ns)):
            rotulo = "%s%%  (%s)" % (pt(v), milhar(n))
            if v > 0.75 * max(vals):      # barra longa: rotulo dentro, em branco
                ax.text(v - 1.5, i, rotulo, va="center", ha="right",
                        fontsize=8, color="white")
            else:                         # barra curta: rotulo fora, na ponta
                ax.text(v + 1.5, i, rotulo, va="center", fontsize=8, color=TINTA)
        ax.set_yticks(range(len(labs)))
        ax.set_yticklabels(labs, fontsize=8.5)
        ax.set_xlim(0, max(vals) * 1.42)
        ax.set_xlabel("% dos artigos")
        limpa(ax, "x")
        # margens fixas, sem bbox "tight": as duas figuras precisam sair com o
        # mesmo tamanho de eixo para ficarem alinhadas lado a lado
        fig.subplots_adjust(left=0.42, right=0.97, bottom=0.19, top=0.97)
        p = os.path.join(OUT, nome)
        fig.savefig(p + ".pdf")
        fig.savefig(p + ".png", dpi=160)
        plt.close(fig)
        print("  ->", nome)

    nomes = {"twitter": "Twitter/X", "reddit": "Reddit", "youtube": "YouTube",
             "facebook": "Facebook", "tiktok": "TikTok", "instagram": "Instagram"}
    barras_h(sorted(((nomes[p], n) for p, n in NUM["plataformas"].items()),
                    key=lambda z: -z[1]), "fig_plataformas")

    # --- Fig. estrategia de coleta (barras) --------------------------------
    rot = {"API": "API", "Dataset pre-existente": "$\\it{Dataset}$ pr\u00e9-existente",
           "Scraping": "$\\it{Scraping}$", "Outro metodo": "Outro m\u00e9todo"}
    barras_h(sorted(((rot[k], n) for k, n in NUM["estrategia"].items()),
                    key=lambda z: -z[1]), "fig_estrategia")

    # --- Fig. banco de dados (pizza): onde se diz que os dados ficaram -----
    # database_tech mistura SGBD e formato de arquivo; separamos os dois.
    # Rodada 6 (v4, 15/set/2026): "big ?query", "banco relacional" e "milvus"
    # entraram; três artigos que citam banco caíam em "só arquivos".
    SGBD = re.compile(r"sql|postgres|mongo|neo4j|elastic|cassandra|redis|big ?query|"
                      r"hbase|\bhive\b|oracle|dynamo|couch|influx|mariadb|arango|"
                      r"janus|\bsolr\b|lucene|firebase|firestore|database|milvus|"
                      r"banco de dados|banco relacional|sgbd|dbms|warehouse|hadoop|hdfs|\bs3\b|"
                      r"\bspark\b|graph ?db|triple ?store|\brdf\b")
    bd = Counter()
    for a in arts:
        g = gem(a)
        t = (g.get("database_tech") or "").strip().lower()
        if not (t or g.get("mentions_database_tech")):
            bd["nenhuma"] += 1
        elif SGBD.search(t):
            bd["sgbd"] += 1
        elif t:
            bd["arquivo"] += 1
        else:
            bd["sem_detalhe"] += 1
    NUM["bd"] = dict(bd)
    print("bd =", dict(bd))
    # Rodada 6 (v4): SGBD e arquivo não se excluem. Quantos da fatia "SGBD"
    # também citam um formato de arquivo (o "file system" do HDFS não conta).
    ARQ = re.compile(r"csv|tsv|json|excel|xlsx?\b|parquet|spreadsheet|planilha|"
                     r"text file|\btxt\b|pickle|\bpkl\b|rdata|hdf5|feather|avro|"
                     r"\barquivos?\b|\bfiles?\b(?! ?system)|\.eml|\bxml\b")
    sgbd_e_arq = 0
    for a in arts:
        t = (gem(a).get("database_tech") or "").strip().lower()
        if t and SGBD.search(t) and ARQ.search(t):
            sgbd_e_arq += 1
    NUM["bd_sgbd_e_arquivo"] = sgbd_e_arq
    print("bd: SGBD que tambem cita arquivo =", sgbd_e_arq)
    # Rodada 6 (v2): quais bancos os artigos da fatia "SGBD" citam (Tab. da
    # Sec. 4.4). Um artigo pode citar mais de um; "Sem nome" = so "banco de
    # dados"/"SQL" genericos, sem produto nomeado.
    SGFAM = [("MongoDB", r"mongo"), ("MySQL/MariaDB", r"mysql|mariadb"),
             ("Elasticsearch", r"elastic"), ("Hadoop (HDFS, Hive)", r"hadoop|hdfs|\bhive\b"),
             ("SQLite", r"sqlite"), ("PostgreSQL", r"postgres"), ("Neo4j", r"neo4j")]
    OUTROS = (r"\bs3\b|dynamo|solr|lucene|sql server|mssql|oracle|big ?query|milvus|redis|cassandra|"
              r"hbase|triple ?store|\brdf\b|graph ?db|\bspark\b|influx|firebase|firestore|"
              r"couch|arango|janus|warehouse")
    sg = [(gem(a).get("database_tech") or "").strip().lower() for a in arts]
    sg = [t for t in sg if t and SGBD.search(t)]
    tipos = {lab: sum(1 for t in sg if re.search(rx, t)) for lab, rx in SGFAM}
    tipos["Outros"] = sum(1 for t in sg if re.search(OUTROS, t))
    tipos["Sem nome"] = sum(1 for t in sg if not re.search(OUTROS, t)
                            and not any(re.search(rx, t) for _, rx in SGFAM))
    NUM["sgbd_tipos"] = {"n": len(sg), "tipos": tipos}
    assert len(sg) == bd["sgbd"], (len(sg), bd["sgbd"])
    fatias = [("Banco de dados (SGBD)", bd["sgbd"], TERRA),
              ("S\u00f3 arquivos (CSV, JSON\u2026)", bd["arquivo"], AZUL),
              ("Menciona, sem dizer qual", bd["sem_detalhe"], "#7F8A94"),
              ("N\u00e3o menciona", bd["nenhuma"], CLARO)]
    fig, ax = plt.subplots(figsize=(4.6, 2.3))
    ax.pie([n for _, n, _ in fatias], colors=[c for _, _, c in fatias],
           startangle=90, counterclock=False,
           wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_aspect("equal")
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in fatias],
              ["%s \u2014 %s (%s%%)" % (l, milhar(n), pt(100 * n / gN)) for l, n, _ in fatias],
              frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8,
              handlelength=1.0, handleheight=1.0)
    salva(fig, "fig_bd")

    # --- Fig. filtragem x amostragem: so o Gemini (rodada 5) -------------
    # O Claude Haiku saiu da figura: leu so 732 artigos, todos de 2023-2026,
    # e aparece no artigo apenas como tentativa de triangulacao (sec. 3.4).
    fig, ax = plt.subplots(figsize=(6.4, 1.6))
    cats = ["Amostragem\nestat\u00edstica", "Filtragem\npor crit\u00e9rio"]
    gv = [100 * g_samp / gN, 100 * g_filt / gN]
    ypos = [0, 1]
    ax.barh(ypos, gv, height=0.56, color=AZUL, edgecolor="white", lw=0.8)
    for y, v in zip(ypos, gv):
        ax.text(v + 1.2, y, "%s%%" % pt(v), va="center", fontsize=8.5, color=TINTA)
    ax.set_yticks(ypos)
    ax.set_yticklabels(cats, fontsize=9)
    ax.set_xlim(0, 100)
    ax.set_xlabel("%% dos artigos (N=%s)" % milhar(gN))
    limpa(ax, "x")
    salva(fig, "fig_amostragem")

    # --- Fig. grandes coletores: tres pizzas sim/nao (rodada 5) ----------
    # Pedido da Mariana: no lugar da tabela dos grandes coletores, tres
    # pizzas lado a lado. "Armazenamento" e o mesmo campo da fig_persistencia
    # (database_tech ou mentions_database_tech: SGBD ou arquivo).
    G = NUM["grandes"]
    trio = [("Amostram", G["amostram"]), ("Filtram por crit\u00e9rio", G["filtram"]),
            ("Mencionam tecnologia\nde armazenamento", G["db_tech"])]
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.35))
    for ax, (tit, n) in zip(axs, trio):
        ax.pie([n, NB - n], colors=[TERRA, CLARO], startangle=90, counterclock=False,
               wedgeprops={"edgecolor": "white", "linewidth": 1.5})
        ax.set_aspect("equal")
        ax.set_title(tit, fontsize=8.5, color=TINTA, pad=4)
        ax.text(0, -1.38, "%s%%  (%d de %d)" % (pt(100 * n / NB, 0), n, NB),
                ha="center", va="top", fontsize=8.5, color=TINTA)
    fig.legend([plt.Rectangle((0, 0), 1, 1, color=TERRA),
                plt.Rectangle((0, 0), 1, 1, color=CLARO)], ["Sim", "N\u00e3o"],
               frameon=False, loc="lower center", ncol=2, fontsize=8,
               bbox_to_anchor=(0.5, -0.04), handlelength=1.0, handleheight=1.0)
    fig.subplots_adjust(bottom=0.2, top=0.86, wspace=0.35)
    salva(fig, "fig_grandes")

    # --- Fig. volume ----------------------------------------------------
    labels = [r"$<10^{3}$", "$10^{3}$\u2013$10^{4}$", "$10^{4}$\u2013$10^{5}$",
              "$10^{5}$\u2013$10^{6}$", "$10^{6}$\u2013$10^{7}$",
              "$10^{7}$\u2013$10^{8}$", r"$\geq 10^{8}$"]
    edges = [1e3, 1e4, 1e5, 1e6, 1e7, 1e8]

    def bucket(v):
        for i, e in enumerate(edges):
            if v < e:
                return i
        return len(edges)

    counts = [0] * len(labels)
    for v in vols:
        counts[bucket(v)] += 1
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.bar(range(len(labels)), counts, color=[AZUL] * (len(labels) - 2) + [TERRA] * 2,
           width=0.72, edgecolor="white", lw=0.6)
    for x, c in zip(range(len(labels)), counts):
        ax.text(x, c + max(counts) * 0.02, str(c), ha="center", va="bottom",
                fontsize=9, color=TINTA)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("N\u00ba de artigos")
    ax.set_xlabel("Volume coletado (itens, ordem de grandeza)")
    ax.set_ylim(0, max(counts) * 1.34)
    # Rodada 6: >=10^7 dividido em duas faixas; a chave sobre as duas barras
    # diz quantos coletam 10 milhoes de itens ou mais.
    x0, x1 = len(labels) - 2 - 0.36, len(labels) - 1 + 0.36
    yb = max(counts[-2:]) + max(counts) * 0.14
    ax.plot([x0, x0, x1, x1], [yb - max(counts) * 0.03, yb, yb, yb - max(counts) * 0.03],
            color=TERRA, lw=1.0)
    ax.text((x0 + x1) / 2, yb + max(counts) * 0.025,
            "%d coletam\n$\\geq$10 milhões de itens" % NB,
            ha="center", va="bottom", fontsize=8.5, color=TERRA, linespacing=1.3)
    limpa(ax, "y")
    salva(fig, "fig_volume")

    # --- Fig. persistencia: corpus x grandes coletores -----------------
    cats = ["Tecnologia de\narmazenamento", "Reposit\u00f3rio\ncom DOI", "GitHub",
            "Sob\nsolicita\u00e7\u00e3o", "Nenhuma\nindica\u00e7\u00e3o"]
    corp = [100 * db_all / gN, 100 * pc_all["doi"] / gN, 100 * pc_all["github"] / gN,
            100 * pc_all["request"] / gN, 100 * pc_all["nenhuma"] / gN]
    grd = [100 * NUM["grandes"]["db_tech"] / NB, 100 * pc_big["doi"] / NB,
           100 * pc_big["github"] / NB, 100 * pc_big["request"] / NB,
           100 * pc_big["nenhuma"] / NB]
    x = range(len(cats))
    w = 0.34
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    ax.bar([i - w / 2 - 0.012 for i in x], corp, width=w, color=AZUL,
           label="Toda a base (N=%s)" % milhar(gN), edgecolor="white", lw=0.6)
    ax.bar([i + w / 2 + 0.012 for i in x], grd, width=w, color=TERRA,
           label="Grandes coletores (n=%d)" % NB, edgecolor="white", lw=0.6)
    for i, v in zip(x, corp):
        ax.text(i - w / 2 - 0.012, v + 1.2, "%.0f" % v, ha="center", fontsize=8, color=TINTA)
    for i, v in zip(x, grd):
        ax.text(i + w / 2 + 0.012, v + 1.2, "%.0f" % v, ha="center", fontsize=8, color=TINTA)
    ax.set_xticks(list(x))
    ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylabel("% dos artigos")
    ax.set_ylim(0, max(corp + grd) * 1.24)
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    limpa(ax, "y")
    salva(fig, "fig_persistencia")

    # ------------------------------------------------------------- dump
    with open(os.path.join(OUT, "numeros.json"), "w", encoding="utf-8") as f:
        json.dump(NUM, f, ensure_ascii=False, indent=2)
    print("\nnumeros.json gravado.")
    for k in ("n_catalogo", "n_extraidos", "N", "rotulo_analise_de_conteudo",
              "plataformas", "estrategia", "analises", "amostragem_filtragem",
              "validacao", "persistencia_gemini", "persistencia_corpus",
              "db_tech_corpus", "volume", "grandes", "api_familias", "extremos",
              "composicao", "reponderado", "bruto", "importacao"):
        print(k, "=", json.dumps(NUM[k], ensure_ascii=False))
    T = NUM["temporal"]
    print("temporal (ano total tw arxiv tw_sem_arxiv):")
    for row in zip(T["anos"], T["total"], T["twitter"], T["arxiv"], T["twitter_sem_arxiv"]):
        print("  ", row)
