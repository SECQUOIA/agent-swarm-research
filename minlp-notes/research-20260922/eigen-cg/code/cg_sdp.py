"""Is a given integer inequality a (general) CG cut of K = {z >= 0 : M(z) PSD}?
alpha.z + c >= 0 with integer alpha is a CG cut of K iff  ceil(min_K alpha.z) >= -c.
(E-CG cuts are the CG cuts of K whose PSD multiplier has rank one.)"""
import sys
import numpy as np
import cvxpy as cp
from bh import pairs
from facets import F13, F14, F15, parse


def min_over_K(n, a):
    P = pairs(n)
    Y = cp.Variable((n + 1, n + 1), symmetric=True)
    cons = [Y >> 0, Y[0, 0] == 1]
    for i in range(n):
        cons += [Y[i + 1, i + 1] == Y[0, i + 1], Y[0, i + 1] >= 0]
    for (i, j) in P:
        cons += [Y[i + 1, j + 1] >= 0]
    obj = sum(a[i] * Y[0, i + 1] for i in range(n)) + sum(a[n + k] * Y[i + 1, j + 1] for k, (i, j) in enumerate(P))
    pr = cp.Problem(cp.Minimize(obj), cons)
    pr.solve(solver=cp.CLARABEL)
    return pr.value


if __name__ == "__main__":
    for name, s in (("(13)", F13), ("(14)", F14), ("(15)", F15)):
        a, c = parse(s)
        v = min_over_K(6, a)
        print(name, "rhs -c =", -c, " min_K =", v, " CG-derivable:", np.ceil(v - 1e-7) >= -c)
