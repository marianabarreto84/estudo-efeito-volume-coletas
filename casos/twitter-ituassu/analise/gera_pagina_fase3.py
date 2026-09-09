# -*- coding: utf-8 -*-
"""Fase 3 do teste cego: por que NDA? -- pagina AUTONOMA (9/set/2026).

Por que separada, e nao mais uma aba da `rotulagem_teste.html`:
o arquivo anterior tem nome e caminho fixos, e o navegador serve `file://`
do cache -- a Mariana clicou na aba "3 - por que NDA" e ela nao abriu, muito
provavelmente por isso. Nome novo nao tem cache possivel. De quebra, a fase 2
esta fechada e exportada, entao a fase 3 nao precisa carregar aquele estado.

O QUE ELA RESOLVE
-----------------
A regra de ouro do codebook ("na duvida entre um lado e NDA, e NDA com
confianca 1") colapsou a confianca de TODO NDA numa constante: 150 de 150 em
conf 1, zero em 2 ou 3. Com isso `confianca >= 2` deixou de ser um teste de
robustez e virou, na pratica, "itens com lado" (26 itens: 19 EA + 7 ED, zero
NDA) -- um kappa de 2 classes, que nao e o que o pre-registro §4 pediu.

Esta fase separa os dois NDA que o codebook fundia:
  sem_lado (conf 3) -- o tweet nao expressa preferencia: pesquisa, placar,
                       noticia sem valencia;
  ambiguo  (conf 2) -- inclina para NDA, mas nao e obvio;
  indeciso (conf 1) -- pode ter lado e nao se conseguiu determinar: ironia
                       ambigua, link morto, texto truncado.

Nao toca na amostra: mesmos 210, mesma semente, mesmo hash. Nao acrescenta
tweet nenhum -- acrescentar itens escolhidos por "confianca provavel" seria
selecionar pela variavel de interesse, que e o erro que a propria dissertacao
documenta.

Uso:  PYTHONUTF8=1 python analise/gera_pagina_fase3.py [caminho_do_csv]
"""
import csv
import io
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANCE = os.path.join(RAIZ, "data", "repl", "compos2014", "stance")
PADRAO = os.path.join(os.path.expanduser("~"), "Downloads",
                      "gold_stance_teste_MARIANA(1).csv")
SAIDA = os.path.join(STANCE, "rotulagem_fase3.html")
HASH_AMOSTRA = "dc8ee39ff69b"

CAMPOS = ["n", "id_tweet", "data_brt", "autor", "nome_autor", "verificado",
          "seguidores", "tweets_do_autor", "eh_retweet", "autor_original",
          "idioma", "texto", "link1", "host1", "hashtags",
          "cidadao", "stance", "confianca", "notas"]


def norm_texto(t):
    t = (t or "").lower()
    t = re.sub(r"^rt @[a-z0-9_]+:\s*", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip()


def main():
    origem = sys.argv[1] if len(sys.argv) > 1 else PADRAO
    with io.open(origem, encoding="utf-8-sig", newline="") as fh:
        linhas = list(csv.DictReader(fh))

    assert len(linhas) == 210, "esperava 210 linhas, veio %d" % len(linhas)
    falta = [r["n"] for r in linhas if not r["stance"].strip()]
    assert not falta, "ha itens sem stance: %s" % falta[:10]

    # grupos de texto entre os NDA, em ordem de primeira aparicao
    grupos = OrderedDict()
    for r in linhas:
        if r["stance"].strip() == "NDA":
            grupos.setdefault(norm_texto(r["texto"]), []).append(r)

    itens = []
    for gi, (chave, membros) in enumerate(grupos.items()):
        itens.append({
            "gid": gi,
            "ids": [m["id_tweet"] for m in membros],
            "ns": [m["n"] for m in membros],
            "autores": [m["autor"] for m in membros],
            "n_membros": len(membros),
            **{c: membros[0][c] for c in
               ("n", "id_tweet", "data_brt", "autor", "nome_autor",
                "texto", "host1", "hashtags", "cidadao", "notas")}
        })

    # o CSV inteiro viaja junto, para a exportacao sair com as 210 linhas
    todos = [{c: r.get(c, "") for c in CAMPOS} for r in linhas]

    tpl = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "_template_fase3.html"), encoding="utf-8").read()
    html = (tpl
            .replace("/*__GRUPOS__*/", json.dumps(itens, ensure_ascii=False))
            .replace("/*__TODOS__*/", json.dumps(todos, ensure_ascii=False))
            .replace("__HASH__", HASH_AMOSTRA))

    tmp = SAIDA + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(html)
    os.replace(tmp, SAIDA)

    nda = sum(len(v) for v in grupos.values())
    print("origem ........... %s" % origem)
    print("NDA .............. %d itens em %d grupos de texto" % (nda, len(grupos)))
    print("   (%d decisoes a menos que item a item)" % (nda - len(grupos)))
    print("gravado em ....... %s" % SAIDA)


if __name__ == "__main__":
    main()
