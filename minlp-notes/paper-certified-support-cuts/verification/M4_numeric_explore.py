"""M4: NUMERICAL exploration (floating point; not a proof).

(E1) Discretized-measure LP for the lifted minimum of
     dist(y,A)^2 + dist(y,C)^2 over pairs of measures on [l,u] with equal
     moments of orders 1..k.  For k = 2 and two-point sets this reproduces
     the exact trichotomy (0 for interleaving, delta^2/2 otherwise); for
     k >= 3 without a zero witness it shows intermediate values that depend
     on [l,u].  An LP on a grid restricts the measures, so its value is an
     upper bound on the true lifted minimum.
(E2) SDP bounds for the family objective with: exact local pair hulls
     (PSD + RLT, exact on 2-D boxes by Anstreicher-Burer), optionally the
     dense 4x4 PSD moment matrix of (1,x,y,z), optionally McCormick for xz.
Single-threaded; runs in well under a minute.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import linprog
import cvxpy as cp


def lifted_lp(A, C, l, u, k, N=2001):
    t = np.linspace(l, u, N)
    dA = np.min((t[:, None] - np.array(A, float)[None, :]) ** 2, axis=1)
    dC = np.min((t[:, None] - np.array(C, float)[None, :]) ** 2, axis=1)
    cost = np.concatenate([dA, dC])
    Aeq = np.zeros((k + 2, 2 * N))
    beq = np.zeros(k + 2)
    Aeq[0, :N] = 1
    beq[0] = 1
    Aeq[1, N:] = 1
    beq[1] = 1
    for j in range(1, k + 1):
        Aeq[j + 1, :N] = t**j
        Aeq[j + 1, N:] = -t**j
    res = linprog(cost, A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
    return res.fun


def glob(A, C):
    return min((s - t) ** 2 for s in A for t in C) / 2


print("(E1) lifted LP values")
for A, C, k in [((0.25, 0.75), (0, 0.625), 2), ((0, 3), (1, 2), 2), ((0, 1), (2, 3), 2),
                ((0, 10), (4, 5), 2), ((0, 2), (1, 3), 2), ((0, 2), (1, 3), 3), ((0, 2), (1, 3), 4),
                ((0, 2, 4), (1, 3), 3), ((0, 2, 4), (1, 3), 4)]:
    lo, hi = min(A + C), max(A + C)
    for (l, u) in [(lo, hi), (lo - 2, hi + 2)]:
        print("  A=%s C=%s k=%d [l,u]=[%g,%g]: lifted %.5f, global %.5f"
              % (A, C, k, l, u, lifted_lp(A, C, l, u, k), glob(A, C)))


def sdp_bound(a, b, c, d, l, u, wx=None, wz=None, dense=True, mcc=True):
    """wx, wz: coefficients of x(1-x), z(1-z); default b^2, d^2 (family)."""
    wx = b * b if wx is None else wx
    wz = d * d if wz is None else wz
    M = cp.Variable((4, 4), symmetric=True)
    X, Y, Z = 1, 2, 3
    E = lambda p, q: M[p, q]
    cons = [M[0, 0] == 1]
    bnd = {X: (0, 1), Y: (l, u), Z: (0, 1)}

    def rlt(i, j):
        li, ui = bnd[i]
        lj, uj = bnd[j]
        return [E(i, j) - lj * E(0, i) - li * E(0, j) + li * lj >= 0,
                E(i, j) - uj * E(0, i) - ui * E(0, j) + ui * uj >= 0,
                -E(i, j) + uj * E(0, i) + li * E(0, j) - li * uj >= 0,
                -E(i, j) + lj * E(0, i) + ui * E(0, j) - ui * lj >= 0]
    for blk in [(X, Y), (Y, Z)]:
        idx = [0, blk[0], blk[1]]
        cons.append(M[np.ix_(idx, idx)] >> 0)
        for i in blk:
            for j in blk:
                if i <= j:
                    cons += rlt(i, j)
    if dense:
        cons.append(M >> 0)
    if mcc:
        cons += rlt(X, Z)
    DL = E(Y, Y) + a * a + b * b * E(X, X) - 2 * a * E(0, Y) - 2 * b * E(X, Y) + 2 * a * b * E(0, X) \
        + wx * (E(0, X) - E(X, X))
    DR = E(Y, Y) + c * c + d * d * E(Z, Z) - 2 * c * E(0, Y) - 2 * d * E(Y, Z) + 2 * c * d * E(0, Z) \
        + wz * (E(0, Z) - E(Z, Z))
    prob = cp.Problem(cp.Minimize(DL + DR), cons)
    prob.solve(solver="CLARABEL")
    return prob.value


print("(E2) SDP bounds (pair hulls = local PSD+RLT)")
cases = [("1/128 example D", (0.25, 0.5, 0, 0.625, 0, 1), dict(wx=1.0, wz=1.0)),
         ("family D~ (same A,C)", (0.25, 0.5, 0, 0.625, 0, 1), {}),
         ("A={0,2},C={1,3}", (0, 2, 1, 2, 0, 3), {}),
         ("A={0,2},C={3,1} (d<0)", (0, 2, 3, -2, -1, 4), {}),
         ("A={2,0},C={1,3} (b<0)", (2, -2, 1, 2, 0, 3), {})]
for name, args, kw in cases:
    out = []
    for dense, mcc in [(False, False), (True, False), (False, True), (True, True)]:
        out.append("dense=%d mcc=%d: %.6f" % (dense, mcc, sdp_bound(*args, dense=dense, mcc=mcc, **kw)))
    a, b, c, d, l, u = args
    print("  %s: %s | global %.6f" % (name, "; ".join(out), glob((a, a + b), (c, c + d))))
