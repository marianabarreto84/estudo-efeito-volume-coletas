"""
Fase 2 (caso AGECovP) — reproduzir o PONTO ORIGINAL sobre o gabarito dos autores.

Roda inteiramente offline, sobre `gabarito_zenodo/` (Zenodo 15800324). Nenhuma
chamada de API. Objetivo: fixar o ponto de partida ANTES da expansao, e descobrir
em que convencao cada numero publicado reproduz.

Alvos-teste (FASE0 §5)
----------------------
  AG1  distribuicao de sentimento dos comentarios (TextBlob 39/39/22; VADER 39/39/22)
  AG2  os comentarios sao mais negativos que os videos            <- o comparativo
  AG4  categorias de canal (Society 56,4%, Lifestyle 13,6%, Knowledge 12,1%,
       Politics 4,1%, Health 3,7%)

AG3 (UGC < 7%) fica de fora: o artigo nao publica a regra que separa "user-generated"
de "veiculo de imprensa", e o gabarito nao traz a coluna. Registrado como pendencia.

Convencoes testadas
-------------------
Nenhum numero e reportado sem antes procurar a convencao que o reproduz — os canais
tem MULTIPLAS categorias, e contar por canal, por atribuicao ou so a primeira da
resultados muito diferentes (76,6% x 42% x ...). O mesmo cuidado do AV1 do vacinas.

Uso: PYTHONIOENCODING=utf-8 python -u analise/fase2_ponto_original.py
Saida: stdout + data/repl/agecovp2020/fase2_ponto_original.json
"""
import collections
import csv
import json
import pathlib
import sys

csv.field_size_limit(10 ** 8)

G = pathlib.Path("data/repl/agecovp2020/gabarito_zenodo")
OUT = pathlib.Path("data/repl/agecovp2020/fase2_ponto_original.json")

ALVO_CATEGORIAS = {"Society": 56.4, "Lifestyle_(sociology)": 13.6, "Knowledge": 12.1,
                   "Politics": 4.1, "Health": 3.7}
ALVO_TEXTBLOB = {"neutro": 39, "positivo": 39, "negativo": 22}
ALVO_VADER = {"positivo": 39, "negativo": 39, "neutro": 22}


def log(m):
    print(m, flush=True)


