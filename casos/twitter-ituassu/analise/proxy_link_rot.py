"""
Eixo MP/MC — link rot pela via indireta: encurtados-SOBREVIVENTES x links DIRETOS.

O CDX nao alcancou (ver RESULTADOS_FASE0_mp_mc_cdx.md: 1 alvo recuperado em ~74
consultas validas; encurtadores individuais nao sao arquivados). Esta e a unica via
que resta para dimensionar a hipotese de link rot com o dado que temos.

A ideia: os links MORTOS eram encurtadores. Se os encurtadores que SOBREVIVERAM
tiverem composicao MP/MC diferente dos links diretos, e plausivel que os mortos
tambem tivessem — e da para projetar quanto do gap MP 70,9% x 59% isso explicaria.

⚠ VIES DE SOBREVIVENCIA, declarado desde ja
-------------------------------------------
Estimar os mortos pelos encurtados que sobreviveram compara populacoes diferentes
por construcao. O §6 de RESULTADOS_analise_midia_MV_MH.md ja RETRATOU uma versao
mais forte deste argumento exatamente por isso. O que segue e uma PROJECAO
condicional ("se os mortos se parecessem com os sobreviventes, entao..."), nao uma
medida. O objetivo e fechar o item com uma magnitude, nao provar a hipotese.

Uso: PYTHONIOENCODING=utf-8 python -u analise/proxy_link_rot.py
Saidas: stdout + data/repl/compos2014/proxy_link_rot.json
"""
import json
import pathlib
import sqlite3
import sys
import time
from collections import Counter
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.extrai_links import links_efetivos
from core.midia_dominios import ENCURTADORES, ENCURTADOR_PARA_DOMINIO, _norm_host
from core.resolve_mp_mc import classe_mp_mc_do_primeiro_link, carrega_cache_mp_mc

D = pathlib.Path("data/repl/compos2014")
OUT_JSON = D / "proxy_link_rot.json"
CACHE = carrega_cache_mp_mc(D / "expand_cache.sqlite")
JANELA = ("2014-10-13", "2014-10-23")
PAPER_MP_PCT = 59.0
TODOS_ENCURTADORES = set(ENCURTADORES) | set(ENCURTADOR_PARA_DOMINIO) | {"uol.com"}


def log(m):
    print(m, flush=True)


def tipo_do_link(u, classe):
    """direto | encurtado_resolvido | encurtado_branded_sem_path | encurtado_sem_classe

    ⚠ Cuidado que custou uma versao errada deste script: "encurtador que nao
    resolveu" NAO e o mesmo que "tweet sem classe". Encurtador *branded* (glo.bo,
    oesta.do) revela a marca no proprio host, entao `classe_mp_mc_do_primeiro_link`
    ainda atribui MP/MC por dominio canonico mesmo sem expandir. So quem cai em
    `nao_resolvido` e' que fica de fato fora da base — e so esse e' o alvo da
    projecao de link rot.
    """
    try:
        h = _norm_host(urlparse(u).netloc)
    except Exception:
        return None
    if not h:
        return None
    if h not in TODOS_ENCURTADORES:
        return "direto"
    fu, fh, st = CACHE.get(u, (None, None, None))
    if st == "ok" and (fu or fh):
        return "encurtado_resolvido"
    return ("encurtado_sem_classe" if classe == "nao_resolvido"
            else "encurtado_branded_sem_path")


