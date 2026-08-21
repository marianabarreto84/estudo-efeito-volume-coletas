"""Efeito INTRA-AUTOR: mesmos autores no NUCLEO e no COMPLEMENTO mudam de comportamento?
NDA = tweet sem link NENHUM (opiniao pura). Desenho pareado: cada autor e seu proprio controle.

CORRECAO (jul/2026): antes NDA era "campo `links` vazio", o que contava como
"opiniao pura" ~9% de tweets que na verdade TINHAM link (t.co so no texto, tipico de
retweet nativo de 2014 — hoje em geral morto). Isso INFLAVA o NDA e, com ele, a tese
"as pessoas comentam em vez de compartilhar". Agora NDA = nenhuma URL no campo NEM no
texto. Ver core/extrai_links.py e RESULTADOS_analise_midia_MV_MH.md."""
import sqlite3, json, math, sys, pathlib
from collections import defaultdict
from scipy import stats
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.extrai_links import links_efetivos

def norm(s):
    tab = str.maketrans("áàâãäçéèêëíìîïóòôõöúùûüýÿñō","aaaaaceeeeiiiiooooouuuuyyno")
    return s.lower().translate(tab)
def is_nucleo(hj):
    return any(norm(t)=="eleicoes2014" for t in (json.loads(hj) if hj else []))
def is_nda(lj, texto):
    return 0 if links_efetivos(lj, texto) else 1

con = sqlite3.connect("data/repl/compos2014/snapshot_full.sqlite")
con.row_factory = sqlite3.Row
rows = con.execute("""SELECT autor, autor_id, hashtags, links, texto FROM tweets
                      WHERE data_brt>='2014-10-19' AND data_brt<'2014-10-26'""").fetchall()
con.close()

# acumula por autor: [nda_nuc, tot_nuc, nda_comp, tot_comp]
A = defaultdict(lambda:[0,0,0,0])
for r in rows:
    key = r["autor_id"] or r["autor"]
    if not key: continue
    nda = is_nda(r["links"], r["texto"])
    if is_nucleo(r["hashtags"]):
        A[key][0]+=nda; A[key][1]+=1
    else:
        A[key][2]+=nda; A[key][3]+=1

autores = len(A)
inter = {k:v for k,v in A.items() if v[1]>0 and v[3]>0}   # presentes nos DOIS grupos
so_nuc = sum(1 for v in A.values() if v[1]>0 and v[3]==0)
so_comp= sum(1 for v in A.values() if v[1]==0 and v[3]>0)
tw_inter = sum(v[1]+v[3] for v in inter.values())
tw_tot = len(rows)

print(f"autores distintos (janela 19-25/out): {autores}")
print(f"  so no NUCLEO:      {so_nuc}")
print(f"  so no COMPLEMENTO: {so_comp}")
print(f"  INTERSECAO (nos 2): {len(inter)}  ({100*len(inter)/autores:.1f}% dos autores)")
print(f"  tweets desses autores da intersecao: {tw_inter} ({100*tw_inter/tw_tot:.1f}% da janela)")

# ---- (1) agregado pareado: NDA% dos MESMOS autores em cada grupo ----
nda_nuc = sum(v[0] for v in inter.values()); tot_nuc = sum(v[1] for v in inter.values())
nda_cmp = sum(v[2] for v in inter.values()); tot_cmp = sum(v[3] for v in inter.values())
print(f"\n[Autores da intersecao] NDA nos tweets NUCLEO    : {nda_nuc}/{tot_nuc} = {100*nda_nuc/tot_nuc:.1f}%")
print(f"[Autores da intersecao] NDA nos tweets COMPLEMENTO: {nda_cmp}/{tot_cmp} = {100*nda_cmp/tot_cmp:.1f}%")

# ---- (2) OR de Mantel-Haenszel estratificado POR AUTOR (efeito intra-autor puro) ----
# 2x2 por autor: a=comp&NDA b=comp&notNDA c=nuc&NDA d=nuc&notNDA
sumR=sumS=0.0; vnum1=vnum2=vnum3=0.0
for v in inter.values():
    a=v[2]; b=v[3]-v[2]; c=v[0]; d=v[1]-v[0]; N=a+b+c+d
    if N==0: continue
    R=a*d/N; S=b*c/N; P=(a+d)/N; Q=(b+c)/N
    sumR+=R; sumS+=S
    vnum1+=P*R; vnum2+=(P*S+Q*R); vnum3+=Q*S
if sumR>0 and sumS>0:
    or_mh=sumR/sumS
    var=vnum1/(2*sumR**2) + vnum2/(2*sumR*sumS) + vnum3/(2*sumS**2)  # Robins-Breslow-Greenland
    se=math.sqrt(var)
    lo=math.exp(math.log(or_mh)-1.96*se); hi=math.exp(math.log(or_mh)+1.96*se)
    print(f"\nOR Mantel-Haenszel (NDA: COMPLEMENTO vs NUCLEO), estratificado POR AUTOR:")
    print(f"  OR = {or_mh:.2f}  [IC95 {lo:.2f}–{hi:.2f}]  (cada autor e seu proprio controle)")

# ---- (3) teste pareado de Wilcoxon nas taxas por autor (autores com >=3 tweets em cada) ----
K=3
pares=[(v[0]/v[1], v[2]/v[3]) for v in inter.values() if v[1]>=K and v[3]>=K]
dif=[c-n for n,c in pares]   # comp - nuc (positivo = mais NDA no complemento)
maior=sum(1 for d in dif if d>0); menor=sum(1 for d in dif if d<0); igual=sum(1 for d in dif if d==0)
print(f"\n[Pareado por autor, >= {K} tweets em cada grupo]  n_autores = {len(pares)}")
print(f"  NDA% MAIOR no COMPLEMENTO: {maior}   MAIOR no NUCLEO: {menor}   empate: {igual}")
if pares:
    med_n=sorted(n for n,_ in pares)[len(pares)//2]; med_c=sorted(c for _,c in pares)[len(pares)//2]
    print(f"  mediana NDA% por autor:  NUCLEO {100*med_n:.0f}%   COMPLEMENTO {100*med_c:.0f}%")
    nz=[d for d in dif if d!=0]
    if nz:
        try:
            w,pw = stats.wilcoxon([c for n,c in pares],[n for n,_ in pares])
            print(f"  Wilcoxon pareado (comp vs nuc): W={w:.0f}  p={pw:.2e}")
        except Exception as e:
            print("  wilcoxon:", e)
        # teste de sinais (binomial exato)
        pb = stats.binomtest(maior, maior+menor, 0.5, alternative="greater").pvalue
        print(f"  teste de sinais (H1: mais NDA no compl.): p={pb:.2e}")

# ---- (4) ilustracao: autores com mais tweets presentes nos dois grupos ----
print(f"\n[Exemplos] autores com maior volume nos dois grupos (NDA% nuc -> comp):")
top=sorted(inter.items(), key=lambda kv: kv[1][1]+kv[1][3], reverse=True)[:10]
print(f"  {'autor_id/autor':<22}{'NUC n':>7}{'NDA%':>7}   {'COMP n':>7}{'NDA%':>7}")
for k,v in top:
    print(f"  {str(k)[:22]:<22}{v[1]:>7}{100*v[0]/v[1]:>6.0f}%   {v[3]:>7}{100*v[2]/v[3]:>6.0f}%")
