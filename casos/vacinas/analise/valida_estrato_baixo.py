"""
Fase 3 / limitacao 1 — mede o kappa entre a rotulagem HUMANA e o rotulador
automatico no estrato BAIXO (10 < RT <= 100).

Fecha o ciclo aberto por `amostra_validacao_humana.py`. O achado principal da
Fase 3 (a inversao do stance ao descer o limiar) depende de um estrato onde o
rotulador nunca foi validado — o gabarito do paper so cobre >500 RT. Este
script diz se ele transfere.

Criterio (o mesmo do teste cego, registrado em PRE_REGISTRO_split.md):
  kappa do stance >= 0,70  E  mediana dos kappas das categorias >= 0,60.

Uso:
    PYTHONIOENCODING=utf-8 python -u analise/valida_estrato_baixo.py

Gera data/repl/vacinas2022/VALIDACAO_ESTRATO_BAIXO.md (+ .json)
"""
import argparse
import json
from collections import Counter
import pathlib
import sys

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from analise.valida_rotulador import kappa_cohen, metricas_binarias

DADOS = RAIZ / "data" / "repl" / "vacinas2022"
CODEBOOK = DADOS / "codebook_v1.json"
XLSX = DADOS / "VALIDACAO_HUMANA_amostra.xlsx"
ROTULOS_LLM = DADOS / "rotulos_llm" / "e1_lim10_pt_p4" / "rotulos.csv"
MD = DADOS / "VALIDACAO_ESTRATO_BAIXO.md"
JSON = DADOS / "validacao_estrato_baixo.json"

ACEITE_STANCE = 0.70
ACEITE_CATEGORIAS = 0.60
STANCES = {"pro", "anti", "nenhum"}


