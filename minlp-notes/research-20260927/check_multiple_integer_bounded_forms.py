"""Exact supporting checks for bounded-form descent; not a proof of its bounds."""

import sympy as sp


z1, z2, t, s = sp.symbols("z1 z2 t s", real=True)
q1 = 2 * z1**2 - z2**2
q2 = 2 * z2**2 - 4 * z1**2
q3 = 4 + (z1 + 1 - t) ** 2 - (z1 + 1 + t) ** 2
assert sp.expand(q2 + 2 * q1) == 0
assert sp.expand(q3 - (4 - 4 * (z1 + 1) * t)) == 0
assert all(sp.diff(q, t, 2) == 0 for q in (q1, q2, q3))
assert q3.subs({z1: 0, t: 1}) == 0

# Square and reciprocal epigraph identities used in the unattained-gap example.
square_residual = (2 * z1 - 1) ** 2 + (s - 1) ** 2 - (s + 1) ** 2
assert sp.expand(square_residual - 4 * ((z1 - sp.Rational(1, 2)) ** 2 - s)) == 0
reciprocal_residual = 4 + (z2 - t) ** 2 - (z2 + t) ** 2
assert sp.expand(reciprocal_residual - 4 * (1 - z2 * t)) == 0
for integer_z1 in range(-4, 5):
    assert (sp.Integer(integer_z1) - sp.Rational(1, 2)) ** 2 >= sp.Rational(1, 4)
for integer_z2 in range(1, 20):
    assert sp.Rational(1, 4) + sp.Rational(1, integer_z2) > sp.Rational(1, 4)

# Expansion of an algebraic normal in the basis (1, sqrt(2)).
# x + sqrt(2)y + 2z = 0 has rational part span{(-2,0,1)}.
expanded_normal = sp.Matrix([[1, 0, 2], [0, 1, 0]])
rational_basis = expanded_normal.nullspace()
assert rational_basis == [sp.Matrix([-2, 0, 1])]
normal = sp.Matrix([[1, sp.sqrt(2), 2]])
assert normal * rational_basis[0] == sp.zeros(1, 1)

# An irrational line has zero rational part: x - sqrt(2)y = 0.
assert sp.Matrix([[1, 0], [0, -1]]).nullspace() == []
print("Passed: SOC identities, h=0 boundary, unattained-gap samples, rational parts.")
