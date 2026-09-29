"""Exact four-variable rational SOS-convexity without rational SOS.

This verifies a concrete Hessian Gram matrix. The no-rational-SOS proof
uses the rational quadratic vanishing space, checked separately below.
"""

from itertools import product
import sympy as s


def icbrt(n):
    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    assert lo**3 <= n < (lo + 1)**3
    return lo


x = s.symbols("x y z w")
u = s.symbols("u0:4")
v = s.symbols("v0:4")
den = 2**31
approximants = []
exposing = 0
residuals = []
for i, c in [(0, 2), (2, 5)]:
    p, q = x[i:i+2]
    a = s.Rational(icbrt(c * den**3), den)
    b = s.Rational(icbrt(c*c * den**3), den)
    approximants.extend([a, b])
    r1, r2, r3 = p*p-q, p*q-c, q*q-c*p
    exposing += b*r1-a*r2+r3
    residuals.extend([r1, r2])

eps = s.Rational(1, 2**26)
scale = 2**40
h = x[1]*(x[2]**3+x[3]**3/s.Integer(5)-3*x[2]*x[3]+5)
f0 = exposing**2+eps*sum(r*r for r in residuals)
f = scale*f0+h
center = dict(zip(x, approximants))


def square_gram(q):
    """Hessian Gram of q² at the rational center, no root arithmetic."""
    d = q.subs(center)
    b = s.Matrix([s.diff(q, t).subs(center) for t in x])
    T = s.hessian(q, x)/2
    C = 2*b*b.T+4*d*T
    D = s.Matrix(4, 16, lambda i, kj:
                 2*b[kj//4]*T[i, kj % 4]+4*b[i]*T[kj//4, kj % 4])
    vec = s.Matrix([T[k, j] for k in range(4) for j in range(4)])
    Q = 8*vec*vec.T+4*s.kronecker_product(T, T)
    return C.row_join(D).col_join(D.T.row_join(Q))


M = square_gram(exposing)
for r in residuals:
    M += eps*square_gram(r)

# Rational right inverse of the Gram coefficient map for the perturbation.
basis = list(v)+[u[k]*v[j] for k in range(4) for j in range(4)]
variables = u+v
groups = {}
for i in range(20):
    for j in range(20):
        exponent = s.Poly(basis[i]*basis[j], variables).monoms()[0]
        groups.setdefault(exponent, []).append((i, j))
shift = {x[i]: approximants[i]+u[i] for i in range(4)}
hh = s.hessian(h, x).subs(shift)
biform = (s.Matrix(v).T*hh*s.Matrix(v))[0]
B = s.zeros(20)
for exponent, coefficient in s.Poly(biform, variables).terms():
    cells = groups[exponent]
    for i, j in cells:
        B[i, j] = coefficient/len(cells)

certificate = scale*M+B
L, D = certificate.LDLdecomposition(hermitian=False)
assert all(D[i, i] > 0 for i in range(20))
assert L*D*L.T == certificate
H = s.hessian(f, x).subs(shift)
claimed = (s.Matrix(basis).T*certificate*s.Matrix(basis))[0]
assert s.Poly(s.expand(claimed-(s.Matrix(v).T*H*s.Matrix(v))[0]), variables).is_zero
print("PASS: exact rational 20x20 positive definite Hessian Gram")
print("approximants:", approximants)
print("scale:", scale, "epsilon:", eps)

# Evaluation at the point in Q[a,b]/(a³-2,b³-5).
a, b = s.symbols("a b")
relations = s.groebner([a**3-2, b**3-5], a, b, domain=s.QQ)
point = dict(zip(x, [a, a*a, b, b*b]))


def reduce_at_point(p):
    return relations.reduce(s.expand(p.subs(point)))[1]


assert reduce_at_point(h) == 0
assert all(reduce_at_point(s.diff(h, t)) == 0 for t in x)
assert reduce_at_point(exposing) == 0
assert all(reduce_at_point(r) == 0 for r in residuals)

monomials2 = [s.prod(x[i]**e[i] for i in range(4))
              for e in product(range(3), repeat=4) if sum(e) <= 2]
field_basis = [(i, j) for i in range(3) for j in range(3)]
evaluation = s.Matrix([[s.Poly(reduce_at_point(m), a, b).coeff_monomial(a**i*b**j)
                       for m in monomials2] for i, j in field_basis])
assert len(monomials2) == 15 and evaluation.rank() == 9
quadrics = [x[0]**2-x[1], x[0]*x[1]-2, x[1]**2-2*x[0],
           x[2]**2-x[3], x[2]*x[3]-5, x[3]**2-5*x[2]]
assert all(reduce_at_point(q) == 0 for q in quadrics)
quadratic_coeffs = s.Matrix([[s.Poly(q, x).coeff_monomial(m)
                             for q in quadrics] for m in monomials2])
assert quadratic_coeffs.rank() == 6
mixed = x[1]*x[2]**3
assert all(s.Poly(q*r, x).coeff_monomial(mixed) == 0
           for q in quadrics for r in quadrics)
assert s.Poly(f, x).coeff_monomial(mixed) == 1
print("PASS: zero, stationarity, six-dimensional quadratic vanishing space")
print("PASS: mixed coefficient excludes every rational SOS decomposition")
