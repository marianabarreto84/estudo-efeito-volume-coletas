#!/usr/bin/env python3
"""AGREGAR nao e COLETAR — este script mede a diferenca (Portao 1b, caso Melton).

A pergunta
----------
O endpoint de **agregacao** (`/search/aggregate`) falha nos subreddits grandes: em
22/ago/2026, `conspiracy` recusou janelas de 166d, 83d, 41,5d, 20,8d, 10,4d e 5,2d,
sempre depois de 300 s de descanso. Isso NAO responde a pergunta que importa para o
caso, que e outra:

    da para COLETAR os itens de um subreddit grande?

Sao endpoints diferentes, com custo diferente para o servidor:

  - `/search/aggregate` **conta**: varre o periodo inteiro e devolve um numero. Caro.
  - `/search` paginado **entrega**: 100 itens por chamada, avancando por `created_utc`.
    Barato por chamada — nunca pede uma varredura inteira de uma vez. Foi assim que o
    caso reddit-buntain trouxe **1,06 milhao de itens** a **95 itens/s** medidos.

O teste
-------
Pagina uma janela CURTA de um subreddit grande e mede: funciona? a que taxa? Com a
taxa, da para extrapolar o custo da Fase 1 sem precisar da contagem exata — que e
exatamente o que o Portao 1 precisa decidir.

De quebra, a contagem paginada de uma janela curta **e** uma medida de volume: se a
agregacao nao conta, contar paginando resolve, so que mais devagar.

Uso:
    python pipeline/testa_coleta.py                      # conspiracy, 24 h
    python pipeline/testa_coleta.py --sub COVID19 --horas 12
    python pipeline/testa_coleta.py --sub conspiracy --tipo comments --horas 6

Saida: stdout + data/repl/melton2021/teste_coleta.json (acumula uma entrada por teste)
"""
import argparse
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

RAIZ = pathlib.Path(__file__).resolve().parents[1]
OUT = RAIZ / "data/repl/melton2021/teste_coleta.json"

BASE = "https://arctic-shift.photon-reddit.com/api"
UA = "Mozilla/5.0 (academic replication; melton-2021; PUC-Rio)"

# janela do artigo; o teste comeca no inicio dela
INI_ARTIGO = int(datetime(2020, 12, 1, tzinfo=timezone.utc).timestamp())

CAMPOS = {
    # so o que a Fase 1 precisa. Texto incluido: LDA e sentimento dependem dele.
    "posts": "id,created_utc,subreddit,author,title,selftext,score,num_comments",
    "comments": "id,created_utc,subreddit,author,body,score",
}
PACING = 1.0     # s entre paginas — a paginacao e barata, mas nao ha pressa


