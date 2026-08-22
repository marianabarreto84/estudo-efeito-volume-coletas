#!/usr/bin/env python3
"""Dimensiona a populacao de um conjunto de subreddits numa janela, pelo Arctic Shift.

Roda sozinho, sem nada do terminal alem de `python`. Escreve tudo em disco: resultado
em JSON, log em texto, e um arquivo de progresso que torna a execucao **retomavel** —
se cair, ou se voce fechar, e so rodar de novo que ele continua de onde parou.

    python pipeline/dimensiona.py                  # caso melton (o padrao)
    python pipeline/dimensiona.py --caso massachs  # reconferencia do reddit-massachs
    python pipeline/dimensiona.py --listar         # so mostra o que falta, sem consultar

Nao tem dependencia externa (so biblioteca padrao) e nao gasta LLM nenhum.

⚠ E LENTO DE PROPOSITO. O Arctic Shift estrangula quem insiste, e a medicao de
22/ago/2026 mostrou que ele precisa de ~300 s de silencio para se recuperar. O script
espera 15 s entre consultas e 300 s quando leva um nao. Nos subreddits grandes isso da
horas. Pode deixar rodando e ir fazer outra coisa: o progresso e gravado a cada janela
fechada, e nada se perde.

Por que o metodo e esse, e nao "dividir o intervalo ao meio": ver `core/agregacao.py`.
"""
import argparse
import json
import pathlib
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.agregacao import conta_janela  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[1]


def ts(a, m, d):
    return int(datetime(a, m, d, tzinfo=timezone.utc).timestamp())


CASOS = {
    # -------------------------------------------------------------- caso Melton 2021
    "melton": {
        "descricao": "Melton et al. 2021 — 13 subreddits, 01/dez/2020 a 15/mai/2021",
        "saida": RAIZ / "data/repl/melton2021",
        "prefixo": "volume_portao1",
        "tipos": ["posts", "comments"],
        "corpus_do_alvo": 11641,
        "janelas": {"artigo": (ts(2020, 12, 1), ts(2021, 5, 16))},
        "subreddits": ["Vaccines", "CovidVaccine", "CovidVaccinated", "AntiVaxxers",
                       "vaxxhappened", "antivaccine", "conspiracy", "conspiracytheories",
                       "NoNewNormal", "conspiracy_commons", "COVID19", "COVID",
                       "coronavirus"],
        # medidos em 22/ago/2026 por 2 rodadas independentes e concordantes
        "ja_medidos": RAIZ / "data/repl/melton2021/volume_portao1_parcial.json",
    },
    # ------------------------------------------- reconferencia do caso Massachs 2020
    # A Fase 3 de la foi declarada "nao dimensionavel" com 34/34 falhas — pela MESMA
    # mensagem de erro que aqui se descobriu ser ambigua. Aquela sonda consultava mes a
    # mes, em sequencia, sem recuo: e a receita do estrangulamento. Esta entrada existe
    # para refazer a conta com paciencia e ver se o veredito muda. Ver ESTADO.md §4.23.
    "massachs": {
        "descricao": "Massachs et al. 2020 — 34 subreddits politicos, 2012 e 2016",
        "saida": RAIZ.parent / "reddit-massachs/data/repl/massachs2016",
        "prefixo": "volume_fase3_paciente",
        "tipos": ["comments"],          # a expansao de la so precisa de comentarios
        "corpus_do_alvo": None,
        "janelas": {"2012": (ts(2012, 1, 1), ts(2013, 1, 1)),
                    "2016": (ts(2016, 1, 1), ts(2017, 1, 1))},
        "subreddits": ["politics", "news", "worldnews", "Libertarian", "GaryJohnson",
                       "TrueReddit", "PoliticalHumor", "atheism", "Documentaries",
                       "todayilearned", "conspiracy", "progressive", "POLITIC",
                       "Futurology", "Conservative", "Economics", "Liberal", "law",
                       "Ask_Politics", "ShitPoliticsSays", "dataisbeautiful",
                       "PoliticalDiscussion", "moderatepolitics", "worldpolitics",
                       "WikiLeaks", "economy", "NeutralPolitics", "Republican",
                       "AmericanPolitics", "lostgeneration", "uspolitics", "democrats",
                       "inthenews", "on"],
        "ja_medidos": None,
    },
}

