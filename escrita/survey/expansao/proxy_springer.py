# =====================================================================
#  Recuperacao via proxy institucional PUC-Rio, restrita a Springer.
#
#  POR QUE ESTE SCRIPT EXISTE, e nao se usa `retry_pdfs --via-proxy`:
#  o `services/pdf_fetcher.fetch_pdf_via_proxy()` devolve `Optional[str]`
#  e engole todo status code (`if r.status_code >= 400: return None`).
#  Um 403 de BLOQUEIO fica indistinguivel de um 404 de artigo inexistente
#  -- e 403 e exatamente o sinal que define a condicao de parada prescrita
#  em EXPANSAO_recuperacao.md sec. 4 ("devagar e com parada ao primeiro
#  403"). Sem enxergar o status, "com cuidado" seria so intencao.
#
#  O QUE ESTE SCRIPT NAO FAZ:
#  - nao escreve no research.db. Salva PDF em pdfs/ com o nome derivado do
#    DOI (mesma convencao do pdf_fetcher) e deixa o `reconcilia_pdfs.py`
#    trazer para o banco depois. Isso evita contencao de escrita com o
#    analyze_pdfs e reusa um caminho ja testado.
#  - nao toca em editora nenhuma alem da Springer (10.1007). ACM, Elsevier,
#    SAGE, T&F, Emerald e Wiley bloqueiam automacao (Cloudflare/anti-bot) e
#    estao fora por decisao, nao por esquecimento. A IEEE funcionava em
#    mai/2026 e passou a devolver 202 com corpo vazio em ago/2026.
#
#  RISCO, declarado: o acesso vem da licenca comercial da PUC-Rio. Volume
#  automatizado e o que dispara deteccao, e um bloqueio recairia sobre a
#  instituicao inteira. Por isso: sequencial, lento, e parada dura.
#
#  Uso:
#    python proxy_springer.py --dry-run            # fila, sem requisicao
#    python proxy_springer.py --max-itens 10       # piloto
#    python proxy_springer.py --pausa 4.0          # corrida lenta
# =====================================================================
import argparse
import asyncio
import os
import random
import re
import sys
import time
from datetime import datetime

REPO = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
sys.path.insert(0, REPO)

import sqlite3
import httpx
from dotenv import load_dotenv

# override=True: o shell pode injetar variaveis vazias; sem override o .env
# nao sobrescreve. Mesmo cuidado que o retry_pdfs.py toma com PUCRIO_PROXY_*.
load_dotenv(os.path.join(REPO, ".env"), override=True)

from services import pdf_fetcher

DB = os.path.join(REPO, "research.db")
PDF_DIR = os.path.join(REPO, "pdfs")
LOG = os.path.join(REPO, "pdfs", ".proxy_springer.log")
PREFIXO = "10.1007"

# Marcadores de bloqueio no corpo da resposta. Qualquer um => PARADA.
#
# ⚠ A segunda linha foi acrescentada em 9/set/2026, depois de a versao
# original NAO pegar o desafio da Springer: ela responde HTTP **200** com
# 3.038 bytes de "Client Challenge / JavaScript is disabled in your
# browser". Status 200 e corpo curto -- nada que um teste de status code
# detecte. Foi por isso que o diagnostico de ago/2026 registrou "Springer
# 200, responde normalmente": ele mediu a landing page, nao o endpoint do
# PDF.
CHALLENGE = re.compile(
    r"just a moment|cf-browser-verification|cf_chl|challenge-platform|"
    r"attention required|access denied|unusual traffic|are you a robot|"
    r"enable javascript and cookies|"
    r"client challenge|javascript is disabled in your browser|"
    r"a required part of this site couldn|please enable javascript to proceed",
    re.IGNORECASE,
)
# Status que significam bloqueio, nao ausencia de artigo.
STATUS_BLOQUEIO = {401, 403, 407, 429, 503}


def agora():
    return datetime.now().strftime("%H:%M:%S")


def log(msg, fh=None):
    linha = f"[{agora()}] {msg}"
    print(linha, flush=True)
    if fh:
        fh.write(linha + "\n")
        fh.flush()


class Bloqueio(Exception):
    """Sinal de parada dura: a editora reagiu ao acesso automatizado."""


def caminho_do(doi):
    return os.path.join(PDF_DIR, doi.replace("/", "_").replace(":", "_") + ".pdf")


def fila():
    """Springer paga, sem pdf_path no banco e sem arquivo em disco."""
    con = sqlite3.connect(DB)
    out = []
    for aid, doi in con.execute(
        "select id, doi from articles "
        "where (pdf_path is null or trim(pdf_path)='') "
        "and doi is not null and lower(doi) like ?||'%' order by id",
        (PREFIXO,),
    ):
        p = caminho_do(doi)
        if os.path.isfile(p) and os.path.getsize(p) > 1024:
            continue
        out.append((aid, doi))
    con.close()
    return out


def checa(resp, etapa):
    """Levanta Bloqueio se a resposta tem cara de barreira anti-automacao."""
    if resp.status_code in STATUS_BLOQUEIO:
        raise Bloqueio(f"{etapa}: HTTP {resp.status_code}")
    # 202 com corpo vazio e a assinatura do desafio da IEEE; vale como bloqueio
    # em qualquer editora.
    if resp.status_code == 202 and len(resp.content) < 512:
        raise Bloqueio(f"{etapa}: HTTP 202 com corpo vazio ({len(resp.content)} bytes)")
    ct = resp.headers.get("content-type", "").lower()
    if "html" in ct and CHALLENGE.search(resp.text[:20000] or ""):
        raise Bloqueio(f"{etapa}: pagina de desafio (HTTP {resp.status_code})")


