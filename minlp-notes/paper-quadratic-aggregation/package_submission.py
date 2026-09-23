#!/usr/bin/env python3
"""Create a deterministic, self-contained manuscript source archive."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build/final"
DIST = ROOT / "dist"


def main():
    for name in ["main.pdf", "main.bbl", "formal-supplement.pdf", "formal-supplement.bbl"]:
        if not (BUILD / name).is_file():
            raise SystemExit(f"Missing {BUILD / name}; run both final latexmk builds first.")
    DIST.mkdir(exist_ok=True)
    files = {}
    def add(path, archive_name=None):
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"Expected a regular source file: {path}")
        files[archive_name or str(path.relative_to(ROOT))] = path.read_bytes()
    for name in ["main.tex", "macros.tex", "references.bib", "README.md",
                 "FORMAL-VERIFICATION.md", "package_submission.py"]:
        add(ROOT / name)
    for path in sorted(ROOT.glob("formal-*.tex")):
        add(path)
    for folder in ["sections", "appendices"]:
        for path in sorted((ROOT / folder).glob("*.tex")):
            add(path)
    add(ROOT / "figures/finite-aggregation-slice.pdf")
    for path in sorted((ROOT / "supplement").glob("*.py")):
        add(path)
    add(ROOT / "supplement/README.md")
    lean = ROOT / "supplement/lean"
    for name in ["README.md", "Formal.lean", "lean-toolchain", "lakefile.toml",
                 "lake-manifest.json", "modules.json", "source-manifest.json", "verify.py"]:
        add(lean / name)
    for path in sorted((lean / "Formal").rglob("*.lean")):
        add(path)
    for audit in sorted((lean / "audits").iterdir()):
        for name in ["AuditAggregation.lean", "modules.json", "CLAIMS.md", "COVERAGE.md"]:
            add(audit / name)
    # Verification evidence is optional; an incomplete run is never represented as success.
    verification = lean / "verification"
    if (verification / "manifest.json").is_file():
        evidence = json.loads((verification / "manifest.json").read_text())
        inputs = evidence.get("inputs_sha256")
        if not isinstance(inputs, dict) or not inputs:
            raise SystemExit("Verification manifest has no input fingerprints.")
        for name, expected in inputs.items():
            data = files.get("supplement/lean/" + name)
            if data is None or hashlib.sha256(data).hexdigest() != expected:
                raise SystemExit(f"Stale verification evidence: {name}; rerun supplement/lean/verify.py.")
        add(verification / "manifest.json")
        for path in sorted(verification.glob("*.log")):
            add(path)
    for name in ["main.bbl", "formal-supplement.bbl"]:
        add(BUILD / name, name)
    record = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
    manifest = (json.dumps(record, indent=2) + "\n").encode()
    files["SOURCE-MANIFEST.json"] = manifest
    (DIST / "source-manifest.json").write_bytes(manifest)
    archive = DIST / "quadratic-aggregation-source.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo("quadratic-aggregation/" + name, (2026, 9, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            out.writestr(info, data)
    shutil.copyfile(BUILD / "main.pdf", ROOT / "paper.pdf")
    shutil.copyfile(BUILD / "formal-supplement.pdf", ROOT / "formal-supplement.pdf")
    print(f"Created {archive}: {len(files)} files, {archive.stat().st_size} bytes")
    print("Copied paper.pdf and formal-supplement.pdf")


if __name__ == "__main__":
    main()
