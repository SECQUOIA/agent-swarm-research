#!/usr/bin/env python3
"""Build the delivered manuscript sources outside the research repository."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
archive_path = ROOT / "delivery/quadratic-intersection-cuts-source.zip"
with tempfile.TemporaryDirectory(prefix="qic-source-delivery-") as temporary:
    destination = Path(temporary)
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        assert all(
            not Path(name).is_absolute() and ".." not in Path(name).parts
            for name in names
        )
        archive.extractall(destination)
    package = destination / "quadratic-intersection-cuts"
    static = subprocess.run(
        [sys.executable, "verification/check_document.py"],
        cwd=package, capture_output=True, text=True, check=True,
    )
    print(static.stdout, end="", flush=True)
    command = [
        "latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
        "-outdir=build", "main.tex",
    ]
    build = subprocess.run(command, cwd=package, capture_output=True, text=True)
    (ROOT / "build/portable-source-build.log").write_text(build.stdout + build.stderr)
    build.check_returncode()
    log_paths = [package / "build/main.log"]
    bib_log = package / "build/main.blg"
    if bib_log.exists():
        log_paths.append(bib_log)
    for path in log_paths:
        assert not re.search(r"Warning|Overfull|Underfull|undefined|Error", path.read_text())
        shutil.copyfile(path, ROOT / "build" / ("portable-" + path.name))
    subprocess.run(
        ["pdftotext", "-layout", "build/main.pdf", "build/main.txt"],
        cwd=package, check=True,
    )
    assert (package / "build/main.txt").read_text() == (ROOT / "build/main.txt").read_text()
    bibliography = package / "build/main.bbl"
    if not bibliography.exists():
        bibliography = package / "main.bbl"
    assert bibliography.read_bytes() == (ROOT / "delivery/main.bbl").read_bytes()
    info = subprocess.check_output(["pdfinfo", str(package / "build/main.pdf")], text=True)
    expected = subprocess.check_output(["pdfinfo", str(ROOT / "paper.pdf")], text=True)
    pages = re.search(r"Pages:\s+(\d+)", info).group(1)
    assert pages == re.search(r"Pages:\s+(\d+)", expected).group(1)
    assert re.search(r"^Author:\s*$", info, re.MULTILINE)
    print(
        f"Portable source build PASS: {len(names)} files, {pages} pages, blank author; "
        "identical manuscript text and bibliography; clean final compilation logs."
    )
