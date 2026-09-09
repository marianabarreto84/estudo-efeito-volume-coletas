# -*- coding: utf-8 -*-
"""Acabamento de entrega (9/set/2026).

Duas mudancas de acabamento, ambas reversiveis numa linha:

[A] O capitulo final deixa de se chamar "Conclusao Parcial e Proximos Passos"
    e passa a "Conclusao". O corpo do capitulo nao se diz parcial em lugar
    nenhum -- ele apresenta a tabela mestre com 15 linhas fechadas, a secao de
    banco de dados, as limitacoes e os proximos passos, que e exatamente o que
    se espera de uma conclusao. "Proximos passos" continua sendo uma secao
    dele, como e padrao. O rotulo "Parcial" era autoavaliacao de uma fase em
    que havia menos casos fechados, e hoje subestima o que esta entregue.

[B] Titulos curtos de sumario para as secoes 2.2 e 2.4, que quebravam em duas
    linhas no sumario. A forma curta preserva o autor de referencia, que foi
    justamente o pedido da Mariana no comentario [5] da rodada 6; o titulo por
    extenso continua na abertura da secao.
"""
import io, os

P = r"c:\Users\maria\Documents\GitHub\dissertacao-mestrado\escrita\dissertacao\corpo.tex"
s = io.open(P, encoding="utf-8", newline="").read()


def rep(old, new, esperado=1):
    """Substitui, com idempotencia: se o novo ja esta la, nao faz nada."""
    global s
    if s.count(new) == esperado and s.count(old) == 0:
        print("  (ja aplicado)", new[:56].replace("\n", " "))
        return
    assert s.count(old) == esperado, (s.count(old), esperado, old[:70])
    s = s.replace(old, new)
    print("  ok:", new[:56].replace("\n", " "))


# --- [A] o capitulo final ---------------------------------------------
rep(u"\\chapter{Conclus\u00e3o Parcial e Pr\u00f3ximos Passos}",
    u"\\chapter{Conclus\u00e3o}")

# --- [B] titulos curtos de sumario ------------------------------------
rep(u"\\section[A cr\u00edtica metodol\u00f3gica ao dado social: de boyd e Crawford ao erro\n"
    u"total]{",
    u"\\section[A cr\u00edtica ao dado social: boyd e Crawford]{")

rep(u"\\section[A sensibilidade dos m\u00e9todos ao dado dispon\u00edvel: de Kossinets ao\n"
    u"multiverso]{",
    u"\\section[A sensibilidade dos m\u00e9todos: Kossinets]{")

tmp = P + ".tmp"
with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
    fh.write(s)
os.replace(tmp, P)
print("gravado")
