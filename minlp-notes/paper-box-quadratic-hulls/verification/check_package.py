"""Build and inspect only this manuscript and its submission archives."""

from pathlib import Path
import json
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile


paper = Path(__file__).resolve().parents[1]
verification = paper / "verification"
# The official repository supplies no publication date. Keep the year omitted
# rather than inventing one to satisfy plainnat's diagnostic convention.
expected_bibtex_diagnostics = {
    "Warning--empty year in BurerBoxQPInstances2019",
}


def run(command, directory, record):
    result = subprocess.run(command, cwd=directory, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (verification / record).write_text(result.stdout)
    if result.returncode:
        raise RuntimeError(f"{command!r} failed; see {verification / record}")
    return result.stdout


def check_log(path, allowed=()):
    lines = path.read_text().splitlines()
    diagnostics = [line for line in lines
                   if re.search(r"Warning(?::|--)|Overfull|Underfull|Undefined control", line)]
    problems = [line for line in diagnostics if line not in allowed]
    if problems:
        raise RuntimeError(f"Unresolved build diagnostics in {path}: {problems}")
    return diagnostics


run(["make"], paper, "build-output.log")
check_log(verification / "main.log")
local_bibtex_diagnostics = check_log(verification / "main.blg",
                                    expected_bibtex_diagnostics)
run([sys.executable, "verification/package.py"], paper, "packaging.log")
info = run(["pdfinfo", "main.pdf"], paper, "pdfinfo.txt")
pages = int(re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE).group(1))
author = re.search(r"^Author:[ \t]*(.*)$", info, re.MULTILINE)
assert author is None or not author.group(1).strip(), "PDF must be anonymous"
assert (paper / "main.pdf").read_bytes() == (verification / "main.pdf").read_bytes()

with TemporaryDirectory(prefix="box-hulls-submission-") as temporary:
    base = Path(temporary)
    with ZipFile(paper / "submission-source.zip") as archive:
        assert archive.testzip() is None
        archive.extractall(base / "source")
        source_count = len(archive.namelist())
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
         "main.tex"], base / "source", "portable-build.log")
    check_log(base / "source" / "main.log")
    portable_bibtex_diagnostics = check_log(base / "source" / "main.blg",
                                           expected_bibtex_diagnostics)

    with ZipFile(paper / "companion.zip") as archive:
        assert archive.testzip() is None
        archive.extractall(base / "records")
        companion_count = len(archive.namelist())
    output = run([sys.executable, "companion/inspect_records.py"],
                 base / "records", "portable-records.log")

results = {
    "pages": pages,
    "anonymous_pdf": True,
    "final_tex_diagnostics": [],
    "expected_bibtex_diagnostics": {
        "local": local_bibtex_diagnostics,
        "portable": portable_bibtex_diagnostics,
    },
    "local_build_exit": 0,
    "portable_source_build_exit": 0,
    "portable_companion_check_exit": 0,
    "source_archive_files": source_count,
    "companion_archive_files": companion_count,
    "companion_check": output.strip().splitlines(),
}
(verification / "final-checks.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
