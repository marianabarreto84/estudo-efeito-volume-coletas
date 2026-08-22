# =====================================================================
#  Reconcilia os PDFs em disco com o banco.
#
#  Por que existe: retry_pdfs.py so faz db.commit() DEPOIS de terminar a
#  fila inteira (o commit vem apos o asyncio.gather de todas as tarefas).
#  Numa fila de 11.093 artigos isso e uma corrida de ~10 h com um unico
#  ponto de gravacao -- se ela for interrompida, o banco nao registra
#  nada, embora os PDFs ja estejam em disco.
#
#  A recuperacao e trivial porque o nome do arquivo e derivado do DOI
#  (services/pdf_fetcher.py: doi.replace("/","_").replace(":","_") + ".pdf").
#  Este script varre pdfs/, casa cada arquivo com o artigo correspondente
#  e grava pdf_path onde estiver faltando.
#
#  Uso:
#    python reconcilia_pdfs.py            -> so relata (nao escreve)
#    python reconcilia_pdfs.py --aplicar  -> grava pdf_path e zera o flag
# =====================================================================
import argparse
import os
import sqlite3

REPO = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
DB = os.path.join(REPO, "research.db")
PDF_DIR = os.path.join(REPO, "pdfs")

MIN_BYTES = 1024  # descarta download truncado/pagina de erro salva como .pdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="grava no banco (default: so relata)")
    args = ap.parse_args()

    em_disco = {
        f[:-4]: os.path.join("pdfs", f)
        for f in os.listdir(PDF_DIR)
        if f.endswith(".pdf")
    }
    con = sqlite3.connect(DB)
    faltando, vazios = [], []
    for aid, doi, pdf_path in con.execute(
        "select id, doi, pdf_path from articles where doi is not null"
    ):
        if pdf_path:
            continue
        chave = doi.replace("/", "_").replace(":", "_")
        rel = em_disco.get(chave)
        if not rel:
            continue
        tam = os.path.getsize(os.path.join(REPO, rel))
        (vazios if tam < MIN_BYTES else faltando).append((aid, rel, tam))

    print(f"PDFs em disco ................ {len(em_disco)}")
    print(f"em disco mas sem pdf_path .... {len(faltando)}")
    if vazios:
        print(f"descartados por tamanho <1KB . {len(vazios)}")

    if not faltando:
        print("\nnada a reconciliar -- o banco esta em dia com o disco.")
        return

    if not args.aplicar:
        print("\n(relatorio apenas; rode com --aplicar para gravar)")
        for aid, rel, tam in faltando[:10]:
            print(f"   id={aid:<6d} {rel}  ({tam//1024} KB)")
        if len(faltando) > 10:
            print(f"   ... e mais {len(faltando)-10}")
        return

    for aid, rel, _ in faltando:
        con.execute(
            "update articles set pdf_path=?, pdf_inaccessible=0 where id=?", (rel, aid)
        )
    con.commit()
    print(f"\ngravados {len(faltando)} pdf_path (e pdf_inaccessible=0 neles).")


if __name__ == "__main__":
    main()
