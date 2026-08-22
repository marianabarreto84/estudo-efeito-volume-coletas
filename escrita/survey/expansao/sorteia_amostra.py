# =====================================================================
#  Sorteia a amostra da expansao do corpus da survey.
#
#  Regra pre-registrada em PRE_REGISTRO_expansao.md sec. 3:
#    populacao = artigos que (a) NAO tinham pdf_path no baseline congelado,
#                (b) ganharam PDF nesta expansao e (c) nao tem analyses;
#    ordenar por id; random.Random(20260929).sample(populacao, 800);
#    se |populacao| <= 800, extrai-se toda ela (censo do estrato).
#
#  Nao gasta nada e nao escreve no banco: so le e grava amostra.json.
#
#  Uso:
#    python sorteia_amostra.py            -> grava amostra.json
#    python sorteia_amostra.py --n 400    -> outro tamanho (registrar antes!)
# =====================================================================
import argparse
import json
import os
import random
import sqlite3

AQUI = os.path.dirname(os.path.abspath(__file__))
DB = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\research.db"
BASELINE = os.path.join(AQUI, "baseline_ids.json")
SAIDA = os.path.join(AQUI, "amostra.json")

SEMENTE = 20260929  # a data da defesa; fixa e sem relacao com os dados
N_ALVO = 800


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=N_ALVO)
    ap.add_argument("--semente", type=int, default=SEMENTE)
    ap.add_argument("--saida", default=SAIDA)
    args = ap.parse_args()

    base = json.load(open(BASELINE, encoding="utf-8"))
    tinha_pdf = set(base["ids_com_pdf_antes"])
    tinha_analise = set(base["ids_com_analise"])

    con = sqlite3.connect(DB)
    com_pdf_agora = {
        aid: p
        for aid, p in con.execute(
            "select id, pdf_path from articles where pdf_path is not null"
        )
    }

    # (a) e (b): ganhou PDF nesta expansao
    novos = set(com_pdf_agora) - tinha_pdf
    # (c): sem analise previa
    populacao = sorted(novos - tinha_analise)

    # Um pdf_path gravado cujo arquivo sumiu nao e extraivel.
    faltando = [i for i in populacao if not os.path.exists(com_pdf_agora[i])]
    populacao = [i for i in populacao if i not in set(faltando)]

    fila_baseline = base["n_fila_sem_pdf"]
    taxa = len(novos) / fila_baseline if fila_baseline else 0.0

    print(f"fila do baseline ....... {fila_baseline}")
    print(f"recuperados ............ {len(novos)}  (taxa {100*taxa:.1f}%)")
    if faltando:
        print(f"pdf_path sem arquivo ... {len(faltando)} (excluidos)")
    print(f"populacao elegivel ..... {len(populacao)}")

    # Condicoes de parada pre-registradas (sec. 8)
    if taxa < 0.11:
        print("\n!! PARAR: taxa de recuperacao abaixo de 11%, o piso do IC da")
        print("   sondagem de 70 DOIs. A extrapolacao de 1.127-2.944 nao vale.")
    if len(populacao) < 100:
        print("\n!! PARAR: populacao recuperada abaixo de 100. Nao ha amostra a")
        print("   sortear; reporta-se so a taxa de recuperacao.")
        return

    if len(populacao) <= args.n:
        amostra = list(populacao)
        modo = "censo"
        print(f"\npopulacao <= n: extrai-se TODA ela ({len(amostra)}) -- e censo do estrato")
    else:
        amostra = sorted(random.Random(args.semente).sample(populacao, args.n))
        modo = "amostra"
        print(f"\nsorteados {len(amostra)} de {len(populacao)} (semente {args.semente})")

    d = {
        "modo": modo,
        "semente": args.semente,
        "n_alvo": args.n,
        "fila_baseline": fila_baseline,
        "n_recuperados": len(novos),
        "taxa_recuperacao": round(taxa, 4),
        "n_populacao": len(populacao),
        "ids_populacao": populacao,
        "ids_amostra": amostra,
    }
    json.dump(d, open(args.saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"gravado em {args.saida}")
    print("\npara extrair (do repo da survey):")
    print("  python -m scripts.analyze_pdfs --models gemini --workers 5 \\")
    print("      --ids $(python -c \"import json;print(' '.join(map(str,json.load(open(r'%s'))['ids_amostra'])))\")" % args.saida)


if __name__ == "__main__":
    main()
