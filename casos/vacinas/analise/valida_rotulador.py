"""
Eixo B / passo 4 — Valida o rotulador contra o gabarito humano (kappa de Cohen).

Este e o passo que legitima (ou reprova) o rotulador. Criterio de aceite
registrado antes de rodar, em PRE_REGISTRO_split.md:
  - kappa do stance          >= 0.70
  - mediana dos kappas das 14 categorias >= 0.60
Ambos medidos no TESTE CEGO, uma unica vez.

Kappa implementado a mao (nao vale puxar sklearn so por isso, e a formula
explicita e mais auditavel que uma chamada de biblioteca).

Uso:
    python -u analise/valida_rotulador.py --conjunto dev --prompt p1
    python -u analise/valida_rotulador.py --conjunto teste --prompt p1

Gera data/repl/vacinas2022/rotulos_llm/<conjunto>_<prompt>/VALIDACAO.md + .json
"""
import argparse
import json
import pathlib
import sys

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
DADOS = RAIZ / "data" / "repl" / "vacinas2022"
XLSX = DADOS / "suplementar_rotulos.xlsx"
CODEBOOK = DADOS / "codebook_v1.json"
SAIDA = DADOS / "rotulos_llm"

ACEITE_STANCE = 0.70
ACEITE_CATEGORIAS_MEDIANA = 0.60


def kappa_cohen(a, b):
    """
    Kappa de Cohen entre dois rotuladores, sobre rotulos categoricos alinhados.
    (Po - Pe) / (1 - Pe). Devolve None quando Pe == 1 (um dos rotuladores usou
    uma unica classe e nao ha margem de acordo acima do acaso).
    """
    a, b = list(a), list(b)
    n = len(a)
    if n == 0:
        return None
    classes = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in classes)
    if abs(1 - pe) < 1e-12:
        return None
    return (po - pe) / (1 - pe)


def metricas_binarias(ouro, prev):
    """Precisao/recall/F1 da classe positiva (1), alem do kappa."""
    vp = sum(1 for o, p in zip(ouro, prev) if o == 1 and p == 1)
    fp = sum(1 for o, p in zip(ouro, prev) if o == 0 and p == 1)
    fn = sum(1 for o, p in zip(ouro, prev) if o == 1 and p == 0)
    prec = vp / (vp + fp) if (vp + fp) else None
    rec = vp / (vp + fn) if (vp + fn) else None
    f1 = (2 * prec * rec / (prec + rec)) if (prec and rec) else None
    return {"vp": vp, "fp": fp, "fn": fn, "precisao": prec, "recall": rec, "f1": f1}


