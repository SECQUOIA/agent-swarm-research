r"""Certified upper bounds on node values of the lifted relaxations L_1 (= optimal perspective = sdp_1)
and L_2 (exact pairwise lifted hull; dominates Atamturk-Gomez sdp_2 and all 2x2 convexifications),
from the null-space completion of Lemma 4.2 / Corollary 4.3 of thresholds.md.

Given a perspective-feasible point (z, beta) of a node, with F = supp z and helper set Z1 = [p] \ F:
    L_1(node) <= P(z, beta) + lam * theta * pi,
    L_2(node) <= P(z, beta) + lam * pi * min_sigma [ sigma + (1+sigma) theta (1 + 1/(sigma (1 - q_max))) ],
where P(z, beta) = ||y - X beta||^2 + lam sum_j beta_j^2 / z_j (perspective objective),
pi = sum_j beta_j^2 (1/z_j - 1), W = X_Z1 X_Z1', theta = ||X_F' W^{-1} X_F||, q_max = max_{m in Z1} x_m' W^{-1} x_m.
Also the Proposition 4.1 bound for L_1: P + lam * delta * pi with delta = max_i x_i'(I + X_{-i} X_{-i}'/lam)^{-1} x_i / lam.
(z, beta) is the perspective node optimum (so P(z, beta) is the perspective node value).
"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ.setdefault(_v, "1")
import numpy as np
from relax import instance, ridge, solve_node
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "code"))
from core import solve_node_cg


def persp_point(X, y, lam, k, S0=(), S1=(), zmin=1e-9, init=()):
    """Perspective node optimum: returns (LB, z_clean, beta, P(z_clean, beta))."""
    p = X.shape[1]
    if p > 800:
        LB, val, z, a, _ = solve_node_cg(X, y, lam, k, S0, S1, init=init, tol=1e-10, maxrounds=200)
    else:
        LB, val, z, a = solve_node(X, y, lam, k, S0, S1, tol=1e-10)
    z = np.where(z > zmin, np.minimum(z, 1.0), 0.0)
    z[list(S1)] = 1.0
    F = np.nonzero(z > 0)[0]
    XF = X[:, F]
    bF = np.linalg.solve(XF.T @ XF + lam * np.diag(1.0 / z[F]), XF.T @ y)
    beta = np.zeros(p); beta[F] = bF
    P = float(np.sum((y - XF @ bF) ** 2) + lam * np.sum(bF ** 2 / z[F]))
    return LB, z, beta, P


def eps2(theta, qmax):
    if not (np.isfinite(theta) and 0 <= qmax < 1):
        return np.inf
    s = np.sqrt(theta * (1 + theta) / (1 - qmax)) if theta > 0 else 0.0
    grid = np.concatenate([[s], s * np.logspace(-1, 1, 41)]) if s > 0 else [0.0]
    vals = [sg + (1 + sg) * theta * (1 + 1 / (sg * (1 - qmax))) for sg in grid if sg > 0]
    return min(vals) if vals else 0.0


def delta_opt_persp(X, lam):
    """delta = max_i x_i'(I + X_{-i}X_{-i}'/lam)^{-1} x_i / lam  (Proposition 4.1)."""
    n, p = X.shape
    M = np.eye(n) + X @ X.T / lam
    Minv = np.linalg.inv(M)
    # x_i'(M - x_i x_i'/lam)^{-1} x_i = q/(1 - q/lam) with q = x_i' M^{-1} x_i
    q = np.einsum('ij,ij->j', X, Minv @ X)
    return float(np.max(q / (1 - q / lam)) / lam)


def bounds_at(X, y, lam, z, beta, P, delta=None):
    F = np.nonzero(z > 0)[0]
    Z1 = np.setdiff1d(np.arange(X.shape[1]), F)
    pi = float(np.sum(beta[F] ** 2 * (1 / z[F] - 1)))
    W = X[:, Z1] @ X[:, Z1].T
    Winv = np.linalg.inv(W)
    XF = X[:, F]
    theta = float(np.linalg.eigvalsh(XF.T @ Winv @ XF).max())
    qmax = float(np.max(np.einsum('ij,ij->j', X[:, Z1], Winv @ X[:, Z1])))
    e2 = eps2(theta, qmax)
    e1 = theta if delta is None else min(theta, delta)
    return dict(P=P, pi=pi, lam_pi=lam * pi, theta=theta, qmax=qmax, eps1=e1, eps2=e2,
                L1_ub=P + lam * pi * e1, L2_ub=P + lam * pi * e2, nF=len(F))


def node_bounds(X, y, lam, k, S0=(), S1=(), delta=None, init=()):
    LB, z, beta, P = persp_point(X, y, lam, k, S0, S1, init=init)
    d = bounds_at(X, y, lam, z, beta, P, delta)
    d['persp_LB'] = LB
    return d


def inflated_value(X, y, lam, F, z, eps):
    """g_eps(z) = min_beta ||y - X_F beta||^2 + sum_j c_j beta_j^2, c_j = lam + lam (1+eps)(1/z_j - 1),
    on the coordinates of F with z_j > 0 (closed form)."""
    z = np.asarray(z, float)
    nz = z > 1e-12
    if not nz.any():
        return float(y @ y)
    XF = X[:, np.asarray(F)[nz]]
    c = lam + lam * (1 + eps) * (1 / z[nz] - 1)
    bF = np.linalg.solve(XF.T @ XF + np.diag(c), XF.T @ y)
    return float(np.sum((y - XF @ bF) ** 2) + np.sum(c * bF ** 2))


def inflated_persp(X, y, lam, k, F, eps, S0=(), S1=()):
    """Upper bound: min over z in K(node) with supp z in F of g_eps(z) (local search; every z is valid).
    Starts from the perspective optimum restricted to F and from indicator points."""
    from scipy.optimize import minimize
    F = list(F)
    pos = {j: s for s, j in enumerate(F)}
    fixed1 = [pos[j] for j in S1]
    fixed0 = [pos[j] for j in S0 if j in pos]
    free = [s for s in range(len(F)) if s not in fixed1 and s not in fixed0]
    kk = k - len(fixed1)

    def full(zf):
        z = np.zeros(len(F)); z[fixed1] = 1.0; z[free] = np.clip(zf, 0, 1)
        return z

    def fun(zf):
        return inflated_value(X, y, lam, F, full(zf), eps)

    starts = []
    try:
        LB, val, zr, a = solve_node(X[:, F], y, lam, k, tuple(fixed0), tuple(fixed1), tol=1e-10)
        starts.append(np.clip(zr[free], 1e-3, 1))
    except Exception:
        pass
    z0 = np.full(len(free), min(1.0, kk / max(1, len(free)))); starts.append(z0)
    best = np.inf
    cons = [{'type': 'ineq', 'fun': lambda zf: kk - np.sum(zf)}]
    for st in starts:
        st = st * min(1.0, kk / max(st.sum(), 1e-12))
        res = minimize(fun, st, method='SLSQP', bounds=[(1e-6, 1.0)] * len(free), constraints=cons,
                       options=dict(maxiter=500, ftol=1e-12))
        zf = np.clip(res.x, 1e-6, 1.0)
        if zf.sum() > kk:
            zf = zf * kk / zf.sum()
        best = min(best, fun(zf))
    return best


def F_eps(X, F):
    """theta_F, q_max for helper set Z1 = [p] minus F, and the L_2 inflation eps2."""
    Z1 = np.setdiff1d(np.arange(X.shape[1]), np.array(sorted(F)))
    n = X.shape[0]
    if len(Z1) < n + 1:
        return np.inf, np.inf, np.inf          # helper set too small: W singular, no bound
    W = X[:, Z1] @ X[:, Z1].T
    if np.linalg.eigvalsh(W).min() <= 1e-8 * np.trace(W):
        return np.inf, np.inf, np.inf
    Winv = np.linalg.inv(W)
    XF = X[:, sorted(F)]
    theta = float(np.linalg.eigvalsh(XF.T @ Winv @ XF).max())
    qmax = float(np.max(np.einsum('ij,ij->j', X[:, Z1], Winv @ X[:, Z1])))
    return theta, qmax, eps2(theta, qmax)


def best_small_F_bound(X, y, lam, k, S, cand, hs=(1, 2, 3, 5, 8, 12), S0=(), S1=(), delta=None):
    """Certified upper bounds on the L_1 and L_2 node values from supports F = S u S1 u cand[:h]."""
    best1, best2, info = np.inf, np.inf, None
    for h in hs:
        F = sorted(set(S) | set(S1) | set(cand[:h]))
        theta, qmax, e2 = F_eps(X, F)
        e1 = theta if delta is None else min(theta, delta)
        v1 = inflated_persp(X, y, lam, k, F, e1, S0, S1) if np.isfinite(e1) else None
        v2 = inflated_persp(X, y, lam, k, F, e2, S0, S1) if np.isfinite(e2) else None
        if v1 is not None and v1 < best1: best1 = v1
        if v2 is not None and v2 < best2: best2, info = v2, dict(h=h, theta=theta, qmax=qmax, eps2=e2)
    return best1, best2, info
