"""Reviewer check: sha256 of every file listed in the track's sources/manifest.tsv; unlisted and missing files."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import csv, hashlib, sys
from pathlib import Path
root = Path((_PUBLIC_REPO + '/research-20260929/publication/literature/small/sources'))
lines = (root / 'manifest.tsv').read_text().split('\n')
rows = [l.split('\t') for l in lines if l.strip() and not l.startswith('#')]
pi, si = 0, 3
print('comment lines:', sum(1 for l in lines if l.startswith('#')))
listed = set(); bad = []; missing = []
for r in rows:
    p = r[pi]; listed.add(p)
    f = root / p
    if not f.exists():
        missing.append(p); continue
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    if h != r[si].strip():
        bad.append(p)
actual = {str(f.relative_to(root)) for f in root.rglob('*') if f.is_file() and f.name != 'manifest.tsv'}
print('rows', len(rows), 'distinct paths', len(listed), 'bad', len(bad), bad, 'missing', len(missing), missing)
print('unlisted', sorted(actual - listed))
