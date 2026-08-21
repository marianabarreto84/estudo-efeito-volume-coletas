"""
Eixo MP/MC — teste do CDX do Internet Archive nos links MORTOS.

O ultimo candidato aberto para a divergencia MP 70,3% x 59%: os 13% de links que
nao resolvem (`nao_resolvido`) saem da base MP/MC. Se os mortos forem
sistematicamente MAIS MC que os vivos, a nossa base resolvida esta enviesada a
favor de MP, e parte do gap se explica.

Ate aqui isso era **hipotese nao testada** (ver §6 de
RESULTADOS_analise_midia_MV_MH.md, que retratou uma versao mais forte dela). Este
script a transforma em medida: sorteia links mortos, pergunta ao Internet Archive
se ha snapshot, recupera o ALVO do redirecionamento e classifica MP/MC.

⚠ Vies de sobrevivencia continua existindo — agora um nivel acima: mede-se a classe
dos mortos QUE O ARCHIVE GUARDOU, que podem nao representar os que ele nao guardou.
O script reporta a taxa de arquivamento para o leitor julgar.

Rede: apenas GET a `archive.org` / `web.archive.org` (APIs publicas, leitura).
Sem VPN. Amostra pequena e com pausa entre requisicoes, de proposito.

Uso: PYTHONIOENCODING=utf-8 python -u analise/cdx_links_mortos.py [--n 200]
Saidas: stdout + data/repl/compos2014/cdx_mortos.json
"""
import argparse
import json
import pathlib
import random
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.midia_mp_mc import classificar_url_mp_mc

D = pathlib.Path("data/repl/compos2014")
OUT_JSON = D / "cdx_mortos.json"
UA = "Mozilla/5.0 (replicacao academica PUC-Rio; contato via GitHub)"
PAUSA = 2.5          # segundos entre requisicoes — polidez + evitar 429
TIMEOUT = 20


def log(m):
    print(m, flush=True)


def get(url, redirect=True):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    if not redirect:
        class NoRedir(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        op = urllib.request.build_opener(NoRedir)
    else:
        op = urllib.request.build_opener()
    return op.open(req, timeout=TIMEOUT)


def snapshot(url, tentativas=3):
    """Consulta o CDX. Devolve ('ok', snap_url) | ('vazio', None) | ('erro', msg).

    ⚠ Distinguir 'vazio' de 'erro' e essencial: a versao anterior deste script usava
    a API `archive.org/wayback/available`, que respondeu **429 Too Many Requests**, e
    contava toda falha como "sem snapshot" — o que produziria um falso 0% de
    arquivamento. Erro nunca vira ausencia aqui.
    """
    alvo = url.split("://", 1)[-1]
    api = ("https://web.archive.org/cdx/search/cdx?url="
           + urllib.parse.quote(alvo, safe="") +
           "&output=json&limit=1&fl=timestamp,original,statuscode")
    for t in range(tentativas):
        try:
            with get(api) as r:
                dados = json.loads(r.read().decode("utf-8", "replace") or "[]")
            if len(dados) <= 1:
                return "vazio", None
            ts, orig = dados[1][0], dados[1][1]
            return "ok", f"https://web.archive.org/web/{ts}id_/{orig}"
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(5 * (t + 1))       # backoff
                continue
            return "erro", f"HTTP {e.code}"
        except Exception as e:
            if t == tentativas - 1:
                return "erro", type(e).__name__
            time.sleep(3 * (t + 1))
    return "erro", "429 persistente"


def alvo_do_redirect(snap_url):
    """Busca o snapshot em modo `id_` (conteudo original) e le o destino."""
    u = snap_url.replace("/http", "id_/http", 1) if "id_/" not in snap_url else snap_url
    try:
        r = get(u, redirect=False)
        code = r.getcode()
        loc = r.headers.get("Location")
        r.close()
        if loc:
            return loc
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location") if e.headers else None
        if loc:
            return loc
    except Exception:
        return None
    return None


def limpa_wayback(u):
    """Se o destino veio prefixado pelo wayback, devolve a URL original."""
    if not u:
        return None
    i = u.find("/http")
    if "web.archive.org" in u and i != -1:
        return u[i + 1:]
    return u


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    args = ap.parse_args()

    con = sqlite3.connect(D / "expand_cache.sqlite")
    mortos = [r[0] for r in con.execute(
        "SELECT url FROM expand WHERE status IN ('morto','erro')")]
    con.close()
    log(f"== {len(mortos):,} links mortos/erro no cache ==")
    amostra = random.Random(20141026).sample(mortos, min(args.n, len(mortos)))
    log(f"   amostra de {len(amostra)} (semente 20141026), pausa de {PAUSA}s\n")

    res = []
    c = Counter()
    for i, u in enumerate(amostra, 1):
        st, snap = snapshot(u)
        if st == "erro":
            c["erro_consulta"] += 1
            res.append({"url": u, "status": "erro", "detalhe": snap})
        elif st == "vazio":
            c["sem_snapshot"] += 1
            res.append({"url": u, "status": "sem_snapshot"})
        else:
            alvo = limpa_wayback(alvo_do_redirect(snap))
            if not alvo:
                c["snapshot_sem_alvo"] += 1
                cl = None
            else:
                cl = classificar_url_mp_mc(alvo)
                c[cl] += 1
                c["recuperado"] += 1
            res.append({"url": u, "status": "arquivado", "snapshot": snap,
                        "alvo": alvo, "classe": cl})
        if i % 20 == 0:
            log(f"   {i}/{len(amostra)} · recuperados {c['recuperado']} · "
                f"sem snapshot {c['sem_snapshot']} · erros {c['erro_consulta']}")
        time.sleep(PAUSA)

    n = len(amostra)
    rec = c["recuperado"]
    validos = n - c["erro_consulta"]
    log(f"\n== Resultado ==")
    log(f"   amostrados             {n:>5}")
    log(f"   erro de consulta       {c['erro_consulta']:>5}  (NAO conta como ausencia)")
    log(f"   consultas validas      {validos:>5}")
    log(f"   sem snapshot no Archive{c['sem_snapshot']:>5} "
        f"({100*c['sem_snapshot']/validos:.1f}% das validas)")
    log(f"   snapshot sem destino   {c['snapshot_sem_alvo']:>5}")
    log(f"   ALVO RECUPERADO        {rec:>5} "
        f"({100*rec/validos:.1f}% das validas)")
    if rec:
        log("\n   classe dos mortos recuperados:")
        for cl in ("MP", "MC", "nao_midia", "indefinido"):
            if c[cl]:
                log(f"     {cl:<12} {c[cl]:>5} ({100*c[cl]/rec:>5.1f}%)")
        mp, mc = c["MP"], c["MC"]
        if mp + mc:
            log(f"\n   >>> MP% entre os mortos recuperados: {100*mp/(mp+mc):.1f}%")
            log(f"       (base resolvida do corpus, mesma janela: 70,9%)")
            log("       Se o valor aqui for MENOR, os mortos sao mais MC e a base"
                " resolvida esta enviesada a favor de MP.")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/cdx_links_mortos.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "n_amostra": n, "semente": 20141026,
        "contagens": dict(c),
        "mp_pct_entre_recuperados": (round(100 * c["MP"] / (c["MP"] + c["MC"]), 1)
                                     if c["MP"] + c["MC"] else None),
        "detalhe": res,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
