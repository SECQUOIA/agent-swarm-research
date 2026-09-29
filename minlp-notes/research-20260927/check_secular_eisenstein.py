"""Targeted exact checks for the explicit secular Eisenstein construction.

The finite checks support, but do not prove, the general modular and local
valuation arguments in secular-eisenstein-review.md.
"""

from math import gcd

import sympy as sp


T, Y = sp.symbols("T Y")


def valuation(integer, prime):
    integer = abs(int(integer))
    if integer == 0:
        return float("inf")
    exponent = 0
    while integer % prime == 0:
        exponent += 1
        integer //= prime
    return exponent


def block(prime, multiplier=None):
    dimension = prime - 1
    kappa = next(k for k in range(1, prime) if (k * k + 1) % prime == 0)
    if multiplier is not None:
        assert multiplier % (prime * prime) == kappa
        kappa = multiplier
    F = sp.Poly(sp.prod(T + i for i in range(1, prime)), T)
    quotients = [F.exquo(sp.Poly(T + i, T)) for i in range(1, prime)]
    P = F * F
    for i, quotient in enumerate(quotients, 1):
        P -= (kappa * i) ** 2 * quotient * quotient

    assert P.degree() == 2 * dimension
    assert P.LC() == 1
    assert all(int(c) % prime == 0 for c in P.all_coeffs()[1:])
    assert valuation(P.TC(), prime) == 1
    assert dimension * kappa * kappa > 1

    # Check the first coefficient with nonzero reduction in the value's
    # convergent p-adic expansion after its constant coefficient.
    coefficients = [sp.Integer(dimension * kappa * kappa - 1)]
    coefficients += [
        (-1) ** (j + 1)
        * kappa * kappa
        * sum(sp.Rational(1, i ** (j - 1)) for i in range(1, prime))
        for j in range(2, dimension + 2)
    ]
    for coefficient in coefficients[:-1]:
        numerator, denominator = sp.fraction(coefficient)
        assert int(numerator) % prime == 0
        assert int(denominator) % prime != 0
    numerator, denominator = sp.fraction(coefficients[-1])
    assert int(numerator) % prime != 0
    assert int(denominator) % prime != 0
    assert gcd(dimension + 1, 2 * dimension) == 1
    return dimension, kappa, F, quotients, P


for prime in [5, 13, 17, 29, 37]:
    dimension, kappa, F, quotients, P = block(prime)
    print(f"p={prime}: degree {P.degree()}, Eisenstein and value-series checks pass")

    if prime == 5:
        # beta = numerator/F at every stationary point. Its resultant has
        # degree eight and the valuation pattern predicted by v_5(beta)=5/8.
        numerator = -T * F.as_expr() - sum(
            (kappa * i) ** 2 * quotient.as_expr()
            for i, quotient in enumerate(quotients, 1)
        )
        resultant = sp.Poly(
            sp.resultant(P.as_expr(), Y * F.as_expr() - numerator, T), Y
        ).primitive()[1]
        assert resultant.degree() == 2 * dimension
        assert valuation(resultant.LC(), prime) == 0
        assert valuation(resultant.TC(), prime) == dimension + 1
        for (degree,), coefficient in resultant.terms():
            assert 2 * dimension * valuation(coefficient, prime) >= (
                2 * dimension - degree
            ) * (dimension + 1)
        assert sp.Poly(resultant, Y, domain=sp.QQ).is_irreducible
        print("p=5: exact degree-eight optimal-value resultant is irreducible")

# Independently check the explicit CRT construction and the simple Hensel
# roots used to make every earlier block split over later local fields.
primes = [5, 13, 17]
for index, prime in enumerate(primes):
    kappa = next(k for k in range(1, prime) if (k * k + 1) % prime == 0)
    later_product = sp.prod(primes[index + 1 :])
    multiplier = kappa * int(later_product) * pow(int(later_product), -1, prime**2)
    dimension, _, _, _, P = block(prime, multiplier)
    for later in primes[index + 1 :]:
        precision = 5
        residues = []
        for i in range(1, prime):
            bi = multiplier * i

            def hensel_function(u, modulus):
                value = u * u - 1
                for j in range(1, prime):
                    if j != i:
                        denominator = j - i + bi * u
                        assert gcd(denominator, modulus) == 1
                        value -= (multiplier * j) ** 2 * u * u * pow(
                            denominator * denominator, -1, modulus
                        )
                return value % modulus

            for sign in [-1, 1]:
                u = sign % later
                power = later
                assert hensel_function(u, later) == 0
                for _ in range(1, precision):
                    residue = hensel_function(u, power * later)
                    assert residue % power == 0
                    correction = -(residue // power) * pow(2 * u, -1, later)
                    u += (correction % later) * power
                    power *= later
                assert hensel_function(u, power) == 0
                root = -i + bi * u
                assert int(P.eval(root)) % (power * later ** (2 * valuation(bi, later))) == 0
                residues.append(root % (later ** (valuation(bi, later) + 1)))
        assert len(set(residues)) == 2 * dimension
        print(f"CRT block p={prime}: {2 * dimension} distinct local branches at q={later}")

print("All targeted secular construction checks passed.")
