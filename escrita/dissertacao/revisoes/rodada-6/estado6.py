# -*- coding: utf-8 -*-
import io, os

P = r"c:\Users\maria\Documents\GitHub\dissertacao-mestrado\ESTADO.md"
s = io.open(P, encoding="utf-8", newline="").read()

old = "| **5** | \u25d0 **Revis\u00e3o da disserta\u00e7\u00e3o \u2014 rodada 4 aplicada em 22/ago/2026.**"
new = (
    "| **5** | \u26a0 **RODADA 6 INTERROMPIDA NO MEIO (22/ago/2026, 20h) \u2014 "
    "retomar por [`revisoes/rodada-6/RETOMAR.md`](escrita/dissertacao/revisoes/rodada-6/RETOMAR.md).** "
    "A Mariana comentou o [`revisao-5.pdf`](escrita/dissertacao/revisoes/revisao-5.pdf): "
    "**23 anota\u00e7\u00f5es** (pp. 12\u201372), todas planejadas. O `dissertacao.tex` (legendas + "
    "coloca\u00e7\u00e3o de floats) e o `referencias.bib` (entrada nova do **Heine 2025**) **j\u00e1 est\u00e3o "
    "gravados**; o **`corpo.tex` est\u00e1 intocado** \u2014 o script de aplica\u00e7\u00e3o abortou num `assert` "
    "antes de gravar, e a grava\u00e7\u00e3o \u00e9 at\u00f4mica, ent\u00e3o nada se perdeu. Retomar \u00e9 rodar "
    "`python revisoes/rodada-6/aplica6.py`, recompilar e publicar o `revisao-6.pdf`. "
    "Falta ainda a se\u00e7\u00e3o da rodada no `REVISOES.md`. Tr\u00eas pedidos estruturais desta leitura: "
    "(a) **a legenda de tabela pela terceira vez** \u2014 tratada de vez, no pre\u00e2mbulo e tabela a "
    "tabela; (b) a **disserta\u00e7\u00e3o do Alexandre Heine** entra nos trabalhos relacionados, na "
    "linha de amostragem (ela acertou o enquadramento); (c) o **cap\u00edtulo do TikTok** \u00e9 "
    "t\u00e9cnico demais e precisa fechar pelo argumento. O registro anterior: "
    "\u25d0 **Revis\u00e3o da disserta\u00e7\u00e3o \u2014 rodada 4 aplicada em 22/ago/2026.**"
)

assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)

tmp = P + ".tmp"
with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
    fh.write(s)
os.replace(tmp, P)
print("ok")
