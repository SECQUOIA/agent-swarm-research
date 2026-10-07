"""Checks for Lemma S and Theorem S (SCIP's fixed-lambda set for w <= xy).
Lemma S: SCIP's (uncompleted) set is {s : 4 N^2 q(s) >= V(s - sbar)^2, tr(R_theta M(s)) >= 0} with
N^2 = (xbar - ybar)^2 + (wbar + 1)^2 and V(d) = (xbar - ybar) d_w - (wbar + 1)(d_x - d_y); so its step along
a ray p is the first s > 0 with 4 N^2 q(sbar + s p) = s^2 V(p)^2.
Theorem S: z_SCIP/z_K >= min(1/2, 1/(2D), sqrt(q(sbar)) / max_j |(p~_jx - p~_jy, p~_jw)|)
           >= min(1/2, 1/(sqrt 6 kappa D)),  kappa = cond(P~)  (3 rays).
usage: python3 check_scip_bound.py SEED NINST"""
import sys
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
seed, ninst = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)


def scip_step_closed(sbar, p):
    xb, yb, wb = sbar
    N2 = (xb - yb) ** 2 + (wb + 1) ** 2
    V = (xb - yb) * p[2] - (wb + 1) * (p[0] - p[1])
    qb = rb.q(sbar)
    a2 = -(4 * N2 * p[0] * p[1] + V * V)
    a1 = 4 * N2 * (rb.grad(sbar) @ p)
    a0 = 4 * N2 * qb
    roots = np.roots([a2, a1, a0]) if abs(a2) > 1e-300 else np.array([-a0 / a1]) if a1 != 0 else np.array([])
    pos = sorted(r.real for r in np.atleast_1d(roots) if abs(r.imag) < 1e-12 and r.real > 0)
    return pos[0] if pos else np.inf


maxdiff, nviol, n = 0.0, 0, 0
mins = []
while n < ninst:
    mode = n % 3
    if mode == 0:
        xb, yb = rng.normal(size=2)
    elif mode == 1:
        xb, yb = rng.choice([-1, 1], 2) * np.exp(rng.uniform(0, 5, 2))
    else:
        R = np.exp(rng.uniform(0, 5))
        xb, yb = R, -R
    qb = np.exp(rng.uniform(-3, 6))
    sbar = np.array([xb, yb, xb * yb + qb])
    P = rng.normal(size=(3, 3)) * np.sqrt(qb)
    P[2] *= np.exp(rng.normal())
    z, lam = rb.zK(sbar, P, np.ones(3))
    if not np.isfinite(z):
        continue
    n += 1
    Pt = P * z
    sA = rb.scip_ratio(sbar, Pt, 'A')
    sc = min(scip_step_closed(sbar, Pt[:, j]) for j in range(3))
    d = 0.0 if (np.isinf(sA) and np.isinf(sc)) else abs(sA - sc) / max(1.0, min(sA, sc))
    maxdiff = max(maxdiff, d)
    D = rb.D_inv(sbar, Pt)
    kap = np.linalg.cond(Pt)
    rad = max(np.hypot(Pt[0, j] - Pt[1, j], Pt[2, j]) for j in range(3))
    b1 = min(0.5, 1 / (2 * D), np.sqrt(qb) / rad)
    b2 = min(0.5, 1 / (np.sqrt(6) * kap * D))
    ok = b2 <= b1 * (1 + 1e-12) and b1 <= sA * (1 + 1e-9)
    nviol += not ok
    mins.append(sA / b1)
print('instances', n)
print('Lemma S: max rel diff closed-form SCIP step vs PSD-based step: %.2e' % maxdiff)
print('Theorem S: violations', nviol, '; min over instances of z_SCIP_A / bound1 = %.4f' % min(mins))
print('PASS' if (maxdiff < 1e-6 and nviol == 0) else 'FAIL')
