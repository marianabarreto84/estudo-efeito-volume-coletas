"""Estatistica inferencial do eixo midia (MV/MH) — ICs, testes, tamanho de efeito."""
import sqlite3, json, math, sys
from collections import Counter
from datetime import date
from pathlib import Path
from scipy import stats
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.resolve_midia import carrega_cache, classe_do_primeiro_link
from core.extrai_links import links_efetivos

D = Path("data/repl/compos2014")
CACHE = carrega_cache(D/"expand_cache.sqlite")

def cls(links_json, texto=None):
    # 1o link efetivo (campo `links`; se vazio, 1a URL do texto) — correcao jul/2026
    c,_ = classe_do_primeiro_link(links_efetivos(links_json, texto), CACHE)
    return c

def norm(s):
    tab = str.maketrans("áàâãäçéèêëíìîïóòôõöúùûüýÿñō","aaaaaceeeeiiiiooooouuuuyyno")
    return s.lower().translate(tab)

def is_nucleo(hj):
    return any(norm(t)=="eleicoes2014" for t in (json.loads(hj) if hj else []))

def verif(v):
    return str(v).lower() in ("1","true","t")

# ---------- utilitarios estatisticos ----------
def wilson(k, n, z=1.96):
    if n==0: return (0,0)
    p=k/n; den=1+z*z/n
    c=(p+z*z/(2*n))/den
    m=z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return (100*(c-m), 100*(c+m))

def ci_str(k,n):
    lo,hi=wilson(k,n); return f"{100*k/n:.1f}% [IC95 {lo:.1f}–{hi:.1f}]"

def z_1prop(k,n,p0):
    p=k/n; se=math.sqrt(p0*(1-p0)/n); z=(p-p0)/se
    p_two=2*(1-stats.norm.cdf(abs(z)))
    return z, p_two

def z_2prop(k1,n1,k2,n2):
    p1,p2=k1/n1,k2/n2; pp=(k1+k2)/(n1+n2)
    se_p=math.sqrt(pp*(1-pp)*(1/n1+1/n2)); z=(p1-p2)/se_p
    p=2*(1-stats.norm.cdf(abs(z)))
    se_d=math.sqrt(p1*(1-p1)/n1+p2*(1-p2)/n2)
    d=100*(p1-p2); lo=d-196*se_d; hi=d+196*se_d
    h=2*math.asin(math.sqrt(p1))-2*math.asin(math.sqrt(p2))  # Cohen's h
    return z,p,d,lo,hi,h

def OR_2x2(a,b,c,d):  # a=exp+/evt, b=exp+/nao, c=exp-/evt, d=exp-/nao
    orr=(a*d)/(b*c)
    se=math.sqrt(1/a+1/b+1/c+1/d)
    lo=math.exp(math.log(orr)-1.96*se); hi=math.exp(math.log(orr)+1.96*se)
    return orr,lo,hi

def sec(t): print("\n"+"="*70+"\n"+t+"\n"+"="*70)

# =========================================================
# 1) MV x MH — dominancia (snapshot inteiro on-hashtag)
# =========================================================
con=sqlite3.connect(D/"snapshot_hashtag.sqlite"); con.row_factory=sqlite3.Row
allrows=con.execute("SELECT links,texto,status_retweet,data_brt FROM tweets").fetchall()
dist=Counter();
for r in allrows: dist[cls(r["links"],r["texto"])]+=1
MV,MH=dist["MV"],dist["MH"]; base=MV+MH
sec("1) MV x MH — predominio de midia vertical (universo on-hashtag, N=%d)"%len(allrows))
print(f"  MV={MV}  MH={MH}  (MV+MH={base})")
print(f"  P(MV | tem midia) = {ci_str(MV,base)}")
z,p=z_1prop(MV,base,0.5)
print(f"  H0: P(MV)=0.5  ->  z={z:.1f}, p={p:.2e}  (MV domina MH ~{MV/MH:.1f}:1)")

# =========================================================
# 2) H1 — RTMV > 50% ?  amostra (100/dia) vs universo (janela)
# =========================================================
sec("2) H1: RTMV > 50%  (retweet cujo 1o link e MV)")
# universo janela 19-25
uni=[r for r in allrows if "2014-10-19"<=r["data_brt"][:10]<="2014-10-25"]
rtmv_u=sum(1 for r in uni if r["status_retweet"] and cls(r["links"],r["texto"])=="MV")
nu=len(uni)
# amostra A_paper
PICO={date(2014,10,19):21,date(2014,10,20):21,date(2014,10,21):21,date(2014,10,22):14,
      date(2014,10,23):21,date(2014,10,24):16,date(2014,10,25):13}
amostra=[]
for dia,h in PICO.items():
    ini=f"{dia.isoformat()}T{h:02d}:00:00"; fim=f"{dia.isoformat()}T23:59:59"
    amostra+=con.execute("SELECT links,texto,status_retweet FROM tweets WHERE data_brt>=? AND data_brt<=? ORDER BY data_brt LIMIT 100",(ini,fim)).fetchall()
