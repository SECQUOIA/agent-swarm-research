"""Exact local diagnostics for the independent witness/output audit.

These checks cover identities and a nonzero-center Taylor Gram. They do
not establish the dimension-uniform bounds, which are checked in prose.
"""

import sympy as sp


def coefficients(polynomials, variables, monomials):
    return sp.Matrix([
        [sp.Poly(polynomial, *variables).coeff_monomial(monomial)
         for monomial in monomials]
        for polynomial in polynomials
    ])


def positive_definite(matrix):
    lower, diagonal = matrix.LDLdecomposition(hermitian=False)
    assert lower * diagonal * lower.T == matrix
    assert all(pivot > 0 for pivot in diagonal.diagonal())


x, y, alpha, b = sp.symbols("x y alpha b")
ell = sp.Matrix([x - alpha, y - alpha * x])
local = sp.Matrix([[alpha**2, alpha / 2], [alpha / 2, 1]])
exposing = (ell.T * local * ell)[0] + (alpha - x) * (b - alpha**3)
relations = y**2 - b * x - alpha * (x * y - b) + alpha**2 * (x**2 - y)
assert sp.expand(exposing - relations) == 0
centered = sp.expand(exposing.subs({x: x + alpha, y: y + alpha**2,
                                  b: alpha**3}))
assert sp.expand(centered - (alpha**2 * x**2 - alpha * x * y + y**2)) == 0
print("PASS: cubic exposing identity and centered quadratic")

t, u, v = sp.symbols("t u v")
integral = sp.integrate((1 - t) * (u + t * v)**2, (t, 0, 1))
assert sp.expand(integral - (u + v / 3)**2 / 2 - v**2 / 36) == 0
print("PASS: exact Taylor square integration")

variables = (x, y)
q = sp.Matrix([sp.Rational(1, 3), -sp.Rational(2, 5)])
d = sp.Matrix(variables) - q
n = len(variables)
monomials = [1, x, y, x**2, x*y, y**2]
z = sp.Matrix(monomials)
identity = sp.eye(n)
vec_identity = sp.Matrix([int(i == j) for i in range(n) for j in range(n)])
centered_hessian_gram = sp.diag(4 * identity,
    8 * vec_identity * vec_identity.T + 4 * sp.eye(n*n))
shift = sp.eye(n+n*n)
shift[n:, :n] = -sp.kronecker_product(q, identity)
A = shift.T * centered_hessian_gram * shift
mu = A.det() / sp.trace(A)**(A.rows-1)
f = (1 + d.dot(d))**2 + d[0] / 1000 + 10
g = sp.Matrix([sp.diff(f, variable).subs(dict(zip(variables, q)))
               for variable in variables])
fq = f.subs(dict(zip(variables, q)))
c = fq - g.dot(g) / (2 * mu)
assert c > 0
positive_definite(A)

hessian_basis = sp.Matrix([u, v, x*u, x*v, y*u, y*v])
directions = sp.Matrix([u, v])
assert sp.expand((hessian_basis.T * A * hessian_basis)[0]
                 - (directions.T * sp.hessian(f, variables) * directions)[0]) == 0
bar_A = A - mu * sp.diag(identity, sp.zeros(n*n))
positive_definite(bar_A)
U = d.col_join(sp.kronecker_product(q, d))
V = sp.zeros(n, 1).col_join(sp.kronecker_product(d, d))
CU = coefficients(U, variables, monomials)
CV = coefficients(V, variables, monomials)
Caff = coefficients(d + g/mu, variables, monomials)
e0 = sp.Matrix([1, 0, 0, 0, 0, 0])
Q = ((CU + CV/3).T * bar_A * (CU + CV/3) / 2
     + CV.T * bar_A * CV / 36 + mu * Caff.T * Caff / 2
     + c * e0 * e0.T)
assert sp.expand((z.T * Q * z)[0] - f) == 0
positive_definite(Q)
print("PASS: nonzero rational center, nonzero gradient, exact full Taylor Gram")
