#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fase 3 - AG1 e AG2 sobre a NOSSA coleta (eixo dos comentarios).

O que testa
-----------
AG1  distribuicao de sentimento dos comentarios. O artigo publica, sobre o corpus
     dele, TextBlob 39 neutro / 39 positivo / 22 negativo.
     Predicao pre-registrada P2: **AG1 muda** - ao soltar o filtro, a distribuicao
     fica MAIS NEGATIVA (conteudo institucional e mais neutro; entra reclamacao).
AG2  os comentarios sao mais negativos que os videos.
     Predicao pre-registrada P3: **AG2 nao muda** - e comparacao entre dois niveis
     do mesmo corpus, e o vies do filtro atinge os dois.

Desenho
-------
Compara os dois lados do filtro de palavra-chave (passa_filtro 1 x 0), restrito aos
videos que passam no teste de tema independente (core.regras.no_tema), que e a mesma
restricao usada em fase3_no_tema.py e fase3_ugc_completo.py. Sem essa restricao a
comparacao mede ruido de busca, nao vies - foi a armadilha da primeira rodada.

Instrumento fixado ao do artigo, com as MESMAS convencoes de fase2_ponto_original.py:
  TextBlob  positivo se polarity > 0, negativo se < 0, neutro se == 0
  VADER     positivo se compound > 0.05, negativo se < -0.05, neutro entre
O limiar de neutralidade nao e declarado pelo artigo (ver DECISOES_regras.md D1); por
isso os dois instrumentos sao reportados lado a lado.

Bandas: reamostragem POR VIDEO (nao por comentario). Comentarios sao aninhados em
videos; reamostrar comentario a comentario infla o n e estreita a banda de mentira.

