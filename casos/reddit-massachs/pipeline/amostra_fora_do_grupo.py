"""
Amostra de usuarios FORA do grupo focal (exemplos negativos) — caso Massachs.

Por que
-------
Os usuarios do grupo (positivos) ja passam do limiar com os 34 subreddits conhecidos,
entao nao revelam os 17 que faltam. O que discrimina a lista e quem NAO esta no grupo:
se alguem de fora tem >=10 comentarios nos dois anos somando um conjunto de subreddits,
esse conjunto nao pode estar inteiro na lista dos 51.

Como
----
Sorteia instantes de 2012 (semente fixa), pega comentarios de r/politics em torno de cada
instante (Arctic Shift, `comments/search`), junta os autores, descarta quem esta entre os
44.924 e as contas apagadas/bots, e sorteia N. Depois conta, por autor, os comentarios
por subreddit em 2012 e 2016 com a mesma funcao do contagem_por_usuario.py.

Uso (da copia COM dados):
    PYTHONIOENCODING=utf-8 python -u pipeline/amostra_fora_do_grupo.py 500
Saida: data/repl/massachs2016/contagem_fora_do_grupo.jsonl
"""
import json
import pathlib
import random
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from contagem_por_usuario import ANOS, CSV, PAUSA, UA, consulta  # noqa: E402

D = pathlib.Path("data/repl/massachs2016")
OUT = D / "contagem_fora_do_grupo.jsonl"
AUTORES = D / "autores_fora_do_grupo.json"
SEED = 20260922
BUSCA = "https://arctic-shift.photon-reddit.com/api/comments/search"
EXCLUIR = {"[deleted]", "AutoModerator", "", None}


def autores_em(instante):
    ini = datetime.fromtimestamp(instante, tz=timezone.utc)
    q = urllib.parse.urlencode({"subreddit": "politics", "after": int(instante),
                                "before": int(instante) + 3600, "limit": 100,
                                "fields": "author"})
    req = urllib.request.Request(BUSCA + "?" + q, headers={"User-Agent": UA})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    return [x.get("author") for x in (d.get("data") or [])], ini


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    grupo = set(pd.read_csv(CSV, header=[0, 1], index_col=0).index)
    rnd = random.Random(SEED)

    if AUTORES.exists():
        candidatos = json.loads(AUTORES.read_text(encoding="utf-8"))
    else:
        t0 = datetime(2012, 1, 1, tzinfo=timezone.utc).timestamp()
        t1 = datetime(2013, 1, 1, tzinfo=timezone.utc).timestamp()
        vistos = set()
        while len(vistos) < 3 * n:
            inst = rnd.uniform(t0, t1 - 3600)
            try:
                autores, quando = autores_em(inst)
            except Exception as e:
                print("  ! busca:", str(e)[:80], "-> espera 300s", flush=True)
                time.sleep(300)
                continue
            novos = {a for a in autores if a not in EXCLUIR and a not in grupo}
            vistos |= novos
            print(f"  {quando:%Y-%m-%d %H}h: +{len(novos)} (total {len(vistos)})", flush=True)
            time.sleep(PAUSA)
        candidatos = sorted(vistos)
        AUTORES.write_text(json.dumps(candidatos, ensure_ascii=False), encoding="utf-8")

    amostra = random.Random(SEED + 1).sample(candidatos, min(n, len(candidatos)))
    feitos = set()
    if OUT.exists():
        feitos = {json.loads(l)["autor"] for l in OUT.read_text(encoding="utf-8").splitlines()}
    print(f"fora do grupo: {len(candidatos)} candidatos; amostra {len(amostra)}; "
          f"ja feitos {len(feitos)}", flush=True)
    with OUT.open("a", encoding="utf-8") as f:
        for i, autor in enumerate(amostra, 1):
            if autor in feitos:
                continue
            reg = {"autor": autor}
            for ano, (ini, fim) in ANOS.items():
                reg[ano] = consulta(autor, ini, fim)
                time.sleep(PAUSA)
            f.write(json.dumps(reg, ensure_ascii=False) + "\n")
            f.flush()
            if i % 25 == 0:
                print(f"{i}/{len(amostra)}", flush=True)
    print("fim", flush=True)


if __name__ == "__main__":
    main()
