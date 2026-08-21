"""
Eixo MP/MC — sensibilidade da divergencia MP 70,3% x 59% do paper de 2018.

A divergencia esta em aberto desde a Fase 0. Este script testa, uma a uma, as tres
alavancas plausiveis e mede o quanto cada uma move o numero:

  (A) curar o residuo `indefinido`  -> `analise/cura_indefinidos.py`
  (B) trocar a convencao de MP:
      - ESTRITA    (atual): MP = lista fechada das 26 marcas do PBM 2014;
      - CONCEITUAL: MP = grande midia profissional em geral, incluindo mainstream
        fora das 26 (Valor, A Tarde, CartaCapital, BBC, WSJ, Abril, Terra...).
  (C) ampliar a regra de coluna/blog hospedado em portal, que REBAIXA MP -> MC
      (o regex atual exige /blog no path e subconta: "Miriam Leitao" mora em
      oglobo.globo.com/economia/miriam-leitao/ — ver §6 de RESULTADOS_analise_midia_MV_MH.md).

A pergunta: alguma delas leva os 70,3% aos 59% do paper? E se nenhuma leva, a
divergencia deixa de ser "de convencao" e vira outra coisa.

Uso: PYTHONIOENCODING=utf-8 python -u analise/sensibilidade_mp_mc.py
Saidas: stdout + data/repl/compos2014/sensibilidade_mp_mc.json
"""
import csv
import json
import pathlib
import re
import sqlite3
import sys
import time
from collections import Counter
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.extrai_links import links_efetivos
from core.midia_mp_mc import MAINSTREAM_REBAIXADA_PARA_MC, _norm_host
from core.resolve_mp_mc import classe_mp_mc_do_primeiro_link, carrega_cache_mp_mc

D = pathlib.Path("data/repl/compos2014")
OUT_JSON = D / "sensibilidade_mp_mc.json"
CACHE = carrega_cache_mp_mc(D / "expand_cache.sqlite")

JANELA = ("2014-10-13", "2014-10-23")     # janela do paper de 2018
PAPER_MP_PCT = 59.0                        # Tabela 2 do paper: MP 59% / MC 41%

# (B) convencao CONCEITUAL: mainstream profissional fora das 26 volta a ser MP.
CONCEITUAL_EXTRA_MP = set(MAINSTREAM_REBAIXADA_PARA_MC) | {
    "gazetadopovo.com.br", "zh.com.br", "correiobraziliense.com.br", "em.com.br",
    "diariodonordeste.verdesmares.com.br", "anoticia.clicrbs.com.br",
    "infomoney.com.br", "theguardian.com", "abc.es", "dw.com", "m.apnews.com",
    "apnews.com", "nytimes.com", "elpais.com", "lemonde.fr", "reuters.com",
    "folhapolitica.org", "gazetaonline.com.br", "opopular.com.br",
}

# (C) regra de coluna ampliada: nomes de colunistas conhecidos no path,
#     alem do /blog que o regex atual ja pega.
RX_COLUNA_AMPLA = re.compile(
    r"/(blog|blogs|colunas?|colunistas?|opiniao|opinion)/"
    r"|/(miriam-leitao|reinaldo|reinaldoazevedo|merval|ancelmo|noblat|"
    r"fausto-macedo|monica-bergamo|elio-gaspari|dora-kramer|vera-magalhaes|"
    r"cora-ronai|helio-schwartsman|clovis-rossi|janio-de-freitas)")


def log(m):
    print(m, flush=True)


def carrega_curadoria():
    d = {}
    p = D / "indefinidos_curados.csv"
    if p.exists():
        for r in csv.DictReader(open(p, encoding="utf-8")):
            d[r["host"]] = r["classe"]
    return d


