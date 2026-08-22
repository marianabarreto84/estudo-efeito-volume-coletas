#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Audita as CONTAS do corpo.tex: aritmetica, faixas, sanidade e procedencia.

Complementa o `audita_numeros.py`, que pergunta *o numero bate com o dado?*
(texto x JSON congelado dos casos). Este aqui pergunta outra coisa, que nao
depende de ter os dados em maos: *a conta fecha?* Ele so conhece o texto, e
verifica que aquilo que o texto afirma sobre os proprios numeros e verdade.

Quatro camadas:

  1. AUTOMATICA -- varre o texto e testa toda ocorrencia dos padroes conhecidos:
     - "de X% para Y% ... N pontos percentuais"  -> |Y-X| = N ?
     - "X% contra/e Y%" que deveriam somar 100
     - "IC95% a--b" / "intervalo de confianca de 95% entre a e b" -> contem a
       estimativa? a < b ?
     - "X de/dos Y" seguido ou precedido de "Z%"  -> X/Y = Z ?
     - linhas de tabela com (total, parte, %)     -> % = parte/total ou
       (total-parte)/total ?
     - tabela com N declarado na legenda          -> % = contagem/N ?

  2. DECLARADA -- relacoes que so um humano enxerga na prosa (numero escrito por
     extenso, conta que atravessa paragrafos, razao implicita). Ficam na tabela
     RELACOES, viram teste de regressao: se alguem mexer num numero e esquecer o
     outro, quebra.

  3. SANIDADE -- o que nunca pode acontecer: percentual fora de [0,100], IC
     invertido, kappa fora de [-1,1], p fora de [0,1], contagem negativa.

  4. PROCEDENCIA -- todo numero do texto que nao aparece em nenhum JSON dos casos
     e nao esta coberto por uma checagem acima nem justificado em
     SEM_FONTE_JUSTIFICADO. E a camada do CLAUDE.md 7: "nada de numero solto".

Uso:
    python audita_contas.py              # so o que precisa de olho
    python audita_contas.py --tudo       # mostra tambem o que passou
    python audita_contas.py --procedencia  # so a camada 4, detalhada

Saida: linhas OK / ATENCAO / ERRO, um resumo, e codigo de saida 1 se houver ERRO.
Convencoes de tolerancia:
    - dois valores arredondados a 1 casa produzem delta com erro de ate 0,1;
      por isso |erro| <= 0,11 conta como arredondamento (OK), acima disso e ERRO.
    - "cerca de", "aproximadamente", "quase", "~" relaxam a tolerancia para 10%.
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
CASOS = os.path.join(RAIZ, "casos")
TEX = os.path.join(AQUI, "corpo.tex")

TOL_ARRED = 0.11        # erro compativel com arredondamento a 1 casa
TOL_HEDGE = 0.10        # 10% relativo, quando o texto diz "cerca de"

HEDGES = (u"cerca de", u"aproximadamente", u"quase", u"~", u"em torno de",
          u"pouco mais", u"pouco menos", u"mais de", u"menos de", u"ordem de",
          u"da ordem", u"praticamente", u"por volta")

# ---------------------------------------------------------------------------
# 0. utilitarios
# ---------------------------------------------------------------------------

RESULTADOS = []          # (nivel, capitulo, linha, rotulo, detalhe)
NIVEIS = {"OK": 0, "ATENCAO": 1, "ERRO": 2}


def registra(nivel, linha, rotulo, detalhe):
    RESULTADOS.append((nivel, linha, rotulo, detalhe))


def pt(v, casas=1):
    u"""Formata como o texto escreve: virgula decimal, ponto de milhar."""
    s = ("{:,.%df}" % casas).format(v)
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def num(txt):
    u"""'1.015.247' -> 1015247.0 ; '57,6' -> 57.6 ; '-6,4' -> -6.4"""
    txt = txt.strip().replace(u"\u2212", "-")
    sinal = -1.0 if txt.startswith("-") else 1.0
    txt = txt.lstrip("+-").strip()
    txt = re.sub(r"[^0-9.,].*$", "", txt)           # corta sufixo ('43,0.' -> '43,0')
    txt = txt.rstrip(".,")
    if not txt:
        return 0.0
    if "," in txt:
        txt = txt.replace(".", "").replace(",", ".")
    elif re.match(r"^\d{1,3}(?:\.\d{3})+$", txt):
        txt = txt.replace(".", "")
    return sinal * float(txt)


# numero pt-BR: 1.015.247 | 43.479 | 938.961 | 57,6 | 279 | -6,4
RE_NUM = re.compile(r"(?<![\w.,])(-?\d{1,3}(?:\.\d{3})+|-?\d+)(?:,(\d+))?")
RE_PCT = re.compile(r"(-?\d{1,3}(?:\.\d{3})+|-?\d+)(?:,(\d+))?\s*%")


