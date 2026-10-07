"""Float sanity check of the lukvle10 certificate (not a proof): every pair problem and the
tail block are sampled on a dense grid over its box and locally minimized from the best grid
points; the sampled minimum must not fall below the certified lower bound."""
import json
import numpy as np
from scipy.optimize import minimize
import lukvle10_bound as L
from lukvle10_lagr import kkt_multipliers, load_sol

def fl(fr): return float(fr)

x = load_sol("minlplib_sol/lukvle10.p5.sol"); lam, _ = kkt_multipliers(x); lam = L.clean_multipliers(lam)
K = 3; m = 1000 - 2 * K
beta, q, _ = L.coeffs_exact(lam, m)
cert = json.load(open("logs/lukvle10_bound_K3.json"))["groups"]

def f(a, b):
    with np.errstate(all="ignore"):
        return (a * a) ** (b * b + 1) + (b * b) ** (a * a + 1)

def make(i, Kp):
    ba, qa, bb, qb = fl(beta[i]), fl(q[i]), fl(beta[i + 1]), fl(q[i + 1])
    def F(a, b):
        v = ba * a + qa * a * a + bb * b + qb * b * b
        x0, x1 = a, b
        for k in range(Kp):
            v = v + f(x0, x1)
            if k < Kp - 1:
                x2 = (1 + 3 * x1 - 2 * x1 * x1 - x0) / 2; x3 = (1 + 3 * x2 - 2 * x2 * x2 - x1) / 2; x0, x1 = x2, x3
        return v
    return F

worst = np.inf; rows = []
for g in cert:
    if g.get("tail"):
        F = make(m, K)
    else:
        F = make(2 * g["first_pair"], 1)
    Ra, Rb = g["R"]
    A, B = np.meshgrid(np.linspace(-Ra, Ra, 1501), np.linspace(-Rb, Rb, 1501), indexing="ij")
    V = F(A, B); V = np.where(np.isfinite(V), V, np.inf)
    idx = np.argsort(V, axis=None)[:20]
    best = V.flat[idx[0]]
    for k in idx:
        z0 = [A.flat[k], B.flat[k]]
        r = minimize(lambda z: F(z[0], z[1]), z0, method="Nelder-Mead", options=dict(xatol=1e-13, fatol=1e-15, maxiter=5000))
        best = min(best, r.fun)
    rows.append(dict(group=g.get("first_pair", "tail"), sampled_min=float(best), certified_LB=g["LB"], margin=float(best - g["LB"])))
    worst = min(worst, best - g["LB"])
print(json.dumps(dict(min_margin=float(worst), n=len(rows))))
json.dump(rows, open("logs/lukvle10_sanity.json", "w"), indent=1)
