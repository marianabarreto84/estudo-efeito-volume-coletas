# -*- coding: utf-8 -*-
"""Gera a pagina de revisao das divergencias do dev (rodada 2 da Mariana).

Uso:
    python analise/gera_pagina_revisao.py

Compara o gabarito humano do dev (gold_stance_dev_MARIANA.csv) com a pre-anotacao
automatica (prerotulagem_dev_LLM.csv), seleciona os itens em que os dois discordam --
no stance ou no portao `cidadao` -- e emite
data/repl/compos2014/stance/revisao_dev.html, onde a anotadora reve cada um, com o
motivo do lado automatico a vista, e justifica por escrito a decisao final.

A revisao e, por construcao, ANCORADA: ela ja viu o outro rotulo. Isso e aceitavel no
dev (que calibra, nao mede) e esta declarado no DECISOES_ROTULADOR.md. O teste de 210
nao passa por nada disso.
"""
import csv
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
STANCE = RAIZ / "data" / "repl" / "compos2014" / "stance"


def le(nome):
    return list(csv.DictReader((STANCE / nome).open(encoding="utf-8-sig")))


def tipo_da_divergencia(h, a):
    if {h["stance"], a["stance"]} == {"EA", "ED"}:
        return "divergência de polo"
    if h["stance"] != a["stance"]:
        return "lado × NDA"
    return "só o portão cidadão"


def main():
    humano = {r["id_tweet"]: r for r in le("gold_stance_dev_MARIANA.csv")}
    auto = le("prerotulagem_dev_LLM.csv")
    porques = json.loads((STANCE / "justificativas_auto_dev.json").read_text(encoding="utf-8"))
    split = json.loads((STANCE / "split_stance.json").read_text(encoding="utf-8"))

    itens = []
    for a in auto:
        h = humano[a["id_tweet"]]
        if h["stance"] == a["stance"] and h["cidadao"] == a["cidadao"]:
            continue
        itens.append({
            "ordem_dev": a["ordem_dev"], "id_tweet": a["id_tweet"], "autor": h["autor"],
            "nome_autor": h["nome_autor"], "verificado": h["verificado"], "seguidores": h["seguidores"],
            "tweets_do_autor": h["tweets_do_autor"], "eh_retweet": h["eh_retweet"],
            "texto": h["texto"], "host1": h["host1"],
            "cidadao_v1": h["cidadao"], "stance_v1": h["stance"], "confianca_v1": h["confianca"],
            "notas_v1": h["notas"],
            "cidadao_auto": a["cidadao"], "stance_auto": a["stance"], "confianca_auto": a["confianca"],
            "tipo": tipo_da_divergencia(h, a),
            "porque": porques.get(a["ordem_dev"], ""),
        })

    ordem = {"divergência de polo": 0, "lado × NDA": 1, "só o portão cidadão": 2}
    itens.sort(key=lambda x: (ordem[x["tipo"]], int(x["ordem_dev"])))
    faltando = [x["ordem_dev"] for x in itens if not x["porque"]]
    if faltando:
        raise SystemExit(f"sem justificativa automática para os itens {faltando}")

    html = (RAIZ / "analise" / "_template_revisao.html").read_text(encoding="utf-8")
    html = html.replace("/*__ITENS__*/", json.dumps(itens, ensure_ascii=False))
    html = html.replace("__SHA__", split["sha256_12_dos_ids"])
    saida = STANCE / "revisao_dev.html"
    saida.write_text(html, encoding="utf-8")

    from collections import Counter
    print(f"OK -> {saida}")
    print("   divergências:", len(itens), dict(Counter(x["tipo"] for x in itens)))


if __name__ == "__main__":
    main()
