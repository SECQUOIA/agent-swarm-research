"""Upper bound for Munoz-Serrano's full Section 5.2 construction with the point rule, independent of how
the transformation is parametrized.

Facts used (checked numerically in point_rule_recheck.py on 300 random transformations per instance, error
~1e-16): whenever MS modify an inequality (tangency point on the wrong side of H), the new halfspace is, in
homogeneous form, a null halfspace tangent to the cone along a null line of H_0 = {t = 0} (the direction
(x_beta, beta) of MS Section 5.2.2 lies in H_0, and maximality forces a null normal).  H_0 meets the cone in
exactly two null lines.  So each set MS can return is either a plain point-rule member (both tangency points
on the slice side) or {kept halfspace of the member} cap {tangent halfspace along one of the two null lines
of H_0}.  Taking the better of the two choices for every member (theta) gives an upper bound on the MS
construction under every transformation.
Usage: python3 ms_asymptote_bound.py
"""
import sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import minimize_scalar
from point_rule_recheck import case2_instance, zK, sylv, bound_normals, unit, J


def members(th, us):
    xh, yh = us[:2], us[2]
    g1 = unit(th); den = g1 @ xh - yh
    if den <= 1e-14:
        return None
    a = (xh @ xh - yh * yh) / (2 * den); bq = a - yh
    if a <= 0 or bq <= 1e-14:
        return None
    return g1, (xh - a * g1) / bq


def h0_null_lines(l):
    """the two null lines of H_0 = {l^T v = 0} (l spacelike for the dual form in Case 2)."""
    B = np.linalg.svd(l[None, :])[2][1:]             # orthonormal basis of l^perp (2 x 3)
    G = B @ J @ B.T                                   # form restricted to H_0 (indefinite)
    mu, V = np.linalg.eigh(G)
    assert mu[0] < 0 < mu[1]
    zs = []
    for s in (1, -1):
        c = np.array([1 / np.sqrt(-mu[0]), s / np.sqrt(mu[1])])   # c^T diag(mu) c = 0
        z = B.T @ (V @ c)
        zs.append(z)
    for z in zs:
        assert abs(z @ J @ z) < 1e-9 * (z @ z) and abs(l @ z) < 1e-9 * np.linalg.norm(z)
    return zs


def value(th, us, Ds, w, l, zs, mode):
    mm = members(th, us)
    if mm is None:
        return 0.0
    g1, g2 = mm
    n1 = np.append(g1, -1.0); n2 = np.append(g2, 1.0)      # inward normals
    t1 = l @ np.append(g1, 1.0); t2 = l @ np.append(g2, -1.0)   # t-coordinates of the tangency rays
    if mode == 'plain' or (t1 >= 0 and t2 >= 0):
        return float(bound_normals(np.array([n1, n2]), us, Ds, w))
    keep = n1 if t1 >= 0 else n2
    best = 0.0
    for z in zs:
        n = J @ z
        n = n if n @ us > 0 else -n
        best = max(best, float(bound_normals(np.array([keep, n]), us, Ds, w)))
    return best


def scan(us, Ds, w, l, zs, mode, n=100001):
    th = np.linspace(0, 2 * np.pi, n)
    v = np.array([value(t, us, Ds, w, l, zs, mode) for t in th])
    k = int(np.argmax(v))
    r = minimize_scalar(lambda t: -value(t, us, Ds, w, l, zs, mode), bounds=(th[max(k - 1, 0)], th[min(k + 1, n - 1)]),
                        method='bounded', options=dict(xatol=1e-14))
    return max(v[k], -r.fun)


if __name__ == '__main__':
    rng = np.random.default_rng(0)
    out = []
    for i in range(40):
        Q, b, c, sbar, P, w = case2_instance(rng)
        zk = zK(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            continue
        W, l = sylv(Q, b, c)
        us = W @ np.append(sbar, 1.0)
        Ds = [W @ np.append(P[:, j], 0.0) for j in range(P.shape[1])]
        zs = h0_null_lines(l)
        zp = scan(us, Ds, w, l, zs, 'plain')
        if zp >= zk * (1 - 1e-6):
            continue
        zu = scan(us, Ds, w, l, zs, 'asym')
        out.append((i, zp / zk, zu / zk))
        print('instance %2d: plain point rule %.6f | upper bound for the MS construction (best asymptote choice) %.6f  (of z_K)'
              % (i, zp / zk, zu / zk), flush=True)
    print('MS construction upper bound reaches z_K in %d of %d plain misses; max upper-bound ratio %.6f'
          % (sum(u >= 1 - 1e-6 for _, _, u in out), len(out), max(u for _, _, u in out)))
