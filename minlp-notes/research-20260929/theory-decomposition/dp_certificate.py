"""Fixed-slope decomposition certificate (Sections 1.5 and 3.3) for the path family

    F(x) = sum_i phi(x_i) + b sum_i x_i x_{i+1} + sum_i c_i x_i,  phi(t) = t^2 - kappa t^4,  x in [-1,1]^n.

Path decomposition: bags t = 0..n-2 with V_t = {t, t+1}, root bag 0, separator S_t = {t}
(t >= 1). Bag t holds phi(x_t) + c_t x_t + b x_t x_{t+1}; the last bag also holds
phi(x_{n-1}) + c_{n-1} x_{n-1}. Unary factors are convex (kappa <= 1/6) and kept exact;
the bilinear factor is relaxed by alphaBB with alpha = |b|/2 (so (U^q) with alpha' = |b|/2).

Cells and leaves are shell partitions (Lemma 3.1) around x*, slopes are
lambda_t = phi'(x*_t) + c_t + b x*_{t+1} (Lemma 3.2) or zero. The beta values are
computed exactly as in Lemma 1.5 by convex minimization over sub-boxes (nested
bisection on monotone derivatives, 60 steps each: floating-point accurate).

(Leaf, cell) pairs are found by a closed intersection test widened by PAIR_TOL. Around a
non-dyadic centre, shell edges are rounded, and boxes that touch in exact arithmetic can be
1 ulp apart. The unwidened test (first version) drops such pairs, which can give a bound higher
than Lemma 1.5's; it stays valid while no pair with positive-length overlap is dropped (remark
after Lemma 1.3). The tolerance must stay below the gaps between boxes that do not meet;
checked in check_pairs_exact.py. At x* = 0 all edges are dyadic and nothing changes.
"""
import math
import itertools
import numpy as np

NB = 60  # bisection steps
PAIR_TOL = 1e-12  # widening of the (leaf, cell) intersection test, as in adaptive/ls_lib.interval_pairs


def phi(t, kappa):
    t2 = t * t
    return t2 - kappa * t2 * t2


def dphi(t, kappa):
    return t * (2 - 4 * kappa * t * t)


def F(x, b, kappa, c):
    return float(np.sum(phi(x, kappa)) + b * np.sum(x[:-1] * x[1:]) + np.dot(c, x))


def shells(p, h, mu, dim, lo=-1.0, hi=1.0):
    """Shell partition Pi(p; h, 2^-mu) of [lo,hi]^dim (Lemma 3.1). Returns (L, U) arrays (N, dim)."""
    p = np.asarray(p, float)
    s0 = hi - lo
    J = max(0, math.ceil(math.log2(s0 / h)))
    corners = np.array(list(itertools.product([0, 1], repeat=dim)), float)
    Ls = [p[None, :] + (corners - 1) * h]
    Us = [Ls[0] + h]
    Nax = 2 ** (mu + 2)
    ar = np.arange(Nax)
    grids = np.stack(np.meshgrid(*([ar] * dim), indexing="ij"), axis=-1).reshape(-1, dim)
    inner = np.all((grids >= Nax // 4) & (grids < 3 * Nax // 4), axis=1)
    grids = grids[~inner]
    for j in range(1, J + 1):
        R = 2.0 ** j * h
        g = 2.0 ** (-mu) * 2.0 ** (j - 1) * h
        edges = p[None, :] - R + g * np.arange(Nax + 1)[:, None]  # (Nax+1, dim)
        cl = np.take_along_axis(edges, grids, axis=0) if dim == 1 else np.stack(
            [edges[grids[:, a], a] for a in range(dim)], axis=1)
        cu = np.stack([edges[grids[:, a] + 1, a] for a in range(dim)], axis=1)
        ok = np.all((cu > lo) & (cl < hi), axis=1)
        Ls.append(cl[ok])
        Us.append(cu[ok])
    L = np.clip(np.concatenate(Ls), lo, hi)
    U = np.clip(np.concatenate(Us), lo, hi)
    keep = np.all(U - L > 1e-15, axis=1)
    return L[keep], U[keep]


def global_min(n, b, kappa, c, G=4001):
    """Grid DP for the global minimizer, then Newton-type refinement (scipy)."""
    from scipy.optimize import minimize
    y = np.linspace(-1, 1, G)
    # backward DP over the path: V_{n-1}(y) = phi(y) + c y
    V = phi(y, kappa) + c[-1] * y
    arg = []
    for i in range(n - 2, -1, -1):
        M = (phi(y, kappa) + c[i] * y)[:, None] + b * y[:, None] * y[None, :] + V[None, :]
        a = np.argmin(M, axis=1)
        arg.append(a)
        V = M[np.arange(G), a]
    arg = arg[::-1]
    i0 = int(np.argmin(V))
    xs = [i0]
    for i in range(n - 1):
        xs.append(int(arg[i][xs[-1]]))
    x0 = y[xs]
    fun = lambda x: F(x, b, kappa, c)
    def grad(x):
        g = dphi(x, kappa) + c
        g[:-1] += b * x[1:]
        g[1:] += b * x[:-1]
        return g
    r = minimize(fun, x0, jac=grad, bounds=[(-1, 1)] * n, method="L-BFGS-B",
                 options={"ftol": 1e-16, "gtol": 1e-13, "maxiter": 10000})
    return r.x, r.fun, float(V[i0])


def min_subbox(l1, u1, l2, u2, L1, U1, lin1, lin2, b, kappa, last, cz2):
    """Vectorized min over z1 in [L1,U1], z2 in [l2,u2] of
       phi(z1) + lin1*z1 + b z1 z2 - (|b|/2)[(z1-l1)(u1-z1) + (z2-l2)(u2-z2)] + lin2*z2
       (+ phi(z2) + cz2*z2 if last).  lin1, lin2 arrays (per pair)."""
    ab = abs(b)

    def z2star(z1):
        if not last:
            return np.clip(((ab / 2) * (l2 + u2) - b * z1 - lin2) / ab, l2, u2)
        # derivative in z2: dphi(z2) + cz2 + b z1 + (ab/2)(2 z2 - l2 - u2) + lin2, increasing
        a, c_ = l2.copy(), u2.copy()
        d = lambda z2: dphi(z2, kappa) + cz2 + b * z1 + (ab / 2) * (2 * z2 - l2 - u2) + lin2
        da, dc = d(a), d(c_)
        for _ in range(NB):
            m = 0.5 * (a + c_)
            dm = d(m)
            pos = dm > 0
            c_ = np.where(pos, m, c_)
            a = np.where(pos, a, m)
        z = 0.5 * (a + c_)
        z = np.where(da >= 0, l2, z)
        z = np.where(dc <= 0, u2, z)
        return z

    def g(z1, z2):
        v = phi(z1, kappa) + lin1 * z1 + b * z1 * z2 - (ab / 2) * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2)) + lin2 * z2
        if last:
            v = v + phi(z2, kappa) + cz2 * z2
        return v

    def hprime(z1):
        z2 = z2star(z1)
        return dphi(z1, kappa) + lin1 + b * z2 + (ab / 2) * (2 * z1 - l1 - u1)

    a, c_ = L1.copy(), U1.copy()
    ha, hc = hprime(a), hprime(c_)
    for _ in range(NB):
        m = 0.5 * (a + c_)
        pos = hprime(m) > 0
        c_ = np.where(pos, m, c_)
        a = np.where(pos, a, m)
    z1 = 0.5 * (a + c_)
    z1 = np.where(ha >= 0, L1, z1)
    z1 = np.where(hc <= 0, U1, z1)
    z1 = np.where(U1 - L1 <= 0, L1, z1)
    return g(z1, z2star(z1))


