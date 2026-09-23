"""Freeze manuscript sources for a named independent-review round."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

paper = Path(__file__).resolve().parents[1]
name = sys.argv[1]
if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for c in name):
    raise SystemExit("Use a lowercase stage/round name")
out = paper / "process" / "snapshots" / name
if out.exists():
    raise SystemExit(f"Snapshot already exists: {out}")
paths = [p for p in paper.glob("*") if p.is_file() and p.suffix in (".tex", ".bib", ".md")]
for folder in ("sections", "appendices", "figures", "tables"):
    base = paper / folder
    if base.exists():
        paths.extend(p for p in base.rglob("*") if p.is_file())
manifest = {}
for path in sorted(paths):
    relative = path.relative_to(paper)
    target = out / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    manifest[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
(out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"{name}: {len(manifest)} files frozen")
