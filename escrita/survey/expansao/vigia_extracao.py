# =====================================================================
#  Vigia da extracao — fica olhando e avisa quando acabar (ou travar).
#
#  Nao precisa do Claude nem de sessao aberta: roda no terminal da
#  Mariana, sozinho. Le so o log; nao toca no research.db.
#
#  Avisa de tres formas, para nao depender de a janela estar visivel:
#    1. imprime uma linha de status a cada checagem
#    2. bipa (console beep)
#    3. abre uma caixa de mensagem do Windows
#
#  ⚠ Detecta TRAVAMENTO, nao so termino. A armadilha de 23/ago/2026 foi
#  um laco que gravou "codigo 0" sobre um erro e ninguem viu por 17 dias.
#  Aqui, se o log parar de crescer por --paciencia minutos, ele grita.
#
#  Uso:
#    python vigia_extracao.py                  # checa a cada 5 min
#    python vigia_extracao.py --intervalo 60   # a cada 1 min
#    python vigia_extracao.py --paciencia 20   # tolera 20 min de silencio
# =====================================================================
import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta

REPO = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
LOG = os.path.join(REPO, "pdfs", ".extracao_expansao.log")
RE_HORA = re.compile(r"^\[(\d{2}):(\d{2}):(\d{2})\]")
RE_TOTAL = re.compile(r"\[analyze_pdfs\]\s+(\d+)\s+artigos")


def le(log):
    """(total, feitos, ok, falhas, primeira, ultima) a partir do log."""
    if not os.path.isfile(log):
        return 0, 0, 0, 0, None, None
    total = ok = falhas = 0
    primeira = ultima = None
    with open(log, encoding="utf-8", errors="replace") as f:
        for ln in f:
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
                t = timedelta(hours=int(h.group(1)), minutes=int(h.group(2)),
                              seconds=int(h.group(3)))
                primeira = primeira or t
                ultima = t
    return total, ok + falhas, ok, falhas, primeira, ultima


def avisa(titulo, corpo):
    """Bipa e abre uma caixa de mensagem. Falha em silencio se nao der."""
    try:
        import winsound
        for _ in range(3):
            winsound.Beep(880, 400)
            time.sleep(0.15)
    except Exception:
        print("\a", end="", flush=True)
    try:
        ps = (f'Add-Type -AssemblyName PresentationFramework;'
              f'[System.Windows.MessageBox]::Show('
              f'"{corpo}","{titulo}") | Out-Null')
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps])
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default=LOG)
    ap.add_argument("--intervalo", type=int, default=300, help="segundos entre checagens")
    ap.add_argument("--paciencia", type=int, default=15,
                    help="minutos de log parado antes de considerar travado")
    a = ap.parse_args()

    print(f"vigiando {a.log}")
    print(f"checando a cada {a.intervalo}s; alarme de travamento em {a.paciencia} min\n")
    print("(deixe esta janela aberta; Ctrl+C para parar)\n")

    while True:
        total, feitos, ok, falhas, pri, ult = le(a.log)
        parado = (time.time() - os.path.getmtime(a.log)) / 60 if os.path.isfile(a.log) else 1e9
        resta = max(0, total - feitos)
        agora = datetime.now().strftime("%H:%M:%S")

        prev = ""
        if pri and ult and feitos > 5:
            dec = (ult - pri).total_seconds()
            if dec > 0:
                taxa = feitos / dec
                if taxa > 0 and resta:
                    fim = datetime.now() + timedelta(seconds=resta / taxa)
                    prev = f" | previsao {fim.strftime('%H:%M')}"

        pct = (100 * feitos / total) if total else 0
        print(f"[{agora}] {feitos}/{total} ({pct:.1f}%)  "
              f"{ok} OK / {falhas} falhas  | parado ha {parado:.0f} min{prev}")

        if total and resta == 0:
            msg = (f"Extracao concluida: {ok} OK e {falhas} falhas de {total}. "
                   f"Proximo passo: expansao/RETOMAR.md secao 3.2 "
                   f"(reconciliar a sonda e extrair os 199).")
            print("\n✅ " + msg)
            avisa("Extracao TERMINOU", msg)
            return 0

        if parado > a.paciencia:
            msg = (f"O log nao cresce ha {parado:.0f} min. Parou em {feitos}/{total}. "
                   f"Nada se perde: o analyze_pdfs grava artigo a artigo e relancar "
                   f"pula quem ja tem analise. Ver RETOMAR.md secao 3.1.")
            print("\n⚠ " + msg)
            avisa("Extracao TRAVOU?", msg)
            return 1

        time.sleep(a.intervalo)


if __name__ == "__main__":
    sys.exit(main())
