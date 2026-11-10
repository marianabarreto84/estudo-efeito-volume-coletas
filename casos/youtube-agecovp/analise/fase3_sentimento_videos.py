#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fase 3 - sentimento dos VIDEOS, com e sem o filtro de palavra-chave.

A pergunta
----------
O AGECovP apura o sentimento dos videos "predominantemente positivo" (59% pela
VADER, 72% pela TextBlob) e **explica** esse resultado pela composicao do corpus:
os videos "em sua maioria vem de veiculos de imprensa, e nao de conteudo gerado
por usuarios". A explicacao usa como causa exatamente aquilo que o funil de
coleta produz. Entao: se soltarmos o filtro que descarta os videos de usuario,
o tom continua positivo?

Desenho
-------
1. INSTRUMENTO. O gabarito (Zenodo 15800324) publica `VADER_SenV` e
   `TextBlob_SenV` por video, mas nao diz sobre que texto. Testado campo a campo,
   o par (titulo + " " + descricao) reproduz os valores publicados. O script
   confere isso antes de qualquer outra coisa: se a taxa de reproducao cair,
   o resto nao vale.
2. CONVENCAO. Banda de neutralidade +-0,05, a mesma que a Fase 2 fixou para os
   comentarios (o artigo nao publica o limiar; ver DECISOES_regras.md D1). Os
   limiares 0 e +-0,1 vao ao lado como sensibilidade.
2b. TEXTO. Usa `videos.description_full` (a descricao completa, trazida por
   `pipeline/completa_descricoes.py`), e NAO a coluna `description`, que guarda o
   trecho truncado do `search.list`. Pontuar o trecho truncado subestima a fatia
   de positivos em ~12 p.p. - artefato de coleta, nao de corpus. O truncado vai
   ao lado como sensibilidade, e o passo 0 mede o tamanho do artefato.
3. APLICACAO. O mesmo instrumento sobre a NOSSA coleta, em tres recortes:
   com filtro (passa_filtro=1, o analogo do corpus do artigo), sem filtro
   (tudo o que a busca devolveu) e so os descartados. Duas bases: todos os
   videos coletados e so os que passam no teste de tema independente
   (core.regras.no_tema), que e a base canonica do caso.
4. A EXPLICACAO DO ARTIGO. Dentro do tema, UGC x institucional pela regra
   declarada em core.regras.eh_ugc. Se o tom positivo vem de a imprensa
   dominar, o UGC tem de ser menos positivo.
5. CONVERGENCIA. Curva A(n) da fatia positiva, para responder "ja tinha
   convergido no volume original?".

Bandas: reamostragem de VIDEOS com reposicao, semente fixa.

