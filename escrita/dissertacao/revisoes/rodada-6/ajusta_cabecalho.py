# -*- coding: utf-8 -*-
"""Encurta o titulo corrente (cabecalho) dos capitulos longos.

Sem isso o \leftmark de dois capitulos estoura a largura do cabecalho: o
Cap. 8 encavala no numero da pagina e o Cap. 6 quebra em duas linhas.
O \chaptermark mexe SO no cabecalho -- sumario e abertura do capitulo
seguem com o titulo por extenso.
"""
import io, os

P = "corpo.tex"
s = io.open(P, encoding="utf-8", newline="").read()

CURTOS = [
    ("Primeiro Caso Executado: \#Elei\u00e7\u00f5es2014 no Twitter",
     "Primeiro Caso: \#Elei\u00e7\u00f5es2014 no Twitter"),
    ("Segundo Caso Executado: o Debate Vacinal no Twitter",
     "Segundo Caso: o Debate Vacinal no Twitter"),
    ("Terceiro e Quarto Casos Executados: Pap\u00e9is Sociais e Homofilia no Reddit",
     "Terceiro e Quarto Casos: o Reddit"),
    ("Quinto Caso Executado: Idosos e Pandemia no YouTube",
     "Quinto Caso: Idosos e Pandemia no YouTube"),
    ("Um Sexto Caso, Parcial: Dele\u00e7\u00e3o de Conte\u00fado Pol\u00edtico no TikTok",
     "Sexto Caso, Parcial: o TikTok"),
]

for longo, curto in CURTOS:
    old = "\chapter{%s}" % longo
    new = "%s\n\chaptermark{%s}" % (old, curto)
    if s.count(new) == 1:          # idempotente
        print("  ja aplicado:", curto)
        continue
    assert s.count(old) == 1, (s.count(old), longo[:40])
    s = s.replace(old, new)
    print("  ok:", curto)

tmp = P + ".tmp"
with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
    fh.write(s)
os.replace(tmp, P)
print("gravado")
