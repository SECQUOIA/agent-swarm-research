#!/usr/bin/env python3
"""Package only the manuscript inputs and the compiled bibliography."""

from pathlib import Path
import hashlib
import re
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DELIVERY = ROOT / "delivery"
DELIVERY.mkdir(exist_ok=True)
shutil.copyfile(ROOT / "build/main.bbl", DELIVERY / "main.bbl")

inputs = set()


def collect(path):
    path = path.resolve()
    if path in inputs:
        return
    path.relative_to(ROOT)
    inputs.add(path)
    text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text(encoding="utf-8"))
    for name in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", text):
        target = ROOT / name
        collect(target if target.suffix else target.with_suffix(".tex"))


collect(ROOT / "main.tex")
inputs.add(ROOT / "references.bib")
inputs.add(ROOT / "verification/check_document.py")

readme = """# Limits and Guarantees for Quadratic Intersection Cuts

Anonymous manuscript source package. The PDF and electronic evidence
companion are supplied separately.

Build from this directory with a standard TeX Live installation:

    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex

All manuscript inputs use relative paths. The package includes references.bib
and the compiled main.bbl. No research notes, literature folder, solver,
external data, or machine-specific path is needed to build the paper.

The optional source check uses only the Python standard library:

    python3 verification/check_document.py
"""

target = DELIVERY / "quadratic-intersection-cuts-source.zip"
prefix = Path("quadratic-intersection-cuts")
with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(inputs):
        archive.write(path, str(prefix / path.relative_to(ROOT)))
    archive.write(DELIVERY / "main.bbl", str(prefix / "main.bbl"))
    archive.writestr(str(prefix / "README.md"), readme)

print(f"Packaged {len(inputs) + 2} files: {target.relative_to(ROOT)}")
print(f"SHA256 {hashlib.sha256(target.read_bytes()).hexdigest()}")