rtmv_a=sum(1 for r in amostra if r["status_retweet"] and cls(r["links"],r["texto"])=="MV")
na=len(amostra)
for nome,k,n in [("AMOSTRA 100/dia",rtmv_a,na),("UNIVERSO janela",rtmv_u,nu)]:
    z,ptwo=z_1prop(k,n,0.5)
    # unicaudal para ">50%": p_um = P(Z> z) se z>0
    p_um=1-stats.norm.cdf(z)
    print(f"  {nome:<16} RTMV={ci_str(k,n)}  n={n}")
    print(f"       H0:=50% -> z={z:+.1f}  p(bicaudal)={ptwo:.2e}  p(>50%, unicaudal)={p_um:.3f}")
con.close()

# =========================================================
# 3) NUCLEO x COMPLEMENTO — de onde vem a diluicao (snapshot_full, janela)
# =========================================================
con=sqlite3.connect(D/"snapshot_full.sqlite"); con.row_factory=sqlite3.Row
fw=con.execute("SELECT hashtags,links,texto,status_verificado FROM tweets WHERE data_brt>='2014-10-19' AND data_brt<'2014-10-26'").fetchall()
con.close()
nuc=[r for r in fw if is_nucleo(r["hashtags"])]
comp=[r for r in fw if not is_nucleo(r["hashtags"])]
def cd(rows):
    c=Counter()
    for r in rows: c[cls(r["links"],r["texto"])]+=1
    return c
dn,dc=cd(nuc),cd(comp)
Nn,Nc=len(nuc),len(comp)
sec("3) NUCLEO (#Eleicoes2014, n=%d) x COMPLEMENTO (so partidaria, n=%d)"%(Nn,Nc))
for lab in ("MV","NDA","MH"):
    z,p,d,lo,hi,h=z_2prop(dn[lab],Nn,dc[lab],Nc)
    print(f"  {lab}: nucleo {ci_str(dn[lab],Nn)}  x  compl {ci_str(dc[lab],Nc)}")
    print(f"       dif={d:+.1f} p.p. [IC95 {lo:+.1f}–{hi:+.1f}]  z={z:+.1f} p={p:.2e}  Cohen's h={h:.2f}")
# chi2 na distribuicao 5-classes
labs=["MV","MH","NDA","nao_resolvido","indefinido"]
tab=[[dn[l] for l in labs],[dc[l] for l in labs]]
chi2,pchi,dof,_=stats.chi2_contingency(tab)
Ntot=Nn+Nc; V=math.sqrt(chi2/(Ntot*(min(2,5)-1)))
print(f"\n  chi2 (2x5) = {chi2:.0f}  dof={dof}  p={pchi:.2e}  Cramer's V={V:.2f}")

# =========================================================
# 4) COMPOSICAO x FUNCAO — NDA estratificado por tipo de autor
# =========================================================
sec("4) Composicao (autor) x Funcao (hashtag): NDA estratificado")
def strat(rows):
    vv=[r for r in rows if verif(r["status_verificado"])]
    nv=[r for r in rows if not verif(r["status_verificado"])]
    def nda(rs): return sum(1 for r in rs if cls(r["links"],r["texto"])=="NDA"), len(rs)
    return nda(vv), nda(nv)
(nvk,nvn),(nnk,nnn)=strat(nuc)      # (NDA_verif, n_verif),(NDA_naoverif,n_naoverif) — nucleo
(cvk,cvn),(cnk,cnn)=strat(comp)     # complemento
print(f"  VERIFICADOS      : NDA nucleo {ci_str(nvk,nvn)}  x  compl {ci_str(cvk,cvn)}")
orr,lo,hi=OR_2x2(cvk, cvn-cvk, nvk, nvn-nvk)
print(f"     OR(NDA compl vs nucleo | verificado) = {orr:.1f} [IC95 {lo:.1f}–{hi:.1f}]")
print(f"  NAO-VERIFICADOS  : NDA nucleo {ci_str(nnk,nnn)}  x  compl {ci_str(cnk,cnn)}")
orr2,lo2,hi2=OR_2x2(cnk, cnn-cnk, nnk, nnn-nnk)
print(f"     OR(NDA compl vs nucleo | nao-verif)  = {orr2:.1f} [IC95 {lo2:.1f}–{hi2:.1f}]")
# Mantel-Haenszel OR comum (efeito hashtag controlando por autor)
def mh(strata):
    num=den=0
    for a,b,c,d in strata:  # a=compl NDA, b=compl notNDA, c=nucleo NDA, d=nucleo notNDA
        N=a+b+c+d
        num+=a*d/N; den+=b*c/N
    return num/den
mh_or=mh([(cvk,cvn-cvk,nvk,nvn-nvk),(cnk,cnn-cnk,nnk,nnn-nnk)])
print(f"\n  Mantel-Haenszel OR comum (hashtag, ajustado por autor) = {mh_or:.1f}")
print(f"  -> efeito da hashtag sobre NDA persiste FORTE dentro de cada estrato de autor")
print(f"     => diluicao e principalmente FUNCAO da hashtag, nao so composicao de autores")
