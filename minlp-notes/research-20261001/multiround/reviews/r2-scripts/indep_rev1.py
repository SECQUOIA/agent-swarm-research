"""Reviewer r2: independent recomputation of the revision-1 statistics from raw records.
Reads logs/main, logs/new, logs/rev1 (not smoke). Paired t-intervals."""
import glob, gzip, json, os, re, sys
import numpy as np
from scipy import stats
B = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
D = {}
for f in sorted(glob.glob(B + '/main/*.jsonl*') + glob.glob(B + '/new/*.jsonl*') + glob.glob(B + '/rev1/rev1*.jsonl*')):
    size = re.search(r'_(\d+x\d+)_', os.path.basename(f)).group(1)
    op = gzip.open if f.endswith('.gz') else open
    with op(f, 'rt') as fh:
        for line in fh:
            r = json.loads(line)
            assert r['status'] == 'ok', (f, r['inst'], r['rule'])
            k = (size, r['inst'], r['rule'])
            c = np.array(r['closed'])
            if k in D:
                assert np.max(np.abs(D[k] - c)) == 0, k
            D[k] = c
sizes = ['4x4', '6x8', '8x12', '10x20']
def diff(rule, base, rnd, ss):
    v = []
    for s in ss:
        insts = sorted({i for (z, i, r) in D if z == s and r == base})
        for i in insts:
            if (s, i, rule) not in D:
                return None
            v.append(D[(s, i, rule)][rnd] - D[(s, i, base)][rnd])
    v = np.array(v)
    m = v.mean(); se = v.std(ddof=1) / np.sqrt(len(v))
    t = stats.t.ppf(0.975, len(v) - 1)
    p = stats.ttest_1samp(v, 0).pvalue if se > 0 else 1.0
    return f"{m:+.4f} [{m - t*se:+.4f}, {m + t*se:+.4f}] p {p:.2g} n {len(v)}"
print("orbit - orbit_core:", {r: diff('orbit', 'orbit_core', r, sizes) for r in (1, 3, 10, 20)})
for rule in ['first_orbit', 'maj2', 'rnd0.33', 'o2s', 'o3s', 'o5s', 's1o', 's3o', 's5o', 'orbit']:
    for blk in [[s] for s in sizes] + [['4x4', '6x8'], ['6x8', '10x20'], sizes]:
        res = {r: diff(rule, 'scip', r, blk) for r in (1, 3, 10, 20)}
        if res[10] is None:
            continue
        print(rule, '+'.join(blk), ' | '.join(f"r{r} {res[r]}" for r in res))
for blk in [[s] for s in sizes] + [sizes]:
    print('maj2 - rnd0.33', '+'.join(blk), {r: diff('maj2', 'rnd0.33', r, blk) for r in (3, 10, 20)})
print('first_orbit - orbit all', {r: diff('first_orbit', 'orbit', r, sizes) for r in (3, 10, 20)})
