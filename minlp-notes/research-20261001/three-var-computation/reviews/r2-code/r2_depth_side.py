"""Reviewer r2: one-sidedness of the stream's computed hull depths at original spar audit points.

The normalized triangle quadratic is a feasible C in Lemma 2 (<C_tri, M_c> = 1/4), so the exact
depth satisfies delta <= -4 * tv for every triple with triangle violation tv > 0. This script
lists triples where the stored depth is above that exact upper bound, and the depth distribution.
Run from three-var-computation/: python reviews/r2-code/r2_depth_side.py
"""
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for name in ['spar050-050-3', 'spar040-050-2', 'spar050-030-3', 'spar100-075-2', 'spar100-050-2',
             'spar125-050-1', 'spar125-050-3', 'spar090-075-1']:
    p = os.path.join(ROOT, 'logs/spar_audit', name + '.json')
    z = np.load(p + '.base.npz')
    d = np.load(p + '.depth.npz')['depths']
    x, Y = z['x'], z['Y']
    n = len(x)
    T = np.array(list(itertools.combinations(range(n), 3)))
    i, j, k = T.T
    V = np.stack([Y[i, j] + Y[i, k] - x[i] - Y[j, k], Y[i, j] + Y[j, k] - x[j] - Y[i, k],
                  Y[i, k] + Y[j, k] - x[k] - Y[i, j], x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1], 1)
    tv = V.max(1)
    excess = d + 4 * tv            # > 0 means stored depth is above the exact bound -4 tv
    pos = tv > 0
    o = np.argsort(-np.where(pos, excess, -np.inf))[:3]
    print(json.dumps(dict(name=name, n_tv_pos=int(pos.sum()), n_excess_gt_1e8=int((pos & (excess > 1e-8)).sum()),
                          n_excess_gt_1e7=int((pos & (excess > 1e-7)).sum()),
                          worst=[dict(T=T[t].tolist(), tv=float(tv[t]), depth=float(d[t]), excess=float(excess[t]))
                                 for t in o],
                          depth_quantiles=[float(q) for q in np.quantile(d, [0, 0.001, 0.01, 0.5, 0.99])],
                          n_depth_lt_1e7=int((d < -1e-7).sum()), n_depth_lt_1e6=int((d < -1e-6).sum()),
                          x_at_bound=int(((x < 1e-6) | (x > 1 - 1e-6)).sum()),
                          diag_slack_max=float(np.max(np.diag(Y) - x)))))
