"""Exact checks for the local-curvature degree-seven quartic example."""

import sympy as sp


x, y, z, t = sp.symbols("x y z t")
variables = (x, y, z)
q = sp.Matrix([z - x**2, y * z - y**2 - 1, x * z + y**2])
polynomial = t**7 + t**6 - 2 * t**3 + 1
coordinate_y = -t**5 - t**4 + t
substitution = {x: t, y: coordinate_y, z: t**2}

assert sp.rem(t**2 * coordinate_y - (1 - t**3), polynomial, t) == 0
assert all(sp.rem(row.subs(substitution), polynomial, t) == 0 for row in q)
assert sp.expand(polynomial - (t**7 + (t**3 - 1) ** 2)) == 0
assert polynomial.subs(t, -2) < 0 < polynomial.subs(t, -1)

# The degree is prime. Rabin's criterion therefore needs only the
# Frobenius identity and the gcd test for degree one factors.
modulus = sp.Poly(polynomial, t, modulus=2)
frobenius = sp.Poly(t, t, modulus=2)
for _ in range(7):
    frobenius = (frobenius * frobenius).rem(modulus)
assert frobenius == sp.Poly(t, t, modulus=2)
assert sp.gcd(modulus, sp.Poly(t**2 - t, t, modulus=2)).degree() == 0

jacobian = q.jacobian(variables)
determinant = sp.rem(jacobian.det().subs(substitution), polynomial, t)
assert sp.rem(t**2 * determinant + sp.diff(polynomial, t), polynomial, t) == 0
assert sp.gcd(determinant, polynomial) == 1

objective = sp.expand(sum(row**2 for row in q))
hessian = sp.hessian(objective, variables)
remainder = hessian - 2 * jacobian.T * jacobian
assert all(
    sp.rem(entry.subs(substitution), polynomial, t) == 0 for entry in remainder
)
assert hessian[0, 0].subs({x: 0, y: 0, z: 1}) == -2

# This independent Sturm isolation agrees with the elementary sign and
# Descartes argument recorded in the note.
assert sp.Poly(polynomial, t).intervals() == [((-2, -1), 1)]

print("PASS: degree-seven field, unique real zero, nondegenerate Jacobian,")
print("      exact SOS Hessian identity, and explicit nonconvexity certificate")
