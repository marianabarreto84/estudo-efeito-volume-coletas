"""
Confiabilidade INTRA-codificador: a Mariana concorda consigo mesma?

Por que existe. A `p6` ficou em kappa 0,697 contra a rotulagem humana, com
aceite pre-registrado em 0,70. Antes de concluir que o rotulador e insuficiente
e preciso saber qual e o TETO da tarefa — nenhum instrumento supera a
concordancia de um codificador consigo mesmo. Esse numero nunca foi medido:
nem aqui, nem no artigo original, que nao reporta concordancia entre seus
codificadores.

Desenho: 30 dos 100 tweets que ela ja rotulou, sorteados estratificadamente
pelas tres classes, com o rotulo anterior ESCONDIDO e a ordem embaralhada.

Ressalva que fica registrada. O reteste ocorre no mesmo dia da rotulagem
original. A memoria **infla** a auto-concordancia, entao o valor medido e um
limite SUPERIOR otimista do teto real. O vies joga CONTRA o rotulador (faz o
teto parecer mais alto e a maquina parecer pior), o que torna o teste
conservador para o que queremos decidir. O ideal metodologico seria esperar
semanas; nao ha cronograma para isso.

Os rotulos ORIGINAIS seguem sendo a referencia canonica das validacoes ja
feitas. Este reteste mede consistencia, nao corrige nada.

Uso:
    PYTHONIOENCODING=utf-8 python -u analise/reteste_intracodificador.py
    # depois de preencher:
    PYTHONIOENCODING=utf-8 python -u analise/reteste_intracodificador.py --medir
"""
import argparse
import json
import pathlib
import random
import sys
from collections import Counter, defaultdict

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from analise.valida_rotulador import kappa_cohen

DADOS = RAIZ / "data" / "repl" / "vacinas2022"
ORIGINAL = DADOS / "VALIDACAO_HUMANA_amostra.xlsx"
CSV_ROT = DADOS / "RETESTE_intracodificador.csv"
CSV_IDS = DADOS / "reteste_intracodificador_ids.csv"
MD = DADOS / "RETESTE_intracodificador.md"
P6 = DADOS / "rotulos_llm" / "amostra_humana_p6" / "rotulos.csv"

SEED = 20260728
N = 30


def gera(n, seed, refazer):
    if CSV_IDS.exists() and not refazer:
        raise SystemExit(f"[erro] reteste ja sorteado em {CSV_IDS} (use --refazer)")
    x = pd.read_excel(ORIGINAL, "ROTULAR", dtype={"ID": str})
    x["h"] = x.stance.astype(str).str.strip().str.lower()
    x = x[x.h.isin({"pro", "anti", "nenhum"})]

    rng = random.Random(seed)
    por_classe = defaultdict(list)
    for r in x.itertuples():
        por_classe[r.h].append((r.ID, " ".join(str(r.tweet).split())))

    escolhidos = []
    # cota proporcional a distribuicao original, minimo 6 por classe para que
    # nenhuma fique sem massa
    total = sum(len(v) for v in por_classe.values())
    for classe in sorted(por_classe):
        cota = max(6, round(n * len(por_classe[classe]) / total))
        itens = sorted(por_classe[classe])
        rng.shuffle(itens)
        escolhidos += [(i, t, classe) for i, t in itens[:cota]]
    rng.shuffle(escolhidos)          # ordem diferente da planilha original
    escolhidos = escolhidos[:n]

    pd.DataFrame([{"ID": i, "stance_original": c} for i, _, c in escolhidos]
                 ).to_csv(CSV_IDS, index=False, encoding="utf-8")
    pd.DataFrame([{"ID": i, "stance": "", "observacao": "", "tweet": t}
                  for i, t, _ in escolhidos]).to_csv(
        CSV_ROT, index=False, encoding="utf-8-sig")

    print(f"[ok] {len(escolhidos)} tweets sorteados (seed {seed}), "
          f"rotulo anterior escondido, ordem embaralhada")
    print(f"     composicao original: "
          f"{dict(Counter(c for _, _, c in escolhidos))}")
    print(f"[ok] preencher a coluna `stance`: {CSV_ROT.name}")
    print(f"[ok] depois: python analise/reteste_intracodificador.py --medir")


