"""Independent helpers for checking Pilanci-Wainwright-El Ghaoui (PWE), Math. Program. 151 (2015),
Theorem 2, in the paper's own notation.

Model (PWE Sect. 3.1): X in R^{n x d} with iid N(0,1) entries, y = X w* + eps, eps iid N(0, gamma^2),
w* k-sparse. Problem (3): P* = min_{||w||_0 <= k} 1/2 ||y - Xw||^2 + 1/2 rho ||w||^2.
Relaxation (19): P_IR = min_{u in [0,1]^d, sum u <= k} y'(X D(u) X'/rho + I)^{-1} y.
(Both are stated without the factor 1/2 below; the factor does not affect exactness.)
M = (I + X_S X_S'/rho)^{-1} as in PWE (20); a_j = X_j' M y.

Written from the paper only; imports nothing from the reviewer's code.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import itertools
import numpy as np
from scipy.special import ndtr

_COMBOS = {}


def instance(n, d, k, b, gamma, seed, noise="entry"):
    """noise='entry': eps iid N(0, gamma^2) (PWE's stated model).
    noise='total': eps iid N(0, gamma^2/n), so E||eps||^2 = gamma^2."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d))
    S = np.sort(rng.choice(d, k, replace=False))
    w = np.zeros(d)
    w[S] = b * rng.choice([-1.0, 1.0], k)
    sd = gamma if noise == "entry" else gamma / np.sqrt(n)
    y = X @ w + sd * rng.standard_normal(n)
    return X, y, S, w


def f_support(X, y, rho, S):
    """y' M_S y via the direct ridge fit (no Gram shortcut): ||y - X_S b||^2 + rho ||b||^2."""
    S = np.asarray(S, int)
    XS = X[:, S]
    beta = np.linalg.solve(rho * np.eye(len(S)) + XS.T @ XS, XS.T @ y)
    r = y - XS @ beta
    return float(r @ r + rho * beta @ beta)


def enumerate_opt(X, y, rho, k, chunk=200000):
    """Exact P* by enumerating all k-subsets (f is nonincreasing in S, so |S| = k suffices).
    Returns (P*, S_opt, second-best value)."""
    d = X.shape[1]
    if (d, k) not in _COMBOS:
        _COMBOS[(d, k)] = np.array(list(itertools.combinations(range(d), k)), dtype=np.int16)
    C = _COMBOS[(d, k)]
    G = X.T @ X
    c = X.T @ y
    yy = float(y @ y)
    I = rho * np.eye(k)
    best = [(np.inf, None), (np.inf, None)]
    for s in range(0, len(C), chunk):
        idx = C[s:s + chunk].astype(np.intp)
        Gs = G[idx[:, :, None], idx[:, None, :]] + I
        cs = c[idx]
        v = yy - np.einsum("ij,ij->i", cs, np.linalg.solve(Gs, cs[..., None])[..., 0])
        two = np.argpartition(v, 1)[:2]
        for t in two:
            best.append((float(v[t]), tuple(int(i) for i in idx[t])))
        best = sorted(best)[:2]
    # recompute the two best directly (guards against Gram-form round-off)
    v1 = f_support(X, y, rho, best[0][1])
    v2 = f_support(X, y, rho, best[1][1])
    if v2 < v1:
        v1, v2 = v2, v1
        best = [best[1], best[0]]
    return v1, np.array(best[0][1]), v2


def cert(X, y, rho, S):
    """PWE Corollary 2 at S: returns (a, min_S |a|, max_{S^c} |a|), a_j = X_j' M y."""
    n, d = X.shape
    S = np.asarray(S, int)
    XS = X[:, S]
    My = y - XS @ np.linalg.solve(rho * np.eye(len(S)) + XS.T @ XS, XS.T @ y)   # M y (PWE p.72 identity)
    a = X.T @ My
    off = np.setdiff1d(np.arange(d), S)
    return a, float(np.min(np.abs(a[S]))), float(np.max(np.abs(a[off]))), My


def G_of_u(X, y, rho, u):
    """G(u) = y'(I + X D(u) X'/rho)^{-1} y and alpha = (I + X D(u) X'/rho)^{-1} y, via the d x d form
    (I + U U')^{-1} = I - U (I + U'U)^{-1} U' with U = X D(u)^{1/2}/sqrt(rho)."""
    s = np.sqrt(np.clip(u, 0, None))
    Xs = X * s
    z = np.linalg.solve(rho * np.eye(len(u)) + Xs.T @ Xs, Xs.T @ y)
    alpha = y - Xs @ z
    return float(y @ alpha), alpha


def dual_value(X, y, rho, k, alpha):
    """Weak-duality lower bound on P_IR: 2 a'y - a'a - (1/rho) * sum of k largest (X_j'a)^2."""
    q = np.sort((X.T @ alpha) ** 2)[::-1]
    return float(2 * alpha @ y - alpha @ alpha - q[:k].sum() / rho)


def project_capped_simplex(v, k):
    """Euclidean projection onto {0 <= u <= 1, sum u <= k}."""
    u = np.clip(v, 0, 1)
    if u.sum() <= k:
        return u
    lo, hi = 0.0, float(np.max(v))
    for _ in range(200):
        tau = 0.5 * (lo + hi)
        if np.clip(v - tau, 0, 1).sum() > k:
            lo = tau
        else:
            hi = tau
    return np.clip(v - hi, 0, 1)


def polish(X, y, rho, k, u, iters=3000):
    """Projected gradient with backtracking on the smooth convex G(u); returns best u and
    the bracket [lower, upper] on P_IR (upper = G(u), lower = dual_value at alpha(u))."""
    Gu, al = G_of_u(X, y, rho, u)
    lo = dual_value(X, y, rho, k, al)
    step = 1.0 / max(1e-12, np.max((X.T @ al) ** 2) / rho)
    for _ in range(iters):
        g = -((X.T @ al) ** 2) / rho
        while True:
            un = project_capped_simplex(u - step * g, k)
            Gn, aln = G_of_u(X, y, rho, un)
            if Gn <= Gu + g @ (un - u) + 0.5 / step * np.sum((un - u) ** 2) + 1e-12 * abs(Gu):
                break
            step *= 0.5
        if np.allclose(un, u, rtol=0, atol=1e-15):
            break
        u, Gu, al = un, Gn, aln
        lo = max(lo, dual_value(X, y, rho, k, al))
        step *= 1.5
    return u, Gu, lo


def relax_cvxpy(X, y, rho, k):
    """P_IR through the perspective form min ||y - Xw||^2 + rho sum_j w_j^2/u_j over the capped
    simplex (equals (19) because the inner minimum over w is the generalized-ridge value)."""
    import cvxpy as cp
    n, d = X.shape
    w = cp.Variable(d)
    u = cp.Variable(d)
    obj = cp.sum_squares(y - X @ w) + rho * cp.sum(cp.hstack([cp.quad_over_lin(w[j], u[j]) for j in range(d)]))
    prob = cp.Problem(cp.Minimize(obj), [u >= 0, u <= 1, cp.sum(u) <= k])
    prob.solve(solver="CLARABEL")
    return float(prob.value), np.clip(u.value, 0, 1)


def swap_certificate(X, y, rho, S, a):
    """If max_{S^c}|a| > min_S |a|, the feasible point u_t = 1_S - t e_j + t e_l (j = weakest in S,
    l = strongest outside) has dG/dt(0) = -(a_l^2 - a_j^2)/rho < 0. Returns min_t G(u_t) over a grid."""
    d = X.shape[1]
    S = np.asarray(S, int)
    off = np.setdiff1d(np.arange(d), S)
    j = S[np.argmin(np.abs(a[S]))]
    l = off[np.argmax(np.abs(a[off]))]
    best = np.inf
    for t in np.concatenate([np.geomspace(1e-4, 0.5, 60), [0.6, 0.7, 0.8, 0.9]]):
        u = np.zeros(d)
        u[S] = 1.0
        u[j] -= t
        u[l] += t
        best = min(best, G_of_u(X, y, rho, u)[0])
    return best


def limit_prob(b, gamma, d, k):
    """n -> infinity limit of P(Corollary 2 certificate at the true support), equal |w*_j| = b."""
    return (1 - 2 * (1 - ndtr(b / gamma))) ** (d - k)
