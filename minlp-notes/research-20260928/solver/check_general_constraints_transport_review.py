"""Independent finite checks for the ordinary-kernel transport sharpening.

Exact identities and sampled inequalities supplement the proof review. They do
not verify all degrees, all pseudomoments, or a numerical SDP certificate.
"""

from fractions import Fraction as F
from itertools import product
from math import comb
from random import Random

import sympy as sp


def arcsine_moment(k):
    return sp.Rational(comb(k, k // 2), 2**k) if k % 2 == 0 else 0


def integrate_arcsine(polynomial, variable):
    poly = sp.Poly(sp.expand(polynomial), variable)
    return sp.expand(sum(coefficient * arcsine_moment(power[0])
                         for power, coefficient in poly.terms()))


def fejer_checks():
    count = 0
    for s in range(2, 65):
        coefficients = {k: F(s - abs(k), s) for k in range(1 - s, s)}
        zero = sum(a * a for a in coefficients.values())
        first = sum(a * coefficients.get(k - 1, F(0))
                    for k, a in coefficients.items())
        assert zero == F(2 * s * s + 1, 3 * s)
        assert zero - first == F(1, s)
        assert 2 * (zero - first) == F(2, s)
        count += 1
    return count


def kernel_checks():
    x, y, z = sp.symbols("x y z")
    cases, samples = 0, 0
    for s, N in product(range(2, 6), (2, 4)):
        S = 1 + sum(2 * (1 - sp.Rational(k, s)) * sp.chebyshevt(k, x)
                    * sp.chebyshevt(k, y) for k in range(1, s))
        M = integrate_arcsine(S**2, y)
        J = integrate_arcsine((x - y)**2 * S**2, y)
        C = sp.Rational(2 * s * s + 1, 3 * s)
        Z = sp.expand(1 - M / C)
        P = sp.expand(sum(Z**k for k in range(N + 1)) / C)
        D = 2 * (s - 1) * (N + 1)
        j = sp.expand(P * J)
        n = sp.expand(P * M)
        c = 4 / (s * C)
        assert sp.expand(n - (1 - Z**(N + 1))) == 0
        assert sp.degree(j, x) <= D + 2
        assert sp.degree(n, x) <= D
        assert c <= sp.Rational(6, s**2)
        # Product-mass module identity used in a two-coordinate bag.
        n_z = n.subs(x, z)
        assert sp.expand(c - j * n_z - ((c - j) * n_z + c * (1 - n_z))) == 0
        for value in (sp.Rational(i, 12) for i in range(-12, 13)):
            assert 0 <= J.subs(x, value) <= sp.Rational(2, s)
            assert 0 <= P.subs(x, value) <= 2 / C
            assert 0 <= j.subs(x, value) <= c
            assert 1 - sp.Rational(1, 2**(N + 1)) <= n.subs(x, value) <= 1
            samples += 1
        cases += 1
    return cases, samples


def lipschitz_module_identities():
    rng = Random(110928)
    cases = 0
    for dimension in (1, 2, 3):
        xs = sp.symbols(f"x0:{dimension}")
        candidates = [alpha for alpha in product(range(4), repeat=dimension)
                      if 0 < sum(alpha) <= 4]
        for _ in range(8):
            terms = [(alpha, sp.Rational(rng.choice((-3, -2, -1, 1, 2, 3)), 3))
                     for alpha in rng.sample(candidates, min(4, len(candidates)))]
            ys = [sp.Rational(rng.randint(-4, 4), 4) for _ in xs]
            polynomial = sum(c * sp.prod(sp.chebyshevt(k, x)
                                        for k, x in zip(alpha, xs))
                             for alpha, c in terms)
            difference = sp.expand(polynomial - polynomial.subs(dict(zip(xs, ys))))
            records = []
            for alpha, c in terms:
                for i, k in enumerate(alpha):
                    if not k:
                        continue
                    quotient, remainder = sp.div(
                        sp.chebyshevt(k, xs[i]) - sp.chebyshevt(k, ys[i]),
                        xs[i] - ys[i], xs[i])
                    assert remainder == 0
                    r = (sp.sign(c) * quotient / k**2
                         * sp.prod(sp.chebyshevt(alpha[j], xs[j]) for j in range(i))
                         * sp.prod(sp.chebyshevt(alpha[j], ys[j])
                                   for j in range(i + 1, dimension)))
                    weight = abs(c) * k**2
                    records.append((weight, xs[i] - ys[i], sp.expand(r)))
            A = sum(weight for weight, _, _ in records)
            assert sp.expand(difference - sum(weight * increment * r
                                             for weight, increment, r in records)) == 0
            left = A * sum(weight * increment**2 for weight, increment, _ in records) - difference**2
            right = A * sum(weight * increment**2 * (1 - r**2)
                            for weight, increment, r in records)
            for i, (weight_i, increment_i, r_i) in enumerate(records):
                for weight_j, increment_j, r_j in records[i + 1:]:
                    right += weight_i * weight_j * (increment_i * r_i - increment_j * r_j)**2
            assert sp.expand(left - right) == 0
            degree = sp.Poly(polynomial, *xs).total_degree()
            assert sp.Poly(sp.expand(left), *xs).total_degree() <= 2 * degree
            for _, _, r in records:
                assert sp.Poly(r, *xs).total_degree() <= degree - 1
                for value in (-1, 0, 1):
                    assert abs(r.subs({x: value for x in xs})) <= 1
            cases += 1
    return cases


if __name__ == "__main__":
    print(f"PASS: {fejer_checks()} exact Fejer autocorrelation/transport constants.")
    kernels, samples = kernel_checks()
    print(f"PASS: {kernels} exact kernel degree, mass, and product identities; {samples} rational inequality samples.")
    print(f"PASS: {lipschitz_module_identities()} exact multivariate divided-difference and weighted-square identities.")