def numeros(txt):
    u"""Todos os numeros de um trecho: [(valor, texto_original, pos)]"""
    out = []
    for m in RE_NUM.finditer(txt):
        inteiro, dec = m.group(1), m.group(2)
        bruto = inteiro + ("," + dec if dec else "")
        out.append((num(bruto), bruto, m.start()))
    return out


def percentuais(txt):
    out = []
    for m in RE_PCT.finditer(txt):
        inteiro, dec = m.group(1), m.group(2)
        bruto = inteiro + ("," + dec if dec else "")
        out.append((num(bruto), bruto, m.start()))
    return out


def tem_hedge(txt):
    baixo = txt.lower()
    return any(h in baixo for h in HEDGES)


def confere(rotulo, esperado, obtido, linha, tol=TOL_ARRED, hedge=False,
            relativo=False, nota="", inteiro=False):
    u"""Compara e registra. `esperado` = o que o texto afirma; `obtido` = a conta."""
    erro = abs(esperado - obtido)
    if inteiro:
        tol = max(tol, 0.5)                 # "14%" ja e um arredondamento
    if hedge:
        limite = max(abs(esperado), abs(obtido)) * TOL_HEDGE
    elif relativo:
        limite = max(abs(esperado), abs(obtido)) * tol
    else:
        limite = tol
    det = u"texto diz %s; a conta da %s%s" % (
        pt(esperado, 2).rstrip("0").rstrip(","), pt(obtido, 2).rstrip("0").rstrip(","),
        (u" (%s)" % nota) if nota else u"")
    if erro <= 1e-9:
        registra("OK", linha, rotulo, u"confere: %s" % pt(esperado, 2).rstrip("0").rstrip(","))
    elif erro <= limite:
        registra("OK", linha, rotulo, det + u" [dentro do arredondamento]")
    elif erro <= limite * 2 and not hedge:
        registra("ATENCAO", linha, rotulo, det)
    else:
        registra("ERRO", linha, rotulo, det)


# ---------------------------------------------------------------------------
# 1. normalizacao do LaTeX (preservando o numero da linha)
# ---------------------------------------------------------------------------

def normaliza_linha(l):
    l = re.sub(r"(?<!\\)%.*$", "", l)              # comentario LaTeX
    l = l.replace("{,}", ",").replace("{.}", ".")   # decimal em modo matematico
    l = l.replace(r"\%", "%").replace(r"\,", " ").replace(r"\ ", " ")
    l = re.sub(r"\\cite\w*\{[^}]*\}", " ", l)
    l = re.sub(r"\\(?:ref|label|cref|eqref)\{[^}]*\}", " REF ", l)
    l = re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}", " ", l)
    l = re.sub(r"\\(?:textbf|emph|textit|texttt|textsc|mathrm|text)\{([^{}]*)\}", r"\1", l)
    l = re.sub(r"\\(?:textbf|emph|textit|texttt|textsc)\{([^{}]*)\}", r"\1", l)
    l = l.replace("---", " - ").replace("--", " a ")   # travessao e faixa LaTeX
    l = l.replace(r"$\approx$", "~").replace(r"$\sim$", "~")
    l = l.replace(r"$\geq$", ">=").replace(r"$\leq$", "<=").replace(r"$\pm$", "+-")
    l = re.sub(r"\$([^$]*)\$", r"\1", l)            # tira modo matematico
    l = re.sub(r"\\[a-zA-Z]+\*?", " ", l)           # comandos restantes
    l = l.replace("{", " ").replace("}", " ")
    l = re.sub(r"\s+", " ", l)
    return l


def carrega_tex():
    linhas = io.open(TEX, encoding="utf-8").read().split("\n")
    return [(i + 1, normaliza_linha(l)) for i, l in enumerate(linhas)]


def paragrafos(linhas):
    u"""Agrupa em paragrafos (linha_inicial, texto)."""
    out, buf, ini = [], [], None
    for n, l in linhas:
        if l.strip():
            if ini is None:
                ini = n
            buf.append(l.strip())
        elif buf:
            out.append((ini, " ".join(buf)))
            buf, ini = [], None
    if buf:
        out.append((ini, " ".join(buf)))
    return out


RE_FIM_FRASE = re.compile(r"(?<=[.;:])\s+")


def frases(linhas):
    u"""Frases com o numero da linha em que comecam."""
    out = []
    for ini, txt in paragrafos(linhas):
        for f in RE_FIM_FRASE.split(txt):
            f = f.strip()
            if f:
                out.append((ini, f))
    return out


# ---------------------------------------------------------------------------
# 2. camada AUTOMATICA
# ---------------------------------------------------------------------------

RE_DE_PARA = re.compile(
    r"de (-?\d[\d.,]*)\s*%?[^.;]{0,60}?\b(?:para|a)\s+(-?\d[\d.,]*)\s*%")
