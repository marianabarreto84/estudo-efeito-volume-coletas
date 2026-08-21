"""
Kit de rotulagem do eixo STANCE (EA/ED/NDA) — sorteio + congelamento do gold set.

O que faz
---------
1. Define a POPULACAO: snapshot_hashtag (#Eleicoes2014), janela 19-25/out/2014
   (n = 32.193) — a mesma janela do eixo midia, para que gold set e curva
   A(volume) falem da mesma populacao.
2. Sorteia n = 320 tweets, ALEATORIO, estratificado por dia (alocacao
   proporcional ao volume do dia, maior resto), seed fixa.
3. Congela o split dev/teste ANTES de qualquer chamada de LLM
   (110 dev / 210 teste, estratificado por dia) em `split_stance.json`.
4. Sorteia o subconjunto de RETESTE intracodificador (40 itens) — mede o TETO
   da tarefa, como no caso vacinas (la o teto foi 0,746).
5. Emite as planilhas prontas para preencher (CSV utf-8-sig, abre no Excel):
     - gold_stance_para_rotular.csv   (320 linhas, ordem embaralhada)
     - gold_stance_RETESTE.csv        (40 linhas, ordem diferente, sem rotulos)

Decisoes registradas (detalhe em data/repl/compos2014/stance/PRE_REGISTRO_stance.md)
------------------------------------------------------------------------------
  - Unidade = TWEET (como no artigo), nao autor.
  - Duplicatas de texto (RTs do mesmo original) sao MANTIDAS: sao peso real no
    universo. O script marca os grupos para que o kappa possa ser reportado com
    e sem deduplicacao (duplicata infla concordancia).
  - A planilha do humano NAO revela dev/teste (evita efeito de expectativa).
  - Idioma: nao ha filtro. ~4,5% da janela nao e 'pt'; o codebook manda rotular
    pelo sentido se compreensivel e NDA + nota caso contrario.
  - O host do 1o link vem do MESMO caminho canonico do eixo midia
    (campo `links`; se vazio, 1a URL do texto; encurtador resolvido pelo cache).

Uso:  PYTHONIOENCODING=utf-8 python -u analise/amostra_stance_humana.py
      (--refazer para sobrescrever um sorteio ja congelado)
"""
import argparse
import csv
import hashlib
import json
import pathlib
import random
import re
import sqlite3
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.extrai_links import links_efetivos
from core.resolve_midia import carrega_cache, classe_do_primeiro_link

D = pathlib.Path("data/repl/compos2014")
OUT = D / "stance"
SNAP = D / "snapshot_hashtag.sqlite"
CACHE_PATH = D / "expand_cache.sqlite"

DIAS = ["2014-10-19", "2014-10-20", "2014-10-21", "2014-10-22",
        "2014-10-23", "2014-10-24", "2014-10-25"]
N_TOTAL = 320
N_DEV = 110          # calibragem do prompt; o resto (210) e teste CEGO
N_RETESTE = 40
SEED = 20260818


def log(m):
    print(m, flush=True)


