#!/usr/bin/env python3
"""Build anonymous submission files from an explicit, auditable input set.

Run with Python's standard library, latexmk, pdfLaTeX, and BibTeX installed.
Temporary build files are created outside the repository and removed on success.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parent
EPOCH = "946684800"
ZIP_TIME = (2000, 1, 1, 0, 0, 0)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def manifest(payload):
    return "".join(f"{sha256(data)}  {name}\n" for name, data in sorted(payload.items())).encode()


def archive(path, top, payload):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(f"{top}/{name}", date_time=ZIP_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            target.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE,
                        help="output directory (default: this delivery directory)")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    inputs = {}

    def read(path):
        data = path.read_bytes()
        inputs[path.relative_to(ROOT).as_posix()] = sha256(data)
        return data

    source = {name: read(PAPER / name) for name in ("main.tex", "references.bib")}
    for folder in ("sections", "tables", "figures"):
        for path in sorted((PAPER / folder).glob("*.tex")):
            source[path.relative_to(PAPER).as_posix()] = read(path)
    source["README.md"] = read(HERE / "README-source.md")
    source["MANIFEST.sha256"] = manifest(source)

    supplement = {
        "README.md": read(HERE / "README-supplement.md"),
        "API.md": read(HERE / "API.md"),
        "requirements.txt": read(HERE / "requirements.txt"),
    }
    paths = []
    for package in ("network_simplex", "network_simplex_compressed"):
        paths.extend(sorted((ROOT / "code" / package).glob("*.py")))
    for name in ("baselines", "strong_baselines", "test_strong_baselines", "run", "paper_stage06"):
        paths.append(ROOT / "code/network_simplex_benchmarks" / f"{name}.py")
    paths.extend([
        ROOT / "code/network_simplex_review/verify_flat_chain_implementation.py",
        ROOT / "code/network-simplex-bounded-rank-verify.py",
    ])
    for name in ("stage02-exact.py", "stage03-exact.py", "stage04-recovery.py",
                 "stage05-padding.py", "stage05-profile.py", "stage07/integral-hull.py",
                 "stage06-tables.py", "stage06-benchmarks.json", "reference/stage06/flat_chain.py"):
        paths.append(PAPER / "verification" / name)
    paths.extend(sorted((PAPER / "tables").glob("*.tex")))
    for path in paths:
        supplement[path.relative_to(ROOT).as_posix()] = read(path)
    for path in sorted((HERE / "checks").glob("*.py")):
        supplement[f"checks/{path.name}"] = read(path)
    supplement["MANIFEST.sha256"] = manifest(supplement)
    read(Path(__file__).resolve())
    read(HERE / "README.md")

    with tempfile.TemporaryDirectory(prefix="network-simplex-delivery-") as temporary:
        build = Path(temporary)
        for name, data in source.items():
            path = build / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        env = dict(os.environ, SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE="1", TZ="UTC")
        command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        result = subprocess.run(command, cwd=build, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode:
            raise SystemExit(result.stdout)
        log = (build / "main.log").read_text()
        forbidden = ("LaTeX Warning:", "Package natbib Warning:", "Overfull", "Underfull")
        if any(term in log for term in forbidden):
            raise SystemExit("Build diagnostics require review:\n" + log)
        shutil.copyfile(build / "main.pdf", output / "submission.pdf")

    archive(output / "latex-source.zip", "latex-source", source)
    archive(output / "computational-supplement.zip", "computational-supplement", supplement)
    result = {
        "schema": 1,
        "scope": "Anonymous submission files; internal review status is recorded separately.",
        "build": {"source_date_epoch": EPOCH, "zip_timestamp": list(ZIP_TIME),
                  "command": command, "determinism": "Same inputs and toolchain produce identical bytes."},
        "inputs": dict(sorted(inputs.items())),
        "payloads": {
            "latex-source.zip": {name: sha256(data) for name, data in sorted(source.items())},
            "computational-supplement.zip": {name: sha256(data) for name, data in sorted(supplement.items())},
        },
        "artifacts": {name: {"sha256": sha256((output / name).read_bytes()),
                             "bytes": (output / name).stat().st_size}
                      for name in ("submission.pdf", "latex-source.zip", "computational-supplement.zip")},
    }
    (output / "manifest.json").write_bytes(json_bytes(result))
    print(json.dumps({"artifacts": result["artifacts"],
                      "source_files": len(source), "supplement_files": len(supplement)}, indent=2))


if __name__ == "__main__":
    main()
