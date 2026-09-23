"""Exact computation of the worst-case CIA rounding gap with a switching budget.

Setting (Sager & Zeile 2021, Sections 3, 6, 7): equidistant grid with N intervals,
t_0 = 0, t_f = N, so Delta_bar = 1 and all values of theta are in units of Delta_bar.
Relaxed controls a in A_N (columns sum to one), binary controls w in Omega_N,

    theta(a, w) = max_{i, k} | sum_{j <= k} (a_{i,j} - w_{i,j}) |,
    TV(w)       = number of intervals j >= 2 on which the active control changes
                  (Definition 10 / constraints (3.1)-(3.2) with the factor 1/2),
    theta_max(N, n_omega, sigma_max) = max_a min_{w : TV(w) <= sigma_max} theta(a, w).

theta_max is computed by row generation: a master MILP maximises theta over a
subject to theta <= theta(a, w) for w in a working set W (each such constraint is
a disjunction over the 2 * n_omega * N linear pieces of theta(a, .), modelled with
binary selectors), and the separation step evaluates min_w theta(a*, w) over ALL
feasible schedules by vectorised enumeration.  The master value is an upper bound
and the separation value a lower bound on theta_max; the loop stops when they meet.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from fractions import Fraction

import numpy as np
import gurobipy as gp
from gurobipy import GRB


def enumerate_schedules(N: int, n: int, sigma_max: int, count_initial: bool = False) -> np.ndarray:
    """All active-control sequences s in [n]^N with at most sigma_max switches.

    count_initial=False: switches are changes of the active control between
    consecutive intervals (paper, Definition 10).
    count_initial=True: alternative reading of (3.2) with w_{i,0} := 0, which adds
    1/2 to the TV of every schedule; then TV <= sigma_max means <= sigma_max - 1 changes.
    """
    budget = sigma_max - 1 if count_initial else sigma_max
    seqs = np.array(list(itertools.product(range(n), repeat=N)), dtype=np.int8)
    changes = (seqs[:, 1:] != seqs[:, :-1]).sum(axis=1)
    return seqs[changes <= budget]


def one_hot(seqs: np.ndarray, n: int) -> np.ndarray:
    M, N = seqs.shape
    W = np.zeros((M, n, N), dtype=np.int8)
    W[np.arange(M)[:, None], seqs, np.arange(N)[None, :]] = 1
    return W


def theta_of(a: np.ndarray, Wcum: np.ndarray) -> np.ndarray:
    """theta(a, w) for every schedule; Wcum = cumsum of one-hot schedules along time."""
    D = np.cumsum(a, axis=1)[None, :, :] - Wcum
    return np.abs(D).max(axis=(1, 2))


@dataclass
class Result:
    N: int
    n: int
    sigma_max: int
    theta_max: float
    a: np.ndarray
    w_seq: np.ndarray        # best schedule for the extremal a (active control per interval)
    n_cuts: int
    n_iter: int
    n_schedules: int


def theta_max_bigM(N: int, n: int, sigma_max: int, tol: float = 1e-6, count_initial: bool = False,
                   verbose: bool = False, seed: int = 0, threads: int = 8) -> Result:
    """Reference solver (big-M disjunctions per schedule); only for very small cases."""
    seqs = enumerate_schedules(N, n, sigma_max, count_initial)
    Wcum = np.cumsum(one_hot(seqs, n), axis=2).astype(np.float64)
    M = len(seqs)
    rng = np.random.default_rng(seed)
    # initial working set: a few random schedules
    work = list(rng.choice(M, size=min(M, 2 * n), replace=False))
    in_work = set(work)
    bigM = 2.0 * N

    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.MIPGap = 0.0
    model.Params.MIPGapAbs = 1e-7
    model.Params.IntFeasTol = 1e-9
    model.Params.FeasibilityTol = 1e-9
    model.Params.Threads = threads
    a = model.addVars(n, N, lb=0.0, ub=1.0, name="a")
    th = model.addVar(lb=0.0, ub=N, name="theta")
    model.setObjective(th, GRB.MAXIMIZE)
    for k in range(N):
        model.addConstr(gp.quicksum(a[i, k] for i in range(n)) == 1)
    # symmetry breaking (controls are interchangeable): order controls by a_{i,1}
    for i in range(n - 1):
        model.addConstr(a[i, 0] >= a[i + 1, 0])
    A = {(i, k): gp.quicksum(a[i, j] for j in range(k + 1)) for i in range(n) for k in range(N)}

    def add_cut(m_idx: int):
        z = model.addVars(2, n, N, vtype=GRB.BINARY)
        model.addConstr(z.sum() == 1)
        for i in range(n):
            for k in range(N):
                c = Wcum[m_idx, i, k]
                model.addConstr(th <= (A[i, k] - c) + bigM * (1 - z[0, i, k]))
                model.addConstr(th <= -(A[i, k] - c) + bigM * (1 - z[1, i, k]))

    for m_idx in work:
        add_cut(m_idx)

    best_lb, best_a, best_w = -1.0, None, None
    it = 0
    while True:
        it += 1
        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"master status {model.Status}")
        ub = th.X
        a_val = np.array([[a[i, k].X for k in range(N)] for i in range(n)])
        thetas = theta_of(a_val, Wcum)
        m_star = int(np.argmin(thetas))
        lb = float(thetas[m_star])
        if lb > best_lb:
            best_lb, best_a, best_w = lb, a_val, seqs[m_star]
        if verbose:
            print(f"  iter {it}: master UB={ub:.6f}  separation LB={lb:.6f}  |W|={len(work)}")
        if ub - lb <= tol:
            break
        # add the violated schedules (all near-minimal ones) to the working set
        cand = np.where(thetas <= lb + 1e-9)[0]
        added = 0
        for m_idx in cand[:5]:
            if m_idx not in in_work:
                add_cut(int(m_idx)); work.append(int(m_idx)); in_work.add(int(m_idx)); added += 1
        if added == 0:
            raise RuntimeError("no new cut found although gap remains; tolerance issue")
    return Result(N, n, sigma_max, best_lb, best_a, best_w, len(work), it, M)


def theta_max(N: int, n: int, sigma_max: int, tol: float = 1e-6, count_initial: bool = False,
              verbose: bool = False, threads: int = 8, batch: int = 200) -> Result:
    """Exact theta_max by a covering MILP with lazily generated schedule rows.

    For a threshold theta and cumulative sums A_{i,k} = sum_{j<=k} a_{i,j}, schedule w
    (cumulative counts C_{i,k}, integers) satisfies theta(a, w) >= theta iff for some (i, k)
    C_{i,k} <= floor(A_{i,k} - theta)  or  C_{i,k} >= ceil(A_{i,k} + theta).
    Binaries y[i,k,m] = [A_{i,k} >= m + theta], x[i,k,m] = [A_{i,k} <= m - theta] encode the
    thresholds; the row for w reads sum_{i,k} y[i,k,C_{i,k}] + x[i,k,C_{i,k}] >= 1.
    Products theta * y are linearised exactly (theta in [0, N]).
    """
    seqs = enumerate_schedules(N, n, sigma_max, count_initial)
    Wcum_i = np.cumsum(one_hot(seqs, n), axis=2)            # int, shape (M, n, N)
    Wcum = Wcum_i.astype(np.float64)
    M = len(seqs)

    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.MIPGap = 0.0
    model.Params.MIPGapAbs = 1e-7
    model.Params.IntFeasTol = 1e-9
    model.Params.FeasibilityTol = 1e-9
    model.Params.Threads = threads
    a = model.addVars(n, N, lb=0.0, ub=1.0, name="a")
    th = model.addVar(lb=0.0, ub=N, name="theta")
    model.setObjective(th, GRB.MAXIMIZE)
    for k in range(N):
        model.addConstr(gp.quicksum(a[i, k] for i in range(n)) == 1)
    for i in range(n - 1):                                   # symmetry breaking
        model.addConstr(a[i, 0] >= a[i + 1, 0])
    A = {(i, k): gp.quicksum(a[i, j] for j in range(k + 1)) for i in range(n) for k in range(N)}
    y, x = {}, {}
    for i in range(n):
        for k in range(N):
            for m in range(k + 2):
                y[i, k, m] = model.addVar(vtype=GRB.BINARY)
                x[i, k, m] = model.addVar(vtype=GRB.BINARY)
            model.addConstr(x[i, k, 0] == 0)                 # A <= -theta impossible
            for m in range(1, k + 2):
                model.addConstr(y[i, k, m] <= y[i, k, m - 1])
                model.addConstr(x[i, k, m - 1] <= x[i, k, m])
            # p = theta * y[i,k,0], q = theta * x[i,k,k+1]  (exact McCormick, theta in [0,N])
            p = model.addVar(lb=0.0, ub=N); q = model.addVar(lb=0.0, ub=N)
            for prod, b in ((p, y[i, k, 0]), (q, x[i, k, k + 1])):
                model.addConstr(prod <= N * b)
                model.addConstr(prod <= th)
                model.addConstr(prod >= th - N * (1 - b))
            model.addConstr(A[i, k] >= p + gp.quicksum(y[i, k, m] for m in range(1, k + 2)))
            model.addConstr(A[i, k] <= (k + 1) - gp.quicksum(x[i, k, m] for m in range(k + 1)) - q)

    def add_row(m_idx: int):
        C = Wcum_i[m_idx]
        model.addConstr(gp.quicksum(y[i, k, int(C[i, k])] + x[i, k, int(C[i, k])]
                                    for i in range(n) for k in range(N)) >= 1)

    rng = np.random.default_rng(0)
    work = set(int(m) for m in rng.choice(M, size=min(M, batch), replace=False))
    for m_idx in work:
        add_row(m_idx)

    best_lb, best_a, best_w = -1.0, None, None
    it = 0
    while True:
        it += 1
        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"master status {model.Status}")
        ub = th.X
        a_val = np.array([[a[i, k].X for k in range(N)] for i in range(n)])
        thetas = theta_of(a_val, Wcum)
        m_star = int(np.argmin(thetas))
        lb = float(thetas[m_star])
        if lb > best_lb:
            best_lb, best_a, best_w = lb, a_val, seqs[m_star]
        if verbose:
            print(f"  iter {it}: master UB={ub:.6f}  separation LB={lb:.6f}  rows={len(work)}")
        if ub - lb <= tol:
            break
        order = np.argsort(thetas)                           # least covered schedules first
        added = 0
        for m_idx in order:
            if thetas[m_idx] >= ub - 1e-9 or added >= batch:
                break
            if int(m_idx) not in work:
                add_row(int(m_idx)); work.add(int(m_idx)); added += 1
        if added == 0:
            raise RuntimeError("no violated row found although gap remains")
    return Result(N, n, sigma_max, best_lb, best_a, best_w, len(work), it, M)


# ---------- reference values from the paper (Delta_bar = 1, t_f - t_0 = N) ----------

def conjecture(N: int, n: int, sigma: int) -> Fraction:
    """Conjecture 1 (7.6), n_omega > 2."""
    if sigma <= n - 2:
        return Fraction(N, sigma + 2) + Fraction(1, 2)
    return Fraction(N, 2 * sigma + 4 - n) + Fraction(1, 2)


def cor7_lower(N: int, n: int, sigma: int) -> Fraction:
    """Corollary 7 (7.5) lower bound, n_omega > 2."""
    if sigma <= n - 2:
        return Fraction(N, sigma + 2)
    return Fraction(N, 2 * sigma + 4 - n)


def cor5_claim(N: int, sigma: int) -> Fraction:
    """Historical Corollary 5 expression, not a valid universal lower bound.

    At n=3, N=5, sigma=2 it returns 8/7, but the exact worst case is 1.
    See results/cia-five-interval-two-switch-minimax.md for the proof.
    """
    return Fraction(N + sigma + 1, 3 + 2 * sigma)


def cor6_upper(N: int, n: int, sigma: int) -> Fraction:
    """Corollary 6 upper bound, n_omega > 2."""
    return Fraction(2 * n - 3, 2 * n - 2) * (Fraction(N, sigma + 1) + 1)


def thm4_lower_n2(N: int, sigma: int) -> Fraction:
    """Theorem 4 / (6.12): ceil_{0.5}(N / (3 + 2 sigma))."""
    R = Fraction(N, 3 + 2 * sigma)
    return Fraction(int(-(-R * 2 // 1)), 2)  # ceil to multiple of 1/2


def cor4_upper_n2(N: int, sigma: int) -> Fraction:
    """Corollary 4 (6.18): (N + sigma + 1)/(3 + 2 sigma), tight if N = k(3+2sigma) + 2 + sigma."""
    return Fraction(N + sigma + 1, 3 + 2 * sigma)
