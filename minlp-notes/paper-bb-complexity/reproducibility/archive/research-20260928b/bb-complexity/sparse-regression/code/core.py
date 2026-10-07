"""Core routines for perspective-relaxation B&B in L0-constrained ridge regression.

Problem:  OPT = min_{|S|<=k} f(S),  f(S) = min_b ||y - X_S b||^2 + lam ||b||^2
                                        = y^T (I + X_S X_S^T/lam)^{-1} y.
Relaxation at node (S0 fixed 0, S1 fixed 1):
    r(S0,S1) = min { g(z) : z in [0,1]^p, sum z <= k, z_S0 = 0, z_S1 = 1 },
    g(z) = y^T (I + X diag(z) X^T / lam)^{-1} y
         = max_a  2 a^T y - ||a||^2 - (1/lam) sum_i z_i (x_i^T a)^2 .
Dual bound: for ANY a in R^n,
    r(S0,S1) >= L(a) = 2a^T y - ||a||^2 - (1/lam)[ sum_{S1} c_i^2 + top_{k-|S1|}(c_F^2) ],
    c = X^T a.  (weak duality; exact at the optimal a)
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
import scipy.sparse as sp


def ridge(X, y, lam, S):
    """Return (f(S), beta_S, residual r_S) for ridge on support S."""
    S = list(S)
    if len(S) == 0:
        return float(y @ y), np.zeros(0), y.copy()
    XS = X[:, S]
    b = np.linalg.solve(XS.T @ XS + lam * np.eye(len(S)), XS.T @ y)
    r = y - XS @ b
    return float(y @ r), b, r


def topsum(v, m):
    if m <= 0:
        return 0.0
    if m >= len(v):
        return float(np.sum(v))
    return float(np.sum(np.partition(v, len(v) - m)[len(v) - m:]))


def dual_bound(X, y, lam, k, a, S0=(), S1=()):
    """L(a) at node (S0,S1): valid lower bound on the node relaxation."""
    c2 = (X.T @ a) ** 2
    p = X.shape[1]
    free = np.ones(p, bool); free[list(S0)] = False; free[list(S1)] = False
    kp = k - len(S1)
    if kp < 0:
        return np.inf
    return float(2 * a @ y - a @ a - (c2[list(S1)].sum() + topsum(c2[free], kp)) / lam)


def g_val(X, y, lam, z):
    P = np.nonzero(z > 0)[0]
    n = X.shape[0]
    if len(P) == 0:
        return float(y @ y), y.copy()
    XP = X[:, P]
    # use the p-side formula when |P| < n
    M = XP.T @ XP + lam * np.diag(1.0 / z[P])
    b = np.linalg.solve(M, XP.T @ y)
    a = y - XP @ b
    return float(y @ a), a


def solve_node(X, y, lam, k, S0=(), S1=(), tol=1e-10):
    """Solve node relaxation by Clarabel (residual form). Returns (LB, val, z, a)
    LB is the dual bound L(a) at the recovered a (valid lower bound)."""
    import clarabel
    n, p = X.shape
    S0s = set(S0); S1 = list(S1); S1s = set(S1)
    kp = k - len(S1)
    if kp < 0:
        return np.inf, np.inf, None, None
    F = [i for i in range(p) if i not in S0s and i not in S1s]
    nf = len(F); n1 = len(S1)
    z = np.zeros(p); z[S1] = 1.0
    if nf <= kp or kp == 0:
        if kp > 0:
            z[F] = 1.0
        v, a = g_val(X, y, lam, z)
        return v, v, z, a
    # variables: rho (n), b1 (n1), bF (nf), t (nf), zf (nf)
    N = n + n1 + 3 * nf
    o_b1, o_bF, o_t, o_z = n, n + n1, n + n1 + nf, n + n1 + 2 * nf
    Pd = np.zeros(N); Pd[:n] = 2.0; Pd[o_b1:o_b1 + n1] = 2.0 * lam
    P = sp.diags(Pd).tocsc()
    q = np.zeros(N); q[o_t:o_t + nf] = lam
    rows, cols, vals = [], [], []
    # equality: rho + X_{S1} b1 + X_F bF = y   (n rows, zero cone)
    I = np.arange(n)
    rows += list(I); cols += list(I); vals += [1.0] * n
    XA = X[:, S1 + F]
    rr, cc = np.meshgrid(np.arange(n), np.arange(n1 + nf), indexing="ij")
    rows += list(rr.ravel()); cols += list((cc + n).ravel()); vals += list(XA.ravel())
    b_eq = y.copy()
    r0 = n
    jj = np.arange(nf)
    # nonneg: -z <= 0 ; z <= 1 ; sum z <= kp
    rows += list(r0 + jj); cols += list(o_z + jj); vals += [-1.0] * nf
    rows += list(r0 + nf + jj); cols += list(o_z + jj); vals += [1.0] * nf
    rows += [r0 + 2 * nf] * nf; cols += list(o_z + jj); vals += [1.0] * nf
    b_nn = np.concatenate([np.zeros(nf), np.ones(nf), [kp]])
    r1 = r0 + 2 * nf + 1
    # SOC: (t+z, 2b, t-z) in SOC3 ; s = b - A x  => A = -(...)
    for m in range(nf):
        base = r1 + 3 * m
        rows += [base, base, base + 1, base + 2, base + 2]
        cols += [o_t + m, o_z + m, o_bF + m, o_t + m, o_z + m]
        vals += [-1.0, -1.0, -2.0, -1.0, 1.0]
    A = sp.csc_matrix((vals, (rows, cols)), shape=(r1 + 3 * nf, N))
    bvec = np.concatenate([b_eq, b_nn, np.zeros(3 * nf)])
    cones = [clarabel.ZeroConeT(n), clarabel.NonnegativeConeT(2 * nf + 1)] + [clarabel.SecondOrderConeT(3)] * nf
    s = clarabel.DefaultSettings(); s.verbose = False
    s.tol_gap_abs = tol; s.tol_gap_rel = tol; s.tol_feas = tol
    sol = clarabel.DefaultSolver(sp.triu(P).tocsc(), q, A, bvec, cones, s).solve()
    x = np.array(sol.x)
    z[F] = np.clip(x[o_z:o_z + nf], 0.0, 1.0)
    # dual vector a = residual at the relaxed optimum (rho)
    a = x[:n].copy()
    LB = dual_bound(X, y, lam, k, a, S0, S1)
    # also evaluate primal value at z (upper bound on node value)
    val, a2 = g_val(X, y, lam, z)
    LB = max(LB, dual_bound(X, y, lam, k, a2, S0, S1))
    return LB, val, z, a2


def instance(n, p, k, b=1.0, sigma=0.5, seed=0, lam=None, tau0=None, signs=True):
    """Gaussian design, k-sparse beta* with entries +-b on random support.
    lam: explicit, or tau0 * sigma * sqrt(2 n log p)/b if tau0 given, else sqrt(n)."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    if b > 0:
        beta[S] = b * (rng.choice([-1.0, 1.0], k) if signs else 1.0)
    y = X @ beta + sigma * rng.standard_normal(n)
    if lam is None:
        lam = tau0 * sigma * np.sqrt(2 * n * np.log(p)) / b if tau0 is not None else np.sqrt(n)
    return X, y, float(lam), tuple(S.tolist())


