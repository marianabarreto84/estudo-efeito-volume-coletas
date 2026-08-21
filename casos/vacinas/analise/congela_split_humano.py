"""
Congela o split calibracao/validacao sobre a rotulagem HUMANA do estrato baixo.

Contexto. A Mariana rotulou 130 tweets: 100 no estrato baixo (10 < RT <= 100) e
30 no viral (teste de calibragem de criterio). Para consertar o rotulador e
depois valida-lo sem circularidade, os 100 do estrato baixo sao divididos aqui
em 50 de calibracao + 50 reservados. Nao e preciso pedir mais rotulagem.

Cuidado com contaminacao. Ao diagnosticar os erros da p4 e da p5 eu **li** o
texto de alguns desses tweets — todos do grupo "humana=nenhum, modelo=lado".
Esses ids vao obrigatoriamente para a CALIBRACAO, para que a metade reservada
contenha apenas tweets cujo texto eu nunca vi. Os ids contaminados sao
reconstruidos aqui pela mesma expressao que os exibiu, e nao a mao.

Ressalva que fica registrada: mesmo assim eu ja vi as ESTATISTICAS agregadas
dos 100 (taxa de `nenhum`, matriz de confusao). A metade reservada e portanto
quase-cega, nao cega. E mais fraca que o teste cego do gabarito, e deve ser
reportada como tal.

Os 30 do estrato viral ficam INTEIROS reservados: deles eu vi so o kappa e a
matriz, nunca um texto individual.

Uso:
    PYTHONIOENCODING=utf-8 python -u analise/congela_split_humano.py
"""
import argparse
import hashlib
import json
import pathlib
import random
import sys
from collections import Counter, defaultdict

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
DADOS = RAIZ / "data" / "repl" / "vacinas2022"
BAIXO = DADOS / "VALIDACAO_HUMANA_amostra.xlsx"
CSV = DADOS / "split_humano_baixo.csv"
MD = DADOS / "PRE_REGISTRO_split_humano.md"

SEED = 20260727
FRACAO_CALIBRACAO = 0.5


