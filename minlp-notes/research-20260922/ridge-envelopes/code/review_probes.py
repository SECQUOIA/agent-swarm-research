"""Probes used by review-theory.md (adversarial review of theory.md).

P1  Step 4: h_{psi,pi} <= g_psi <= f on [0,1]^n for random concave, non-monotone
    psi with psi(0) != 0 and every permutation pi (n = 3).
P2  A y that is feasible for the Step 3 program (affine minorant on the simplex
    Lambda) but whose interpolant is not concave gives a linear cut that is
    invalid outside Delta_pi.
P3  Corollary 2 fails for mixed signs of a (chain z1 >= z2, a = (1, -1)).
P4  Corollary 2 on a non-chain poset (zigzag on 4 elements), grid LP over O(Q)
    versus Theorem 1.
P5  Corollary 2 with a zero coefficient inside a chain (a = (1, 0, 2)).
"""
import itertools

import gurobipy as gp
import numpy as np
from gurobipy import GRB

from common import gurobi_model
from ridge_envelope import envelope_box


def staircase_value(y_of_t, a, x):
    order = np.argsort(-x, kind="stable")
    xs = np.concatenate([[1.0], x[order], [0.0]])
    p = xs[:-1] - xs[1:]
    t = np.concatenate([[0.0], np.cumsum(a[order])])
    return p @ y_of_t(t)


def h_pi(y_of_t, a, pi, z):
    t = np.concatenate([[0.0], np.cumsum(a[list(pi)])])
    y = y_of_t(t)
    return y[0] + z[:, list(pi)] @ np.diff(y)


def p1(rng):
    n, worst_hg, worst_gf = 3, -np.inf, -np.inf
    Z = np.vstack([rng.random((4000, n)), np.array(list(itertools.product([0, 1], repeat=n)), float)])
    for _ in range(200):
        a = rng.uniform(0.2, 2.0, n)
        # concave psi = min of random lines (non-monotone, psi(0) != 0); sigma = psi + bump >= psi
        m, c = rng.normal(0, 3, 5), rng.normal(0, 2, 5)
        psi = lambda s: np.min(np.outer(np.atleast_1d(s), m) + c, axis=1)
        sig = lambda s: psi(s) + 0.5 * np.sin(3 * np.atleast_1d(s)) ** 2
        g = np.array([staircase_value(psi, a, z) for z in Z])
        f = sig(Z @ a)
        worst_gf = max(worst_gf, np.max(g - f))
        for pi in itertools.permutations(range(n)):
            worst_hg = max(worst_hg, np.max(h_pi(psi, a, pi, Z) - g))
    print(f"P1 max(h - g) = {worst_hg:.2e}, max(g - f) = {worst_gf:.2e}")


def p2():
    # sigma(s) = s, a = (1, 1), pi = identity, t = (0, 1, 2); y = (0, -10, 2).
    # Lambda-feasibility: 0*l0 - 10 l1 + 2 l2 <= l1 + 2 l2 for all lambda (true).
    y = np.array([0.0, -10.0, 2.0])
    lam_ok = all(y @ l <= np.array([0, 1, 2]) @ l + 1e-12 for l in np.random.default_rng(0).dirichlet([1, 1, 1], 1000))
    z = np.array([0.0, 1.0])
    h = y[0] + (y[1] - y[0]) * z[0] + (y[2] - y[1]) * z[1]
    print(f"P2 Lambda-feasible: {lam_ok}; h(0,1) = {h}, f(0,1) = {z.sum()}")


def grid_lp(points, fvals, x):
    m = gurobi_model()
    lam = [m.addVar(lb=0.0) for _ in range(len(points))]
    for i in range(points.shape[1]):
        m.addConstr(gp.LinExpr(points[:, i].tolist(), lam) == float(x[i]))
    m.addConstr(gp.LinExpr([1.0] * len(points), lam) == 1.0)
    m.setObjective(gp.LinExpr(fvals.tolist(), lam), GRB.MINIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal


def order_grid(n, N, rel):
    G = np.array(list(itertools.product(np.linspace(0, 1, N), repeat=n)))
    ok = np.all([G[:, i] >= G[:, j] - 1e-12 for i, j in rel], axis=0)
    return G[ok]


def p3():
    sig = lambda s: -np.asarray(s, float) ** 2
    a = np.array([1.0, -1.0])
    x = np.array([0.5, 0.5])
    P = order_grid(2, 41, [(0, 1)])
    vo = grid_lp(P, sig(P @ a), x)
    vb = envelope_box(sig, np.zeros(2), np.ones(2), a, 0.0, x)["value"]
    print(f"P3 mixed signs: vex_O(Q) = {vo:.6f}, vex_box = {vb:.6f}")


def p4(rng):
    rel = [(0, 2), (1, 2), (1, 3)]  # z1 >= z3, z2 >= z3, z2 >= z4 (zigzag poset)
    P = order_grid(4, 11, rel)
    worst = 0.0
    for trial in range(12):
        a = rng.uniform(0.3, 1.5, 4)
        b = rng.uniform(-4, 1)
        sig = np.sin if trial % 2 else (lambda s: np.asarray(s, float) ** 3 - 3 * np.asarray(s, float))
        x = P[rng.choice(len(P), 6)].T @ rng.dirichlet(np.ones(6))
        vo = grid_lp(P, sig(P @ a + b), x)
        E = envelope_box(sig, np.zeros(4), np.ones(4), a, b, x)
        rng_f = np.ptp(sig(P @ a + b))
        worst = max(worst, (E["value"] - vo) / rng_f)
        print(f"P4 trial {trial}: grid(O(Q)) - thm1 = {(vo - E['value']) / rng_f:.2e} R")
    print(f"P4 worst (thm1 - grid) = {worst:.2e} R (must be <= 0 up to tolerance)")


def p5(rng):
    rel = [(0, 1), (1, 2)]  # chain z1 >= z2 >= z3
    P = order_grid(3, 31, rel)
    a = np.array([1.0, 0.0, 2.0])
    for trial in range(4):
        b = rng.uniform(-3, 0)
        x = P[rng.choice(len(P), 5)].T @ rng.dirichlet(np.ones(5))
        vo = grid_lp(P, np.sin(P @ a + b), x)
        vb = envelope_box(np.sin, np.zeros(3), np.ones(3), a, b, x)["value"]
        print(f"P5 trial {trial}: grid(O(Q)) - vex_box = {vo - vb:.2e}")


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    p1(rng)
    p2()
    p3()
    p4(rng)
    p5(rng)
