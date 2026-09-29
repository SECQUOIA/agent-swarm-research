"""Independent re-check code for phase-transition.md (sparse regression), written for this recheck.

Nothing is imported from the author's code/ or from the earlier reviewers' scripts.
Only the instance generator mirrors the author's documented generator (same RNG call order), so
that the stored seeds can be re-decided; the stored f(S*) values are compared to confirm the match.

Model: y = X beta* + sigma w, f(S) = min_b ||y - X_S b||^2 + lam ||b||^2 = y'(I + X_S X_S'/lam)^{-1} y.
Node relaxation r(S0,S1) = min{ g(z) : z in [0,1]^p, sum z <= k, z_S0 = 0, z_S1 = 1 },
g(z) = y'(I + X diag(z) X'/lam)^{-1} y.
Certificates used here (both checked by own closed-form evaluation, independent of any solver):
  * lower bound:  for any a,  r(S0,S1) >= 2a'y - a'a - (1/lam)[sum_{S1} c_i^2 + top_{k-|S1|}(c_F^2)],  c = X'a;
  * upper bound:  g(z) at a feasible z (closed form, n-side).
"""
import os
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[v] = "1"
import numpy as np


def make_instance(n, p, k, seed, rule, b=1.0, sigma=0.5):
    """Mirror of the note's generator: default_rng(seed); X; support; signs; noise; ridge rule."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    if b > 0:
        beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    if rule == 'sqrtn':
        lam = np.sqrt(n)
    else:
        lam = float(rule) * sigma * np.sqrt(2 * n * np.log(p)) / b
    return X, y, float(lam), [int(s) for s in S]


def fit(X, y, lam, S):
    """f(S), coefficients, residual r_S = M_S^{-1} y (p-side normal equations)."""
    XS = X[:, S]
    beta = np.linalg.solve(XS.T @ XS + lam * np.eye(len(S)), XS.T @ y)
    r = y - XS @ beta
    return float(y @ r), beta, r


def g_and_a(X, y, lam, z):
    """g(z) and its maximizing dual vector a(z) = M_z^{-1} y (n-side, stable for tiny z_i)."""
    P = np.nonzero(z > 0)[0]
    n = X.shape[0]
    if len(P) == 0:
        return float(y @ y), y.copy()
    XP = X[:, P] * np.sqrt(z[P] / lam)
    M = np.eye(n) + XP @ XP.T
    a = np.linalg.solve(M, y)
    return float(y @ a), a


def node_lb(X, y, lam, k, a, S0=(), S1=()):
    """Weak-duality lower bound on r(S0,S1) at dual vector a (full node, all p variables)."""
    c2 = (X.T @ a) ** 2
    m = k - len(S1)
    free = np.ones(len(c2), bool)
    free[list(S0)] = False
    free[list(S1)] = False
    cf = np.sort(c2[free])[::-1]
    return float(2 * a @ y - a @ a - (c2[list(S1)].sum() + cf[:m].sum()) / lam)


def single_fixing_lbs(X, y, lam, k, a, S, nulls):
    """Lower bounds at a for every removal node ({i},{}) (i in S) and forced-in node ({},{j}) (j in nulls).
    Removal of i: top_k over [p]\\{i}.  Forced-in j: c_j^2 + top_{k-1} over [p]\\{j}."""
    c2 = (X.T @ a) ** 2
    base = float(2 * a @ y - a @ a)
    desc = np.sort(c2)[::-1]
    csum = np.concatenate([[0.0], np.cumsum(desc)])
    thr_k = desc[k - 1]          # k-th largest value
    thr_k1 = desc[k - 2] if k >= 2 else np.inf   # (k-1)-th largest value
    S = np.asarray(S)
    nulls = np.asarray(nulls)
    # removal: if c2_i is among the top k (c2_i >= k-th largest), drop it and take the (k+1)-th
    ci = c2[S]
    top_wo_i = np.where(ci >= thr_k, csum[k + 1] - ci, csum[k])
    rem = base - top_wo_i / lam
    cj = c2[nulls]
    top_wo_j = np.where(cj >= thr_k1, csum[k] - cj, csum[k - 1])
    frc = base - (cj + top_wo_j) / lam
    return rem, frc


def solve_restricted(X, y, lam, k, W, S1):
    """min g(z) over z supported on W (S1 subset of W fixed to 1), perspective SOCP via cvxpy/Clarabel.
    Returns a feasible z (full length) after clipping/rescaling."""
    import cvxpy as cp
    n, p = X.shape
    W = list(W)
    XW = X[:, W]
    m = len(W)
    beta = cp.Variable(m)
    z = cp.Variable(m)
    t = cp.Variable(m)
    fixed = np.array([w in set(S1) for w in W])
    cons = [z >= 0, z <= 1, cp.sum(z) <= k,
            cp.SOC(t + z, cp.vstack([2 * beta, t - z]), axis=0)]
    if fixed.any():
        cons.append(z[np.nonzero(fixed)[0]] == 1)
    obj = cp.Minimize(cp.sum_squares(y - XW @ beta) + lam * cp.sum(t))
    prob = cp.Problem(obj, cons)
    try:
        prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    except Exception:
        prob.solve(solver=cp.CLARABEL)
    zz = np.clip(np.asarray(z.value).ravel(), 0.0, 1.0)
    zz[fixed] = 1.0
    free = ~fixed
    budget = k - fixed.sum()
    if zz[free].sum() > budget:
        zz[free] *= budget / zz[free].sum()
    zfull = np.zeros(p)
    zfull[W] = zz
    resid = y - XW @ np.asarray(beta.value).ravel()     # solver's residual = candidate dual vector
    return zfull, resid


def solve_node(X, y, lam, k, S0=(), S1=(), W0=(), target=None, maxrounds=100, add=40, tol=1e-9, fail_below=None):
    """Column generation for r(S0,S1).  Returns dict(lb, ub, z, a, rounds, status):
    lb = certified lower bound (full node), ub = g(z) of a feasible z.  Stops at lb >= target,
    ub < fail_below, or ub - lb <= tol*ub."""
    n, p = X.shape
    free = np.ones(p, bool)
    free[list(S0)] = False
    free[list(S1)] = False
    W = set(int(i) for i in W0 if free[i]) | set(int(i) for i in S1)
    c0 = np.abs(X.T @ y)
    c0[~free] = -1
    for i in np.argsort(-c0)[:max(2 * k, 20)]:
        W.add(int(i))
    best_lb, best_ub, best_z, best_a = -np.inf, np.inf, None, None
    for rnd in range(1, maxrounds + 1):
        z, resid = solve_restricted(X, y, lam, k, sorted(W), S1)
        ub, a = g_and_a(X, y, lam, z)
        lb = node_lb(X, y, lam, k, a, S0, S1)
        lb2 = node_lb(X, y, lam, k, resid, S0, S1)
        if lb2 > lb:
            lb, a = lb2, resid
        if ub < best_ub:
            best_ub, best_z = ub, z
        if lb > best_lb:
            best_lb, best_a = lb, a
        if target is not None and best_lb >= target:
            return dict(lb=best_lb, ub=best_ub, z=best_z, a=best_a, rounds=rnd, status='above_target')
        if fail_below is not None and best_ub < fail_below:
            return dict(lb=best_lb, ub=best_ub, z=best_z, a=best_a, rounds=rnd, status='below')
        if best_ub - best_lb <= tol * abs(best_ub):
            return dict(lb=best_lb, ub=best_ub, z=best_z, a=best_a, rounds=rnd, status='converged')
        c2 = (X.T @ a) ** 2
        c2[~free] = -1
        c2[sorted(W)] = -1
        new = [int(i) for i in np.argsort(-c2)[:add] if c2[i] > 0]
        if not new:
            return dict(lb=best_lb, ub=best_ub, z=best_z, a=best_a, rounds=rnd, status='stalled')
        W.update(new)
    return dict(lb=best_lb, ub=best_ub, z=best_z, a=best_a, rounds=maxrounds, status='maxrounds')


def node_value_dual_socp(X, y, lam, k, S0=(), S1=()):
    """Independent formulation: solve the full (unrestricted) dual
    max_a 2a'y - a'a - (1/lam)[sum_{S1} c_i^2 + m t + sum_F u_i],  u_i >= c_i^2 - t, u >= 0,
    (the variational form of top_m).  Returns (dual optimal value reported by solver, certified lb at a)."""
    import cvxpy as cp
    n, p = X.shape
    m = k - len(S1)
    F = [i for i in range(p) if i not in set(S0) and i not in set(S1)]
    a = cp.Variable(n)
    t = cp.Variable()
    u = cp.Variable(len(F))
    cF = X[:, F].T @ a
    obj = 2 * y @ a - cp.sum_squares(a) - (m * t + cp.sum(u)) / lam
    if len(S1):
        obj = obj - cp.sum_squares(X[:, list(S1)].T @ a) / lam
    cons = [u >= 0, cp.square(cF) - t <= u]
    prob = cp.Problem(cp.Maximize(obj), cons)
    prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
    av = np.asarray(a.value).ravel()
    return float(prob.value), node_lb(X, y, lam, k, av, S0, S1), av


def decide_c1(X, y, lam, k, S, tol_fail=1e-7, tol_pass=1e-9, max_solves=3000, verbose=False):
    """Exact decision of C1 at S.  Pool of dual vectors -> lower bounds on all single fixings;
    the weakest undecided node is solved by column generation (its best dual vector joins the pool).
    'fail' is certified by a feasible z with g(z) < f(S)(1 - tol_fail); 'C1' by lower bounds
    >= f(S)(1 + tol_pass) on every single fixing (strict C1, so S is the unique optimum)."""
    n, p = X.shape
    S = sorted(S)
    Ss = set(S)
    nulls = np.array([j for j in range(p) if j not in Ss])
    fS, bS, r = fit(X, y, lam, S)
    thr = fS * (1 + tol_pass)
    low = fS * (1 - tol_fail)
    rem = np.full(len(S), -np.inf)
    frc = np.full(len(nulls), -np.inf)

    def absorb(a):
        rr, ff = single_fixing_lbs(X, y, lam, k, a, S, nulls)
        np.maximum(rem, rr, out=rem)
        np.maximum(frc, ff, out=frc)

    absorb(r)
    root = solve_node(X, y, lam, k, W0=S)
    absorb(root['a'])
    W0 = set(S) | set(np.nonzero(root['z'] > 1e-7)[0].tolist())
    solved = 0
    undecided = []
    status = None
    fail = None
    decided = np.zeros(len(S) + len(nulls), bool)
    while solved < max_solves:
        allb = np.concatenate([rem, frc])
        allb[decided] = np.inf
        idx = int(np.argmin(allb))
        if allb[idx] >= thr:
            status = 'C1' if not undecided else 'undecided'
            break
        if idx < len(S):
            S0, S1 = (S[idx],), ()
        else:
            S0, S1 = (), (int(nulls[idx - len(S)]),)
        res = solve_node(X, y, lam, k, S0, S1, W0=W0, target=thr, fail_below=low)
        solved += 1
        absorb(res['a'])
        decided[idx] = True
        if res['ub'] < low:
            status = 'fail'
            fail = dict(S0=list(S0), S1=list(S1), ub=res['ub'], lb=res['lb'])
            break
        if res['lb'] < thr:
            undecided.append(dict(S0=list(S0), S1=list(S1), lb=res['lb'], ub=res['ub'], st=res['status']))
        if verbose:
            print(solved, S0, S1, res['lb'] - fS, res['ub'] - fS, res['status'], flush=True)
    if status is None:
        status = 'max_solves'
    return dict(status=status, fS=fS, solved=solved, fail=fail, undecided=undecided,
                root_lb=root['lb'], root_ub=root['ub'],
                tau2=float((lam * np.abs(bS).min() / np.linalg.norm(r)) ** 2))
