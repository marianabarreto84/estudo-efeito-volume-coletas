# =====================================================================
#  Audita o rotulo "analise de conteudo" contra o TEXTO INTEGRAL do PDF.
#
#  Por que contra o PDF e nao contra o resumo: a coluna `abstract` do
#  research.db esta VAZIA nos 2.139 artigos extraidos. Qualquer teste de
#  "o artigo tem marca de analise de conteudo?" feito sobre titulo+resumo
#  roda, na pratica, so sobre o titulo -- e um titulo quase nunca diz
#  "codebook". O texto do PDF esta em disco e e onde a marca vive.
#
#  O que mede: entre os artigos que o Gemini rotulou "analise de
#  conteudo", quantos tem no corpo do texto alguma marca do metodo
#  (o termo literal, livro de codigos, dois codificadores, kappa,
#  Krippendorff, Bardin...). Compara com um grupo de controle de artigos
#  que NAO receberam o rotulo -- sem controle, a taxa nao quer dizer nada.
#
#  Nao usa LLM e nao gasta nada: le PDF de disco e casa expressao regular.
#
#  Uso:
#    python audita_rotulo_conteudo.py --n 150
# =====================================================================
import argparse
import json
import os
import random
import re
import sqlite3
import sys
import unicodedata

REPO = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
DB = os.path.join(REPO, "research.db")
sys.path.insert(0, REPO)

ROTULO = "analise de conteudo"

# Marcas do metodo, em tres graus de forca.
FORTE = re.compile(
    r"content analysis|analise de conteudo|an[aá]lise de conte[uú]do|"
    r"krippendorff|bardin|holsti|inter-?coder reliability|intercoder reliability|"
    r"inter-?rater reliability|interrater reliability|codebook|code book|"
    r"livro de c[oó]digos|coding scheme|coding frame",
    re.I,
)
FRACA = re.compile(
    r"cohen'?s kappa|\bkappa\b|two (independent )?coders|three coders|"
    r"human coders|manual(ly)? coded|manual coding|qualitative coding|"
    r"thematic analysis|analise tematica|annotation guidelines|"
    r"dois codificadores|anotadores independentes",
    re.I,
)


def norm(s):
    if not isinstance(s, str):
        return ""
    return unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode("ascii")


def classifica(txt):
    if FORTE.search(txt):
        return "forte"
    if FRACA.search(txt):
        return "fraca"
    return "nenhuma"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=150, help="tamanho de cada grupo")
    ap.add_argument("--semente", type=int, default=20260929)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    from services.pdf_extractor import extract_text

    con = sqlite3.connect(DB)
    com, sem = [], []
    for aid, titulo, pdf_path, a in con.execute(
        "select id, title, pdf_path, analyses from articles "
        "where pdf_path is not null and analyses is not null "
        "and trim(analyses) not in ('','null','[]','{}')"
    ):
        try:
            d = json.loads(a)
        except Exception:
            continue
        g = d.get("gemini")
        if not isinstance(g, dict):
            continue
        rot = {norm(x) for x in (g.get("analysis_types") or []) if isinstance(x, str)}
        (com if ROTULO in rot else sem).append((aid, titulo, pdf_path))

    print(f"rotulados '{ROTULO}' .... {len(com)}")
    print(f"nao rotulados (controle) . {len(sem)}")

    rnd = random.Random(args.semente)
    grupos = {
        "ROTULADOS": rnd.sample(com, min(args.n, len(com))),
        "CONTROLE": rnd.sample(sem, min(args.n, len(sem))),
    }

    saida = {}
    for nome, grupo in grupos.items():
        cont = {"forte": 0, "fraca": 0, "nenhuma": 0, "ilegivel": 0}
        exemplos = []
        for i, (aid, titulo, rel) in enumerate(grupo, 1):
            caminho = rel if os.path.isabs(rel) else os.path.join(REPO, rel)
            txt = extract_text(caminho) if os.path.exists(caminho) else None
            if not txt:
                cont["ilegivel"] += 1
                continue
            c = classifica(txt)
            cont[c] += 1
            if c == "nenhuma" and len(exemplos) < 8:
                exemplos.append((aid, (titulo or "")[:80]))
            if i % 25 == 0:
                print(f"  {nome}: {i}/{len(grupo)}...", flush=True)
        lidos = cont["forte"] + cont["fraca"] + cont["nenhuma"]
        saida[nome] = dict(cont, lidos=lidos, exemplos=exemplos)
        print(f"\n== {nome} (n lidos = {lidos}; ilegiveis {cont['ilegivel']}) ==")
        for k in ("forte", "fraca", "nenhuma"):
            print(f"   marca {k:8s}: {cont[k]:4d}  ({100*cont[k]/max(lidos,1):5.1f}%)")
        if exemplos:
            print("   sem marca nenhuma, exemplos:")
            for aid, t in exemplos:
                print(f"     #{aid} {t}")

    r, c = saida["ROTULADOS"], saida["CONTROLE"]
    pr = (r["forte"] + r["fraca"]) / max(r["lidos"], 1)
    pc = (c["forte"] + c["fraca"]) / max(c["lidos"], 1)
    print("\n" + "=" * 66)
    print(f"marca (forte ou fraca) nos ROTULADOS: {100*pr:.1f}%")
    print(f"marca (forte ou fraca) no CONTROLE .: {100*pc:.1f}%")
    print(f"diferenca: {100*(pr-pc):+.1f} p.p.")
    print()
    print("Leitura: se a diferenca for pequena, o rotulo nao esta separando")
    print("quem faz analise de conteudo de quem nao faz -- ele esta sendo")
    print("aposto em quase todo mundo, e a informacao que carrega e ~zero.")
    print("=" * 66)

    if args.json:
        json.dump(saida, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
