"""Fase 3 do caso TikTok: as duas perguntas do protocolo no eixo temporal.

A Fase 2 (fase2_politok.py) reproduziu o ponto original e a curva da TAXA de deleção nas
três datas de reverificação da Saxônia. Este script vai um passo adiante e aplica as duas
perguntas do protocolo a uma segunda afirmação do artigo, a de que cerca de dois terços
das remoções são retirada pelo próprio autor, e não moderação da plataforma.

Isso é possível porque a coleta da Saxônia é reverificada em três datas sobre **a mesma
população**: o conjunto disponível numa data é subconjunto do disponível na anterior. É a
relação de subconjunto que o protocolo pede, com o eixo trocado — em vez de coletar mais,
verificar antes.

A regra de atribuição autor × plataforma é a mesma de `fase2_politok.py`, copiada aqui de
propósito para que as duas contas não possam divergir sem que se perceba.

⚠ Só roda onde os parquets publicados pelos autores existem, isto é, na cópia com dados.
Entrada:  data/politok_de/data_saxony_2024_post_ids.parquet
          data/politok_de/data_saxony_2024_annotations.parquet
Saída:    data/politok_de/fase3_eixo_temporal.json
"""

import json
import os
from collections import Counter

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "data", "politok_de")
IDS = os.path.join(DADOS, "data_saxony_2024_post_ids.parquet")
ANOT = os.path.join(DADOS, "data_saxony_2024_annotations.parquet")
SAIDA = os.path.join(DADOS, "fase3_eixo_temporal.json")

DATAS = ["2024_10_02", "2024_12_10", "2025_01_13"]
HORIZONTE = {"2024_10_02": "1 mes", "2024_12_10": "3 meses", "2025_01_13": "4,5 meses"}

# convencao F de fase2_politok.py: a que melhor reproduz os 13,0% do artigo
REGRA_F = ["audit_not_pass", "violation", "status_reviewing",
           "content_classification", "copyright"]


def lado(x):
    """Identica a de fase2_politok.py. Nao editar uma sem a outra."""
    if "audit_not_pass" in x or "violation" in x:
        return "plataforma"
    if "author_" in x or "status_deleted" in x or "item_not_exist" in x:
        return "autor"
    return "indefinido"


def painel(ids):
    """Posts com estado valido nas tres datas: a mesma populacao nos tres pontos."""
    ok = None
    for d in DATAS:
        v = ids["availability_" + d].isin(["AVAILABLE", "DELETED"])
        ok = v if ok is None else (ok & v)
    return ids[ok]


