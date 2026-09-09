# -*- coding: utf-8 -*-
"""Aplica o rotulador congelado a amostra do universo (§6.2 do PRE_REGISTRO).

Importa o prompt e o parser de `rotula_stance.py` -- nao os reescreve. Se o
prompt daquele arquivo mudar, este muda junto, e e isso que garante que a
matriz de confusao medida nos 210 descreve ESTE rotulador.

Economia declarada: rotula os **textos distintos** (2.762) e propaga para os
5.000 itens. E a mesma regra que o gabarito humano usou na fase 2 -- o stance de
um RT sem comentario e propriedade do texto, nao da conta. Corta ~45% do custo.

Uso:
    python analise/rotula_universo.py --dry-run
    python analise/rotula_universo.py
"""
import argparse
import csv
import io
import json
import os
import pathlib
import re
import sys
import time
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PROJETO = RAIZ.parents[1]
sys.path.insert(0, str(PROJETO / "casos" / "vacinas"))
sys.path.insert(0, str(RAIZ / "analise"))

from core import orcamento as orc_mod                     # noqa: E402
from core.llm import cliente                              # noqa: E402
from rotula_stance import (SISTEMA, MODELO, MAX_SAIDA_POR_TWEET,   # noqa: E402
                           bloco_do_tweet, extrai_json)

STANCE = RAIZ / "data" / "repl" / "compos2014" / "stance"
AMOSTRA = STANCE / "amostra_universo_stance.json"
SAIDA = STANCE / "rotulos_universo_LLM.csv"
LOTE = 15


def norm_texto(t):
    t = (t or "").lower()
    t = re.sub(r"^rt @[a-z0-9_]+:\s*", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip()


def host_do_link(links):
    """Mesmo campo `host1` que o gabarito mostrava, quando da para extrair."""
    if not links:
        return ""
    m = re.search(r"https?://([^/\s\"']+)", links)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--lote", type=int, default=LOTE)
    args = ap.parse_args()

    doc = json.loads(AMOSTRA.read_text(encoding="utf-8"))
    itens = doc["itens"]
    print("amostra congelada  n=%d, sha=%s" % (doc["n_total"], doc["sha256_12_dos_ids"]))

    # um representante por texto distinto
    grupos = {}
    for it in itens:
        grupos.setdefault(norm_texto(it["texto"]), []).append(it)
    reps = [v[0] for v in grupos.values()]
    for r in reps:
        r["host1"] = host_do_link(r.get("links", ""))
    print("textos distintos ... %d (de %d itens)" % (len(reps), len(itens)))

    lotes = [reps[k:k + args.lote] for k in range(0, len(reps), args.lote)]
    cli = cliente()

    total_ent = 0
    for lote in lotes:
        total_ent += cli.messages.count_tokens(
            model=MODELO, system=SISTEMA,
            messages=[{"role": "user",
                       "content": "Rotule os %d tweets a seguir.\n\n" % len(lote)
                       + "\n\n---\n\n".join(bloco_do_tweet(x) for x in lote)}]
        ).input_tokens

    saida_pior = len(reps) * MAX_SAIDA_POR_TWEET
    custo = orc_mod.custo_usd(MODELO, entrada=total_ent, saida=saida_pior, batch=False)
    orc = orc_mod.Orcamento()
    print("lotes .............. %d" % len(lotes))
    print("entrada ............ %s tokens" % f"{total_ent:,}")
    print("custo (pior caso) .. US$ %.4f" % custo)
    print("saldo .............. US$ %.2f -> US$ %.2f" % (orc.saldo, orc.saldo - custo))

    if args.dry_run:
        print("\n[dry-run] nada foi enviado.")
        return

    ident = orc.reservar(usd=custo, descricao="stance ituassu: universo 5k (2.762 textos)",
                         detalhe={"textos": len(reps), "itens": len(itens),
                                  "lotes": len(lotes), "modelo": MODELO,
                                  "sha_amostra": doc["sha256_12_dos_ids"]})
    print("\nreserva %s feita. enviando...\n" % ident)

    por_texto, ent_real, sai_real, k = {}, 0, 0, 0
    try:
        for k, lote in enumerate(lotes, 1):
            r = cli.messages.create(
                model=MODELO, max_tokens=len(lote) * MAX_SAIDA_POR_TWEET,
                system=SISTEMA,
                messages=[{"role": "user",
                           "content": "Rotule os %d tweets a seguir.\n\n" % len(lote)
                           + "\n\n---\n\n".join(bloco_do_tweet(x) for x in lote)}])
            ent_real += r.usage.input_tokens
            sai_real += r.usage.output_tokens
            dados = extrai_json(r.content[0].text)
            if len(dados) != len(lote):
                raise ValueError("lote %d: esperava %d, veio %d" % (k, len(lote), len(dados)))
            for it, d in zip(lote, dados):
                if str(d.get("id")) != it["id_tweet"]:
                    raise ValueError("lote %d: id fora de ordem" % k)
                por_texto[norm_texto(it["texto"])] = {
                    "cidadao": d.get("cidadao", ""), "stance": d.get("stance", ""),
                    "confianca": str(d.get("confianca", "")), "notas": d.get("notas", "") or ""}
            if k % 20 == 0 or k == len(lotes):
                print("  lote %3d/%d" % (k, len(lotes)))
            time.sleep(0.25)
    except Exception as e:
        if ent_real or sai_real:
            orc.concilia(ident, modelo=MODELO, entrada=ent_real, saida=sai_real, batch=False)
            print("[falhou no lote %d] consumo lancado: %s / %s"
                  % (k, f"{ent_real:,}", f"{sai_real:,}"))
        else:
            orc.libera(ident, motivo="falhou antes de gastar")
        raise

    orc.concilia(ident, modelo=MODELO, entrada=ent_real, saida=sai_real, batch=False)

    with io.open(SAIDA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id_tweet", "data_brt", "cidadao", "stance",
                                           "confianca", "notas", "origem"])
        w.writeheader()
        for it in itens:
            ch = norm_texto(it["texto"])
            d = por_texto[ch]
            w.writerow({"id_tweet": it["id_tweet"], "data_brt": it["data_brt"],
                        **d,
                        "origem": "manual" if grupos[ch][0]["id_tweet"] == it["id_tweet"]
                                  else "propagado"})

    print("\ngravado: %s (%d itens)" % (SAIDA, len(itens)))
    print("gasto real: entrada %s / saida %s" % (f"{ent_real:,}", f"{sai_real:,}"))
    print(orc.resumo())


if __name__ == "__main__":
    main()