RE_PP = re.compile(r"(-?\d[\d.,]*)\s*(?:pontos? percentuais?|p\.p\.)")


def checa_deltas(fs):
    u"""'de X% para Y% ... N pontos percentuais' -> |Y-X| == N ?"""
    for i, (linha, f) in enumerate(fs):
        for mpp in RE_PP.finditer(f):
            n = num(mpp.group(1))
            par = RE_DE_PARA.search(f)
            escopo = f
            pista = re.search(r"diferen\w+|dist\w+ncia|delta|desloca|salto|"
                              r"movimento|queda|encolh", f, re.I)
            if not par and i > 0 and pista:
                # 'A diferenca e de N p.p.' costuma vir na frase seguinte ao par
                ant = fs[i - 1][1]
                pcts = percentuais(ant)
                if len(pcts) >= 2:
                    a, b = pcts[-2][0], pcts[-1][0]
                    esp, obt = (n, b - a) if n < 0 else (abs(n), abs(b - a))
                    confere(u"delta declarado", esp, obt, linha,
                            hedge=tem_hedge(f),
                            nota=u"%s%% -> %s%% da frase anterior" % (pt(a), pt(b)))
                    continue
            if par:
                a, b = num(par.group(1)), num(par.group(2))
                confere(u"delta declarado", abs(n), abs(b - a), linha,
                        hedge=tem_hedge(escopo),
                        nota=u"de %s a %s" % (pt(a), pt(b)))


RE_PAR_100 = re.compile(
    r"(\d{1,3}(?:,\d+)?)\s*%[^.;]{0,50}?\b(?:contra|e|ante|versus|x)\b[^.;]{0,50}?"
    r"(\d{1,3}(?:,\d+)?)\s*%")


def checa_soma_100(fs):
    u"""Pares complementares que deveriam somar 100."""
    for linha, f in fs:
        for m in RE_PAR_100.finditer(f):
            a, b = num(m.group(1)), num(m.group(2))
            s = a + b
            if 98.0 <= s <= 102.0 and abs(s - 100.0) > 0.15:
                registra("ATENCAO", linha, u"par complementar",
                         u"%s%% + %s%% = %s%% (nao fecha 100; ha classe residual?)"
                         % (pt(a), pt(b), pt(s)))
            elif abs(s - 100.0) <= 0.15 and s != 100.0:
                registra("OK", linha, u"par complementar",
                         u"%s%% + %s%% = %s%% [arredondamento]" % (pt(a), pt(b), pt(s)))


RE_IC = re.compile(
    r"(?:IC\s?95\s*%|intervalo de confian\w+ de 95\s*%)"
    r"[^0-9-]{0,30}?(-?\d[\d.,]*)\s*%?\s*(?:--|-|a|e|entre|,)\s*(-?\d[\d.,]*)")
RE_IC2 = re.compile(
    r"(?:IC\s?95\s*%|intervalo de confian\w+ de 95\s*%)\s*(?:de \w+\s*)?"
    r"(?:entre\s*)?(-?\d[\d.,]*)\s*%?\s*(?:--|\ba\b|\be\b)\s*(-?\d[\d.,]*)")


def checa_ic(fs):
    for i, (linha, f) in enumerate(fs):
        for m in list(RE_IC2.finditer(f)) or list(RE_IC.finditer(f)):
            lo, hi = num(m.group(1)), num(m.group(2))
            if lo >= hi:
                registra("ERRO", linha, u"IC invertido",
                         u"limite inferior %s >= superior %s" % (pt(lo), pt(hi)))
                continue
            # estimativa = ultimo numero antes do IC, na frase ou na anterior
            antes = f[:m.start()]
            cands = percentuais(antes) or numeros(antes)
            if not cands and i > 0:
                cands = percentuais(fs[i - 1][1]) or numeros(fs[i - 1][1])
            if i > 0:                       # o IC costuma vir em nota de rodape
                cands = cands + (percentuais(fs[i - 1][1]) or numeros(fs[i - 1][1]))
            if not cands:
                continue
            dentro = [c for c in cands if lo <= c[0] <= hi]
            meio = (lo + hi) / 2.0
            perto = min(cands, key=lambda c: abs(c[0] - meio))
            if dentro:
                registra("OK", linha, u"IC contem a estimativa",
                         u"%s em [%s; %s]" % (pt(dentro[0][0]), pt(lo), pt(hi)))
            else:
                registra("ATENCAO", linha, u"IC nao contem estimativa vizinha",
                         u"nenhum valor vizinho cai em [%s; %s]; o mais proximo e %s"
                         % (pt(lo), pt(hi), pt(perto[0])))


RE_FRACAO = re.compile(
    r"(\d[\d.]*)\s+(?:de|dos|das|em)\s+(\d[\d.]*)\b")


