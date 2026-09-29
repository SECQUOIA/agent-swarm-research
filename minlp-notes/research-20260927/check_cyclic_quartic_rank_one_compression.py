"""Independent exact checks of the cyclic family's rational SOS compression.

This checks the new rank-one factorization, parameter range, and actual
integer output. The universal proof is in the companion review.
"""

from fractions import Fraction as F

import sympy as sp

from check_cyclic_quartic_exponential_degree import (
    family_data,
    parameters,
    weight_approximation,
)


def choose_r(radius_squared, scale, residual_count):
    target = F(3, 2 * scale)
    low, high = F(1, 8), F(8 * residual_count)

    def parameter(r):
        return (radius_squared - r * r) / (2 * r)

    assert parameter(low) > F(2, scale)
    assert parameter(high) < 0
    while high - low > F(1, 4000 * residual_count * scale):
        midpoint = (low + high) / 2
        if parameter(midpoint) > target:
            low = midpoint
        else:
            high = midpoint
    r = (low + high) / 2
    t = parameter(r)
    assert F(1, scale) < t < F(2, scale)
    assert r.denominator & (r.denominator - 1) == 0
    return r, t


def compression_parameters(n):
    scale, _ = parameters(n)
    m = n + 1
    mu, nu = F(1, 16 * n * n), F(1, 8 * n)
    bound = 9 + 8 * m
    largest_eps = F(4, scale * scale)
    assert largest_eps <= min(
        F(1), mu * mu / (2 * m), nu * nu * mu * mu / (36 * n * bound * bound)
    )
    assert F(3, 2) * F(1, scale * scale) * nu * nu * (16 * scale * n) ** 2 == 6


def compressed_output(n):
    scale, denominator = parameters(n)
    m, degree, exponents, wraps = family_data(n)
    z = [weight_approximation(s, degree, denominator) for s in exponents]
    integer_radius = sum(v * v for v in z)
    radius_squared = F(integer_radius, denominator * denominator)
    assert F(m, 25) < radius_squared < 25 * m
    r, t = choose_r(radius_squared, scale, m)
    a, b = r.numerator, r.denominator
    s = (radius_squared + r * r) / (2 * r)
    assert s * s == t * t + radius_squared
    assert s + t == radius_squared / r
    z_vector = sp.Matrix(z)
    g = z_vector / denominator
    transform = sp.Rational(t.numerator, t.denominator) * sp.eye(m)
    transform += sp.Rational(a, b * integer_radius) * z_vector * z_vector.T
    assert transform * transform == sp.Rational(t * t) * sp.eye(m) + g * g.T

    common_denominator = 2 * a * b * denominator * denominator * integer_radius
    assert all((entry * common_denominator).q == 1 for entry in transform)
    variables = (sp.Integer(1),) + sp.symbols(f'x1:{m}')
    residuals = sp.Matrix([
        variables[i] ** 2 - sp.Rational(2) ** wraps[i]
        * variables[(i + 1) % m] * variables[(i + 2) % m]
        for i in range(m)
    ])
    integer_multiplier = 32 * scale * n * common_denominator
    factors = integer_multiplier * transform * residuals
    assert len(factors) == n + 1
    for factor in factors:
        assert all(c.q == 1 for c in sp.Poly(factor, *variables[1:]).coeffs())
    quartic = sp.Poly(sum(factor * factor for factor in factors), *variables[1:])
    expected = integer_multiplier ** 2 * (
        (g.dot(residuals)) ** 2 + sp.Rational(t * t) * residuals.dot(residuals)
    )
    assert sp.expand(quartic.as_expr() - expected) == 0
    assert quartic.total_degree() == 4
    assert all(c.q == 1 for c in quartic.coeffs())
    return (
        n,
        degree,
        len(factors),
        len(quartic.terms()),
        max(abs(int(c)).bit_length() for c in quartic.coeffs()),
    )


if __name__ == '__main__':
    for dimension in range(2, 81):
        compression_parameters(dimension)
    rows = [compressed_output(dimension) for dimension in range(2, 7)]
    print('Passed: fourfold regularization range and scaling for n=2..80.')
    print('Exact compressed output (n, degree, factors, monomials, maximum coefficient bits):')
    for row in rows:
        print(row)