async def tenta(client, doi):
    """Devolve ('ok', caminho) | ('sem_pdf', motivo). Levanta Bloqueio."""
    destino = caminho_do(doi)

    r = await client.get(f"https://doi.org/{doi}")
    checa(r, "landing")
    if r.status_code >= 400:
        return "sem_pdf", f"landing HTTP {r.status_code}"

    ct = r.headers.get("content-type", "").lower()
    if "pdf" in ct or r.content[:4] == b"%PDF":
        if len(r.content) < 1024:
            return "sem_pdf", "PDF truncado"
        with open(destino, "wb") as f:
            f.write(r.content)
        return "ok", destino

    url_pdf = pdf_fetcher._extract_pdf_url(r.text, str(r.url), doi)
    if not url_pdf:
        return "sem_pdf", "sem citation_pdf_url na landing"

    r2 = await client.get(url_pdf)
    checa(r2, "pdf")
    if r2.status_code >= 400:
        return "sem_pdf", f"pdf HTTP {r2.status_code}"
    if not (r2.content[:4] == b"%PDF" or "pdf" in r2.headers.get("content-type", "").lower()):
        return "sem_pdf", "resposta nao e PDF"
    if len(r2.content) < 1024:
        return "sem_pdf", "PDF truncado"
    with open(destino, "wb") as f:
        f.write(r2.content)
    return "ok", destino


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="mostra a fila e sai, sem nenhuma requisicao")
    ap.add_argument("--max-itens", type=int, default=0, help="teto de tentativas nesta corrida (0 = fila toda)")
    ap.add_argument("--pausa", type=float, default=3.0, help="segundos entre tentativas (default: %(default)s)")
    ap.add_argument("--max-falhas-seguidas", type=int, default=25,
                    help="para se acumular tantas falhas benignas seguidas: pode ser bloqueio silencioso "
                         "(default: %(default)s)")
    args = ap.parse_args()

    q = fila()
    print(f"fila Springer (sem PDF, prefixo {PREFIXO}): {len(q)} artigos")
    if args.dry_run:
        for aid, doi in q[:10]:
            print(f"   id={aid:<6d} {doi}")
        if len(q) > 10:
            print(f"   ... e mais {len(q)-10}")
        print("\n(dry-run: nenhuma requisicao feita)")
        return

    proxy = pdf_fetcher._build_proxy_url()
    if not proxy:
        print("ERRO: PUCRIO_PROXY* nao configurados no .env. Aborta.")
        sys.exit(1)

    alvo = q[: args.max_itens] if args.max_itens else q
    os.makedirs(PDF_DIR, exist_ok=True)
    fh = open(LOG, "a", encoding="utf-8")
    log(f"=== inicio: {len(alvo)} tentativas, pausa {args.pausa}s, "
        f"parada em {args.max_falhas_seguidas} falhas seguidas ===", fh)

    ok = falhas = 0
    seguidas = 0
    t0 = time.time()
    headers = {
        "User-Agent": pdf_fetcher.BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml,application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8",
    }
    motivo_parada = "fila esgotada"
    try:
        async with httpx.AsyncClient(proxy=proxy, timeout=60, follow_redirects=True,
                                     headers=headers) as client:
            for i, (aid, doi) in enumerate(alvo, 1):
                try:
                    estado, det = await tenta(client, doi)
                except Bloqueio as e:
                    motivo_parada = f"BLOQUEIO -- {e}"
                    log(f"  [{i}/{len(alvo)}] {doi}: !! {e}", fh)
                    break
                except Exception as e:
                    estado, det = "sem_pdf", f"{type(e).__name__}: {e}"

                if estado == "ok":
                    ok += 1
                    seguidas = 0
                    log(f"  [{i}/{len(alvo)}] {doi}: OK -> {os.path.basename(det)}", fh)
                else:
                    falhas += 1
                    seguidas += 1
                    log(f"  [{i}/{len(alvo)}] {doi}: sem PDF ({det})", fh)
                    if seguidas >= args.max_falhas_seguidas:
                        motivo_parada = (f"PARADA PREVENTIVA -- {seguidas} falhas seguidas "
                                         f"(possivel bloqueio silencioso)")
                        log(f"  !! {motivo_parada}", fh)
                        break

                if i < len(alvo):
                    await asyncio.sleep(args.pausa + random.uniform(0, args.pausa * 0.3))
    finally:
        dt = time.time() - t0
        tent = ok + falhas
        taxa = (100.0 * ok / tent) if tent else 0.0
        log(f"=== fim: {ok} OK / {falhas} sem PDF de {tent} tentativas "
            f"({taxa:.1f}%) em {dt/60:.1f} min -- {motivo_parada} ===", fh)
        fh.close()
        print("\nPDFs ficaram em disco. Para leva-los ao banco:")
        print("    python reconcilia_pdfs.py --aplicar")


if __name__ == "__main__":
    asyncio.run(main())
