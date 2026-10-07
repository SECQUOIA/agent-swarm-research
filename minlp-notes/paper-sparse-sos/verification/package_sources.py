#!/usr/bin/env python3
"""Package the standalone manuscript, excluding research and review records."""

from pathlib import Path
import hashlib
import json
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DELIVERY = ROOT / "delivery"
DELIVERY.mkdir(exist_ok=True)
files = list(ROOT.glob("*.tex")) + list(ROOT.glob("*.bib"))
for folder in ("sections", "appendices", "figures", "tables"):
    directory = ROOT / folder
    if directory.exists():
        files.extend(path for path in directory.rglob("*") if path.is_file()
                     and path.suffix in {".tex", ".pdf", ".png", ".jpg", ".eps"})
files.append(ROOT / "delivery" / "BUILD.md")
files.append(ROOT / "verification" / "check_sources.py")
if not all(path.is_file() for path in files):
    raise SystemExit("A required source or BUILD.md is missing.")
manifest = {}
archive = DELIVERY / "sparse-sos-source.zip"
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as out:
    for path in sorted(set(files)):
        name = "BUILD.md" if path.name == "BUILD.md" else str(path.relative_to(ROOT))
        data = path.read_bytes()
        out.writestr(name, data)
        manifest[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    out.writestr("source-manifest.json", json.dumps(manifest, indent=2) + "\n")
(DELIVERY / "source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Packaged {len(manifest)} files in {archive.relative_to(ROOT)}")
