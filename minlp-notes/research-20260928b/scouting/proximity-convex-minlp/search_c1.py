"""Counterexample search for the candidate conjecture
   (C1)  prox_inf <= C(n) * Delta(A) * max(1/2, rho_inf(Q)),
where rho_inf(Q) is the l_inf radius of the Q-Voronoi cell of Z^n (the exact
unconstrained proximity).  Hessians are Q = U^T D U with U unimodular, so
rho_inf(Q) = 1/2 * max row sum of |U^{-1}| exactly, while D may be very
ill-conditioned.  Reports the instances with the largest ratio
prox / (Delta(A) * max(1/2, rho)).
"""
from fractions import Fraction as F
import random, sys, math, json
import numpy as np
from qip import qp_opt, int_opt, prox_inf, max_subdet

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
trials = int(sys.argv[3]) if len(sys.argv) > 3 else 300


def rand_unimodular(n, steps, amp):
    U = [[int(i == j) for j in range(n)] for i in range(n)]
    for _ in range(steps):
        i, j = random.sample(range(n), 2)
        k = random.choice([v for v in range(-amp, amp + 1) if v])
        U[i] = [U[i][t] + k * U[j][t] for t in range(n)]
    return U


def inv_int(U):
    Ui = np.linalg.inv(np.array(U, dtype=float))
    return [[int(round(v)) for v in row] for row in Ui]


results = []
for trial in range(trials):
    U = rand_unimodular(n, random.randint(1, 5), 2)
    Ui = inv_int(U)
    rho = 0.5 * max(sum(abs(v) for v in row) for row in Ui)
    D = [F(random.choice([1, 1, 2, 3])) * F(10) ** random.randint(0, 4) for _ in range(n)]
    Q = [[sum(U[r][i] * D[r] * U[r][j] for r in range(n)) for j in range(n)] for i in range(n)]
    m = random.randint(n, n + 3)
    A = [[random.randint(-2, 2) for _ in range(n)] for _ in range(m)]
    if any(not any(row) for row in A):
        continue
    integral_b = random.random() < 0.5
    b = [F(random.randint(-6, 12), 1 if integral_b else random.randint(1, 7)) for _ in range(m)]
    c = [F(random.randint(-40, 40), random.randint(1, 5)) * max(D) for _ in range(n)]
    xs = qp_opt(Q, c, A, b)
    if xs is None:
        continue
    opts = int_opt(Q, c, A, b, xs, max_points=200000)
    if opts is None or opts == "big" or not opts:
        continue
    p = float(prox_inf(xs, opts))
    delta = max_subdet(A)
    ratio = p / (delta * max(0.5, rho))
    results.append((ratio, p, delta, rho, integral_b, U, [str(d) for d in D], A,
                    [str(v) for v in b], [str(v) for v in c], [str(v) for v in xs], opts[:3]))

results.sort(key=lambda r: -r[0])
print(f"n={n} evaluated={len(results)}")
for r in results[:8]:
    print(json.dumps({"ratio": round(r[0], 3), "prox": round(r[1], 3), "Delta": r[2], "rho": r[3],
                      "int_b": r[4], "U": r[5], "D": r[6], "A": r[7], "b": r[8], "c": r[9],
                      "xstar": r[10], "zopt": r[11]}))
