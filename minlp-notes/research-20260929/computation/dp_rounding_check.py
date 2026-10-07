"""After review: rounding error of the min-sum DP (section 4.3).

For every iteration of chain_bb (amp 0.2, seed 0, eps 1e-6, mode quad), the
piece bounds are recorded, and the forward DP bound and all min-marginals are
recomputed in float64 and in np.longdouble. Reported: the largest differences
over all iterations, and the first-order recursive-summation error bound for
the forward pass, u * sum_e (max|f_e + P_e| + max|f_{e+1}|) (two roundings per
step; the min is exact), maximized over iterations.

Usage: python3 dp_rounding_check.py 8192
"""
import sys
import numpy as np
import instances as I
import chain_bb as CB

n = int(sys.argv[1])
U = np.finfo(np.float64).eps / 2
iters = []
orig_us = CB.unary_lb_sub


def us(prob, vidx, p, q, Qt, Lt, sub):
    out = orig_us(prob, vidx, p, q, Qt, Lt, sub)
    iters.append({"K": np.bincount(vidx, minlength=prob.n), "u": out.copy(), "P": []})
    return out


class Rec(I.Probe3Chain):
    def pair_lb(self, *a):
        out = super().pair_lb(*a)
        iters[-1]["P"].append(out.copy())
        return out


CB.unary_lb_sub = us
r = CB.chain_bb(Rec(I.coeffs(n, 0, 0.2)), 1e-6, mode="quad", unary_sub=16)


def dp(K, uflat, pflat, dtype):
    uo = np.concatenate([[0], np.cumsum(K)]); po = np.concatenate([[0], np.cumsum(K[:-1] * K[1:])])
    u = [uflat[uo[i]:uo[i + 1]].astype(dtype) for i in range(n)]
    P = [pflat[po[e]:po[e + 1]].reshape(K[e], K[e + 1]).astype(dtype) for e in range(n - 1)]
    f = [u[0]]; bound = 0.0
    for e in range(n - 1):
        s = f[e][:, None] + P[e]
        f.append(s.min(axis=0) + u[e + 1])
        bound += U * (float(np.abs(s).max()) + float(np.abs(f[-1]).max()))
    g = [None] * n; g[n - 1] = np.zeros(K[n - 1], dtype)
    for e in range(n - 2, -1, -1):
        g[e] = (P[e] + (u[e + 1] + g[e + 1])[None, :]).min(axis=1)
    return f[-1].min(), np.concatenate([f[i] + g[i] for i in range(n)]), bound


wlb = wm = wb = 0.0
for it in iters:
    pflat = np.concatenate(it["P"])
    lb64, m64, bnd = dp(it["K"], it["u"], pflat, np.float64)
    lbl, ml, _ = dp(it["K"], it["u"], pflat, np.longdouble)
    wlb = max(wlb, abs(float(lb64 - lbl))); wm = max(wm, float(np.abs(m64 - ml).max())); wb = max(wb, bnd)
print(f"n={n} status={r['status']} iterations={len(iters)}")
print(f"max over iterations |LB_dp float64 - longdouble| = {wlb:.2e}")
print(f"max over iterations and cells |marginal float64 - longdouble| = {wm:.2e}")
print(f"first-order forward-pass rounding bound (max over iterations) = {wb:.2e}")
