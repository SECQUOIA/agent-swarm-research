"""Exact checks for pitfalls in the two-quadratic rationality review."""

import sympy as sp


t, x, y = sp.symbols("t x y")

# Two tangent rational balls: raw determinant has an extra double root.
q1 = sp.diag(1, 1, 1, -1)
q2 = sp.Matrix([[1, 0, 0, -2], [0, 1, 0, 0],
                [0, 0, 1, 0], [-2, 0, 0, 3]])
matrix = q1 + t * q2
assert sp.factor(matrix.det()) == -(t - 1) ** 2 * (t + 1) ** 2
scalar = sp.cancel(matrix.det() / matrix[:3, :3].det())
assert sp.cancel(scalar + (t - 1) ** 2 / (t + 1)) == 0
numerator, denominator = sp.fraction(scalar)
assert sp.Poly(sp.gcd(numerator, sp.diff(numerator, t)), t).monic().as_expr() == t - 1
assert sp.degree(sp.gcd(matrix.det(), sp.diff(matrix.det(), t)), t) == 2

# A zero second Hessian produces a genuine negative quadratic term.
aggregate = x ** 2 - 2 * x + t * (2 * x)
assert sp.expand(aggregate.subs(x, 1 - t) + (t - 1) ** 2) == 0
assert aggregate.subs({x: 0, t: 1}) == 0

# Identically zero scalar minimum, with no poles of positive residue.
aggregate = x ** 2 + t * (2 * x ** 2)
assert aggregate.subs(x, 0) == 0
assert sp.diff(aggregate, x).subs(x, 0) == 0

# Common-kernel linear terms force a rational multiplier directly.
aggregate = x ** 2 + y + t * (x ** 2 - 2 * y)
assert sp.expand(aggregate.subs(t, sp.Rational(1, 2))) == 3 * x ** 2 / 2

print("Passed: reduced/raw determinant distinction and three degeneracies.")
