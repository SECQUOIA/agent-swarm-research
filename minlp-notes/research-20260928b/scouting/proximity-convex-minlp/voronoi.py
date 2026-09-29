"""l_inf radius of Voronoi cells of lattices in a quadratic norm (float LP).

rho_inf(Q; B) = max { ||B u||_inf : B u in Vor_Q(B Z^k) }, where the lattice is
B Z^k (B an n x k integer basis) and the metric is Q restricted to span(B).
Voronoi-relevant vectors have Q-norm <= 2 mu (mu = covering radius), and
mu <= 1/2 sqrt(sum ||b_i*||^2) for any basis (nearest-plane bound), so we
LLL-reduce, bound mu, and enumerate all lattice vectors of Q-norm <= 2 mu
with Fincke-Pohst before solving 2n LPs.
"""
import math
import numpy as np
from scipy.optimize import linprog


def gram_schmidt(Bc, G):
    k = Bc.shape[1]
    Bs = np.zeros_like(Bc, dtype=float)
    mu = np.zeros((k, k))
    for i in range(k):
        v = Bc[:, i].astype(float).copy()
        for j in range(i):
            mu[i, j] = (Bc[:, i] @ G @ Bs[:, j]) / (Bs[:, j] @ G @ Bs[:, j])
            v -= mu[i, j] * Bs[:, j]
        Bs[:, i] = v
    return Bs, mu


def lll(B, G, delta=0.99):
    B = np.array(B, dtype=float).copy()
    k = B.shape[1]
    i = 1
    while i < k:
        Bs, mu = gram_schmidt(B, G)
        for j in range(i - 1, -1, -1):
            q = round(mu[i, j])
            if q:
                B[:, i] -= q * B[:, j]
                Bs, mu = gram_schmidt(B, G)
        ni = Bs[:, i] @ G @ Bs[:, i]
        nm = Bs[:, i - 1] @ G @ Bs[:, i - 1]
        if ni >= (delta - mu[i, i - 1] ** 2) * nm:
            i += 1
        else:
            B[:, [i, i - 1]] = B[:, [i - 1, i]]
            i = max(i - 1, 1)
    return np.round(B)


def short_vectors(B, G, R2):
    """All nonzero coefficient vectors u with ||B u||_G^2 <= R2 (Fincke-Pohst)."""
    k = B.shape[1]
    Gc = B.T @ G @ B
    L = np.linalg.cholesky(Gc)  # Gc = L L^T ; ||u||^2 = ||L^T u||^2
    Rm = L.T  # upper triangular
    out = []

    def rec(level, u, partial):
        if level < 0:
            if any(u):
                out.append(u.copy())
            return
        # contribution of rows >= level: (Rm[level] @ u)^2 with u[level] free
        s = sum(Rm[level, j] * u[j] for j in range(level + 1, k))
        d = Rm[level, level]
        rem = R2 - partial
        if rem < 0:
            return
        r = math.sqrt(rem) / abs(d)
        c = -s / d
        for v in range(math.ceil(c - r - 1e-12), math.floor(c + r + 1e-12) + 1):
            u[level] = v
            val = (d * v + s) ** 2
            if partial + val <= R2 * (1 + 1e-12):
                rec(level - 1, u, partial + val)
        u[level] = 0

    rec(k - 1, [0] * k, 0.0)
    return out


def rho_inf(G, B=None):
    G = np.array(G, dtype=float)
    n = G.shape[0]
    if B is None:
        B = np.eye(n)
    B = lll(np.array(B, dtype=float), G)
    Bs, _ = gram_schmidt(B, G)
    mu2 = 0.25 * sum(Bs[:, i] @ G @ Bs[:, i] for i in range(B.shape[1]))
    vecs = short_vectors(B, G, 4 * mu2)
    k = B.shape[1]
    Gc = B.T @ G @ B
    Aub = np.array([np.array(u) @ Gc for u in vecs])
    bub = np.array([0.5 * np.array(u) @ Gc @ np.array(u) for u in vecs])
    nr = np.linalg.norm(Aub, axis=1)
    Aub, bub = Aub / nr[:, None], bub / nr
    best = 0.0
    for i in range(n):
        for sgn in (1, -1):
            obj = -sgn * B[i, :]
            res = linprog(obj, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * k, method="highs")
            assert res.status == 0, res.message
            best = max(best, -res.fun)
    return best, len(vecs), math.sqrt(mu2)