def ids_contaminados():
    """
    Reconstroi os ids cujo texto ja foi exibido durante o diagnostico.
    Mesma expressao usada na epoca: os primeiros N do subconjunto
    "humana = nenhum, modelo != nenhum", na ordem da planilha, para p4 e p5.
    """
    x = pd.read_excel(BAIXO, "ROTULAR", dtype={"ID": str})
    x["h"] = x.stance.astype(str).str.strip().str.lower()
    vistos = set()
    for pasta, quantos in [("e1_lim10_pt_p4", 7), ("amostra_humana_p5", 6)]:
        caminho = DADOS / "rotulos_llm" / pasta / "rotulos.csv"
        if not caminho.exists():
            continue
        m = pd.read_csv(caminho, dtype={"ID": str}).set_index("ID")
        alvo = x[x.ID.isin(m.index)].copy()
        alvo["m"] = [m.loc[i, "stance"] for i in alvo.ID]
        err = alvo[(alvo.h == "nenhum") & (alvo.m != "nenhum")]
        vistos |= set(err.head(quantos).ID)
    return vistos


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refazer", action="store_true")
    args = ap.parse_args()

    if CSV.exists() and not args.refazer:
        raise SystemExit(f"[erro] split ja congelado em {CSV} (use --refazer)")

    x = pd.read_excel(BAIXO, "ROTULAR", dtype={"ID": str})
    x["h"] = x.stance.astype(str).str.strip().str.lower()
    x = x[x.h.isin({"pro", "anti", "nenhum"})]

    contaminados = ids_contaminados()
    rng = random.Random(SEED)

    # estratifica pelo rotulo humano, para as tres classes aparecerem dos dois
    # lados — sobretudo `nenhum`, que e a classe em disputa
    por_classe = defaultdict(list)
    for r in x.itertuples():
        por_classe[r.h].append(r.ID)

    particao = {i: "calibracao" for i in contaminados}
    for classe in sorted(por_classe):
        livres = sorted(i for i in por_classe[classe] if i not in contaminados)
        rng.shuffle(livres)
        # desconta os ja forcados para calibracao ao calcular a cota
        cota = round(len(por_classe[classe]) * FRACAO_CALIBRACAO)
        ja = sum(1 for i in por_classe[classe] if i in contaminados)
        for k, i in enumerate(livres):
            particao[i] = "calibracao" if (ja + k) < cota else "reservado"

    d = pd.DataFrame({
        "ID": list(x.ID),
        "particao": [particao[i] for i in x.ID],
        "stance_humano": list(x.h),
        "texto_ja_visto": [i in contaminados for i in x.ID],
    })
    d.to_csv(CSV, index=False, encoding="utf-8")
    sha = hashlib.sha256(CSV.read_bytes()).hexdigest()

    cal = d[d.particao == "calibracao"]
    res = d[d.particao == "reservado"]

    L = [
        "# Pré-registro — split calibração/validação da rotulagem humana",
        "",
        "> Congelado **antes** de escrever a `p6`. Gerado por",
        "> `analise/congela_split_humano.py`.",
        "",
        "## Por que existe",
        "",
        "O rotulador precisa de material de calibração com a classe neutra",
        "representada — o gabarito do paper não tem (ver `CALIBRAGEM_criterio.md`).",
        "A fonte é a rotulagem da Mariana. Para não validar no mesmo material em",
        "que se calibra, os 100 tweets do estrato baixo são divididos aqui.",
        "**Nenhuma rotulagem adicional foi solicitada** — os 130 tweets já",
        "rotulados bastam.",
        "",
        "## Parâmetros",
        "",
        f"- Seed: `{SEED}` · fração de calibração: `{FRACAO_CALIBRACAO}`",
        "- Estratificado pelo rótulo humano (as três classes nos dois lados)",
        f"- `split_humano_baixo.csv` SHA-256: `{sha}`",
        "",
        "| partição | n | pro | anti | nenhum |",
        "|---|---:|---:|---:|---:|",
    ]
    for nome, sub in [("calibração", cal), ("reservado", res)]:
        c = Counter(sub.stance_humano)
        L.append(f"| {nome} | {len(sub)} | {c.get('pro',0)} | "
                 f"{c.get('anti',0)} | {c.get('nenhum',0)} |")
    L += [
        "",
        "## Contaminação declarada",
        "",
        f"- **{len(contaminados)} tweets** tiveram o texto exibido durante o",
        "  diagnóstico dos erros da `p4` e da `p5`. Todos foram **forçados para",
        "  a calibração**, de modo que a partição reservada contém apenas",
        "  tweets cujo texto nunca foi lido.",
        "- ⚠️ Ainda assim, as **estatísticas agregadas** dos 100 já eram",
        "  conhecidas (taxa de `nenhum`, matriz de confusão) quando este split",
        "  foi feito. A partição reservada é, portanto, **quase-cega**, não",
        "  cega. É mais fraca que o teste cego do gabarito e deve ser reportada",
        "  com essa ressalva.",
        "- Os **30 tweets do estrato viral** (`CALIBRAGEM_criterio.csv`) ficam",
        "  inteiros reservados: deles só foram vistos o κ e a matriz de",
        "  confusão, nunca um texto individual. Servem como segunda checagem,",
        "  em estrato diferente.",
        "",
        "## Critério de aceite (registrado antes de medir)",
        "",
        "κ de Cohen ≥ **0,70** contra a rotulagem humana, na partição reservada,",
        "medido **uma única vez**. Mesmo patamar exigido do rotulador contra o",
        "gabarito do paper.",
        "",
        "## Aposta pré-registrada",
        "",
        "- A `p6` com exemplos neutros deve passar de 0,591 (`p5`) para a faixa",
        "  de 0,75–0,85: a classe `nenhum` deixa de depender só de prosa e passa",
        "  a ter exemplos.",
        "- Não deve chegar perto de 1: parte dos desacordos é irredutível —",
        "  notícia selecionada e fala citada admitem leitura dupla, e alguns dos",
        "  casos examinados pareciam mais defensáveis do lado do modelo.",
        "- No estrato viral (os 30), espera-se **queda** de concordância com o",
        "  gabarito do paper, por construção: adotar a classe neutra afasta o",
        "  rotulador do esquema binário forçado. Isso é o desenho, não falha.",
    ]
    MD.write_text("\n".join(L), encoding="utf-8")

    print(f"[ok] calibração={len(cal)}  reservado={len(res)}")
    print(f"     contaminados forçados p/ calibração: {len(contaminados)}")
    for nome, sub in [("calibração", cal), ("reservado", res)]:
        print(f"     {nome:<12} {dict(Counter(sub.stance_humano))}")
    print(f"[ok] escrito: {CSV}  (sha {sha[:16]}…)")
    print(f"[ok] escrito: {MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
