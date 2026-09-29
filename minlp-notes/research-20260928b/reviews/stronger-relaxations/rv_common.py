"""Independent reviewer implementations (no import from the author's code).

Problem: OPT = min_{|S| <= k} f(S), f(S) = min_b ||y - X_S b||^2 + lam ||b||^2.
Lifted objective Phi(beta, B) = y'y - 2 y'X beta + <X'X + lam I, B>.

Relaxations (node fixings z[S0] = 0, z[S1] = 1, sum z <= k):
  persp : min ||y - X beta||^2 + lam sum t_j, beta_j^2 <= z_j t_j
  sdp1  : [[1, beta'], [beta, B]] >= 0, beta_j^2 <= z_j B_jj
  sdp2  : sdp1 + for pairs T: 0 <= w_T <= min(1, z(T)), [[w_T, beta_T'], [beta_T, B_T]] >= 0
  Lr    : sdp1 + exact lifted hull H_T on every |T| = r (r = 2 or 3), disjunctive form
  zb    : moment matrix in (1, zeta, beta) >= 0, diag Z = z, diag U = beta, McCormick,
          Z 1 <= k z, and U_jm^2 <= Z_jm B_mm (j != m)
"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[_v] = "1"
import itertools
import numpy as np
import cvxpy as cp


def gen_core(n, p, k, b=1.0, sigma=0.5, seed=0, lam=None, tau0=None):
    """Mirror of the parent note's documented generator (RNG call order read from core.instance)."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    if b > 0:
        beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    if lam is None:
        lam = tau0 * sigma * np.sqrt(2 * n * np.log(p)) / b if tau0 is not None else np.sqrt(n)
    return X, y, float(lam), tuple(int(s) for s in S)


def gen_nested(n, k, pmax, p, seed, b=1.0, sigma=0.5):
    """Mirror of the nested design of Section 7.2 (exp_mech.make, read)."""
    rng = np.random.default_rng(seed)
    Xf = rng.standard_normal((n, pmax))
    beta = np.zeros(pmax); beta[:k] = b * rng.choice([-1.0, 1.0], k)
    y = Xf @ beta + sigma * rng.standard_normal(n)
    lam = 1.5 * sigma * np.sqrt(2 * n * np.log(200)) / b
    return Xf[:, :p].copy(), y, float(lam), tuple(range(k))


def fval(X, y, lam, S):
    S = list(S)
    if not S:
        return float(y @ y), np.zeros(0), y.copy()
    XS = X[:, S]
    bS = np.linalg.solve(XS.T @ XS + lam * np.eye(len(S)), XS.T @ y)
    r = y - XS @ bS
    return float(y @ r), bS, r


def opt_enum(X, y, lam, k, S0=(), S1=()):
    """Exact node optimum by enumeration of all supports of size k (f is monotone)."""
    p = X.shape[1]
    free = [j for j in range(p) if j not in set(S0) and j not in set(S1)]
    best, arg = np.inf, None
    for C in itertools.combinations(free, k - len(S1)):
        v = fval(X, y, lam, list(S1) + list(C))[0]
        if v < best:
            best, arg = v, tuple(sorted(list(S1) + list(C)))
    return best, arg


def _solve(prob, solver="CLARABEL"):
    try:
        if solver == "CLARABEL":
            prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10, max_iter=500)
        else:
            prob.solve(solver=cp.SCS, eps=1e-8, max_iters=200000)
    except Exception as e:  # noqa: BLE001
        return None
    if prob.status not in ("optimal", "optimal_inaccurate"):
        return None
    return float(prob.value)


def _zcons(z, k, S0, S1):
    c = [z >= 0, z <= 1, cp.sum(z) <= k]
    if len(S0):
        c.append(z[list(S0)] == 0)
    if len(S1):
        c.append(z[list(S1)] == 1)
    return c


def persp(X, y, lam, k, S0=(), S1=()):
    n, p = X.shape
    beta, z, t = cp.Variable(p), cp.Variable(p), cp.Variable(p)
    cons = _zcons(z, k, S0, S1) + [cp.SOC(z + t, cp.vstack([2 * beta, z - t]), axis=0)]
    return _solve(cp.Problem(cp.Minimize(cp.sum_squares(y - X @ beta) + lam * cp.sum(t)), cons))


