"""Exact OPT by vectorized enumeration (reviewer code).
opt3: all triples, 3x3 adjugate formula, looping over the smallest index.
optk: general k, chunked batched solves over itertools.combinations."""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import itertools
import numpy as np


def opt3(X, y, lam):
    p = X.shape[1]
    G = X.T @ X + lam * np.eye(p)
    c = X.T @ y
    yy = float(y @ y)
    best, arg = np.inf, None
    for i in range(p - 2):
        J, M = np.triu_indices(p - i - 1, 1)
        J = J + i + 1; M = M + i + 1
        a, b_, cc = G[i, i], G[J, J], G[M, M]
        d, e, f = G[i, J], G[i, M], G[J, M]
        u, v, w = c[i], c[J], c[M]
        # adjugate of [[a,d,e],[d,b,f],[e,f,cc]]
        A11 = b_ * cc - f * f; A22 = a * cc - e * e; A33 = a * b_ - d * d
        A12 = -(d * cc - e * f); A13 = d * f - e * b_; A23 = -(a * f - d * e)
        det = a * A11 + d * A12 + e * A13
        qf = (u * u * A11 + v * v * A22 + w * w * A33 + 2 * u * v * A12 + 2 * u * w * A13 + 2 * v * w * A23) / det
        t = int(np.argmax(qf))
        if yy - qf[t] < best:
            best, arg = yy - qf[t], (i, int(J[t]), int(M[t]))
    return best, arg


def optk(X, y, lam, k, chunk=200000):
    p = X.shape[1]
    G = X.T @ X + lam * np.eye(p)
    c = X.T @ y
    yy = float(y @ y)
    best, arg = np.inf, None
    it = itertools.combinations(range(p), k)
    while True:
        blk = np.array(list(itertools.islice(it, chunk)), dtype=np.int64)
        if blk.size == 0:
            break
        Gb = G[blk[:, :, None], blk[:, None, :]]
        cb = c[blk]
        sol = np.linalg.solve(Gb, cb[:, :, None])[:, :, 0]
        qf = np.einsum('bi,bi->b', cb, sol)
        t = int(np.argmax(qf))
        if yy - qf[t] < best:
            best, arg = yy - qf[t], tuple(int(v) for v in blk[t])
    return best, arg
