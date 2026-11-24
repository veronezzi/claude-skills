#!/usr/bin/env python3
"""Converte um DOCX em PDF usando LibreOffice ou pandoc.

Uso:
  python cv_to_pdf.py input.docx output.pdf
"""
import shutil
import subprocess
import sys
from pathlib import Path


def convert(docx_path, pdf_path):
    docx_path = Path(docx_path).resolve()
    pdf_path = Path(pdf_path).resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    # Tenta LibreOffice
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(pdf_path.parent), str(docx_path)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        produced = pdf_path.parent / (docx_path.stem + ".pdf")
        if produced != pdf_path and produced.exists():
            produced.rename(pdf_path)
        print(f"OK (LibreOffice): {pdf_path}")
        return

    # Tenta pandoc
    pandoc = shutil.which("pandoc")
    if pandoc:
        subprocess.run([pandoc, str(docx_path), "-o", str(pdf_path)], check=True)
        print(f"OK (pandoc): {pdf_path}")
        return

    print("ERRO: nem LibreOffice nem pandoc encontrados. Instale um deles.", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Uso: python cv_to_pdf.py input.docx output.pdf", file=sys.stderr)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
