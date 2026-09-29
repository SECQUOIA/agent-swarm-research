"""Recheck of Proposition 12 (staggered 3SAT embedding).

Construction (note §7.2): L0 = rf*sqrt(N)/tan(theta) (rf in [1, 1.01] models the rational rounding),
eta = L0/30, L = L0 + 3 eta.  X_s = [0,1]^N x {0}, X_t = [0,1]^N x {(m+1)L}; literal j=(k,a) of
clause i is {x in [0,1]^N : x_k = a} x {iL + j eta}; consecutive layers fully connected.

Checks: (1) pairwise disjointness; (2) every edge aperture <= theta (SOCP on vertex differences);
(3) exact OPT by enumerating all literal paths (L-BFGS-B per path, smooth convex objective; the
best paths re-solved with cvxpy/Clarabel); YES: OPT = (m+1)L; NO: OPT >= (m+1)L + 1/(2mL+1) and
OPT/((m+1)L) - 1 >= tan^2/(4N(m+1)^2); (4) the ratio algebra on a parameter grid."""
import itertools
import sys
import time
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize
from rc import sec_aperture, SOLVER


def build(clauses, N, theta, rf=1.0):
    m = len(clauses)
    L0 = rf * np.sqrt(N) / np.tan(theta)
    eta = L0 / 30
    L = L0 + 3 * eta
    # vertices: ('s',), ('t',), (i, j) with clause i (1..m), literal j (1..len)
    sets = {"s": (None, 0.0), "t": (None, (m + 1) * L)}
    for i, cl in enumerate(clauses, 1):
        for j, lit in enumerate(cl, 1):
            sets[(i, j)] = (lit, i * L + j * eta)
    return sets, L, eta, m


def face_vertices(lit, N):
    V = np.array(list(itertools.product([0.0, 1.0], repeat=N)))
    if lit is None:
        return V
    k, a = lit
    return V[V[:, k] == a]


def disjoint_check(sets, N):
    names = list(sets)
    min_gap = np.inf
    bad = 0
    for p, q in itertools.combinations(names, 2):
        (lp, hp), (lq, hq) = sets[p], sets[q]
        if abs(hp - hq) > 0:
            min_gap = min(min_gap, abs(hp - hq))
            continue
        # same height: faces meet unless they fix the same variable to different values
        if lp is not None and lq is not None and lp[0] == lq[0] and lp[1] != lq[1]:
            continue
        bad += 1
    return bad, min_gap


def edges_of(sets, m, clauses):
    E = [("s", (1, j)) for j in range(1, len(clauses[0]) + 1)]
    for i in range(1, m):
        E += [((i, j), (i + 1, jj)) for j in range(1, len(clauses[i - 1]) + 1) for jj in range(1, len(clauses[i]) + 1)]
    E += [((m, j), "t") for j in range(1, len(clauses[m - 1]) + 1)]
    return E


def max_aperture(sets, E, N):
    worst = 1.0
    for u, v in E:
        (lu, hu), (lv, hv) = sets[u], sets[v]
        Vu = np.c_[face_vertices(lu, N), np.full(len(face_vertices(lu, N)), hu)]
        Vv = np.c_[face_vertices(lv, N), np.full(len(face_vertices(lv, N)), hv)]
        W = np.array([b - a for a in Vu for b in Vv])
        worst = max(worst, sec_aperture(W))
    return worst


def path_min_lbfgs(lits, heights, N):
    """min sum_k sqrt(h_k^2 + |x_{k+1} - x_k|^2) over x_0 in [0,1]^N (s), x_1..x_m on faces, x_{m+1} in [0,1]^N (t)."""
    K = len(heights)  # points: s, layers..., t
    h = np.diff(heights)
    lo = np.zeros((K, N))
    hi = np.ones((K, N))
    x0 = np.full((K, N), 0.5)
    for idx, lit in enumerate(lits, 1):
        k, a = lit
        lo[idx, k] = hi[idx, k] = a
        x0[idx, k] = a

    def f(xf):
        X = xf.reshape(K, N)
        D = np.diff(X, axis=0)
        r = np.sqrt(h ** 2 + np.sum(D ** 2, axis=1))
        g = np.zeros_like(X)
        G = D / r[:, None]
        g[1:] += G
        g[:-1] -= G
        return r.sum(), g.ravel()

    res = minimize(f, x0.ravel(), jac=True, method="L-BFGS-B", bounds=list(zip(lo.ravel(), hi.ravel())),
                   options=dict(ftol=1e-15, gtol=1e-12, maxiter=5000))
    return float(res.fun)


def path_min_cvx(lits, heights, N):
    K = len(heights)
    h = np.diff(heights)
    X = cp.Variable((K, N))
    cons = [X >= 0, X <= 1]
    for idx, (k, a) in enumerate(lits, 1):
        cons.append(X[idx, k] == a)
    obj = sum(cp.norm(cp.hstack([h[k], X[k + 1] - X[k]])) for k in range(K - 1))
    pr = cp.Problem(cp.Minimize(obj), cons)
    pr.solve(solver=SOLVER)
    return float(pr.value)


