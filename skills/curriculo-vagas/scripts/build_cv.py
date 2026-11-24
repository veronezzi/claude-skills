#!/usr/bin/env python3
"""Gera um currículo DOCX ATS-friendly a partir de um JSON.

Uso:
  python build_cv.py input.json output.docx
"""
import json
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
except ImportError as e:
    print("ERRO: python-docx não instalado. Rode: pip install python-docx", file=sys.stderr)
    sys.exit(1)


def set_base_style(doc):
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.line_spacing = 1.08
    for section in doc.sections:
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)


def add_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text.upper())
    r.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(0x1F, 0x3B, 0x5C)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p


def build(data, out_path):
    doc = Document()
    set_base_style(doc)

    # Cabeçalho
    name = data.get("name", "")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(name)
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = RGBColor(0x1F, 0x3B, 0x5C)
    p.paragraph_format.space_after = Pt(0)

    title = data.get("target_title", "")
    if title:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        p.paragraph_format.space_after = Pt(2)

    contact = data.get("contact", {}) or {}
    parts = []
    if contact.get("email"):
        parts.append(contact["email"])
    if contact.get("phone"):
        parts.append(contact["phone"])
    if contact.get("linkedin"):
        parts.append(contact["linkedin"])
    if contact.get("city"):
        parts.append(contact["city"])
    if parts:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(" | ".join(parts))
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        p.paragraph_format.space_after = Pt(6)

    # Resumo
    summary = data.get("summary", "")
    if summary:
        add_heading(doc, "Resumo profissional")
        p = doc.add_paragraph(summary)

    # Experiência
    exps = data.get("experience", []) or []
    if exps:
        add_heading(doc, "Experiência profissional")
        for e in exps:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(e.get("title", ""))
            r.bold = True
            company = e.get("company", "")
            if company:
                r2 = p.add_run(f"  |  {company}")
                r2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            period = e.get("period", "")
            if period:
                p2 = doc.add_paragraph()
                p2.paragraph_format.space_after = Pt(2)
                r = p2.add_run(period)
                r.italic = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
            for b in e.get("bullets", []) or []:
                add_bullet(doc, b)

    # Formação
    edus = data.get("education", []) or []
    if edus:
        add_heading(doc, "Formação acadêmica")
        for ed in edus:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(ed.get("degree", ""))
            r.bold = True
            inst = ed.get("institution", "")
            year = ed.get("year", "")
            if inst:
                p.add_run(f"  |  {inst}")
            if year:
                r = p.add_run(f"  ({year})")
                r.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    # Skills
    skills = data.get("skills", []) or []
    if skills:
        add_heading(doc, "Skills")
        p = doc.add_paragraph()
        p.add_run(", ".join(skills))

    # Idiomas
    langs = data.get("languages", []) or []
    if langs:
        add_heading(doc, "Idiomas")
        for l in langs:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(l.get("name", ""))
            r.bold = True
            if l.get("level"):
                p.add_run(f" - {l['level']}")

    # Projetos
    projs = data.get("projects", []) or []
    if projs:
        add_heading(doc, "Projetos e certificações")
        for pr in projs:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(pr.get("name", ""))
            r.bold = True
            if pr.get("description"):
                p.add_run(f" - {pr['description']}")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    print(f"OK: {out_path}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python build_cv.py input.json output.docx", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8-sig") as f:
        data = json.load(f)
    build(data, sys.argv[2])


if __name__ == "__main__":
    main()