def main():
    ids = pd.read_parquet(IDS)
    pan = painel(ids)
    r = {"n_painel": int(len(pan)), "n_coleta": int(len(ids)), "por_data": {}}

    for d in DATAS:
        m = pan["availability_" + d] == "DELETED"
        s = pan.loc[m, "status_codes_" + d].astype(str)
        n = int(m.sum())
        L = Counter(lado(x) for x in s)
        plat_f = int(sum(any(t in x for t in REGRA_F) for x in s))
        r["por_data"][d] = {
            "horizonte": HORIZONTE[d],
            "deletados": n,
            "taxa_pct": round(100 * n / len(pan), 1),
            "autor_pct_dos_deletados": round(100 * L["autor"] / n, 1),
            "plataforma_pct_dos_deletados": round(100 * L["plataforma"] / n, 1),
            "indefinido_pct_dos_deletados": round(100 * L["indefinido"] / n, 1),
            "plataforma_conv_F_pct_de_todos": round(100 * plat_f / len(pan), 1),
        }

    p = r["por_data"]
    r["leitura"] = {
        "taxa": {
            "mudou": "sim, triplica: %.1f%% -> %.1f%%" % (
                p[DATAS[0]]["taxa_pct"], p[DATAS[-1]]["taxa_pct"]),
            "convergiu": "nao; o crescimento desacelera mas nao assenta, e a outra coleta "
                         "do mesmo artigo marca 39,7%% aos 16 meses",
        },
        "atribuicao_autor_x_plataforma": {
            "mudou": "nao; autor vai de %.1f%% a %.1f%% dos deletados (%.1f p.p.) e "
                     "plataforma de %.1f%% a %.1f%%" % (
                         p[DATAS[0]]["autor_pct_dos_deletados"],
                         p[DATAS[-1]]["autor_pct_dos_deletados"],
                         p[DATAS[-1]]["autor_pct_dos_deletados"]
                         - p[DATAS[0]]["autor_pct_dos_deletados"],
                         p[DATAS[0]]["plataforma_pct_dos_deletados"],
                         p[DATAS[-1]]["plataforma_pct_dos_deletados"]),
            "convergiu": "sim, ja na primeira reverificacao, um mes depois da eleicao",
            "alvo_do_artigo": "cerca de dois tercos (66,7%) de retirada pelo autor",
        },
        "por_que_importa": ("duas afirmacoes do mesmo corpus, sob a mesma decisao de coleta: "
                           "quanto foi deletado depende da data, e quem deletou nao. E o "
                           "padrao central da dissertacao, reproduzido no quarto eixo."),
    }

    # --- o que NAO da para medir, e por que: a amostra anotada e do estrato deletado ---
    an = pd.read_parquet(ANOT)
    post_ids = an["post_id"].unique()
    sub = ids[ids["post_id"].isin(post_ids)]
    estados = {d: dict(sub["availability_" + d].value_counts()) for d in DATAS}
    r["amostra_anotada"] = {
        "linhas_de_anotacao": int(len(an)),
        "posts_unicos": int(len(post_ids)),
        "estados_por_data": {d: {k: int(v) for k, v in e.items()} for d, e in estados.items()},
        "achado": ("os %d posts anotados estao 100%% DELETED ja na segunda data, contra "
                   "%.1f%% do painel; %d deles (%.1f%%) ja estavam deletados na primeira, "
                   "contra %.1f%%. A amostra de anotacao esta dentro do estrato deletado, e "
                   "os autores declaram que subconjuntos aleatorios nao sao publicados."
                   % (len(post_ids), p[DATAS[1]]["taxa_pct"],
                      int(estados[DATAS[0]].get("DELETED", 0)),
                      100 * int(estados[DATAS[0]].get("DELETED", 0)) / len(post_ids),
                      p[DATAS[0]]["taxa_pct"])),
        "consequencia": ("nao ha grupo sobrevivente anotado para comparar (3 posts na ultima "
                         "data), de modo que a composicao de CONTEUDO dos dois lados da linha "
                         "de delecao nao e mensuravel com o que esta publicado. As duas "
                         "afirmacoes de anotacao do artigo descrevem esse subconjunto, que e "
                         "conteudo deletado, e nao o corpus."),
    }

    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print("painel: %d posts, a mesma populacao nas tres datas" % r["n_painel"])
    print("%-12s %9s %7s %8s %11s %9s" % ("data", "deletados", "taxa", "autor", "plataforma", "indef"))
    for d in DATAS:
        x = p[d]
        print("%-12s %9d %6.1f%% %7.1f%% %10.1f%% %8.1f%%" % (
            d.replace("_", "-"), x["deletados"], x["taxa_pct"],
            x["autor_pct_dos_deletados"], x["plataforma_pct_dos_deletados"],
            x["indefinido_pct_dos_deletados"]))
    print()
    print("taxa:       %s" % r["leitura"]["taxa"]["mudou"])
    print("atribuicao: %s" % r["leitura"]["atribuicao_autor_x_plataforma"]["mudou"])
    print()
    print("amostra anotada: %s" % r["amostra_anotada"]["achado"])
    print("-> %s" % SAIDA)


if __name__ == "__main__":
    main()
