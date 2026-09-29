"""Targeted exact checks for the one-integer tail argument.

These check illustrative algebraic identities and edge cases, not general
quantifier elimination, analytic continuation, or the complexity theorem.
"""

import sympy as sp

z, t = sp.symbols("z t")

# A rational decreasing tail and the finite value added at infinity.
g = z * t - 1
assert sp.resultant(g, sp.diff(g, t), t) == z
assert sp.resultant(g, sp.diff(g, z), t) == 1
assert sp.Poly(g, z).LC() == t
assert sp.limit(1 / z, z, sp.oo) == 0

# An irrational finite limit; a leading-z coefficient controls that limit.
g = z * (t**2 - 2) - 1
assert sp.Poly(g, z).LC() == t**2 - 2
assert sp.factor(sp.resultant(g, sp.diff(g, t), t)) == -4 * z**2 * (2 * z + 1)
assert sp.resultant(g, sp.diff(g, z), t) == 1
assert sp.limit(sp.sqrt(2 + 1 / z), z, sp.oo) == sp.sqrt(2)

# Horizontal factors must omit Res_t(G,G_z), which would be identically zero.
g = t**2 - 2
assert sp.diff(g, z) == 0
assert sp.resultant(g, sp.diff(g, t), t) == -8

# Branch crossings are caught by pairwise resultants.
g, k = z * t - 1, z * (t + 1) - 2
assert sp.factor(sp.resultant(g, k, t)) == z * (z - 1)
assert sp.simplify((2 / z - 1) - 1 / z) == (1 - z) / z

# Derivative projection catches a stationary point even with simple t roots.
g = t - (z - 7)**2
assert sp.resultant(g, sp.diff(g, t), t) == 1
assert sp.resultant(g, sp.diff(g, z), t) == 14 - 2 * z

# Rational MISOCP example: its only nonlinear row has zero xx Hessian.
x = sp.symbols("x")
residual = sp.expand(4 + (z - x)**2 - (z + x)**2)
assert residual == 4 - 4 * z * x
assert sp.diff(residual, x, 2) == 0
for j in range(1, 65):
    assert residual.subs({z: j, x: sp.Rational(1, j)}) == 0
    assert sp.Rational(1, j) > 0
    assert sp.Rational(1, j + 1) < sp.Rational(1, j)

print("Passed: 5 exact projection/limit cases and 64 exact cone fibers.")
