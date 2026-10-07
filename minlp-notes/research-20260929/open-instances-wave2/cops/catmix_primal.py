"""Primal points for catmix100/200/400/800.

1. float chord DP on a theta grid (non-rigorous; only used to find a policy),
2. forward extraction of the DP policy, L-BFGS-B refinement (reduced problem in u),
3. evaluation: (a) interval enclosure (mpmath iv, 60 digits) of the objective of the
   exactly feasible point defined by the float controls (states solved exactly from
   the rows), (b) 50-digit evaluation of the OSIL rows at the double-rounded full vector.
"""
import json
import sys
import time
from fractions import Fraction

import mpmath as mp
import numpy as np
from mpmath import iv
from scipy.optimize import minimize

import catmix_model as cmx
import osilx


def float_dp_policy(N, K, dtheta=1e-5):
    fm = cmx.FloatModel(K, N)
    a, b, c, ep, em = fm.a, fm.b, fm.c, fm.ep, fm.em

    def Mapply(uu, y1, y2):
        P11 = 1 + a * uu; P12 = -b * uu; P21 = -a * uu; P22 = ep + c * uu
        det = P11 * P22 - P12 * P21
        x1 = (P22 * y1 - P12 * y2) / det; x2 = (P11 * y2 - P21 * y1) / det
        return (1 - a * uu) * x1 + b * uu * x2, a * uu * x1 + (em - c * uu) * x2

    def Pinv_sum(uu, y1, y2):
        P11 = 1 + a * uu; P12 = -b * uu; P21 = -a * uu; P22 = ep + c * uu
        det = P11 * P22 - P12 * P21
        return ((P22 * y1 - P12 * y2) + (P11 * y2 - P21 * y1)) / det

    def vargmin(f, shape):
        us = np.linspace(0, 1, 201)
        vals = np.stack([f(np.full(shape, uu)) for uu in us])
        k = np.argmin(vals, axis=0); best = vals.min(axis=0); ub = us[k]
        lo = np.clip(us[k] - 1 / 200, 0, 1); hi = np.clip(us[k] + 1 / 200, 0, 1)
        gr = (np.sqrt(5) - 1) / 2
        x1 = hi - gr * (hi - lo); x2 = lo + gr * (hi - lo); f1 = f(x1); f2 = f(x2)
        for _ in range(45):
            m_ = f1 < f2
            hi = np.where(m_, x2, hi); lo = np.where(m_, lo, x1)
            x2n = np.where(m_, x1, lo + gr * (hi - lo)); x1n = np.where(m_, hi - gr * (hi - lo), x2)
            x1, x2 = x1n, x2n; f1 = f(x1); f2 = f(x2)
        fb = np.minimum(f1, f2); xb = np.where(f1 < f2, x1, x2)
        return np.where(fb < best, fb, best), np.where(fb < best, xb, ub)

    th = np.concatenate([np.arange(0, 0.1, dtheta), np.linspace(0.1, 1, 91)])
    y1, y2 = 1 - th, th
    W = [None] * N
    w, _ = vargmin(lambda uu: Pinv_sum(uu, y1, y2), th.shape)
    W[N - 1] = w
    for i in range(N - 1, 0, -1):
        def f(uu, w=w):
            z1, z2 = Mapply(uu, y1, y2); s = z1 + z2
            return s * np.interp(z2 / s, th, w)
        w, _ = vargmin(f, th.shape)
        W[i - 1] = w

    def f0(uu):
        z1 = 1 - a * uu; z2 = a * uu; s = z1 + z2
        return s * np.interp(z2 / s, th, W[0])
    v0, u0 = vargmin(f0, ())
    us = [float(u0)]
    y = np.array([1 - a * u0, a * u0])
    for i in range(1, N):
        Wi = W[i]

        def fi(uu):
            z1, z2 = Mapply(uu, y[0], y[1]); s = z1 + z2
            return s * np.interp(z2 / s, th, Wi)
        _, ui = vargmin(fi, ())
        us.append(float(ui))
        y = np.array(Mapply(ui, y[0], y[1]))
    _, uN = vargmin(lambda uu: Pinv_sum(uu, y[0], y[1]), ())
    us.append(float(uN))
    return np.array(us), float(v0) - 1