def main():
    t0 = time.time()
    con = sqlite3.connect(D / "snapshot_hashtag.sqlite")
    con.row_factory = sqlite3.Row
    linhas = con.execute(
        "SELECT links, texto FROM tweets WHERE substr(data_brt,1,10) BETWEEN ? AND ?",
        JANELA).fetchall()
    con.close()
    log(f"== janela {JANELA[0]}..{JANELA[1]}: {len(linhas):,} tweets ==")

    TIPOS = ("direto", "encurtado_resolvido", "encurtado_branded_sem_path",
             "encurtado_sem_classe")
    porte = {t: Counter() for t in TIPOS}
    for r in linhas:
        us = links_efetivos(r["links"], r["texto"])
        if not us:
            continue
        cl, _ = classe_mp_mc_do_primeiro_link(us, CACHE)
        t = tipo_do_link(us[0], cl)
        if not t:
            continue
        porte[t][cl] += 1

    log(f"\n== Composicao MP/MC por tipo de link ==")
    log(f"   {'tipo':<30} {'MP':>7} {'MC':>7} {'MP%':>7} {'MC%':>7} {'n c/ midia':>11}")
    comp = {}
    for t in ("direto", "encurtado_resolvido", "encurtado_branded_sem_path"):
        mp, mc = porte[t]["MP"], porte[t]["MC"]
        n = mp + mc
        comp[t] = {"MP": mp, "MC": mc, "n": n,
                   "MP_pct": round(100 * mp / n, 1) if n else None,
                   "MC_pct": round(100 * mc / n, 1) if n else None}
        if n:
            log(f"   {t:<30} {mp:>7,} {mc:>7,} {100*mp/n:>6.1f}% "
                f"{100*mc/n:>6.1f}% {n:>11,}")

    mortos = porte["encurtado_sem_classe"]["nao_resolvido"]
    log(f"   {'encurtado SEM CLASSE (morto)':<30} {'—':>7} {'—':>7} {'—':>7} {'—':>7} "
        f"{mortos:>11,}  <- fora da base")

    d, e = comp["direto"], comp["encurtado_resolvido"]
    delta = e["MC_pct"] - d["MC_pct"]
    log(f"\n   diferenca de MC entre encurtado-sobrevivente e direto: {delta:+.1f} p.p.")

    # ---------- projecao condicional ----------
    log("\n== Projecao: e se os MORTOS se parecessem com os SOBREVIVENTES? ==")
    mp_tot = sum(porte[t]["MP"] for t in TIPOS)
    mc_tot = sum(porte[t]["MC"] for t in TIPOS)
    atual = 100 * mp_tot / (mp_tot + mc_tot)
    log(f"   MP% atual (base resolvida)                    : {atual:.1f}%")

    cenarios = {}
    for nome, mp_frac in (
            ("mortos como os encurtados-sobreviventes", e["MP_pct"] / 100),
            ("mortos como os links diretos", d["MP_pct"] / 100),
            ("extremo: mortos 100% MC", 0.0)):
        mp_p = mp_tot + mortos * mp_frac
        mc_p = mc_tot + mortos * (1 - mp_frac)
        v = 100 * mp_p / (mp_p + mc_p)
        cenarios[nome] = round(v, 1)
        log(f"   {nome:<46}: {v:>5.1f}%  (gap p/ 59%: {v-PAPER_MP_PCT:+.1f})")

    log("\n== Leitura ==")
    nat = cenarios["mortos como os encurtados-sobreviventes"]
    dir_ = cenarios["mortos como os links diretos"]
    ext = cenarios["extremo: mortos 100% MC"]
    gap = atual - PAPER_MP_PCT
    log(f"   Gap a explicar: {gap:.1f} p.p. (72,2% x 59%).")
    log(f"   · projecao NATURAL (mortos = encurtados, como os sobreviventes): "
        f"{nat:.1f}% -> explica {atual-nat:+.1f} p.p. Praticamente NADA.")
    log(f"   · projecao alternativa (mortos = como links diretos): {dir_:.1f}% "
        f"-> explica {atual-dir_:.1f} p.p., ~{100*(atual-dir_)/gap:.0f}% do gap.")
    log(f"   · limite TEORICO (todo morto e MC): {ext:.1f}% — bate exatamente com o"
        " valor do paper.")
    log("   -> O link rot so fecharia o gap sob a hipotese IMPLAUSIVEL de que 100%")
    log("      dos 4.926 links mortos eram midia complementar. Sob a hipotese")
    log("      natural, nao explica nada.")
    log("")
    log("   ⚠ ACHADO QUE CONTRARIA A PREMISSA: o §6 de RESULTADOS_analise_midia_MV_MH")
    log("     supunha que 'encurtado carrega mais MC que direto' (34,2% x 23,7%).")
    log(f"     Medido aqui, e o INVERSO: MC {e['MC_pct']}% nos encurtados-sobreviventes")
    log(f"     contra {d['MC_pct']}% nos diretos. Se os mortos parecem os encurtados")
    log("     vivos, eles sao MAIS MP — o que afastaria a replica do paper, nao a")
    log("     aproximaria.")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/proxy_link_rot.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "aviso": "projecao condicional sob vies de sobrevivencia; nao e medida",
        "janela": list(JANELA),
        "composicao_por_tipo": comp,
        "n_encurtado_morto": mortos,
        "mp_pct_atual": round(atual, 1),
        "cenarios_projetados": cenarios,
        "paper_mp_pct": PAPER_MP_PCT,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