def norm_texto(t):
    """Chave de duplicata: minusculas, sem acento, sem URL, sem o prefixo 'RT @x:'."""
    t = (t or "").lower()
    t = re.sub(r"^rt @[a-z0-9_]+:\s*", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip()


def aloca_por_dia(contagens, n):
    """Alocacao proporcional com maior resto (soma exata = n)."""
    tot = sum(contagens.values())
    bruto = {d: n * c / tot for d, c in contagens.items()}
    base = {d: int(v) for d, v in bruto.items()}
    resto = n - sum(base.values())
    ordem = sorted(contagens, key=lambda d: bruto[d] - base[d], reverse=True)
    for d in ordem[:resto]:
        base[d] += 1
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refazer", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    split_path = OUT / "split_stance.json"
    if split_path.exists() and not args.refazer:
        log("JA CONGELADO: " + str(split_path))
        log("Refazer o sorteio invalida qualquer kappa ja medido. Use --refazer se e isso mesmo.")
        return 1

    cache = carrega_cache(CACHE_PATH)
    cx = sqlite3.connect(SNAP)
    cx.row_factory = sqlite3.Row

    q = ("SELECT id_tweet, data_brt, autor, nome_autor, status_verificado, num_seguidores,"
         " num_tweets, status_retweet, autor_original, texto, links, hashtags, idioma"
         " FROM tweets WHERE substr(data_brt,1,10) BETWEEN ? AND ? ORDER BY id_tweet")
    linhas = [dict(r) for r in cx.execute(q, (DIAS[0], DIAS[-1]))]
    cx.close()
    log("populacao (19-25/out): %d tweets" % len(linhas))

    por_dia = {}
    for r in linhas:
        por_dia.setdefault(r["data_brt"][:10], []).append(r)
    cont = {d: len(v) for d, v in por_dia.items()}
    cota = aloca_por_dia(cont, N_TOTAL)
    log("cota por dia (proporcional): " + ", ".join("%s=%d" % (d[-5:], cota[d]) for d in DIAS))

    rng = random.Random(SEED)
    amostra = []
    for d in DIAS:
        amostra += rng.sample(por_dia[d], cota[d])
    rng.shuffle(amostra)          # dias interleaved: evita deriva do anotador por bloco

    # duplicatas de texto DENTRO da amostra
    grupos, gid = {}, 0
    for r in amostra:
        k = norm_texto(r["texto"])
        if k not in grupos:
            gid += 1
            grupos[k] = gid
    dup_count = {}
    for r in amostra:
        g = grupos[norm_texto(r["texto"])]
        dup_count[g] = dup_count.get(g, 0) + 1

    # split dev/teste estratificado por dia (congelado ANTES de qualquer LLM)
    rng2 = random.Random(SEED + 1)
    ids_por_dia = {}
    for r in amostra:
        ids_por_dia.setdefault(r["data_brt"][:10], []).append(r["id_tweet"])
    cota_dev = aloca_por_dia({d: len(v) for d, v in ids_por_dia.items()}, N_DEV)
    dev = set()
    for d, ids in ids_por_dia.items():
        dev |= set(rng2.sample(sorted(ids), cota_dev[d]))
    teste = [r["id_tweet"] for r in amostra if r["id_tweet"] not in dev]

    # reteste intracodificador: 40 itens, estratificado por dia, ordem propria
    rng3 = random.Random(SEED + 2)
    cota_ret = aloca_por_dia({d: len(v) for d, v in ids_por_dia.items()}, N_RETESTE)
    ret = set()
    for d, ids in ids_por_dia.items():
        ret |= set(rng3.sample(sorted(ids), cota_ret[d]))

    COLS = ["n", "id_tweet", "data_brt", "autor", "nome_autor", "verificado",
            "seguidores", "tweets_do_autor", "eh_retweet", "autor_original",
            "idioma", "texto", "link1", "host1", "hashtags",
            "cidadao", "stance", "confianca", "notas"]

    def linha_csv(i, r):
        links = links_efetivos(r["links"], r["texto"])
        _, host = classe_do_primeiro_link(links, cache)
        return {
            "n": i, "id_tweet": r["id_tweet"], "data_brt": r["data_brt"],
            "autor": r["autor"], "nome_autor": r["nome_autor"],
            "verificado": r["status_verificado"], "seguidores": r["num_seguidores"],
            "tweets_do_autor": r["num_tweets"], "eh_retweet": r["status_retweet"],
            "autor_original": r["autor_original"] or "", "idioma": r["idioma"],
            "texto": (r["texto"] or "").replace("\n", " / "),
            "link1": links[0] if links else "", "host1": host or "",
            "hashtags": r["hashtags"] or "",
            "cidadao": "", "stance": "", "confianca": "", "notas": "",
        }

    def escreve(path, rows):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
            w.writeheader()
            for row in rows:
                w.writerow(row)

    escreve(OUT / "gold_stance_para_rotular.csv",
            [linha_csv(i, r) for i, r in enumerate(amostra, 1)])

    amostra_ret = [r for r in amostra if r["id_tweet"] in ret]
    rng3.shuffle(amostra_ret)
    escreve(OUT / "gold_stance_RETESTE.csv",
            [linha_csv(i, r) for i, r in enumerate(amostra_ret, 1)])

    h = hashlib.sha256(
        ",".join(str(r["id_tweet"]) for r in amostra).encode()).hexdigest()[:12]
    meta = {
        "gerado_por": "analise/amostra_stance_humana.py",
        "populacao": {"snapshot": SNAP.name, "janela": [DIAS[0], DIAS[-1]],
                      "n_populacao": len(linhas)},
        "seed": SEED, "n_total": N_TOTAL,
        "cota_por_dia": cota,
        "sha256_12_dos_ids": h,
        "dev": sorted(dev), "teste": sorted(teste), "reteste": sorted(ret),
        "duplicatas": {"grupos_distintos": gid,
                       "itens_em_grupo_repetido": sum(c for c in dup_count.values() if c > 1)},
    }
    split_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

    log("")
    log("dev %d / teste %d / reteste %d" % (len(dev), len(teste), len(ret)))
    log("textos distintos na amostra: %d/%d (%d itens em grupo repetido)"
        % (gid, N_TOTAL, meta["duplicatas"]["itens_em_grupo_repetido"]))
    log("sha256(ids)[:12] = " + h)
    log("escrito em " + str(OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
