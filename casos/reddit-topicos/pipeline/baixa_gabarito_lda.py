#!/usr/bin/env python3
"""Baixa e congela o GABARITO PARCIAL do alvo (Portao 1, caso Melton).

O artigo nao publica o corpus, mas publica em github.com/Cheltone/NLP_Reddit sete
saidas de **pyLDAvis** — uma do conjunto combinado e uma por mes. O HTML do
pyLDAvis carrega embutido o payload do modelo: a matriz topico-termo e a fracao de
tokens por topico. Isso e o modelo AJUSTADO que gerou o artigo, e permite comparar
os nossos topicos contra os deles termo a termo (RBO), em vez de comparar prosa.

Confere sozinho: a fracao do topico 4 do modelo combinado tem de bater com a
legenda da Fig. 4 do artigo ("13.4% of tokens").

Uso: PYTHONIOENCODING=utf-8 python -u pipeline/baixa_gabarito_lda.py
Saida: data/repl/melton2021/gabarito_lda_autores.json
"""
import hashlib
import json
import pathlib
import re
import sys
import urllib.request
from collections import defaultdict

UA = "Mozilla/5.0 (academic replication; melton-2021; PUC-Rio)"
RAW = "https://raw.githubusercontent.com/Cheltone/NLP_Reddit/main/"
OUT = pathlib.Path("data/repl/melton2021/gabarito_lda_autores.json")

ARQUIVOS = {
    "combinado": "CompleteData_LDA.html",
    "2020-12": "LDA_Dec.html",
    "2021-01": "LDA_Jan.html",
    "2021-02": "LDA_Feb.html",
    "2021-03": "LDA_Mar.html",
    "2021-04": "LDA_April.html",
    "2021-05": "LDA_May.html",
}

N_TERMOS = 30   # o proprio pyLDAvis do artigo mostra "Top-30 Most Relevant Terms"


def extrai(html):
    """Le o payload do pyLDAvis e devolve {freq: [...], topicos: {id: [termos]}}."""
    m = re.search(r"var ldavis_el\w+_data = (\{.*?\});", html, re.S)
    if not m:
        raise ValueError("payload do pyLDAvis nao encontrado no HTML")
    d = json.loads(m.group(1))
    mds = d["mdsDat"]
    por_topico = defaultdict(list)
    tinfo = d["tinfo"]
    for cat, termo, logprob in zip(tinfo["Category"], tinfo["Term"], tinfo["logprob"]):
        if cat.startswith("Topic"):
            por_topico[int(cat[5:])].append((logprob, termo))
    topicos = {}
    for t, itens in por_topico.items():
        # o pyLDAvis ja grava as linhas por relevancia; ordenar por logprob desc
        # reproduz o painel com lambda=1 (frequencia dentro do topico).
        topicos[str(t)] = [w for _, w in sorted(itens, reverse=True)][:N_TERMOS]
    return {
        "n_topicos": len(mds["topics"]),
        "ordem_topicos": mds["topics"],
        "pct_tokens": [round(x, 2) for x in mds["Freq"]],
        "termos_por_topico": topicos,
    }


def main():
    res = {}
    for rot, arq in ARQUIVOS.items():
        req = urllib.request.Request(RAW + arq, headers={"User-Agent": UA})
        bruto = urllib.request.urlopen(req, timeout=120).read()
        html = bruto.decode("utf8", errors="replace")
        d = extrai(html)
        d["arquivo"] = arq
        d["sha256"] = hashlib.sha256(bruto).hexdigest()[:16]
        d["bytes"] = len(bruto)
        res[rot] = d
        print("%-12s %s  k=%d  %%tokens=%s  sha=%s"
              % (rot, arq, d["n_topicos"], d["pct_tokens"], d["sha256"]))
        sys.stdout.flush()

    # auto-conferencia contra o numero impresso na legenda da Fig. 4
    comb = res["combinado"]
    esperado = 13.4
    achado = comb["pct_tokens"][3] if len(comb["pct_tokens"]) > 3 else None
    bate = achado is not None and abs(achado - esperado) < 0.1
    print("\nconferencia Fig. 4 do artigo ('Topic 4 — 13.4%% of tokens'): "
          "achado %.2f%% -> %s" % (achado, "BATE" if bate else "NAO BATE"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "fonte": "github.com/Cheltone/NLP_Reddit (repositorio citado pelo artigo)",
        "o_que_e": "modelo LDA AJUSTADO pelos autores, lido do payload pyLDAvis. "
                   "NAO e o corpus — o corpus nao foi publicado.",
        "n_termos_por_topico": N_TERMOS,
        "confere_fig4": {"esperado_no_artigo": esperado, "achado": achado, "bate": bate},
        "modelos": res,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("escrito em %s" % OUT)


if __name__ == "__main__":
    main()