def solve_node_cg(X, y, lam, k, S0=(), S1=(), init=(), target=None, tol=1e-9, maxrounds=60, add=20):
    """Exact node relaxation by column generation.
    Restricted problem on candidate set C (other free vars fixed to 0); the dual bound
    L(a) is evaluated on the FULL node, so it is always valid.  Stops when
    (i) L >= target (certified prune), or (ii) restricted value - L <= tol*max(1,|val|).
    Returns (LB, val_restricted, z, a, rounds)."""
    n, p = X.shape
    S0s = set(S0); S1s = set(S1)
    kp = k - len(S1)
    if kp < 0:
        return np.inf, np.inf, None, None, 0
    free = np.array([i not in S0s and i not in S1s for i in range(p)])
    C = set(i for i in init if free[i])
    # seed with top correlations to y
    c0 = np.abs(X.T @ y); c0[~free] = -1
    for i in np.argsort(-c0)[:max(2 * kp, 10)]:
        if free[i]:
            C.add(int(i))
    best_LB = -np.inf
    for rnd in range(maxrounds):
        Cl = sorted(C)
        S0r = [i for i in range(p) if free[i] and i not in C] + list(S0)
        # solve restricted: pass reduced matrix
        idx = list(S1) + Cl
        Xr = X[:, idx]
        LBr, val, zr, a = solve_node(Xr, y, lam, k, (), tuple(range(len(S1))))
        LB = dual_bound(X, y, lam, k, a, S0, S1)
        best_LB = max(best_LB, LB)
        z = np.zeros(p); z[idx] = zr
        if target is not None and best_LB >= target:
            return best_LB, val, z, a, rnd + 1
        if val - best_LB <= tol * max(1.0, abs(val)):
            return best_LB, val, z, a, rnd + 1
        # add free columns outside C with the largest c^2
        c2 = (X.T @ a) ** 2
        c2[~free] = -1; c2[list(C)] = -1
        cand = np.argsort(-c2)[:add]
        newc = [int(i) for i in cand if c2[i] > 0]
        if not newc:
            return best_LB, val, z, a, rnd + 1
        C.update(newc)
    return best_LB, val, z, a, maxrounds


