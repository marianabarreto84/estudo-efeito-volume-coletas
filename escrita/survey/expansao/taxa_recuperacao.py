# =====================================================================
#  Taxa de recuperacao da expansao, decomposta.
#
#  A condicao de parada pre-registrada (sec. 8) e "taxa abaixo de 11%",
#  o piso do IC da sondagem de 70 DOIs -- e aquela sondagem foi feita SO
#  no estrato pago. A fila da expansao mistura dois estratos bem
#  diferentes:
#
#    - closed -> o estrato pago. E dele que fala a sondagem, e e nele que
#      a condicao de parada se aplica.
#    - open   -> artigos que o DBLP disse serem abertos e que mesmo assim
#      falharam antes. Sao, em boa parte, falhas duras (URL ruim, DOI sem
#      deposito) e puxam a taxa global para baixo sem dizer nada sobre
#      paywall.
#
#  ---------------------------------------------------------------
#  CORRIGIDO EM 22/AGO/2026 -- duas leituras falsas que este script
#  produzia, ambas capazes de disparar a condicao de parada por engano:
#
#  1. O ESTRATO VINHA DA COLUNA pdf_inaccessible, que o retry_pdfs e o
#     reconcilia_pdfs reescrevem a cada sucesso (True -> False). Todo
#     artigo pago recuperado saia do estrato pago no instante em que era
#     recuperado, entao a taxa do estrato pago so podia dar 0,0% -- e deu,
#     com um "!! PARAR" junto. E a armadilha que o README da pasta
#     documenta: o ato de medir apaga a variavel pela qual se mede. Agora
#     o estrato vem de estratos.json, congelado do campo <access> dos
#     dumps do DBLP, que nenhuma corrida reescreve.
#
#  2. O DENOMINADOR ERA A FILA INTEIRA, mas a varredura cobriu so parte
#     dela. Dividir os recuperados pela fila toda mede COBERTURA, nao
#     taxa, e subestima a taxa por um fator igual ao avanco da fila.
#     Agora, se os logs de tentativa existirem, o denominador da taxa e o
#     conjunto TENTADO; a fila inteira aparece ao lado, como cobertura. A
#     comparacao com os 11% usa a taxa, nunca a cobertura.
#
#  Nao escreve nada: so le o banco, o baseline congelado e os logs.
# =====================================================================
import argparse
import glob
import json
import os
import re
import sqlite3
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO_SURVEY = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
DB = os.path.join(REPO_SURVEY, "research.db")
BASELINE = os.path.join(AQUI, "baseline_ids.json")
ESTRATOS = os.path.join(AQUI, "estratos.json")
LOGS_PADRAO = os.path.join(REPO_SURVEY, "pdfs", ".*.log")

EDITORAS = {
    "10.1007": "Springer", "10.1109": "IEEE", "10.1145": "ACM",
    "10.1016": "Elsevier", "10.1002": "Wiley", "10.1177": "SAGE",
    "10.1080": "Taylor & Francis", "10.1108": "Emerald",
    "10.3390": "MDPI", "10.1371": "PLOS", "10.48550": "arXiv",
    "10.1140": "EPJ/Springer", "10.1093": "Oxford UP",
    "10.1017": "Cambridge UP", "10.1186": "BMC/Springer",
}

# linha de tentativa do retry_pdfs:
#   [hh:mm:ss]   [12/11040] 10.1145/xxx: sem PDF
RE_TENTATIVA = re.compile(r"\]\s+(10\.\S+?):\s+(?:OK ->|sem PDF)")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (max(0.0, 100 * (c - r) / d), min(100.0, 100 * (c + r) / d))


def linha(rot, k, n):
    if n == 0:
        return f"  {rot:22s}      -        -"
    lo, hi = wilson(k, n)
    return f"  {rot:22s} {k:6d}/{n:<6d} {100*k/n:5.1f}%   IC95% [{lo:4.1f}; {hi:4.1f}]"


