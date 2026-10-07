#!/usr/bin/env python3
"""Quick exact check of the Horn-perturbation numbers (preordering-certificate remark)."""
import sympy as sp
A = sp.zeros(5)
for i in range(5):
    A[i, (i + 1) % 5] = A[(i + 1) % 5, i] = 1
J = sp.ones(5)
Q = J - 2 * A + sp.Rational(1, 5) * sp.eye(5)
W = sp.Rational(13, 8) * sp.eye(5) + A
minors = [W[:k, :k].det() for k in range(1, 6)]
assert minors == [sp.Rational(13, 8), sp.Rational(105, 64), sp.Rational(533, 512), sp.Rational(209, 4096), sp.Rational(29, 32768)]
assert sum(Q[i, j] * W[i, j] for i in range(5) for j in range(5)) == sp.Rational(-1, 4)
assert all(2 * Q[i, i] == sp.Rational(12, 5) for i in range(5))
print('Horn remark numbers PASS; eigenvalues of Q:', sorted(Q.eigenvals().keys(), key=lambda e: float(e)))
