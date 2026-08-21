"""
Eixo E2 (escopo tematico) — compara a distribuicao de midia entre:
  A_mais_hashtag (so #Eleicoes2014)  vs  A_mais_full (todas as hashtags eleitorais)
na janela 19-25/out. Isola o efeito de ALARGAR o escopo de hashtags, mantendo
janela/densidade plenas (E1+E3 fixos no maximo).

Usa o cache de expansao compartilhado. Nao depende de stance.
"""
import json, sqlite3
from collections import Counter
from pathlib import Path
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.resolve_midia import carrega_cache, classe_do_primeiro_link
from core.extrai_links import links_efetivos

DIR = Path("data/repl/compos2014")
CACHE = carrega_cache(DIR / "expand_cache.sqlite")


def dist_janela(snap_path, ini="2014-10-19", fim="2014-10-26"):
    con = sqlite3.connect(snap_path)
    d = Counter()
    for links_json, texto, rt in con.execute(
            "SELECT links, texto, status_retweet FROM tweets WHERE data_brt>=? AND data_brt<?", (ini, fim)):
        # 1o link efetivo (campo `links`; se vazio, 1a URL do texto) — correcao jul/2026
        cl, _ = classe_do_primeiro_link(links_efetivos(links_json, texto), CACHE)
        d[cl] += 1
        d["n"] += 1
        if rt and cl == "MV":
            d["_RTMV"] += 1
    con.close()
    return d


def linha(nome, d):
    n = d["n"]; base = n - d["nao_resolvido"]
    return dict(nome=nome, n=n, MV=d["MV"], MH=d["MH"], NDA=d["NDA"],
                nao_res=d["nao_resolvido"], ind=d["indefinido"],
                mv=100*d["MV"]/n, mh=100*d["MH"]/n, nda=100*d["NDA"]/n,
                rtmv=100*d["_RTMV"]/n, rtmv_base=100*d["_RTMV"]/base if base else 0)


def main():
    alvos = [("A_mais_hashtag (#Eleicoes2014)", DIR/"snapshot_hashtag.sqlite"),
             ("A_mais_full (hashtags eleitorais)", DIR/"snapshot_full.sqlite")]
    res = []
    for nome, path in alvos:
        if not path.exists():
            print(f"[aviso] snapshot ausente: {path} — pulei"); continue
        res.append(linha(nome, dist_janela(path)))

    print(f"\n{'escopo':<38}{'n':>8}{'MV%':>7}{'MH%':>7}{'NDA%':>7}{'RTMV%':>8}{'RTMVb%':>8}")
    print("-"*84)
    for r in res:
        print(f"{r['nome']:<38}{r['n']:>8}{r['mv']:>6.1f}%{r['mh']:>6.1f}%"
              f"{r['nda']:>6.1f}%{r['rtmv']:>7.1f}%{r['rtmv_base']:>7.1f}%")

    if len(res) == 2:
        h, f = res
        md = f"""# Eixo E2 (escopo temático) — mídia: hashtag única vs todas hashtags eleitorais

Janela 19–25/out. Isola o efeito de alargar o escopo de hashtags (E1+E3 fixos).

| escopo | n | MV% | MH% | NDA% | RTMV% | RTMV% (base resolvida) |
|---|--:|--:|--:|--:|--:|--:|
| {h['nome']} | {h['n']} | {h['mv']:.1f}% | {h['mh']:.1f}% | {h['nda']:.1f}% | {h['rtmv']:.1f}% | {h['rtmv_base']:.1f}% |
| {f['nome']} | {f['n']} | {f['mv']:.1f}% | {f['mh']:.1f}% | {f['nda']:.1f}% | {f['rtmv']:.1f}% | {f['rtmv_base']:.1f}% |

**Leitura:** diferença nas proporções de mídia atribuível ao *escopo de hashtags*
(E2), não ao volume (E1) nem à janela (E3), pois estes estão fixos no máximo.
ΔMV = {f['mv']-h['mv']:+.1f} p.p. · ΔMH = {f['mh']-h['mh']:+.1f} p.p. · ΔRTMV = {f['rtmv']-h['rtmv']:+.1f} p.p.
"""
        out = DIR / "RESULTADOS_E2_escopo_midia.md"
        out.write_text(md, encoding="utf-8")
        print(f"\n[ok] relatorio -> {out}")


if __name__ == "__main__":
    main()