def main():
    t0 = time.time()
    curado = carrega_curadoria()
    log(f"== Curadoria carregada: {len(curado)} hosts ==")

    con = sqlite3.connect(D / "snapshot_hashtag.sqlite")
    con.row_factory = sqlite3.Row
    linhas = con.execute(
        "SELECT links, texto, data_brt FROM tweets "
        "WHERE substr(data_brt,1,10) BETWEEN ? AND ?", JANELA).fetchall()
    con.close()
    log(f"   janela {JANELA[0]}..{JANELA[1]}: {len(linhas):,} tweets")

    # pre-calcula classe base + host + url final de cada tweet
    base = []
    for r in linhas:
        cl, host = classe_mp_mc_do_primeiro_link(
            links_efetivos(r["links"], r["texto"]), CACHE)
        # URL FINAL para poder olhar o path. O cache mapeia url -> (final_url,
        # final_host, status) — TUPLA, nao dict.
        us = links_efetivos(r["links"], r["texto"])
        url = None
        if us:
            u = us[0]
            fu, fh, st = CACHE.get(u, (None, None, None))
            url = fu if (st == "ok" and fu) else u
        base.append((cl, host, url))

    def mede(usar_curadoria, conceitual, coluna_ampla):
        c = Counter()
        for cl, host, url in base:
            k = cl
            if usar_curadoria and k == "indefinido":
                k = curado.get(host, "indefinido")
            if conceitual and k == "MC" and host in CONCEITUAL_EXTRA_MP:
                k = "MP"
            if coluna_ampla and k == "MP" and url and RX_COLUNA_AMPLA.search(url):
                k = "MC"
            c[k] += 1
        mp, mc = c["MP"], c["MC"]
        tot_midia = mp + mc
        return {"MP": mp, "MC": mc, "com_midia": tot_midia,
                "MP_pct_de_C": round(100 * mp / tot_midia, 1) if tot_midia else None,
                "indefinido": c["indefinido"], "NDA": c["NDA"],
                "nao_resolvido": c["nao_resolvido"], "nao_midia": c["nao_midia"]}

    cenarios = [
        ("base (estrita, sem curadoria)", False, False, False),
        ("A · + curadoria do indefinido", True, False, False),
        ("B · convencao CONCEITUAL", True, True, False),
        ("C · + regra de coluna ampliada", True, False, True),
        ("A+B+C (tudo junto)", True, True, True),
    ]
    log(f"\n== Sensibilidade do MP% (base = tweets com midia) ==")
    log(f"   {'cenario':<34} {'MP':>7} {'MC':>7} {'MP%':>7} {'gap p/ 59%':>11}")
    res = {}
    for nome, cur, conc, col in cenarios:
        m = mede(cur, conc, col)
        gap = m["MP_pct_de_C"] - PAPER_MP_PCT
        res[nome] = {**m, "gap_vs_paper_pp": round(gap, 1)}
        log(f"   {nome:<34} {m['MP']:>7,} {m['MC']:>7,} "
            f"{m['MP_pct_de_C']:>6.1f}% {gap:>+10.1f}")

    log(f"\n   paper de 2018 (Tabela 2): MP {PAPER_MP_PCT}% · MC {100-PAPER_MP_PCT}%")

    # -------- diagnostico: em quantos MP da para VER o path? --------
    log("\n== Diagnostico: visibilidade do path nos links MP ==")
    com_path = sem_path = 0
    for cl, host, url in base:
        if cl != "MP":
            continue
        p = urlparse(url).path if url else ""
        if url and host and _norm_host(urlparse(url).netloc) == host and len(p) > 1:
            com_path += 1
        else:
            sem_path += 1
    tot_mp = com_path + sem_path
    log(f"   MP com path inspecionavel : {com_path:>7,} ({100*com_path/tot_mp:.1f}%)")
    log(f"   MP so por host (encurtador branded nao resolvido, path invisivel): "
        f"{sem_path:>5,} ({100*sem_path/tot_mp:.1f}%)")
    log("   -> a regra (C) so pode agir sobre a primeira fatia; a segunda e um"
        " TETO de subcontagem que este corpus nao permite medir.")
    res["_diagnostico_path"] = {"mp_com_path": com_path, "mp_sem_path": sem_path,
                                "pct_sem_path": round(100 * sem_path / tot_mp, 1)}

    log("\n== Leitura ==")
    b = res["base (estrita, sem curadoria)"]["MP_pct_de_C"]
    a = res["A · + curadoria do indefinido"]["MP_pct_de_C"]
    cc = res["C · + regra de coluna ampliada"]["MP_pct_de_C"]
    bb = res["B · convencao CONCEITUAL"]["MP_pct_de_C"]
    tudo = res["A+B+C (tudo junto)"]["MP_pct_de_C"]
    log(f"   (A) curar o indefinido move {a-b:+.1f} p.p. — residuo pequeno (1,5% do corpus)")
    log(f"   (B) convencao conceitual move {bb-a:+.1f} p.p. — vai na direcao ERRADA:")
    log(f"       alargar MP so aumenta MP%. A estrita ja e o MINIMO possivel de MP.")
    log(f"   (C) regra de coluna ampliada move {cc-a:+.1f} p.p. — a unica que reduz")
    log(f"   melhor cenario para fechar o gap: {min(b,a,cc,tudo):.1f}% "
        f"(ainda {min(b,a,cc,tudo)-PAPER_MP_PCT:+.1f} p.p. do paper)")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/sensibilidade_mp_mc.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "janela": list(JANELA),
        "paper_mp_pct": PAPER_MP_PCT,
        "cenarios": res,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