def _lift(X, y, lam, k, S0, S1):
    n, p = X.shape
    Q = X.T @ X + lam * np.eye(p)
    M = cp.Variable((p + 1, p + 1), PSD=True)
    beta, B = M[0, 1:], M[1:, 1:]
    z = cp.Variable(p)
    cons = [M[0, 0] == 1] + _zcons(z, k, S0, S1)
    cons.append(cp.SOC(z + cp.diag(B), cp.vstack([2 * beta, z - cp.diag(B)]), axis=0))
    obj = float(y @ y) - 2 * (X.T @ y) @ beta + cp.trace(Q @ B)
    return M, beta, B, z, cons, obj


def sdp1(X, y, lam, k, S0=(), S1=(), fix_z=None, solver="CLARABEL"):
    M, beta, B, z, cons, obj = _lift(X, y, lam, k, S0, S1)
    if fix_z is not None:
        cons.append(z == fix_z)
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def sdp2(X, y, lam, k, S0=(), S1=(), solver="CLARABEL"):
    p = X.shape[1]
    M, beta, B, z, cons, obj = _lift(X, y, lam, k, S0, S1)
    for i, j in itertools.combinations(range(p), 2):
        w = cp.Variable()
        blk = cp.Variable((3, 3), PSD=True)
        cons += [w >= 0, w <= 1, w <= z[i] + z[j], blk[0, 0] == w, blk[0, 1] == beta[i], blk[0, 2] == beta[j],
                 blk[1, 1] == B[i, i], blk[1, 2] == B[i, j], blk[2, 2] == B[j, j]]
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def hull_constraints(zT, bT, BT):
    """Constraints saying (zT, bT, BT) lies in the closed lifted hull H_T (disjunctive form):
    patterns zeta != 0 with blocks [[l, g'], [g, H]] >= 0 on supp zeta; l_0 = 1 - sum l >= 0;
    zT = sum l zeta; bT = sum g; BT - sum H >= 0 (recession)."""
    r = len(zT)
    pats = [pt for pt in itertools.product([0, 1], repeat=r) if any(pt)]
    cons, ls = [], []
    gsum = [0] * r
    Hsum = [[0] * r for _ in range(r)]
    zsum = [0] * r
    for pt in pats:
        s = [i for i in range(r) if pt[i]]
        m = len(s)
        blk = cp.Variable((m + 1, m + 1), PSD=True)
        l = blk[0, 0]
        ls.append(l)
        for a, i in enumerate(s):
            zsum[i] = zsum[i] + l
            gsum[i] = gsum[i] + blk[0, a + 1]
            for c_, j in enumerate(s):
                Hsum[i][j] = Hsum[i][j] + blk[a + 1, c_ + 1]
    cons.append(sum(ls) <= 1)
    for i in range(r):
        cons.append(zT[i] == zsum[i])
        cons.append(bT[i] == gsum[i])
    R = cp.Variable((r, r), PSD=True)
    for i in range(r):
        for j in range(r):
            cons.append(BT[i][j] == Hsum[i][j] + R[i, j])
    return cons


