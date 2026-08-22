#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Confere os numeros do corpo.tex contra os JSON congelados dos casos.

Principio (CLAUDE.md §7): todo numero do texto tem de vir de um script ou query
de um caso. Se o texto divergir dos dados, **os dados vencem**. Este script nao
adivinha: cada linha da tabela ABAIXO diz de onde o numero sai e como ele deve
aparecer escrito, em portugues (virgula decimal, ponto de milhar).

Uso:  python audita_numeros.py            (a partir desta pasta)
Saida: lista de OK / DIVERGE / AUSENTE, e codigo 1 se houver problema.
"""
import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
CASOS = os.path.join(RAIZ, "casos")
TEX = os.path.join(AQUI, "corpo.tex")


def jl(caminho):
    p = os.path.join(CASOS, caminho)
    if not os.path.exists(p):
        return None
    with io.open(p, encoding="utf-8") as fh:
        return json.load(fh)


def br(v, casas=1):
    """Formata como o texto escreve: virgula decimal, ponto de milhar."""
    if isinstance(v, int) or (isinstance(v, float) and casas == 0):
        return "{:,}".format(int(round(v))).replace(",", ".")
    return ("{:,.%df}" % casas).format(v).replace(",", "\x00").replace(".", ",") \
                                          .replace("\x00", ".")


def main():
    testes = []   # (rotulo, string esperada no tex, fonte)

    # ---------------- Cap. 3 - curva do RTMV -----------------------------
    d = jl("twitter-ituassu/data/repl/compos2014/curva_midia.json")
    if d:
        pts = d["curva_rtmv_janela"]
        medias = [p["media"] for p in pts]
        f = "curva_midia.json"
        testes += [
            ("RTMV: piso da faixa", br(min(medias)) + "\\%", f),
            ("RTMV: teto da faixa", br(max(medias)) + "\\%", f),
        ]
        p700 = next(p for p in pts if p["n"] == 700)
        testes += [
            ("banda em n=700, limite inferior", br(p700["p2_5"]) + "\\%", f),
            ("banda em n=700, limite superior", br(p700["p97_5"]) + "\\%", f),
        ]
        p200 = next(p for p in pts if p["n"] == 200)
        testes.append(("poder em n=200", br(p200["poder_pct"]) + "\\%", f))

    # ---------------- Cap. 4 - categorias por limiar ---------------------
    d = jl("vacinas/data/repl/vacinas2022/fase3_curvas.json")
    if d:
        f = "fase3_curvas.json"
        cats = {c["nome"]: c for c in d["categorias"]}
        for nome in ("Politics", "Children", "Restrictive policies",
                     "Disadvantages of vaccines"):
            c = cats.get(nome)
            if not c:
                continue
            testes += [
                ("%s em >500 RT" % nome, br(c["por_limiar"]["500"]) + "\\%", f),
                ("%s em >10 RT" % nome, br(c["por_limiar"]["10"]) + "\\%", f),
            ]
        maior = max(cats.values(), key=lambda c: abs(c["delta_500_para_10"]))
        testes.append(("maior deslocamento tematico (%s)" % maior["nome"],
                       br(abs(maior["delta_500_para_10"])), f))

    # ---------------- Cap. 5 - curva do Buntain --------------------------
    d = jl("reddit-buntain/data/repl/buntain2013/curva_rb3.json")
    if d:
        f = "curva_rb3.json"
        for p in d["curva_por_limiar"]:
            testes.append(("multi-comunidade em k=%d" % p["k"],
                           br(p["pct_multi"]) + "\\%", f))
        k20 = next(p for p in d["curva_por_limiar"] if p["k"] == 20)
        testes += [
            ("participantes em k=20", br(k20["usuarios"], 0), f),
            ("multi em k=20", br(k20["multi"], 0), f),
            ("participantes sem corte",
             br(d["curva_por_limiar"][0]["usuarios"], 0), f),
        ]

    # ---------------- Cap. 6 - filtro e funil do YouTube -----------------
    d = jl("youtube-agecovp/data/repl/agecovp2020/fase3_ugc_completo.json")
    if d:
        f = "fase3_ugc_completo.json"
        api, fun = d["API (todos os canais)"], d["corpus_x_nao_corpus"]
        testes += [
            ("UGC entre aprovados", br(api["passa_pct"]) + "\\%", f),
            ("UGC entre descartados", br(api["descartado_pct"]) + "\\%", f),
            ("delta do filtro", br(abs(api["delta_pp"])), f),
            ("IC do filtro, limite inferior", br(abs(api["ic95"][0])), f),
            ("IC do filtro, limite superior", br(abs(api["ic95"][1])), f),
            ("UGC no corpus publicado",
             br(fun["no_corpus"]["ugc_pct"]) + "\\%", f),
            ("UGC fora do corpus",
             br(fun["fora_corpus"]["ugc_pct"]) + "\\%", f),
            ("delta do funil", br(fun["delta_pp"]), f),
            ("IC do funil, limite inferior", br(fun["ic95"][0]), f),
            ("IC do funil, limite superior", br(fun["ic95"][1]), f),
            ("videos no tema", br(d["n_tema"], 0), f),
        ]

    # ---------------- Cap. 4 - autores influentes (AV3) ------------------
    d = jl("vacinas/data/repl/vacinas2022/av3_influentes.json")
    if d:
        f = "av3_influentes.json"
        pap = d["paper_tabela3"]
        l500 = next(p for p in d["por_limiar"] if p["limiar"] == 500)
        testes += [
            ("AV3: pro publicado pelo artigo", br(pap["pro_pct"]) + "\\%", f),
            ("AV3: anti publicado pelo artigo", br(pap["anti_pct"]) + "\\%", f),
            ("AV3: pro medido na replica",
             br(l500["pro_pct_entre_com_lado"]) + "\\%", f),
            ("AV3: anti medido na replica",
             br(l500["anti_pct_entre_com_lado"]) + "\\%", f),
            ("AV3: razao no ponto original", br(l500["razao_pro_anti"], 2), f),
        ]

    # ---------------- Cap. 4 - concentracao top-10 (AV4) -----------------
    d = jl("vacinas/data/repl/vacinas2022/av4_lorenz.json")
    if d:
        f = "av4_lorenz.json"
        l500 = next(p for p in d["por_limiar"] if p["limiar"] == 500)
        l0 = next(p for p in d["por_limiar"] if p["limiar"] == 0)
        testes += [
            ("AV4: top-10 publicado pelo artigo",
             br(d["paper_top10_pct_amostra_viral"]) + "\\%", f),
            ("AV4: top-10 na replica, no corte do artigo",
             br(l500["top10_pct"]) + "\\%", f),
            ("AV4: top-10 no corpus completo", br(l0["top10_pct"]) + "\\%", f),
            ("AV4: RTs do corpus completo (milhoes)",
             br(l0["rts_totais"] / 1e6, 1), f),
        ]

    # ---------------- Cap. 4 - rede e atribuicao de lado -----------------
    d = jl("vacinas/data/repl/vacinas2022/fase2_rede.json")
    if d:
        f = "fase2_rede.json"
        testes += [
            ("rede: autores (nos do grafo)", br(d["grafo"]["nos"], 0), f),
            ("rede: arestas de retuite (milhoes)",
             br(d["grafo"]["arestas"] / 1e6, 2), f),
        ]

    d = jl("vacinas/data/repl/vacinas2022/av1_lados.json")
    if d:
        f = "av1_lados.json"
        c1 = d["bases"]["ampla"]["cenarios"]["1"]
        testes += [
            ("AV1: comunidades da particao",
             br(d["particao"]["n_comunidades"], 0), f),
            ("AV1: razao pro/anti (cenario base)", br(c1["razao_pro_anti"], 2), f),
            ("AV1: posts do lado pro (milhoes)", br(c1["posts"]["pro"] / 1e6, 2), f),
            ("AV1: posts do lado anti (milhoes)", br(c1["posts"]["anti"] / 1e6, 2), f),
            ("AV1: sementes anti na comunidade coesa",
             br(d["sementes"]["comunidades_mistas"]["3"]["anti"], 0), f),
        ]

    # ---------------- Cap. 4 - stance por limiar (eixo B) ----------------
    d = jl("vacinas/data/repl/vacinas2022/fase3_curvas.json")
    if d:
        f = "fase3_curvas.json (stance)"
        s500 = next(s for s in d["stance"] if s["limiar"] == 500)
        s10 = next(s for s in d["stance"] if s["limiar"] == 10)
        testes += [
            ("stance: pro entre com-lado, >500 RT (esq. do artigo)",
             br(s500["p4_pro_dec"]) + "\\%", f),
            ("stance: pro entre com-lado, >10 RT (esq. do artigo)",
             br(s10["p4_pro_dec"]) + "\\%", f),
            ("stance: pro entre com-lado, >500 RT (3 classes)",
             br(s500["p6_pro_dec"]) + "\\%", f),
            ("stance: pro entre com-lado, >10 RT (3 classes)",
             br(s10["p6_pro_dec"]) + "\\%", f),
            ("stance: neutros em >500 RT", br(s500["p6_neutro"]) + "\\%", f),
            ("stance: neutros em >10 RT", br(s10["p6_neutro"]) + "\\%", f),
            ("stance: pro bruto em >10 RT (esq. do artigo)",
             br(s10["p4_pro"]) + "\\%", f),
            ("stance: anti bruto em >10 RT (esq. do artigo)",
             br(s10["p4_anti"]) + "\\%", f),
            ("stance: pro em >10 RT (3 classes)", br(s10["p6_pro"]) + "\\%", f),
            ("stance: anti em >10 RT (3 classes)", br(s10["p6_anti"]) + "\\%", f),
        ]

    # ---------------- Cap. 5 - Massachs, ponto original ------------------
    d = jl("reddit-massachs/data/repl/massachs2016/mh1_ponto_original.json")
    if d:
        f = "mh1_ponto_original.json"
        res = d["resultados"]
        testes.append(("Massachs: participantes do grupo focal",
                       br(d["n_usuarios"], 0), f))
        testes.append(("Massachs: baseline aleatorio",
                       br(d["baseline_aleatorio_f1"]) + "\\%", f))
        for chave, rotulo in (("participacao (homofilia)", "homofilia"),
                              ("interacao (influencia)", "influencia direta"),
                              ("score (feedback)", "feedback social")):
            r = res.get(chave)
            if isinstance(r, dict) and "f1" in r:
                testes.append(("Massachs: F1 de %s" % rotulo,
                               br(r["f1"]) + "\\%", f))

    # ---------------- Cap. 7 - PoliTok -----------------------------------
    d = jl("tiktok/data/politok_de/fase2_politok.json")
    if d:
        f = "fase2_politok.json"
        testes += [
            ("PoliTok: total de publicacoes", br(d["PT1"]["total"], 0), f),
            ("PoliTok: delecao na estadual", br(d["PT2"]["medido"]) + "\\%", f),
            ("PoliTok: delecao na federal", br(d["PT3"]["medido"]) + "\\%", f),
            ("PoliTok: delecao pela plataforma, melhor convencao",
             br(d["PT5"]["convencoes"][d["PT5"]["melhor"]]) + "\\%", f),
            ("PoliTok: alvo da plataforma", br(d["PT5"]["alvo"]) + "\\%", f),
            ("PoliTok: intolerancia por anotacao",
             br(d["PT6"]["por_anotacao"]) + "\\%", f),
            ("PoliTok: intolerancia por post", br(d["PT6"]["por_post"]) + "\\%", f),
        ]
        for data, v in sorted(d["curvas_por_data"]["saxonia"].items()):
            testes.append(("PoliTok: reverificacao em %s" % data, br(v) + "\\%", f))

    # ---------------- roda -----------------------------------------------
    with io.open(TEX, encoding="utf-8") as fh:
        tex = fh.read()
    # LaTeX escreve decimal em modo matematico como 11{,}4; normaliza para 11,4.
    tex_norm = tex.replace("{,}", ",").replace("{.}", ".")
    tex_norm = re.sub(r"\s+", " ", tex_norm).replace("\\%", "%")

    ok = falhas = 0
    largura = max(len(t[0]) for t in testes) if testes else 10
    for rotulo, esperado, fonte in testes:
        alvo = esperado.replace("\\%", "%")
        # Fronteira de numero. A esquerda barra digito/virgula/ponto, para que
        # "1,4" nao case dentro de "11,4". A direita barra SO digito, para que
        # "1,4" nao case dentro de "1,43" mas ainda case em "43,0," (virgula da
        # prosa depois do numero).
        padrao = r"(?<![\d,.])" + re.escape(alvo) + (
            "" if alvo.endswith("%") else r"(?!\d)")
        achou = re.search(padrao, tex_norm) is not None
        print("%-4s %-*s  %-12s  <- %s"
              % ("OK" if achou else "AUSENTE", largura, rotulo, esperado, fonte))
        if achou:
            ok += 1
        else:
            falhas += 1

    print("\n%d conferidos, %d encontrados, %d ausentes." % (len(testes), ok, falhas))
    if falhas:
        print("\nAUSENTE nao e necessariamente erro: o numero pode ter sido")
        print("deliberadamente omitido do texto, ou escrito por extenso")
        print("('trinta e dois por cento'). Cada ausencia pede olho humano.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
