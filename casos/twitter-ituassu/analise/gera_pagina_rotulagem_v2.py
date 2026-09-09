# -*- coding: utf-8 -*-
"""Gera a pagina de rotulagem do teste cego em DUAS FASES (pedido da Mariana, 9/set/2026).

Diferencas para a `rotulagem_teste.html` original:

  1. FASE 1 -- portao `cidadao` para os 210, de uma vez so. O portao e propriedade
     da CONTA que publicou, e nao do texto, entao continua item a item.
  2. FASE 2 -- `stance` + `confianca` por GRUPO DE TEXTO. Textos identicos (RTs do
     mesmo original vindos de contas diferentes) sao decididos uma vez e o rotulo
     e PROPAGADO para o grupo inteiro. Sao 179 grupos em vez de 210 itens.

A chave de grupo e exatamente a `norm_texto` do sorteio congelado
(`analise/amostra_stance_humana.py`): minusculas, sem o prefixo `RT @x:`, sem URL,
sem acento, espacos colapsados. Nao se inventa criterio novo aqui.

⚠ CONSEQUENCIA METODOLOGICA, registrada de proposito:
  o codebook mandava "texto repetido: rotule de novo, sem procurar o anterior", e
  era isso que fazia das duplicatas uma medida de consistencia intra-codificador.
  Com a propagacao essa medida deixa de existir DENTRO do teste -- ela passa a
  viver so no RETESTE de 40 itens, que e onde foi desenhada para viver. O kappa
  "com duplicatas" fica inflado por construcao, e o numero primario passa a ser o
  "sem duplicatas". Ver DECISOES_ROTULADOR.md.

O trabalho ja feito e preservado: a pagina semeia o estado a partir do CSV que a
Mariana exportou, e usa a MESMA chave de localStorage da pagina anterior.

Uso:  PYTHONUTF8=1 python analise/gera_pagina_rotulagem_v2.py
"""
import csv
import io
import json
import os
import re
import unicodedata
from collections import OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANCE = os.path.join(RAIZ, "data", "repl", "compos2014", "stance")
CSV_ENTRADA = os.path.join(RAIZ, "..", "..", "gold_stance_teste_MARIANA.csv")
SAIDA = os.path.join(STANCE, "rotulagem_teste.html")
HASH_AMOSTRA = "dc8ee39ff69b"

CAMPOS = ["n", "id_tweet", "data_brt", "autor", "nome_autor", "verificado",
          "seguidores", "tweets_do_autor", "eh_retweet", "autor_original",
          "idioma", "texto", "link1", "host1", "hashtags",
          "cidadao", "stance", "confianca", "notas"]


def norm_texto(t):
    """Chave de duplicata: identica a do sorteio congelado."""
    t = (t or "").lower()
    t = re.sub(r"^rt @[a-z0-9_]+:\s*", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip()


def main():
    with io.open(CSV_ENTRADA, encoding="utf-8-sig", newline="") as fh:
        linhas = list(csv.DictReader(fh))
    assert len(linhas) == 210, len(linhas)

    # --- grupos de texto, em ordem de primeira aparicao -----------------
    grupos = OrderedDict()
    for r in linhas:
        grupos.setdefault(norm_texto(r["texto"]), []).append(r)

    itens, semente = [], {}
    for gi, (chave, membros) in enumerate(grupos.items()):
        for r in membros:
            itens.append({
                "gid": gi,
                "gsize": len(membros),
                **{c: r[c] for c in CAMPOS if c not in ("cidadao", "stance", "confianca", "notas")}
            })
            marcado = {k: r[k].strip() for k in ("cidadao", "stance", "confianca", "notas")}
            if any(marcado.values()):
                semente[r["id_tweet"]] = marcado

    # --- conflitos ja existentes dentro de um grupo ---------------------
    conflitos = {}
    for gi, (chave, membros) in enumerate(grupos.items()):
        vistos = {}
        for r in membros:
            s = r["stance"].strip()
            if s:
                vistos.setdefault(s, []).append(r["n"])
        if len(vistos) > 1:
            conflitos[gi] = vistos

    # ordem de exibicao da fase 2: um representante por grupo
    ordem_grupos = list(range(len(grupos)))

    tpl = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "_template_rotulagem_v2.html"),
                  encoding="utf-8").read()
    html = (tpl
            .replace("/*__ITENS__*/", json.dumps(itens, ensure_ascii=False))
            .replace("/*__SEMENTE__*/", json.dumps(semente, ensure_ascii=False))
            .replace("/*__CONFLITOS__*/", json.dumps(conflitos, ensure_ascii=False))
            .replace("/*__GRUPOS__*/", json.dumps(ordem_grupos))
            .replace("__HASH__", HASH_AMOSTRA))

    tmp = SAIDA + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(html)
    os.replace(tmp, SAIDA)

    print("itens ............ %d" % len(itens))
    print("grupos de texto .. %d  (economia: %d rotulagens de stance)"
          % (len(grupos), len(itens) - len(grupos)))
    print("ja rotulados ..... %d" % len(semente))
    print("conflitos ........ %d %s" % (len(conflitos), list(conflitos) or ""))
    print("gravado em ....... %s" % SAIDA)


if __name__ == "__main__":
    main()
