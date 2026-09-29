"""Targeted exact checks for the cyclic strongly convex quartic family.

Uses rational arithmetic and symbolic identities. It does not replace
the universal curvature proof or establish publication novelty.
"""

from fractions import Fraction as F
from math import factorial

import sympy as sp


def family_data(n):
    m = n + 1
    sigma = (-1) ** m
    degree = (2 ** m - sigma) // 3
    exponents = [((-2) ** i - 1) // 3 for i in range(m)]
    wraps = [0] * (m - 2) + [sigma, -sigma]
    return m, degree, exponents, wraps


def parameters(n):
    m = n + 1
    scale = 10 ** 6 * n ** 5
    eps = F(1, scale ** 2)
    denominator = 32 * m * scale ** 2
    mu = F(1, 16 * n ** 2)
    nu = F(1, 8 * n)
    bound = 9 + 8 * m
    assert bound <= 17 * n
    assert eps <= min(F(1), mu ** 2 / (2 * m), nu ** 2 * mu ** 2 / (36 * n * bound ** 2))
    assert F(m, denominator) <= F(1, 16 * n ** 2)
    assert F(8 * m, denominator) <= eps / 4
    assert F(3 * denominator ** 2, 32 * scale ** 2 * n ** 2) >= 1
    gram_quartic = 2 * mu ** 2
    gram_schur = F(3, 2) * eps * nu ** 2
    gram_cross = 6 * n * eps * bound
    assert gram_schur < gram_quartic
    assert gram_cross / gram_quartic < 1
    assert gram_schur / (36 * n ** 2) == F(1, 1536 * scale ** 2 * n ** 4)
    assert F(1, 128 * n ** 2) - eps / 4 > 0
    return scale, denominator


def weight_approximation(exponent, degree, denominator):
    count = 1
    while 9 ** count < 256 * denominator:
        count += 1
    log_approx = 2 * sum((F(1, 3 ** (2 * j + 1) * (2 * j + 1)) for j in range(count)), F(0))
    multiplier = F(-2 * exponent, degree)
    argument = multiplier * log_approx
    assert abs(argument) < 2
    order = 2
    while F(2 ** (order + 2), factorial(order + 1)) > F(1, 8 * denominator):
        order += 1
    approximation = sum((argument ** j / factorial(j) for j in range(order + 1)), F(0))
    error = 9 * abs(multiplier) * F(1, 9 ** count) + F(2 ** (order + 2), factorial(order + 1))
    assert error < F(1, 4 * denominator)
    rounded = (denominator * approximation + F(1, 2)).__floor__()
    assert abs(F(rounded, denominator) - approximation) + error < F(1, denominator)
    # Independent algebraic check for this finite example. The true
    # positive weight satisfies w^degree = 2^(-2*exponent).
    low, high = approximation - error, approximation + error
    target = F(2) ** (-2 * exponent)
    assert low > 0 and low ** degree <= target <= high ** degree
    return rounded


def symbolic_structure(n):
    m, degree, exponents, wraps = family_data(n)
    assert degree % 2 == 1
    assert exponents[1] == -1
    assert all(abs(s) < degree for s in exponents)
    for i in range(m):
        assert 2 * exponents[i] - exponents[(i + 1) % m] - exponents[(i + 2) % m] == degree * wraps[i]
    shift = sp.zeros(m)
    for i in range(m):
        shift[i, (i + 1) % m] = 1
    jacobian = 2 * sp.eye(m) - shift - shift ** 2
    assert jacobian == (2 * sp.eye(m) + shift) * (sp.eye(m) - shift)
    assert jacobian[1:, 1:].det() == degree

    variables = (sp.Integer(1),) + sp.symbols(f'X1:{m}')
    residuals = [variables[i] ** 2 - variables[(i + 1) % m] * variables[(i + 2) % m] for i in range(m)]
    energy = sum((variables[i] - variables[(i + 1) % m]) ** 2 for i in range(m)) / 2
    assert sp.expand(sum(residuals) - energy) == 0
    actual_jacobian = sp.Matrix(residuals).jacobian(variables[1:]).subs(dict.fromkeys(variables[1:], 1))
    assert actual_jacobian == jacobian[:, 1:]


def integer_output(n):
    m, degree, exponents, wraps = family_data(n)
    scale, denominator = parameters(n)
    weights = [weight_approximation(s, degree, denominator) for s in exponents]
    variables = (sp.Integer(1),) + sp.symbols(f'x1:{m}')
    residuals = [variables[i] ** 2 - sp.Rational(2) ** wraps[i] * variables[(i + 1) % m] * variables[(i + 2) % m] for i in range(m)]
    main = 2 * sum(z * q for z, q in zip(weights, residuals))
    assert (2 * denominator) % scale == 0
    factors = [main] + [(2 * denominator // scale) * q for q in residuals]
    for factor in factors:
        assert all(coefficient.q == 1 for coefficient in sp.Poly(factor, *variables[1:]).coeffs())
    quartic = sp.Poly(sum(factor ** 2 for factor in factors), *variables[1:])
    assert quartic.total_degree() == 4
    assert all(coefficient.q == 1 for coefficient in quartic.coeffs())
    # Translation cannot introduce irrational coefficients or lose degree.
    translated = sp.Poly(quartic.as_expr().subs(variables[1], variables[1] - 1), *variables[1:])
    assert translated.total_degree() == 4
    assert all(coefficient.q == 1 for coefficient in translated.coeffs())
    t = sp.Symbol('t')
    minimal = sp.Poly(2 * (t - 1) ** degree - 1, t)
    assert len(minimal.terms()) == degree + 1
    assert minimal.TC() == -3
    return degree, len(quartic.terms()), max(abs(int(c)).bit_length() for c in quartic.coeffs())


if __name__ == '__main__':
    for n in range(2, 81):
        parameters(n)
    for n in range(2, 13):
        symbolic_structure(n)
    outputs = [(n, *integer_output(n)) for n in range(2, 7)]
    print('Passed: parameter bounds n=2..80; cyclic/Jacobian/energy identities n=2..12.')
    print('Certified integer outputs (n, algebraic degree, monomials, maximum coefficient bits):')
    for row in outputs:
        print(row)
