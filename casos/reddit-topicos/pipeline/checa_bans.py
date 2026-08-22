#!/usr/bin/env python3
"""Portao 1(c) — quais dos 13 subreddits do alvo ainda existem hoje?

Por que importa
---------------
Subreddits banidos somem da API oficial mas CONTINUAM nos arquivos historicos. Se
parte do corpus do artigo so existe no arquivo, entao a rota oficial de hoje **nem
alcanca** o corpus que o artigo analisou — o que e achado (a replicacao por PRAW e
impossivel em 2026) e obstaculo ao mesmo tempo.

Metodo
------
A API do Reddit devolve 403 para acesso automatizado (testado em 22/ago/2026: os 13
deram 403), entao "perguntar ao Reddit" nao serve. O teste aqui e **por atividade no
arquivo**: conta itens no Arctic Shift em tres janelas —

  (a) a janela do artigo         (dez/2020 a mai/2021)  -> o corpus existe no arquivo?
  (b) logo apos o banimento em massa (out-dez/2021)     -> parou de existir?
  (c) recente                    (jan-mar/2026)         -> esta vivo hoje?

Um subreddit vivo tem atividade em (a), (b) e (c). Um banido em 2021 tem atividade
em (a) e zero em (b) e (c).

Uso: PYTHONIOENCODING=utf-8 python -u pipeline/checa_bans.py
Saida: stdout + data/repl/melton2021/status_subreddits.json
"""
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (academic replication; melton-2021; PUC-Rio)"
BASE = "https://arctic-shift.photon-reddit.com/api"
OUT = pathlib.Path("data/repl/melton2021/status_subreddits.json")

SUBS = ["Vaccines", "CovidVaccine", "CovidVaccinated", "AntiVaxxers", "vaxxhappened",
        "antivaccine", "conspiracy", "conspiracytheories", "NoNewNormal",
        "conspiracy_commons", "COVID19", "COVID", "coronavirus"]


def ts(*a):
    return int(datetime(*a, tzinfo=timezone.utc).timestamp())


JANELAS = {
    "janela_do_artigo": (ts(2020, 12, 1), ts(2021, 5, 16)),
    "pos_banimentos_2021": (ts(2021, 10, 1), ts(2022, 1, 1)),
    "hoje_2026": (ts(2026, 1, 1), ts(2026, 4, 1)),
}


def conta(sub, ini, fim, tentativas=3):
    p = urllib.parse.urlencode({"subreddit": sub, "after": ini, "before": fim,
                                "aggregate": "subreddit"})
    url = "%s/posts/search/aggregate?%s" % (BASE, p)
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            d = json.loads(urllib.request.urlopen(req, timeout=120).read())
            return sum(int(x.get("count", 0)) for x in (d.get("data") or []))
        except Exception:
            if k == tentativas - 1:
                return None
            time.sleep(2.5 * (k + 1))


def main():
    res = {}
    print("%-20s %14s %14s %12s  %s" % ("subreddit", "janela artigo", "out-dez/2021",
                                        "jan-mar/2026", "leitura"))
    for s in SUBS:
        linha = {}
        for rot, (a, b) in JANELAS.items():
            linha[rot] = conta(s, a, b)
            time.sleep(0.3)
        art, pos, hoje = (linha["janela_do_artigo"], linha["pos_banimentos_2021"],
                          linha["hoje_2026"])
        if None in (art, pos, hoje):
            leitura = "INDETERMINADO (consulta falhou)"
        elif hoje and hoje > 0:
            leitura = "VIVO"
        elif pos == 0 and hoje == 0 and art and art > 0:
            leitura = "MORTO/BANIDO — so existe no arquivo"
        else:
            leitura = "inativo"
        linha["leitura"] = leitura
        res[s] = linha
        fmt = lambda v: "{:,}".format(v) if v is not None else "erro"
        print("%-20s %14s %14s %12s  %s" % (s, fmt(art), fmt(pos), fmt(hoje), leitura))
        sys.stdout.flush()

    mortos = [s for s, v in res.items() if v["leitura"].startswith("MORTO")]
    print("\n%d de 13 so existem no arquivo: %s" % (len(mortos), ", ".join(mortos) or "-"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "fonte": "arctic-shift.photon-reddit.com (agregacao de submissoes)",
        "metodo": "atividade no arquivo em 3 janelas; a API oficial devolve 403 "
                  "para acesso automatizado e nao serve de teste",
        "janelas": {k: {"after": a, "before": b} for k, (a, b) in JANELAS.items()},
        "subreddits": res,
        "so_no_arquivo": mortos,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("escrito em %s" % OUT)


if __name__ == "__main__":
    main()