def checa_fracoes(fs):
    u"""'X de Y' com um percentual perto -> X/Y = pct ?"""
    for linha, f in fs:
        for m in RE_FRACAO.finditer(f):
            a, b = num(m.group(1)), num(m.group(2))
            if b <= 0 or a > b or b < 10:
                continue
            trecho = f[max(0, m.start() - 90): m.end() + 90]
            pcts = [p for p in percentuais(trecho) if 0 < p[0] <= 100]
            if not pcts:
                continue
            esperado = a / b * 100.0
            # aceita se ALGUM percentual proximo corresponde
            melhor = min(pcts, key=lambda p: abs(p[0] - esperado))
            if abs(melhor[0] - esperado) <= max(0.6, esperado * 0.02):
                registra("OK", linha, u"fracao x percentual",
                         u"%s/%s = %s%% ~ %s%%" % (pt(a, 0), pt(b, 0),
                                                   pt(esperado), pt(melhor[0])))


# --- tabelas ---------------------------------------------------------------

def blocos_tabela(bruto):
    out = []
    for m in re.finditer(r"\\begin\{table\}(.*?)\\end\{table\}", bruto, re.S):
        linha = bruto[:m.start()].count("\n") + 1
        out.append((linha, m.group(1)))
    return out


def checa_tabelas(bruto):
    for linha0, bloco in blocos_tabela(bruto):
        legenda = ""
        mleg = re.search(r"\\caption\{(.*?)\}\s*\n", bloco, re.S)
        if mleg:
            legenda = normaliza_linha(mleg.group(1).replace("\n", " "))
        mn = re.search(r"N\s*=\s*(\d[\d.]*)", legenda)
        n_decl = num(mn.group(1)) if mn else None

        corpo = bloco
        for cmd in (r"\toprule", r"\midrule", r"\bottomrule"):
            corpo = corpo.replace(cmd, "")
        for l in corpo.split(r"\\"):
            l = normaliza_linha(l.replace("\n", " "))
            if "&" not in l:
                continue
            celulas = [c.strip() for c in l.split("&")]
            vals = []          # (valor, tem_simbolo_pct, escrito_sem_decimal)
            for c in celulas:
                c2 = c.replace("%", "").strip()
                if re.match(r"^-?\d[\d.,]*$", c2):
                    vals.append((num(c2), "%" in c, "," not in c2))
            rot = celulas[0][:30] if celulas else "?"
            if n_decl:
                # tabela com N na legenda: pares (contagem, % sobre N)
                for a, b in zip(vals, vals[1:]):
                    if a[0] > b[0] and 0 < b[0] <= 100 and a[0] > 100:
                        confere(u"tabela: %% sobre N=%s" % pt(n_decl, 0), b[0],
                                a[0] / n_decl * 100.0, linha0, inteiro=b[2],
                                nota=u"linha '%s'" % rot)
            elif len(vals) == 3 and not vals[0][1] and not vals[1][1]:
                a, b, p = vals[0][0], vals[1][0], vals[2][0]
                if a <= 0 or p > 100:
                    continue
                alvo = min((b / a * 100.0, u"parte/total"),
                           ((a - b) / a * 100.0, u"descarte"),
                           key=lambda t: abs(t[0] - p))
                confere(u"tabela: %s" % alvo[1], p, alvo[0], linha0,
                        inteiro=vals[2][2], nota=u"linha '%s'" % rot)


# ---------------------------------------------------------------------------
# 3. camada SANIDADE
# ---------------------------------------------------------------------------

def checa_sanidade(fs):
    for linha, f in fs:
        for v, bruto, pos in percentuais(f):
            if v > 100.0 or v < -100.0:
                registra("ERRO", linha, u"percentual fora de faixa",
                         u"%s%% em '%s'" % (bruto, f[max(0, pos - 40):pos + 20].strip()))
        for m in re.finditer(r"kappa\s*=\s*(-?\d[\d.,]*)", f):
            v = num(m.group(1))
            if not (-1.0 <= v <= 1.0):
                registra("ERRO", linha, u"kappa fora de [-1,1]", pt(v, 3))
        for m in re.finditer(r"\bp\s*=\s*(\d[\d.,]*)\s*(\S*)", f):
            v = num(m.group(1))
            if "10" in m.group(2):
                continue                        # p = 3,0 x 10^-18
            if v > 1.0:
                registra("ERRO", linha, u"p-valor > 1", pt(v, 3))


# ---------------------------------------------------------------------------
# 4. camada DECLARADA (relacoes que so um humano enxerga)
# ---------------------------------------------------------------------------
# Cada entrada: (capitulo, rotulo, valor_afirmado_no_texto, conta, tolerancia)
# `conta` e o valor que a aritmetica produz a partir de outros numeros do texto.

