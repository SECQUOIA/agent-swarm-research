"""Targeted exact checks for the Chebyshev sparse-moment path construction.

No SDP solver is used. Rational Laurent averages reconstruct the local
moments of the real angular-grid probability measures in the proof.
"""

from fractions import Fraction
from math import comb

import sympy as sp


def multiply(left, right):
    result = {}
    for i, a in left.items():
        for j, b in right.items():
            result[i + j] = result.get(i + j, Fraction(0)) + a * b
    return {k: v for k, v in result.items() if v}


def power(poly, degree):
    result = {0: Fraction(1)}
    for _ in range(degree):
        result = multiply(result, poly)
    return result


def cosine(frequency):
    return {frequency: Fraction(1, 2), -frequency: Fraction(1, 2)}


def average(poly, n, sign):
    # Average z^k over roots of z^n=sign. Negative multiples are allowed.
    return sum(
        (value * Fraction(sign) ** (frequency // n)
         for frequency, value in poly.items() if frequency % n == 0),
        Fraction(0),
    )


def q_update(poly):
    result = {k: 2 * value for k, value in multiply(poly, poly).items()}
    result[0] = result.get(0, Fraction(0)) - 1
    return {k: value for k, value in result.items() if value}


def edge_moment(a, b, level, n, sign):
    return average(
        multiply(power(cosine(2 ** (level - 1)), a),
                 power(cosine(2 ** level), b)),
        n,
        sign,
    )


def main():
    matched = constraints = overlaps = 0
    for m in range(1, 8):
        n = 2 ** m
        x = cosine(1)
        for degree in range(n):
            plus = average(power(x, degree), n, 1)
            minus = average(power(x, degree), n, -1)
            expected = (Fraction(comb(degree, degree // 2), 2 ** degree)
                        if degree % 2 == 0 else Fraction(0))
            assert plus == minus == expected
            matched += 1
        assert (average(power(x, n), n, 1)
                - average(power(x, n), n, -1)) == Fraction(1, 2 ** (n - 2))
        for sign in (1, -1):
            assert average(cosine(n), n, sign) == sign
            assert average(power(cosine(n), 2), n, sign) == 1

    for m in range(2, 6):
        n = 2 ** m
        order = min(n // 2 - 1, 4)
        for sign in (1, -1):
            for level in range(1, m + 1):
                for a in range(2 * order - 1):
                    for b in range(2 * order - 1 - a):
                        # L[a^i b^j (b-2a^2+1)] = 0.
                        value = (edge_moment(a, b + 1, level, n, sign)
                                 - 2 * edge_moment(a + 2, b, level, n, sign)
                                 + edge_moment(a, b, level, n, sign))
                        assert value == 0
                        constraints += 1
                if level < m:
                    for degree in range(2 * order + 1):
                        assert (edge_moment(0, degree, level, n, sign)
                                == edge_moment(degree, 0, level + 1, n, sign))
                        overlaps += 1

    perturbed_costs = []
    for m in range(1, 8):
        n = 2 ** m
        delta = Fraction(1, 4 ** m)
        v = {k: (1 - delta) * value for k, value in cosine(2).items()}
        for _ in range(1, m):
            v = q_update(v)
        v_plus_one = dict(v)
        v_plus_one[0] = v_plus_one.get(0, Fraction(0)) + 1
        cost = average(power(v_plus_one, 2), n, -1)
        assert 0 <= cost <= Fraction(1, 16)
        perturbed_costs.append(cost)

    a, b, c, e = sp.symbols("a b c e")
    q = lambda z: 2 * z ** 2 - 1
    d, s = a - b, a + b
    assert sp.expand(4 * d ** 2 - d ** 2 * s ** 2
                     - 2 * d ** 2 * (1 - a ** 2)
                     - 2 * d ** 2 * (1 - b ** 2) - d ** 4) == 0
    assert sp.expand((q(a) - q(b)) ** 2 - 4 * d ** 2 * s ** 2) == 0
    assert sp.expand((c - q(a)) + (q(a) - q(b)) - (c - q(b))) == 0
    assert sp.expand((c - q(b)) - (e - q(b)) - (c - e)) == 0
    assert sp.expand(1 - q(a) ** 2 - 4 * a ** 2 * (1 - a ** 2)) == 0
    delta = sp.symbols("delta")
    g = b - (1 - delta) * a
    assert sp.expand(delta ** 2 - (a - b) ** 2
                     - delta ** 2 * (1 - a ** 2) - g * (2 * delta * a - g)) == 0
    h, k = c - q(a), e - q(b)
    rb, rc = h * (h + 4 * d * s), k * (k - 2 * (c - q(b)))
    assert sp.expand(16 * d ** 2 - (c - e) ** 2
                     - 8 * d ** 2 * (1 - a ** 2)
                     - 8 * d ** 2 * (1 - b ** 2) - 4 * d ** 4 + rb + rc) == 0
    terminal = (a - 1) ** 2 + (b + 1) ** 2 - sp.Rational(49, 32)
    cert = ((a + b) ** 2 / 2 + 4 * (a - b - sp.Rational(1, 4)) ** 2
            + sp.Rational(7, 2) * (sp.Rational(1, 16) - (a - b) ** 2))
    assert sp.expand(terminal - cert) == 0
    quotients = 0
    for degree in range(1, 33):
        p = sp.chebyshevt(degree, b)
        difference = sp.expand(p - p.subs(b, q(a)))
        quotient, remainder = sp.div(difference, b - q(a), b)
        assert remainder == 0
        assert sp.Poly(quotient, a, b).total_degree() <= 2 * degree - 2
        quotients += 1
    print(f"PASS: {matched} exact shared moments, 7 first-difference checks, "
          f"{constraints} equality moments, {overlaps} edge overlaps, "
          f"{quotients} Chebyshev quotient degree checks, "
          "8 width-two/perturbation identities, "
          f"{len(perturbed_costs)} exact perturbed witness costs.")


if __name__ == "__main__":
    main()
