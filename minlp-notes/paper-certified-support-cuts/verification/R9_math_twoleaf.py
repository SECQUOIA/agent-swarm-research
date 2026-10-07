#!/usr/bin/env python3
"""Round-2 math lens: rows that involve two leaves already make the star problem hard.

Reduction from maximum stable set: for a graph G on n vertices,
    min  sum_i ( -x_i + n x_i (1 - x_i) )  s.t.  x_i + x_j <= 1 (ij in E),  0 <= x <= 1
equals -alpha(G).  Every row involves exactly two leaves (no center).  The objective is
separable concave, so the minimum is attained at a vertex of the fractional stable-set
polytope; those vertices are half-integral (Balinski 1965; Nemhauser-Trotter 1974), so
minimizing over the feasible points of {0, 1/2, 1}^n is exact.  Coefficients are bounded
by n, so the reduction gives strong NP-hardness (unlike the subset-sum example).
Exact check on C5 (alpha 2), the Petersen graph (alpha 4) and random graphs (n <= 9).

Run: .venv/bin/python R9_math_twoleaf.py
"""
import itertools
import random
import sys
from fractions import Fraction as Q

sys.dont_write_bytecode = True


def alpha(n, E):
    best = 0
    for mask in range(1 << n):
        if all(not (mask >> i & 1 and mask >> j & 1) for i, j in E):
            best = max(best, bin(mask).count("1"))
    return best


def relax_min(n, E):
    vals = (Q(0), Q(1, 2), Q(1))
    best = None
    for x in itertools.product(vals, repeat=n):
        if all(x[i] + x[j] <= 1 for i, j in E):
            v = sum(-xi + n * xi * (1 - xi) for xi in x)
            best = v if best is None or v < best else best
    return best


graphs = {"C5": (5, [(i, (i + 1) % 5) for i in range(5)]),
          "Petersen": (10, [(i, (i + 1) % 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
                       + [(i, 5 + i) for i in range(5)])}
rng = random.Random(3)
for t in range(25):
    n = rng.randint(4, 9)
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4]
    graphs[f"rand{t}"] = (n, E)
ok = True
for name, (n, E) in graphs.items():
    a, m = alpha(n, E), relax_min(n, E)
    ok &= m == -a
    if name in ("C5", "Petersen"):
        print(f"{name}: alpha = {a}, relaxation minimum = {m}")
print("PASS" if ok else "FAIL", f"two-leaf-row reduction exact on {len(graphs)} graphs")
sys.exit(0 if ok else 1)
