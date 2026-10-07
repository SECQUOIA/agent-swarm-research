"""Random exploration of SCIP's rule (Case-4 set) vs the parabolic-cylinder bound rho_par
(a lower bound on the best orbit ratio) on random bilinear corners with N = 3 rays, costs 1.
usage: python3 scip_random.py SEED NSAMPLES MODE
MODE: 'origin' (sbar = O(1)), 'far' (|xbar|,|ybar| log-uniform up to 1e3), 'antidiag'
(sbar = (R, -R, w) with w near 1), 'axis' (sbar = (R, 0, q)).
Prints one JSON line per sample with z_K finite: D, cond(P~), grazing margin, SCIP ratios
(A: uncompleted cone, B: Case-4 set) and rho_par."""
import sys
import json
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
seed, n, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = np.random.default_rng(seed)
for k in range(n):
    if mode == 'origin':
        xb, yb = rng.normal(size=2)
        qb = np.exp(rng.normal() * 1.5)
    elif mode == 'far':
        xb, yb = rng.choice([-1, 1], 2) * np.exp(rng.uniform(0, 7, 2))
        qb = np.exp(rng.uniform(-3, 9))
    elif mode == 'antidiag':
        R = np.exp(rng.uniform(0, 7))
        xb, yb = R, -R
        qb = (1 + R * R) * np.exp(rng.normal() * 0.3)
    else:  # axis
        R = np.exp(rng.uniform(0, 7))
        xb, yb = R * rng.choice([-1, 1]), 0.0
        qb = np.exp(rng.uniform(-3, 5))
    sbar = np.array([xb, yb, xb * yb + qb])
    # rays: random directions, lengths scaled to the vertex depth sqrt(qbar)
    P = rng.normal(size=(3, 3))
    P[2] *= np.exp(rng.normal() * 2)          # random relative weight of the w-row
    P *= np.sqrt(qb)
    z, lam = rb.zK(sbar, P, np.ones(3))
    if not np.isfinite(z):
        continue
    Pt = P * z
    qv = rb.q(sbar)
    disc = []
    for j in range(3):
        p = Pt[:, j]
        A_, B_ = -p[0] * p[1], rb.grad(sbar) @ p
        disc.append((B_ * B_ - 4 * A_ * qv) / (B_ * B_ + abs(4 * A_ * qv)))
    try:
        sB = rb.scip_ratio(sbar, Pt, 'B')
        sA = rb.scip_ratio(sbar, Pt, 'A')
    except Exception:
        continue
    rp = rb.rho_par(sbar, Pt, ngrid=801)[0]
    print(json.dumps(dict(sbar=sbar.tolist(), D=rb.D_inv(sbar, Pt), cond=float(np.linalg.cond(Pt)),
                          mu=float(min(abs(d) for d in disc)), scipA=sA, scipB=sB, rho_par=rp,
                          supp=int((lam > 1e-12).sum()))), flush=True)
