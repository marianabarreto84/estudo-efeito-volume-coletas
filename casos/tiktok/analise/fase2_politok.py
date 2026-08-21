"""
Fase 2 do caso TikTok — o ponto original do PoliTok-DE, reproduzido OFFLINE.

Contexto
--------
A credencial da Research API do eTC esta morta (README §2b), o que matou a rota de
coleta. Mas o alvo escolhido para a celula TikTok publica seu dataset no Hugging
Face sob CC-BY, e a parte que sustenta as afirmacoes centrais — o **status de
disponibilidade** de cada post em varias datas — vem no arquivo de IDs. Ou seja: o
ponto original e verificavel **sem hidratar nada e sem cota**.

Alvo
----
Ruiz et al., "PoliTok-DE: A Multimodal Dataset of Political TikToks and Deletions
From Germany", arXiv 2509.15860 (2025). Dados:
huggingface.co/datasets/tomasruiz/PoliTok-DE

Afirmacoes testadas (do resumo do artigo)
-----------------------------------------
  PT1  "over 930,000 posts"
  PT2  18,7% dos posts da Saxonia foram deletados
  PT3  39,7% dos posts da eleicao federal foram deletados
  PT4  "about two thirds of the deletions were creator withdrawals"
  PT5  "platform-deletion rate we computed was 13.0% of all posts"
  PT6  "about one in five posts conveyed intolerance"
  PT7  "a majority conveyed humor"

Uso: PYTHONIOENCODING=utf-8 python -u analise/fase2_politok.py
Saida: stdout + data/politok_de/fase2_politok.json
"""
import json
import pathlib
import sys
from collections import Counter

import pandas as pd

D = pathlib.Path("data/politok_de")
OUT = D / "fase2_politok.json"

# regras candidatas para "delecao pela plataforma" (o artigo nao publica a dele)
REGRAS_PLATAFORMA = {
    "A: audit_not_pass + violation": ["audit_not_pass", "violation"],
    "B: A + status_reviewing": ["audit_not_pass", "violation", "status_reviewing"],
    "C: A + content_classification": ["audit_not_pass", "violation", "content_classification"],
    "D: A + reviewing + content_classification":
        ["audit_not_pass", "violation", "status_reviewing", "content_classification"],
    "F: D + copyright": ["audit_not_pass", "violation", "status_reviewing",
                         "content_classification", "copyright"],
}


def log(m):
    print(m, flush=True)


def veredito(medido, alvo, tol):
    return "REPLICA" if abs(medido - alvo) <= tol else "nao replica"


