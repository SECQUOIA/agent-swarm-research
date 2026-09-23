#!/usr/bin/env python3
"""Compile the standalone paper and record source, text, and layout checks."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[1]
records = root / "verification"
records.mkdir(exist_ok=True)
command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
result = subprocess.run(command, cwd=root, capture_output=True, text=True)
(records / "latexmk.log").write_text(result.stdout + result.stderr)
if result.returncode:
    raise SystemExit(f"LaTeX build failed; see {records / 'latexmk.log'}")
log = (root / "main.log").read_text(errors="replace")
(records / "latex.log").write_text(log)
failures = [line for line in log.splitlines() if re.search(
    r"Overfull|undefined|multiply defined|There were multiply-defined", line)]
warnings = [line for line in log.splitlines() if "Warning" in line or "Underfull" in line]
info = subprocess.run(["pdfinfo", "main.pdf"], cwd=root, capture_output=True,
                      text=True, check=True).stdout
subprocess.run(["pdftotext", "-layout", "main.pdf", "verification/paper.txt"],
               cwd=root, check=True)
report = {
    "command": command,
    "pages": int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1)),
    "failures": failures,
    "warnings": warnings,
    "sha256": {path: hashlib.sha256((root / path).read_bytes()).hexdigest()
               for path in ["main.tex", "references.bib", "main.pdf", "verification/paper.txt"]},
}
(records / "paper-build.json").write_text(json.dumps(report, indent=2) + "\n")
if failures:
    raise SystemExit(f"Paper checks failed: {failures}")
print(f"PASS: {report['pages']} pages, no unresolved references or overfull boxes; "
      f"{len(warnings)} layout/package warnings.")
