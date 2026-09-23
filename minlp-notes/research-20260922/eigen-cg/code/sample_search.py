"""Random search for E-CG cuts violated at given points z of P_BH(n).

f(z; v) = floor(v0^2) + sum ceil(v_i^2 + 2 v_i v0) x_i + sum ceil(2 v_i v_j) X_ij
        = q_M(v) + rounding-up terms - frac(v0^2),  q_M(v) = (v0,v)^T M (v0,v) >= 0 on P_BH.
So a violation needs q_M(v) < 1: sample (v0,v) uniformly in the ellipsoid {q_M < 1}.
"""
import numpy as np
from bh import pairs, moment_matrix, dim


def switch(n, z, S):
    """Image of z under x_i -> 1 - x_i for i in S (automorphism of BQP_n and of P_BH)."""
    P = pairs(n)
    x = z[:n].copy()
    X = {p: z[n + k] for k, p in enumerate(P)}
    nx = x.copy()
    for i in S:
        nx[i] = 1 - x[i]
    nz = list(nx)
    for (i, j) in P:
        if i in S and j in S:
            nz.append(1 - x[i] - x[j] + X[(i, j)])
        elif i in S:
            nz.append(x[j] - X[(i, j)])
        elif j in S:
            nz.append(x[i] - X[(i, j)])
        else:
            nz.append(X[(i, j)])
    return np.array(nz)


def ecg_values(n, z, V):
    """E-CG left-hand side at z for each row (v0, v) of V (N x (n+1))."""
    v0 = V[:, 0]
    v = V[:, 1:]
    f = np.floor(v0 ** 2)
    for i in range(n):
        f = f + np.ceil(v[:, i] ** 2 + 2 * v[:, i] * v0) * z[i]
    for k, (i, j) in enumerate(pairs(n)):
        if z[n + k] != 0:
            f = f + np.ceil(2 * v[:, i] * v[:, j]) * z[n + k]
    return f


def search(n, z, N=10 ** 6, rounds=10, rng=None, scale=1.0):
    rng = rng or np.random.default_rng()
    M = moment_matrix(n, z)
    L = np.linalg.cholesky(M)
    Linv_T = np.linalg.inv(L).T
    best = (np.inf, None)
    for _ in range(rounds):
        u = rng.standard_normal((N, n + 1))
        u /= np.linalg.norm(u, axis=1, keepdims=True)
        u *= rng.random((N, 1)) ** (1.0 / (n + 1)) * scale
        V = u @ Linv_T.T
        f = ecg_values(n, z, V)
        k = int(np.argmin(f))
        if f[k] < best[0]:
            best = (f[k], V[k].copy())
    return best
