"""R9 referee lens: the 'representation, not strength' message on a FOUR-variable path.

Burer, Natarajan and Willemsen (arXiv:2504.03996, Example 4 and Section 6.4) give a
submodular box QP in n = 4 variables whose Hessian Q is tridiagonal, i.e. whose
interaction graph is the path x1-x2-x3-x4, for which the Shor relaxation with the
RLT upper bounds is not exact. Here we check:
  (a) the exact minimum over [0,1]^4 (face enumeration in exact rationals,
      Theorem 4.1 of the manuscript);
  (b) the dense Shor relaxation with ALL McCormick/RLT inequalities of every
      product and square (the relaxation that Section 3.4 shows to be exact on
      three-variable paths);
  (c) the same relaxation restricted to the path's own products (sparse).
If (b) < (a), the manuscript's general reading in the introduction and the
conclusions ("the advantage of joint blocks over their pairs is one of
representation") holds only for three-variable paths, and a single exact
support cut of the 4-variable block is strictly stronger than the dense
first-level relaxation. Read-only, single-threaded; SDPs in floating point.
"""
import itertools
import os
from fractions import Fraction as F

os.environ.setdefault("OMP_NUM_THREADS", "1")
import cvxpy as cp
import sympy as sp

Q = [[8, -14, 0, 0], [-14, 25, -25, 0], [0, -25, 25, -14], [0, 0, -14, 8]]
c = [12, 29, 0, 0]
n = 4


def f(x):
    return sum(Q[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(c[i] * x[i] for i in range(n))


def exact_box_min():
    """Theorem 4.1 on the box: for every face (fix a subset to bounds), solve the
    stationarity system of the free coordinates when it is nonsingular."""
    best = None
    for pattern in itertools.product((0, 1, None), repeat=n):
        free = [i for i in range(n) if pattern[i] is None]
        fixed = {i: F(pattern[i]) for i in range(n) if pattern[i] is not None}
        if free:
            H = sp.Matrix([[2 * Q[i][j] for j in free] for i in free])
            if H.det() == 0:
                continue
            rhs = sp.Matrix([-(c[i] + sum(2 * Q[i][j] * fixed[j] for j in fixed)) for i in free])
            sol = H.LUsolve(rhs)
            x = [None] * n
            for k, i in enumerate(free):
                x[i] = F(int(sp.fraction(sol[k])[0]), int(sp.fraction(sol[k])[1]))
            for i in fixed:
                x[i] = fixed[i]
            if any(v < 0 or v > 1 for v in x):
                continue
        else:
            x = [fixed[i] for i in range(n)]
        val = f(x)
        if best is None or val < best[0]:
            best = (val, x)
    return best


def shor_rlt(pairs):
    M = cp.Variable((n + 1, n + 1), symmetric=True)
    cons = [M >> 0, M[0, 0] == 1]
    for i in range(1, n + 1):
        cons += [M[0, i] >= 0, M[0, i] <= 1]
    for (i, j) in pairs:
        p, q = i + 1, j + 1
        w, u, v = M[p, q], M[0, p], M[0, q]
        cons += [w >= 0, w >= u + v - 1, w <= u, w <= v]
    obj = sum(Q[i][j] * M[i + 1, j + 1] for i in range(n) for j in range(n)) + sum(c[i] * M[0, i + 1] for i in range(n))
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=cp.CLARABEL)
    return prob.value


val, x = exact_box_min()
print("exact minimum over [0,1]^4:", val, "at", x)
all_pairs = [(i, j) for i in range(n) for j in range(i, n)]
path_pairs = [(i, i) for i in range(n)] + [(0, 1), (1, 2), (2, 3)]
print("dense Shor + McCormick of all products and squares:", shor_rlt(all_pairs))
print("Shor + McCormick of path products and squares only:", shor_rlt(path_pairs))
