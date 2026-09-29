"""Audita o quanto a taxonomia de tipos de análise cobre os rótulos extraídos.

A Tabela 2 da revisão (e a Tabela 1.1 da dissertação) não é uma lista fechada que o
modelo escolheu: o campo `analysis_types` é aberto, e o que produz as categorias da
tabela é o `bucketize` de `figuras.py`, aplicado depois da extração. Este script mede a
cobertura desse mapeamento — quantos rótulos entram na tabela, quantos ficam fora e
quais são os que ficam fora.

O mapeamento é lido do próprio `figuras.py`, e não reescrito aqui, para que as duas
contas não possam divergir.

Saída: `rotulos_analise_auditoria.json`, ao lado deste arquivo.
Uso: python audita_rotulos_analise.py
"""

import io
import json
import os
import re
import sqlite3
import unicodedata
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
DB = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey\research.db"
SAIDA = os.path.join(AQUI, "rotulos_analise_auditoria.json")

# O guarda-chuva que foi excluído da tabela de propósito (ver §4.2 da revisão).
GUARDA_CHUVA = "analise de conteudo"


def carrega_mapeamento():
    """Importa norm/ANALYSIS_BUCKETS/bucketize do figuras.py, sem executar o resto."""
    src = io.open(os.path.join(AQUI, "figuras.py"), encoding="utf-8").read()
    bloco = src[src.index("def norm("):src.index("VOL_BLOCK")]
    ns = {"re": re, "unicodedata": unicodedata}
    exec(bloco, ns)
    return ns["norm"], ns["bucketize"], ns["ANALYSIS_BUCKETS"]


def carrega_base():
    """Mesma base da revisão: extração do modelo adotado, sem os descartados."""
    con = sqlite3.connect(DB)
    rows = con.execute(
        "select analyses from articles where analyses is not null "
        "and trim(analyses) not in ('','null','[]','{}')"
    ).fetchall()
    base = []
    for (t,) in rows:
        try:
            a = json.loads(t)
        except Exception:
            continue
        g = a.get("gemini")
        if not isinstance(g, dict) or g.get("suggested_discard"):
            continue
        base.append(g)
    return base


def main():
    norm, bucketize, buckets = carrega_mapeamento()
    base = carrega_base()

    rotulos = 0
    fora = 0
    fora_sem_guarda_chuva = 0
    com_rotulo = 0
    sem_categoria_nenhuma = 0
    orfaos = Counter()
    por_categoria = Counter()

    for g in base:
        labs = [x.strip() for x in (g.get("analysis_types") or [])
                if isinstance(x, str) and x.strip()]
        if labs:
            com_rotulo += 1
        cats = {bucketize(x) for x in labs} - {None}
        if labs and not cats:
            sem_categoria_nenhuma += 1
        for c in cats:
            por_categoria[c] += 1
        for x in labs:
            rotulos += 1
            if bucketize(x) is None:
                fora += 1
                n = norm(x)
                orfaos[n] += 1
                if n != GUARDA_CHUVA:
                    fora_sem_guarda_chuva += 1

    r = {
        "base": len(base),
        "artigos_com_rotulo": com_rotulo,
        "rotulos": rotulos,
        "rotulos_por_artigo": round(rotulos / com_rotulo, 2) if com_rotulo else None,
        "fora_da_taxonomia": fora,
        "fora_pct": round(100 * fora / rotulos, 1) if rotulos else None,
        "fora_sem_guarda_chuva": fora_sem_guarda_chuva,
        "fora_sem_guarda_chuva_pct": (round(100 * fora_sem_guarda_chuva / rotulos, 1)
                                      if rotulos else None),
        "artigos_sem_categoria_nenhuma": sem_categoria_nenhuma,
        "artigos_sem_categoria_pct": round(100 * sem_categoria_nenhuma / len(base), 1),
        "categorias": len(buckets),
        "artigos_por_categoria": dict(por_categoria.most_common()),
        "orfaos_mais_frequentes": orfaos.most_common(30),
    }
    io.open(SAIDA, "w", encoding="utf-8", newline="\n").write(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n")

    print("base: %d artigos" % r["base"])
    print("rotulos extraidos: %d (%.2f por artigo)" % (r["rotulos"], r["rotulos_por_artigo"]))
    print("fora da taxonomia: %d (%.1f%%); sem o guarda-chuva: %d (%.1f%%)" % (
        r["fora_da_taxonomia"], r["fora_pct"],
        r["fora_sem_guarda_chuva"], r["fora_sem_guarda_chuva_pct"]))
    print("artigos que nao entram em categoria nenhuma: %d (%.1f%%)" % (
        r["artigos_sem_categoria_nenhuma"], r["artigos_sem_categoria_pct"]))
    print("-> %s" % SAIDA)


if __name__ == "__main__":
    main()
