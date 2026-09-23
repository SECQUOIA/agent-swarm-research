"""Freeze manuscript inputs for an independent review round."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) != 2 or '/' in sys.argv[1] or sys.argv[1] in {'.', '..'}:
        raise SystemExit('usage: python verification/snapshot.py ROUND_NAME')
    dest = ROOT / 'process' / 'snapshots' / sys.argv[1]
    dest.mkdir(parents=True, exist_ok=False)
    inputs = []
    for pattern in ('*.tex', '*.bib', 'README.md', 'PROCESS.md',
                    'sections/**/*.tex', 'appendices/**/*.tex',
                    'checks/**/*.py', 'checks/**/*.json',
                    'verification/*.py', 'verification/reference/*.py',
                    'process/coverage.md'):
        inputs.extend(ROOT.glob(pattern))
    manifest = {}
    for src in sorted(set(inputs)):
        if not src.is_file():
            continue
        rel = src.relative_to(ROOT)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        manifest[str(rel)] = hashlib.sha256(src.read_bytes()).hexdigest()
    (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'{dest}: {len(manifest)} inputs frozen')


if __name__ == '__main__':
    main()