def relacoes():
    R = []
    a = R.append

    # --- Cap. 1: o levantamento ---
    a((u"cap.1", u"1.718 = 2.139 - 421 excluidos", 1718.0, 2139.0 - 421.0, 0.0))
    a((u"cap.1", u"2.106 PDFs abertos <= 13.395 - 10.230 com paywall",
       2106.0, min(2106.0, 13395.0 - 10230.0), 0.0))
    a((u"cap.1", u"'seis em cada dez' abaixo de 1 M (mediana ~273 mil e coerente)",
       1.0, 1.0, 0.0))

    # --- Cap. 3: #Eleicoes2014 ---
    a((u"cap.3", u"'cerca de 46 vezes': 32.193 / 700", 46.0, 32193.0 / 700.0, 1.0))
    a((u"cap.3", u"'5 para 1': 83,4 / 16,6", 5.0, 83.4 / 16.6, 0.15))
    a((u"cap.3", u"MV + MH = 100 (83,4 + 16,6)", 100.0, 83.4 + 16.6, 0.0))
    a((u"cap.3", u"queda de 12,2 p.p.: 48,3 -> 36,1", 12.2, 48.3 - 36.1, TOL_ARRED))
    a((u"cap.3", u"'queda de doze pontos' = 12,2 p.p.", 12.0, 12.2, 0.5))
    a((u"cap.3", u"banda do artigo (n=700): 39,9 - 32,6", 7.3, 39.9 - 32.6, TOL_ARRED))
    a((u"cap.3", u"48,3% cai FORA da banda 32,6--39,9 (o texto afirma isso)",
       1.0, 1.0 if not (32.6 <= 48.3 <= 39.9) else 0.0, 0.0))
    a((u"cap.3", u"RTMV medio varia <0,5 p.p.: 36,1 - 35,7", 0.4, 36.1 - 35.7, TOL_ARRED))

    # --- Cap. 4: debate vacinal ---
    a((u"cap.4", u"'cerca de 19 vezes': 29.978 / 1.525", 19.0, 29978.0 / 1525.0,
       1.0))
    a((u"cap.4", u"'um em cada onze retuites': 100 / 9,3", 11.0, 100.0 / 9.3, 0.4))
    a((u"cap.4", u"razao pro/anti em posts: 3,13 / 2,01 M", 1.56, 3.13 / 2.01, 0.02))
    a((u"cap.4", u"artigo: 2,02 / 1,98 M = 1,02", 1.02, 2.02 / 1.98, 0.01))
    a((u"cap.4", u"maior deslocamento tematico: 31,8 - 23,4", 8.4, 31.8 - 23.4,
       TOL_ARRED))
    a((u"cap.4", u"razao AV3 publicada: 58,6 / 40,9", 1.43, 58.6 / 40.9, 0.02))
    a((u"cap.4", u"razao AV3 na replica: 58,9 / 41,1", 1.43, 58.9 / 41.1, 0.02))
    a((u"cap.4", u"diferenca de 0,3 p.p.: 58,9 - 58,6", 0.3, 58.9 - 58.6, 0.01))
    a((u"cap.4", u"58,9 + 41,1 = 100 (a replica nao deixa residuo)", 100.0,
       58.9 + 41.1, 0.0))
    a((u"cap.4", u"pro entre os com lado (esquema binario, >10 RT): 58,8/(58,8+35,1)",
       62.6, 58.8 / (58.8 + 35.1) * 100.0, 0.15))
    a((u"cap.4", u"pro entre os com lado (3 classes, >10 RT): 41,1/(41,1+25,5)",
       61.7, 41.1 / (41.1 + 25.5) * 100.0, 0.15))
    a((u"cap.4", u"3 classes somam 100: 41,1 + 25,5 + 33,4", 100.0,
       41.1 + 25.5 + 33.4, 0.05))
    a((u"cap.4", u"'cerca de 18 pontos' entre esquemas: 58,8 - 41,1", 18.0,
       58.8 - 41.1, 0.5))
    a((u"cap.4", u"neutros: 'um em cada quatro' virais = 24,6%", 25.0, 24.6, 1.0))
    a((u"cap.4", u"neutros: 'um em cada tres' no corpus = 33,4%", 33.3, 33.4, 1.0))
    a((u"cap.4", u"BBC: razao 1,92 = 65,8 / 34,2", 1.92, 65.8 / 34.2, 0.01))
    a((u"cap.4", u"BBC: 65,8 + 34,2 = 100", 100.0, 65.8 + 34.2, 0.0))
    a((u"cap.4", u"12% mais retuites: 4,5 M / 4,0 M", 1.12, 4.5 / 4.0, 0.02))

    # --- Cap. 5: Reddit ---
    a((u"cap.5", u"RB3 no universo sob corte: 3.450 / 5.991", 57.6,
       3450.0 / 5991.0 * 100.0, TOL_ARRED))
    a((u"cap.5", u"RB3 sem corte: 33.115 / 217.386", 15.2,
       33115.0 / 217386.0 * 100.0, TOL_ARRED))
    a((u"cap.5", u"artigo: 7 / 279 = 2,5% (texto diz 'cerca de 3%')", 3.0,
       7.0 / 279.0 * 100.0, 0.6))
    a((u"cap.5", u"'dezenove vezes': 57,6 / 3", 19.0, 57.6 / 3.0, 0.5))
    a((u"cap.5", u"'pouco mais de um milesimo': 279 / 217.386", 1.0,
       279.0 / 217386.0 * 1000.0, 0.3))
    a((u"cap.5", u"assenta em <3 p.p. entre k=10 e k=50: 57,6 - 55,0", 3.0,
       57.6 - 55.0, 0.45))
    a((u"cap.5", u"Massachs: 7.083 / 44.924", 15.77,
       7083.0 / 44924.0 * 100.0, TOL_ARRED))
    a((u"cap.5", u"Massachs: 15,8% declarado ~ 15,77% medido", 15.8,
       7083.0 / 44924.0 * 100.0, 0.05))
    a((u"cap.5", u"distancia entre as pontas: 34,6 - 26,8", 7.8, 34.6 - 26.8,
       TOL_ARRED))
    a((u"cap.5", u"'menos de um quarto de ponto': max(|34,6-34,8|,|26,8-26,7|)",
       0.25, max(abs(34.6 - 34.8), abs(26.8 - 26.7)), 0.06))
    a((u"cap.5", u"'fator de quatro' sem reponderar: 34,6 / 8,2", 4.0,
       34.6 / 8.2, 0.25))
    a((u"cap.5", u"13 subreddits = 10 com participante + 3 sem", 13.0, 10.0 + 3.0,
       0.0))

    # --- Cap. 6: YouTube ---
    a((u"cap.6", u"funil: 3.353 + 1.025 = 4.378 entram na uniao", 4378.0,
       3353.0 + 1025.0, 0.0))
    a((u"cap.6", u"funil: descarte da busca = (6.997-3.353)/6.997", 52.0,
       (6997.0 - 3353.0) / 6997.0 * 100.0, 0.5))
    a((u"cap.6", u"funil: descarte dos sugeridos = (104.172-1.025)/104.172", 99.0,
       (104172.0 - 1025.0) / 104172.0 * 100.0, 0.5))
    a((u"cap.6", u"funil: descarte na uniao = (4.378-3.782)/4.378", 14.0,
       (4378.0 - 3782.0) / 4378.0 * 100.0, 0.5))
    a((u"cap.6", u"delta do filtro: 32,7 - 39,0", -6.4, 32.7 - 39.0, TOL_ARRED))
    a((u"cap.6", u"delta do funil: 61,7 - 23,5", 38.3, 61.7 - 23.5, TOL_ARRED))
    a((u"cap.6", u"IC do filtro contem -6,4: [-11,4; -1,4]", 1.0,
       1.0 if -11.4 <= -6.4 <= -1.4 else 0.0, 0.0))
    a((u"cap.6", u"IC do funil contem 38,3: [33,5; 43,0]", 1.0,
       1.0 if 33.5 <= 38.3 <= 43.0 else 0.0, 0.0))
    a((u"cap.6", u"'duas ordens de grandeza': 199.000 / 1.070", 100.0,
       199000.0 / 1070.0, 100.0))
    a((u"cap.6", u"'quase um em cada quatro descartes no tema' = 23,0%", 25.0,
       23.0, 2.5))
    a((u"cap.6", u"'menos de 7% copiado' implica 'mais de 93% de usuario'", 93.0,
       100.0 - 7.0, 0.0))
    a((u"cap.6", u"17 termos x 5 = 85 buscas", 85.0, 17.0 * 5.0, 0.0))
    a((u"cap.6", u"descarte fora do tema: 1.654 / 1.831 (fase3_no_tema.json)",
       90.3, 1654.0 / 1831.0 * 100.0, TOL_ARRED))
    a((u"cap.6", u"descarte no tema: 493 / 1.615", 30.5, 493.0 / 1615.0 * 100.0,
       TOL_ARRED))
    a((u"cap.6", u"residuo: 493 no tema entre 2.147 descartados", 23.0,
       493.0 / 2147.0 * 100.0, TOL_ARRED))
    a((u"cap.6", u"os dois lados do funil somam o tema: 1.040 + 575", 1615.0,
       1040.0 + 575.0, 0.0))
    a((u"cap.6", u"descartados = 493 no tema + 1.654 fora", 2147.0,
       493.0 + 1654.0, 0.0))

    # --- Cap. 7: TikTok ---
    a((u"cap.7", u"PoliTok: 195.373 + 743.588 = 938.961", 938961.0,
       195373.0 + 743588.0, 0.0))
    a((u"cap.7", u"deleção pela plataforma: 13,0 - 11,6 = 1,4 p.p.", 1.4,
       13.0 - 11.6, TOL_ARRED))
    a((u"cap.7", u"entre a 2a e a 3a verificacao: 18,7 - 17,3", 1.4, 18.7 - 17.3,
       TOL_ARRED))
    a((u"cap.7", u"'triplica': 18,7 / 6,3", 3.0, 18.7 / 6.3, 0.15))
    a((u"cap.7", u"serie com denominador cheio ~ serie x 0,54 (46% nao reverificado)",
       3.3, 6.3 * 0.54, 0.35))
    a((u"cap.7", u"02/out/2024 = 31 dias apos a eleicao da Saxonia (01/set/2024)",
       31.0, 31.0, 0.0))
    a((u"cap.7", u"10/dez/2024 = 100 dias apos 01/set/2024", 100.0, 100.0, 0.0))
    a((u"cap.7", u"13/jan/2025 = 134 dias apos 01/set/2024", 134.0, 134.0, 0.0))
    a((u"cap.7", u"'um em cada cinco' com intolerancia = 20,5%", 20.0, 20.5, 1.0))
    a((u"cap.7", u"'6 das 7 afirmacoes reproduzem' -> 1 nao fecha", 1.0,
       7.0 - 6.0, 0.0))

    # --- Cap. 8: conclusao (coerencia com os capitulos) ---
    a((u"cap.8", u"conclusao repete 57,6% do cap.5", 57.6, 57.6, 0.0))
    a((u"cap.8", u"conclusao repete 38,3 p.p. do cap.6", 38.3, 61.7 - 23.5,
       TOL_ARRED))
    a((u"cap.8", u"conclusao repete 6,4 p.p. do cap.6", 6.4, 39.0 - 32.7,
       TOL_ARRED))
    a((u"cap.8", u"tabela mestre: 4 de 13 linhas com fracao minima", 13.0, 13.0, 0.0))
    a((u"cap.8", u"6 casos = 5 inteiros + 1 parcial", 6.0, 5.0 + 1.0, 0.0))
    return R


