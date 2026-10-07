"""Review r2: compare the 'review copies' (research-20260929/reviews/**/<name>.html) with today's page head (r1 re-fetch)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import glob, os
R = (_PUBLIC_REPO + '/research-20260929')
INST = R + '/publication/reviews/minlplib-status-r1/dl/inst'
names = {os.path.basename(p)[:-5] for p in glob.glob(INST + '/*.html')}
n = same = 0
for p in sorted(glob.glob(R + '/reviews/**/*.html', recursive=True)):
    nm = os.path.basename(p)[:-5]
    if nm not in names:
        continue
    b = open(p, 'rb').read()
    k = b.find(b'<PRE>')
    head = b[:k] if k > 0 else b
    cur = open(f'{INST}/{nm}.html', 'rb').read()
    kc = cur.find(b'<PRE>')
    cur = cur[:kc] if kc > 0 else cur
    n += 1; same += (head == cur)
    if head != cur:
        print('DIFF', os.path.relpath(p, R), len(head), len(cur))
print('review copies compared', n, 'identical heads', same)
