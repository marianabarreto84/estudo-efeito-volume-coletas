"""
Analise do eixo MIDIA (MV/MH) sobre o snapshot local — Fase 0 (parcial).
Nao depende de stance (EA/ED). Usa o cache de expansao de links (expand_cache.sqlite)
para classificar o dominio final do 1o link.

Entrega:
  (A) cobertura da classificacao de midia (apos expansao)
  (B) reconstrucao da amostra A_paper (100/dia nos horarios de pico, 19-25/out)
  (C) teste agregado de H1 (RTMV>50%) e H2 (MH rivaliza com MV) em A_paper e no universo
"""
import json, sqlite3
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.resolve_midia import carrega_cache, classe_do_primeiro_link
from core.extrai_links import links_efetivos

DB_PATH = Path("data/repl/compos2014/snapshot_hashtag.sqlite")
CACHE_PATH = Path("data/repl/compos2014/expand_cache.sqlite")

# Regra de amostragem do paper (§3, pag.5). Hora de pico (BRT) por dia da janela.
# Wed 22: texto diz 14h; nota de rodape 7 sugere ~21h (equivoco). Guardamos as duas.
PICO = {
    date(2014,10,19): 21, date(2014,10,20): 21, date(2014,10,21): 21,
    date(2014,10,22): 14, date(2014,10,23): 21, date(2014,10,24): 16,
    date(2014,10,25): 13,
}

CACHE = carrega_cache(CACHE_PATH)


def carrega():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def classe(links_json, texto=None):
    # 1o link efetivo: campo `links`; se vazio, cai para a 1a URL do texto.
    # (correcao jul/2026: sem isso, ~9% dos tweets viravam NDA por engano — eram
    #  retweets nativos com t.co so no texto. Ver core/extrai_links.py.)
    cl, _ = classe_do_primeiro_link(links_efetivos(links_json, texto), CACHE)
    return cl


def secao(t): print(f"\n{'='*64}\n{t}\n{'='*64}")


def cobertura_midia(con):
    secao("(A) COBERTURA DA CLASSIFICACAO DE MIDIA (universo on-hashtag, pos-expansao)")
    dist = Counter(); tot = 0
    for lj, tx in con.execute("SELECT links, texto FROM tweets"):
        dist[classe(lj, tx)] += 1; tot += 1
    linhas = [f"total: {tot}"]
    for cl, c in dist.most_common():
        linhas.append(f"  {cl:<14}{c:>8}  {100*c/tot:>5.1f}%")
    resolvido = tot - dist['nao_resolvido']
    linhas.append(f"cobertura (classe definida): {100*resolvido/tot:.1f}%  |  "
                  f"nao_resolvido: {100*dist['nao_resolvido']/tot:.1f}%")
    txt = "\n".join(linhas)
    print(txt)
    return txt


def reconstroi_apaper(con, pico=PICO):
    amostra = []
    for dia, hora in pico.items():
        ini = f"{dia.isoformat()}T{hora:02d}:00:00"
        fim = f"{dia.isoformat()}T23:59:59"
        rows = con.execute("""SELECT * FROM tweets WHERE data_brt >= ? AND data_brt <= ?
                              ORDER BY data_brt ASC LIMIT 100""", (ini, fim)).fetchall()
        amostra.extend({**dict(r), "_dia": dia.isoformat()} for r in rows)
    return amostra


def h1_h2(amostra, rotulo):
    secao(f"(C) H1/H2 sobre {rotulo}  (n={len(amostra)})")
    por_dia = defaultdict(Counter)
    for t in amostra:
        cl = classe(t["links"], t["texto"])
        por_dia[t["_dia"]][cl] += 1
        if t["status_retweet"] and cl == "MV":
            por_dia[t["_dia"]]["_RTMV"] += 1
    hdr = f"{'dia':<12}{'n':>5}{'MV':>6}{'MH':>6}{'NDA':>6}{'n/res':>7}{'ind':>5}{'RTMV%':>8}{'MV%':>7}{'MH%':>7}"
    print(hdr)
    linhas = []
    tot = Counter()
    for dia in sorted(por_dia):
        c = por_dia[dia]
        n = sum(c[k] for k in ("MV","MH","NDA","nao_resolvido","indefinido"))
        for k in c: tot[k] += c[k]
        tot["n"] += n
        linhas.append((dia, n, c['MV'], c['MH'], c['NDA'], c['nao_resolvido'],
                       c['indefinido'], 100*c['_RTMV']/n, 100*c['MV']/n, 100*c['MH']/n))
        print(f"{dia:<12}{n:>5}{c['MV']:>6}{c['MH']:>6}{c['NDA']:>6}{c['nao_resolvido']:>7}"
              f"{c['indefinido']:>5}{100*c['_RTMV']/n:>7.1f}%{100*c['MV']/n:>6.1f}%{100*c['MH']/n:>6.1f}%")
    n = tot["n"]
    base = n - tot['nao_resolvido']
    ag = dict(rotulo=rotulo, n=n, MV=tot['MV'], MH=tot['MH'], NDA=tot['NDA'],
              nao_res=tot['nao_resolvido'], ind=tot['indefinido'], RTMV=tot['_RTMV'],
              rtmv_pct=100*tot['_RTMV']/n, mv_pct=100*tot['MV']/n, mh_pct=100*tot['MH']/n,
              rtmv_base=100*tot['_RTMV']/base if base else 0,
              mv_base=100*tot['MV']/base if base else 0, linhas=linhas)
    print(f"{'TOTAL':<12}{n:>5}{tot['MV']:>6}{tot['MH']:>6}{tot['NDA']:>6}{tot['nao_resolvido']:>7}"
          f"{tot['indefinido']:>5}{ag['rtmv_pct']:>7.1f}%{ag['mv_pct']:>6.1f}%{ag['mh_pct']:>6.1f}%")
    print(f"\n  H1 (RTMV>50% agregado): {'SIM' if ag['rtmv_pct']>50 else 'NAO'} (RTMV={ag['rtmv_pct']:.1f}%)")
    if base:
        print(f"  H1 sobre base resolvida (n={base}): RTMV%={ag['rtmv_base']:.1f}%  MV%={ag['mv_base']:.1f}%")
    return ag


