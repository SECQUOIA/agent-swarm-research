"""Exact boundary checks for the independent unbounded-integer review.

These examples challenge rank changes, diverging multipliers, and denominator
signs. They do not implement or verify the general elimination theorem.
"""

import sympy as s


z, lam = s.symbols("z lam", real=True)
x = s.symbols("x", real=True)

# A rational rank chart valid generically can miss a feasible exceptional
# parameter, and its unique point can diverge near that parameter.
B = s.Matrix([[z, 1], [0, z]])
rhs = s.Matrix([z**2, z])
generic = B.inv() * rhs
assert generic == s.Matrix([z - 1 / z, 1])
assert B.subs(z, 0).rank() == 1
assert rhs.subs(z, 0) == s.zeros(2, 1)
assert s.limit(generic[0], z, 0, dir="+") == -s.oo

# The row-1, column-2 pivot gives a(z)+V(z)u. Both consistency
# equations are needed to make this a chart of the complete affine space.
a = s.Matrix([0, z**2])
V = s.Matrix([1, -z])
assert B * a - rhs == s.Matrix([0, z**3 - z])
assert B * V == s.Matrix([0, -z**2])
assert a.subs(z, 0) == s.zeros(2, 1)
assert V.subs(z, 0) == s.Matrix([1, 0])

# The jointly convex constraint (x-z)^2 <= 0 has feasible point x=z.
# Stationarity for x^2 + lam*(x-z)^2 approaches it only at unbounded
# multipliers when z != 0; no finite multiplier cutoff is justified.
q = (x - z) ** 2
candidate = lam * z / (1 + lam)
assert s.simplify(s.diff(x**2 + lam * q, x).subs(x, candidate)) == 0
assert s.simplify(q.subs(x, candidate)) == z**2 / (1 + lam) ** 2
assert s.limit(candidate, lam, s.oo) == z
assert s.factor(z**2 - candidate**2) == z**2 * (2 * lam + 1) / (lam + 1) ** 2
assert s.hessian(q, (z, x)).eigenvals() == {4: 1, 0: 1}

# Clearing by a denominator, instead of a positive even power, reverses
# the order on a negative-denominator chart. This is a real boundary case.
for denominator in (-3, -1, 1, 2):
    rational_row = s.Rational(1, denominator)
    cleared_row = denominator
    assert (rational_row <= 0) == (cleared_row <= 0)
assert s.Rational(1, -1) <= 0
assert not (1 <= 0)

print("PASS: exceptional rank chart, diverging multipliers, and denominator signs")
