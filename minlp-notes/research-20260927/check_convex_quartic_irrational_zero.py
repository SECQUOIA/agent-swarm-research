"""Exact checks supporting convex-quartic-irrational-zero.md."""

import sympy as sp


x, y, r, u, v = sp.symbols("x y r u v")
q1 = x**2 - y
q2 = y**2 - 2 * x
q3 = (x - y) ** 2 - 2 * x - y + 4
A = 12599 * x**2 - 10000 * x * y + 7937 * y**2 - 15874 * x - 12599 * y + 20000
F = A**2 + 10000 * (q1**2 + q2**2)
a, b = sp.Rational(7599, 5000), sp.Rational(2937, 5000)
epsilon = sp.Rational(1, 2500)
G = A / 5000
f = F / 5000**2


def reduce_at_root(expression):
    return sp.rem(sp.expand(expression), r**3 - 2, r)


def assert_zero(expression):
    if isinstance(expression, sp.MatrixBase):
        assert all(reduce_at_root(entry) == 0 for entry in expression)
    else:
        assert reduce_at_root(expression) == 0


assert sp.expand(A - 7599 * q1 - 2937 * q2 - 5000 * q3) == 0
assert sp.Poly(F, x, y).total_degree() == 4
assert all(coefficient.is_Integer for coefficient in sp.Poly(F, x, y).coeffs())
assert max(abs(coefficient) for coefficient in sp.Poly(F, x, y).coeffs()) < 2**30
assert sp.Poly(r**3 - 2, r).is_irreducible
for polynomial in (q1, q2, q3, A, F):
    assert_zero(polynomial.subs({x: r, y: r**2}))

H = sp.Matrix([[sp.Rational(12599, 5000), -1], [-1, sp.Rational(7937, 5000)]])
j1, j2 = sp.Matrix([2 * r, -1]), sp.Matrix([-2, 2 * r**2])
J = sp.Matrix.vstack(j1.T, j2.T)
z = sp.Matrix([u, v])
d1, d2 = 2 * r - 1 - a, r**2 - 1 - b
ell = -d1 * j1 - d2 * j2
h = (z.T * H * z)[0]
shift = {x: r + u, y: r**2 + v}
assert_zero(q1.subs(shift) - (j1.dot(z) + u**2))
assert_zero(q2.subs(shift) - (j2.dot(z) + v**2))
assert_zero(G.subs(shift) - (ell.dot(z) + h))
assert_zero(sp.hessian(G, (x, y)) - 2 * H)

lo, hi = sp.Rational(1259921, 10**6), sp.Rational(1259922, 10**6)
assert lo**3 < 2 < hi**3
assert 1 < lo < hi < sp.Rational(13, 10)
assert 1 < lo**2 < hi**2 < 2
assert d1.subs(r, lo) > 0 and d2.subs(r, lo) > 0
assert (d1 + d2).subs(r, hi) == sp.Rational(11861521, 250000000000)
assert (d1 + d2).subs(r, hi) < sp.Rational(1, 20000)
assert min(H[0, 0] - 1, H[1, 1] - 1) == sp.Rational(2937, 5000)
assert sp.Rational(2937, 5000) > sp.Rational(1, 2)
assert sp.trace(H) < 5
assert j1.dot(j1).subs(r, sp.Rational(13, 10)) < 16
assert j2.dot(j2).subs(r, sp.Rational(13, 10)) < 16
assert_zero(J.det() - 6)
assert_zero(sp.trace(J.T * J) - (5 + 4 * r**2 + 8 * r))
assert (5 + 4 * r**2 + 8 * r).subs(r, sp.Rational(13, 10)) < 23
assert sp.Rational(36, 23) > 1
assert 4 * sp.Rational(1, 20000) == sp.Rational(1, 5000)

f2 = ell.dot(z) ** 2 + epsilon * (j1.dot(z) ** 2 + j2.dot(z) ** 2)
f3 = 2 * ell.dot(z) * h + 2 * epsilon * (j1.dot(z) * u**2 + j2.dot(z) * v**2)
f4 = h**2 + epsilon * (u**4 + v**4)
assert_zero(f.subs(shift) - f2 - f3 - f4)
assert_zero(sp.hessian(f2, (u, v)) - 2 * ell * ell.T - 2 * epsilon * J.T * J)
assert_zero(sp.hessian(h**2, (u, v)) - 8 * (H * z) * (H * z).T - 4 * h * H)
assert_zero(sp.hessian(epsilon * (u**4 + v**4), (u, v)) - 12 * epsilon * sp.diag(u**2, v**2))

c1, c2, t11, t12, t22 = sp.symbols("c1 c2 t11 t12 t22")
c = sp.Matrix([c1, c2])
T = sp.Matrix([[t11, t12], [t12, t22]])
cubic = 2 * c.dot(z) * (z.T * T * z)[0]
expected_hessian = 4 * (c.dot(z) * T + c * (T * z).T + (T * z) * c.T)
assert_zero(sp.hessian(cubic, (u, v)) - expected_hessian)

cubic_bound = 12 * sp.Rational(1, 5000) * 5 + 12 * epsilon * (4 + 4)
assert cubic_bound == sp.Rational(63, 1250)
margin = 2 * epsilon - cubic_bound**2 / 4
assert margin == sp.Rational(1031, 6250000) > 0
assert 5000**2 * margin == 4124
print("PASS: integer quartic, irrational zero, exact shifted identities, and all global-convexity certificate constants.")
print("Certified by the note's matrix inequalities: Hessian(F) >= 4124 I on R^2.")
