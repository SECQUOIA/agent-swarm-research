"""Exact three-variable convex quartic without rational SOS.

The Hessian certificate and arithmetic obstruction are independent checks.
No numerical SDP or approximate root calculation is used here.
"""

from itertools import product

import sympy as s


x, y, z = variables = s.symbols("x y z")
u = s.symbols("u0:3")
v = s.symbols("v0:3")
residuals = [
    2 - 2*x*y,
    2*x*x - 2*y*z,
    2*y*y - 4*z,
    2*z*z - x,
    2*x*z - y,
]
exposing = sum(c*q for c, q in zip([4, 5, 3, 9], residuals))
polynomial = s.expand(exposing**2 + sum(q*q for q in residuals[:4])
                      - residuals[4]**2)
center = dict(zip(variables, [s.Rational(3, 4), s.Integer(1),
                              s.Rational(1, 2)]))


def square_gram(q):
    """Exact Hessian Gram of q² on (v, u tensor v), with x=center+u."""
    d = q.subs(center)
    b = s.Matrix([s.diff(q, t).subs(center) for t in variables])
    T = s.hessian(q, variables)/2
    C = 2*b*b.T + 4*d*T
    D = s.Matrix(3, 9, lambda i, kj:
                 2*b[kj//3]*T[i, kj % 3]
                 + 4*b[i]*T[kj//3, kj % 3])
    vec = s.Matrix([T[k, j] for k in range(3) for j in range(3)])
    Q = 8*vec*vec.T + 4*s.kronecker_product(T, T)
    return C.row_join(D).col_join(D.T.row_join(Q))


certificate = square_gram(exposing)
certificate += sum((square_gram(q) for q in residuals[:4]), s.zeros(12))
certificate -= square_gram(residuals[4])
L, D = (certificate - s.eye(12)).LDLdecomposition(hermitian=False)
assert all(D[i, i] > 0 for i in range(12))
assert L*D*L.T == certificate - s.eye(12)
basis = list(v) + [u[k]*v[j] for k in range(3) for j in range(3)]
shift = {variables[i]: center[variables[i]] + u[i] for i in range(3)}
H = s.hessian(polynomial, variables).subs(shift)
claimed = (s.Matrix(basis).T*certificate*s.Matrix(basis))[0]
actual = (s.Matrix(v).T*H*s.Matrix(v))[0]
assert s.Poly(s.expand(claimed-actual), u+v).is_zero
print("PASS: rational 12x12 Hessian Gram; M-I positive definite")
print("PASS: differentiated polynomial identity and exact LDL factorization")
baseline_gram = certificate + square_gram(residuals[4])
baseline_L, baseline_D = baseline_gram.LDLdecomposition(hermitian=False)
assert all(baseline_D[i, i] > 0 for i in range(12))
assert baseline_L*baseline_D*baseline_L.T == baseline_gram
print("PASS: rational SOS baseline also has a positive definite Hessian Gram")

# The point is (a^-1,a,a^-3)=(a^4/2,a,a^2/2), where a^5=2.
a = s.symbols("a")
point = {x: a**4/2, y: a, z: a**2/2}


def at_point(p):
    return s.rem(s.expand(p.subs(point)), a**5-2, a, domain=s.QQ)


assert all(at_point(q) == 0 for q in residuals)
assert at_point(polynomial) == 0
assert all(at_point(s.diff(polynomial, t)) == 0 for t in variables)
monomials2 = [s.prod(variables[i]**e[i] for i in range(3))
              for e in product(range(3), repeat=3) if sum(e) <= 2]
evaluation = s.Matrix([
    [s.Poly(at_point(m), a).coeff_monomial(a**i) for m in monomials2]
    for i in range(5)
])
quadratic_coefficients = s.Matrix([
    [s.Poly(q, variables).coeff_monomial(m) for q in residuals]
    for m in monomials2
])
assert len(monomials2) == 10 and evaluation.rank() == 5
assert quadratic_coefficients.rank() == 5
print("PASS: zero, stationarity, five-dimensional rational vanishing space")


def obstruction(p):
    coefficients = s.Poly(p, variables)
    return 2*coefficients.coeff_monomial(z) + 4*coefficients.coeff_monomial(y*y)


assert all(obstruction(residuals[i]*residuals[j])
           == (4 if i == j == 4 else 0)
           for i in range(5) for j in range(5))
assert obstruction(polynomial) == -4
print("PASS: coefficient functional excludes rational SOS")

# Optional structural check: the Gram matrix on this vanishing space is unique.
pairs = [(i, j) for i in range(5) for j in range(i, 5)]
monomials_yz = [y**j*z**k for j in range(5) for k in range(5-j)]
minor = s.Matrix([
    [s.Poly((residuals[i]*residuals[j]).subs(x, 0), y, z).coeff_monomial(m)
     for i, j in pairs] for m in monomials_yz
])
assert minor.det() == -2**26
assert len(s.Poly(polynomial, variables).terms()) == 31
assert max(abs(c) for c in s.Poly(polynomial, variables).coeffs()) == 448
print("PASS: 15 independent products; unique vanishing-space Gram is indefinite")
print("Polynomial: 31 monomials; maximum absolute integer coefficient 448")
print("Hessian Gram entry numerator/denominator bit bound:",
      max(max(abs(t.p).bit_length(), t.q.bit_length()) for t in certificate))
