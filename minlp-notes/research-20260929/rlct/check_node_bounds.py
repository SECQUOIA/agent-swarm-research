"""Check the batched node bounds of bisect_bb.py against SciPy L-BFGS-B.

For random boxes (sides 2^-k of the root side, placed near and away from the
zero set), compare the certified lower bound and the upper bound returned by
the batched solver with the best of 5 L-BFGS-B runs on the same convex
problem.  Reports the largest violations.
"""
import numpy as np
from scipy.optimize import minimize

import instances


def batched(fun, l, u, alpha, L, iters=400):
    x = 0.5 * (l + u)
    y = x.copy()
    t = np.ones(l.shape[0])
    fprev = np.full(l.shape[0], np.inf)
    for _ in range(iters):
        _, g = fun(y)
        g = g + alpha * (2 * y - l - u)
        xn = np.clip(y - g / L, l, u)
        v, _ = fun(xn)
        fv = v - alpha * np.sum((xn - l) * (u - xn), axis=1)
        rs = fv > fprev
        tn = 0.5 * (1 + np.sqrt(1 + 4 * t * t))
        y = np.where(rs[:, None], xn, xn + ((t - 1) / tn)[:, None] * (xn - x))
        t = np.where(rs, 1.0, tn)
        x = xn
        fprev = fv
    v, g = fun(x)
    g = g + alpha * (2 * x - l - u)
    fv = v - alpha * np.sum((x - l) * (u - x), axis=1)
    lb = fv + np.sum(np.minimum(g * (l - x), g * (u - x)), axis=1)
    return lb, fv


def scipy_min(fun, l, u, alpha, rng):
    def obj(z):
        v, g = fun(z[None, :])
        q = np.sum((z - l) * (u - z))
        return v[0] - alpha * q, g[0] + alpha * (2 * z - l - u)
    best = np.inf
    for k in range(5):
        z0 = l + rng.random(l.size) * (u - l) if k else 0.5 * (l + u)
        r = minimize(obj, z0, jac=True, method="L-BFGS-B",
                     bounds=list(zip(l, u)), options=dict(ftol=1e-15, gtol=1e-12))
        best = min(best, r.fun)
    return best


def main():
    rng = np.random.default_rng(0)
    for name in ["xy2", "sep24", "cusp", "xy2z4", "bdry", "rrr1e-2"]:
        d = instances.get(name)
        fun, n, lo, s0, alpha = d["fun"], d["n"], d["lo"], d["side"], d["alpha"]
        L = d["hmax"] + 2 * alpha
        ls, us = [], []
        for _ in range(150):
            k = rng.integers(1, 12)
            s = s0 * 2.0 ** (-k)
            # half of the boxes near the origin (where the zero sets cross)
            if rng.random() < 0.5:
                c = np.clip(rng.normal(0, 3 * s, n), lo, lo + s0 - s)
            else:
                c = lo + rng.random(n) * (s0 - s)
            ls.append(c)
            us.append(c + s)
        l, u = np.array(ls), np.array(us)
        lb, ub = batched(fun, l, u, alpha, L)
        ref = np.array([scipy_min(fun, l[i], u[i], alpha, rng) for i in range(len(l))])
        scale = np.maximum(1e-12, np.abs(ref))
        print(f"{name:8s} boxes={len(l)}  max(lb-ref)={np.max(lb - ref):.2e}  "
              f"max(ref-ub)={np.max(ref - ub):.2e}  max rel gap (ub-lb)/|ref|="
              f"{np.max((ub - lb) / scale):.2e}")


if __name__ == "__main__":
    main()
