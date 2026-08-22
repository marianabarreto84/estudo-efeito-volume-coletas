#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extrai as anotacoes (destaques + notas) de um PDF revisado.

Uso:  python extrai_comentarios.py revisao-2.pdf [> comentarios.md]

Para cada anotacao imprime: pagina, tipo, o texto destacado (recortado dos
/QuadPoints com pdfplumber) e o comentario da Mariana (/Contents).
Faz parte do fluxo descrito em REVISOES.md.
"""
import sys
import pdfplumber
from pypdf import PdfReader


def quad_bboxes(quadpoints):
    """/QuadPoints -> lista de bboxes (x0, top, x1, bottom) em coord. PDF."""
    pts = [float(p) for p in quadpoints]
    out = []
    for i in range(0, len(pts), 8):
        xs = pts[i:i + 8:2]
        ys = pts[i + 1:i + 8:2]
        out.append((min(xs), min(ys), max(xs), max(ys)))
    return out


def main(path):
    reader = PdfReader(path)
    plumb = pdfplumber.open(path)
    n = 0
    for pno, page in enumerate(reader.pages, start=1):
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            subtype = str(obj.get("/Subtype", ""))
            if subtype in ("/Link", "/Popup"):
                continue
            contents = (obj.get("/Contents") or "").strip()
            highlighted = ""
            qp = obj.get("/QuadPoints")
            if qp:
                ppage = plumb.pages[pno - 1]
                h = ppage.height
                chunks = []
                for (x0, y0, x1, y1) in quad_bboxes(qp):
                    # PDF: y cresce pra cima; pdfplumber: top cresce pra baixo
                    crop = (max(x0 - 1, 0), max(h - y1 - 1, 0),
                            min(x1 + 1, ppage.width), min(h - y0 + 1, h))
                    try:
                        t = ppage.crop(crop).extract_text() or ""
                    except Exception:
                        t = ""
                    if t.strip():
                        chunks.append(" ".join(t.split()))
                highlighted = " / ".join(chunks)
            if not (contents or highlighted):
                continue
            n += 1
            print(f"\n### [{n}] p.{pno}  {subtype}")
            if highlighted:
                print(f"TRECHO: {highlighted}")
            if contents:
                print(f"COMENTARIO: {contents}")
    plumb.close()
    print(f"\n---\nTOTAL: {n} anotacoes", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "revisao-1.pdf")