def Lr(X, y, lam, k, r=2, S0=(), S1=(), solver="CLARABEL", sets=None):
    p = X.shape[1]
    M, beta, B, z, cons, obj = _lift(X, y, lam, k, S0, S1)
    T_all = sets if sets is not None else list(itertools.combinations(range(p), r))
    for T in T_all:
        cons += hull_constraints([z[i] for i in T], [beta[i] for i in T], [[B[i, j] for j in T] for i in T])
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def hull_margin(zT, bT, BT):
    """max d such that (zT, bT, BT) is in the hull with all blocks >= d I and l_0 >= d.
    d >= -tol means membership up to tol (d can be positive only for interior points)."""
    r = len(zT)
    pats = [pt for pt in itertools.product([0, 1], repeat=r) if any(pt)]
    d = cp.Variable()
    cons, ls = [], []
    zsum = [0.0] * r; gsum = [0.0] * r; Hsum = [[0.0] * r for _ in range(r)]
    for pt in pats:
        s = [i for i in range(r) if pt[i]]
        m = len(s)
        blk = cp.Variable((m + 1, m + 1), symmetric=True)
        cons.append(blk - d * np.eye(m + 1) >> 0)
        l = blk[0, 0]; ls.append(l)
        for a, i in enumerate(s):
            zsum[i] = zsum[i] + l
            gsum[i] = gsum[i] + blk[0, a + 1]
            for c_, j in enumerate(s):
                Hsum[i][j] = Hsum[i][j] + blk[a + 1, c_ + 1]
    cons.append(1 - sum(ls) >= d)
    R = cp.Variable((r, r), symmetric=True)
    cons.append(R - d * np.eye(r) >> 0)
    for i in range(r):
        cons += [zsum[i] == zT[i], gsum[i] == bT[i]]
        for j in range(r):
            cons.append(Hsum[i][j] + R[i, j] == BT[i][j])
    scale = max(1.0, float(np.max(np.abs(BT))))
    cons.append(d <= 1e-3 * scale)
    pr = cp.Problem(cp.Maximize(d), cons)
    try:
        pr.solve(solver=cp.CLARABEL)
    except Exception:  # noqa: BLE001
        return -np.inf
    return float(d.value) / scale if d.value is not None else -np.inf


def zb(X, y, lam, k, S0=(), S1=(), fix_z=None, product_cones=True, solver="CLARABEL"):
    n, p = X.shape
    Q = X.T @ X + lam * np.eye(p)
    Y = cp.Variable((2 * p + 1, 2 * p + 1), PSD=True)
    z, beta = Y[0, 1:p + 1], Y[0, p + 1:]
    Z, U, B = Y[1:p + 1, 1:p + 1], Y[1:p + 1, p + 1:], Y[p + 1:, p + 1:]
    cons = [Y[0, 0] == 1, cp.diag(Z) == z, cp.diag(U) == beta] + _zcons(z, k, S0, S1)
    for j in range(p):
        for m in range(p):
            if j == m:
                continue
            cons += [Z[j, m] >= 0, Z[j, m] <= z[j], Z[j, m] <= z[m], Z[j, m] >= z[j] + z[m] - 1]
    cons.append(cp.sum(Z, axis=1) <= k * z)
    if product_cones:
        for j in range(p):
            for m in range(p):
                if j != m:
                    cons.append(cp.SOC(Z[j, m] + B[m, m], cp.hstack([2 * U[j, m], Z[j, m] - B[m, m]])))
    if fix_z is not None:
        cons.append(z == fix_z)
    obj = float(y @ y) - 2 * (X.T @ y) @ beta + cp.trace(Q @ B)
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def zb_vec(X, y, lam, k, S0=(), S1=(), fix_z=None, solver="CLARABEL"):
    """Same relaxation as zb(), vectorized constraints (for p ~ 100)."""
    n, p = X.shape
    Q = X.T @ X + lam * np.eye(p)
    Y = cp.Variable((2 * p + 1, 2 * p + 1), PSD=True)
    z, beta = Y[0, 1:p + 1], Y[0, p + 1:]
    Z, U, B = Y[1:p + 1, 1:p + 1], Y[1:p + 1, p + 1:], Y[p + 1:, p + 1:]
    one = np.ones((p, 1))
    zc = cp.reshape(z, (p, 1), order="C")
    cons = [Y[0, 0] == 1, cp.diag(Z) == z, cp.diag(U) == beta] + _zcons(z, k, S0, S1)
    cons += [Z >= 0, Z <= zc @ one.T, Z <= one @ zc.T, Z >= zc @ one.T + one @ zc.T - 1, Z @ np.ones(p) <= k * z]
    J, M = np.nonzero(~np.eye(p, dtype=bool))
    Uv = cp.vec(U, order="C")[J * p + M]
    Zv = cp.vec(Z, order="C")[J * p + M]
    Bm = cp.diag(B)[M]
    cons.append(cp.SOC(Zv + Bm, cp.vstack([2 * Uv, Zv - Bm]), axis=0))
    if fix_z is not None:
        cons.append(z == fix_z)
    obj = float(y @ y) - 2 * (X.T @ y) @ beta + cp.trace(Q @ B)
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)