def main():
    sx = pd.read_parquet(D / "data_saxony_2024_post_ids.parquet")
    fd = pd.read_parquet(D / "data_federal_2025_post_ids.parquet")
    an = pd.read_parquet(D / "data_saxony_2024_annotations.parquet")
    res = {}

    # ---- PT1: volume ----
    tot = len(sx) + len(fd)
    log("PT1  posts: saxonia %d + federal %d = **%d**  (artigo: >930.000)  -> %s"
        % (len(sx), len(fd), tot, "REPLICA" if tot > 930000 else "nao replica"))
    res["PT1"] = {"saxonia": len(sx), "federal": len(fd), "total": tot,
                  "alvo": ">930000", "replica": bool(tot > 930000)}

    # ---- PT2/PT3: taxa de delecao ----
    log("\n== taxas de delecao por coleta e por data de checagem ==")
    curvas = {}
    for nome, df in (("saxonia", sx), ("federal", fd)):
        curvas[nome] = {}
        for c in [c for c in df.columns if c.startswith("availability")]:
            data = c.replace("availability_", "").replace("_", "-")
            vc = df[c].value_counts()
            p = 100 * vc.get("DELETED", 0) / len(df)
            curvas[nome][data] = round(p, 1)
            log("  %-8s %s : %6.1f%% deletado  (disponivel %.1f%%, nao-rechecado %.1f%%)"
                % (nome, data, p, 100 * vc.get("AVAILABLE", 0) / len(df),
                   100 * vc.get("NOT_RESCRAPED", 0) / len(df)))
    sax_final = curvas["saxonia"]["2025-01-13"]
    fed_final = curvas["federal"]["2026-06-11"]
    log("\nPT2  saxonia deletados: **%.1f%%**  (artigo 18,7%%)  -> %s"
        % (sax_final, veredito(sax_final, 18.7, 0.3)))
    log("PT3  federal deletados: **%.1f%%**  (artigo 39,7%%)  -> %s"
        % (fed_final, veredito(fed_final, 39.7, 0.3)))
    res["PT2"] = {"medido": sax_final, "alvo": 18.7}
    res["PT3"] = {"medido": fed_final, "alvo": 39.7}
    res["curvas_por_data"] = curvas

    # ---- PT4/PT5: autor x plataforma (so na coleta federal, que e a do artigo) ----
    d = fd[fd["availability_2026_06_11"] == "DELETED"]
    s = d["status_codes_2026_06_11"].astype(str)

    def lado(x):
        if "audit_not_pass" in x or "violation" in x:
            return "plataforma"
        if "author_" in x or "status_deleted" in x or "item_not_exist" in x:
            return "autor"
        return "indefinido"

    L = Counter(lado(x) for x in s)
    p_autor = 100 * L["autor"] / len(d)
    log("\nPT4  retirada pelo AUTOR: **%.1f%%** dos deletados  (artigo ~2/3 = 66,7%%)  -> %s"
        % (p_autor, veredito(p_autor, 66.7, 3.0)))
    log("     (plataforma %.1f%% | indefinido %.1f%% dos deletados)"
        % (100 * L["plataforma"] / len(d), 100 * L["indefinido"] / len(d)))
    res["PT4"] = {"medido_pct_dos_deletados": round(p_autor, 1), "alvo": 66.7,
                  "distribuicao": dict(L)}

    log("\nPT5  taxa de delecao pela PLATAFORMA (artigo: 13,0%% de TODOS os posts)")
    log("     o artigo nao publica quais codigos conta como plataforma; convencoes:")
    melhor, melhor_err = None, 1e9
    conv = {}
    for nome, toks in REGRAS_PLATAFORMA.items():
        n = int(s.apply(lambda x: any(t in x for t in toks)).sum())
        p = 100 * n / len(fd)
        conv[nome] = round(p, 1)
        err = abs(p - 13.0)
        log("       %-44s %6.1f%%  (erro %.1f p.p.)" % (nome, p, err))
        if err < melhor_err:
            melhor, melhor_err = nome, err
    log("     -> mais proxima: %s = %.1f%% | erro **%.1f p.p.** -> %s"
        % (melhor, conv[melhor], melhor_err,
           "REPLICA aprox." if melhor_err <= 2 else "nao replica"))
    res["PT5"] = {"convencoes": conv, "alvo": 13.0, "melhor": melhor,
                  "erro_pp": round(melhor_err, 1)}

    # ---- PT6/PT7: anotacoes humanas ----
    log("\n== anotacoes (Saxonia): %d anotacoes sobre %d posts, %d anotadores ==="
        % (len(an), an["post_id"].nunique(), an["annotator_id"].nunique()))
    por_anotacao = {}
    for col in ("is_intolerant", "is_hedonic_entertainment"):
        vc = an[col].value_counts(normalize=True) * 100
        por_anotacao[col] = round(float(vc.get("yes", 0)), 1)
    # por POST (voto majoritario), ja que 300 posts tem mais de uma anotacao
    por_post = {}
    for col in ("is_intolerant", "is_hedonic_entertainment"):
        g = an.groupby("post_id")[col].apply(
            lambda x: (x == "yes").sum() > (x == "no").sum())
        por_post[col] = round(100 * float(g.mean()), 1)

    log("PT6  intolerancia: por anotacao **%.1f%%** | por post (voto majoritario) %.1f%%"
        "   (artigo: ~1 em 5 = 20%%)  -> %s"
        % (por_anotacao["is_intolerant"], por_post["is_intolerant"],
           veredito(por_anotacao["is_intolerant"], 20.0, 2.0)))
    log("PT7  humor (hedonic): por anotacao **%.1f%%** | por post %.1f%%"
        "   (artigo: maioria = >50%%)  -> %s"
        % (por_anotacao["is_hedonic_entertainment"], por_post["is_hedonic_entertainment"],
           "REPLICA" if por_anotacao["is_hedonic_entertainment"] > 50 else "nao replica"))
    res["PT6"] = {"por_anotacao": por_anotacao["is_intolerant"],
                  "por_post": por_post["is_intolerant"], "alvo": 20.0}
    res["PT7"] = {"por_anotacao": por_anotacao["is_hedonic_entertainment"],
                  "por_post": por_post["is_hedonic_entertainment"], "alvo": ">50"}
    res["nota_anotacoes"] = ("935 anotacoes sobre 360 posts (300 com mais de uma). "
                             "As porcentagens do artigo batem com a contagem POR ANOTACAO; "
                             "por post o valor muda. Convencao nao declarada no artigo.")

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    log("\nescrito em %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