def checa_relacoes():
    for cap, rotulo, afirmado, conta, tol in relacoes():
        confere(u"[%s] %s" % (cap, rotulo), afirmado, conta, 0, tol=tol)


# ---------------------------------------------------------------------------
# 5. camada PROCEDENCIA
# ---------------------------------------------------------------------------

def valores_json():
    u"""Todo numero que aparece em algum JSON congelado dos casos, em variantes
    de formatacao pt-BR (inteiro, 1 e 2 casas, e o mesmo x100)."""
    idx = set()

    def anota(v):
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return
        # o texto escreve o mesmo valor em varias escalas: 3.343.405 arestas,
        # "3,34 milhoes", "939 mil", fracao 0,1577 escrita como 15,77%
        for escala in (1.0, 100.0, 1e-3, 1e-6):
            x = v * escala
            if abs(x) > 1e12:
                continue
            for casas in (0, 1, 2, 3):
                idx.add(pt(x, casas))
            idx.add(pt(round(x), 0))

    def anda(o):
        if isinstance(o, dict):
            for k, val in o.items():
                anda(k)
                anda(val)
        elif isinstance(o, list):
            for val in o:
                anda(val)
        elif isinstance(o, (int, float)):
            anota(o)
        elif isinstance(o, str):
            for m in RE_NUM.finditer(o):
                idx.add(m.group(0))

    for raiz, _, arquivos in os.walk(CASOS):
        for nome in arquivos:
            if not nome.endswith(".json"):
                continue
            caminho = os.path.join(raiz, nome)
            if os.path.getsize(caminho) > 40 * 1024 * 1024:
                continue
            try:
                anda(json.load(io.open(caminho, encoding="utf-8")))
            except Exception:
                continue
    return idx


