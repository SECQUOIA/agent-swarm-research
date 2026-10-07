"""Instance generators that follow the published descriptions.

Neither Buchheim-Traversi (B-T, Optimization Online 2013/07/3953, Sec. 6.1)
nor de Meijer et al. (dMPSS, arXiv:2603.28979v1, Appendix A) publish their
instance files or seeds, so these generators draw from the stated
distributions with our own seeds.  Every instance is a ternary problem
  min x^T Q x + c^T x   s.t. x in {-1,0,1}^n   [and 1^T x = 0 for TQP-Linear].

B-T state bounds l <= x <= u without values in Sec. 6.1; their RLT relaxation
uses -1 <= x <= 1 and they speak of "ternary instances", so l = -1, u = 1.
"""
import numpy as np


def _orthonormal(rng, n):
    A = rng.uniform(-1.0, 1.0, size=(n, n))
    Qm, R = np.linalg.qr(A)
    # Gram-Schmidt sign convention: make diag(R) positive
    Qm = Qm * np.sign(np.diag(R))
    return Qm


def bt_instance(n, p, seed):
    """B-T Sec. 6.1: p eigenvalues U[-1,0], n-p eigenvalues U[0,1],
    eigenvectors = orthonormalized U[-1,1] vectors, L ~ U[-1,1]^n, c = 0."""
    rng = np.random.default_rng([2013, n, p, seed])
    lam = np.concatenate([rng.uniform(-1, 0, p), rng.uniform(0, 1, n - p)])
    V = _orthonormal(rng, n)
    Q = (V * lam) @ V.T
    Q = (Q + Q.T) / 2
    L = rng.uniform(-1, 1, n)
    return dict(name=f"bt_n{n}_p{p}_s{seed}", family="BT", n=n, Q=Q, c=L,
                linear=False)


def dm_instance(kind, typ, n, p, seed):
    """dMPSS Appendix A.  kind in {'QUTO','LIN'}; typ in {1,2,3}; p in {25,50,75}.

    Type-2: the text says the first floor(n/2) entries of mu are zero and
    "each remaining entry is nonnegative with probability p/100 and zero
    otherwise".  We read this as: each remaining entry is U[0,1] with
    probability p/100 and 0 otherwise (so Q is PSD of rank <= ceil(n/2)).
    For QUTO the diagonal of Q is replaced by its absolute value.
    """
    rng = np.random.default_rng([2026, {"QUTO": 1, "LIN": 2}[kind], typ, n, p, seed])
    if typ == 1:
        k = (p * n) // 100
        mu = np.concatenate([rng.uniform(-1, 0, k), rng.uniform(0, 1, n - k)])
        V = _orthonormal(rng, n)
        Q = (V * mu) @ V.T
    elif typ == 2:
        V = _orthonormal(rng, n)
        mu = np.zeros(n)
        m = n // 2
        mask = rng.uniform(size=n - m) < p / 100
        mu[m:] = np.where(mask, rng.uniform(0, 1, n - m), 0.0)
        Q = (V * mu) @ V.T
    elif typ == 3:
        U = np.where(rng.uniform(size=(n, n)) < p / 100,
                     rng.uniform(-1, 1, size=(n, n)), 0.0)
        Q = np.triu(U)
        Q = Q + np.triu(Q, 1).T
    else:
        raise ValueError(typ)
    Q = (Q + Q.T) / 2
    if kind == "QUTO":
        Q[np.diag_indices(n)] = np.abs(np.diag(Q))
    c = rng.uniform(-1, 1, n)
    return dict(name=f"dm_{kind}_t{typ}_n{n}_p{p}_s{seed}", family="DM-" + kind,
                n=n, Q=Q, c=c, linear=(kind == "LIN"))


def brute_force_opt(inst):
    """Exact optimum by enumeration of {-1,0,1}^n (n <= 14)."""
    import itertools
    n, Q, c = inst["n"], inst["Q"], inst["c"]
    best, arg = np.inf, None
    pts = np.array(list(itertools.product([-1, 0, 1], repeat=n)), dtype=float)
    if inst["linear"]:
        pts = pts[np.abs(pts.sum(1)) < 0.5]
    vals = np.einsum("ij,jk,ik->i", pts, Q, pts) + pts @ c
    k = int(np.argmin(vals))
    return float(vals[k]), pts[k]