def le(nome):
    with open(G / nome, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def cats(r):
    """Categorias de um canal, normalizadas (o campo e uma lista de URLs da Wikipedia)."""
    t = r.get("TopicCategories") or ""
    out = []
    for x in t.split(","):
        x = x.strip().strip("[]'\" ")
        if not x:
            continue
        out.append(x.split("/")[-1])
    return out


def pct(d):
    tot = sum(d.values())
    return {k: round(100 * v / tot, 1) for k, v in d.items()} if tot else {}


def classifica(v, pos, neg):
    if v is None:
        return None
    return "positivo" if v > pos else ("negativo" if v < neg else "neutro")


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    res = {}

    # ---------------- AG4: categorias de canal ----------------
    ch = le("channels.csv")
    log("canais: %d" % len(ch))
    por_canal = collections.Counter()       # canal conta 1 em cada categoria sua
    por_atribuicao = collections.Counter()  # cada par (canal, categoria) conta 1
    primeira = collections.Counter()        # so a 1a categoria de cada canal
    sem_cat = 0
    for r in ch:
        cs = cats(r)
        if not cs:
            sem_cat += 1
            continue
        primeira[cs[0]] += 1
        for c in set(cs):
            por_canal[c] += 1
        for c in cs:
            por_atribuicao[c] += 1

    log("canais sem categoria: %d" % sem_cat)
    convs = {
        "por canal (fracao dos canais)": {k: round(100 * v / len(ch), 1)
                                          for k, v in por_canal.items()},
        "por atribuicao (fracao das atribuicoes)": pct(por_atribuicao),
        "primeira categoria": pct(primeira),
        "por canal, so quem tem categoria": {k: round(100 * v / (len(ch) - sem_cat), 1)
                                             for k, v in por_canal.items()},
    }
    log("\n== AG4: categorias de canal (alvo: Society 56,4 / Lifestyle 13,6 / "
        "Knowledge 12,1 / Politics 4,1 / Health 3,7)")
    melhor, melhor_erro = None, 1e9
    for nome, d in convs.items():
        erro = sum(abs(d.get(k, 0) - v) for k, v in ALVO_CATEGORIAS.items())
        log("  %-42s %s  | erro total %.1f p.p."
            % (nome, " ".join("%s=%.1f" % (k[:9], d.get(k, 0)) for k in ALVO_CATEGORIAS), erro))
        if erro < melhor_erro:
            melhor, melhor_erro = nome, erro
    log("  -> convencao mais proxima: **%s** (erro %.1f p.p.)" % (melhor, melhor_erro))
    res["AG4"] = {"convencoes": convs, "alvo": ALVO_CATEGORIAS,
                  "melhor_convencao": melhor, "erro_pp": round(melhor_erro, 1)}

    # ---------------- AG1: sentimento dos comentarios ----------------
    cm = le("comments.csv")
    log("\ncomentarios: %d" % len(cm))
    tb = collections.Counter()
    vd = collections.Counter()
    for r in cm:
        t = classifica(num(r.get("TextBlob_SenC")), 0.0, 0.0)
        v = classifica(num(r.get("VADER_SenC")), 0.05, -0.05)
        if t:
            tb[t] += 1
        if v:
            vd[v] += 1
    log("\n== AG1: sentimento dos comentarios")
    log("  TextBlob  medido %s   | artigo %s" % (pct(tb), ALVO_TEXTBLOB))
    log("  VADER     medido %s   | artigo %s" % (pct(vd), ALVO_VADER))
    e_tb = sum(abs(pct(tb).get(k, 0) - v) for k, v in ALVO_TEXTBLOB.items())
    e_vd = sum(abs(pct(vd).get(k, 0) - v) for k, v in ALVO_VADER.items())
    log("  erro total: TextBlob %.1f p.p. | VADER %.1f p.p." % (e_tb, e_vd))
    res["AG1"] = {"textblob": pct(tb), "vader": pct(vd), "alvo_textblob": ALVO_TEXTBLOB,
                  "alvo_vader": ALVO_VADER, "erro_textblob_pp": round(e_tb, 1),
                  "erro_vader_pp": round(e_vd, 1)}

    # ---------------- AG2: comentarios x videos ----------------
    vids = le("videos.csv")
    ktox_v = "Toxicity"
    tox_v = [num(r.get(ktox_v)) for r in vids]
    tox_v = [x for x in tox_v if x is not None]
    tox_c = [num(r.get("Toxicity")) for r in cm]
    tox_c = [x for x in tox_c if x is not None]
    log("\n== AG2: comentarios sao mais negativos que os videos?")
    if tox_v and tox_c:
        mv = sum(tox_v) / len(tox_v)
        mc = sum(tox_c) / len(tox_c)
        log("  toxicidade media: videos %.4f (n=%d) x comentarios %.4f (n=%d)"
            % (mv, len(tox_v), mc, len(tox_c)))
        log("  -> comentarios %s toxicos" % ("MAIS" if mc > mv else "MENOS"))
        res["AG2"] = {"toxicidade_media_videos": round(mv, 4),
                      "toxicidade_media_comentarios": round(mc, 4),
                      "comentarios_mais_toxicos": bool(mc > mv),
                      "n_videos": len(tox_v), "n_comentarios": len(tox_c)}
    else:
        log("  (sem coluna de toxicidade utilizavel nos dois lados)")

    # sentimento dos videos nao vem no gabarito -> registrado como limite
    res["AG2_ressalva"] = ("o gabarito traz sentimento so dos comentarios; a comparacao "
                           "video x comentario foi feita por TOXICIDADE, que existe nos "
                           "dois. Declarar no capitulo.")

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    log("\nescrito em %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
