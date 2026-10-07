"""Independent uniqueness/interiority certificate and a boundary-minimum check (probe3 family).

(a) Certificate (compare study 4.4). M_i(t) = min{F(x) : x_i = t} = Ff_i(t) + Vb_i(t) - u_i(t),
with forward/backward value functions Ff_i, Vb_i. Ff_i - t^2 and Vb_i - t^2 are concave
(see indep_grid_dp.py), and -u_i is concave on [-1,1] (u_i'' = 2 - 12 kappa t^2 >= 0.8),
so M_i - 2 t^2 is concave and on a grid interval of width h, M_i >= min(endpoint values) - h^2/2.
Grid lower bounds Ffhat <= Ff, Vbhat <= Vb come from the semi-concave grid DP. Any x with
F(x) <= UB has x_i in I_i = hull{grid intervals whose bound is <= UB}. If the box prod I_i lies
in (-1,1)^n and tridiag(2 - 12 kappa max(lo^2, hi^2), b) is positive definite there, the global
minimizer is unique, interior and nondegenerate.

(b) Boundary check: rigorous LB of min F over [-a, a]^n (same grid DP with endpoints +-a).
If it exceeds F at a point of [-1,1]^n, every global minimizer has a coordinate with |x_i| > a.
"""
import sys, json, time
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal
import indep_grid_dp as G

KAPPA, B = G.KAPPA, G.B


def sweep(c, y, order):
    """Semi-concave grid DP lower bounds of the value functions along `order`."""
    K = len(y); h = y[1] - y[0]; loss = h * h / 4 + 1e-12
    out = {}
    i0 = order[0]
    V = y * y - KAPPA * y**4 + c[i0] * y
    out[i0] = V
    for i in order[1:]:
        W = np.empty(K)
        for k0 in range(0, K, 400):
            W[k0:k0 + 400] = (B * y[k0:k0 + 400, None] * y[None, :] + V[None, :]).min(axis=1)
        V = y * y - KAPPA * y**4 + c[i] * y + W - loss
        out[i] = V
    return out


def certificate(c, K, UB):
    n = len(c); y = np.linspace(-1, 1, K); h = y[1] - y[0]
    Ff = sweep(c, y, list(range(n)))
    Vb = sweep(c, y, list(range(n - 1, -1, -1)))
    lo = np.empty(n); hi = np.empty(n)
    for i in range(n):
        Mh = Ff[i] + Vb[i] - (y * y - KAPPA * y**4 + c[i] * y)
        lbint = np.minimum(Mh[:-1], Mh[1:]) - h * h / 2 - 1e-12
        alive = np.nonzero(lbint <= UB)[0]
        lo[i], hi[i] = y[alive[0]], y[alive[-1] + 1]
    d = 2 - 12 * KAPPA * np.maximum(lo * lo, hi * hi)
    lmin = float(eigvalsh_tridiagonal(d, np.full(n - 1, B), select="i", select_range=(0, 0))[0])
    return dict(interior=bool((lo > -1).all() and (hi < 1).all()), lmin=lmin,
                max_width=float((hi - lo).max()), max_abs=float(np.maximum(abs(lo), abs(hi)).max()))


def restricted_lb(c, K, a):
    n = len(c); y = np.linspace(-a, a, K); h = y[1] - y[0]
    V = sweep(c, y, list(range(n - 1, -1, -1)))[0]
    return float(V.min()) - h * h / 4 - 1e-12


if __name__ == "__main__":
    K = int(sys.argv[1])
    for amp, n, seed, kind in json.loads(sys.argv[2]):
        c = G.coeffs(n, seed, amp); t0 = time.time()
        LB, xg = G.grid_dp(c, K)
        xp, fp = G.polish(xg, c); UB = min(fp, G.F(xg, c))
        rec = dict(amp=amp, n=n, seed=seed, K=K, LB=LB, UB=UB)
        if kind == "cert":
            rec.update(certificate(c, K, UB))
        else:
            rec.update(a=kind, restricted_LB=restricted_lb(c, K, kind),
                       coords_at_bound=int((abs(xp) > 1 - 1e-9).sum()))
            rec["restricted_LB_minus_UB"] = rec["restricted_LB"] - UB
        rec["time"] = time.time() - t0
        print(json.dumps(rec), flush=True)