Uso: python analise/fase3_comentarios.py [--replicas 300]
"""
import argparse
import collections
import json
import io
import os
import random
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.regras import no_tema  # noqa: E402

from textblob import TextBlob  # noqa: E402
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(AQUI, "..", "data", "repl", "agecovp2020", "snapshot_agecovp.sqlite")
SAIDA = os.path.join(AQUI, "..", "data", "repl", "agecovp2020",
                     "fase3_comentarios.json")
SEED = 20260821
ALVO_TEXTBLOB = {"neutro": 39, "positivo": 39, "negativo": 22}

_vader = SentimentIntensityAnalyzer()


def classifica_tb(texto):
    p = TextBlob(texto).sentiment.polarity
    return ("positivo" if p > 0 else "negativo" if p < 0 else "neutro"), p


def classifica_vd(texto):
    c = _vader.polarity_scores(texto)["compound"]
    return ("positivo" if c > 0.05 else "negativo" if c < -0.05 else "neutro"), c


def pct(cont):
    t = sum(cont.values())
    return {k: round(100.0 * v / t, 1) for k, v in sorted(cont.items())} if t else {}


def escrita_latina(texto):
    """Heuristica: >90% das letras em ASCII.

    Nao e deteccao de idioma - e o recorte onde os dois instrumentos do artigo
    tem alguma chance de significar algo. Comentario em escrita nao-latina faz
    TextBlob e VADER devolverem 0, que a convencao do artigo conta como
    'neutro'; isso infla o neutro sem que ninguem tenha escrito nada neutro.
    Medido em 21/ago/2026 sobre a coleta parcial: ~10% dos comentarios caem
    fora deste recorte.
    """
    letras = [c for c in texto if c.isalpha()]
    if not letras:
        return False
    return sum(1 for c in letras if ord(c) < 128) / len(letras) > 0.9


def banda(valores_por_video, replicas, agg):
    """Percentis 2,5 e 97,5 reamostrando VIDEOS com reposicao."""
    if not valores_por_video:
        return (None, None)
    rnd = random.Random(SEED)
    n = len(valores_por_video)
    saidas = []
    for _ in range(replicas):
        amostra = [valores_por_video[rnd.randrange(n)] for _ in range(n)]
        v = agg([x for grupo in amostra for x in grupo])
        if v is not None:
            saidas.append(v)
    saidas.sort()
    if not saidas:
        return (None, None)
    lo = saidas[max(0, int(0.025 * len(saidas)) - 1)]
    hi = saidas[min(len(saidas) - 1, int(0.975 * len(saidas)))]
    return (round(lo, 4), round(hi, 4))


def banda_diferenca(grupos_a, grupos_b, replicas, agg):
    """IC95 da DIFERENCA b - a, reamostrando videos dentro de cada estrato.

    Comparar duas bandas separadas e teste conservador: bandas podem se
    sobrepor e a diferenca ainda excluir zero. O resto da Fase 3
    (fase3_ugc_completo.py) reporta IC na diferenca; aqui e igual.
    """
    if not grupos_a or not grupos_b:
        return (None, None)
    rnd = random.Random(SEED)
    na, nb = len(grupos_a), len(grupos_b)
    saidas = []
    for _ in range(replicas):
        aa = [x for _ in range(na) for x in grupos_a[rnd.randrange(na)]]
        bb = [x for _ in range(nb) for x in grupos_b[rnd.randrange(nb)]]
        va, vb = agg(aa), agg(bb)
        if va is not None and vb is not None:
            saidas.append(vb - va)
    if not saidas:
        return (None, None)
    saidas.sort()
    lo = saidas[max(0, int(0.025 * len(saidas)) - 1)]
    hi = saidas[min(len(saidas) - 1, int(0.975 * len(saidas)))]
    return (round(lo, 3), round(hi, 3))


def media(xs):
    return sum(xs) / len(xs) if xs else None


def frac(classe):
    def _f(rotulos):
        return (100.0 * sum(1 for r in rotulos if r == classe) / len(rotulos)
                if rotulos else None)
    return _f


frac_neg = frac("negativo")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicas", type=int, default=300)
    a = ap.parse_args()

    if not os.path.exists(DB):
        sys.exit("snapshot nao encontrado: %s" % DB)
    cx = sqlite3.connect(DB)

    # --- videos com comentarios ja coletados, restritos ao tema -----------
    videos = {}
    for vid, pf, tit, desc in cx.execute(
            "SELECT v.video_id, v.passa_filtro, v.title, v.description FROM videos v "
            "JOIN log_comentarios l ON l.video_id = v.video_id AND l.done = 1"):
        tit, desc = tit or "", desc or ""
        if not no_tema(tit, desc):
            continue
        videos[vid] = {"passa": int(pf), "titulo": tit, "desc": desc}

    coments = collections.defaultdict(list)
    for vid, txt in cx.execute("SELECT video_id, texto FROM comentarios"):
        if vid in videos and txt and txt.strip():
            coments[vid].append(txt.strip())

    # --- atrito: quase metade dos videos nao tem comentario algum ----------
    # (desativados ou zero). AG1/AG2 acabam medidos num sub-estrato do
    # sub-estrato, entao e preciso checar se esse atrito e enviesado pelo
    # filtro - se fosse, contaminaria a comparacao inteira.
    atrito = {}
    for nome, quer in (("passa_filtro", 1), ("descartado", 0)):
        vs = [v for v, d in videos.items() if d["passa"] == quer]
        atrito[nome] = {
            "no_tema": len(vs),
            "com_comentario": sum(1 for v in vs if coments.get(v)),
            "pct_com_comentario": round(
                100.0 * sum(1 for v in vs if coments.get(v)) / len(vs), 1) if vs else None,
        }
    rnd = random.Random(SEED)

    def _taxa(vs):
        return 100.0 * sum(1 for v in vs if coments.get(v)) / len(vs) if vs else None

    va = [v for v, d in videos.items() if d["passa"] == 1]
    vb = [v for v, d in videos.items() if d["passa"] == 0]
    difs = []
    for _ in range(300):
        aa = [va[rnd.randrange(len(va))] for _ in va] if va else []
        bb = [vb[rnd.randrange(len(vb))] for _ in vb] if vb else []
        ta, tb2 = _taxa(aa), _taxa(bb)
        if ta is not None and tb2 is not None:
            difs.append(tb2 - ta)
    difs.sort()
    atrito["delta_pp_descartado_menos_passa"] = (
        round(atrito["descartado"]["pct_com_comentario"]
              - atrito["passa_filtro"]["pct_com_comentario"], 1)
        if all(atrito[k]["pct_com_comentario"] is not None
               for k in ("descartado", "passa_filtro")) else None)
    atrito["ic95_da_diferenca"] = (
        (round(difs[int(0.025 * len(difs))], 1), round(difs[int(0.975 * len(difs))], 1))
        if difs else (None, None))
    print("atrito (videos no tema SEM comentario algum): aprovados %s%% x descartados %s%% "
          "| delta %s p.p. IC95 %s"
          % (atrito["passa_filtro"]["pct_com_comentario"],
             atrito["descartado"]["pct_com_comentario"],
             atrito["delta_pp_descartado_menos_passa"], atrito["ic95_da_diferenca"]))

    videos = {v: d for v, d in videos.items() if coments.get(v)}
    print("videos no tema com comentarios: %d | comentarios: %d"
          % (len(videos), sum(len(c) for c in coments.values())))

    # --- rotula ------------------------------------------------------------
    res = {"seed": SEED, "replicas": a.replicas,
           "n_videos": len(videos),
           "n_comentarios": sum(len(coments[v]) for v in videos),
           "alvo_artigo_textblob": ALVO_TEXTBLOB,
           "atrito_sem_comentarios": atrito, "estratos": {}}

    for nome, quer in (("passa_filtro", 1), ("descartado", 0)):
        vids = [v for v, d in videos.items() if d["passa"] == quer]
        cont_tb, cont_vd = collections.Counter(), collections.Counter()
        cont_tb_lat = collections.Counter()
        n_lat = 0
        rot_tb_por_video, pol_com_por_video, pol_vid = [], [], []
        for v in vids:
            rot_v, pol_v = [], []
            for txt in coments[v]:
                t, pt = classifica_tb(txt)
                d, _ = classifica_vd(txt)
                cont_tb[t] += 1
                cont_vd[d] += 1
                if escrita_latina(txt):
                    cont_tb_lat[t] += 1
                    n_lat += 1
                rot_v.append(t)
                pol_v.append(pt)
            rot_tb_por_video.append(rot_v)
            pol_com_por_video.append(pol_v)
            _, pv = classifica_tb((videos[v]["titulo"] + ". " + videos[v]["desc"])[:5000])
            pol_vid.append([pv])

        est = {
            "n_videos": len(vids),
            "n_comentarios": sum(cont_tb.values()),
            "AG1_textblob": pct(cont_tb),
            "AG1_vader": pct(cont_vd),
            "AG1_textblob_so_escrita_latina": pct(cont_tb_lat),
            "n_comentarios_escrita_latina": n_lat,
            "pct_negativo_textblob": round(frac_neg(
                [r for g in rot_tb_por_video for r in g]) or 0, 2),
            "pct_negativo_ic95": banda(rot_tb_por_video, a.replicas, frac_neg),
            "polaridade_media_comentarios": round(media(
                [p for g in pol_com_por_video for p in g]) or 0, 4),
            "polaridade_comentarios_ic95": banda(pol_com_por_video, a.replicas, media),
            "polaridade_media_videos": round(media(
                [p for g in pol_vid for p in g]) or 0, 4),
            "polaridade_videos_ic95": banda(pol_vid, a.replicas, media),
        }
        est["AG2_comentarios_mais_negativos"] = (
            est["polaridade_media_comentarios"] < est["polaridade_media_videos"])
        est["_rot_por_video"] = rot_tb_por_video     # internos, removidos ao gravar
        est["_pol_com"] = pol_com_por_video
        est["_pol_vid"] = pol_vid
        res["estratos"][nome] = est
        print("\n== %s (%d videos, %d comentarios)" % (nome, est["n_videos"],
                                                      est["n_comentarios"]))
        print("   AG1 TextBlob %s | VADER %s" % (est["AG1_textblob"], est["AG1_vader"]))
        print("   AG1 TextBlob so escrita latina (%d de %d): %s"
              % (est["n_comentarios_escrita_latina"], est["n_comentarios"],
                 est["AG1_textblob_so_escrita_latina"]))
        print("   negativos %.2f%% IC95 %s" % (est["pct_negativo_textblob"],
                                               est["pct_negativo_ic95"]))
        print("   polaridade: comentarios %.4f %s | videos %.4f %s -> AG2 %s"
              % (est["polaridade_media_comentarios"], est["polaridade_comentarios_ic95"],
                 est["polaridade_media_videos"], est["polaridade_videos_ic95"],
                 "SIM" if est["AG2_comentarios_mais_negativos"] else "NAO"))

    # --- vereditos das predicoes ------------------------------------------
    p, d = res["estratos"].get("passa_filtro"), res["estratos"].get("descartado")
    if p and d and p["n_comentarios"] and d["n_comentarios"]:
        delta = d["pct_negativo_textblob"] - p["pct_negativo_textblob"]
        ic = banda_diferenca(p["_rot_por_video"], d["_rot_por_video"],
                             a.replicas, frac_neg)
        exclui_zero = ic[0] is not None and (ic[0] > 0 or ic[1] < 0)
        res["P2_AG1"] = {
            "delta_pp_negativos_descartado_menos_passa": round(delta, 2),
            "ic95_da_diferenca": ic,
            "ic95_exclui_zero": bool(exclui_zero),
            "predicao": "descartados mais negativos que aprovados",
            "veredito": ("CONFIRMA" if delta > 0 and exclui_zero else
                         "REFUTA" if delta < 0 and exclui_zero else "INCONCLUSIVO"),
        }
        # A distribuicao inteira, e nao so a classe negativa. P2 foi escrita
        # sobre negatividade; se o que se move for outra classe, a predicao
        # falha mas o efeito existe - e e isso que precisa ficar visivel.
        res["deslocamento_por_classe"] = {}
        for classe in ("positivo", "neutro", "negativo"):
            fa = frac(classe)
            va = fa([r for g in p["_rot_por_video"] for r in g])
            vb = fa([r for g in d["_rot_por_video"] for r in g])
            ic_c = banda_diferenca(p["_rot_por_video"], d["_rot_por_video"],
                                   a.replicas, fa)
            res["deslocamento_por_classe"][classe] = {
                "passa_filtro_pct": round(va, 2), "descartado_pct": round(vb, 2),
                "delta_pp": round(vb - va, 2), "ic95_da_diferenca": ic_c,
                "significativo": bool(ic_c[0] is not None
                                      and (ic_c[0] > 0 or ic_c[1] < 0)),
            }

        # AG2 tambem por IC da diferenca (comentarios - videos), por estrato,
        # em vez de simples comparacao de sinal.
        for nome, est in (("passa_filtro", p), ("descartado", d)):
            ic_ag2 = banda_diferenca(est["_pol_vid"], est["_pol_com"],
                                     a.replicas, media)
            est["AG2_delta_comentarios_menos_videos"] = round(
                est["polaridade_media_comentarios"]
                - est["polaridade_media_videos"], 4)
            est["AG2_ic95_da_diferenca"] = ic_ag2
            est["AG2_significativo"] = bool(ic_ag2[0] is not None
                                            and (ic_ag2[0] > 0 or ic_ag2[1] < 0))

        res["P3_AG2"] = {
            "predicao": "comentarios mais negativos que videos nos dois estratos",
            "veredito": ("CONFIRMA" if (p["AG2_comentarios_mais_negativos"] and
                                        d["AG2_comentarios_mais_negativos"])
                         else "REFUTA"),
            "significativo_nos_dois": bool(p["AG2_significativo"]
                                           and d["AG2_significativo"]),
        }
        print("\n== deslocamento da distribuicao inteira (descartado - aprovado)")
        for classe, v in res["deslocamento_por_classe"].items():
            print("   %-9s %5.1f%% -> %5.1f%%  delta %+5.2f p.p.  IC95 %s%s"
                  % (classe, v["passa_filtro_pct"], v["descartado_pct"],
                     v["delta_pp"], v["ic95_da_diferenca"],
                     "  <- exclui zero" if v["significativo"] else ""))
        print("\n== predicoes pre-registradas")
        print("   P2 (AG1 muda, mais negativo ao soltar o filtro): %s"
              "  (delta %+.2f p.p., IC95 da diferenca %s)"
              % (res["P2_AG1"]["veredito"], delta, ic))
        print("   P3 (AG2 nao muda): %s" % res["P3_AG2"]["veredito"])

    for est in res["estratos"].values():
        for k in ("_rot_por_video", "_pol_com", "_pol_vid"):
            est.pop(k, None)

    tmp = SAIDA + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, SAIDA)
    print("\njson: %s" % os.path.abspath(SAIDA))


if __name__ == "__main__":
    main()
