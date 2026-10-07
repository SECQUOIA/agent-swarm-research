"""Shared routines for the consistency-relaxation checks.

One separator s in an interval.  The split relaxation with exact bag minima
has gap

    gap(Phi) = inf_{phi in Phi} [ max_s (phi - U) + max_s (L - phi) ],

where U = v_A (child-side value function) and L = f* - v_B (Theorem 2.1 of
consistency-relaxations.md).  On a finite grid this is an LP in the
coefficients of phi and two scalars a, b.  Values on a grid are lower
estimates of the continuum gap; re-evaluating the LP solution on a finer
grid gives an upper estimate (up to the grid resolution of the finer grid).
All computations are floating point (HiGHS via scipy); they are
illustrations, not certified values.
"""
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog


def grid(lo, hi, m=4001, extra=()):
    """Uniform grid plus Chebyshev points plus given breakpoints, sorted."""
    u = np.linspace(lo, hi, m)
    k = np.arange(m)
    ch = 0.5 * (lo + hi) + 0.5 * (hi - lo) * np.cos(np.pi * (k + 0.5) / m)
    pts = np.concatenate([u, ch, np.array([x for x in extra if lo <= x <= hi])])
    return np.unique(pts)


def cheb_basis(s, deg, lo=-1.0, hi=1.0):
    """Chebyshev basis T_0..T_deg on [lo, hi] evaluated at s (m x (deg+1))."""
    t = (2 * s - (lo + hi)) / (hi - lo)
    return C.chebvander(np.clip(t, -1, 1), deg)


def band_gap(B, U, L, tight=False):
    """min a + b s.t. B c - U <= a, L - B c <= b.  Returns (gap, c, a, b).
    tight=True uses HiGHS feasibility tolerances 1e-10 instead of 1e-7."""
    m, d = B.shape
    # variables x = [c (d), a, b]
    cost = np.zeros(d + 2)
    cost[d] = 1.0
    cost[d + 1] = 1.0
    A1 = np.hstack([B, -np.ones((m, 1)), np.zeros((m, 1))])
    A2 = np.hstack([-B, np.zeros((m, 1)), -np.ones((m, 1))])
    A = np.vstack([A1, A2])
    rhs = np.concatenate([U, -L])
    opts = {}
    if tight:
        opts = {"primal_feasibility_tolerance": 1e-10,
                "dual_feasibility_tolerance": 1e-10}
    res = linprog(cost, A_ub=A, b_ub=rhs, bounds=[(None, None)] * (d + 2),
                  method="highs", options=opts)
    if res.status != 0:
        raise RuntimeError(res.message)
    x = res.x
    return res.fun, x[:d], x[d], x[d + 1]


def eval_gap(phi_vals, U, L):
    """Value max(phi - U) + max(L - phi) of a fixed split on a grid."""
    return np.max(phi_vals - U) + np.max(L - phi_vals)


def poly_gap(Ufun, Lfun, deg, lo=-1.0, hi=1.0, m=4001, mfine=100001, extra=()):
    """Gap of the degree-deg polynomial class. Returns (lower_est, upper_est)."""
    s = grid(lo, hi, m, extra)
    B = cheb_basis(s, deg, lo, hi)
    g, c, _, _ = band_gap(B, Ufun(s), Lfun(s))
    sf = grid(lo, hi, mfine, extra)
    phif = cheb_basis(sf, deg, lo, hi) @ c
    return g, eval_gap(phif, Ufun(sf), Lfun(sf))


def cell_gap(Ufun, Lfun, lo, hi, deg, m=801, mfine=8001, extra=()):
    """Per-cell gap g_D for polynomials of degree deg on the cell [lo, hi]."""
    s = grid(lo, hi, m, extra)
    B = cheb_basis(s, deg, lo, hi)
    g, c, _, _ = band_gap(B, Ufun(s), Lfun(s))
    sf = grid(lo, hi, mfine, extra)
    phif = cheb_basis(sf, deg, lo, hi) @ c
    return g, eval_gap(phif, Ufun(sf), Lfun(sf))


def cellwise_gap(Ufun, Lfun, cells, degs, extra=(), m=801, mfine=8001):
    """Gap of a discontinuous cellwise class = max over cells of g_D
    (Proposition 2.3).  cells: list of (lo, hi); degs: list of degrees."""
    lows, ups = [], []
    for (lo, hi), p in zip(cells, degs):
        g, gu = cell_gap(Ufun, Lfun, lo, hi, p, m=m, mfine=mfine, extra=extra)
        lows.append(g)
        ups.append(gu)
    return max(lows), max(ups), lows


def joint_cellwise_gap(Ufun, Lfun, cells, degs, m=801, extra=()):
    """Same class solved as one LP with a single pair (a, b); used to check
    that the gap of a cellwise class is the maximum of the per-cell gaps."""
    blocks, Us, Ls = [], [], []
    ncoef = sum(p + 1 for p in degs)
    off = 0
    for (lo, hi), p in zip(cells, degs):
        s = grid(lo, hi, m, extra)
        Bc = cheb_basis(s, p, lo, hi)
        Bfull = np.zeros((len(s), ncoef))
        Bfull[:, off:off + p + 1] = Bc
        off += p + 1
        blocks.append(Bfull)
        Us.append(Ufun(s))
        Ls.append(Lfun(s))
    g, _, _, _ = band_gap(np.vstack(blocks), np.concatenate(Us), np.concatenate(Ls))
    return g


def hat_basis(s, nodes):
    """Continuous piecewise-linear hat functions on the given nodes."""
    B = np.zeros((len(s), len(nodes)))
    for j in range(len(nodes)):
        e = np.zeros(len(nodes))
        e[j] = 1.0
        B[:, j] = np.interp(s, nodes, e)
    return B
