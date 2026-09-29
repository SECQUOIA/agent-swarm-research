"""Adversarial test of Conjecture 16: minimize z_A / z_K over bilinear corners (S = {w <= xy},
N = 3, w = 1) whose unique minimizer is the first contact of ray 1 at a vertex t0 = v1,
with transversal contact (|grad q(t0).p1| >= MARGIN |grad q(t0)| |p1|) and no ray
within MARGIN of grazing.  Usage: SEED RESTARTS MARGIN"""
import sys, json, numpy as np, warnings; warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
Q, b, c = bilinear_quadratic('+')
MARGIN = 1e-2


def build(th):
    x0, y0 = th[:2]; t0 = np.array([x0, y0, x0 * y0])
    sbar = t0 + th[2:5]; v2 = t0 + th[5:8]; v3 = t0 + th[8:11]
    return sbar, np.stack([t0 - sbar, v2 - sbar, v3 - sbar], 1), t0


def ratio(th, iters=22):
    sbar, P, t0 = build(th)
    g0 = qval(Q, b, c, sbar)
    if g0 <= 1e-6 or abs(np.linalg.det(P)) < 1e-8 * (1 + np.abs(P).max() ** 3):
        return 2.0
    gr = 2 * Q @ t0 + b
    if gr @ P[:, 0] > -MARGIN * np.linalg.norm(gr) * np.linalg.norm(P[:, 0]):
        return 2.0
    for j in range(3):
        p = P[:, j]; A_ = p @ Q @ p; B_ = 2 * p @ (Q @ sbar + b / 2)
        if abs(B_ * B_ - 4 * A_ * g0) <= MARGIN * (B_ * B_ + abs(4 * A_ * g0)):
            return 2.0
    zk, lam = corner_bound(Q, b, c, sbar, P, np.ones(3), return_point=True)
    if not (abs(zk - 1) < 1e-8 and lam[0] > 1 - 1e-8 and lam[1] < 1e-12 and lam[2] < 1e-12):
        return 2.0
    # unique minimizer: all other supports strictly worse
    z23 = corner_bound(Q, b, c, sbar, P[:, 1:], np.ones(2))
    if z23 < 1 + 1e-6:
        return 2.0
    cert, hi, F = best_orbit_bound('+', sbar, P, np.ones(3), 1.0, iters=iters)
    return hi


if __name__ == '__main__':
    seed = int(sys.argv[1]); restarts = int(sys.argv[2]); MARGIN = float(sys.argv[3])
    rng = np.random.default_rng(seed)
    for rs in range(restarts):
        for _ in range(3000):
            th = np.concatenate([rng.normal(size=2) * 2, rng.normal(size=9) * 3])
            f0 = ratio(th, iters=14)
            if f0 <= 1.0:
                break
        else:
            continue
        res = minimize(ratio, th, method='Nelder-Mead', options=dict(maxiter=400, xatol=1e-6, fatol=1e-7))
        print(json.dumps(dict(restart=rs, start=f0, final=ratio(res.x, iters=40), theta=res.x.tolist())), flush=True)