def single_fixing_bounds(X, y, lam, k, S, alpha):
    """Exact dual bounds L(alpha) for all single wrong fixings relative to support S.
    Returns (rem[i in S], frc[j notin S]) as arrays (same order as sorted S / sorted nonS)."""
    c2 = (X.T @ alpha) ** 2
    base = float(2 * alpha @ y - alpha @ alpha)
    p = X.shape[1]
    S = sorted(S); Ss = set(S)
    order = np.argsort(-c2)[:k + 2]
    rem = np.array([base - sum([c2[j] for j in order if j != i][:k]) / lam for i in S])
    nonS = np.array([j for j in range(p) if j not in Ss])
    topk1 = [c2[m] for m in order]
    frc = np.empty(len(nonS))
    for t, j in enumerate(nonS):
        vals = [c2[m] for m in order if m != j][:k - 1]
        frc[t] = base - (c2[j] + sum(vals)) / lam
    return rem, frc


def saturated_witness(X, y, lam, S, kappa):
    """Dual vector alpha = r - M_S^{-1} X_V H^{-1}(a_V - kappa sign a_V), V = {l notin S: |a_l|>kappa}.
    Returns (alpha, info dict with D=u^T H u, |V|, m=min_S|c|, M=max_nonS|c|)."""
    n, p = X.shape
    S = sorted(S)
    XS = X[:, S]
    G = XS.T @ XS
    fS, bS, r = ridge(X, y, lam, S)
    a = X.T @ r
    nonS = np.array([j for j in range(p) if j not in set(S)])
    V = nonS[np.abs(a[nonS]) > kappa]
    if len(V) == 0:
        alpha = r; D = 0.0
    else:
        XV = X[:, V]
        MinvXV = XV - XS @ np.linalg.solve(lam * np.eye(len(S)) + G, XS.T @ XV)
        H = XV.T @ MinvXV
        rhs = a[V] - kappa * np.sign(a[V])
        u = np.linalg.solve(H, rhs)
        D = float(rhs @ u)
        alpha = r - MinvXV @ u
    c = np.abs(X.T @ alpha)
    info = dict(D=D, nV=len(V), m=float(c[S].min()), M=float(c[nonS].max()), fS=fS,
                lam_bmin=float(lam * np.abs(bS).min()))
    return alpha, info


def best_saturated(X, y, lam, k, S, grid=None):
    """Try a grid of kappa (as fractions of lam*min|beta_S|); return best min margin and details."""
    fS, bS, r = ridge(X, y, lam, S)
    base = lam * np.abs(bS).min()
    if grid is None:
        grid = np.linspace(0.5, 1.0, 26)
    best = (-np.inf, None, None)
    for th in grid:
        alpha, info = saturated_witness(X, y, lam, S, th * base)
        rem, frc = single_fixing_bounds(X, y, lam, k, S, alpha)
        marg = min(rem.min(), frc.min()) - fS
        if marg > best[0]:
            best = (marg, th, info)
    return best



