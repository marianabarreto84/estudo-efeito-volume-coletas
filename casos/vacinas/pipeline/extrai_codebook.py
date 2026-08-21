"""
Eixo B / passo 1 — Extrai o CODEBOOK do material suplementar do paper.

Le `suplementar_rotulos.xlsx` (abas `Table broad categories` e
`Table subcategories`) e produz o codebook que vai DENTRO do prompt do
rotulador, com proveniencia: cada categoria carrega a coluna binaria
correspondente no gabarito (aba `Spreadsheet 1`) e os totais publicados.

Por que importa: o rotulador so e defensavel se as definicoes das categorias
vierem do paper, nao da nossa cabeca. Este script e a ponte auditavel entre a
Tabela 5 do preprint e o prompt.

Uso:
    PYTHONIOENCODING=utf-8 python -u pipeline/extrai_codebook.py

Gera em data/repl/vacinas2022/:
  - codebook_v1.json  (consumido pelo rotulador)
  - CODEBOOK.md       (leitura humana / anexo da dissertacao)

ACHADO: o paper fala em "11 categorias" no corpo do texto, mas o suplemento
tem 14 categorias amplas numeradas. Os dados vencem — usamos as 14.
"""
import argparse
import json
import pathlib
import sys

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "data" / "repl" / "vacinas2022"
XLSX = SAIDA / "suplementar_rotulos.xlsx"

VERSAO = "v1"

# Categoria ampla (numero do suplemento) -> coluna binaria agregada na aba
# `Spreadsheet 1`. As tabelas-resumo usam nomes curtos (All_Category_1); o
# gabarito usa os nomes longos. Este mapa e a unica costura manual do script,
# e cada linha e conferida contra o total publicado (ver confere_totais).
COLUNA_AGREGADA = {
    1: "All_Category_1_Politics",
    2: "About_all_Children",
    3: "All_Category_3_RestrictivePolicies",
    4: "About_all_disadvantages_vaccines_",
    5: "ALL_Category_5_AntivaxPeople",
    6: "About_Other_Countries",
    7: "About_all_advantages_vaccines",
    8: "About_COVID_risks",
    9: "About_Misinformation",
    10: "About_All_InformationSources_Social_OR_Official",
    11: "About_SCIENCE",
    12: "About_All_VaccinesLabs_L1_to_L9_OR",
    13: "Religion",
    14: "About_OtherDrugs_CloroquinaORIvermectna",
}

# Nomes das categorias 1/3/5 vem em branco na coluna "Broad Categories" da aba
# de categorias amplas (as celulas repetem o numero). Recuperados da aba de
# subcategorias / do proprio nome da coluna agregada.
NOME_FALLBACK = {
    1: "Politics",
    3: "Restrictive policies",
    5: "Anti-vaccine people",
}

# Traducao PT-BR das categorias amplas, para o texto da dissertacao. O prompt
# do rotulador usa o nome em INGLES (identico ao paper) para nao introduzir
# deriva semantica na traducao.
NOME_PT = {
    1: "Politica",
    2: "Criancas",
    3: "Politicas restritivas",
    4: "Desvantagens das vacinas",
    5: "Pessoas anti-vacina",
    6: "Internacional",
    7: "Vantagens das vacinas",
    8: "Riscos da COVID",
    9: "Fontes de desinformacao",
    10: "Fontes de informacao",
    11: "Ciencia",
    12: "Tipos de vacina / laboratorios",
    13: "Religiao",
    14: "Outras drogas",
}


def _num(v):
    """
    Converte 'Category number' para int; devolve None em '5 and 6', NaN etc.
    A coluna vem como float no xlsx (1.0, 2.0), dai o float() antes do int().
    """
    try:
        return int(float(str(v).strip()))
    except (TypeError, ValueError):
        return None


def extrai(xlsx=XLSX):
    amplas = pd.read_excel(xlsx, "Table broad categories")
    subs = pd.read_excel(xlsx, "Table subcategories")
    gab = pd.read_excel(xlsx, "Spreadsheet 1")

    categorias = []
    for _, linha in amplas.iterrows():
        numero = _num(linha["Category number"])
        if numero is None or numero not in COLUNA_AGREGADA:
            continue  # linhas de cabecalho (Tweet_ProVax/AntiVax) e ruido

        coluna = COLUNA_AGREGADA[numero]
        nome = str(linha["Broad Categories"]).strip()
        if nome == str(numero) or nome in ("nan", ""):
            nome = NOME_FALLBACK[numero]

        # Subcategorias: so as que pertencem exclusivamente a esta categoria
        # ampla (numero puro). As de fronteira ("5 and 6") viram nota.
        proprias, fronteira = [], []
        for _, s in subs.iterrows():
            n_s = _num(s["Category number"])
            refinada = str(s["Refined categories"]).strip()
            if refinada in ("nan", "", str(numero)):
                continue
            alvo = proprias if n_s == numero else None
            if alvo is None:
                # "5 and 6", "5 and 1", "5 and 2": conta para as duas pontas
                if n_s is None and str(numero) in str(s["Category number"]).split(" and "):
                    alvo = fronteira
                else:
                    continue
            alvo.append({
                "refinada": refinada,
                "coluna": str(s["Category names"]).strip(),
                "total": None if pd.isna(s["TOTAL"]) else int(s["TOTAL"]),
                "pro": None if pd.isna(s["TOTAL_ProVax"]) else int(s["TOTAL_ProVax"]),
                "anti": None if pd.isna(s["TOTAL_AntiVax"]) else int(s["TOTAL_AntiVax"]),
            })

        categorias.append({
            "numero": numero,
            "nome_en": nome,
            "nome_pt": NOME_PT[numero],
            "coluna": coluna,
            "total_publicado": int(linha["TOTAL"]),
            "pro_publicado": int(linha["TOTAL_ProVax"]),
            "anti_publicado": int(linha["TOTAL_AntiVax"]),
            "total_no_gabarito": int(gab[coluna].sum()),
            "subcategorias": proprias,
            "subcategorias_fronteira": fronteira,
        })

    categorias.sort(key=lambda c: c["numero"])
    return categorias, gab


