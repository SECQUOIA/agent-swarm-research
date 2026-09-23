"""Create a review snapshot without build debris or prior review snapshots."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) != 2 or Path(sys.argv[1]).name != sys.argv[1]:
        raise SystemExit("usage: python verification/freeze_stage.py STAGE-ROUND")
    target = ROOT / "process" / "snapshots" / sys.argv[1]
    if target.exists():
        raise SystemExit(f"snapshot already exists: {target}")
    paths = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if not path.is_file() or any(p in {"process", "__pycache__", ".git"} for p in rel.parts):
            continue
        if any(p.startswith("reviewer") for p in rel.parts):
            continue
        if path.suffix in {".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk", ".blg", ".pyc"}:
            continue
        paths.append((path, rel))
    target.mkdir(parents=True)
    manifest = {}
    for path, rel in sorted(paths):
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        manifest[str(rel)] = hashlib.sha256(dest.read_bytes()).hexdigest()
    (target / "snapshot-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"snapshot": str(target), "files": len(manifest)}))


if __name__ == "__main__":
    main()
