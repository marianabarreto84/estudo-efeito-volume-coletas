# =====================================================================
#  Progresso e previsao de termino da extracao.
#
#  Existe para que a Mariana nao dependa de uma sessao aberta para saber
#  se a extracao anda. Le so o log -- nao toca no banco, nao interfere.
#
#  ⚠ Lembrete da armadilha de 23/ago/2026: o laco anterior gravou
#  "codigo 0" (sucesso) por cima de um erro, e ninguem percebeu por 17
#  dias. Por isso este script NAO confia na ultima linha: ele mede se o
#  arquivo cresceu, e avisa quando parou de crescer.
#
#  Uso:  python progresso_extracao.py
#        python progresso_extracao.py --log <caminho>
# =====================================================================
import argparse
import os
import re
import time
from datetime import datetime, timedelta

REPO = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
LOG_PADRAO = os.path.join(REPO, "pdfs", ".extracao_expansao.log")

RE_HORA = re.compile(r"^\[(\d{2}):(\d{2}):(\d{2})\]")
RE_TOTAL = re.compile(r"\[analyze_pdfs\]\s+(\d+)\s+artigos")


def hhmmss(seg):
    seg = int(max(0, seg))
    h, r = divmod(seg, 3600)
    m, s = divmod(r, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default=LOG_PADRAO)
    a = ap.parse_args()

    if not os.path.isfile(a.log):
        raise SystemExit(f"log nao encontrado: {a.log}")

    with open(a.log, encoding="utf-8", errors="replace") as f:
        linhas = f.readlines()

    total = 0
    ok = falhas = 0
    primeira = ultima = None
    for ln in linhas:
        m = RE_TOTAL.search(ln)
        if m and not total:
            total = int(m.group(1))
        if "gemini✓" in ln:
            ok += 1
        elif "gemini✗" in ln:
            falhas += 1
        else:
            continue
        h = RE_HORA.match(ln)
        if h:
            t = timedelta(hours=int(h.group(1)), minutes=int(h.group(2)), seconds=int(h.group(3)))
            primeira = primeira or t
            ultima = t

    feitos = ok + falhas
    resta = max(0, total - feitos)
    print(f"log ......... {a.log}")
    print(f"alvo ........ {total} artigos")
    print(f"concluidos .. {feitos}  ({ok} OK / {falhas} falhas"
          + (f", {100*falhas/feitos:.1f}% de falha)" if feitos else ")"))
    if total:
        print(f"progresso ... {100*feitos/total:.1f}%")
    print(f"restam ...... {resta}")

    # o log parou de crescer?
    parado_ha = time.time() - os.path.getmtime(a.log)
    print(f"\nultima escrita no log ha {hhmmss(parado_ha)}")

    if primeira and ultima and feitos > 5:
        decorrido = (ultima - primeira).total_seconds()
        taxa = feitos / decorrido if decorrido else 0
        if taxa:
            print(f"ritmo ....... {taxa*60:.1f} artigos/min")
            fim = datetime.now() + timedelta(seconds=resta / taxa)
            print(f"previsao .... {fim.strftime('%H:%M')}  (faltam ~{hhmmss(resta/taxa)})")

    print()
    if resta == 0:
        print("✅ TERMINOU. Proximo passo: expansao/RETOMAR.md secao 3.2")
    elif parado_ha > 900:
        print("⚠ O log nao cresce ha mais de 15 min. Pode ter travado ou caido.")
        print("  Confira se o processo vive:  tasklist | findstr python")
        print("  Nada se perde: o analyze_pdfs grava por artigo, e relancar pula")
        print("  os que ja tem analise. Ver RETOMAR.md secao 3.1.")
    else:
        print("◐ rodando. Nada mais pode escrever no research.db ate terminar.")


if __name__ == "__main__":
    main()
