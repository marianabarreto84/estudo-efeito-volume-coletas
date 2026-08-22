# =====================================================================
#  Congela o rotulo de estrato (pago x aberto) a partir dos dumps do DBLP.
#
#  POR QUE ISTO EXISTE. A coluna `articles.pdf_inaccessible` NAO serve
#  como rotulo de estrato durante a expansao, porque retry_pdfs.py a
#  reescreve enquanto roda:
#     - sucesso  -> pdf_inaccessible = False
#     - falha    -> pdf_inaccessible = True (quando nao e --only-open)
#  Ou seja, o proprio ato de medir apaga a variavel pela qual se mede:
#  artigos recuperados saem do estrato pago, e artigos que o DBLP dizia
#  abertos entram nele ao falhar. Medir a taxa do estrato pago contra a
#  coluna viva subestima a taxa e infla a do outro estrato.
#
#  Isso ja aconteceu nesta sessao: entre duas leituras, o estrato pago
#  caiu de 10,4% (22/212) para 5,1% (19/369) sem que nenhuma medida real
#  mudasse -- so a coluna havia sido reescrita por um commit concorrente.
#
#  A fonte estavel e o campo <access> dos dumps XML em dblp_dumps/, que
#  foi o que definiu pdf_inaccessible na importacao original
#  (scripts/import_dblp.py: pdf_inaccessible = access=="closed" ...).
#  Os XML sao de mai/2026 e ninguem escreve neles.
#
#  Uso:  python congela_estratos.py     -> grava estratos.json
# =====================================================================
import json
import os
import re
import xml.etree.ElementTree as ET
from collections import Counter

REPO = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
DUMPS = os.path.join(REPO, "dblp_dumps")
AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "estratos.json")

DOI_RE = re.compile(r"^https?://(dx\.)?doi\.org/", re.I)


def norm_doi(url):
    if not url:
        return None
    u = url.strip()
    if DOI_RE.match(u):
        return DOI_RE.sub("", u).lower()
    if u.lower().startswith("10."):
        return u.lower()
    return None


def main():
    acesso = {}
    conflitos = 0
    arquivos = sorted(f for f in os.listdir(DUMPS) if f.endswith(".xml"))
    for i, fn in enumerate(arquivos, 1):
        try:
            tree = ET.parse(os.path.join(DUMPS, fn))
        except ET.ParseError:
            continue
        for hit in tree.iter("hit"):
            info = hit.find("info")
            if info is None:
                continue
            acc = (info.findtext("access") or "").strip().lower()
            doi = None
            for ee in info.iter("ee"):
                doi = norm_doi(ee.text)
                if doi:
                    break
            if not doi or not acc:
                continue
            if doi in acesso and acesso[doi] != acc:
                # dedupe do import_dblp prefere "open" quando o mesmo paper
                # aparece em conferencia e no arXiv; repete-se a regra aqui.
                conflitos += 1
                if acc == "open":
                    acesso[doi] = acc
            else:
                acesso[doi] = acc
        if i % 20 == 0:
            print(f"  {i}/{len(arquivos)} dumps...", flush=True)

    c = Counter(acesso.values())
    print(f"\n{len(arquivos)} dumps lidos | {len(acesso)} DOIs com <access>")
    print(f"  open   : {c.get('open', 0)}")
    print(f"  closed : {c.get('closed', 0)}")
    for k, v in c.items():
        if k not in ("open", "closed"):
            print(f"  {k or '(vazio)'} : {v}")
    print(f"  DOIs com access divergente entre dumps (resolvidos p/ open): {conflitos}")

    json.dump(
        {"congelado_em": "2026-08-21", "fonte": "dblp_dumps/*.xml campo <access>",
         "n": len(acesso), "acesso": acesso},
        open(SAIDA, "w", encoding="utf-8"), ensure_ascii=False,
    )
    print(f"\ngravado em {SAIDA}")


if __name__ == "__main__":
    main()