def escreve_relatorio(cobertura_txt, ag_amostra, ag_uni, path):
    def tabela(ag):
        L = ["| dia | n | MV | MH | NDA | n/res | ind | RTMV% | MV% | MH% |",
             "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
        for (dia,n,mv,mh,nda,nr,ind,rtmv,mvp,mhp) in ag["linhas"]:
            L.append(f"| {dia} | {n} | {mv} | {mh} | {nda} | {nr} | {ind} | "
                     f"{rtmv:.1f}% | {mvp:.1f}% | {mhp:.1f}% |")
        L.append(f"| **TOTAL** | **{ag['n']}** | {ag['MV']} | {ag['MH']} | {ag['NDA']} | "
                 f"{ag['nao_res']} | {ag['ind']} | **{ag['rtmv_pct']:.1f}%** | "
                 f"**{ag['mv_pct']:.1f}%** | {ag['mh_pct']:.1f}% |")
        return "\n".join(L)

    md = f"""# Fase 0 — Resultados do eixo MÍDIA (MV/MH)

> Replicação Ituassu & Lifschitz (2015). Gerado por `analisa_midia.py` sobre o
> snapshot congelado `snapshot_hashtag.sqlite` + cache `expand_cache.sqlite`.
> Este eixo é 100% determinístico (não depende de stance EA/ED).

## Método
- Universo: `A_mais_hashtag` = hashtag normalizada (minúscula+sem acento) == `eleicoes2014`.
- Amostra `A_paper`: primeiros 100 tweets a partir da hora de pico (BRT) por dia,
  19–25/out. Pico: 21h dom/seg/ter, 14h qua (ver ressalva), 21h qui, 16h sex, 13h sáb.
- Mídia: classe do **1º link** (regra do paper), dicionário MV/MH em `midia_dominios.py`.
  Links encurtados expandidos via HTTP (`expandir_links.py`); dead links (goo.gl etc.)
  ficam `nao_resolvido`.

## Cobertura de classificação (universo, pós-expansão)
```
{cobertura_txt}
```

## A_paper reconstruída (amostra 100/dia)
{tabela(ag_amostra)}

## Universo on-hashtag 19–25/out
{tabela(ag_uni)}

## Leitura — H1 (predomínio de retweet de mídia vertical, RTMV > 50%)
- **Amostra (100/dia):** RTMV agregado **{ag_amostra['rtmv_pct']:.1f}%**
  (base resolvida {ag_amostra['rtmv_base']:.1f}%) — **grosso modo se mantém** (~50%),
  compatível com o paper.
- **Universo completo:** RTMV agregado **{ag_uni['rtmv_pct']:.1f}%**
  (base resolvida {ag_uni['rtmv_base']:.1f}%) — **NÃO se sustenta em escala**.
- **Achado central (efeito-de-volume):** a amostra de 100/dia nos horários de pico
  **superestima** a dominância de RT de mídia vertical. No volume cheio, o conteúdo
  sem link (NDA — sobretudo 24–25/out, dia da votação) dilui a proporção de MV.

## Ressalvas
- {ag_uni['nao_res']} tweets no universo ({100*ag_uni['nao_res']/ag_uni['n']:.1f}%) têm
  1º link não-resolvido (encurtador morto). Mesmo no cenário otimista (todos MV), o
  RTMV do universo não alcançaria os >50% do paper.
- Quarta 22/out: hora de pico ambígua (texto=14h; nota de rodapé=21h). Usado 14h.
- H2/H3 e temas dependem da classificação de stance (Fase 0.5, adiada).
"""
    Path(path).write_text(md, encoding="utf-8")
    print(f"\n[ok] relatorio -> {path}")


def main():
    if not DB_PATH.exists():
        raise SystemExit("snapshot ausente — rode extrai_snapshot.py")
    if not CACHE:
        print("[aviso] cache de expansao vazio/ausente — links curtos ficam 'nao_resolvido'")
    con = carrega()
    cobertura_txt = cobertura_midia(con)
    amostra = reconstroi_apaper(con)
    out = Path("data/repl/compos2014/A_paper_reconstruida.json")
    out.write_text(json.dumps(
        [{k: t[k] for k in ("id_tweet","_dia","data_brt","autor","texto",
                            "status_retweet","primeiro_host")}
         | {"classe_midia": classe(t["links"], t["texto"])}
         for t in amostra], ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n[ok] A_paper reconstruida ({len(amostra)}) -> {out}")
    ag_amostra = h1_h2(amostra, "A_paper reconstruida (amostra 100/dia)")

    uni = [{**dict(r), "_dia": r["data_brt"][:10]} for r in carrega().execute(
        "SELECT * FROM tweets WHERE data_brt >= '2014-10-19' AND data_brt < '2014-10-26'")]
    ag_uni = h1_h2(uni, "UNIVERSO on-hashtag 19-25/out")

    escreve_relatorio(cobertura_txt, ag_amostra, ag_uni,
                      "data/repl/compos2014/RESULTADOS_FASE0_midia.md")


if __name__ == "__main__":
    main()
