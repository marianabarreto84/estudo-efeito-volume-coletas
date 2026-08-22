# =====================================================================
#  Compara os achados da survey ANTES e DEPOIS da expansao do corpus.
#
#  Implementa os dois criterios pre-registrados (PRE_REGISTRO_expansao.md
#  sec. 5):
#
#    Criterio 1 - deslocamento: o valor recomputado sobre a base COMBINADA
#      cai fora do IC95% de bootstrap do valor de hoje (2.000 reamostragens
#      com reposicao da base antiga)?
#
#    Criterio 2 - vies de acesso: o valor medido SO no estrato novo difere
#      do valor de hoje? Proporcoes: teste z de duas proporcoes, alfa=0,05.
#      Mediana: bootstrap da diferenca, IC95% percentil.
#
#  As primitivas (norm, bucketize, max_collected, uniao de modelos, filtro
#  de descarte) sao copia literal de agg_results.py. Para garantir que nao
#  divergiram, o script RECOMPUTA o baseline sobre a base antiga e ABORTA se
#  nao bater com baseline_agg.txt.
#
#  Uso:
#    python compara.py                 -> relatorio no stdout
#    python compara.py --json X.json   -> grava tambem os numeros crus
# =====================================================================
import argparse
import json
import math
import os
import random
import re
import sqlite3
import statistics
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
DB = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\research.db"
BASELINE = os.path.join(AQUI, "baseline_ids.json")
ACTIVE_MODELS = ("gemini", "claude_haiku")
B = 2000  # reamostragens

# --- primitivas: copia literal de agg_results.py ----------------------


def norm(s):
    if not isinstance(s, str):
        return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s)


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


def union_list(a, field):
    out = set()
    for m in ACTIVE_MODELS:
        v = a.get(m)
        if isinstance(v, dict):
            for x in (v.get(field) or []):
                if isinstance(x, str) and x.strip():
                    out.add(x.strip())
    return out


def union_bool(a, field):
    return any(isinstance(a.get(m), dict) and a[m].get(field) is True for m in ACTIVE_MODELS)


def gem(a):
    return a.get("gemini") if isinstance(a.get("gemini"), dict) else {}


# --- os achados pre-registrados --------------------------------------
# Cada um vira um indicador 0/1 por artigo (proporcoes) ou um valor
# numerico por artigo (volume). Assim bootstrap e teste z saem iguais
# para todos, sem caso especial.

def ind_twitter(a):
    return 1 if any("twitter" in norm(s) for s in union_list(a, "social_networks")) else 0


def ind_amostragem(a):
    return 1 if gem(a).get("sampling_used") is True else 0


def ind_filtragem(a):
    return 1 if (gem(a).get("mentions_filtering") or gem(a).get("filtering_info")) else 0


def ind_api(a):
    return 1 if union_bool(a, "uses_api") else 0


def ind_doi(a):
    parts = []
    for m in ACTIVE_MODELS:
        v = a.get(m)
        if isinstance(v, dict) and isinstance(v.get("persistence_info"), str):
            parts.append(v["persistence_info"])
    return 1 if re.search(r"zenodo|figshare|osf|dryad|dataverse", " ; ".join(parts).lower()) else 0


PROPORCOES = [
    ("A3a", "amostragem", ind_amostragem, 18.7, "nao move"),
    ("A3b", "filtragem", ind_filtragem, 80.3, "nao move"),
    ("A4", "Twitter", ind_twitter, 63.7, "cai 2-6 p.p."),
    ("B1", "API", ind_api, 69.7, "(secundario)"),
    ("B3", "DOI persistente", ind_doi, 8.3, "(secundario)"),
]

# --- estatistica ------------------------------------------------------


def ic_bootstrap(valores, fn, b=B, semente=20260929):
    rnd = random.Random(semente)
    n = len(valores)
    reps = []
    for _ in range(b):
        reps.append(fn([valores[rnd.randrange(n)] for _ in range(n)]))
    reps.sort()
    return reps[int(0.025 * b)], reps[int(0.975 * b) - 1]


def z_duas_proporcoes(k1, n1, k2, n2):
    """Retorna (diferenca em p.p., z, p bicaudal). 1 = novo, 2 = antigo."""
    if n1 == 0 or n2 == 0:
        return None, None, None
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 100 * (p1 - p2), None, None
    z = (p1 - p2) / se
    pval = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return 100 * (p1 - p2), z, pval


