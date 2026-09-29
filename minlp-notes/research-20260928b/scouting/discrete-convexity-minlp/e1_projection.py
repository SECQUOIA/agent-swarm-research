"""E1/E2: value functions v(x) = min_y F(x,y), x integer, y real.

E1: F is a continuous 2-separable convex function (univariate convex terms of
z_i and z_u +/- z_v, z = (x, y)) plus optional UTVPI constraints
z_u +/- z_v <= c and bounds.  Prediction (Theorem in report): v restricted to
Z^n is DDM-convex (hence integrally convex), and so is x -> v(x/2).
E2 (control): same, plus one generic jointly convex coupling term
(a_1 z_u + a_2 z_v + a_3 z_w)^2 with random integer coefficients; v is then
only convex-extensible and violations are expected.
"""
import sys
import itertools
import numpy as np
import cvxpy as cp
from dcheck import ddm_violations, ic_violations, lnat_violations, ninf_false_local_minima, box, INF

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)


def rand_phi(t):
    k = rng.integers(5)
    a = rng.uniform(0.2, 3.0)
    c = rng.uniform(-2.5, 2.5)
    if k == 0:
        return a * cp.square(t - c)
    if k == 1:
        return a * cp.abs(t - c)
    if k == 2:
        return a * cp.pos(t - c) + rng.uniform(0, 1) * cp.pos(c - 1.3 - t)
    if k == 3:
        return a * cp.huber(t - c, rng.uniform(0.2, 1.5))
    return 0.3 * a * cp.exp(0.5 * (t - c))


def build(n, m, generic, with_cons):
    N = n + m
    xp = cp.Parameter(n)
    y = cp.Variable(m)
    z = [xp[i] for i in range(n)] + [y[j] for j in range(m)]
    terms = [0.01 * cp.sum_squares(y)]
    cons = []
    for i in range(N):
        if rng.random() < 0.5:
            terms.append(rand_phi(z[i]))
    for u, v in itertools.combinations(range(N), 2):
        if rng.random() < 0.7:
            s = rng.choice([-1, 1])
            terms.append(rand_phi(z[u] + s * z[v]))
    if with_cons:
        for u, v in itertools.combinations(range(N), 2):
            if (u >= n or v >= n) and rng.random() < 0.3:
                s = rng.choice([-1, 1])
                cons.append(z[u] + s * z[v] <= rng.uniform(0.5, 3.5))
        cons += [y >= -6, y <= 6]
    if generic:
        idx = rng.choice(N, size=3, replace=False)
        coef = rng.integers(1, 3, size=3) * rng.choice([-1, 1], size=3)
        terms.append(rng.uniform(1, 3) * cp.square(sum(int(coef[k]) * z[idx[k]] for k in range(3)) - rng.uniform(-1, 1)))
    prob = cp.Problem(cp.Minimize(sum(terms)), cons)
    return prob, xp


def tabulate(prob, xp, pts, scale=1):
    f = {}
    for p in pts:
        xp.value = np.array(p, dtype=float) / scale
        try:
            prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        except Exception:
            prob.solve(solver=cp.SCS, eps=1e-9)
        f[p] = prob.value if prob.status in ("optimal", "optimal_inaccurate") else INF
    return f


def run(trials, n, generic, with_cons):
    stats = dict(inst=0, ddm=0, ic=0, lnat=0, falselocal=0, ddm_half=0, feasible_pts=0)
    for _ in range(trials):
        m = int(rng.integers(1, 4))
        prob, xp = build(n, m, generic, with_cons)
        pts = box(-2, 2, n)
        f = tabulate(prob, xp, pts)
        if sum(v < INF for v in f.values()) < 2:
            continue
        stats["inst"] += 1
        stats["feasible_pts"] += sum(v < INF for v in f.values())
        stats["ddm"] += bool(ddm_violations(f))
        stats["ic"] += bool(ic_violations(f))
        stats["lnat"] += bool(lnat_violations(f))
        stats["falselocal"] += bool(ninf_false_local_minima(f))
        if n == 2:
            f2 = tabulate(prob, xp, box(-3, 3, n), scale=2)
            stats["ddm_half"] += bool(ddm_violations(f2))
    return stats


if __name__ == "__main__":
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    for n in (2, 3):
        for generic in (False, True):
            for with_cons in (False, True):
                s = run(T if n == 2 else T // 2, n, generic, with_cons)
                print(f"n={n} generic={generic!s:5} cons={with_cons!s:5} -> instances with violations: {s}", flush=True)
