"""Freeze manuscript and executable dependencies for an independent review round."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / 'paper-network-simplex'
REVISION = Path(__file__).resolve().parent

def freeze(name):
    target = REVISION / name
    target.mkdir()  # Never replace a prior review freeze.
    sources = []
    for name in ('main.tex', 'main.pdf', 'references.bib', 'README.md', 'PROCESS.md'):
        sources.append(PAPER / name)
    for name in ('sections', 'tables', 'figures', 'appendices', 'delivery'):
        folder = PAPER / name
        if folder.exists():
            sources += [p for p in folder.rglob('*')
                        if p.is_file() and '__pycache__' not in p.parts]
    for name in ('network_simplex', 'network_simplex_compressed',
                 'network_simplex_benchmarks', 'network_simplex_review'):
        sources += [p for p in (ROOT / 'code' / name).rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts]
    sources.append(ROOT / 'code/network-simplex-bounded-rank-verify.py')
    sources += list((PAPER / 'verification').glob('*.py'))
    sources += list((PAPER / 'verification').glob('stage*.json'))
    for name in ('verification/stage07/integral-hull.py',
                 'verification/reference/stage06/flat_chain.py'):
        sources.append(PAPER / name)
    manifest = {}
    for source in sorted(set(sources)):
        relative = source.relative_to(ROOT)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        manifest[str(relative)] = hashlib.sha256(destination.read_bytes()).hexdigest()
    (target / 'sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'snapshot': str(target), 'files': len(manifest)}))

if __name__ == '__main__':
    freeze(sys.argv[1])
