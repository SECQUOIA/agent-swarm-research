"""Exact symbolic check of Section 5's ambient residual equations.

Run from the repository root:
    python \
        papers/pooling/process/whole-round-02/review09-check.py

This checks three fully symbolic ambient coordinates. It supplements the
general cancellation proof; it does not implement the chart algorithm.
"""

import sympy as S


q = S.symbols("q1 q2 q3")
C1 = S.symbols("c11 c12 c13")
C2 = S.symbols("c21 c22 c23")
B = S.symbols("B1 B2 B3")
beta = S.symbols("beta1 beta2 beta3")
b, w = S.symbols("b w")

g1 = sum(beta[h] * (C1[h] - q[h]) for h in range(3))
g2 = sum(beta[h] * (C2[h] - q[h]) for h in range(3))
R = b * sum(beta[h] * (B[h] - q[h]) for h in range(3))

for h in range(3):
    a = S.expand((C1[h] - q[h]) * g2 - (C2[h] - q[h]) * g1)
    f = S.expand(g1 * (b * (B[h] - q[h]) * g2 - (C2[h] - q[h]) * R))
    residual = (
        (C1[h] - q[h]) * w / g1
        + (C2[h] - q[h]) * (R - w) / g2
        - b * (B[h] - q[h])
    )
    assert S.cancel(g1 * g2 * residual - (a * w - f)) == 0
    assert S.Poly(a, *q).total_degree() <= 1
    assert S.Poly(f, *q).total_degree() <= 2

print(
    "Exact symbolic verification: all three ambient residual equations equal "
    "the cleared original quality equations; a has quality degree <=1 and f <=2."
)
print(
    "This is an identity check in three symbolic coordinates, supplementing "
    "the general cancellation proof; no numerical tolerance used."
)