def confere_totais(categorias):
    """O total da coluna no gabarito TEM de bater com o total publicado."""
    problemas = [
        f"  cat {c['numero']} ({c['nome_en']}): publicado={c['total_publicado']} "
        f"gabarito={c['total_no_gabarito']} coluna={c['coluna']}"
        for c in categorias
        if c["total_publicado"] != c["total_no_gabarito"]
    ]
    if problemas:
        raise SystemExit(
            "[erro] divergencia entre a Tabela 5 publicada e a aba do gabarito:\n"
            + "\n".join(problemas)
        )
    if not categorias:
        raise SystemExit("[erro] nenhuma categoria extraida — o layout do xlsx mudou?")
    print(f"[ok] {len(categorias)}/{len(COLUNA_AGREGADA)} categorias conferem "
          f"com os totais publicados (Tabela 5)")


def escreve_json(categorias, gab, destino):
    doc = {
        "versao": VERSAO,
        "fonte": "suplementar_rotulos.xlsx (Apendice A, Verjovsky et al. 2023)",
        "n_gabarito": int(len(gab)),
        "stance": {
            "coluna_pro": "Tweet_ProVax",
            "coluna_anti": "Tweet_AntiVax",
            "n_pro": int(gab["Tweet_ProVax"].sum()),
            "n_anti": int(gab["Tweet_AntiVax"].sum()),
            "n_nenhum": int(((gab["Tweet_ProVax"] != 1) & (gab["Tweet_AntiVax"] != 1)).sum()),
        },
        "categorias": categorias,
    }
    destino.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return doc


def escreve_md(doc, destino):
    L = [
        f"# Codebook do eixo B ({doc['versao']}) — gerado, nao editar a mao",
        "",
        "> Extraido de `suplementar_rotulos.xlsx` por `pipeline/extrai_codebook.py`.",
        "> Toda definicao vem do material suplementar do paper; os totais sao os",
        "> publicados na Tabela 5 e foram conferidos contra a aba do gabarito.",
        "",
        "## Stance",
        "",
        f"- `Tweet_ProVax` = {doc['stance']['n_pro']} | `Tweet_AntiVax` = "
        f"{doc['stance']['n_anti']} | nenhum dos dois = {doc['stance']['n_nenhum']}"
        f" | total = {doc['n_gabarito']}",
        "- Sao mutuamente exclusivos no gabarito (0 tweets com ambos).",
        "",
        "## Categorias amplas (14 — nao 11; ver nota)",
        "",
        "> O corpo do preprint fala em 11 categorias; o suplemento numera **14**.",
        "> Seguimos o suplemento, que e o dado.",
        "",
        "| # | Categoria (paper) | PT-BR | Coluna do gabarito | Total | Pro | Anti |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for c in doc["categorias"]:
        L.append(
            f"| {c['numero']} | {c['nome_en']} | {c['nome_pt']} | `{c['coluna']}` | "
            f"{c['total_publicado']} | {c['pro_publicado']} | {c['anti_publicado']} |"
        )
    L += ["", "## Subcategorias (o que cada categoria abrange)", ""]
    for c in doc["categorias"]:
        L.append(f"### {c['numero']}. {c['nome_en']} ({c['nome_pt']})")
        L.append("")
        if not c["subcategorias"] and not c["subcategorias_fronteira"]:
            L += ["_Sem subcategorias no suplemento (categoria atomica)._", ""]
            continue
        for s in c["subcategorias"]:
            L.append(f"- {s['refinada']} — `{s['coluna']}` (n={s['total']}, "
                     f"pro={s['pro']}, anti={s['anti']})")
        for s in c["subcategorias_fronteira"]:
            L.append(f"- _(fronteira)_ {s['refinada']} — `{s['coluna']}` (n={s['total']})")
        L.append("")
    destino.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--xlsx", default=str(XLSX))
    ap.add_argument("--out", default=str(SAIDA))
    args = ap.parse_args()

    xlsx = pathlib.Path(args.xlsx)
    if not xlsx.exists():
        raise SystemExit(f"[erro] suplemento nao encontrado: {xlsx}")
    saida = pathlib.Path(args.out)

    categorias, gab = extrai(xlsx)
    confere_totais(categorias)

    doc = escreve_json(categorias, gab, saida / f"codebook_{VERSAO}.json")
    escreve_md(doc, saida / "CODEBOOK.md")

    n_sub = sum(len(c["subcategorias"]) for c in categorias)
    print(f"[ok] {len(categorias)} categorias amplas, {n_sub} subcategorias proprias")
    print(f"[ok] gabarito: {doc['n_gabarito']} tweets "
          f"({doc['stance']['n_pro']} pro / {doc['stance']['n_anti']} anti / "
          f"{doc['stance']['n_nenhum']} nenhum)")
    print(f"[ok] escrito: {saida / f'codebook_{VERSAO}.json'}")
    print(f"[ok] escrito: {saida / 'CODEBOOK.md'}")


if __name__ == "__main__":
    sys.exit(main())
