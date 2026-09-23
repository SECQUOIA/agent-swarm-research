"""Compile the manuscript and record reference, layout, and input checks."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PAPER = Path(__file__).resolve().parents[1]


def main():
    build = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        cwd=PAPER, capture_output=True, text=True, check=False,
    )
    (PAPER / "verification" / "build-output.txt").write_text(build.stdout + build.stderr)
    log = (PAPER / "main.log").read_text(errors="replace") if (PAPER / "main.log").exists() else ""
    warnings = [
        line for line in log.splitlines()
        if re.search(r"Warning:|Overfull|undefined|multiply defined", line, re.I)
    ]
    files = sorted(PAPER.glob("*.tex")) + sorted((PAPER / "sections").glob("*.tex"))
    labels = {}
    for path in files:
        for label in re.findall(r"\\label\{([^}]+)\}", path.read_text()):
            labels.setdefault(label, []).append(str(path.relative_to(PAPER)))
    duplicates = {label: paths for label, paths in labels.items() if len(paths) > 1}
    appendix = (PAPER / "sections" / "appendix-cubic-certificates.tex").read_text()
    printed_checker = "".join(re.findall(
        r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", appendix, re.S,
    ))
    checker_matches = printed_checker == (
        PAPER / "verification" / "check_stage02_finite.py"
    ).read_text()
    report = {
        "compile_exit": build.returncode,
        "warnings": warnings,
        "duplicate_labels": duplicates,
        "printed_stage02_checker_matches_file": checker_matches,
        "inputs": {
            str(path.relative_to(PAPER)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in files + sorted(PAPER.glob("*.bib"))
        },
    }
    pdf = PAPER / "main.pdf"
    if pdf.exists():
        report["pdf_sha256"] = hashlib.sha256(pdf.read_bytes()).hexdigest()
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True)
        report["pdfinfo"] = info.stdout
        subprocess.run(["pdftotext", "-layout", str(pdf), str(PAPER / "verification" / "manuscript.txt")], check=True)
    (PAPER / "verification" / "build-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "inputs"}, indent=2))
    unresolved = any(re.search(r"undefined|multiply defined", line, re.I) for line in warnings)
    return int(bool(build.returncode or duplicates or unresolved or not checker_matches))


if __name__ == "__main__":
    sys.exit(main())
