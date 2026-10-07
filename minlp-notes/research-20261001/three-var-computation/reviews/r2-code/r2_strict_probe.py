"""Reviewer r2: independent five-tetrahedron lift depths (cvxpy + Clarabel, tol 1e-11) at the
strict spar090-075-1 point for (a) the 40 triples whose stored depth most exceeds the exact
triangle/cap upper bound, (b) the 40 triples with the most negative exact bound, (c) the 40
most negative stored depths. Diagnostic of one-sided depth accuracy, not a full re-audit.
Run from three-var-computation/: python reviews/r2-code/r2_strict_probe.py
"""
import importlib.util
import itertools
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('probe', os.path.join(HERE, 'r2_lift_probe_core.py'))
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

z = np.load(os.path.join(ROOT, 'logs/strict_r1/spar090-075-1.base.npz'))
d = np.load(os.path.join(ROOT, 'logs/strict_r1/spar090-075-1.depth.npz'))['depths']
x, Y = z['x'], z['Y']
T = np.array(list(itertools.combinations(range(len(x)), 3)))
i, j, k = T.T
tv = np.stack([Y[i, j] + Y[i, k] - x[i] - Y[j, k], Y[i, j] + Y[j, k] - x[j] - Y[i, k],
               Y[i, k] + Y[j, k] - x[k] - Y[i, j], x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1], 1).max(1)
cap = np.diag(Y) - x
capT = np.maximum(np.maximum(cap[i], cap[j]), cap[k])
bound = np.minimum(-4 * np.maximum(tv, 0), -6 * np.maximum(capT, 0))
groups = dict(excess=np.argsort(-(d - bound))[:40], bound=np.argsort(bound)[:40], stored=np.argsort(d)[:40])
Mfull = np.block([[np.ones((1, 1)), x[None, :]], [x[:, None], Y]])
allmin = []
for gname, idx in groups.items():
    res = []
    for t in idx:
        sel = [0] + [a + 1 for a in T[t]]
        dd, st = core.depth(Mfull[np.ix_(sel, sel)])
        res.append(dict(T=T[t].tolist(), stored=float(d[t]), bound=float(bound[t]), lift=dd, status=st))
    allmin += res
    w = min(res, key=lambda r: r['lift'])
    print(json.dumps(dict(group=gname, n=len(res), min_lift=w['lift'], at=w,
                          max_stored_minus_lift=max(r['stored'] - r['lift'] for r in res),
                          max_lift_minus_bound=max(r['lift'] - r['bound'] for r in res),
                          statuses=sorted(set(r['status'] for r in res)))))
w = min(allmin, key=lambda r: r['lift'])
print('most negative lift depth among probed triples:', json.dumps(w))