# Numeros que nao vem de dado nosso e nao precisam de JSON. Cada um com o motivo.
SEM_FONTE_JUSTIFICADO = {
    u"0": u"zero retorico", u"1": u"contagem em prosa", u"2": u"contagem em prosa",
    u"3": u"contagem em prosa", u"4": u"contagem em prosa", u"5": u"contagem em prosa",
    u"6": u"contagem em prosa", u"7": u"contagem em prosa", u"8": u"contagem em prosa",
    u"9": u"contagem em prosa", u"10": u"contagem em prosa", u"12": u"contagem em prosa",
    u"14": u"14 categorias de enquadramento (codebook_v1.json)",
    u"95": u"nivel de confianca", u"50": u"limiar H1 do artigo-alvo",
    u"100": u"complemento percentual / top-100 do artigo-alvo",
    u"2,5": u"percentil da banda", u"97,5": u"percentil da banda",
    u"2013": u"ano", u"2014": u"ano", u"2016": u"ano", u"2019": u"ano",
    u"2020": u"ano", u"2021": u"ano", u"2022": u"ano", u"2023": u"ano",
    u"2024": u"ano", u"2025": u"ano", u"2026": u"ano", u"2012": u"ano",
    u"2018": u"ano", u"2015": u"ano",
}


def valores_md():
    u"""Segunda camada de procedencia: numeros que aparecem nos .md dos casos.
    Vale menos que um JSON (nao e reexecutavel), mas distingue 'numero que a
    documentacao do caso registra' de 'numero que so existe no corpo.tex'."""
    idx = {}
    for raiz, _, arquivos in os.walk(CASOS):
        for nome in arquivos:
            if not nome.endswith(".md"):
                continue
            caminho = os.path.join(raiz, nome)
            try:
                txt = io.open(caminho, encoding="utf-8").read()
            except Exception:
                continue
            rel = os.path.relpath(caminho, CASOS).replace("\\", "/")
            for m in RE_NUM.finditer(txt):
                idx.setdefault(m.group(0), rel)
    return idx


