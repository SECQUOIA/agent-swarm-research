"""Reviewer r2: do diagonal-cap residuals explain the bulk depths near -1e-7 at original spar points?

The cap x_i - x_i^2 >= 0 has uniform mean 1/6, so a point with Y_ii - x_i = c > 0 has exact depth
<= -6c on every triple containing i. Compare stored depths with -6 * (largest cap residual in the
triple) and -4 * (triangle residual).
Run from three-var-computation/: python reviews/r2-code/r2_cap_residual.py
"""
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for name in ['spar125-050-1', 'spar100-050-2', 'spar050-050-3', 'spar125-050-3', 'spar100-050-1']:
    p = os.path.join(ROOT, 'logs/spar_audit', name + '.json')
    z = np.load(p + '.base.npz')
    d = np.load(p + '.depth.npz')['depths']
    x, Y = z['x'], z['Y']
    T = np.array(list(itertools.combinations(range(len(x)), 3)))
    i, j, k = T.T
    cap = np.diag(Y) - x
    capT = np.maximum(np.maximum(cap[i], cap[j]), cap[k])
    tv = np.stack([Y[i, j] + Y[i, k] - x[i] - Y[j, k], Y[i, j] + Y[j, k] - x[j] - Y[i, k],
                   Y[i, k] + Y[j, k] - x[k] - Y[i, j], x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1], 1).max(1)
    bound = np.minimum(-6 * np.maximum(capT, 0), -4 * np.maximum(tv, 0))
    has = bound < 0
    feas = tv <= 0
    print(json.dumps(dict(
        name=name, cap_residual_max=float(cap.max()), n_cap_pos=int((cap > 0).sum()), n=len(x),
        n_triples=len(T), n_with_exact_bound=int(has.sum()),
        median_depth=float(np.median(d)), median_minus6cap=float(np.median(-6 * np.maximum(capT, 0))),
        tri_feasible_min_depth=float(d[feas].min()),
        tri_feasible_min_minus6cap=float((-6 * np.maximum(capT, 0))[feas].min()),
        depth_over_bound_quantiles=[float(q) for q in np.quantile(d[has] / bound[has], [0.01, 0.5, 0.99])])))
