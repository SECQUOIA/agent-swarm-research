"""Freeze manuscript inputs for one independent review round."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

root = Path(__file__).resolve().parents[1]
label = sys.argv[1]
if not label or Path(label).name != label:
    raise SystemExit("Supply a single review-round directory name")
target = root / "process" / "snapshots" / label
target.mkdir(parents=True, exist_ok=False)
files = []
for path in sorted(root.rglob("*")):
    relative = path.relative_to(root)
    if not path.is_file() or relative.parts[0] in {"build", "verification", "process", ".git"}:
        continue
    if path.suffix in {".tex", ".bib", ".sty", ".cls", ".pdf", ".png", ".svg", ".csv", ".json", ".py", ".md"} or path.name in {"Makefile", ".latexmkrc"}:
        files.append(path)
coverage = root / "process" / "coverage.md"
if coverage.exists():
    files.append(coverage)
hashes = {}
for source in files:
    relative = source.relative_to(root)
    destination = target / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    hashes[str(relative)] = hashlib.sha256(source.read_bytes()).hexdigest()
manifest = json.dumps(hashes, indent=2, sort_keys=True) + "\n"
(target / "SHA256.json").write_text(manifest)
print(json.dumps({"snapshot": str(target), "files": len(hashes), "manifest_sha256": hashlib.sha256(manifest.encode()).hexdigest()}))
