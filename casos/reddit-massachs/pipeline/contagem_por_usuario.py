"""
Contagem de comentarios por usuario e por subreddit (2012 e 2016) — caso Massachs.

Para que serve
--------------
O grupo focal do artigo sao os usuarios com >=10 comentarios em 2012 E >=10 em 2016
"em r/politics + os 50 subreddits mais similares" (51). A lista dos 51 nao foi
publicada; o dataset dos autores so deixa ver 34 nomes (colunas de interacao). Mas o
dataset traz o NOME DE USUARIO de cada um dos 44.924. Entao, para uma amostra deles,
contamos no acervo do Reddit quantos comentarios cada um fez em cada subreddit, em
2012 e em 2016. Com isso da para ver quais subreddits a lista PRECISA conter para que
todos atinjam o limiar — engenharia reversa da lista.

Rota
----
Arctic Shift (acervo Pushshift e sucessores), endpoint de agregacao por AUTOR
(`comments/search/aggregate?author=X&aggregate=subreddit`). Uma chamada por usuario e
ano; resposta pequena (<1 s no teste de 22/set/2026).

Cuidados
--------
- Ritmo lento (PAUSA entre chamadas) e recuo longo quando a API responde
  "Timeout. Maybe slow down a bit" — que, como mediu o caso reddit-topicos, e sobretudo
  estrangulamento por taxa (ESTADO §4.23).
- Retomavel: cada resultado vai para um .jsonl; usuarios ja feitos sao pulados.
- Amostra sorteada com semente fixa, para ser reproduzivel.

Uso (rodar da copia COM dados, Documents/dissertacao/casos/reddit-massachs):
    PYTHONIOENCODING=utf-8 python -u pipeline/contagem_por_usuario.py 500
Saida: data/repl/massachs2016/contagem_por_usuario.jsonl
"""
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

import pandas as pd

UA = "Mozilla/5.0 (academic replication; massachs-2020; PUC-Rio)"
URL = "https://arctic-shift.photon-reddit.com/api/comments/search/aggregate"
D = pathlib.Path("data/repl/massachs2016")
CSV = D / "reddit-politics-12-16.csv.bz2"
OUT = D / "contagem_por_usuario.jsonl"
SEED = 20260922
PAUSA = 1.5          # segundos entre chamadas
RECUO = 300          # segundos de silencio apos "slow down" (medido em §4.23)
ANOS = {"2012": ("2012-01-01", "2013-01-01"), "2016": ("2016-01-01", "2017-01-01")}


def consulta(autor, ini, fim, tentativas=4):
    q = urllib.parse.urlencode({"author": autor, "aggregate": "subreddit",
                                "after": ini, "before": fim})
    for k in range(tentativas):
        try:
            req = urllib.request.Request(URL + "?" + q, headers={"User-Agent": UA})
            d = json.loads(urllib.request.urlopen(req, timeout=120).read())
            if d.get("error"):
                raise RuntimeError(d["error"])
            return {x["key"]: int(x["count"]) for x in (d.get("data") or [])}
        except Exception as e:
            msg = str(e)
            espera = RECUO if "slow down" in msg.lower() else 10 * (k + 1)
            print(f"  ! {autor} {ini[:4]}: {msg[:80]} -> espera {espera}s", flush=True)
            time.sleep(espera)
    return None


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    usuarios = pd.read_csv(CSV, header=[0, 1], index_col=0).index
    amostra = pd.Series(usuarios).sample(n=n, random_state=SEED).tolist()

    feitos = set()
    if OUT.exists():
        for linha in OUT.read_text(encoding="utf-8").splitlines():
            feitos.add(json.loads(linha)["autor"])
    print(f"amostra {n}; ja feitos {len(feitos)}", flush=True)

    t0 = time.time()
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
                print(f"{i}/{n}  {time.time() - t0:.0f}s", flush=True)
    print("fim", flush=True)


if __name__ == "__main__":
    main()