def carrega_tentados(padrao):
    """DOIs que a varredura de fato tentou, lidos dos logs do retry_pdfs.

    Sem isto o denominador seria a fila inteira, inclusive o que nunca foi
    tentado -- o que mede cobertura, e nao taxa.
    """
    dois = set()
    for caminho in glob.glob(padrao):
        with open(caminho, encoding="utf-8", errors="replace") as fh:
            for ln in fh:
                m = RE_TENTATIVA.search(ln)
                if m:
                    dois.add(m.group(1).strip().lower())
    return dois


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", default=LOGS_PADRAO,
                    help="glob dos logs de tentativa (default: %(default)s)")
    ap.add_argument("--sem-logs", action="store_true",
                    help="ignora os logs e usa a fila inteira como denominador "
                         "(so cobertura; NAO comparavel com o piso de 11%%)")
    a = ap.parse_args()

    base = json.load(open(BASELINE, encoding="utf-8"))
    tinha_pdf = set(base["ids_com_pdf_antes"])
    acesso = json.load(open(ESTRATOS, encoding="utf-8"))["acesso"]
    acesso = {k.strip().lower(): v for k, v in acesso.items()}
    tentados = set() if a.sem_logs else carrega_tentados(a.logs)

    con = sqlite3.connect(DB)
    # Fila = todo artigo com DOI que estava sem PDF quando o baseline foi
    # congelado; inclui os que ja sairam dela por terem sido recuperados.
    fila = [
        (aid, doi, pdf)
        for aid, doi, pdf in con.execute(
            "select id, doi, pdf_path from articles where doi is not null and doi <> ''"
        )
        if aid not in tinha_pdf
    ]

    tot, ok, tot_t, ok_t = Counter(), Counter(), Counter(), Counter()
    for aid, doi, pdf in fila:
        d = (doi or "").strip().lower()
        estrato = {"closed": "pago", "open": "aberto-que-falhou"}.get(
            acesso.get(d), "sem rotulo no DBLP")
        pref = d.split("/")[0]
        ed = EDITORAS.get(pref, f"outra ({pref})" if pref else "sem DOI")
        acertou = bool(pdf)
        foi_tentado = d in tentados or acertou
        for chave in (("TOTAL",), ("estrato", estrato),
                      ("estrato+editora", estrato, ed)):
            tot[chave] += 1
            ok[chave] += acertou
            if foi_tentado:
                tot_t[chave] += 1
                ok_t[chave] += acertou

    usa_tentados = bool(tentados)
    T, O = (tot_t, ok_t) if usa_tentados else (tot, ok)

    print("TAXA DE RECUPERACAO DA EXPANSAO")
    print("=" * 62)
    if usa_tentados:
        pct = 100 * tot_t[("TOTAL",)] / max(tot[("TOTAL",)], 1)
        print(f"denominador = artigos TENTADOS ({tot_t[('TOTAL',)]} dos "
              f"{tot[('TOTAL',)]} da fila, {pct:.0f}% dela)")
        print(f"fonte dos logs: {a.logs}")
    else:
        print("!! denominador = FILA INTEIRA. Isto e COBERTURA, nao taxa,")
        print("   e nao pode ser comparado com o piso de 11%.")
    print()
    print(linha("tentados", O[("TOTAL",)], T[("TOTAL",)]))

    print("\npor estrato (rotulo estavel de estratos.json, <access> do DBLP):")
    for e in ("pago", "aberto-que-falhou", "sem rotulo no DBLP"):
        print(linha(e, O[("estrato", e)], T[("estrato", e)]))

    print("\n>> A condicao de parada de 11% vale sobre o estrato PAGO,")
    print("   que e o unico comparavel a sondagem de 70 DOIs (18,6%).")
    n_pago, k_pago = T[("estrato", "pago")], O[("estrato", "pago")]
    taxa = k_pago / max(n_pago, 1)
    lo, hi = wilson(k_pago, n_pago)
    if not usa_tentados:
        print("   (sem os logs nao da pra avaliar a condicao de parada.)")
    elif hi < 11.0:
        print(f"   !! PARAR: estrato pago em {100*taxa:.1f}%, IC95% inteiro abaixo "
              f"do piso de 11% (teto em {hi:.1f}%).")
    elif taxa < 0.11:
        print(f"   ATENCAO: estrato pago em {100*taxa:.1f}%, abaixo de 11%, mas o IC "
              f"alcanca {hi:.1f}% -- nao e parada, e a extrapolacao encolhe.")
    else:
        print(f"   OK: estrato pago em {100*taxa:.1f}% (piso do IC em {lo:.1f}%).")

    print("\npor editora, dentro do estrato pago (>= 30 tentados):")
    eds = sorted(
        {c[2] for c in T if c[0] == "estrato+editora" and c[1] == "pago"},
        key=lambda e: -O[("estrato+editora", "pago", e)],
    )
    for e in eds:
        n = T[("estrato+editora", "pago", e)]
        if n >= 30:
            print(linha(e, O[("estrato+editora", "pago", e)], n))

    rec = ok[("TOTAL",)]
    n_cat = con.execute("select count(*) from articles").fetchone()[0]
    print(f"\nGanho ate aqui: {rec} artigos que estavam marcados como inacessiveis")
    print(f"ou irrecuperaveis foram obtidos sem credencial nenhuma -- "
          f"{100*rec/n_cat:.1f}% do catalogo de {n_cat}.")
    if usa_tentados:
        falta = tot[("estrato", "pago")] - n_pago
        print(f"Projecao para o resto do estrato pago ({falta} nao tentados): "
              f"+{falta*taxa:.0f} artigos")
        print(f"  faixa pelo IC95% da taxa: +{falta*lo/100:.0f} a +{falta*hi/100:.0f}")


if __name__ == "__main__":
    main()