def pagina(kind, sub, after, before, campos, timeout=120):
    qs = urllib.parse.urlencode({"subreddit": sub, "after": int(after),
                                 "before": int(before), "sort": "asc",
                                 "limit": 100, "fields": campos})
    url = "%s/%s/search?%s" % (BASE, kind, qs)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        bruto = urllib.request.urlopen(req, timeout=timeout).read()
    except urllib.error.HTTPError as e:
        corpo = ""
        try:
            corpo = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            pass
        return None, "http:%s %s" % (e.code, corpo.replace("\n", " ")), 0
    except Exception as e:
        return None, "rede:%s" % type(e).__name__, 0
    d = json.loads(bruto)
    if isinstance(d, dict) and d.get("error"):
        return None, "erro:%s" % str(d["error"])[:80], len(bruto)
    dados = d.get("data") if isinstance(d, dict) else d
    return (dados or []), "ok", len(bruto)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sub", default="conspiracy")
    ap.add_argument("--tipo", default="posts", choices=["posts", "comments"])
    ap.add_argument("--horas", type=float, default=24.0,
                    help="tamanho da janela de teste, em horas (padrao 24)")
    ap.add_argument("--max-paginas", type=int, default=200)
    ap.add_argument("--inicio", default=None,
                    help="inicio da janela de teste, AAAA-MM-DD (padrao: 2020-12-01, "
                         "o inicio da janela do artigo). Serve para testar outros casos")
    args = ap.parse_args()

    if args.inicio:
        a_, m_, d_ = (int(x) for x in args.inicio.split("-"))
        ini = int(datetime(a_, m_, d_, tzinfo=timezone.utc).timestamp())
    else:
        ini = INI_ARTIGO
    fim = int(ini + args.horas * 3600)
    campos = CAMPOS[args.tipo]

    print("Teste de COLETA paginada (nao agregacao)")
    print("  subreddit : r/%s" % args.sub)
    print("  tipo      : %s" % args.tipo)
    print("  janela    : %s a %s (%.0f h)"
          % (datetime.fromtimestamp(ini, timezone.utc).strftime("%d/%m/%Y %H:%M"),
             datetime.fromtimestamp(fim, timezone.utc).strftime("%d/%m/%Y %H:%M"),
             args.horas))
    print("  campos    : %s\n" % campos)

    cursor = ini
    itens = paginas = bytes_tot = 0
    falhas = []
    t0 = time.time()
    while paginas < args.max_paginas:
        dados, motivo, nb = pagina(args.tipo, args.sub, cursor, fim, campos)
        paginas += 1
        if dados is None:
            falhas.append({"pagina": paginas, "motivo": motivo})
            print("  pagina %3d FALHOU: %s" % (paginas, motivo))
            break
        bytes_tot += nb
        if not dados:
            print("  pagina %3d vazia -> fim da janela" % paginas)
            break
        itens += len(dados)
        ultimo = dados[-1].get("created_utc")
        print("  pagina %3d  +%3d itens  (total %5d)  ate %s"
              % (paginas, len(dados), itens,
                 datetime.fromtimestamp(ultimo, timezone.utc).strftime("%d/%m %H:%M")))
        sys.stdout.flush()
        if ultimo is None or len(dados) < 100:
            break
        cursor = ultimo + 1
        time.sleep(PACING)

    seg = time.time() - t0
    taxa = itens / seg if seg > 0 else 0
    ok = not falhas and itens > 0
    kb_item = (bytes_tot / itens / 1024) if itens else 0

    print("\n%s" % ("=" * 62))
    print("resultado : %s" % ("FUNCIONA" if ok else "FALHOU"))
    print("itens     : {:,} em {:.0f}s ({} paginas)".format(itens, seg, paginas))
    print("taxa      : %.1f itens/s" % taxa)
    print("peso      : %.2f kB/item (com texto)" % kb_item)
    if ok:
        por_dia = itens / args.horas * 24
        print("\nextrapolacao (linear, so para ordem de grandeza):")
        print("  ~{:,.0f} {} por dia em r/{}".format(por_dia, args.tipo, args.sub))
        print("  166 dias da janela do artigo -> ~{:,.0f} itens".format(por_dia * 166))
        print("  a %.1f itens/s isso custaria %.1f h de API"
              % (taxa, por_dia * 166 / taxa / 3600))
        print("  e ~%.1f GB em disco" % (por_dia * 166 * kb_item * 1024 / 1e9))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    hist = json.load(open(OUT, encoding="utf-8")) if OUT.exists() else {"testes": []}
    hist["testes"].append({
        "subreddit": args.sub, "tipo": args.tipo, "horas_da_janela": args.horas,
        "after": ini, "before": fim, "campos": campos,
        "funciona": ok, "itens": itens, "paginas": paginas, "segundos": round(seg, 1),
        "itens_por_s": round(taxa, 2), "kb_por_item": round(kb_item, 3),
        "bytes_recebidos": bytes_tot, "falhas": falhas,
        "nota": "endpoint /search paginado — NAO e /search/aggregate, que falha "
                "nos subreddits grandes",
    })
    OUT.write_text(json.dumps(hist, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nescrito em %s" % OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
