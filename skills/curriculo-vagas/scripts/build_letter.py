#!/usr/bin/env python3
"""Gera uma carta de apresentação em DOCX.

Uso:
  python build_letter.py input.json output.docx
"""
import json
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    print("ERRO: python-docx não instalado. Rode: pip install python-docx", file=sys.stderr)
    sys.exit(1)


def build(data, out_path):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    for s in doc.sections:
        s.top_margin = Cm(2.5)
        s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(2.5)
        s.right_margin = Cm(2.5)

    # Remetente
    p = doc.add_paragraph(data.get("sender_name", ""))
    p.runs[0].bold = True
    for line in data.get("sender_contact", []):
        doc.add_paragraph(line)
    doc.add_paragraph("")

    # Data
    doc.add_paragraph(data.get("date", ""))
    doc.add_paragraph("")

    # Destinatário
    for line in data.get("recipient", []):
        doc.add_paragraph(line)
    doc.add_paragraph("")

    # Saudação
    doc.add_paragraph(data.get("salutation", "Prezado(a),"))
    doc.add_paragraph("")

    # Corpo
    for para in data.get("body", []):
        doc.add_paragraph(para)

    doc.add_paragraph("")
    doc.add_paragraph(data.get("closing", "Atenciosamente,"))
    doc.add_paragraph("")
    p = doc.add_paragraph(data.get("sender_name", ""))
    p.runs[0].bold = True

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    print(f"OK: {out_path}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python build_letter.py input.json output.docx", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8-sig") as f:
        data = json.load(f)
    build(data, sys.argv[2])


if __name__ == "__main__":
    main()
