"""
Fase 3 / eixo A — AV4 por limiar: a concentracao e estrutural ou artefato do corte?

A afirmacao do alvo (Tabela 3/4): os 10 autores mais retuitados concentram 15,7%
de todos os RTs — numero computado DENTRO da amostra viral (>500 RT).

O teste: baixar o limiar e ver se a concentracao se mantem. Duas medidas:
  - top-k share (top-10, top-100): depende do tamanho do universo, entao CAI por
    construcao ao alargar. Serve para comparar com o ponto publicado.
  - Gini + curva de Lorenz: medida de DESIGUALDADE, invariante ao tamanho. E ela
    que responde se a concentracao e estrutural.

Nota de dado
------------
`rt_arestas.tweet_referenciado_id` esta 100% nulo na re-coleta, entao nao da para
ligar cada evento de RT ao tweet que o originou. Usa-se a coluna `retweets` dos
originais (contagem da API por tweet), agregada por autor — que e exatamente o que
a aba `Authors` do suplemento reporta (`SUM_Retweets_Per_Author`). Confere-se o
ponto >500 RT contra o valor publicado.

Saidas: stdout + data/repl/vacinas2022/av4_lorenz.json
Uso: PYTHONIOENCODING=utf-8 python -u analise/av4_lorenz_por_limiar.py
"""
import collections
import json
import pathlib
import sqlite3
import time

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
OUT_JSON = RAIZ / "data/repl/vacinas2022/av4_lorenz.json"

LIMIARES = (500, 250, 100, 50, 25, 10, 0)
PAPER_TOP10_PCT = 15.7          # dentro da amostra viral (>500 RT)


def log(msg):
    print(msg, flush=True)


def gini(vals):
    """Gini sobre valores nao-negativos (0 = igualdade, 1 = concentracao total)."""
    v = sorted(vals)
    n = len(v)
    s = sum(v)
    if n == 0 or s == 0:
        return None
    acum = 0
    for i, x in enumerate(v, 1):
        acum += i * x
    return (2 * acum) / (n * s) - (n + 1) / n


def lorenz(vals, pontos=(10, 25, 50, 75, 90, 95, 99)):
    """% dos RTs detido pelos X% de autores no topo."""
    v = sorted(vals, reverse=True)
    s = sum(v)
    n = len(v)
    if not s:
        return {}
    out = {}
    for p in pontos:
        k = max(1, round(n * p / 100))
        out[f"top_{p}pct_autores"] = round(100 * sum(v[:k]) / s, 1)
    return out


def main():
    t0 = time.time()
    db = sqlite3.connect(SNAP)
    cur = db.cursor()

    log("== AV4 — concentracao dos RTs recebidos, por limiar ==")
    log(f"   {'limiar':>7} {'autores':>9} {'RTs':>11} {'top10':>7} {'top100':>7} "
        f"{'Gini':>6} {'top10%aut':>10}")
    linhas = []
    for lim in LIMIARES:
        por_autor = collections.Counter()
        for autor, rts in cur.execute(
                "SELECT autor, retweets FROM originais "
                "WHERE idioma='pt' AND retweets > ?", (lim,)):
            if autor and rts:
                por_autor[autor] += rts
        vals = list(por_autor.values())
        total = sum(vals)
        if not total:
            continue
        top = sorted(vals, reverse=True)
        top10 = 100 * sum(top[:10]) / total
        top100 = 100 * sum(top[:100]) / total
        g = gini(vals)
        lz = lorenz(vals)
        linhas.append({
            "limiar": lim, "n_autores": len(vals), "rts_totais": total,
            "top10_pct": round(top10, 1), "top100_pct": round(top100, 1),
            "gini": round(g, 3), "lorenz": lz,
        })
        log(f"   {(lim if lim else 'todos'):>7} {len(vals):>9,} {total:>11,} "
            f"{top10:>6.1f}% {top100:>6.1f}% {g:>6.3f} "
            f"{lz.get('top_10pct_autores', 0):>9.1f}%")

    log("== Confronto no ponto publicado (>500 RT) ==")
    p = linhas[0]
    log(f"   paper  : top-10 = {PAPER_TOP10_PCT}% dos RTs da amostra viral")
    log(f"   replica: top-10 = {p['top10_pct']}% "
        f"(n={p['n_autores']:,} autores, {p['rts_totais']:,} RTs)")

    log("== Leitura ==")
    g0, g1 = linhas[0]["gini"], linhas[-1]["gini"]
    t0_, t1_ = linhas[0]["top10_pct"], linhas[-1]["top10_pct"]
    log(f"   top-10 share: {t0_:.1f}% (>500 RT) -> {t1_:.1f}% (todos) — cai, como se"
        " espera ao alargar o universo")
    log(f"   Gini        : {g0:.3f} (>500 RT) -> {g1:.3f} (todos)")
    log("   -> se o Gini SOBE ou se mantem alto, a concentracao e estrutural e o"
        " top-10 share so refletia o tamanho do recorte")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/av4_lorenz_por_limiar.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "nota_dado": ("tweet_referenciado_id 100% nulo na re-coleta; usa-se a coluna "
                      "`retweets` dos originais agregada por autor (= "
                      "SUM_Retweets_Per_Author do suplemento)"),
        "paper_top10_pct_amostra_viral": PAPER_TOP10_PCT,
        "por_limiar": linhas,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    db.close()
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
