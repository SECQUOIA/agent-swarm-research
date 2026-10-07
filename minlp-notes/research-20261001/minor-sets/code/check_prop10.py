"""Numerical illustration of Proposition 10 on the random corners of exp_random.py (N = 4).
For support-one corners (minimizer on ray j alone) report the angle between xhat(p_j) and
xhat(sbar), xhat(M) = ((a + d)/2, (c - b)/2), for the corners where SCIP's set attains z_K
within 1e-5 and, for comparison, the distribution over all support-one corners.
Usage: python3 check_prop10.py LOG.jsonl [LOG2.jsonl ...]
"""
import sys
import json
import numpy as np
from minor_core import det4

xhat = lambda s: np.array([(s[0] + s[3]) / 2, (s[2] - s[1]) / 2])
ang_att, ang_all, ratio_all = [], [], []
for path in sys.argv[1:]:
    recs = {r['idx']: r for r in map(json.loads, open(path)) if r.get('zK') is not None}
    seed = next(iter(recs.values()))['seed']
    N = next(iter(recs.values()))['N']
    rng = np.random.default_rng(seed)
    tries = 0
    maxidx = max(recs)
    while tries < maxidx:
        tries += 1
        s = rng.normal(size=4)
        if det4(s) <= 0:
            continue
        P = rng.normal(size=(4, N))
        rng.uniform(0.2, 2.0, N)
        r = recs.get(tries)
        if r is None or len(r['support']) != 1:
            continue
        j = r['support'][0]
        a, b = xhat(P[:, j]), xhat(s)
        ang = np.degrees(np.arccos(abs(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))))
        ang_all.append(ang)
        ratio_all.append(r['ratios']['scip'])
        if r['ratios']['scip'] >= 1 - 1e-5:
            ang_att.append(ang)
ang_all, ratio_all = np.array(ang_all), np.array(ratio_all)
print('support-one corners: %d; SCIP attains (1e-5) in %d; their angles (deg): %s' % (
    len(ang_all), len(ang_att), [round(float(x), 3) for x in sorted(ang_att)]))
print('angle quantiles over all support-one corners (deg): 1%%: %.2f  10%%: %.2f  50%%: %.2f' % tuple(
    np.quantile(ang_all, [0.01, 0.1, 0.5])))
for lo, hi in ((0, 1), (1, 5), (5, 20), (20, 90)):
    m = (ang_all >= lo) & (ang_all < hi)
    if m.any():
        print('angle in [%2d, %2d) deg: n = %3d, mean SCIP ratio %.4f' % (lo, hi, m.sum(), ratio_all[m].mean()))
