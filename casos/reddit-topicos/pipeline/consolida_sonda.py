#!/usr/bin/env python3
"""Consolida as duas rodadas da sonda de volume num JSON congelado (Portao 1b).

Por que existe
--------------
A sonda foi interrompida pelo rate limit do Arctic Shift antes de fechar os 13
subreddits (ver PORTAO1_relatorio.md §3). O que ela alcancou — os 6 subreddits
menores — foi medido DUAS VEZES, em rodadas independentes, e as duas rodadas
concordam item a item. Este script le os dois logs, exige a concordancia e so
entao grava o parcial. Assim nenhum numero do caso e digitado a mao (CLAUDE.md §7).

⚠ O JSON resultante e explicitamente PARCIAL. A chave COMPLETO fica false e a soma
NAO e o universo — 7 dos 13 subreddits, entre eles os tres maiores, nao foram
medidos. Nunca citar a soma como populacao.

Uso: PYTHONIOENCODING=utf-8 python -u pipeline/consolida_sonda.py
Saida: data/repl/melton2021/volume_portao1_parcial.json
"""
import json
import pathlib
import re
import sys

LOGS = {
    "rodada1": pathlib.Path("data/repl/melton2021/logs/sonda_rodada1.log"),
    "rodada2": pathlib.Path("data/repl/melton2021/logs/sonda_rodada2.log"),
}
OUT = pathlib.Path("data/repl/melton2021/volume_portao1_parcial.json")

SUBS = ["Vaccines", "CovidVaccine", "CovidVaccinated", "AntiVaxxers", "vaxxhappened",
        "antivaccine", "conspiracy", "conspiracytheories", "NoNewNormal",
        "conspiracy_commons", "COVID19", "COVID", "coronavirus"]

LINHA = re.compile(r"^(\S+)\s+([\d,]+)\s+([\d,]+)\s+(\d+)\s+(\d+)\s*([dh])\s*$")


def le(p):
    out = {}
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        m = LINHA.match(ln)
        if not m or m.group(1) not in SUBS:
            continue
        out[m.group(1)] = {
            "submissoes": int(m.group(2).replace(",", "")),
            "comentarios": int(m.group(3).replace(",", "")),
            "chamadas": int(m.group(4)),
            "menor_janela_que_respondeu": m.group(5) + m.group(6),
        }
    return out


def main():
    r = {k: le(p) for k, p in LOGS.items()}
    for k, v in r.items():
        print("%s: %d subreddits" % (k, len(v)))

    comuns = sorted(set(r["rodada1"]) & set(r["rodada2"]), key=SUBS.index)
    medidos, divergentes = {}, []
    for s in comuns:
        a, b = r["rodada1"][s], r["rodada2"][s]
        if a["submissoes"] != b["submissoes"] or a["comentarios"] != b["comentarios"]:
            divergentes.append(s)
            continue
        medidos[s] = {
            "submissoes": a["submissoes"],
            "comentarios": a["comentarios"],
            "total": a["submissoes"] + a["comentarios"],
            "confirmado_em_2_rodadas": True,
            "chamadas_rodada1": a["chamadas"],
            "chamadas_rodada2": b["chamadas"],
        }

    if divergentes:
        print("[!] rodadas discordam em: %s — nao gravado" % ", ".join(divergentes))

    faltam = [s for s in SUBS if s not in medidos]
    ts = sum(v["submissoes"] for v in medidos.values())
    tc = sum(v["comentarios"] for v in medidos.values())

    print("\n%-22s %12s %14s" % ("subreddit", "submissoes", "comentarios"))
    for s, v in medidos.items():
        print("%-22s %12s %14s" % (s, "{:,}".format(v["submissoes"]),
                                   "{:,}".format(v["comentarios"])))
    print("%-22s %12s %14s" % ("PARCIAL (%d/13)" % len(medidos),
                               "{:,}".format(ts), "{:,}".format(tc)))
    print("\n[!] NAO medidos (%d): %s" % (len(faltam), ", ".join(faltam)))
    print("[!] A soma acima NAO e o universo.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "fonte": "arctic-shift.photon-reddit.com (agregacao)",
        "janela": "2020-12-01T00:00:00Z a 2021-05-16T00:00:00Z (exclusivo)",
        "COMPLETO": False,
        "motivo_incompleto": "rate limit do Arctic Shift ('Timeout. Maybe slow down "
                             "a bit'); o prompt do caso manda parar, nao contornar",
        "medidos": medidos,
        "nao_medidos": faltam,
        "soma_parcial_submissoes": ts,
        "soma_parcial_comentarios": tc,
        "soma_parcial_total": ts + tc,
        "aviso": "PARCIAL: 7 de 13 subreddits nao medidos, entre eles os 3 maiores "
                 "(conspiracy, COVID19, coronavirus). A soma NAO e a populacao.",
        "corpus_do_alvo": {"submissoes": 1401, "comentarios": 10240, "total": 11641},
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nescrito em %s" % OUT)
    return 0 if not divergentes else 1


if __name__ == "__main__":
    sys.exit(main())