def refine(N, K, u):
    fm = cmx.FloatModel(K, N)
    u = np.clip(u, 0, 1)
    u[np.abs(u - 1) < 1e-6] = 1
    u[u < 1e-6] = 0
    sc = 1e4
    res = minimize(lambda v: (lambda r: (r[0] * sc, r[1] * sc))(fm.J_grad(v)[:2]), u, jac=True,
                   method="L-BFGS-B", bounds=[(0, 1)] * (N + 1),
                   options=dict(maxiter=100000, ftol=1e-20, gtol=1e-16, maxcor=100))
    u = np.clip(res.x, 0, 1)
    J, g, x = fm.J_grad(u)
    free = (u > 1e-12) & (u < 1 - 1e-12)
    kkt = dict(n_free=int(free.sum()), max_abs_grad_free=float(np.abs(g[free]).max()) if free.any() else 0.0,
               min_grad_at_0=float(g[u <= 1e-12].min()) if (u <= 1e-12).any() else None,
               max_grad_at_1=float(g[u >= 1 - 1e-12].max()) if (u >= 1 - 1e-12).any() else None)
    return u, float(J), kkt


def exact_objective_enclosure(K, u, dps=60):
    """interval enclosure of x1_N + x2_N - 1 for the exactly feasible point with controls u."""
    iv.dps = dps
    a, b, c, ep, em = (iv.mpf(K[k]) for k in ("a", "b", "c", "ep", "em"))
    x1, x2 = iv.mpf(1), iv.mpf(0)
    for i in range(len(u) - 1):
        ui, un = iv.mpf(float(u[i])), iv.mpf(float(u[i + 1]))
        q1 = (1 - a * ui) * x1 + b * ui * x2
        q2 = a * ui * x1 + (em - c * ui) * x2
        P11, P12, P21, P22 = 1 + a * un, -b * un, -a * un, ep + c * un
        det = P11 * P22 - P12 * P21
        x1, x2 = (P22 * q1 - P12 * q2) / det, (P11 * q2 - P21 * q1) / det
    J = x1 + x2 - 1
    return J


def double_vector_check(N, m, K, u):
    """states in 50 digits from the controls, rounded to double; OSIL rows evaluated in 50 digits."""
    mp.mp.dps = 50
    x = cmx.simulate(K, [mp.mpf(float(v)) for v in u], num=mp.mpf)
    X = [float(v) for v in u] + [float(s[0]) for s in x] + [float(s[1]) for s in x]
    X[N + 1] = 1.0
    X[2 * N + 2] = 0.0
    Xm = [mp.mpf(v) for v in X]
    viol = max(abs(osilx.ev_row(r, Xm, mp.mpf, {})) for r in m["cons"])
    obj = osilx.ev_row(dict(constant=m["obj"]["constant"], lin=m["obj"]["lin"], quad=[], nl=None), Xm, mp.mpf, {})
    bnd = max(max(0.0, -X[j]) + max(0.0, X[j] - 1) for j in range(N + 1))
    return X, mp.nstr(obj, 20), mp.nstr(viol, 3), bnd


def main(N):
    t0 = time.time()
    m, K = cmx.extract(N)
    upol, dpval = float_dp_policy(N, K)
    fm = cmx.FloatModel(K, N)
    Jpol = fm.J_grad(upol)[0]
    u, J, kkt = refine(N, K, upol)
    Jiv = exact_objective_enclosure(K, u)
    X, obj_d, viol_d, bviol = double_vector_check(N, m, K, u)
    out = dict(N=N, float_dp_value=dpval, policy_J=Jpol, refined_J_float=J, kkt=kkt,
               exact_point_objective_enclosure=[mp.nstr(Jiv.a, 20), mp.nstr(Jiv.b, 20)],
               double_vector_objective=obj_d, double_vector_max_row_violation=viol_d,
               double_vector_bound_violation=bviol, seconds=time.time() - t0)
    np.save("logs/catmix%d_u.npy" % N, u)
    with open("logs/catmix%d_primal.json" % N, "w") as f:
        json.dump(out, f, indent=1)
    with open("logs/catmix%d_primal.txt" % N, "w") as f:
        f.write("\n".join(repr(v) for v in X) + "\n")
    print(json.dumps(out, indent=1), flush=True)


if __name__ == "__main__":
    for N in [int(v) for v in sys.argv[1:]]:
        main(N)
