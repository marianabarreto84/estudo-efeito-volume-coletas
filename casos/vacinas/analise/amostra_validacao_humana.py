"""
Fase 3 / limitacao 1 — sorteia a amostra do estrato BAIXO para rotulagem humana.

Por que existe: o rotulador foi validado (kappa 0,759 no stance) so contra o
gabarito do paper, que existe apenas para >500 RT. A conclusao principal da
Fase 3 — a inversao do stance ao descer o limiar — depende justamente do
estrato NAO validado. Esta amostra permite medir o kappa la e confirmar ou
derrubar o achado.

Desenho:
  - universo: tweets com 10 < RT <= 100 (o estrato baixo, 80% do corpus do E1
    e o que mais difere do estrato de validacao);
  - estratificado por faixa de RT (10-25, 25-50, 50-100), para nao concentrar
    no fundo da distribuicao;
  - CEGO: a planilha nao mostra o rotulo do LLM, senao a rotuladora ancora
    nele e o kappa mede concordancia induzida, nao concordancia;
  - ordem embaralhada com seed publicada.

Uso:
    PYTHONIOENCODING=utf-8 python -u analise/amostra_validacao_humana.py
    (--n 100 --seed 20260726)

Gera em data/repl/vacinas2022/:
  - VALIDACAO_HUMANA_amostra.xlsx  (abas INSTRUCOES + ROTULAR — e o que preencher)
  - validacao_humana_amostra.csv   (os ids sorteados, congelados)
"""
import argparse
import json
import pathlib
import random
import sqlite3
import sys

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
DADOS = RAIZ / "data" / "repl" / "vacinas2022"
CODEBOOK = DADOS / "codebook_v1.json"
SNAPSHOT = DADOS / "snapshot_vacinas.sqlite"
XLSX = DADOS / "VALIDACAO_HUMANA_amostra.xlsx"
CSV = DADOS / "validacao_humana_amostra.csv"

FAIXAS = [(10, 25), (25, 50), (50, 100)]
SEED = 20260726


def sorteia(n, seed):
    con = sqlite3.connect(SNAPSHOT)
    rng = random.Random(seed)
    por_faixa = n // len(FAIXAS)
    escolhidos = []
    for i, (lo, hi) in enumerate(FAIXAS):
        # a ultima faixa absorve o resto da divisao
        quero = por_faixa if i < len(FAIXAS) - 1 else n - por_faixa * (len(FAIXAS) - 1)
        linhas = con.execute(
            "SELECT twitter_id, texto, retweets FROM originais "
            "WHERE retweets > ? AND retweets <= ? AND idioma = 'pt' "
            "AND texto IS NOT NULL AND trim(texto) != '' ORDER BY twitter_id",
            (lo, hi)).fetchall()
        rng.shuffle(linhas)
        for tid, texto, rt in linhas[:quero]:
            escolhidos.append({"ID": str(tid), "faixa_RT": f"{lo}-{hi}",
                               "retweets": int(rt), "tweet": str(texto).strip()})
    con.close()
    rng.shuffle(escolhidos)  # embaralha as faixas entre si
    return escolhidos


def escreve_xlsx(amostra, codebook, destino):
    instrucoes = [
        ["ROTULAGEM MANUAL — validacao do rotulador no estrato baixo", ""],
        ["", ""],
        ["Leia o guia completo antes de comecar:", "GUIA_ROTULAGEM.md"],
        ["", ""],
        ["O QUE PREENCHER (aba ROTULAR), duas colunas:", ""],
        ["", ""],
        ["1) stance", "escreva: pro, anti ou nenhum"],
        ["", "'pro'    = defende/apoia a vacinacao"],
        ["", "'anti'   = questiona/ataca/desencoraja a vacinacao"],
        ["", "'nenhum' = nao da para decidir de lado nenhum (raro)"],
        ["", "Julgue a posicao do AUTOR, nao a de quem ele cita."],
        ["", "Ironia conta: reproduzir fala antivacina para ridicularizar e 'pro'."],
        ["", ""],
        ["2) categorias", "os NUMEROS das que se aplicam, separados por virgula"],
        ["", "ex.: 1,2,8   (pode ser nenhuma: deixe vazio)"],
        ["", "Marque o tema se ele for citado ou aludido, ainda que de passagem."],
        ["", ""],
        ["AS 14 CATEGORIAS", ""],
    ]
    for c in codebook["categorias"]:
        instrucoes.append([f"{c['numero']}. {c['nome_en']}", c["nome_pt"]])
    instrucoes += [
        ["", ""],
        ["IMPORTANTE", ""],
        ["", "Esta planilha NAO mostra o rotulo do modelo, de proposito."],
        ["", "Ver o rotulo dele antes ancoraria o seu, e o kappa mediria"],
        ["", "concordancia induzida em vez de concordancia real."],
        ["", "Nao consulte data/repl/vacinas2022/rotulos_llm/ antes de terminar."],
        ["", ""],
        ["", "Nao pule tweets dificeis: um tweet dificil para voce provavelmente"],
        ["", "foi dificil para o modelo, e e exatamente onde o kappa informa."],
        ["", "Se ficar em duvida, decida e anote o porque na coluna 'observacao'."],
    ]

    tabela = pd.DataFrame([{
        "ID": t["ID"], "tweet": t["tweet"], "retweets": t["retweets"],
        "stance": "", "categorias": "", "observacao": "",
    } for t in amostra])

    with pd.ExcelWriter(destino, engine="openpyxl") as w:
        pd.DataFrame(instrucoes, columns=["", ""]).to_excel(
            w, sheet_name="INSTRUCOES", index=False)
        tabela.to_excel(w, sheet_name="ROTULAR", index=False)
        ws = w.sheets["ROTULAR"]
        larguras = {"A": 22, "B": 90, "C": 10, "D": 12, "E": 16, "F": 30}
        for col, larg in larguras.items():
            ws.column_dimensions[col].width = larg
        for linha in ws.iter_rows(min_row=2, min_col=2, max_col=2):
            linha[0].alignment = linha[0].alignment.copy(wrapText=True)
        ws.freeze_panes = "A2"
        w.sheets["INSTRUCOES"].column_dimensions["A"].width = 46
        w.sheets["INSTRUCOES"].column_dimensions["B"].width = 70


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--refazer", action="store_true",
                    help="sobrescreve uma amostra ja sorteada")
    args = ap.parse_args()

    if CSV.exists() and not args.refazer:
        raise SystemExit(
            f"[erro] amostra ja congelada em {CSV}.\n"
            "       Re-sortear depois de comecar a rotular enviesa a validacao.\n"
            "       Use --refazer so se nada foi rotulado ainda."
        )

    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    amostra = sorteia(args.n, args.seed)
    if len(amostra) < args.n:
        print(f"[aviso] so {len(amostra)} tweets disponiveis (pedido: {args.n})")

    pd.DataFrame(amostra).to_csv(CSV, index=False, encoding="utf-8")
    escreve_xlsx(amostra, codebook, XLSX)

    print(f"[ok] {len(amostra)} tweets sorteados (seed {args.seed}), "
          f"cegos ao rotulo do modelo")
    for lo, hi in FAIXAS:
        q = sum(1 for t in amostra if t["faixa_RT"] == f"{lo}-{hi}")
        print(f"     faixa {lo}-{hi} RT: {q}")
    print(f"[ok] preencher: {XLSX}")
    print(f"[ok] ids congelados: {CSV}")
    print(f"[ok] guia de rotulagem: {DADOS / 'GUIA_ROTULAGEM.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
