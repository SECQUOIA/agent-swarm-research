"""COPS catalyst mixing (catmix100/200/400/800): exact structure check,
reduced (control-only) model, adjoint gradient and a local primal solve.

OSIL structure (asserted in `extract`): variables u_0..u_N (idx 0..N, bounds
[0,1]), x1_0..x1_N (idx N+1..2N+1), x2_0..x2_N (idx 2N+2..3N+2); x1_0 = 1,
x2_0 = 0, other states free.  Objective: min x1_N + x2_N + constant, with the
constant "-1" held in the objective's `constant` attribute.  Rows i = 0..N-1:

  x1-row i:    x1_{i+1} - x1_i + a(u_i x1_i + u_{i+1} x1_{i+1})
                                - b(u_i x2_i + u_{i+1} x2_{i+1}) = 0
  x2-row N+i:  ep x2_{i+1} - em x2_i - a(u_i x1_i + u_{i+1} x1_{i+1})
                                + c(u_i x2_i + u_{i+1} x2_{i+1}) = 0

with decimal constants a, b, c, ep, em read from the file (a = h/2, b = 10a,
ep/em = 1 +- a, and c = 9a up to a float artifact, e.g. 4.5000000000000005e-2).
Equivalently P(u_{i+1}) x_{i+1} = Q(u_i) x_i with
  P(u) = [[1 + a u, -b u], [-a u, ep + c u]],  Q(u) = [[1 - a u, b u], [a u, em - c u]].
det P(u) > 0 on [0,1], so the states are determined by the controls.
"""
import os
import sys
from fractions import Fraction

import numpy as np

import osilx

OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "catmix%d.osil")


def extract(N):
    m = osilx.read(OSIL % N)
    nv = 3 * N + 3
    assert len(m["names"]) == nv and len(m["cons"]) == 2 * N
    assert all(t == "C" for t in m["vt"])
    U = lambda i: i
    X1 = lambda i: N + 1 + i
    X2 = lambda i: 2 * N + 2 + i
    for j in range(nv):
        lu = (m["lb"][j], m["ub"][j])
        if j <= N:
            assert lu == ("0", "1"), j
        elif j == X1(0):
            assert lu == ("1", "1")
        elif j == X2(0):
            assert lu == ("0", "0")
        else:
            assert lu == ("-INF", "INF"), j
    o = m["obj"]
    assert o["sense"] == "min" and o["constant"] == "-1" and o["weight"] == "1"
    assert o["lin"] == {X1(N): "1", X2(N): "1"} and o["quad"] == [] and o["nl"] is None
    r0 = m["cons"][0]
    a = r0["quad"][0][2]
    b = r0["quad"][1][2].lstrip("-")
    r1 = m["cons"][N]
    c = r1["quad"][1][2]
    em = r1["lin"][X2(0)].lstrip("-")
    ep = r1["lin"][X2(1)]
    for i in range(N):
        r = m["cons"][i]
        assert r["lb"] == "0" and r["ub"] == "0" and r["constant"] == "0" and r["nl"] is None
        assert r["lin"] == {X1(i): "-1", X1(i + 1): "1"}, i
        assert r["quad"] == [(U(i), X1(i), a), (U(i), X2(i), "-" + b),
                             (U(i + 1), X1(i + 1), a), (U(i + 1), X2(i + 1), "-" + b)], i
        r = m["cons"][N + i]
        assert r["lb"] == "0" and r["ub"] == "0" and r["constant"] == "0" and r["nl"] is None
        assert r["lin"] == {X2(i): "-" + em, X2(i + 1): ep}, i
        assert r["quad"] == [(U(i), X1(i), "-" + a), (U(i), X2(i), c),
                             (U(i + 1), X1(i + 1), "-" + a), (U(i + 1), X2(i + 1), c)], i
    F = Fraction
    A, B, C, EP, EM = F(a), F(b), F(c), F(ep), F(em)
    assert A == F(1, 2 * N) and B == 10 * A and EP == 1 + A and EM == 1 - A
    assert abs(C - 9 * A) < F(1, 10 ** 15), (C, 9 * A)
    return m, dict(a=a, b=b, c=c, ep=ep, em=em)


