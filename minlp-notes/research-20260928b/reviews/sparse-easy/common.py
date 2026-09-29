"""Independent helpers for the review of phase-transition.md (Sections 1-3, 6).
Written from the note's definitions only; does not import the author's code."""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
    os.environ.setdefault(v, "1")
import numpy as np
import cvxpy as cp


def make_instance(n, p, k, b=1.0, sigma=0.5, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    return X, y, S, beta


def ridge_on(X, y, lam, S):
    """f(S), beta^S, r_S computed through the n x n form M_S^{-1} y (not the p-side solve)."""
    n = X.shape[0]
    S = np.asarray(S, int)
    if len(S) == 0:
        return float(y @ y), np.zeros(0), y.copy()
    XS = X[:, S]
    M = np.eye(n) + XS @ XS.T / lam
    r = np.linalg.solve(M, y)
    beta = XS.T @ r / lam           # X_S' r = lam beta^S
    return float(y @ r), beta, r


def g_closed(X, y, lam, z):
    n = X.shape[0]
    M = np.eye(n) + (X * z) @ X.T / lam
    a = np.linalg.solve(M, y)
    return float(y @ a), a


def h_val(X, y, lam, a, z):
    c = X.T @ a
    return float(2 * a @ y - a @ a - np.sum(z * c * c) / lam)


def topsum(v, m):
    if m <= 0:
        return 0.0
    v = np.sort(np.asarray(v))[::-1]
    return float(v[:m].sum())


def dual_L(X, y, lam, k, a, S0=(), S1=()):
    """L_{S0,S1}(a) of Lemma 1.1."""
    p = X.shape[1]
    c2 = (X.T @ a) ** 2
    S0 = list(S0); S1 = list(S1)
    free = np.ones(p, bool); free[S0] = False; free[S1] = False
    kp = k - len(S1)
    if kp < 0:
        return np.inf
    return float(2 * a @ y - a @ a - (c2[S1].sum() + topsum(c2[free], kp)) / lam)


def node_primal_cvx(X, y, lam, k, S0=(), S1=(), cols=None, solver="CLARABEL"):
    """Perspective (SOC) node relaxation, restricted to columns `cols` (all by default).
    Returns (value, z_full, beta_full, residual). Restriction gives an UPPER bound on r(S0,S1)."""
    n, p = X.shape
    if cols is None:
        cols = np.arange(p)
    cols = np.array(sorted(set(int(c) for c in cols) - set(int(s) for s in S0)), int)
    S1 = [int(s) for s in S1]
    assert all(s in set(cols.tolist()) for s in S1)
    m = len(cols)
    Xc = X[:, cols]
    beta = cp.Variable(m); z = cp.Variable(m); t = cp.Variable(m)
    lo = np.zeros(m); pos = {c: i for i, c in enumerate(cols)}
    for s in S1:
        lo[pos[s]] = 1.0
    cons = [z >= lo, z <= 1, cp.sum(z) <= k,
            cp.SOC(t + z, cp.vstack([2 * beta, t - z]), axis=0)]
    obj = cp.sum_squares(y - Xc @ beta) + lam * cp.sum(t)
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=solver)
    zf = np.zeros(p); zf[cols] = np.clip(z.value, 0, 1)
    bf = np.zeros(p); bf[cols] = beta.value
    return float(prob.value), zf, bf, y - X @ bf


def node_dual_cvx(X, y, lam, k, S0=(), S1=(), solver="CLARABEL"):
    """max_a L_{S0,S1}(a), written with the top-k variational form, solved independently."""
    n, p = X.shape
    S0 = set(int(s) for s in S0); S1 = [int(s) for s in S1]
    F = [i for i in range(p) if i not in S0 and i not in set(S1)]
    kp = k - len(S1)
    a = cp.Variable(n); tt = cp.Variable(); s = cp.Variable(len(F))
    cF = X[:, F].T @ a
    obj = 2 * a @ y - cp.sum_squares(a) - (cp.sum_squares(X[:, S1].T @ a) if S1 else 0) / lam \
        - (kp * tt + cp.sum(s)) / lam
    cons = [s >= 0, s >= cp.square(cF) - tt]
    prob = cp.Problem(cp.Maximize(obj), cons)
    prob.solve(solver=solver)
    return float(prob.value), a.value


def saturated_witness(X, y, lam, S, kappa):
    """Proposition 2.3 witness, built from the definitions."""
    n, p = X.shape
    S = np.asarray(S, int)
    XS = X[:, S]
    Minv = np.linalg.inv(np.eye(n) + XS @ XS.T / lam)
    fS, bS, r = ridge_on(X, y, lam, S)
    a = X.T @ r
    null = np.setdiff1d(np.arange(p), S)
    V = null[np.abs(a[null]) > kappa]
    if len(V) == 0:
        return r, 0.0, V, fS
    XV = X[:, V]
    H = XV.T @ Minv @ XV
    rhs = a[V] - kappa * np.sign(a[V])
    u = np.linalg.solve(H, rhs)
    Gamma = float(rhs @ u)
    alpha = r - Minv @ XV @ u
    return alpha, Gamma, V, fS
