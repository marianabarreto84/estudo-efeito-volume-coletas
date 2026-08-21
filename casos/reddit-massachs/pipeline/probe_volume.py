"""
Sonda de volume da Fase 3 (caso Massachs) — quanto custa "coletar mais"?

O que se quer coletar
---------------------
Para refazer o focus group com limiar de atividade menor (o eixo "coletar mais"),
precisamos de **todos os comentarios** dos subreddits politicos em **2012** e
**2016** — so `author + subreddit + created_utc` (o rotulo e a atividade sao
estruturais; nao precisa de texto).

Lista de subreddits
-------------------
O artigo diz "r/politics + os 50 mais similares" = 51. O dataset publicado expoe
**34** nomes (as colunas `dist_int_12`/`pos_int_12`) — sao os subreddits sobre os
quais ele reporta interacao. Usamos esses 34, e a divergencia 34 x 51 fica
declarada: a lista dos 51 nao esta publicada, e o metodo de similaridade que a
gerou (shorttails) depende de um snapshot de 2015 que nao e recuperavel hoje.

Metodo
------
Endpoint de agregacao do Arctic Shift (`comments/search/aggregate`), que devolve a
**contagem exata** sem baixar os itens. 2 chamadas por subreddit (2012 e 2016).

Uso: PYTHONIOENCODING=utf-8 python -u pipeline/probe_volume.py
Saida: stdout + data/repl/massachs2016/volume_fase3.json
"""
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (academic replication; massachs-2020; PUC-Rio)"
BASE = "https://arctic-shift.photon-reddit.com/api"
OUT = pathlib.Path("data/repl/massachs2016/volume_fase3.json")

# os 34 subreddits politicos expostos pelo dataset dos autores.
# 'on' e 'POLITIC' vem assim do CSV (nomes truncados/estranhos na fonte) — mantidos
# para rastreabilidade, mas marcados como suspeitos.
SUBS = ["politics", "news", "worldnews", "Libertarian", "GaryJohnson", "TrueReddit",
        "PoliticalHumor", "atheism", "Documentaries", "todayilearned", "conspiracy",
        "progressive", "POLITIC", "Futurology", "Conservative", "Economics", "Liberal",
        "law", "Ask_Politics", "ShitPoliticsSays", "dataisbeautiful",
        "PoliticalDiscussion", "moderatepolitics", "worldpolitics", "WikiLeaks",
        "economy", "NeutralPolitics", "Republican", "AmericanPolitics",
        "lostgeneration", "uspolitics", "democrats", "inthenews", "on"]
SUSPEITOS = {"on", "POLITIC"}

ANOS = {"2012": ("2012-01-01", "2013-01-01"), "2016": ("2016-01-01", "2017-01-01")}
TAXA_OBSERVADA = 95.0     # itens/s medidos na coleta do caso Buntain


def _um_intervalo(sub, ini, fim, tentativas=4):
    p = urllib.parse.urlencode({"subreddit": sub, "after": ini, "before": fim,
                                "aggregate": "subreddit"})
    url = "%s/comments/search/aggregate?%s" % (BASE, p)
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            d = json.loads(urllib.request.urlopen(req, timeout=120).read())
            dados = d.get("data") or []
            return int(dados[0]["count"]) if dados else 0
        except Exception:
            if k == tentativas - 1:
                return None
            time.sleep(3 * (k + 1))


def conta(sub, ini, fim):
    """
    Soma MES A MES. A consulta de ano inteiro estoura o tempo nos subreddits
    grandes (politics, news, worldnews...) — a 1a versao desta sonda devolvia None
    para 20 dos 34 e ainda assim somava os demais, produzindo um "total" que NAO
    era o universo. Agora: 12 consultas por ano, e se QUALQUER mes falhar o
    subreddit-ano inteiro vira None (nunca um total parcial disfarcado).
    """
    ano = int(ini[:4])
    total = 0
    for m in range(1, 13):
        a = "%04d-%02d-01" % (ano, m)
        b = "%04d-%02d-01" % (ano + 1, 1) if m == 12 else "%04d-%02d-01" % (ano, m + 1)
        c = _um_intervalo(sub, a, b)
        if c is None:
            return None
        total += c
        time.sleep(0.2)
    return total


def main():
    res = {}
    print("%-22s %14s %14s" % ("subreddit", "2012", "2016"))
    for s in SUBS:
        linha = {}
        for ano, (i, f) in ANOS.items():
            linha[ano] = conta(s, i, f)
            time.sleep(0.4)
        res[s] = linha
        marca = "  <- nome suspeito" if s in SUSPEITOS else ""
        print("%-22s %14s %14s%s"
              % (s, "{:,}".format(linha["2012"]) if linha["2012"] is not None else "erro",
                 "{:,}".format(linha["2016"]) if linha["2016"] is not None else "erro", marca))
        sys.stdout.flush()

    falhas = [s for s, v in res.items() if v["2012"] is None or v["2016"] is None]
    t12 = sum(v["2012"] or 0 for v in res.values())
    t16 = sum(v["2016"] or 0 for v in res.values())
    tot = t12 + t16
    print("\n%-22s %14s %14s" % ("soma do que respondeu", "{:,}".format(t12), "{:,}".format(t16)))

    if falhas:
        # NUNCA reportar total parcial como se fosse o universo (foi o erro da 1a versao)
        print("\n⚠ %d subreddit(s) sem contagem completa: %s" % (len(falhas), ", ".join(falhas)))
        print("⚠ O total ACIMA E PARCIAL e NAO e o universo. Rode de novo para fechar.")
        completo = False
    else:
        print("universo da Fase 3: {:,} comentarios".format(tot))
        horas = tot / TAXA_OBSERVADA / 3600
        print("a %.0f itens/s (taxa medida no caso Buntain): **%.0f horas** (%.1f dias) de API"
              % (TAXA_OBSERVADA, horas, horas / 24))
        completo = True

    OUT.write_text(json.dumps({"subreddits": res,
                               "COMPLETO": completo,
                               "falhas": falhas,
                               "soma_2012": t12, "soma_2016": t16,
                               "soma_total": tot,
                               "aviso": (None if completo else
                                         "PARCIAL: %d subreddits sem contagem; a soma "
                                         "NAO e o universo" % len(falhas)),
                               "taxa_itens_por_s": TAXA_OBSERVADA,
                               "nota": "34 subreddits do dataset; o artigo declara 51"},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nescrito em %s" % OUT)


if __name__ == "__main__":
    main()