def mats(K, u, num=float):
    a, b, c, ep, em = (num(K[k]) for k in ("a", "b", "c", "ep", "em"))
    P = [[1 + a * u, -b * u], [-a * u, ep + c * u]]
    Q = [[1 - a * u, b * u], [a * u, em - c * u]]
    return P, Q


def solve2(P, r):
    det = P[0][0] * P[1][1] - P[0][1] * P[1][0]
    return [(P[1][1] * r[0] - P[0][1] * r[1]) / det, (P[0][0] * r[1] - P[1][0] * r[0]) / det]


def mv(Q, x):
    return [Q[0][0] * x[0] + Q[0][1] * x[1], Q[1][0] * x[0] + Q[1][1] * x[1]]


def simulate(K, u, num=float):
    """states x_0..x_N for controls u_0..u_N (exact if num=Fraction)."""
    N = len(u) - 1
    x = [[num(1), num(0)]]
    for i in range(N):
        _, Qi = mats(K, u[i], num)
        Pn, _ = mats(K, u[i + 1], num)
        x.append(solve2(Pn, mv(Qi, x[-1])))
    return x


# ------------- vectorized float model for optimization -------------
class FloatModel:
    def __init__(self, K, N):
        self.N = N
        self.a, self.b, self.c, self.ep, self.em = (float(Fraction(K[k])) for k in ("a", "b", "c", "ep", "em"))

    def J_grad(self, u):
        N, a, b, c, ep, em = self.N, self.a, self.b, self.c, self.ep, self.em
        x = np.zeros((N + 1, 2))
        x[0] = (1.0, 0.0)
        Ps = []
        for i in range(N):
            ui, un = u[i], u[i + 1]
            q = np.array([(1 - a * ui) * x[i, 0] + b * ui * x[i, 1], a * ui * x[i, 0] + (em - c * ui) * x[i, 1]])
            P = np.array([[1 + a * un, -b * un], [-a * un, ep + c * un]])
            Ps.append(P)
            x[i + 1] = np.linalg.solve(P, q)
        J = x[N, 0] + x[N, 1] - 1.0
        # adjoint: rows R_i = P_{i+1} x_{i+1} - Q_i x_i ; mu_{i+1} = P_{i+1}^{-T} lam_{i+1}
        Pp = np.array([[a, -b], [-a, c]])  # dP/du ; dQ/du = -Pp
        lam = np.array([1.0, 1.0])
        mu = np.zeros((N + 2, 2))
        for i in range(N, 0, -1):
            mu[i] = np.linalg.solve(Ps[i - 1].T, lam)
            Q = np.array([[1 - a * u[i - 1], b * u[i - 1]], [a * u[i - 1], em - c * u[i - 1]]])
            lam = Q.T @ mu[i]
        g = np.array([-(mu[k] + mu[k + 1]) @ (Pp @ x[k]) for k in range(N + 1)])
        return J, g, x


def primal(N, K, verbose=False):
    from scipy.optimize import minimize
    fm = FloatModel(K, N)
    t = np.arange(N + 1) / N
    u0 = np.where(t < 0.1, 1.0, np.where(t < 0.9, 0.2, 0.0))
    res = minimize(lambda u: fm.J_grad(u)[:2], u0, jac=True, method="L-BFGS-B",
                   bounds=[(0, 1)] * (N + 1), options=dict(maxiter=20000, ftol=1e-16, gtol=1e-14, maxcor=50))
    if verbose:
        print(res.message, res.nit, res.fun)
    return np.clip(res.x, 0, 1), res.fun


if __name__ == "__main__":
    for N in [int(v) for v in sys.argv[1:]]:
        m, K = extract(N)
        print(N, K)
        u, J = primal(N, K, verbose=True)
        print("  J =", repr(J), " bang fractions:", np.mean(u > 1 - 1e-9), np.mean(u < 1e-9))