def opt_all_paths(sets, clauses, N):
    m = len(clauses)
    vals = []
    for choice in itertools.product(*[range(1, len(c) + 1) for c in clauses]):
        lits = [sets[(i, j)][0] for i, j in zip(range(1, m + 1), choice)]
        hts = [0.0] + [sets[(i, j)][1] for i, j in zip(range(1, m + 1), choice)] + [sets["t"][1]]
        vals.append((path_min_lbfgs(lits, hts, N), lits, hts))
    vals.sort(key=lambda r: r[0])
    # re-solve the 5 best with cvxpy (and the claimed optimum is the min of those)
    top = [(path_min_cvx(l, h, N), v) for v, l, h in vals[:5]]
    return min(t[0] for t in top), max(abs(a - b) for a, b in top), len(vals)


def run(name, clauses, N, theta_deg, rf):
    th = np.radians(theta_deg)
    sets, L, eta, m = build(clauses, N, th, rf)
    E = edges_of(sets, m, clauses)
    bad, gap = disjoint_check(sets, N)
    secmax = max_aperture(sets, E, N)
    t0 = time.time()
    opt, dev, npaths = opt_all_paths(sets, clauses, N)
    base = (m + 1) * L
    lb_abs = base + 1 / (2 * m * L + 1)
    claim = np.tan(th) ** 2 / (4 * N * (m + 1) ** 2)
    print(f"{name:10s} N={N} m={m} theta={theta_deg:7.3f} rf={rf:.2f} tan/sqrtN={np.tan(th)/np.sqrt(N):5.2f} L={L:.4f}"
          f" | disjoint-violations={bad} min height gap={gap:.4f} | sec(theta_e)max={secmax:.6f} <= sec(theta)={1/np.cos(th):.6f}: {secmax <= 1/np.cos(th) + 1e-9}"
          f" | paths={npaths} OPT={opt:.9f} (m+1)L={base:.9f} excess={opt/base-1:.3e} "
          f"abs-LB-ok={opt >= lb_abs - 1e-9} claim={claim:.3e} ratio-ok={opt/base - 1 >= claim - 1e-12} "
          f"[lbfgs-vs-cvx max dev {dev:.1e}, {time.time()-t0:.0f}s]", flush=True)


def algebra_grid():
    worst = np.inf
    viol = 0
    for N in range(1, 61):
        for m in range(1, 61):
            for tt in np.linspace(1e-3, 3.3 * np.sqrt(N), 40):
                for rf in (1.0, 1.01):
                    L = 1.1 * rf * np.sqrt(N) / tt
                    lhs = 1 / ((m + 1) * L * (2 * m * L + 1))
                    rhs = tt ** 2 / (4 * N * (m + 1) ** 2)
                    worst = min(worst, lhs / rhs)
                    viol += lhs < rhs * (1 - 1e-12)
    print(f"algebra grid (N,m<=60, tan<=3.3 sqrt N, rf in {{1,1.01}}): violations={viol}, min lhs/rhs={worst:.4f}")
    # beyond the hypothesis the algebraic bound fails (L < 1/3):
    N, m = 1, 1
    for tt in (3.3, 5.0, 20.0):
        L = 1.1 * 1.01 * np.sqrt(N) / tt
        print(f"   N=1,m=1,rf=1.01,tan={tt}: L={L:.3f}  1/((m+1)L(2mL+1)) / claim = "
              f"{(1/((m+1)*L*(2*m*L+1))) / (tt**2/(4*N*(m+1)**2)):.3f}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    # unsatisfiable 2-CNF on 2 variables (as in the note's t9) and its satisfiable 3-clause prefix
    c2 = [[(0, 1), (1, 1)], [(0, 1), (1, 0)], [(0, 0), (1, 1)], [(0, 0), (1, 0)]]
    # unsatisfiable 3-CNF: all 8 sign patterns on 3 variables; satisfiable: drop the clause (x1 v x2 v x3)
    c3 = [[(0, a), (1, b), (2, c)] for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    c3sat = [c for c in c3 if c != [(0, 1), (1, 1), (2, 1)]]
    if which in ("all", "alg"):
        algebra_grid()
    if which in ("all", "n2"):
        tb2 = np.degrees(np.arctan(3.3 * np.sqrt(2)))
        for th in (30, 10, 3, tb2):
            for rf in (1.0, 1.01):
                run("2CNF-unsat", c2, 2, th, rf)
            run("2CNF-sat", c2[:3], 2, th, 1.01)
    if which in ("all", "n3"):
        tb3 = np.degrees(np.arctan(3.3 * np.sqrt(3)))
        for th in (30, 3, tb3):
            run("3CNF-unsat", c3, 3, th, 1.01)
        run("3CNF-sat", c3sat, 3, 30, 1.01)
