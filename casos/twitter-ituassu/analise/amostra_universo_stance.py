# -*- coding: utf-8 -*-
"""Sorteia e CONGELA a amostra do universo para a estimativa corrigida (§6).

Espelha `amostra_stance_humana.py`: mesma populacao (janela 19-25/out do
`snapshot_hashtag.sqlite`), mesma alocacao proporcional por dia, mesma chave de
duplicata. So muda o tamanho (5.000) e a semente (20260909), ambos declarados
no PRE_REGISTRO §6.2 antes de rodar.

O script se recusa a re-sortear por cima de um sorteio ja congelado sem
--refazer, pela mesma razao do original: sorteio que muda depois de medido nao
e sorteio.

Uso:  PYTHONUTF8=1 python analise/amostra_universo_stance.py
"""
import argparse
import hashlib
import io
import json
import os
import pathlib
import random
import re
import sqlite3
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parents[1]
STANCE = RAIZ / "data" / "repl" / "compos2014" / "stance"
SAIDA = STANCE / "amostra_universo_stance.json"

# O snapshot vive na copia COM dados (o repo git nao versiona *.sqlite).
CANDIDATOS = [
    pathlib.Path(r"c:\Users\maria\Documents\dissertacao\casos\twitter-ituassu"
                 r"\data\repl\compos2014\snapshot_hashtag.sqlite"),
    RAIZ / "data" / "repl" / "compos2014" / "snapshot_hashtag.sqlite",
]

DIAS = ["2014-10-%d" % d for d in range(19, 26)]
N_TOTAL = 5000
SEED = 20260909


def norm_texto(t):
    t = (t or "").lower()
    t = re.sub(r"^rt @[a-z0-9_]+:\s*", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip()


def aloca_por_dia(cont, n):
    """Proporcional com maior resto (soma exata = n)."""
    tot = sum(cont.values())
    bruto = {d: n * c / tot for d, c in cont.items()}
    base = {d: int(v) for d, v in bruto.items()}
    resto = n - sum(base.values())
    for d in sorted(cont, key=lambda d: -(bruto[d] - base[d]))[:resto]:
        base[d] += 1
    return base


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refazer", action="store_true")
    args = ap.parse_args()

    if SAIDA.exists() and not args.refazer:
        d = json.loads(SAIDA.read_text(encoding="utf-8"))
        raise SystemExit(
            "[parado] ja existe sorteio congelado em %s\n"
            "         n=%d, semente=%s, sha=%s\n"
            "         use --refazer so se souber por que."
            % (SAIDA, d["n_total"], d["seed"], d["sha256_12_dos_ids"]))

    banco = next((c for c in CANDIDATOS if c.exists()), None)
    if banco is None:
        raise SystemExit("[erro] snapshot_hashtag.sqlite nao encontrado em:\n  "
                         + "\n  ".join(str(c) for c in CANDIDATOS))

    cx = sqlite3.connect(str(banco))
    cx.row_factory = sqlite3.Row
    q = ("SELECT id_tweet, data_brt, autor, nome_autor, status_verificado,"
         " num_seguidores, num_tweets, status_retweet, autor_original, texto,"
         " links, hashtags, idioma"
         " FROM tweets WHERE substr(data_brt,1,10) BETWEEN ? AND ?"
         " ORDER BY id_tweet")
    linhas = [dict(r) for r in cx.execute(q, (DIAS[0], DIAS[-1]))]
    cx.close()
    print("banco ............ %s" % banco)
    print("populacao ........ %d tweets (19-25/out)" % len(linhas))

    por_dia = {}
    for r in linhas:
        por_dia.setdefault(r["data_brt"][:10], []).append(r)
    cota = aloca_por_dia({d: len(v) for d, v in por_dia.items()}, N_TOTAL)
    print("cota por dia ..... " + ", ".join("%s=%d" % (d[-5:], cota[d]) for d in DIAS))

    rng = random.Random(SEED)
    amostra = []
    for d in DIAS:
        amostra += rng.sample(por_dia[d], cota[d])
    rng.shuffle(amostra)

    ids = [str(r["id_tweet"]) for r in amostra]
    sha = hashlib.sha256("|".join(ids).encode()).hexdigest()[:12]

    grupos = {}
    for r in amostra:
        grupos.setdefault(norm_texto(r["texto"]), []).append(str(r["id_tweet"]))
    repetidos = {k: v for k, v in grupos.items() if len(v) > 1}

    # sobreposicao com o gold ja rotulado a mao
    gold = STANCE / "gold_stance_teste_MARIANA.csv"
    ids_gold = set()
    if gold.exists():
        import csv
        with io.open(gold, encoding="utf-8-sig", newline="") as fh:
            ids_gold = {r["id_tweet"] for r in csv.DictReader(fh)}
    sobrep = len(set(ids) & ids_gold)

    doc = {
        "gerado_por": "analise/amostra_universo_stance.py",
        "prereg": "PRE_REGISTRO_stance.md §6.2",
        "populacao": {"snapshot": banco.name, "janela": [DIAS[0], DIAS[-1]],
                      "n_populacao": len(linhas)},
        "seed": SEED,
        "n_total": N_TOTAL,
        "cota_por_dia": cota,
        "sha256_12_dos_ids": sha,
        "grupos_de_texto": len(grupos),
        "itens_em_grupo_repetido": sum(len(v) for v in repetidos.values()),
        "sobreposicao_com_gold_210": sobrep,
        "ids": ids,
        "itens": [{"id_tweet": str(r["id_tweet"]), "data_brt": r["data_brt"],
                   "autor": r["autor"], "nome_autor": r["nome_autor"],
                   "verificado": str(r["status_verificado"] or 0),
                   "seguidores": str(r["num_seguidores"] or 0),
                   "tweets_do_autor": str(r["num_tweets"] or 0),
                   "eh_retweet": str(r["status_retweet"] or 0),
                   "autor_original": r["autor_original"] or "",
                   "idioma": r["idioma"] or "", "texto": r["texto"],
                   "links": r["links"] or "", "hashtags": r["hashtags"] or ""}
                  for r in amostra],
    }
    tmp = str(SAIDA) + ".tmp"
    io.open(tmp, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False))
    os.replace(tmp, str(SAIDA))

    print("grupos de texto .. %d (%d itens em grupo repetido)"
          % (len(grupos), doc["itens_em_grupo_repetido"]))
    print("sobrepoe o gold .. %d dos 210" % sobrep)
    print("sha256(ids)[:12] . %s" % sha)
    print("congelado em ..... %s" % SAIDA)


if __name__ == "__main__":
    main()
