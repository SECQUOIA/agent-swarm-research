"""Review r2 (finishing verifier): spot checks of report claims.
1. side-table examples (methanol50 5.01625659, lop97icx 11.2897376) present in cmp_forms diffs;
2. methanol50 audit verify record (max_move, Krawczyk rho, obj enclosure);
3. Last-Modified dates of the 69 current .gms/.osil files (author's part_a.json)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, collections
from fractions import Fraction as F
R = (_PUBLIC_REPO + '/research-20260929')
L = f'{R}/publication/reviews/minlplib-status-r2/logs'
for n, v in [('methanol50', '5.01625659'), ('lop97icx', '11.2897376')]:
    for m, a, b in json.load(open(f'{L}/cmp_forms_{n}.json'))['diffs']:
        if F(a) == F(v):
            print(n, 'monomial', m, 'gms', float(F(a)), 'osil', repr(float(F(b))))
d = json.load(open(f'{R}/bound-audit/logs/verify/methanol50.p4.json'))
print('methanol50.p4 audit:', d['status'], d['route'], 'max_move', d['max_move'], 'krawczyk', d['krawczyk'], 'obj', d['obj_lo'][:16], d['obj_hi'][:16])
c = collections.defaultdict(list)
def walk(o, path, name):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'last_modified':
                c[(path, v[5:16])].append(name)
            else:
                walk(v, path + '/' + k, name)
    elif isinstance(o, list):
        for x in o:
            walk(x, path, name)
for n, v in json.load(open(f'{R}/publication/minlplib-status/data/part_a.json'))['instances'].items():
    walk(v, '', n)
for k, v in sorted(c.items()):
    print('Last-Modified', k, len(v), v if len(v) < 10 else '')
