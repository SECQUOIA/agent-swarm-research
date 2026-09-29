"""Adversarial search (usage: SEED RESTARTS [MARGIN]): minimize z_A / z_K (sliced orbit family) over tangent-edge bilinear
corners parametrized as t0 = (x0, y0, x0 y0), d = (1, -e^g, y0 - x0 e^g) (tangent, dx dy < 0),
v1 = t0 + e^a d, v2 = t0 - e^b d, sbar = t0 + s, v3 = t0 + r;  w = (1,1,1).
Valid iff z_K = 1 with minimizer support {v1, v2} (checked exactly by corner_bound).
Also records the (B) bound of the final (A)-optimal F (a lower bound for z_B)."""
import sys, json, numpy as np, warnings; warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
MARGIN = 0.0
Q, b, c = bilinear_quadratic('+')


def build(th):
    x0, y0, g, a, bb = th[:5]; s = th[5:8]; r = th[8:11]
    t0 = np.array([x0, y0, x0 * y0]); e = np.exp(g)
    d = np.array([1.0, -e, y0 - x0 * e])
    v1 = t0 + np.exp(a) * d; v2 = t0 - np.exp(bb) * d; sbar = t0 + s; v3 = t0 + r
    return sbar, np.stack([v1 - sbar, v2 - sbar, v3 - sbar], 1)


def ratio(th, iters=22):
    sbar, P = build(th)
    if qval(Q, b, c, sbar) <= 1e-6 or abs(np.linalg.det(P)) < 1e-8 * (1 + np.abs(P).max() ** 3):
        return 2.0
    g0 = qval(Q, b, c, sbar)
    for j in range(3):          # non-degeneracy: no ray within MARGIN of grazing dS
        p = P[:, j]; A_ = p @ Q @ p; B_ = 2 * p @ (Q @ sbar + b / 2)
        if abs(B_ * B_ - 4 * A_ * g0) <= MARGIN * (B_ * B_ + abs(4 * A_ * g0)):
            return 2.0
    zk, lam = corner_bound(Q, b, c, sbar, P, np.ones(3), return_point=True)
    if not (abs(zk - 1) < 1e-8 and lam[2] < 1e-10 and min(lam[0], lam[1]) > 1e-6):
        return 2.0
    cert, hi, F = best_orbit_bound('+', sbar, P, np.ones(3), 1.0, iters=iters)
    return hi


if __name__ == '__main__':
    seed = int(sys.argv[1]); restarts = int(sys.argv[2])
    MARGIN = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    rng = np.random.default_rng(seed)
    best = (2.0, None)
    for rs in range(restarts):
        for _ in range(2000):
            th = np.concatenate([rng.normal(size=2) * 2, rng.normal(size=3), rng.normal(size=6) * 3])
            f0 = ratio(th, iters=14)
            if f0 < 1.0 - 1e-6:
                break
        else:
            continue
        res = minimize(ratio, th, method='Nelder-Mead', options=dict(maxiter=400, xatol=1e-6, fatol=1e-7))
        val = ratio(res.x, iters=40)
        print(json.dumps(dict(restart=rs, start=f0, final=val, theta=res.x.tolist())), flush=True)
        if val < best[0]:
            best = (val, res.x)
    print('BEST', best[0], json.dumps(best[1].tolist() if best[1] is not None else None))