def ic_dif_medianas(novos, antigos, b=B, semente=20260929):
    rnd = random.Random(semente)
    na, nb = len(novos), len(antigos)
    reps = []
    for _ in range(b):
        x = statistics.median([novos[rnd.randrange(na)] for _ in range(na)])
        y = statistics.median([antigos[rnd.randrange(nb)] for _ in range(nb)])
        reps.append(x - y)
    reps.sort()
    return reps[int(0.025 * b)], reps[int(0.975 * b) - 1]


# --- carga ------------------------------------------------------------


def carrega():
    base = json.load(open(BASELINE, encoding="utf-8"))
    antigos_ids = set(base["ids_com_analise"])
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "select id, analyses from articles where analyses is not null "
        "and trim(analyses) not in ('','null','[]','{}')"
    ).fetchall()
    antigos, novos, desc_a, desc_n = [], [], 0, 0
    for r in rows:
        try:
            a = json.loads(r["analyses"])
        except Exception:
            continue
        if not any(isinstance(a.get(m), dict) for m in ACTIVE_MODELS):
            continue
        eh_antigo = r["id"] in antigos_ids
        g = a.get("gemini")
        if isinstance(g, dict) and bool(g.get("suggested_discard")):
            if eh_antigo:
                desc_a += 1
            else:
                desc_n += 1
            continue
        (antigos if eh_antigo else novos).append(a)
    return antigos, novos, desc_a, desc_n