TAXA_ITENS_POR_S = 95.0   # medida na coleta do caso Buntain (ago/2026)
ROTULO = {"posts": "submissoes", "comments": "comentarios"}


def carrega(cfg):
    """Estado inicial: o que ja foi medido antes (e nao precisa ser consultado)."""
    est = {}
    jm = cfg.get("ja_medidos")
    if jm and pathlib.Path(jm).exists():
        d = json.load(open(jm, encoding="utf-8"))
        for s, v in d.get("medidos", {}).items():
            est[s] = {"artigo": {"submissoes": v["submissoes"],
                                 "comentarios": v["comentarios"]},
                      "completo": True,
                      "origem": "sonda de 22/ago/2026 (2 rodadas concordantes)"}
    prog = cfg["saida"] / (cfg["prefixo"] + "_progresso.json")
    if prog.exists():
        est.update(json.load(open(prog, encoding="utf-8")))
    return est


def falta(cfg, est):
    return [s for s in cfg["subreddits"] if not est.get(s, {}).get("completo")]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--caso", default="melton", choices=sorted(CASOS))
    ap.add_argument("--listar", action="store_true",
                    help="so mostra o que ja foi medido e o que falta; nao consulta")
    args = ap.parse_args()

    cfg = CASOS[args.caso]
    cfg["saida"].mkdir(parents=True, exist_ok=True)
    est = carrega(cfg)
    pendentes = falta(cfg, est)

    print("Caso: %s" % cfg["descricao"])
    print("Subreddits: %d — ja medidos %d, faltam %d"
          % (len(cfg["subreddits"]), len(cfg["subreddits"]) - len(pendentes),
             len(pendentes)))
    if args.listar:
        for s in cfg["subreddits"]:
            print("  %-22s %s" % (s, "ok" if s not in pendentes else "FALTA"))
        return 0
    if not pendentes:
        print("Nada a fazer — todos medidos.")
    else:
        print("Faltam: %s" % ", ".join(pendentes))
    print("\n⚠ Isto e lento de proposito (15s entre consultas, 300s quando leva um nao).")
    print("   Pode deixar rodando; o progresso e gravado a cada janela fechada.\n")

    log_path = cfg["saida"] / (cfg["prefixo"] + ".log")
    flog = open(log_path, "a", encoding="utf-8")

    def log(m):
        print(m)
        sys.stdout.flush()
        flog.write("%s  %s\n" % (datetime.now().strftime("%d/%m %H:%M:%S"), m))
        flog.flush()

    log("=== inicio: caso %s, %d pendentes ===" % (args.caso, len(pendentes)))
    t_inicio = time.time()

    for i, sub in enumerate(pendentes, 1):
        log("[%d/%d] %s" % (i, len(pendentes), sub))
        linha = est.get(sub, {})
        linha["origem"] = "sonda paciente"
        completo = True
        for jrot, (a, b) in cfg["janelas"].items():
            linha.setdefault(jrot, {})
            for kind in cfg["tipos"]:
                rot = ROTULO[kind]
                if linha[jrot].get(rot) is not None:
                    continue                      # ja medido numa execucao anterior
                r = conta_janela(kind, sub, a, b, log=log)
                linha[jrot][rot] = r["total"] if r["completo"] else None
                linha[jrot][rot + "_diag"] = {k: r[k] for k in
                                              ("completo", "ladrilho_final_d", "chamadas",
                                               "descansos", "encolhidas", "segundos",
                                               "motivos")}
                completo = completo and r["completo"]
                log("    %-9s %-12s %s (ladrilho %.1fd, %d chamadas, %d descansos, %.0fs)"
                    % (jrot, rot,
                       "{:,}".format(r["total"]) if r["completo"] else "INCOMPLETO",
                       r["ladrilho_final_d"], r["chamadas"], r["descansos"],
                       r["segundos"]))
        linha["completo"] = completo
        est[sub] = linha
        (cfg["saida"] / (cfg["prefixo"] + "_progresso.json")).write_text(
            json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---------------------------------------------------------------- relatorio final
    incompletos = falta(cfg, est)
    somas = {j: {ROTULO[k]: 0 for k in cfg["tipos"]} for j in cfg["janelas"]}
    for s in cfg["subreddits"]:
        v = est.get(s, {})
        if not v.get("completo"):
            continue
        for j in cfg["janelas"]:
            for k in cfg["tipos"]:
                somas[j][ROTULO[k]] += (v.get(j) or {}).get(ROTULO[k]) or 0

    log("")
    cab = "%-22s" % "subreddit"
    for j in cfg["janelas"]:
        for k in cfg["tipos"]:
            cab += " %16s" % ("%s/%s" % (j, ROTULO[k]))[:16]
    log(cab)
    for s in cfg["subreddits"]:
        v = est.get(s, {})
        ln = "%-22s" % s
        for j in cfg["janelas"]:
            for k in cfg["tipos"]:
                x = (v.get(j) or {}).get(ROTULO[k]) if v.get("completo") else None
                ln += " %16s" % ("{:,}".format(x) if x is not None else "INCOMPLETO")
        log(ln)

    total = sum(somas[j][ROTULO[k]] for j in cfg["janelas"] for k in cfg["tipos"])
    log("%-22s %s" % ("SOMA" if not incompletos else "SOMA PARCIAL",
                      "  ".join("%s/%s=%s" % (j, r, "{:,}".format(v))
                                for j, d in somas.items() for r, v in d.items())))

    if incompletos:
        log("\n[!] %d sem contagem: %s" % (len(incompletos), ", ".join(incompletos)))
        log("[!] A SOMA ACIMA E PARCIAL e NAO e a populacao.")
    else:
        horas = total / TAXA_ITENS_POR_S / 3600
        log("\nPOPULACAO: {:,} itens".format(total))
        log("a %.0f itens/s (taxa medida no caso Buntain): %.1f h (%.2f dias) de API"
            % (TAXA_ITENS_POR_S, horas, horas / 24))
        if cfg.get("corpus_do_alvo"):
            log("razao contra o corpus do alvo (%s): %.1fx"
                % ("{:,}".format(cfg["corpus_do_alvo"]), total / cfg["corpus_do_alvo"]))

    saida = cfg["saida"] / (cfg["prefixo"] + ".json")
    saida.write_text(json.dumps({
        "caso": args.caso,
        "descricao": cfg["descricao"],
        "fonte": "arctic-shift.photon-reddit.com (agregacao)",
        "metodo": "ladrilho adaptativo com descanso de 300s; o descanso separa "
                  "estrangulamento de tamanho — ver core/agregacao.py",
        "janelas": {j: {"after": a, "before": b} for j, (a, b) in cfg["janelas"].items()},
        "COMPLETO": not incompletos,
        "incompletos": incompletos,
        "subreddits": est,
        "somas": somas,
        "soma_total": total,
        "corpus_do_alvo": cfg.get("corpus_do_alvo"),
        "razao_contra_corpus_do_alvo": (round(total / cfg["corpus_do_alvo"], 2)
                                        if cfg.get("corpus_do_alvo") and not incompletos
                                        else None),
        "taxa_itens_por_s": TAXA_ITENS_POR_S,
        "aviso": None if not incompletos else
                 "PARCIAL: %d sem contagem; a soma NAO e a populacao" % len(incompletos),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    log("escrito em %s" % saida)
    log("=== fim (%.0f min) ===" % ((time.time() - t_inicio) / 60))
    flog.close()
    return 0 if not incompletos else 1


if __name__ == "__main__":
    sys.exit(main())