def checa_procedencia(fs, mostrar):
    idx = valores_json()
    idx_md = valores_md()
    vistos = {}
    for linha, f in fs:
        for v, bruto, pos in numeros(f):
            if bruto in vistos:
                continue
            vistos[bruto] = (linha, f[max(0, pos - 60):pos + 40].strip())
    # o que uma relacao declarada ja confere nao precisa de fonte propria:
    # e resultado de outros numeros do texto (deltas, razoes, somas)
    declarados = set()
    for _, _, afirmado, _, _ in relacoes():
        for casas in (0, 1, 2):
            declarados.add(pt(afirmado, casas))
            declarados.add(pt(-afirmado, casas))

    faltam, so_md = [], []
    for bruto, (linha, ctx) in sorted(vistos.items(), key=lambda kv: kv[1][0]):
        if bruto in idx or bruto in SEM_FONTE_JUSTIFICADO or bruto in declarados:
            continue
        if bruto in idx_md:
            so_md.append((linha, bruto, ctx, idx_md[bruto]))
        else:
            faltam.append((linha, bruto, ctx))
    if mostrar:
        print(u"\n--- PROCEDENCIA (1): numeros do corpo.tex que nao estao em "
              u"nenhum JSON congelado nem em .md de caso ---")
        print(u"(nao e erro automaticamente: pode ser numero do artigo-alvo, do "
              u"levantamento (research.db,\n fora deste repo) ou de fonte "
              u"externa citada. Serve para saber o que depende de olho humano.)\n")
        for linha, bruto, ctx in faltam:
            print(u"  L%-5d %-12s  %s" % (linha, bruto, ctx[:86]))
        print(u"\n--- PROCEDENCIA (2): so em .md de caso, sem JSON reexecutavel ---\n")
        for linha, bruto, ctx, arq in so_md:
            print(u"  L%-5d %-12s  %-46s  <- %s" % (linha, bruto, ctx[:46], arq))
    return len(vistos), len(faltam), len(so_md)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv):
    tudo = "--tudo" in argv
    so_proc = "--procedencia" in argv

    linhas = carrega_tex()
    fs = frases(linhas)
    bruto = io.open(TEX, encoding="utf-8").read()

    if not so_proc:
        checa_deltas(fs)
        checa_soma_100(fs)
        checa_ic(fs)
        checa_fracoes(fs)
        checa_tabelas(bruto)
        checa_sanidade(fs)
        checa_relacoes()

        RESULTADOS.sort(key=lambda r: (-NIVEIS[r[0]], r[1]))
        larg = max((len(r[2]) for r in RESULTADOS), default=10)
        print(u"=" * 78)
        print(u"AUDITORIA DAS CONTAS DO corpo.tex")
        print(u"=" * 78)
        for nivel, linha, rotulo, detalhe in RESULTADOS:
            if nivel == "OK" and not tudo:
                continue
            onde = (u"L%d" % linha) if linha else u"--"
            print(u"%-8s %-6s %-*s  %s" % (nivel, onde, larg, rotulo, detalhe))
        cont = {n: 0 for n in NIVEIS}
        for r in RESULTADOS:
            cont[r[0]] += 1
        print(u"\n%d checagens: %d OK, %d ATENCAO, %d ERRO."
              % (len(RESULTADOS), cont["OK"], cont["ATENCAO"], cont["ERRO"]))

    total, faltam, so_md = checa_procedencia(fs, mostrar=(tudo or so_proc))
    print(u"\nPROCEDENCIA: %d numeros distintos no corpo.tex -- %d sem fonte "
          u"nenhuma neste repo,\n%d so em .md de caso (sem JSON reexecutavel), "
          u"o resto rastreado ate um JSON congelado.\n(rode com --procedencia "
          u"para ver as duas listas.)" % (total, faltam, so_md))

    if not so_proc:
        return 1 if any(r[0] == "ERRO" for r in RESULTADOS) else 0
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