def certificate(n, b, kappa, c, xstar, h, mu, slopes="affine", keep=False):
    """Returns (root bound, size, details). Bags t = 0..n-2."""
    lam = np.zeros(n)
    if slopes == "affine":
        for t in range(1, n - 1):
            lam[t] = dphi(xstar[t], kappa) + c[t] + b * xstar[t + 1]
    child = None  # (cell_lo, cell_hi, beta) of separator of bag t+1
    size = 0
    store = {}
    for t in range(n - 2, -1, -1):
        last = (t == n - 2)
        L, U = shells(xstar[t:t + 2], h, mu, 2)
        size += len(L)
        l1, u1, l2, u2 = L[:, 0], U[:, 0], L[:, 1], U[:, 1]
        if child is not None:
            clo, chi, cbeta = child
            # min beta over child cells meeting [l2,u2] (closed test, widened by PAIR_TOL)
            meet = (clo[None, :] <= u2[:, None] + PAIR_TOL) & (chi[None, :] >= l2[:, None] - PAIR_TOL)
            off = np.where(meet, cbeta[None, :], np.inf).min(axis=1)
            lin2 = np.full(len(L), lam[t + 1])
        else:
            off = np.zeros(len(L))
            lin2 = np.zeros(len(L))
        cz2 = c[n - 1]
        if t == 0:
            vals = min_subbox(l1, u1, l2, u2, l1.copy(), u1.copy(), np.full(len(L), c[0]), lin2, b, kappa, last, cz2) + off
            root = float(vals.min())
            if keep:
                store[t] = (L, U, None)
            return root, size, store, lam
        Pl, Pu = shells(xstar[t:t + 1], h, mu, 1)
        size += len(Pl)
        plo, phi_ = Pl[:, 0], Pu[:, 0]
        # pairs (leaf, cell) with nonempty closed intersection in coordinate t (widened by PAIR_TOL)
        meet = (plo[None, :] <= u1[:, None] + PAIR_TOL) & (phi_[None, :] >= l1[:, None] - PAIR_TOL)
        bi, di = np.nonzero(meet)
        L1 = np.maximum(l1[bi], plo[di])
        U1 = np.minimum(u1[bi], phi_[di])
        vals = min_subbox(l1[bi], u1[bi], l2[bi], u2[bi], L1, U1,
                          np.full(len(bi), c[t] - lam[t]), lin2[bi], b, kappa, last, cz2) + off[bi]
        beta = np.full(len(plo), np.inf)
        np.minimum.at(beta, di, vals)
        child = (plo, phi_, beta)
        if keep:
            store[t] = (Pl, Pu, beta)


def grid_value_functions(n, b, kappa, c, G=2001):
    """phi_t on a grid of s (upper approximations: min over a y-grid). Returns dict t -> (s, phi_t(s))."""
    y = np.linspace(-1, 1, G)
    out = {}
    V = None
    for t in range(n - 2, 0, -1):
        base = (phi(y, kappa) + c[t] * y)[:, None] + b * y[:, None] * y[None, :]
        if t == n - 2:
            M = base + (phi(y, kappa) + c[n - 1] * y)[None, :]
        else:
            M = base + V[None, :]
        V = M.min(axis=1)
        out[t] = (y, V.copy())
    return out
