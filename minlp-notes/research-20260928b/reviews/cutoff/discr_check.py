"""Does the Theorem 3.1 test discriminate the endpoint formula Phi from the
rejected full-range formula Phi_full?  Regenerates the instances of
t31_check.py (same seed, same draw order) and compares min over sub-boxes of
Phi and of Phi_full (vectorized grid + Nelder-Mead).  Where min Phi_full >
min Phi, the full-range formula predicts an empty fixed point at
c = min Phi + d, but the propagator found it nonempty (t31_check.log)."""
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import minimize
import t31_check as T


def stats_full(terms, i, g):
    G = len(g); p, q = np.triu_indices(G)
    M = np.zeros(len(p)); W = np.zeros(len(p))
    for var, c, _ in terms:
        if var != i:
            continue
        v = P.polyval(g, c)
        mn = np.minimum(v[p], v[q]); mx = np.maximum(v[p], v[q])
        for r in T.real_roots(P.polyder(c), g[0], g[-1]):
            ins = (g[p] <= r) & (r <= g[q]); val = P.polyval(r, c)
            mn = np.where(ins, np.minimum(mn, val), mn); mx = np.where(ins, np.maximum(mx, val), mx)
        M += mn; W = np.maximum(W, mx - mn)
    return M, W, g[p], g[q]


def min_full(terms, box, G):
    st = [stats_full(terms, i, np.linspace(lo, hi, G)) for i, (lo, hi) in enumerate(box)]
    if len(box) == 1:
        M, W, a, b = st[0]; k = int(np.argmin(M + W)); x0 = [a[k], b[k]]
    else:
        (M1, W1, a1, b1), (M2, W2, a2, b2) = st
        V = M1[:, None] + M2[None, :] + np.maximum(W1[:, None], W2[None, :])
        i, j = np.unravel_index(np.argmin(V), V.shape); x0 = [a1[i], b1[i], a2[j], b2[j]]
    n = len(box)

    def obj(z):
        bx = []
        for k in range(n):
            lo, hi = sorted((z[2 * k], z[2 * k + 1])); L, U = box[k]
            bx.append((min(max(lo, L), U), min(max(hi, L), U)))
        return T.Phi(terms, bx, full=True)
    r = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-14, maxiter=4000))
    return min(obj(x0), r.fun)


for nvar, N, G, Gf in ((1, 120, 400, 400), (2, 80, 120, 60)):
    disc = 0; gaps = []
    for k in range(N):
        terms = T.rand_terms(nvar)
        box = []
        for _ in range(nvar):
            lo = T.rng.uniform(-1.5, 1.0); box.append((lo, lo + T.rng.uniform(0.3, 2.0)))
        pm = T.phi_min(terms, box, G)
        pf = min_full(terms, box, Gf)
        scale = 1.0 + sum(float(np.abs(c).sum()) for _, c, _ in terms)
        if pf - pm > 1e-4 * scale:
            disc += 1; gaps.append((pf - pm) / scale)
    print(f'nvar={nvar}: {N} instances; min Phi_full exceeds min Phi by > 1e-4*scale in {disc}; '
          f'median relative gap {np.median(gaps) if gaps else 0:.3g}', flush=True)
