"""Window problems for the two-state examples of extension-n2.md (float screening).

Uses the example family and Euler transcription of theory-bangbang/n2/ (model.py, discrete.py; read
only).  For a quadratic calibration family S_t(x) = p_t.x + (x - xbar_t)^T P_t (x - xbar_t) / 2, the
window objective
    J_W(x_a, u_a..u_{b-1}) = sum_{t=a}^{b-1} h [l0(x_t) + l1(x_t) u_t] + S_b(x_b) - S_a(x_a)
is an exact quadratic in v = (d_a, om_a, ..., om_{b-1}) because the dynamics are linear.  Its minimum
over the reachable entry box times U^W is computed by enumerating the faces of the whole box
(box_min_full; exact in floating point up to rounding).
"""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "n2"))
from model import B, Par, continuous_family  # noqa: E402
import discrete as dz  # noqa: E402

EXAMPLES = {
    # extension-n2.md example A (kappa_tau = b.w = +0.3)
    "A": Par(rho=2, k1=-.3, k2=-.3, q=.3, c=1, x20=.5),
    # the same data with k2 -> +0.3: kappa_tau = -0.3 (counterexample to window exactness)
    "Aminus": Par(rho=2, k1=-.3, k2=.3, q=.3, c=1, x20=.5),
    # k2 = 0: kappa_tau = 0 (degenerate case)
    "Azero": Par(rho=2, k1=-.3, k2=0.0, q=.3, c=1, x20=.5),
}


def transferred(p, kk, eps, delta1):
    """Transferred continuous tangential family: P_t = P(t h) (continuous_family, linear rate)."""
    Pf, dg = continuous_family(p, eps, delta1=delta1)
    N, h = kk["N"], kk["h"]
    return np.array([Pf(t * h) for t in range(N + 1)]), dg


def window_quad(p, kk, Ps, a, b):
    N, h, x, u, pc = kk["N"], kk["h"], kk["x"], kk["u"], kk["p"]
    F = dz.fx(h)
    m = b - a
    n = 2 + m
    kvec = np.array([p.k1, p.k2])
    E = np.zeros((2, n))
    E[:, :2] = np.eye(2)
    g = np.zeros(n)
    H = np.zeros((n, n))
    Ea = E.copy()
    for t in range(a, b):
        f = np.zeros(n)
        f[2 + t - a] = 1.0
        gl0 = np.array([p.q * x[t, 0], p.e - p.c * x[t, 1]])
        g += h * E.T @ (gl0 + u[t] * kvec) + h * (kvec @ x[t]) * f
        H += h * E.T @ p.Hxx @ E + h * (np.outer(E.T @ kvec, f) + np.outer(f, E.T @ kvec))
        E = F @ E + h * np.outer(B, f)
    g += E.T @ pc[b] - Ea.T @ pc[a]
    H += E.T @ Ps[b] @ E - Ea.T @ Ps[a] @ Ea
    lo_b, hi_b = dz.reach_box(p, N, h)
    lo = np.concatenate([lo_b[a] - x[a], [-1.0 - u[t] for t in range(a, b)]])
    hi = np.concatenate([hi_b[a] - x[a], [1.0 - u[t] for t in range(a, b)]])
    if a == 0:
        lo[:2] = hi[:2] = 0.0
    return g, H, lo, hi


def box_min_full(g, H, lo, hi):
    """Minimum of g.v + v^T H v / 2 over the box by enumerating all faces (entry block included).
    Faces whose free Hessian block is not positive definite are skipped: their relative-interior
    stationary points are not minima, and a minimizer then also exists on a smaller face."""
    n = len(g)
    fixed_dims = [i for i in range(n) if lo[i] == hi[i]]
    var = [i for i in range(n) if lo[i] < hi[i]]
    best, bv = np.inf, None
    for pat in itertools.product((0, 1, 2), repeat=len(var)):
        v = lo.astype(float).copy()
        pat = np.array(pat)
        vv = np.array(var)
        v[vv[pat == 1]] = hi[vv[pat == 1]]
        free = vv[pat == 2]
        if len(free):
            fx_ = np.setdiff1d(np.arange(n), free)
            Hff = H[np.ix_(free, free)]
            if np.linalg.eigvalsh(Hff).min() <= 0:
                continue
            vf = np.linalg.solve(Hff, -(g[free] + H[np.ix_(free, fx_)] @ v[fx_]))
            if np.any(vf < lo[free] - 1e-15) or np.any(vf > hi[free] + 1e-15):
                continue
            v[free] = np.clip(vf, lo[free], hi[free])
        val = g @ v + 0.5 * v @ H @ v
        if val < best:
            best, bv = val, v
    return best, bv