def pct(k, n):
    return 100 * k / n if n else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    ap.add_argument("--sem-guarda", action="store_true",
                    help="nao aborta se o baseline recomputado nao bater (use so pra depurar)")
    args = ap.parse_args()

    antigos, novos, desc_a, desc_n = carrega()
    na, nn = len(antigos), len(novos)
    print(f"base antiga (baseline congelado, pos-descarte) . {na}   (descartados {desc_a})")
    print(f"estrato novo (esta expansao, pos-descarte) ..... {nn}   (descartados {desc_n})")
    print(f"base combinada ................................. {na + nn}")

    # --- guarda: a base antiga tem de reproduzir baseline_agg.txt ---
    esperado = {"A3a": (321, 18.7), "A3b": (1379, 80.3), "A4": (1095, 63.7),
                "B1": (1198, 69.7), "B3": (143, 8.3)}
    if na != 1718:
        msg = f"base antiga = {na}, esperado 1718"
        if not args.sem_guarda:
            sys.exit(f"\n!! ABORTA: {msg}. O baseline congelado nao bate com o banco.")
        print(f"  (aviso: {msg})")
    for cod, lab, fn, _, _ in PROPORCOES:
        k = sum(fn(a) for a in antigos)
        ek, ep = esperado[cod]
        if k != ek:
            msg = f"{cod} ({lab}) = {k} na base antiga, baseline_agg.txt diz {ek}"
            if not args.sem_guarda:
                sys.exit(f"\n!! ABORTA: {msg}. As primitivas divergiram de agg_results.py.")
            print(f"  (aviso: {msg})")
    print("guarda OK: a base antiga reproduz baseline_agg.txt")

    if nn == 0:
        sys.exit("\nEstrato novo vazio -- nada a comparar ainda. Rode a extracao antes.")

    saida = {"n_antigos": na, "n_novos": nn, "descartados_novos": desc_n, "achados": {}}

    # --- proporcoes -------------------------------------------------
    print("\n" + "=" * 78)
    print("PROPORCOES  (crit.1 = combinada fora do IC95% da antiga; crit.2 = novo vs antigo)")
    print("=" * 78)
    cab = f"{'':4s} {'achado':18s} {'antiga':>8s} {'novo':>8s} {'comb.':>8s}  {'IC95% antiga':>16s}  {'c1':>3s} {'c2':>3s} {'p':>8s}"
    print(cab)
    print("-" * 78)
    for cod, lab, fn, ref, aposta in PROPORCOES:
        va = [fn(a) for a in antigos]
        vn = [fn(a) for a in novos]
        vc = va + vn
        pa, pn, pc_ = pct(sum(va), na), pct(sum(vn), nn), pct(sum(vc), na + nn)
        lo, hi = ic_bootstrap(va, lambda s: 100 * sum(s) / len(s))
        c1 = "SIM" if (pc_ < lo or pc_ > hi) else "nao"
        dif, z, p = z_duas_proporcoes(sum(vn), nn, sum(va), na)
        c2 = "SIM" if (p is not None and p < 0.05) else "nao"
        print(f"{cod:4s} {lab:18s} {pa:7.1f}% {pn:7.1f}% {pc_:7.1f}%  "
              f"[{lo:5.1f}; {hi:5.1f}]  {c1:>3s} {c2:>3s} {p:8.4f}" if p is not None else
              f"{cod:4s} {lab:18s} {pa:7.1f}% {pn:7.1f}% {pc_:7.1f}%  [{lo:5.1f}; {hi:5.1f}]  {c1:>3s} {c2:>3s}      n/a")
        saida["achados"][cod] = dict(rotulo=lab, antiga=pa, novo=pn, combinada=pc_,
                                     ic_antiga=[lo, hi], moveu_c1=c1 == "SIM",
                                     moveu_c2=c2 == "SIM", dif_pp=dif, p=p, aposta=aposta)

    # --- volume (A1 mediana, A2 fracao < 1 milhao) -------------------
    def vols(arts):
        return [v for v in (max_collected(gem(a)) for a in arts) if v]

    wa, wn = vols(antigos), vols(novos)
    wc = wa + wn
    print("\n" + "=" * 78)
    print(f"VOLUME  (base com quantidade legivel: antiga {len(wa)}, novo {len(wn)}, comb. {len(wc)})")
    print("=" * 78)

    if wn:
        # A1 - mediana
        ma, mn, mc = statistics.median(wa), statistics.median(wn), statistics.median(wc)
        lo, hi = ic_bootstrap(wa, statistics.median)
        c1 = "SIM" if (mc < lo or mc > hi) else "nao"
        dlo, dhi = ic_dif_medianas(wn, wa)
        c2 = "SIM" if not (dlo <= 0 <= dhi) else "nao"
        print(f"A1   mediana de itens   antiga {ma:>13,.0f}   novo {mn:>13,.0f}   comb. {mc:>13,.0f}")
        print(f"     IC95% da antiga [{lo:,.0f}; {hi:,.0f}]   -> crit.1 moveu: {c1}")
        print(f"     IC95% da diferenca (novo-antiga) [{dlo:,.0f}; {dhi:,.0f}]   -> crit.2 moveu: {c2}")
        saida["achados"]["A1"] = dict(rotulo="mediana de itens", antiga=ma, novo=mn,
                                      combinada=mc, ic_antiga=[lo, hi],
                                      ic_diferenca=[dlo, dhi], moveu_c1=c1 == "SIM",
                                      moveu_c2=c2 == "SIM", aposta="cai, talvez < 200 mil")

        # A2 - fracao abaixo de 1 milhao
        fa = [1 if v < 1e6 else 0 for v in wa]
        fn_ = [1 if v < 1e6 else 0 for v in wn]
        fc = fa + fn_
        pa, pn, pc_ = pct(sum(fa), len(fa)), pct(sum(fn_), len(fn_)), pct(sum(fc), len(fc))
        lo, hi = ic_bootstrap(fa, lambda s: 100 * sum(s) / len(s))
        c1 = "SIM" if (pc_ < lo or pc_ > hi) else "nao"
        dif, z, p = z_duas_proporcoes(sum(fn_), len(fn_), sum(fa), len(fa))
        c2 = "SIM" if (p is not None and p < 0.05) else "nao"
        print(f"\nA2   < 1 milhao         antiga {pa:.1f}%   novo {pn:.1f}%   comb. {pc_:.1f}%")
        print(f"     IC95% da antiga [{lo:.1f}; {hi:.1f}]  -> crit.1 moveu: {c1} | crit.2 moveu: {c2} (p={p:.4f})")
        saida["achados"]["A2"] = dict(rotulo="fracao < 1 milhao", antiga=pa, novo=pn,
                                      combinada=pc_, ic_antiga=[lo, hi], moveu_c1=c1 == "SIM",
                                      moveu_c2=c2 == "SIM", dif_pp=dif, p=p, aposta="sobe 2-5 p.p.")

        # B2 - grandes coletores
        ga = [1 if v >= 1e7 else 0 for v in wa]
        gn = [1 if v >= 1e7 else 0 for v in wn]
        gc = ga + gn
        print(f"\nB2   >= 10 milhoes      antiga {pct(sum(ga),len(ga)):.1f}%   "
              f"novo {pct(sum(gn),len(gn)):.1f}%   comb. {pct(sum(gc),len(gc)):.1f}%")

    print("\n" + "=" * 78)
    print("Leitura: crit.1 responde 'o numero do artigo muda?'; crit.2 responde")
    print("'o estrato inacessivel era diferente?'. Eles podem discordar quando o")
    print("estrato novo e pequeno diante da base antiga -- isso e resultado, nao erro.")
    print("=" * 78)

    if args.json:
        json.dump(saida, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nnumeros crus em {args.json}")


if __name__ == "__main__":
    main()
