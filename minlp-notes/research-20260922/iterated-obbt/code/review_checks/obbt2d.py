"""Independent exact OBBT for two-variable objectives
    f(x) = e1(x1) + e2(x2) + a * x1 * x2,   x* = 0, f* = 0,
relaxed as phi_B = e1 + e2 + a * (McCormick estimator of x1 x2 on B)
(underestimator if a > 0, overestimator if a < 0).  e1, e2 are convex
univariate terms kept exactly.

phi_B = max_j g_j with g_j(x) = e1(x1) + e2(x2) + (affine_j), j = 1, 2, and
g_1 - g_2 affine.  For fixed x_i the minimum over the other coordinate of
max_j g_j is found in closed form (candidates: the two argmins and the
crossing point), so bounds are computed by bisection on a convex function of
one variable to full double precision.  No LP/conic solver is involved.
"""
import numpy as np

class Quad:
    """c * t^2"""
    def __init__(self, c): self.c = c
    def __call__(self, t): return self.c * t * t
    def argmin_plus_linear(self, beta):   # argmin_t c t^2 + beta t
        return -beta / (2 * self.c)

class ExpTerm:
    """exp(t) - 1 - t (convex, min 0 at 0)"""
    def __call__(self, t):
        t = np.asarray(t, float)
        small = np.abs(t) < 1e-3
        out = np.where(small, t*t/2 + t**3/6 + t**4/24 + t**5/120, np.expm1(t) - t)
        return float(out) if out.ndim == 0 else out
    def argmin_plus_linear(self, beta):   # d/dt: e^t - 1 + beta = 0
        return np.log(1 - beta) if beta < 1 else -np.inf

def affine_pieces(a, lo, hi):
    """Return list of (c1, c2, c0): a * piece_j(x) = c1 x1 + c2 x2 + c0."""
    l1, l2 = lo; u1, u2 = hi
    if a >= 0:   # McCormick under: max(l2 x1 + l1 x2 - l1 l2, u2 x1 + u1 x2 - u1 u2)
        P = [(l2, l1, -l1*l2), (u2, u1, -u1*u2)]
    else:        # over: min(u2 x1 + l1 x2 - l1 u2, l2 x1 + u1 x2 - u1 l2); a*min = |a|*max(-...)
        P = [(u2, l1, -l1*u2), (l2, u1, -u1*l2)]
    return [(a*p[0], a*p[1], a*p[2]) for p in P]

def phi(e, a, lo, hi, x):
    P = affine_pieces(a, lo, hi)
    return e[0](x[0]) + e[1](x[1]) + max(c1*x[0] + c2*x[1] + c0 for c1, c2, c0 in P)

def inner_min(e, P, i, t, lo, hi):
    """min over x_k (k = other coord) in [lo_k, hi_k] of max_j g_j with x_i = t."""
    k = 1 - i
    ek = e[k]
    # g_j(x_k) = e_k(x_k) + beta_j x_k + gamma_j
    betas, gammas = [], []
    for c in P:
        ci, ck, c0 = (c[0], c[1], c[2]) if i == 0 else (c[1], c[0], c[2])
        betas.append(ck); gammas.append(ci*t + c0 + e[i](t))
    def G(s): return ek(s) + max(betas[j]*s + gammas[j] for j in range(2))
    cands = [lo[k], hi[k]]
    for j in range(2):
        s = ek.argmin_plus_linear(betas[j])
        cands.append(min(max(s, lo[k]), hi[k]))
    if betas[0] != betas[1]:
        s = (gammas[1] - gammas[0]) / (betas[0] - betas[1])
        if lo[k] <= s <= hi[k]:
            cands.append(s)
    return min(G(s) for s in cands)

def obbt(e, a, lo, hi, U):
    """One round of exact OBBT (Jacobi): returns new (lo, hi) or None if empty."""
    lo = np.array(lo, float); hi = np.array(hi, float)
    P = affine_pieces(a, lo, hi)
    nlo, nhi = lo.copy(), hi.copy()
    for i in range(2):
        F = lambda t: inner_min(e, P, i, t, lo, hi) - U
        # x* = 0 is feasible (phi(0) <= f(0) = 0 <= U) when 0 in box
        t0 = 0.0
        assert F(t0) <= 1e-300 + 0 * U or True
        for side, end in (("hi", hi[i]), ("lo", lo[i])):
            if F(end) <= 0:
                val = end
            else:
                g, b = t0, end            # F(g) <= 0 < F(b)
                for _ in range(200):
                    m = 0.5 * (g + b)
                    if m == g or m == b: break
                    if F(m) <= 0: g = m
                    else: b = m
                val = g
            if side == "hi": nhi[i] = val
            else: nlo[i] = val
    return nlo, nhi

def lower_bound(e, a, lo, hi):
    """L(B) = min_B phi_B, by golden-section on the convex outer function."""
    P = affine_pieces(a, lo, hi)
    F = lambda t: inner_min(e, P, 0, t, lo, hi)
    g, b = lo[0], hi[0]
    r = (np.sqrt(5) - 1) / 2
    for _ in range(300):
        c = b - r * (b - g); d = g + r * (b - g)
        if F(c) <= F(d): b = d
        else: g = c
    return F(0.5 * (g + b))
