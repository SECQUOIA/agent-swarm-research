"""Randomised exact check of the linearization lemma:
for every integer optimum z of min{f(x): Ax <= b, x in Z^n} (f convex quadratic,
Hessian Q > 0) and every integer optimum z' of the linearised ILP
min{grad f(x*)^T x : Ax <= b, x in Z^n}:   ||z - x*||_Q <= ||z' - x*||_Q.
(Proof: 1/2||z-x*||_Q^2 = f(z)-f(x*)-g^T(z-x*) <= f(z')-f(x*)-g^T(z-x*)
        = 1/2||z'-x*||_Q^2 + g^T(z'-z) <= 1/2||z'-x*||_Q^2.)
Instances are bounded by a box so the ILP can be enumerated."""
from fractions import Fraction as F
from itertools import product
import random, sys
from qip import qp_opt, int_opt, fval

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
n = 3
checked = viol = 0
for t in range(150):
    L = [[random.randint(-3, 3) for _ in range(n)] for _ in range(n)]
    Q = [[sum(L[k][i] * L[k][j] for k in range(n)) + (i == j) for j in range(n)] for i in range(n)]
    c = [F(random.randint(-30, 30), random.randint(1, 4)) for _ in range(n)]
    m = random.randint(1, 3)
    A = [[random.randint(-2, 2) for _ in range(n)] for _ in range(m)]
    b = [F(random.randint(-5, 9), random.randint(1, 5)) for _ in range(m)]
    U = 4  # box -U <= x_i <= U
    for i in range(n):
        A.append([int(j == i) for j in range(n)]); b.append(F(U))
        A.append([-int(j == i) for j in range(n)]); b.append(F(U))
    xs = qp_opt(Q, c, A, b)
    if xs is None:
        continue
    opts = int_opt(Q, c, A, b, xs)
    if not opts or opts == "big":
        continue
    g = [sum(F(Q[i][j]) * xs[j] for j in range(n)) + c[i] for i in range(n)]
    pts = [z for z in product(range(-U, U + 1), repeat=n)
           if all(sum(A[r][j] * z[j] for j in range(n)) <= b[r] for r in range(len(A)))]
    gmin = min(sum(g[i] * z[i] for i in range(n)) for z in pts)
    lin_opt = [z for z in pts if sum(g[i] * z[i] for i in range(n)) == gmin]
    qn = lambda z: sum(F(Q[i][j]) * (z[i] - xs[i]) * (z[j] - xs[j]) for i in range(n) for j in range(n))
    rad = min(qn(z) for z in lin_opt)
    for z in opts:
        checked += 1
        if qn(z) > rad:
            viol += 1
print(f"integer optima checked: {checked}, violations: {viol}")
