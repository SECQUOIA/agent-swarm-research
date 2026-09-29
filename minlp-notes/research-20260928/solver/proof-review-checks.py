"""Exact small examples supporting the independent smoothing proof review.

These checks do not prove the general theorem or verify an SDP solver.
"""

from itertools import product

import sympy as sp


x, y, z = sp.symbols("x y z", real=True)


def coefficient(m: int, k: int) -> sp.Expr:
    b = lambda j: max(m-abs(j), 0)
    numerator = sum(b(j)*b(j-k) for j in range(-m+1, m))
    denominator = sum(b(j)**2 for j in range(-m+1, m))
    return sp.Rational(numerator, denominator)


def squared_fejer_kernel(m: int, source: sp.Expr, target: sp.Expr) -> sp.Expr:
    result = sp.Integer(1)
    for k in range(1, 2*m-1):
        result += 2 * coefficient(m, k) * sp.chebyshevt(k, source) * sp.chebyshevt(k, target)
    return sp.expand(result)


k2 = squared_fejer_kernel(2, x, y)
k3 = squared_fejer_kernel(3, x, y)
assert sp.simplify(k2 - (1 + sp.Rational(4, 3) * x * y + sp.Rational(1, 3) * (2*x*x-1) * (2*y*y-1))) == 0

for m in range(2, 13):
    a0 = sum((m-abs(j))**2 for j in range(-m+1, m))
    assert a0 == (2*m**3+m)//3
    assert 1-coefficient(m, 1) == sp.Rational(3, 2*m*m+1)
    for k in range(2*m+5):
        g = coefficient(m, k)
        assert 0 <= g <= 1
        assert 1-g <= sp.Rational(3*k*k, 2*m*m+1)
        if k > 2*m-2:
            assert g == 0

# The finite Fourier identity is exact as a Laurent polynomial.
for m in range(2, 8):
    a0 = sp.Rational(2*m**3+m, 3)
    fourier = 1 + sum(coefficient(m, k)*(z**k+z**(-k)) for k in range(1, 2*m-1))
    direct = sum(z**j for j in range(m))**2 * sum(z**(-j) for j in range(m))**2 / a0
    assert sp.expand(fourier-direct) == 0

# Endpoint zero: nonnegative does not mean strictly positive.
assert sp.simplify(k2.subs(y, 1) - sp.Rational(2, 3)*(x+1)**2) == 0
assert k2.subs({x: -1, y: 1}) == 0

# Lebesgue probability measure is not the correct reference measure.
uniform_mass = sp.integrate(k2, (y, -1, 1)) / 2
assert sp.simplify(uniform_mass - (1 - sp.chebyshevt(2, x)/9)) == 0

# First-moment consistency alone does not match degree-two smoothed marginals.
from_delta_zero = k2.subs(x, 0)
from_endpoints = (k2.subs(x, 1) + k2.subs(x, -1)) / 2
assert sp.simplify(from_endpoints - from_delta_zero - sp.Rational(2, 3)*sp.chebyshevt(2, y)) == 0

# Equal source measures but inconsistent kernel bandwidths also fail to match.
assert sp.simplify(k2.subs(x, 1) - k3.subs(x, 1)) != 0

# Verify the sign-product identity used to bound all rectangular moments.
for width in range(1, 7):
    a = sp.symbols(f"a0:{width}")
    for sign in (-1, 1):
        rhs = sum(
            sp.prod(1 + si*ai for si, ai in zip(signs, a))
            for signs in product((-1, 1), repeat=width)
            if sp.prod(signs) == sign
        ) / sp.Integer(2)**(width-1)
        assert sp.expand(rhs - (1 + sign*sp.prod(a))) == 0

print("PASS: exact Fourier, coefficient, endpoint, measure, marginal-consistency, and sign-product checks")