Uso: python analise/fase3_sentimento_videos.py [--replicas 400]
"""
import argparse
import csv
import json
import os
import random
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.regras import no_tema, eh_ugc, LIMIAR_INSCRITOS  # noqa: E402

from textblob import TextBlob  # noqa: E402
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "..", "data", "repl", "agecovp2020")
DB = os.path.join(D, "snapshot_agecovp.sqlite")
GAB = os.path.join(D, "gabarito_zenodo", "videos.csv")
SAIDA = os.path.join(D, "fase3_sentimento_videos.json")

SEED = 20260928
BANDA = 0.05                                       # limiar de neutralidade (Fase 2)
ALVO = {"vader_pos": 59.0, "textblob_pos": 72.0}   # o que o artigo publica

_vader = SentimentIntensityAnalyzer()
_log = []


def log(s=""):
    print(s)
    _log.append(s)


def pol_vader(t):
    return _vader.polarity_scores(t)["compound"]


def pol_tb(t):
    return TextBlob(t).sentiment.polarity


def classifica(p, banda=BANDA):
    return "positivo" if p > banda else "negativo" if p < -banda else "neutro"


def dist(pols, banda=BANDA):
    n = len(pols)
    if not n:
        return {}
    c = {"positivo": 0, "neutro": 0, "negativo": 0}
    for p in pols:
        c[classifica(p, banda)] += 1
    return {k: round(100.0 * v / n, 1) for k, v in c.items()}


def frac_pos(pols, banda=BANDA):
    return (100.0 * sum(1 for p in pols if p > banda) / len(pols)) if pols else None


def media(xs):
    return sum(xs) / len(xs) if xs else None


def banda_ic(pols, replicas, agg):
    """IC95 reamostrando videos com reposicao."""
    if not pols:
        return (None, None)
    rnd = random.Random(SEED)
    n = len(pols)
    saidas = []
    for _ in range(replicas):
        am = [pols[rnd.randrange(n)] for _ in range(n)]
        v = agg(am)
        if v is not None:
            saidas.append(v)
    saidas.sort()
    lo = saidas[max(0, int(0.025 * len(saidas)) - 1)]
    hi = saidas[min(len(saidas) - 1, int(0.975 * len(saidas)))]
    return (round(lo, 1), round(hi, 1))


def ic_diferenca(a, b, replicas, agg):
    """IC95 de agg(b) - agg(a), reamostrando videos dentro de cada lado."""
    if not a or not b:
        return (None, None)
    rnd = random.Random(SEED)
    na, nb = len(a), len(b)
    saidas = []
    for _ in range(replicas):
        aa = [a[rnd.randrange(na)] for _ in range(na)]
        bb = [b[rnd.randrange(nb)] for _ in range(nb)]
        va, vb = agg(aa), agg(bb)
        if va is not None and vb is not None:
            saidas.append(vb - va)
    saidas.sort()
    lo = saidas[max(0, int(0.025 * len(saidas)) - 1)]
    hi = saidas[min(len(saidas) - 1, int(0.975 * len(saidas)))]
    return (round(lo, 1), round(hi, 1))


def escrita_latina(texto):
    """Mesma heuristica do eixo dos comentarios: >90% das letras em ASCII."""
    letras = [c for c in texto if c.isalpha()]
    if not letras:
        return False
    return sum(1 for c in letras if ord(c) < 128) / len(letras) > 0.9


# ------------------------------------------------------------------ passo 1
def confere_instrumento(res, n_amostra=400):
    log("== 1. o instrumento: sobre que texto os autores pontuaram? ==")
    if not os.path.exists(GAB):
        log("  gabarito ausente - passo pulado")
        return
    rows = list(csv.DictReader(open(GAB, encoding="utf-8-sig", errors="replace")))
    kv = [k for k in rows[0] if "VADER" in k][0]
    kt = [k for k in rows[0] if "TextBlob" in k][0]
    rnd = random.Random(SEED)
    am = rnd.sample(rows, min(n_amostra, len(rows)))
    campos = {
        "so o titulo":
            lambda r: (r["Title"] or ""),
        "so a descricao":
            lambda r: (r["Description"] or ""),
        "titulo + descricao":
            lambda r: (r["Title"] or "") + " " + (r["Description"] or ""),
        "titulo + descricao + tags":
            lambda r: (r["Title"] or "") + " " + (r["Description"] or "") + " " + (r["Tags"] or ""),
    }
    tabela = {}
    for nome, f in campos.items():
        ev = et = 0
        dv = dt = 0.0
        for r in am:
            txt = f(r)
            gv, gt = float(r[kv]), float(r[kt])
            pv, pt = pol_vader(txt), pol_tb(txt)
            ev += abs(pv - gv) < 1e-6
            et += abs(pt - gt) < 1e-6
            dv += abs(pv - gv)
            dt += abs(pt - gt)
        tabela[nome] = {"vader_exatos_pct": round(100.0 * ev / len(am), 1),
                        "vader_mae": round(dv / len(am), 4),
                        "textblob_exatos_pct": round(100.0 * et / len(am), 1),
                        "textblob_mae": round(dt / len(am), 4)}
        log("  %-27s VADER %5.1f%% exatos (MAE %.4f) | TextBlob %5.1f%% exatos (MAE %.4f)"
            % (nome, tabela[nome]["vader_exatos_pct"], tabela[nome]["vader_mae"],
               tabela[nome]["textblob_exatos_pct"], tabela[nome]["textblob_mae"]))
    res["instrumento"] = {"n_amostra": len(am), "campos": tabela,
                          "escolhido": "titulo + descricao"}

    gv = [float(r[kv]) for r in rows]
    gt = [float(r[kt]) for r in rows]
    log("")
    log("== 2. o ponto original (gabarito, colunas publicadas, n=%d) ==" % len(rows))
    ponto = {}
    for nome, xs, alvo in (("VADER", gv, ALVO["vader_pos"]),
                           ("TextBlob", gt, ALVO["textblob_pos"])):
        for b in (0.0, BANDA, 0.1):
            d = dist(xs, b)
            marca = "  <- convencao adotada" if b == BANDA else ""
            log("  %-9s banda +-%.2f: pos %4.1f  neu %4.1f  neg %4.1f   (artigo: pos %.0f; erro %+.1f p.p.)%s"
                % (nome, b, d["positivo"], d["neutro"], d["negativo"], alvo,
                   d["positivo"] - alvo, marca))
            ponto["%s_banda_%.2f" % (nome, b)] = dict(d, erro_pp=round(d["positivo"] - alvo, 1))
    res["ponto_original_gabarito"] = {"n": len(rows), "alvo_artigo": ALVO, "medido": ponto}


# ------------------------------------------------------------------ passo 2
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicas", type=int, default=400)
    a = ap.parse_args()
    res = {"seed": SEED, "banda_neutralidade": BANDA, "replicas": a.replicas,
           "limiar_inscritos": LIMIAR_INSCRITOS}

    confere_instrumento(res)

    if not os.path.exists(DB):
        sys.exit("snapshot nao encontrado: %s" % DB)
    cx = sqlite3.connect(DB)
    inscritos, titulo_canal = {}, {}
    for cid, tit, ins in cx.execute("SELECT channel_id, title, inscritos FROM canais"):
        inscritos[cid] = ins
        titulo_canal[cid] = tit

    vids = []
    n_sem_full = 0
    for vid, cid, ctit, tit, desc, full, pf in cx.execute(
            "SELECT video_id, channel_id, channel_title, title, description, "
            "description_full, passa_filtro FROM videos"):
        tit, desc = tit or "", desc or ""
        if not full:
            n_sem_full += 1
            full = desc          # video apagado desde a coleta: sobra o trecho
        txt = tit + " " + full
        txt_trunc = tit + " " + desc
        vids.append({
            "id": vid, "passa": int(pf),
            "tema": no_tema(tit, full), "tema_trunc": no_tema(tit, desc),
            "latina": escrita_latina(txt),
            "vader": pol_vader(txt), "tb": pol_tb(txt),
            "vader_trunc": pol_vader(txt_trunc), "tb_trunc": pol_tb(txt_trunc),
            "len_desc": len(desc), "len_full": len(full),
            "ugc": eh_ugc(titulo_canal.get(cid, ctit), inscritos.get(cid, 0)),
            "tem_canal": cid in inscritos,
        })

    log("")
    log("== 0. o texto: trecho truncado x descricao completa ==")
    import statistics
    med_t = statistics.median([v["len_desc"] for v in vids])
    med_f = statistics.median([v["len_full"] for v in vids])
    log("  mediana de caracteres na descricao: truncada %d  x  completa %d  (%d sem completa)"
        % (med_t, med_f, n_sem_full))
    for inst, rot in (("vader", "VADER"), ("tb", "TextBlob")):
        dt_ = dist([v[inst + "_trunc"] for v in vids])
        df_ = dist([v[inst] for v in vids])
        log("  %-9s fatia positiva: texto truncado %4.1f  x  texto completo %4.1f  (%+.1f p.p.)"
            % (rot, dt_["positivo"], df_["positivo"], df_["positivo"] - dt_["positivo"]))
    log("  no tema pela descricao truncada: %d  x  pela completa: %d"
        % (sum(v["tema_trunc"] for v in vids), sum(v["tema"] for v in vids)))
    res["artefato_do_texto_truncado"] = {
        "mediana_truncada": med_t, "mediana_completa": med_f,
        "sem_descricao_completa": n_sem_full,
        "no_tema_truncada": sum(v["tema_trunc"] for v in vids),
        "no_tema_completa": sum(v["tema"] for v in vids),
        "pos_truncada": {r: dist([v[i + "_trunc"] for v in vids])["positivo"]
                         for i, r in (("vader", "VADER"), ("tb", "TextBlob"))},
        "pos_completa": {r: dist([v[i] for v in vids])["positivo"]
                         for i, r in (("vader", "VADER"), ("tb", "TextBlob"))}}

    # --- validacao cruzada: os videos que estao dos DOIS lados -------------
    if os.path.exists(GAB):
        gab = {}
        for r in csv.DictReader(open(GAB, encoding="utf-8-sig", errors="replace")):
            kid = "Video_id" if "Video_id" in r else list(r)[0]
            gab[r[kid]] = r
        kv = [k for k in list(gab.values())[0] if "VADER" in k][0]
        kt = [k for k in list(gab.values())[0] if "TextBlob" in k][0]
        inter = [v for v in vids if v["id"] in gab]
        log("")
        log("== 2b. validacao cruzada: os %d videos que estao na nossa coleta E no gabarito ==" % len(inter))
        val = {"n": len(inter)}
        for inst, rot, k in (("vader", "VADER", kv), ("tb", "TextBlob", kt)):
            nosso = dist([v[inst] for v in inter])
            trunc = dist([v[inst + "_trunc"] for v in inter])
            deles = dist([float(gab[v["id"]][k]) for v in inter])
            log("  %-9s publicado pelos autores pos %4.1f | nosso texto completo pos %4.1f (%+.1f p.p.) | nosso truncado pos %4.1f (%+.1f p.p.)"
                % (rot, deles["positivo"], nosso["positivo"],
                   nosso["positivo"] - deles["positivo"], trunc["positivo"],
                   trunc["positivo"] - deles["positivo"]))
            val[rot] = {"publicado": deles, "nosso_completo": nosso, "nosso_truncado": trunc}
        res["validacao_cruzada"] = val

    log("")
    log("== 3. a nossa coleta: %d videos, %d no tema ==" % (len(vids), sum(v["tema"] for v in vids)))

    bases = (("todos os coletados", lambda v: True),
             ("so no tema", lambda v: v["tema"]))
    recortes = (("com filtro (analogo ao corpus do artigo)", lambda v: v["passa"] == 1),
                ("SEM filtro (tudo o que a busca devolveu)", lambda v: True),
                ("so os descartados pelo filtro", lambda v: v["passa"] == 0))

    res["coleta"] = {}
    for nome_base, fb in bases:
        sub = [v for v in vids if fb(v)]
        log("")
        log("-- base: %s (n=%d) --" % (nome_base, len(sub)))
        bloco = {"n": len(sub)}
        for nome_rec, fr in recortes:
            g = [v for v in sub if fr(v)]
            d = {"n": len(g)}
            for inst, rot in (("vader", "VADER"), ("tb", "TextBlob")):
                pols = [v[inst] for v in g]
                dd = dist(pols)
                ic = banda_ic(pols, a.replicas, frac_pos)
                d[rot] = dict(dd, pos_ic95=list(ic),
                              polaridade_media=round(media(pols), 4),
                              pos_menos_neg_pp=round(dd["positivo"] - dd["negativo"], 1))
                log("   %-42s %-9s pos %4.1f [%4.1f; %4.1f]  neu %4.1f  neg %4.1f   pos-neg %+5.1f p.p."
                    % (nome_rec if inst == "vader" else "", rot, dd["positivo"],
                       ic[0], ic[1], dd["neutro"], dd["negativo"],
                       dd["positivo"] - dd["negativo"]))
            bloco[nome_rec] = d

        com = [v for v in sub if v["passa"] == 1]
        bloco["delta_sem_menos_com"] = {}
        for inst, rot in (("vader", "VADER"), ("tb", "TextBlob")):
            ic = ic_diferenca([v[inst] for v in com], [v[inst] for v in sub],
                              a.replicas, frac_pos)
            delta = round(frac_pos([v[inst] for v in sub]) - frac_pos([v[inst] for v in com]), 1)
            muda = bool(ic[0] > 0 or ic[1] < 0)
            bloco["delta_sem_menos_com"][rot] = {"delta_pp": delta, "ic95": list(ic),
                                                 "significativo": muda}
            log("   delta na fatia positiva (sem filtro - com filtro), %-9s %+5.1f p.p.  IC95 [%+.1f; %+.1f]  %s"
                % (rot, delta, ic[0], ic[1], "MUDA" if muda else "nao separa de zero"))
        res["coleta"][nome_base] = bloco

    # ------------------------------------------------ a explicacao do artigo
    log("")
    log("== 4. a explicacao do artigo: o tom positivo vem de a imprensa dominar? ==")
    tema = [v for v in vids if v["tema"] and v["tem_canal"]]
    expl = {"n": len(tema)}
    for rotulo, f in (("UGC (conteudo de usuario)", lambda v: v["ugc"]),
                      ("institucional / imprensa", lambda v: not v["ugc"])):
        g = [v for v in tema if f(v)]
        e = {"n": len(g)}
        for inst, rot in (("vader", "VADER"), ("tb", "TextBlob")):
            pols = [v[inst] for v in g]
            dd = dist(pols)
            e[rot] = dict(dd, polaridade_media=round(media(pols), 4))
            log("   %-26s %-9s pos %4.1f  neu %4.1f  neg %4.1f   polaridade media %+.4f (n=%d)"
                % (rotulo if inst == "vader" else "", rot, dd["positivo"],
                   dd["neutro"], dd["negativo"], media(pols), len(g)))
        expl[rotulo] = e
    ugc = [v for v in tema if v["ugc"]]
    ins = [v for v in tema if not v["ugc"]]
    expl["delta_ugc_menos_institucional"] = {}
    for inst, rot in (("vader", "VADER"), ("tb", "TextBlob")):
        ic = ic_diferenca([v[inst] for v in ins], [v[inst] for v in ugc], a.replicas, frac_pos)
        delta = round(frac_pos([v[inst] for v in ugc]) - frac_pos([v[inst] for v in ins]), 1)
        sep = bool(ic[0] > 0 or ic[1] < 0)
        expl["delta_ugc_menos_institucional"][rot] = {"delta_pp": delta, "ic95": list(ic),
                                                      "significativo": sep}
        log("   delta pos (UGC - institucional), %-9s %+5.1f p.p.  IC95 [%+.1f; %+.1f]  %s"
            % (rot, delta, ic[0], ic[1], "separa de zero" if sep else "NAO separa de zero"))
    res["explicacao_do_artigo"] = expl

    # ------------------------------------------- sensibilidades e convergencia
    log("")
    log("== 5. sensibilidades (base: no tema) ==")
    sub = [v for v in vids if v["tema"]]
    sens = {}
    for b in (0.0, 0.05, 0.1):
        linha = {}
        for inst, rot in (("vader", "VADER"), ("tb", "TextBlob")):
            dc = dist([v[inst] for v in sub if v["passa"] == 1], b)
            ds = dist([v[inst] for v in sub], b)
            linha[rot] = {"com_filtro": dc, "sem_filtro": ds,
                          "delta_pp": round(ds["positivo"] - dc["positivo"], 1)}
            log("   banda +-%.2f  %-9s com filtro pos %4.1f  |  sem filtro pos %4.1f  (delta %+.1f p.p.)"
                % (b, rot, dc["positivo"], ds["positivo"], ds["positivo"] - dc["positivo"]))
        sens["banda_%.2f" % b] = linha
    lat = [v for v in sub if v["latina"]]
    linha = {}
    for inst, rot in (("vader", "VADER"), ("tb", "TextBlob")):
        dc = dist([v[inst] for v in lat if v["passa"] == 1])
        ds = dist([v[inst] for v in lat])
        linha[rot] = {"com_filtro": dc, "sem_filtro": ds,
                      "delta_pp": round(ds["positivo"] - dc["positivo"], 1)}
        log("   so escrita latina (n=%d)  %-9s com filtro pos %4.1f  |  sem filtro pos %4.1f  (delta %+.1f p.p.)"
            % (len(lat), rot, dc["positivo"], ds["positivo"], ds["positivo"] - dc["positivo"]))
    sens["so_escrita_latina"] = dict(linha, n=len(lat))
    linha = {}
    for inst, rot in (("vader_trunc", "VADER"), ("tb_trunc", "TextBlob")):
        dc = dist([v[inst] for v in sub if v["passa"] == 1])
        ds = dist([v[inst] for v in sub])
        linha[rot] = {"com_filtro": dc, "sem_filtro": ds,
                      "delta_pp": round(ds["positivo"] - dc["positivo"], 1)}
        log("   texto TRUNCADO (o do snapshot)  %-9s com filtro pos %4.1f  |  sem filtro pos %4.1f  (delta %+.1f p.p.)"
            % (rot, dc["positivo"], ds["positivo"], ds["positivo"] - dc["positivo"]))
    sens["texto_truncado"] = linha
    res["sensibilidade"] = sens

    log("")
    log("== 6. convergencia: a fatia positiva em funcao do volume (sem filtro, no tema) ==")
    rnd = random.Random(SEED)
    curva = {}
    for n in (50, 100, 200, 400, 800, 1200, len(sub)):
        if n > len(sub):
            continue
        av, at = [], []
        for _ in range(a.replicas):
            am = rnd.sample(sub, n)
            av.append(frac_pos([v["vader"] for v in am]))
            at.append(frac_pos([v["tb"] for v in am]))
        av.sort()
        at.sort()

        def faixa(xs):
            return (round(xs[max(0, int(0.025 * len(xs)) - 1)], 1),
                    round(xs[min(len(xs) - 1, int(0.975 * len(xs)))], 1))

        curva[n] = {"VADER": {"pos": round(media(av), 1), "ic95": list(faixa(av))},
                    "TextBlob": {"pos": round(media(at), 1), "ic95": list(faixa(at))}}
        log("   n=%5d  VADER pos %4.1f [%4.1f; %4.1f]   TextBlob pos %4.1f [%4.1f; %4.1f]"
            % (n, curva[n]["VADER"]["pos"], curva[n]["VADER"]["ic95"][0],
               curva[n]["VADER"]["ic95"][1], curva[n]["TextBlob"]["pos"],
               curva[n]["TextBlob"]["ic95"][0], curva[n]["TextBlob"]["ic95"][1]))
    res["convergencia_sem_filtro_no_tema"] = curva

    with open(SAIDA, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    log("")
    log("saida: %s" % os.path.abspath(SAIDA))


if __name__ == "__main__":
    main()
