"""Check the Appendix H claim on E3 with kappa_target = 2 (F-dependencies-3):
filtered uniform grids use exactly 4(floor(sqrt(n/4))+1)+1 nodes per free
coordinate (plateau statistic of Figure E2 left: max over free coordinates,
median over the last four stages and the three seeds)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import csv, math, statistics
from collections import defaultdict
P = (_PUBLIC_REPO + '/paper-decomposition-aware/experiments/results/E3_stages.csv')
rows = [r for r in csv.DictReader(open(P)) if r['kappa_target'] == '2']
print('methods', sorted({r['method'] for r in rows}))
by = defaultdict(list)
for r in rows:
    by[(r['method'], int(r['n']), r['seed'])].append(r)
for meth in sorted({k[0] for k in by}):
    for n in sorted({k[1] for k in by if k[0] == meth}):
        f = 4 * (math.isqrt(n // 4) if False else int(math.floor(math.sqrt(n / 4))) + 1) + 1
        last4 = []
        allstages = set()
        for (m, nn, s), rs in by.items():
            if m != meth or nn != n:
                continue
            rs.sort(key=lambda r: int(r['stage']))
            last4 += [int(r['max_nodes_free']) for r in rs[-4:]]
            allstages |= {int(r['max_nodes_free']) for r in rs[-4:]}
        print(meth, n, 'formula', f, 'median last4', statistics.median(last4), 'set', sorted(allstages))
