#!/usr/bin/env python3
"""Fingerprint the distribution, excluding caches and transient TeX files."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output = root / "verification" / "SHA256SUMS"
transient = {".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".out", ".toc"}
paths = []
for path in root.rglob("*"):
    rel = path.relative_to(root)
    if not path.is_file() or path == output:
        continue
    if any(part in {".lake", "__pycache__", "pages"} for part in rel.parts):
        continue
    if path.suffix in transient or rel.as_posix() == "main.log":
        continue
    paths.append(path)
output.write_text("".join(
    f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root).as_posix()}\n"
    for path in sorted(paths)
))
print(f"Recorded {len(paths)} delivery files in {output.relative_to(root)}.")
