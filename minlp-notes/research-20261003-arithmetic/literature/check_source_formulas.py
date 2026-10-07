"""Exact checks of formula-transfer cautions in Hesse's Redemption v1.

These small checks validate the displayed counterexamples and algebraic
normalizations in source-audit.md. They do not refute the main source
theorems or validate the research package's universal claims.
"""

from fractions import Fraction as F
from math import comb, factorial


def compositions(total, width):
    if width == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, width - 1):
            yield (first,) + rest


def check_affine_slope():
    # f(x,t)=x^2-c*t; the printed direction has grad(f)'v=-1.
    for c in (F(2), F(3), F(5, 2)):
        v = 1 / c
        assert -c * v == -1
        assert -v != -c
        repaired_slope = v / (v * v)
        assert repaired_slope == c


def check_one_sided_bound():
    # P={t<=0}, f=x^2-t, Ux=x, lambda=1, z=0, b=0.
    x, t = F(0), F(-1)
    assert t <= 0
    assert t <= 0 + 0 * x
    assert not abs(t) <= 0 + 0 * x

    # On f<=2, the missing lower bound is t>=x^2-2.
    checked = 0
    for i in range(-8, 9):
        for j in range(-16, 1):
            x, t = F(i, 4), F(j, 4)
            if x * x - t <= 2:
                assert x * x - 2 <= t <= 0
                assert abs(t) <= 2
                checked += 1
    return checked


def check_quadratic_normalization():
    # The cited tangent inequality gives lambda/(4D^2), whereas the
    # next display sets mu=lambda/(2D^2). The safe coefficient is mu/2.
    for degree in range(2, 20):
        eigenvalue_lower_bound = F(3, 7)
        coefficient = eigenvalue_lower_bound / (4 * degree**2)
        mu = eigenvalue_lower_bound / (2 * degree**2)
        assert coefficient == mu / 2
        assert 2 * coefficient == mu  # Hessian of coefficient*t^2.


def check_sparse_substitution():
    # f=sum x_i^(2r), U=I-(2/n)11': U is rational orthogonal.
    # Every even monomial of total degree 2r in f(Uy) has positive
    # coefficient. Their count is binomial(n+r-1,r), exponential when
    # r=n/2, although f and U have polynomial encodings.
    checked = 0
    for n in (4, 6, 8):
        r = n // 2
        u = [[F(int(i == j)) - F(2, n) for j in range(n)]
             for i in range(n)]
        for i in range(n):
            for j in range(n):
                assert sum(u[k][i] * u[k][j] for k in range(n)) == int(i == j)
        found = 0
        for beta in compositions(r, n):
            alpha = tuple(2 * b for b in beta)
            denominator = 1
            for a in alpha:
                denominator *= factorial(a)
            coefficient = F(0)
            for row in u:
                term = F(factorial(2 * r), denominator)
                for entry, exponent in zip(row, alpha):
                    term *= entry**exponent
                coefficient += term
            assert coefficient > 0
            found += 1
        assert found == comb(n + r - 1, r)
        checked += found
    return checked


def check_convexity_requirement():
    # For f(t)=-t^2 and level -1, y=0 is outside the sublevel while
    # x=1 is inside; the zero gradient cannot give strict separation.
    level, x, y = F(-1), F(1), F(0)
    assert -(x * x) <= level < -(y * y)
    gradient_at_y = -2 * y
    assert not gradient_at_y * x < gradient_at_y * y


if __name__ == "__main__":
    check_affine_slope()
    sublevel_points = check_one_sided_bound()
    check_quadratic_normalization()
    sparse_coefficients = check_sparse_substitution()
    check_convexity_requirement()
    print("PASS: affine-slope normalization, one-sided bound, quadratic "
          "coefficient, sparse substitution, convexity requirement")
    print(f"Exact fixtures: {sublevel_points} sublevel points; "
          f"{sparse_coefficients} positive even-monomial coefficients")
