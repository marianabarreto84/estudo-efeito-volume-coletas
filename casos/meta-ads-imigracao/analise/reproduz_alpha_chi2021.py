"""Reproduz o alfa de Krippendorff publicado no CHI 2021 (Capozzi et al.).

Fonte dos dados: os 12 CSVs de anotadores publicados pelos autores em
github.com/PotenteOpossum/Clandestino-or-Rifugiato-Anti-immigration-Facebook-Ad-Targeting-in-Italy
baixados para ../data/repl/metaads2019/anotacoes_chi2021/.

O paper (secao 4.1) afirma:
  - remove os anuncios julgados 'irrelevant' por >=2 anotadores: 26 ads (13%);
  - alfa ORDINAL nos 5 rotulos = 0,76 com n = 174;
  - agrupando {1,2} (pro) x {4,5} (anti): n = 150 e alfa = 0,92.

Deterministico, offline, sem dependencia externa (so a biblioteca padrao).
Uso: python analise/reproduz_alpha_chi2021.py
"""

import csv
import glob
import os
from collections import Counter, defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..", "data", "repl", "metaads2019",
                    "anotacoes_chi2021")


def carrega():
    """ad_url -> lista de rotulos (strings), na ordem em que aparecem."""
    por_ad = defaultdict(list)
    for caminho in sorted(glob.glob(os.path.join(BASE, "annotator_*.csv"))):
        with open(caminho, encoding="utf-8") as fh:
            for linha in csv.DictReader(fh):
                por_ad[linha["ad_url"]].append((linha["Label"] or "").strip())
    return por_ad


def alpha(unidades, delta2):
    """Alfa de Krippendorff. `unidades` = lista de listas de valores (ja validos)."""
    o = Counter()
    for valores in unidades:
        m = len(valores)
        if m < 2:
            continue
        for i, c in enumerate(valores):
            for j, k in enumerate(valores):
                if i != j:
                    o[(c, k)] += 1.0 / (m - 1)

    n_c = defaultdict(float)
    for (c, k), v in o.items():
        n_c[c] += v
    n = sum(n_c.values())
    if n < 2:
        return float("nan")

    do = sum(v * delta2(c, k) for (c, k), v in o.items()) / n
    de = sum(n_c[c] * n_c[k] * delta2(c, k)
             for c in n_c for k in n_c) / (n * (n - 1))
    return 1.0 - do / de if de else float("nan")


def metrica_ordinal(n_c, ordem):
    """delta^2 ordinal de Krippendorff, fechado sobre as frequencias marginais."""
    idx = {v: i for i, v in enumerate(ordem)}

    def d2(c, k):
        i, j = idx[c], idx[k]
        if i > j:
            i, j = j, i
        soma = sum(n_c[ordem[g]] for g in range(i, j + 1))
        return (soma - (n_c[c] + n_c[k]) / 2.0) ** 2

    return d2


def nominal(c, k):
    return 0.0 if c == k else 1.0


def main():
    por_ad = carrega()
    print(f"anuncios: {len(por_ad)} | anotacoes: {sum(len(v) for v in por_ad.values())}")

    # 1) remove os julgados irrelevantes por >= 2 anotadores (regra do paper)
    removidos = [a for a, ls in por_ad.items() if ls.count("irrelevant") >= 2]
    mantidos = {a: ls for a, ls in por_ad.items() if a not in set(removidos)}
    pct = 100.0 * len(removidos) / len(por_ad)
    print(f"\n[1] removidos por irrelevancia (>=2): {len(removidos)} ({pct:.0f}%)"
          f"  -> paper: 26 (13%)")
    print(f"    restantes: {len(mantidos)}")

    # 2) alfa ordinal nos 5 rotulos; 'irrelevant' residual tratado como ausente
    unidades5, ord5 = [], ["1", "2", "3", "4", "5"]
    for ls in mantidos.values():
        vals = [x for x in ls if x in ord5]
        if len(vals) >= 2:
            unidades5.append(vals)
    marg = defaultdict(float)
    for vals in unidades5:
        for v in vals:
            marg[v] += 1.0
    a5 = alpha(unidades5, metrica_ordinal(marg, ord5))
    print(f"\n[2] alfa ORDINAL (5 rotulos): {a5:.3f}  em n = {len(unidades5)}"
          f"  -> paper: 0,76 em n = 174")

    # 3) duas polaridades: {1,2} = pro, {4,5} = anti; 3 e irrelevant fora
    mapa = {"1": "pro", "2": "pro", "4": "anti", "5": "anti"}
    unidades2 = []
    for ls in mantidos.values():
        vals = [mapa[x] for x in ls if x in mapa]
        if len(vals) >= 2:
            unidades2.append(vals)
    a2 = alpha(unidades2, nominal)
    print(f"\n[3] alfa (2 polaridades, {{1,2}} x {{4,5}}): {a2:.3f}  em n = {len(unidades2)}"
          f"  -> paper: 0,92 em n = 150")

    # 4) distribuicao de rotulos (contexto)
    todos = Counter(x for ls in por_ad.values() for x in ls)
    print(f"\n[4] distribuicao das 600 anotacoes: {dict(sorted(todos.items()))}")


if __name__ == "__main__":
    main()
