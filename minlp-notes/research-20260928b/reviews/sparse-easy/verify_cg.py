"""Exact C1 decision at S* by column generation, for the runs the note reports as 'capped'
(p = 1600, 3200) and for spot checks.  Instances follow the note's data specification (Section 6 setup,
seeds 1000.. of exp_c1.py); the decision logic is independent of the author's code:
 - lower bounds: L(a) of Lemma 1.1 evaluated on the FULL node, for a pool of dual vectors
   (r_S, saturated witnesses, and the optimal residual of every node solved so far), vectorized over all
   single-fixing nodes;
 - upper bounds: restricted perspective SOCP (cvxpy/Clarabel) over a growing column set
   (restriction => value >= node value).
The weakest undecided node is solved to optimality by CG; its residual joins the dual pool.
usage: python3 verify_cg.py p k rule alpha seed[,seed...]   (rule = sqrtn or tau0 value)"""
import sys, json, time
from common import node_primal_cvx, dual_L, saturated_witness, ridge_on
import numpy as np


def author_instance(n, p, k, rule, seed, b=1.0, sigma=0.5):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p); beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    lam = np.sqrt(n) if rule == 'sqrtn' else float(rule) * sigma * np.sqrt(2 * n * np.log(p)) / b
    return X, y, float(lam), S


def all_single_bounds(X, y, lam, k, a, S, nulls):
    """L(a) for every removal node (i in S) and forced-in node (j in nulls), vectorized."""
    c2 = (X.T @ a) ** 2
    B = 2 * a @ y - a @ a
    order = np.argsort(-c2)
    rank = np.empty(len(c2), int); rank[order] = np.arange(len(c2))
    csum = np.concatenate([[0.0], np.cumsum(c2[order])])
    T = lambda m: csum[m]
    rem = B - np.where(rank[S] >= k, T(k), T(k + 1) - c2[S]) / lam
    frc = B - (c2[nulls] + np.where(rank[nulls] >= k - 1, T(k - 1), T(k) - c2[nulls])) / lam
    return rem, frc


def solve_node_cg(X, y, lam, k, S0, S1, fS, a0, S, max_rounds=40, add=25):
    p = X.shape[1]
    S0 = tuple(S0); S1 = tuple(S1)
    fixed0 = set(S0)
    c2 = (X.T @ a0) ** 2; c2[list(fixed0)] = -1
    cols = set(int(i) for i in S if i not in fixed0) | set(S1)
    cols |= set(int(i) for i in np.argsort(-c2)[:60] if i not in fixed0)
    best_L = -np.inf
    for rnd in range(max_rounds):
        v, z, bb, res = node_primal_cvx(X, y, lam, k, (), S1, cols=sorted(cols))
        L = dual_L(X, y, lam, k, res, S0, S1)
        best_L = max(best_L, L)
        if fS is not None and v < fS * (1 - 1e-7):
            return 'fail', v, best_L, res, rnd + 1
        if fS is not None and best_L >= fS * (1 + 1e-9):
            return 'pass', v, best_L, res, rnd + 1
        if fS is None and v - best_L <= 1e-8 * max(1.0, abs(v)):
            return 'optimal', v, best_L, res, rnd + 1
        if v - best_L <= 1e-8 * max(1.0, abs(v)):
            return ('passtol' if best_L >= fS * (1 - 1e-7) else 'tie'), v, best_L, res, rnd + 1
        c2 = (X.T @ res) ** 2; c2[list(fixed0)] = -1; c2[sorted(cols)] = -1
        new = [int(i) for i in np.argsort(-c2)[:add] if c2[i] > 0]
        if not new:
            return 'stalled', v, best_L, res, rnd + 1
        cols |= set(new)
    return 'maxrounds', v, best_L, res, max_rounds


def decide(n, p, k, rule, seed):
    t0 = time.time()
    X, y, lam, S = author_instance(n, p, k, rule, seed)
    fS, bS, r = ridge_on(X, y, lam, S)
    a = X.T @ r; nulls = np.setdiff1d(np.arange(p), S); m0 = np.min(np.abs(a[S]))
    duals = [r]
    for th in np.linspace(0.5, 1.0, 11):
        al, Gam, V, _ = saturated_witness(X, y, lam, S, th * m0)
        if len(V) <= n - k - 1:
            duals.append(al)
    rem = np.full(k, -np.inf); frc = np.full(len(nulls), -np.inf)
    def absorb(dv):
        rr, ff = all_single_bounds(X, y, lam, k, dv, S, nulls)
        np.maximum(rem, rr, out=rem); np.maximum(frc, ff, out=frc)
    for dv in duals:
        absorb(dv)
    # root relaxation (for the gap) by CG
    stR, vR, LR, resR, _ = solve_node_cg(X, y, lam, k, (), (), None, r, S, max_rounds=80)
    absorb(resR)
    solved = 0; status = 'C1'; fail = None; notes = []
    while True:
        allb = np.concatenate([rem, frc])
        idx = int(np.argmin(allb))
        if allb[idx] >= fS * (1 + 1e-9):
            break
        node = ((int(S[idx]),), ()) if idx < k else ((), (int(nulls[idx - k]),))
        st, v, L, res, rounds = solve_node_cg(X, y, lam, k, node[0], node[1], fS, duals[-1] if solved == 0 else res_last, S)
        solved += 1; res_last = res
        absorb(res)
        if idx < k:
            rem[idx] = max(rem[idx], L if st != 'pass' else max(L, fS * (1 + 1e-9)))
        else:
            frc[idx - k] = max(frc[idx - k], L if st != 'pass' else max(L, fS * (1 + 1e-9)))
        if st == 'passtol':
            notes.append('passtol')
            if idx < k: rem[idx] = np.inf
            else: frc[idx - k] = np.inf
        if st == 'fail':
            status = 'fail'; fail = 'rem' if idx < k else 'frc'; break
        if st in ('tie', 'stalled', 'maxrounds'):
            notes.append(st)
            if idx < k: rem[idx] = np.inf
            else: frc[idx - k] = np.inf
            status = 'undecided'
    return dict(p=p, n=n, k=k, rule=rule, seed=seed, lam=lam, status=status, fail=fail, solved=solved,
                notes=notes, root_gap=fS - LR, root_status=stR, tau2=float((m0 / np.linalg.norm(r)) ** 2),
                pwe=bool(np.max(np.abs(a[nulls])) <= m0), time=time.time() - t0)


if __name__ == '__main__':
    p, k, rule, alpha = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
    seeds = [int(s) for s in sys.argv[5].split(',')]
    n = max(k + 2, int(round(alpha * k * np.log(p))))
    for s in seeds:
        print(json.dumps(decide(n, p, k, rule, s)), flush=True)
