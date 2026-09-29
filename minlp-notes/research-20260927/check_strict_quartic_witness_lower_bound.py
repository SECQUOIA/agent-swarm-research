"""Focused exact checks for the strict convex-quartic witness construction.

The all-k Hessian construction is imported from its independently reviewed
theorem. This file checks the new circuit promises and arithmetic constants.
"""

from fractions import Fraction as Q

import sympy as sp


for k in [1, 2, 3, 4, 8, 12, 20]:
    M = 1000 ** (k + 3)
    delta0 = Q(1, M)
    previous = None
    for i in range(1, k + 1):
        w = Q(1000**i, M)
        lo, hi = 1 - w, 1 + w
        if i == 1:
            il = iu = 1 + 3 * delta0**2
        else:
            l, h = previous
            il = 4 + 3 * l**2 - 6 * h
            iu = 4 + 3 * h**2 - 6 * l
        assert 0 < lo < hi
        assert lo**3 <= il <= iu <= hi**3
        previous = (lo, hi)

    kappa = Q(M, M - 1000**k)
    assert kappa == Q(10**9, 10**9 - 1)
    assert kappa < 2
    assert kappa * previous[1] < 2
    assert 5 * kappa * delta0**2 < 1

    # Cubic irrationality uses consecutive integer cubes, not a numerical root.
    cube_base = 100 ** (k + 3)
    assert cube_base**3 == M**2
    assert cube_base**3 < M**2 + 3 < (cube_base + 1)**3
    A = M * (M**2 + 3)
    B = (M - 1000**k)**3
    assert Q(A, B) == kappa**3 * (1 + 3 * delta0**2)
    assert B < M**3
    assert 135 * B * kappa < 270 * M**3
    if k >= 3:
        assert 2**k - 3 >= 2 ** (k - 1)

# The localization quadratic has positive value beyond the claimed radius.
r, u = sp.symbols("r u", positive=True)
lower = r**2 / 2 - 2 * u * r - u**2
assert sp.expand(lower.subs(r, 5 * u)) == sp.Rational(3, 2) * u**2
assert sp.expand(sp.diff(lower, r).subs(r, 5 * u)) == 3 * u
assert 6 < 3**2  # 2+sqrt(6)<5.

# Rank-one perturbation check on two exact, nondiagonal positive definite Grams.
for M0 in [sp.Matrix([[sp.Rational(1, 8), sp.Rational(1, 10)],
                      [sp.Rational(1, 10), sp.Rational(1, 4)]]),
           sp.Matrix([[5, 2, 1], [2, 3, 1], [1, 1, 2]])]:
    assert all(d > 0 for d in M0.LDLdecomposition(hermitian=False)[1].diagonal())
    mu = M0.det() / sp.trace(M0) ** (M0.rows - 1)
    scale = sp.ceiling(3 / mu)
    e = sp.zeros(M0.rows, 1)
    e[-1, 0] = 1
    remaining = scale * M0 - 2 * e * e.T - sp.eye(M0.rows)
    assert all(d > 0 for d in remaining.LDLdecomposition(hermitian=False)[1].diagonal())

print("PASS: exact root boxes, fixed normalization, cubic irrationality brackets,")
print("      localization and denominator constants, and rank-one Gram margins")
