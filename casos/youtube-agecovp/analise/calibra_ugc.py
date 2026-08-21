"""
Calibra a regra UGC no GABARITO do artigo, para tornar o alvo-teste AG3 testavel.

O problema
----------
AG3 diz "UGC representa menos de 7%" — mas o artigo nao publica a regra que separa
usuario de veiculo, e o gabarito nao traz a coluna. Sem regra, AG3 nao e testavel.

A saida
-------
Ajustar o limiar de inscritos de `core.regras.eh_ugc` de modo que a regra reproduza
o "<7%" **sobre o corpus do proprio artigo** (3.782 videos x 2.243 canais). Um
limiar que reproduz o numero publicado e evidencia de que a regra capta o que os
autores captaram. So depois ela e aplicada a nossa coleta.

Ressalva registrada: isto e calibragem, nao descoberta. O valor absoluto de AG3
passa a ser, por construcao, proximo do publicado. O que a Fase 3 mede e a
DIFERENCA entre os dois lados do filtro sob a mesma regra — e essa diferenca nao e
afetada pela calibragem.

Uso: PYTHONIOENCODING=utf-8 python -u analise/calibra_ugc.py
Saida: stdout + data/repl/agecovp2020/calibragem_ugc.json
"""
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.regras import eh_ugc, no_tema

csv.field_size_limit(10 ** 8)
G = pathlib.Path("data/repl/agecovp2020/gabarito_zenodo")
OUT = pathlib.Path("data/repl/agecovp2020/calibragem_ugc.json")
LIMIARES = [1000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]
ALVO = 7.0     # "UGC accounts for less than 7%"


def le(nome):
    with open(G / nome, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def main():
    ch = {r["Channel_id"]: r for r in le("channels.csv")}
    vids = le("videos.csv")
    kid = list(vids[0])[0]          # 1a coluna traz BOM
    log = print

    log("videos no gabarito: %d | canais: %d" % (len(vids), len(ch)))
    sem_canal = sum(1 for v in vids if v.get("Channel_id") not in ch)
    log("videos cujo canal nao esta em channels.csv: %d" % sem_canal)

    log("\n%-12s %14s %14s %8s" % ("limiar", "UGC (videos)", "UGC (canais)", "erro"))
    melhor, melhor_err = None, 1e9
    tabela = {}
    for lim in LIMIARES:
        n_ugc_v = 0
        n_v = 0
        for v in vids:
            c = ch.get(v.get("Channel_id"))
            if not c:
                continue
            n_v += 1
            if eh_ugc(c.get("Title"), c.get("Subscriptions"), lim):
                n_ugc_v += 1
        n_ugc_c = sum(1 for c in ch.values()
                      if eh_ugc(c.get("Title"), c.get("Subscriptions"), lim))
        pv = 100 * n_ugc_v / n_v if n_v else 0
        pc = 100 * n_ugc_c / len(ch)
        err = abs(pv - ALVO)
        tabela[str(lim)] = {"ugc_videos_pct": round(pv, 1), "ugc_canais_pct": round(pc, 1)}
        log("%-12s %13.1f%% %13.1f%% %7.1f" % ("{:,}".format(lim), pv, pc, err))
        if err < melhor_err:
            melhor, melhor_err = lim, err

    log("\n-> limiar que melhor reproduz o '<7%%' do artigo: **%s inscritos** "
        "(UGC = %.1f%% dos videos, erro %.1f p.p.)"
        % ("{:,}".format(melhor), tabela[str(melhor)]["ugc_videos_pct"], melhor_err))

    # quanto do corpus do artigo esta "no tema" pela nossa regra independente?
    n_tema = sum(1 for v in vids if no_tema(v.get("Title"), v.get("Description"),
                                            v.get("Tags", "")))
    log("\ncontrole: a regra `no_tema` aprova %d de %d videos do corpus do artigo (%.1f%%)"
        % (n_tema, len(vids), 100 * n_tema / len(vids)))
    log("  (esperado ALTO — e o corpus que o artigo declara ser sobre o tema; se for")
    log("   baixo, a regra `no_tema` esta severa demais e precisa ser afrouxada)")

    OUT.write_text(json.dumps({"alvo_AG3": ALVO, "limiares": tabela,
                               "limiar_escolhido": melhor,
                               "erro_pp": round(melhor_err, 1),
                               "controle_no_tema_pct": round(100 * n_tema / len(vids), 1)},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    log("\nescrito em %s" % OUT)


if __name__ == "__main__":
    main()
