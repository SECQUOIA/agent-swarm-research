"""Search rational tangent-edge bilinear corners (side '+', w = 1, z_K = 1 at t0 in the
relative interior of edge [v1, v2]) where both families (A) and (B) are excluded by the
kappa-analysis, maximizing the gap 1 - z_A (LMI bisection).  Writes JSON lines."""
import sys, json, numpy as np, warnings; warnings.filterwarnings('ignore')
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
from bilinear import kappa_pencil, kappa_set_A, kappa_ok_B
seed = int(sys.argv[1]); ntr = int(sys.argv[2])
rng = np.random.default_rng(seed)
Q, b, c = bilinear_quadratic('+')
kg = np.unique(np.concatenate([-np.logspace(6, -6, 600), [0.0], np.logspace(-6, 6, 600)]))
best = 1.0
for trial in range(ntr):
    x0, y0 = rng.integers(-3, 4, 2)
    dx = int(rng.integers(1, 5)); dy = -int(rng.integers(1, 5))
    t0 = np.array([x0, y0, x0 * y0], float)
    d = np.array([dx, dy, y0 * dx + x0 * dy], float)
    a, bb = rng.integers(1, 4, 2) / rng.integers(1, 3, 2)
    v1 = t0 + a * d; v2 = t0 - bb * d
    sbar = t0 + np.array(rng.integers(-8, 9, 3), float) / 2
    v3 = t0 + np.array(rng.integers(-12, 13, 3), float) / 2
    if qval(Q, b, c, sbar) <= 0: continue
    P = np.stack([v1 - sbar, v2 - sbar, v3 - sbar], 1)
    if abs(np.linalg.det(P)) < 1e-9: continue
    zk, lam = corner_bound(Q, b, c, sbar, P, np.ones(3), return_point=True)
    if not (abs(zk - 1) < 1e-10 and lam[2] < 1e-12 and lam[0] > 1e-6 and lam[1] > 1e-6): continue
    G0, G1 = kappa_pencil('+', t0, d)
    ivs = [kappa_set_A(G0, G1, '+', v) for v in (sbar, v1, v2, v3)]
    if any(iv is None for iv in ivs): feasA = False
    else: feasA = max(iv[0] for iv in ivs) <= min(iv[1] for iv in ivs) + 1e-12
    if feasA: continue
    if any(all(kappa_ok_B(G0, G1, '+', v, k) for v in (sbar, v1, v2, v3)) for k in kg): continue
    cert, hi, F = best_orbit_bound('+', sbar, P, np.ones(3), 1.0, iters=30)
    rec = dict(trial=trial, gapA=1 - hi, sbar=sbar.tolist(), v1=v1.tolist(), v2=v2.tolist(), v3=v3.tolist(), t0=t0.tolist(), d=d.tolist(), a=float(a), b=float(bb))
    print(json.dumps(rec), flush=True)
