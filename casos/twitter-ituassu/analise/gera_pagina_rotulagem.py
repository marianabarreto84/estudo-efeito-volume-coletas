# -*- coding: utf-8 -*-
"""Gera a pagina local de rotulagem do eixo stance (lote do dev).

Uso:
    python analise/gera_pagina_rotulagem.py

Le o gold set congelado + o split + a pre-anotacao automatica e emite
data/repl/compos2014/stance/rotulagem_dev.html -- uma pagina estatica, sem rede,
que roda por file:// e exporta o CSV no mesmo formato do gold set.

A pre-anotacao automatica vai embutida em base64 e so e revelada pela pagina
depois que a anotadora FECHA um lote de 20. E anteparo contra ver sem querer,
nao criptografia: quem abrir o fonte ve. O ponto e nao ancorar a leitura.
"""
import base64
import csv
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
STANCE = RAIZ / "data" / "repl" / "compos2014" / "stance"
LOTE = 20

CAMPOS = ["n", "id_tweet", "data_brt", "autor", "nome_autor", "verificado", "seguidores",
          "tweets_do_autor", "eh_retweet", "autor_original", "idioma", "texto", "link1",
          "host1", "hashtags", "cidadao", "stance", "confianca", "notas"]


def carrega(conjunto):
    rows = list(csv.DictReader((STANCE / "gold_stance_para_rotular.csv").open(encoding="utf-8-sig")))
    split = json.loads((STANCE / "split_stance.json").read_text(encoding="utf-8"))
    alvo = {str(i) for i in split[conjunto]}
    itens = [r for r in rows if r["id_tweet"] in alvo]
    assert len(itens) == len(split[conjunto]), (len(itens), len(split[conjunto]))
    pre = {}
    if conjunto == "dev":
        pre = {r["id_tweet"]: r for r in
               csv.DictReader((STANCE / "prerotulagem_dev_LLM.csv").open(encoding="utf-8-sig"))}
        assert len(pre) == len(itens)
    return itens, pre, split


def main():
    conjunto = sys.argv[1] if len(sys.argv) > 1 else "dev"
    if conjunto not in ("dev", "teste"):
        raise SystemExit("uso: gera_pagina_rotulagem.py [dev|teste]")
    itens, pre, split = carrega(conjunto)
    itens = [{k: r.get(k, "") for k in CAMPOS} for r in itens]
    segredo = ""
    if pre:
        segredo = base64.b64encode(json.dumps(
            {i: {"cidadao": p["cidadao"], "stance": p["stance"],
                 "confianca": p["confianca"], "notas": p["notas"]}
             for i, p in pre.items()}, ensure_ascii=False).encode("utf-8")).decode("ascii")

    fim = ("Exporte o CSV e me avise. O que vem depois e o teste cego de 210, "
           "que voce rotula sem ver nada meu."
           if conjunto == "dev" else
           "Exporte o CSV e me avise. Este e o conjunto que produz o numero: "
           "e contra ele que o rotulador automatico e medido, uma vez so.")

    html = (RAIZ / "analise" / "_template_rotulagem.html").read_text(encoding="utf-8")
    html = html.replace("/*__ITENS__*/", json.dumps(itens, ensure_ascii=False))
    html = html.replace("__SEGREDO__", segredo)
    html = html.replace("__LOTE__", str(LOTE))
    html = html.replace("__SHA__", split["sha256_12_dos_ids"])
    html = html.replace("__CONJUNTO__", conjunto)
    html = html.replace("__N__", str(len(itens)))
    html = html.replace("__FIM_TXT__", fim)
    html = html.replace("__SAIDA__", f"gold_stance_{conjunto}_MARIANA.csv")
    saida = STANCE / f"rotulagem_{conjunto}.html"
    saida.write_text(html, encoding="utf-8")
    reveal = "com revelacao por lote" if segredo else "SEM pre-anotacao (cego)"
    print(f"OK -> {saida}  ({len(itens)} itens, lotes de {LOTE}, {reveal})")


if __name__ == "__main__":
    main()