def all_single_bounds(X, y, lam, k, a, S, nulls):
    """Vectorized L(a) (Lemma 1.1) for every removal node ({i},{}) , i in S, and every
    forced-in node ({},{j}), j in nulls.  Returns (rem, frc)."""
    c2 = (X.T @ a) ** 2
    B = float(2 * a @ y - a @ a)
    order = np.argsort(-c2)
    rank = np.empty(len(c2), int); rank[order] = np.arange(len(c2))
    cs = np.concatenate([[0.0], np.cumsum(c2[order])])
    S = np.asarray(S); nulls = np.asarray(nulls)
    # removal of i: top_k over [p]\{i}
    rem = B - np.where(rank[S] >= k, cs[k], cs[k + 1] - c2[S]) / lam
    # forced-in j: c_j^2 + top_{k-1} over [p]\{j}
    frc = B - (c2[nulls] + np.where(rank[nulls] >= k - 1, cs[k - 1], cs[k] - c2[nulls])) / lam
    return rem, frc


def decide_c1_exact(X, y, lam, k, S, tol_fail=1e-7, tol_pass=1e-9, max_solves=5000):
    """Exact decision of C1 at S (no cap).  Lower bounds: max over a pool of dual vectors of L(a),
    evaluated on every single-fixing node; the pool starts with r_S, saturated witnesses and the root
    residual, and grows by the residual of every node solved.  The weakest undecided node is solved by
    column generation (solve_node_cg): restricted primal value < f(S)(1-tol_fail) => C1 fails (certain);
    certified dual bound >= f(S)(1+tol_pass) => node passes; converged within tolerance => 'passtol'.
    Returns dict(status, solved, notes, root_gap, fail_node) with status
      'C1'          every single fixing strictly above f(S) (strict C1; S is the unique optimum),
      'C1-nonstrict' all pass but some node equals f(S) within tolerance (C1 with eps >= tolerance;
                     uniqueness of S not certified),
      'fail'        some single-fixing node has a feasible point below f(S)(1 - tol_fail),
      'undecided'   a node could not be decided, or max_solves was exhausted."""
    n, p = X.shape
    S = np.array(sorted(S)); Ss = set(S.tolist())
    nulls = np.array([j for j in range(p) if j not in Ss])
    fS, bS, r = ridge(X, y, lam, list(S))
    m0 = lam * np.abs(bS).min()
    rem = np.full(len(S), -np.inf); frc = np.full(len(nulls), -np.inf)
    def absorb(a):
        rr, ff = all_single_bounds(X, y, lam, k, a, S, nulls)
        np.maximum(rem, rr, out=rem); np.maximum(frc, ff, out=frc)
    absorb(r)
    for th in np.linspace(0.5, 1.0, 11):
        al, info = saturated_witness(X, y, lam, list(S), th * m0)
        if info['nV'] <= n - k - 1:
            absorb(al)
    LBr, vr, zr, ar, _ = solve_node_cg(X, y, lam, k, init=tuple(S), maxrounds=200, add=40)
    absorb(ar)
    init = tuple(S) + tuple(np.nonzero(zr > 1e-6)[0])
    solved = 0; notes = []; status = 'C1'; fail_node = None
    thr_pass = fS * (1 + tol_pass)
    while solved < max_solves:
        allb = np.concatenate([rem, frc])
        idx = int(np.argmin(allb))
        if allb[idx] >= thr_pass:
            break
        node = ((int(S[idx]),), ()) if idx < len(S) else ((), (int(nulls[idx - len(S)]),))
        LB, val, z, a, rounds = solve_node_cg(X, y, lam, k, node[0], node[1], init=init,
                                              target=thr_pass, maxrounds=200, add=40)
        solved += 1
        absorb(a)
        if val < fS * (1 - tol_fail):
            status = 'fail'; fail_node = dict(S0=node[0], S1=node[1], value=float(val), fS=float(fS)); break
        if LB >= thr_pass:
            pass
        elif val - LB <= 1e-8 * max(1.0, abs(val)):
            notes.append('passtol')           # node value = f(S) up to tolerance
        else:
            notes.append('undecided'); status = 'undecided'
        if idx < len(S): rem[idx] = np.inf
        else: frc[idx - len(S)] = np.inf
    else:
        status = 'undecided'; notes.append('max_solves exhausted')
    if status == 'C1' and 'passtol' in notes:
        status = 'C1-nonstrict'
    return dict(status=status, solved=solved, notes=notes, root_gap=float(fS - LBr), fS=float(fS),
                fail_node=fail_node, tau2=float((m0 / np.linalg.norm(r)) ** 2))