def stance_ouro(linha):
    if linha["Tweet_ProVax"] == 1:
        return "pro"
    if linha["Tweet_AntiVax"] == 1:
        return "anti"
    return "nenhum"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conjunto", default="dev", choices=["dev", "teste", "tudo"])
    ap.add_argument("--prompt", default="p1")
    args = ap.parse_args()

    pasta = SAIDA / f"{args.conjunto}_{args.prompt}"
    csv = pasta / "rotulos.csv"
    if not csv.exists():
        raise SystemExit(
            f"[erro] {csv} nao existe. Rode antes:\n"
            f"       python pipeline/rotula_conteudo.py --conjunto {args.conjunto} "
            f"--prompt {args.prompt}"
        )

    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    categorias = codebook["categorias"]
    prev = pd.read_csv(csv, dtype={"ID": str})
    gab = pd.read_excel(XLSX, "Spreadsheet 1")
    gab["ID"] = gab["ID"].astype(str)
    gab = gab[gab.ID.isin(set(prev.ID))].set_index("ID")

    ids = [i for i in prev.ID if i in gab.index]
    if len(ids) != len(prev):
        print(f"[aviso] {len(prev) - len(ids)} IDs previstos nao estao no gabarito")
    prev = prev.set_index("ID").loc[ids]

    # ---- stance ----
    ouro_s = [stance_ouro(gab.loc[i]) for i in ids]
    prev_s = [prev.loc[i, "stance"] for i in ids]
    k_stance = kappa_cohen(ouro_s, prev_s)
    acuracia = sum(1 for a, b in zip(ouro_s, prev_s) if a == b) / len(ids)

    # ---- categorias ----
    linhas_cat = []
    for c in categorias:
        ouro = [int(gab.loc[i, c["coluna"]] == 1) for i in ids]
        p = [int(prev.loc[i, f"cat_{c['numero']}"] == 1) for i in ids]
        m = metricas_binarias(ouro, p)
        linhas_cat.append({
            "numero": c["numero"], "nome": c["nome_en"], "nome_pt": c["nome_pt"],
            "n_ouro": sum(ouro), "n_previsto": sum(p),
            "kappa": kappa_cohen(ouro, p), **m,
        })

    kappas = [l["kappa"] for l in linhas_cat if l["kappa"] is not None]
    kappas_ord = sorted(kappas)
    mediana = (kappas_ord[len(kappas_ord) // 2] if len(kappas_ord) % 2
               else (kappas_ord[len(kappas_ord)//2 - 1] + kappas_ord[len(kappas_ord)//2]) / 2)

    passou_stance = k_stance is not None and k_stance >= ACEITE_STANCE
    passou_cats = mediana >= ACEITE_CATEGORIAS_MEDIANA
    veredito = "APROVADO" if (passou_stance and passou_cats) else "REPROVADO"

    res = {
        "conjunto": args.conjunto, "prompt": args.prompt, "n": len(ids),
        "stance": {"kappa": k_stance, "acuracia": acuracia,
                   "aceite": ACEITE_STANCE, "passou": passou_stance},
        "categorias": {"kappas_mediana": mediana,
                       "aceite": ACEITE_CATEGORIAS_MEDIANA,
                       "passou": passou_cats, "por_categoria": linhas_cat},
        "veredito": veredito,
    }
    (pasta / "VALIDACAO.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    def f(v):
        return "—" if v is None else f"{v:.3f}"

    L = [
        f"# Validacao do rotulador — conjunto `{args.conjunto}`, prompt `{args.prompt}`",
        "",
        f"**{veredito}** (n = {len(ids)})",
        "",
        "| Metrica | Valor | Aceite | |",
        "|---|---:|---:|---|",
        f"| kappa do stance | {f(k_stance)} | {ACEITE_STANCE:.2f} | "
        f"{'passou' if passou_stance else 'reprovou'} |",
        f"| mediana dos kappas das categorias | {f(mediana)} | "
        f"{ACEITE_CATEGORIAS_MEDIANA:.2f} | {'passou' if passou_cats else 'reprovou'} |",
        f"| acuracia do stance | {acuracia:.3f} | — | |",
        "",
        "## Por categoria",
        "",
        "| # | Categoria | n (gabarito) | n (LLM) | kappa | precisao | recall | F1 |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for l in sorted(linhas_cat, key=lambda x: -(x["kappa"] or -1)):
        L.append(
            f"| {l['numero']} | {l['nome']} | {l['n_ouro']} | {l['n_previsto']} | "
            f"{f(l['kappa'])} | {f(l['precisao'])} | {f(l['recall'])} | {f(l['f1'])} |"
        )
    if args.conjunto == "teste":
        L += ["", "> Teste cego: medido uma unica vez, com o prompt ja congelado.",
              "> Ajustar o prompt a partir daqui invalida este numero."]
    (pasta / "VALIDACAO.md").write_text("\n".join(L), encoding="utf-8")

    print(f"[{veredito}] n={len(ids)}")
    print(f"  stance: kappa={f(k_stance)} (aceite {ACEITE_STANCE}) "
          f"acuracia={acuracia:.3f}")
    print(f"  categorias: mediana kappa={f(mediana)} "
          f"(aceite {ACEITE_CATEGORIAS_MEDIANA})")
    for l in sorted(linhas_cat, key=lambda x: (x["kappa"] is not None, x["kappa"] or 0)):
        print(f"    {l['numero']:>2} {l['nome'][:34]:<34} kappa={f(l['kappa'])} "
              f"n_ouro={l['n_ouro']:>4} n_llm={l['n_previsto']:>4}")
    print(f"[ok] escrito: {pasta / 'VALIDACAO.md'}")
    return 0 if veredito == "APROVADO" else 2


if __name__ == "__main__":
    sys.exit(main())
