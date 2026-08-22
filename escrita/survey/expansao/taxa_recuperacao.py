# =====================================================================
#  Taxa de recuperacao da expansao, decomposta.
#
#  A condicao de parada pre-registrada (sec. 8) e "taxa abaixo de 11%",
#  o piso do IC da sondagem de 70 DOIs -- e aquela sondagem foi feita SO
#  no estrato pago. A fila da expansao mistura dois estratos bem
#  diferentes:
#
#    - pdf_inaccessible = 1  -> o estrato pago (10.074). E dele que fala
#      a sondagem, e e nele que a condicao de parada se aplica.
#    - pdf_inaccessible nulo/0 -> 1.019 artigos que o DBLP disse serem
#      abertos e que mesmo assim falharam antes. Sao, em boa parte,
#      falhas duras (URL ruim, DOI sem deposito) e puxam a taxa global
#      para baixo sem dizer nada sobre paywall.
#
#  Reportar a taxa global sem separar os dois seria comparar a sondagem
#  com outra coisa. Este script separa, e quebra tambem por editora
#  (prefixo de DOI), que e o que a limitacao do artigo afirma.
#
#  Nao escreve nada: so le o banco e o baseline congelado.
# =====================================================================
import json
import os
import sqlite3
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
DB = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\research.db"
BASELINE = os.path.join(AQUI, "baseline_ids.json")

EDITORAS = {
    "10.1007": "Springer", "10.1109": "IEEE", "10.1145": "ACM",
    "10.1016": "Elsevier", "10.1002": "Wiley", "10.1177": "SAGE",
    "10.1080": "Taylor & Francis", "10.1108": "Emerald",
    "10.3390": "MDPI", "10.1371": "PLOS", "10.48550": "arXiv",
    "10.1140": "EPJ/Springer", "10.1093": "Oxford UP",
    "10.1017": "Cambridge UP", "10.1186": "BMC/Springer",
}


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


def main():
    base = json.load(open(BASELINE, encoding="utf-8"))
    tinha_pdf = set(base["ids_com_pdf_antes"])
    con = sqlite3.connect(DB)

    # Fila do baseline = quem estava sem PDF quando o baseline foi congelado.
    fila = list(con.execute(
        "select id, doi, pdf_inaccessible from articles "
        "where doi is not null and id not in (select id from articles where pdf_path is not null)"
    ))
    # ...mais os que ja sairam da fila por terem sido recuperados agora.
    recuperados = set(
        aid for (aid,) in con.execute("select id from articles where pdf_path is not null")
    ) - tinha_pdf
    for aid, doi, inac in con.execute(
        "select id, doi, pdf_inaccessible from articles where pdf_path is not null"
    ):
        if aid in recuperados:
            fila.append((aid, doi, inac))

    tot = Counter()
    ok = Counter()
    for aid, doi, inac in fila:
        estrato = "pago" if inac == 1 else "aberto-que-falhou"
        pref = (doi or "").split("/")[0]
        ed = EDITORAS.get(pref, f"outra ({pref})" if pref else "sem DOI")
        acertou = aid in recuperados
        for chave in (("TOTAL",), ("estrato", estrato), ("editora", ed),
                      ("estrato+editora", estrato, ed)):
            tot[chave] += 1
            if acertou:
                ok[chave] += 1

    print("TAXA DE RECUPERACAO DA EXPANSAO")
    print("=" * 62)
    print(linha("fila inteira", ok[("TOTAL",)], tot[("TOTAL",)]))
    print("\npor estrato:")
    for e in ("pago", "aberto-que-falhou"):
        print(linha(e, ok[("estrato", e)], tot[("estrato", e)]))

    print("\n>> A condicao de parada de 11% vale sobre o estrato PAGO,")
    print("   que e o unico comparavel a sondagem de 70 DOIs (18,6%).")
    taxa_pago = ok[("estrato", "pago")] / max(tot[("estrato", "pago")], 1)
    lo, _ = wilson(ok[("estrato", "pago")], tot[("estrato", "pago")])
    if taxa_pago < 0.11:
        print(f"   !! PARAR: estrato pago em {100*taxa_pago:.1f}%, abaixo do piso de 11%.")
    else:
        print(f"   OK: estrato pago em {100*taxa_pago:.1f}% (piso do IC em {lo:.1f}%).")

    print("\npor editora, dentro do estrato pago (>= 30 na fila):")
    eds = sorted(
        {c[2] for c in tot if c[0] == "estrato+editora" and c[1] == "pago"},
        key=lambda e: -ok[("estrato+editora", "pago", e)],
    )
    for e in eds:
        n = tot[("estrato+editora", "pago", e)]
        if n >= 30:
            print(linha(e, ok[("estrato+editora", "pago", e)], n))

    n_cat = con.execute("select count(*) from articles").fetchone()[0]
    print(f"\nExtrapolacao sobre o catalogo: {len(recuperados)} artigos que estavam")
    print(f"marcados como inacessiveis ou irrecuperaveis foram obtidos sem credencial")
    print(f"nenhuma -- {100*len(recuperados)/n_cat:.1f}% do catalogo de {n_cat}.")


if __name__ == "__main__":
    main()