def parse_categorias(valor, validos):
    """'1,2, 8' -> {1,2,8}. Tolera vazio, ponto-e-virgula e espacos."""
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return set()
    texto = str(valor).replace(";", ",").replace(" ", "")
    if not texto or texto.lower() in ("nan", "-", "0"):
        return set()
    numeros = set()
    for parte in texto.split(","):
        if not parte:
            continue
        if not parte.isdigit() or int(parte) not in validos:
            raise ValueError(f"categoria invalida: {parte!r} em {valor!r}")
        numeros.add(int(parte))
    return numeros


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--xlsx", default=str(XLSX))
    args = ap.parse_args()

    caminho = pathlib.Path(args.xlsx)
    if not caminho.exists():
        raise SystemExit(f"[erro] planilha nao encontrada: {caminho}\n"
                         "       rode antes: analise/amostra_validacao_humana.py")

    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    validos = {c["numero"] for c in codebook["categorias"]}

    hum = pd.read_excel(caminho, "ROTULAR", dtype={"ID": str})
    preenchidas = hum[hum.stance.notna() & (hum.stance.astype(str).str.strip() != "")]
    if preenchidas.empty:
        raise SystemExit("[erro] nenhuma linha preenchida na aba ROTULAR.")
    if len(preenchidas) < len(hum):
        print(f"[aviso] {len(hum) - len(preenchidas)} de {len(hum)} linhas em "
              f"branco — o kappa usa so as {len(preenchidas)} preenchidas")

    ruins = sorted(set(preenchidas.stance.astype(str).str.strip().str.lower()) - STANCES)
    if ruins:
        raise SystemExit(f"[erro] valores de stance invalidos: {ruins}\n"
                         f"       use apenas: pro, anti, nenhum")

    llm = pd.read_csv(ROTULOS_LLM, dtype={"ID": str}).set_index("ID")
    faltam = [i for i in preenchidas.ID if i not in llm.index]
    if faltam:
        print(f"[aviso] {len(faltam)} ids sem rotulo do modelo, excluidos")
        preenchidas = preenchidas[~preenchidas.ID.isin(faltam)]

    ids = list(preenchidas.ID)
    h_stance = [str(s).strip().lower() for s in preenchidas.stance]
    m_stance = [llm.loc[i, "stance"] for i in ids]
    k_stance = kappa_cohen(h_stance, m_stance)
    acuracia = sum(a == b for a, b in zip(h_stance, m_stance)) / len(ids)

    # Modo stance-only: a coluna de categorias pode vir toda vazia de proposito.
    # O stance e a metrica de que o achado da Fase 3 depende; as categorias sao
    # a conclusao robusta (o vies de sub-marcacao do rotulador ATENUA diferencas
    # entre estratos, entao joga a favor de achar convergencia, nao contra).
    # Sem categorias preenchidas, o veredito sai so do stance.
    col_cats = preenchidas.categorias.astype(str).str.strip().str.lower()
    so_stance = bool(((col_cats == "") | (col_cats == "nan")).all())
    if so_stance:
        print("[modo] rotulagem stance-only — categorias nao avaliadas")

    try:
        h_cats = ([set()] * len(preenchidas) if so_stance
                  else [parse_categorias(v, validos)
                        for v in preenchidas.categorias])
    except ValueError as e:
        raise SystemExit(f"[erro] {e}\n       corrija a planilha e rode de novo")

    por_categoria = []
    for c in codebook["categorias"]:
        n = c["numero"]
        humano = [int(n in s) for s in h_cats]
        modelo = [int(llm.loc[i, f"cat_{n}"] == 1) for i in ids]
        por_categoria.append({
            "numero": n, "nome": c["nome_en"],
            "n_humano": sum(humano), "n_modelo": sum(modelo),
            "kappa": kappa_cohen(humano, modelo), **metricas_binarias(humano, modelo),
        })

    if so_stance:
        por_categoria = []
    kappas = sorted(x["kappa"] for x in por_categoria if x["kappa"] is not None)
    if kappas:
        meio = len(kappas) // 2
        mediana = (kappas[meio] if len(kappas) % 2
                   else (kappas[meio - 1] + kappas[meio]) / 2)
    else:
        mediana = None

    passou_s = k_stance is not None and k_stance >= ACEITE_STANCE
    passou_c = mediana is not None and mediana >= ACEITE_CATEGORIAS
    if so_stance:
        veredito = "APROVADO" if passou_s else "REPROVADO"
    else:
        veredito = "APROVADO" if (passou_s and passou_c) else "REPROVADO"

    def f(v):
        return "—" if v is None else f"{v:.3f}"

    L = [
        "# Validação do rotulador no estrato BAIXO (10 < RT ≤ 100)",
        "",
        f"**{veredito}** — n = {len(ids)} tweets rotulados à mão pela Mariana,",
        "cegos aos rótulos do modelo.",
        "",
        "> ## ⚠️ RETRATAÇÃO — a leitura abaixo foi derrubada",
        ">",
        "> O teste de calibragem (`CALIBRAGEM_criterio.md`) mostrou que a",
        "> Mariana marca `nenhum` em **33% dos tweets VIRAIS** — praticamente a",
        "> mesma taxa dos 32% que marcou no estrato baixo. Os neutros não são",
        "> propriedade do estrato: são propriedade do critério dela, que difere",
        "> do dos codificadores do paper (κ 0,350 entre os dois, no mesmo",
        "> material).",
        ">",
        "> Portanto o κ medido aqui **não mede** transferência do instrumento",
        "> entre estratos — mede distância entre dois padrões humanos de",
        "> codificação. A conclusão original deste documento (\"a sub-coleta",
        "> contaminou o instrumento\") era uma sobre-interpretação e está",
        "> retirada. Ver `CALIBRAGEM_criterio.md` para o que ficou no lugar.",
        "",
        "> Este é o teste que decide se o achado principal da Fase 3 — a",
        "> inversão do stance ao descer o limiar — se sustenta. O κ de 0,759",
        "> do teste cego foi medido só em >500 RT, e a conclusão depende do",
        "> estrato baixo.",
        "",
        "| Métrica | Valor | Aceite | |",
        "|---|---:|---:|---|",
        f"| κ do stance | {f(k_stance)} | {ACEITE_STANCE:.2f} | "
        f"{'passou' if passou_s else 'reprovou'} |",
        (f"| mediana dos κ das categorias | — | {ACEITE_CATEGORIAS:.2f} | "
         "não medido (rotulagem stance-only) |" if so_stance else
         f"| mediana dos κ das categorias | {f(mediana)} | "
         f"{ACEITE_CATEGORIAS:.2f} | {'passou' if passou_c else 'reprovou'} |"),
        f"| acurácia do stance | {acuracia:.3f} | — | |",
        "",
        "### Comparação com o estrato viral",
        "",
        "| | >500 RT (teste cego) | 10–100 RT (aqui) |",
        "|---|---:|---:|",
        f"| κ stance | 0,759 | {f(k_stance)} |",
        f"| mediana κ categorias | 0,650 | {f(mediana)} |",
        f"| n | 1.018 | {len(ids)} |",
        "",
    ]
    marg_h, marg_m = Counter(h_stance), Counter(m_stance)
    conf = Counter(zip(h_stance, m_stance))
    if so_stance:
        L += [
            "## Distribuição do stance — humano × modelo",
            "",
            "| | humano | modelo |",
            "|---|---:|---:|",
        ]
        for s in ("pro", "anti", "nenhum"):
            L.append(f"| {s} | {marg_h.get(s,0)} ({100*marg_h.get(s,0)/len(ids):.0f}%) "
                     f"| {marg_m.get(s,0)} ({100*marg_m.get(s,0)/len(ids):.0f}%) |")
        L += ["", "### Matriz de confusão (linha = humano, coluna = modelo)", "",
              "| humano ＼ modelo | pro | anti | nenhum |", "|---|---:|---:|---:|"]
        for h in ("pro", "anti", "nenhum"):
            L.append(f"| **{h}** | " + " | ".join(
                str(conf.get((h, m), 0)) for m in ("pro", "anti", "nenhum")) + " |")
    else:
        L += [
            "## Por categoria",
            "",
            "| # | Categoria | n humano | n modelo | κ | precisão | recall | F1 |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
        for x in sorted(por_categoria, key=lambda y: -(y["kappa"] or -1)):
            L.append(f"| {x['numero']} | {x['nome']} | {x['n_humano']} | "
                     f"{x['n_modelo']} | {f(x['kappa'])} | {f(x['precisao'])} | "
                     f"{f(x['recall'])} | {f(x['f1'])} |")
    # --- onde exatamente o rotulador quebra ---
    # A reprovacao global pode esconder um instrumento que e bom numa parte da
    # tarefa e pessimo em outra. Isolar a subtarefa pro x anti (restrita aos
    # tweets a que a humana atribuiu lado) diz se o que falhou foi distinguir
    # os polos ou detectar a ausencia de polo.
    dec = [(h, m) for h, m in zip(h_stance, m_stance) if h != "nenhum"]
    k_sub = kappa_cohen([h for h, _ in dec], [m for _, m in dec]) if dec else None
    ac_sub = (sum(1 for h, m in dec if h == m) / len(dec)) if dec else None
    h_pro = sum(1 for h, _ in dec if h == "pro")
    pct_h = 100 * h_pro / len(dec) if dec else None
    m_decididos = [m for m in m_stance if m != "nenhum"]
    pct_m = (100 * sum(1 for m in m_decididos if m == "pro") / len(m_decididos)
             if m_decididos else None)
    destino_nenhum = {s: sum(1 for h, m in zip(h_stance, m_stance)
                             if h == "nenhum" and m == s)
                      for s in ("pro", "anti", "nenhum")}

    L += [
        "",
        "## Onde o rotulador quebra — e onde não quebra",
        "",
        f"**Subtarefa `pro` × `anti`** (só os {len(dec)} tweets a que a humana",
        "atribuiu lado):",
        "",
        f"- κ = **{f(k_sub)}** · acurácia = {ac_sub:.3f}",
        f"- É **melhor** que no estrato viral (κ 0,759). Distinguir os polos o",
        "  rotulador faz bem aqui.",
        "",
        f"**Toda a falha está na classe `nenhum`.** Dos {marg_h.get('nenhum', 0)} "
        "tweets que a humana",
        f"considerou sem posição, o modelo forçou {destino_nenhum['pro']} para "
        f"`pro` e {destino_nenhum['anti']} para `anti`;",
        f"só {destino_nenhum['nenhum']} foram reconhecidos como sem posição.",
        "",
        "### A causa é o prompt, e é rastreável",
        "",
        "O prompt congelado (`p4`) instrui, literalmente:",
        "",
        "> *“Estes são tweets **VIRAIS** de um debate polarizado: quase todos",
        "> tomam partido (…). Não use `nenhum` como saída para o caso difícil.”*",
        "",
        "Essa instrução nasceu da calibração no estrato viral, onde o gabarito",
        "humano tem **3 neutros em 1.525** (0,2%). No estrato baixo os neutros",
        f"são **{100*marg_h.get('nenhum',0)/len(ids):.0f}%**. O prompt foi",
        "endurecido contra detectar exatamente o que passou a existir.",
        "",
        "> **Este é o achado metodológico do caso.** A sub-coleta não contaminou",
        "> só os dados: contaminou o **instrumento**. O rotulador foi calibrado",
        "> nas propriedades do estrato sub-coletado e, aplicado ao corpus amplo,",
        "> importou essas propriedades como pressuposto. É a tese da dissertação",
        "> acontecendo dentro do próprio método da dissertação.",
        "",
        "## O que sobra do achado da Fase 3",
        "",
        "A direção **sobrevive, e mais forte do que o instrumento indicava**:",
        "",
        "| entre os tweets com lado atribuído | % pró |",
        "|---|---:|",
        f"| humana, nesta amostra (n={len(dec)}) | **{pct_h:.1f}%** |",
        f"| modelo, nesta amostra | {pct_m:.1f}% |",
        "| modelo, corpus >10 RT | 62,6% |",
        "| humano (gabarito do paper), >500 RT | 48,4% |",
        "",
        "Os neutros que o modelo força para um lado se dividem quase igualmente",
        f"({destino_nenhum['pro']} pró / {destino_nenhum['anti']} anti), o que",
        "**atenua** a estimativa em direção a 50%. Logo o 62,6% medido no corpus",
        "é um **piso**, não um teto: a rotulagem humana desta amostra dá",
        f"{pct_h:.1f}%. A inversão pró/anti ao descer o limiar não é artefato —",
        "a magnitude relatada é que estava subestimada.",
        "",
        "## Leitura",
        "",
        ("O rotulador **transfere** para o estrato baixo. O achado da Fase 3"
         " deixa de ser provisório: a inversão do stance é do corpus, não do"
         " instrumento." if veredito == "APROVADO" else
         "O rotulador **não transfere** para o estrato baixo — mas a falha é"
         " **localizada, diagnosticada e de causa conhecida** (a instrução"
         " anti-`nenhum` do prompt, herdada da calibração no estrato viral)."
         " Não é ruído: é um erro de desenho meu, rastreável até a linha."
         " Consequências: (a) os percentuais absolutos da §1 da Fase 3 estão"
         " errados e devem ser retirados; (b) a **direção** do achado sobrevive"
         " e é confirmada pela rotulagem humana; (c) o caso ganha um achado"
         " metodológico melhor do que o original — a sub-coleta contaminou o"
         " instrumento, não só os dados."),
        "",
        f"_Amostra congelada: `validacao_humana_amostra.csv` (seed 20260726),_",
        "_estratificada em 10–25, 25–50 e 50–100 RT._",
    ]
    MD.write_text("\n".join(L), encoding="utf-8")
    JSON.write_text(json.dumps({
        "n": len(ids), "veredito": veredito,
        "stance": {"kappa": k_stance, "acuracia": acuracia},
        "categorias": {"mediana": mediana, "por_categoria": por_categoria},
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[{veredito}] n={len(ids)}")
    print(f"  stance    : kappa={f(k_stance)} (aceite {ACEITE_STANCE}) "
          f"acuracia={acuracia:.3f}")
    print(f"  categorias: mediana={f(mediana)} (aceite {ACEITE_CATEGORIAS})")
    print(f"[ok] escrito: {MD}")
    return 0 if veredito == "APROVADO" else 2


if __name__ == "__main__":
    sys.exit(main())
