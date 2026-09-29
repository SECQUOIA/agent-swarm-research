"""Exact finite checks for active-region-rates.md; not a theorem prover.

Run from the repository root:
    python3 -B research-20260928/solver/check_active_region_rates.py

Only rational arithmetic and symbolic polynomial identities are tested.
The general cone argument, infinite coefficient series, measurable
selection, and literature priority remain mathematical/source reviews.
"""

from fractions import Fraction as F
from itertools import product
from math import prod

import sympy as sp


x, v = sp.symbols("x v", real=True)


def kernel_multipliers(m):
    triangular = {j: m - abs(j) for j in range(1 - m, m)}
    normalizer = sum(value * value for value in triangular.values())
    assert normalizer == m * (2 * m * m + 1) // 3
    values = {
        j: F(sum(value * triangular.get(k - j, 0)
                 for k, value in triangular.items()), normalizer)
        for j in range(2 * m - 1)
    }
    return lambda j: values.get(abs(j), F(0))


def arcsine_integral(polynomial):
    value = 0
    for (degree,), coefficient in sp.Poly(polynomial, v).terms():
        if degree % 2 == 0:
            value += coefficient * sp.binomial(degree, degree // 2) / 2**degree
    return sp.expand(value)


# Explicit interval certificates also check the odd-degree rounding used
# in Lemma 3. For odd n, convert endpoint weights to 1-x^2 certificates.
interval_count = 0
for n in range(1, 17):
    for sign in (-1, 1):
        if n % 2 == 0:
            d = n // 2
            certificate = (2 * sp.chebyshevt(d, x)**2 if sign == 1 else
                           2 * (1 - x*x) * sp.chebyshevu(d - 1, x)**2)
        else:
            d = (n + 1) // 2
            previous = sp.chebyshevu(d - 2, x) if d >= 2 else 0
            factor = sp.chebyshevu(d - 1, x) - sign * previous
            certificate = ((1 + sign*x)**2 * factor**2
                           + (1 - x*x) * factor**2) / 2
        assert sp.expand(certificate - 1 - sign * sp.chebyshevt(n, x)) == 0
        assert sp.Poly(certificate, x).degree() <= 2 * ((n + 1) // 2)
        interval_count += 1


tensor_identity_count = 0
for dimension in range(1, 6):
    variables = sp.symbols(f"z0:{dimension}")
    for sign in (-1, 1):
        certificate = sum(
            prod(1 + eta_i * z_i for eta_i, z_i in zip(eta, variables))
            for eta in product((-1, 1), repeat=dimension)
            if prod(eta) == sign
        ) / sp.Integer(2)**(dimension - 1)
        assert sp.expand(certificate - 1 - sign * prod(variables)) == 0
        tensor_identity_count += 1


coefficient_count = 0
commutator_count = 0
for m in range(2, 13):
    g = kernel_multipliers(m)
    loss = 1 - g(1)
    assert loss == F(3, 2*m*m + 1)
    for j in range(4*m + 1):
        assert abs(g(j + 1) - g(j)) <= (2*j + 1) * loss
        coefficient_count += 1
    if m <= 7:
        kernel = 1 + 2 * sum(sp.Rational(g(j).numerator, g(j).denominator)
                            * sp.chebyshevt(j, x) * sp.chebyshevt(j, v)
                            for j in range(1, 2*m - 1))
        displacement = arcsine_integral(sp.expand(kernel * (x - v)**2))
        a0 = sp.Rational(m * (2*m*m + 1), 3)
        variance = sp.Rational(3*(4*m - 3), 2*m*(2*m*m + 1))
        assert sp.expand(displacement - variance - (3 - 2*m)*x*x/a0) == 0
        assert variance < sp.Rational(6, 2*m*m + 1)
        for j in range(2*m + 3):
            actual = arcsine_integral(sp.expand(kernel * sp.chebyshevt(j, v)
                                                * (x - v)))
            if j == 0:
                predicted = sp.Rational(loss.numerator, loss.denominator) * x
            else:
                up, down = (g(j)-g(j+1))/2, (g(j)-g(j-1))/2
                predicted = (sp.Rational(up.numerator, up.denominator)
                             * sp.chebyshevt(j+1, x)
                             + sp.Rational(down.numerator, down.denominator)
                             * sp.chebyshevt(j-1, x))
                assert abs(up) + abs(down) <= 2*j*loss
            assert sp.expand(actual - predicted) == 0
            commutator_count += 1


# The frequencies need not have total degree <= r. Their rounded half
# degrees must sum to <= r, including modes just beyond kernel support.
tensor_frequency_count = 0
outside_simple_bound = 0
for dimension in range(1, 4):
    for m in range(2, 5):
        g = kernel_multipliers(m)
        r = dimension * (m - 1) + 1
        for alpha in product(range(2*m + 2), repeat=dimension):
            for i in range(dimension):
                other = prod(g(alpha[j]) for j in range(dimension) if j != i)
                k = alpha[i]
                terms = [(1, 1-g(1))] if k == 0 else [
                    (k+1, (g(k)-g(k+1))/2),
                    (k-1, (g(k)-g(k-1))/2),
                ]
                mass = 0
                for frequency, coefficient in terms:
                    coefficient *= other
                    mass += abs(coefficient)
                    if coefficient:
                        output = list(alpha)
                        output[i] = frequency
                        assert sum((j + 1)//2 for j in output) <= r
                        assert sum(output) <= 2*r - 1
                        outside_simple_bound += sum(output) > r
                        tensor_frequency_count += 1
                assert mass <= max(1, 2*k) * (1-g(1))
assert outside_simple_bound > 0


# The sharp regular example: exact KKT residual identity in both regions.
# The multiplier projection for z >= u is -2*u_+.
y, u = sp.symbols("y u", real=True)
for optimizer, multiplier in [(0, 0), (u, 2*u)]:
    assert sp.expand(2*optimizer - multiplier) == 0
    residual = y*y - optimizer*optimizer - multiplier*(y-u)
    assert sp.expand(residual - (y-optimizer)**2) == 0

# The same stationarity/complementarity identity holds in arbitrary
# dimensions; this non-diagonal exact fixture checks the signs.
Q = sp.Matrix([[2, 1], [1, 3]])
ystar = sp.Matrix([u, 1-u])
yvec = sp.Matrix(sp.symbols("y0:2"))
C = sp.Matrix([[1, 2], [-1, 0], [0, -1]])
lam = sp.Matrix([1+u, 2, 3])
q = -2*Q*ystar - C.T*lam
rhs = C*ystar
f = lambda z: (z.T*Q*z)[0] + (q.T*z)[0]
assert sp.expand(f(yvec)-f(ystar)-(lam.T*(rhs-C*yvec))[0]
                 - ((yvec-ystar).T*Q*(yvec-ystar))[0]) == 0

print(f"PASS: {interval_count} interval and {tensor_identity_count} tensor certificate identities (exact)")
print(f"PASS: {coefficient_count} multiplier inequalities, {commutator_count} commutator identities, 6 displacement identities (exact)")
print(f"PASS: {tensor_frequency_count} tensor output frequencies, including {outside_simple_bound} above the simpler total-degree bound (exact)")
print("PASS: sharp regular-example KKT identities and a non-diagonal matrix KKT identity (exact)")
