"""Search for counterexamples to (the withdrawn) Conjecture 16 with rational data.

Side '+', S = {w <= xy}, w = (1,1,1), z_K = 1.  Construction (after the reviewer's idea):
  t* = (x0, y0, x0 y0) = v1 (first contact of ray 1), a nearly tangent edge
  v2 = t* + d + eps*g with grad q(t*).d = 0, -dx dy > 0 and grad q(t*).g > 0 (transversal),
  v3 = t* + r with grad q(t*).r > 0,  sbar = t* - p with grad q(t*).(sbar - t*) > 0, q(sbar) > 0.
Accept if the (numerical) corner minimizer is unique with support {1}; report z_A (LMI bisection).
Usage: python3 search_supp1_cex.py SEED NTRIALS"""
import sys, json, numpy as np, warnings
warnings.filterwarnings('ignore')
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
Q, b, c = bilinear_quadratic('+')
seed, T = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)
for trial in range(T):
    x0, y0 = rng.integers(-3, 4, 2)
    t = np.array([x0, y0, x0 * y0], float); gq = np.array([-y0, -x0, 1.0])
    dx = int(rng.integers(1, 4)); dy = -int(rng.integers(1, 4))
    d = np.array([dx, dy, y0 * dx + x0 * dy], float) * rng.integers(1, 4)
    eps = rng.choice([1, 2, 4]) / 100.0
    v2 = t + d + eps * np.linalg.norm(d) * gq / (gq @ gq) * np.linalg.norm(gq)
    v2 = np.round(v2 * 100) / 100                     # rational (hundredths)
    r = rng.integers(-6, 7, 3) / 2.0
    p = rng.integers(-6, 7, 3) / 2.0
    v3 = t + r; sbar = t - p
    if gq @ (v2 - t) <= 0 or gq @ r <= 0.05 * np.linalg.norm(gq) * np.linalg.norm(r):
        continue
    if gq @ (sbar - t) <= 0.05 * np.linalg.norm(gq) * np.linalg.norm(p) or qval(Q, b, c, sbar) <= 0.05:
        continue
    P = np.stack([t - sbar, v2 - sbar, v3 - sbar], 1)
    if abs(np.linalg.det(P)) < 1e-6:
        continue
    zk, lam = corner_bound(Q, b, c, sbar, P, np.ones(3), return_point=True)
    if not (abs(zk - 1) < 1e-12 and abs(lam[0] - 1) < 1e-12):
        continue
    z23 = corner_bound(Q, b, c, sbar, P[:, 1:], np.ones(2))
    z13 = corner_bound(Q, b, c, sbar, P[:, [0, 2]], np.ones(2))
    z12 = corner_bound(Q, b, c, sbar, P[:, [0, 1]], np.ones(2))
    if z23 < 1 + 1e-4:
        continue
    cert, hi, F = best_orbit_bound('+', sbar, P, np.ones(3), 1.0, iters=30)
    if hi < 0.9995:
        print(json.dumps(dict(trial=trial, zA_hi=hi, zA_cert=cert, sbar=sbar.tolist(), v1=t.tolist(), v2=v2.tolist(),
                              v3=v3.tolist(), eps=float(eps), cos_edge=float(gq @ (v2 - t) / np.linalg.norm(gq) / np.linalg.norm(v2 - t)))),
              flush=True)
