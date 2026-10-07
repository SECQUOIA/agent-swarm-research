"""camshape: structure extraction from the OSIL, reduced model, and local NLP solve.

OSIL model (n = 100, 200, 400, 800; checked by extract()):
  vars r_1..r_n (x1..xn), d_1..d_{n-1} (x_{n+1}..x_{2n-1})
  min  -c0 * sum_i r_i
  G_1 : -r_1 + c r_2 - r_1 r_2 <= 0                          (row e_n)
  G_i : -r_{i-1} r_i + c r_{i-1} r_{i+1} - r_i r_{i+1} <= 0     (i = 2..n-1)
  G_n : c2 r_{n-1} - 2 r_n - r_{n-1} r_n <= 0                 (row e_{n+1})
  E   : c r_n^2 - 4 r_n <= 0                                  (row e_{n+2}; implied by r_n <= 2 < 4/c)
  D_i : r_i - r_{i+1} + d_i = 0                               (i = 1..n-1)
  bounds: r_1 in [1, ub1], r_i in [1, 2], r_n in [lbn, 2], d_1 free, |d_i| <= alpha (i >= 2).
Reduced model: eliminate d (d_1 free; |r_{i+1} - r_i| <= alpha for i = 2..n-1).
Since all r > 0, dividing G_i by the product of its variables gives the equivalent
  g_1 = 1 + 1/r_2 - c/r_1 >= 0,  g_i = 1/r_{i-1} + 1/r_{i+1} - c/r_i >= 0,
  g_n = 1/r_{n-1} + 1/2 - (c2/2)/r_n >= 0.
"""
import numpy as np
from scipy.optimize import minimize

from osil_eval import load


def extract(n):
    I = load(f"camshape{n}")
    assert len(I["vt"]) == 2 * n - 1 and I["ncons"] == 2 * n
    obj = I["rows"][-1]
    c0s = set(obj["lin"].values())
    assert len(c0s) == 1 and sorted(obj["lin"]) == list(range(n)) and obj["quad"] == [] and obj["nl"] is None
    c0 = -c0s.pop()
    row = I["rows"][0]
    c = row["quad"][1][2]
    for i in range(2, n):  # G_i rows are rows 0..n-3 (e2..e_{n-1})
        row = I["rows"][i - 2]
        a, b, d = i - 2, i - 1, i  # 0-based indices of r_{i-1}, r_i, r_{i+1}
        assert row["lin"] == {} and sorted(row["quad"]) == sorted([(a, b, -1.0), (a, d, c), (b, d, -1.0)]), (i, row)
        assert row["ub"] == 0.0 and row["lb"] == -np.inf
    r1 = I["rows"][n - 2]
    assert r1["lin"] == {0: -1.0, 1: c} and r1["quad"] == [(0, 1, -1.0)] and r1["ub"] == 0.0
    rn = I["rows"][n - 1]
    c2 = rn["lin"][n - 2]
    assert rn["lin"] == {n - 2: c2, n - 1: -2.0} and rn["quad"] == [(n - 2, n - 1, -1.0)] and rn["ub"] == 0.0
    re = I["rows"][n]
    assert re["lin"] == {n - 1: -4.0} and re["quad"] == [(n - 1, n - 1, c)] and re["ub"] == 0.0
    for i in range(1, n):
        row = I["rows"][n + i]
        assert row["lin"] == {i - 1: 1.0, i: -1.0, n + i - 1: 1.0} and row["lb"] == row["ub"] == 0.0
    lb, ub = I["lb"], I["ub"]
    alpha = ub[n + 1]
    assert np.isinf(lb[n]) and np.isinf(ub[n])
    for j in range(n + 1, 2 * n - 1):
        assert lb[j] == -alpha and ub[j] == alpha
    assert lb[0] == 1.0 and lb[n - 1] > 1.0 and ub[n - 1] == 2.0
    for j in range(1, n - 1):
        assert lb[j] == 1.0 and ub[j] == 2.0
    return dict(I=I, n=n, c0=c0, c=c, c2=c2, alpha=alpha, lb=np.array(lb[:n]), ub=np.array(ub[:n]))


def g_all(r, m):
    """Reciprocal-form constraints g >= 0 (vector of length n)."""
    c, c2 = m["c"], m["c2"]
    u = 1.0 / r
    g = np.empty(len(r))
    g[0] = 1.0 + u[1] - c * u[0]
    g[1:-1] = u[:-2] + u[2:] - c * u[1:-1]
    g[-1] = u[-2] + 0.5 - 0.5 * c2 * u[-1]
    return g


def solve_local(m, r0, maxiter=500):
    n, alpha = m["n"], m["alpha"]
    c, c2 = m["c"], m["c2"]

    def G(r):  # original bilinear forms, required <= 0 -> return -G >= 0
        out = np.empty(n)
        out[0] = -(-r[0] + c * r[1] - r[0] * r[1])
        out[1:-1] = -(-r[:-2] * r[1:-1] + c * r[:-2] * r[2:] - r[1:-1] * r[2:])
        out[-1] = -(c2 * r[-2] - 2 * r[-1] - r[-2] * r[-1])
        return out

    def JG(r):
        J = np.zeros((n, n))
        J[0, 0] = -(-1 - r[1]); J[0, 1] = -(c - r[0])
        for i in range(1, n - 1):
            J[i, i - 1] = -(-r[i] + c * r[i + 1]); J[i, i] = -(-r[i - 1] - r[i + 1]); J[i, i + 1] = -(c * r[i - 1] - r[i])
        J[-1, -2] = -(c2 - r[-1]); J[-1, -1] = -(-2 - r[-2])
        return J

    k = np.arange(1, n - 1)  # curvature for i = 2..n-1 (0-based pairs (i-1, i) for i in 1..n-2)
    A = np.zeros((n - 2, n))
    A[np.arange(n - 2), k] = -1.0
    A[np.arange(n - 2), k + 1] = 1.0
    cons = [dict(type="ineq", fun=G, jac=JG),
            dict(type="ineq", fun=lambda r: alpha - A @ r, jac=lambda r: -A),
            dict(type="ineq", fun=lambda r: alpha + A @ r, jac=lambda r: A)]
    bnds = list(zip(m["lb"], m["ub"]))
    res = minimize(lambda r: -np.sum(r), r0, jac=lambda r: -np.ones(n), bounds=bnds, constraints=cons,
                   method="SLSQP", options=dict(maxiter=maxiter, ftol=1e-15))
    return res


def heuristic_start(m):
    """Straight line r = 1/cos(theta) (convexity active) until the slope limit, then slope alpha."""
    n, alpha, c = m["n"], m["alpha"], m["c"]
    dth = np.arccos(c / 2)
    r = np.empty(n)
    r[0] = 1.0
    for i in range(1, n):
        cand = 1.0 / np.cos(min(i * dth, 1.4))
        r[i] = min(cand, r[i - 1] + alpha, 2.0)
    r[-1] = max(r[-1], m["lb"][-1])
    return np.clip(r * (1 - 1e-6), m["lb"], m["ub"])
