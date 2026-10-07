"""Validate corner_bound (support enumeration, closed forms) against SCIP global solves
on random bilinear and general k = 2, 3 instances."""
import sys, numpy as np
import core
from core import corner_bound, bilinear_quadratic, qval
from scout_sfree import corner_bound_scip
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
T = int(sys.argv[2]) if len(sys.argv) > 2 else 60
worst = 0; nmis = 0; cnt = 0
for t in range(T):
    kind = t % 3
    if kind == 0:
        side = '+' if rng.random() < .5 else '-'; Q, b, c = bilinear_quadratic(side); k = 3
    else:
        k = 2 if kind == 1 else 3
        A = rng.normal(size=(k, k)); Q = (A + A.T) / 2; b = rng.normal(size=k); c = float(rng.normal())
        ev = np.linalg.eigvalsh(Q)
        if ev.min() > 0 or ev.max() < 0: continue
    while True:
        sbar = rng.normal(size=k)
        if qval(Q, b, c, sbar) > 0.05: break
    N = int(rng.integers(k, 7))
    P = rng.normal(size=(k, N)); w = rng.uniform(0.1, 1.0, N)
    z1 = corner_bound(Q, b, c, sbar, P, w)
    z2 = corner_bound_scip(Q, b, c, sbar, P, w, timelimit=60)
    cnt += 1
    if np.isfinite(z1) and np.isfinite(z2):
        rel = abs(z1 - z2) / max(1e-9, abs(z2))
        worst = max(worst, rel)
        if rel > 1e-5:
            nmis += 1; print('MISMATCH kind', kind, z1, z2, flush=True)
    elif np.isfinite(z1) != np.isfinite(z2) and not (z2 > 1e3):
        nmis += 1; print('MISMATCH inf', kind, z1, z2, flush=True)
print('instances', cnt, 'mismatches', nmis, 'max rel diff', worst, 'two_ray grid-net activations', core.TWO_RAY_WARN[0])
