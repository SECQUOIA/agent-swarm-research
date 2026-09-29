"""Upper bound for Munoz-Serrano's full construction with the point rule (Section 6.1).

Signature (2,1), Case 2.  A point-rule member {g1^T x >= y, g2^T x >= -y} (Sylvester coordinates,
tangency rays (g1, 1), (g2, -1)) is returned unchanged when both tangency rays have homogenizing
coordinate h >= 0.  Otherwise MS (Section 5.2, phi_lambda and r(beta)) keep the good halfspace and replace
the other by a null halfspace of the same type whose tangency line lies in H_0 = {h = 0}: its exposing
vector (x_beta, beta) satisfies a^T x_beta + d^T beta = 0 (recheck, sfree-recheck.md Section 2).  In
signature (2,1) there are at most two such lines, so the MS set is one of at most two explicit sets.  The
maximum over theta of (plain value if both tangencies are good, else the better of the two replacements)
is therefore an upper bound for the best MS set; if it is below z_K, MS's construction misses z_K.
Usage: python3 ms_asymptote_check.py   (instances of point_rule_check.py, seed 0, 40 generated)"""
import numpy as np
from scipy.optimize import minimize_scalar
from point_rule_check import case2_instance
from core import corner_bound
from orbit_n1 import sylvester

rng = np.random.default_rng(0)
out = []
for i in range(40):
    Q, b, c, sbar, P, w = case2_instance(rng)
    zk = corner_bound(Q, b, c, sbar, P, w)
    if not np.isfinite(zk):
        continue
    W, n, m = sylvester(Q, b, c); Wi = np.linalg.inv(W)
    us = W @ np.append(sbar, 1.0); xh, yh = us[:2], us[2]
    D = [W @ np.append(P[:, j], 0.0) for j in range(P.shape[1])]
    rrow = Wi[-1]                      # h(u) = rrow . u
    rx, ry = rrow[:2], rrow[2]

    def pair_bound(g1, g2):
        vals = []
        for j, d in enumerate(D):
            al = np.inf
            for (g, s) in ((g1, 1.0), (g2, -1.0)):
                v0 = g @ xh - s * yh; sl = g @ d[:2] - s * d[2]
                if v0 <= 0:
                    return 0.0
                if sl < 0:
                    al = min(al, v0 / -sl)
            if np.isfinite(al):
                vals.append(w[j] * al)
        return min(vals) if vals else np.inf

    def asymptote_normals(sign):
        """unit g with h((g, sign)) = rx.g + ry*sign = 0 (tangency line in H_0)."""
        nr = np.linalg.norm(rx)
        cst = -ry * sign / nr
        if abs(cst) > 1:
            return []
        e = rx / nr; f = np.array([-e[1], e[0]])
        return [cst * e + sq * np.sqrt(1 - cst * cst) * f for sq in (1.0, -1.0)]

    A_minus = asymptote_normals(-1.0); A_plus = asymptote_normals(1.0)

    def member(th):
        g1 = np.array([np.cos(th), np.sin(th)]); den = g1 @ xh - yh
        if den <= 1e-14:
            return None
        a = (xh @ xh - yh * yh) / (2 * den); bq = a - yh
        if a <= 0 or bq <= 1e-14:
            return None
        return g1, (xh - a * g1) / bq

    def plain(th):
        mm = member(th)
        return 0.0 if mm is None else pair_bound(*mm)

    def ms_ub(th):
        mm = member(th)
        if mm is None:
            return 0.0
        g1, g2 = mm
        h1 = rx @ g1 + ry; h2 = rx @ g2 - ry
        if h1 >= 0 and h2 >= 0:
            return pair_bound(g1, g2)
        if h1 >= 0:                      # replace the (g2, -1) halfspace
            return max([pair_bound(g1, g) for g in A_minus] + [0.0])
        return max([pair_bound(g, g2) for g in A_plus] + [0.0])

    def best(fun):
        ths = np.linspace(0, 2 * np.pi, 100001)
        vals = np.array([fun(t) for t in ths]); k = int(np.argmax(vals))
        lo, hi = ths[max(0, k - 1)], ths[min(len(ths) - 1, k + 1)]
        r = minimize_scalar(lambda t: -fun(t), bounds=(lo, hi), method='bounded', options=dict(xatol=1e-14))
        return max(vals[k], -r.fun)

    pv = best(plain)
    if pv >= zk * (1 - 1e-6):
        continue
    mv = best(ms_ub)
    out.append((i, pv / zk, min(mv, zk) / zk))
    print('instance %2d: plain point rule %.4f | upper bound for MS full construction %.4f (of z_K)' % out[-1], flush=True)
print('instances with finite z_K: counted above; plain misses: %d; MS construction reaches z_K in %d of them; max MS ratio %.6f'
      % (len(out), sum(1 for o in out if o[2] >= 1 - 1e-6), max(o[2] for o in out)))
