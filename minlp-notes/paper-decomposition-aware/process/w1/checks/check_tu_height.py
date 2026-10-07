"""Check the KKT saddle-matrix height bound on random TU-constrained QPs.

F(x) = (x^T H x + c^T x + e)/D, H integral symmetric (possibly indefinite),
feasible set {l<=x<=u, A x <= b} with TU A and integral data.
Global minimum by exact enumeration of all faces (row subsets) whose saddle
matrix is nonsingular. Verify:
  * some global optimizer has common denominator dividing |det K| <= R,
    R = (3 n C_H)^n  (Hadamard), and also <= (4 n C_H)^(2n) (report's bound);
  * value denominator divides D * det^2 <= D R^2;
  * no finer grid point beats the computed optimum (sanity).
"""
import math
import random
from fractions import Fraction as Fr
from itertools import combinations, product
from tu_exact_util import det, rank, solve, dot

random.seed(11)

TU_MATS = [
    [[1, 1, 0], [0, 1, 1]],                 # interval
    [[1, -1, 0], [0, 1, -1]],               # order/difference
    [[1, 1, -1]],                           # single sum row
    [[1, 0, 1], [-1, 1, 0], [0, -1, -1]],   # network incidence (3 arcs)
    [[1, 1], [1, 0]],
]


def global_min(H, c, e, D, A, b, l, u):
    n = len(H)
    M = [list(r) for r in A] + [[int(i == k) for k in range(n)] for i in range(n)] + \
        [[-int(i == k) for k in range(n)] for i in range(n)]
    d = list(b) + list(u) + [-x for x in l]
    G = [[2 * H[i][k] for k in range(n)] for i in range(n)]
    best = None
    rec = []
    for size in range(0, n + 1):
        for T in combinations(range(len(M)), size):
            rows = [M[t] for t in T]
            if rank(rows) < size:
                continue
            K = [G[i] + [-rows[k][i] for k in range(size)] for i in range(n)] + \
                [rows[k] + [0] * size for k in range(size)]
            dk = det(K)
            if dk == 0:
                continue
            rhs = [-Fr(c[i]) for i in range(n)] + [Fr(d[t]) for t in T]
            sol = solve(K, rhs)
            x = sol[:n]
            if all(dot(M[r], x) <= d[r] for r in range(len(M))):
                val = (sum(H[i][k] * x[i] * x[k] for i in range(n) for k in range(n))
                       + dot(c, x) + e) / D
                rec.append((val, x, abs(dk)))
                if best is None or val < best:
                    best = val
    return best, [(x, dk) for val, x, dk in rec if val == best]


def trial():
    A = random.choice(TU_MATS)
    n = len(A[0])
    H = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(i, n):
            H[i][k] = H[k][i] = random.randint(-3, 3)
    c = [random.randint(-9, 9) for _ in range(n)]
    e = random.randint(-5, 5)
    D = random.randint(1, 7)
    l = [random.randint(-2, 0) for _ in range(n)]
    u = [li + random.randint(1, 3) for li in l]
    # rhs: make feasible by evaluating A at a random box point and adding slack
    x0 = [random.randint(li, ui) for li, ui in zip(l, u)]
    b = [dot(r, x0) + random.randint(0, 2) for r in A]
    best, opts = global_min(H, c, e, D, A, b, l, u)
    CH = max(1, max(abs(v) for row in H for v in row))
    CP = 2 * CH                      # P = Delta * Hessian = 2H with Delta = D
    R = (3 * n * CH) ** n
    R_tex = (2 * n * CP) ** n        # constant of tu-proofs.tex
    for x, dk in opts:               # Hadamard: dk^2 <= (2 n^2 CP^2)^n
        assert dk * dk <= (2 * n * n * CP * CP) ** n <= R_tex ** 2
    R_old = (4 * n * CH) ** (2 * n)
    ok = False
    for x, dk in opts:
        den = 1
        for xi in x:
            den = den * xi.denominator // math.gcd(den, xi.denominator)
        assert dk % den == 0
        if den <= dk <= R <= R_old:
            ok = True
    assert ok, (A, H, c, opts)
    assert (D * min(dk for _, dk in opts) ** 2) % best.denominator == 0
    assert best.denominator <= D * R * R
    # sanity: grid points (mesh 1/8) are never better than the optimum
    h = Fr(1, 8)
    for y in product(*[[li + h * k for k in range(int((ui - li) / h) + 1)]
                       for li, ui in zip(l, u)]):
        if all(dot(r, y) <= bb for r, bb in zip(A, b)):
            val = (sum(H[i][k] * y[i] * y[k] for i in range(n) for k in range(n))
                   + dot(c, y) + e) / D
            assert val >= best
    return best, len(opts), max(dk for _, dk in opts), R


if __name__ == "__main__":
    worst = 0
    for t in range(60):
        best, nopt, dk, R = trial()
        worst = max(worst, dk)
    print("60 random TU QPs: height bound verified; largest optimal-face |det K| =", worst)
    print("ALL HEIGHT CHECKS PASSED")
