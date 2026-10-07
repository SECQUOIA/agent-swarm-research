# Reviewer r2: recompute sha256 of every manifest row; list unlisted/missing files.
import hashlib, os, sys
root = sys.argv[1]
rows = []
for line in open(os.path.join(root, 'manifest.tsv'), encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    f = line.rstrip('\n').split('\t')
    rows.append(f)
bad = []; missing = []
listed = set()
for f in rows:
    path = f[0]; sha = f[-1].strip()
    listed.add(path)
    p = os.path.join(root, path)
    if not os.path.exists(p):
        missing.append(path); continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if h != sha:
        bad.append((path, h, sha))
allfiles = set()
for d, _, fs in os.walk(root):
    for x in fs:
        rel = os.path.relpath(os.path.join(d, x), root)
        if rel != 'manifest.tsv':
            allfiles.add(rel)
print('rows', len(rows), 'distinct paths', len(listed))
print('missing', missing)
print('bad', bad)
print('unlisted', sorted(allfiles - listed))