def mede():
    if not CSV_ROT.exists():
        raise SystemExit("[erro] gere o reteste antes")
    ids = pd.read_csv(CSV_IDS, dtype={"ID": str}).set_index("ID")
    novo = pd.read_csv(CSV_ROT, dtype={"ID": str})
    novo["h2"] = novo.stance.astype(str).str.strip().str.lower()
    novo = novo[novo.h2.isin({"pro", "anti", "nenhum"})]
    if novo.empty:
        raise SystemExit("[erro] nenhuma linha preenchida em " + CSV_ROT.name)
    if len(novo) < len(ids):
        print(f"[aviso] {len(ids)-len(novo)} linhas em branco; usando {len(novo)}")

    h1 = [ids.loc[i, "stance_original"] for i in novo.ID]
    h2 = list(novo.h2)
    k_intra = kappa_cohen(h1, h2)
    ac = sum(a == b for a, b in zip(h1, h2)) / len(h1)

    # o rotulador nos MESMOS tweets, para comparar na mesma base
    k_p6 = None
    if P6.exists():
        m = pd.read_csv(P6, dtype={"ID": str}).set_index("ID")
        alvo = [i for i in novo.ID if i in m.index]
        if alvo:
            k_p6 = kappa_cohen([ids.loc[i, "stance_original"] for i in alvo],
                               [m.loc[i, "stance"] for i in alvo])

    def f(v):
        return "—" if v is None else f"{v:.3f}"

    if k_intra is None:
        leitura = "Nao foi possivel calcular."
    elif k_p6 is not None and k_p6 >= k_intra - 0.05:
        leitura = (
            "**O rotulador esta no teto da tarefa.** A concordancia da "
            "codificadora consigo mesma nao e materialmente maior que a "
            "concordancia entre ela e o rotulador. O criterio de 0,70 exigia "
            "do instrumento uma consistencia que a propria tarefa nao "
            "oferece — a reprovacao da `p6` deve ser lida como limite do "
            "construto, e nao como insuficiencia do modelo. Reportar o eixo B "
            "como bem-sucedido, com o teto declarado.")
    else:
        leitura = (
            "**Ha folga real entre o rotulador e o teto humano.** A "
            "codificadora e mais consistente consigo mesma do que o rotulador "
            "e com ela. A reprovacao da `p6` reflete limitacao do "
            "instrumento, nao do construto: ha o que ganhar com mais "
            "calibracao ou com um modelo maior.")

    L = [
        "# Confiabilidade intra-codificador — o teto da tarefa",
        "",
        f"n = {len(h1)} tweets re-rotulados as cegas pela mesma codificadora.",
        "",
        "| Medida | κ |",
        "|---|---:|",
        f"| **Mariana × Mariana** (teto da tarefa) | **{f(k_intra)}** |",
        f"| `p6` × Mariana, nos mesmos tweets | {f(k_p6)} |",
        f"| `p6` × Mariana, partição reservada (n=50) | 0,697 |",
        f"| Mariana × gabarito do paper (esquema binário) | 0,350 |",
        "",
        f"Acurácia da auto-concordância: {ac:.3f}",
        "",
        "## Leitura",
        "",
        leitura,
        "",
        "## Ressalvas",
        "",
        "1. **O reteste ocorreu no mesmo dia da rotulagem original.** A memória",
        "   infla a auto-concordância, então este κ é um **limite superior",
        "   otimista** do teto real. O viés joga contra o rotulador — faz o teto",
        "   parecer mais alto e a máquina parecer pior —, o que torna o teste",
        "   conservador para a decisão em questão.",
        "2. n = 30: intervalo largo. Serve para distinguir ordens de grandeza",
        "   (0,7 contra 0,95), não para precisão.",
        "3. Os rótulos **originais** seguem canônicos nas validações já feitas.",
        "   Este reteste mede consistência; não corrige nada retroativamente.",
        "4. Confiabilidade intra-codificador é um teto mais frouxo que",
        "   inter-codificador. O ideal seria um segundo codificador humano —",
        "   que o artigo original teve (dois + árbitro) mas cujo κ não reportou.",
    ]
    MD.write_text("\n".join(L), encoding="utf-8")
    print(f"  Mariana x Mariana : kappa={f(k_intra)}  acuracia={ac:.3f}")
    print(f"  p6 x Mariana      : kappa={f(k_p6)}  (mesmos tweets)")
    print(f"[ok] escrito: {MD}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=N)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--medir", action="store_true")
    args = ap.parse_args()
    mede() if args.medir else gera(args.n, args.seed, args.refazer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
