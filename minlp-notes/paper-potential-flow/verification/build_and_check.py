#!/usr/bin/env python3
"""Build both papers and retain input hashes and final LaTeX diagnostics."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def diagnostics(log):
    patterns = {
        "errors": r"^!.*$|^.+:\d+: .*Error.*$|^.*Emergency stop.*$|^.*Fatal error.*$",
        "undefined_references": r"^.*(?:Reference .* undefined|There were undefined references).*$",
        "undefined_citations": r"^.*(?:Citation .* undefined|There were undefined citations).*$",
        "duplicate_labels": r"^.*(?:Label .* multiply defined|There were multiply-defined labels).*$",
    }
    result = {key: re.findall(pattern, log, re.MULTILINE)
              for key, pattern in patterns.items()}
    result["overfull_boxes"] = len(re.findall(r"Overfull \\[hv]box", log))
    return result


def build(paper):
    folder = ROOT / paper
    command = ["latexmk", "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
               "-outdir=build", "main.tex"]
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(folder.rglob("*"))
              if p.suffix in {".tex", ".bib"} and "build" not in p.relative_to(folder).parts}
    result = {"command": command, "cwd": paper, "input_sha256": hashes,
              "build_performed": False}
    stdout = stderr = ""
    try:
        process = subprocess.run(command, cwd=folder, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", check=False)
        result.update(returncode=process.returncode, build_performed=True)
        stdout, stderr = process.stdout, process.stderr
    except OSError as error:
        result["returncode"] = 1
        stderr = str(error)
    log_path = folder / "build/main.log"
    result.update(diagnostics(log_path.read_text(errors="replace") if log_path.exists() else ""))
    if not log_path.is_file():
        result["errors"].append("Missing build/main.log")
    result["pdf_exists"] = (folder / "build/main.pdf").is_file()
    if not result["pdf_exists"]:
        result["errors"].append("Missing build/main.pdf")
    result["passed"] = result["returncode"] == 0 and not any(
        result[key] for key in ("errors", "undefined_references", "undefined_citations",
                               "duplicate_labels"))
    if not result["passed"]:
        print(stdout, end="", file=sys.stdout)
        print(stderr, file=sys.stderr)
    return result


def main():
    papers = {paper: build(paper) for paper in ("complexity", "uncertainty")}
    passed = all(result["passed"] for result in papers.values())
    report = {"passed": passed, "papers": papers}
    (ROOT / "verification/build-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    for paper, result in papers.items():
        print(f"{'PASS' if result['passed'] else 'FAIL'}: {paper}; "
              f"overfull boxes: {result['overfull_boxes']}")
        if not result["passed"]:
            for key in ("errors", "undefined_references", "undefined_citations", "duplicate_labels"):
                for message in result[key]:
                    print(message, file=sys.stderr)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
