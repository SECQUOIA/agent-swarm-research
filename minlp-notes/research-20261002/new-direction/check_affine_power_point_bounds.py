"""Exact scalar and completion-budget diagnostics, not a convex solver."""
from fractions import Fraction as F


def main():
    scalar = 0
    values = [F(i, 4) for i in range(-12, 13)]
    for p in (2, 4, 6, 8):
        for s in values:
            for t in values:
                divergence = t**p - s**p - p * s**(p - 1) * (t - s)
                assert divergence >= F(1, 2 ** (p - 2)) * abs(t - s)**p
                scalar += 1

    coefficients = 0
    for p in (2, 4, 6, 8):
        for weight in (F(1, 2**101), F(1, 3), F(1), F(2**103)):
            correction = F(1, 2 ** (p - 2))
            bound = max(F(1), 1 / (weight * correction))
            assert bound**p * weight * correction >= 1
            # This is the exact rational replacement for taking a pth root.
            assert bound.numerator.bit_length() <= 110
            assert bound.denominator.bit_length() <= 110
            coefficients += 1

    rates = 0
    for degree in range(2, 9):
        for radius, gamma in ((F(1), F(1)), (F(7), F(2**120)), (F(2**90), F(5))):
            for q in (0, 1, 12, 80):
                eps = F(1, 2**q)
                tau = eps ** (2 * degree - 2) / (2 ** (3 * degree) * radius**degree * gamma**degree)
                assert tau * radius**2 <= 1
                assert 2 * radius * tau * gamma**degree <= (eps**2 / (8 * radius)) ** (degree - 1)
                for k in (1, 2, 7):
                    beta = F(13, 3)
                    eta = tau * eps**2 / 8
                    delta = tau * eps**2 / (32 * beta * k)
                    # k >= sqrt(k), so this is a conservative rational test.
                    assert eta + 2 * beta * k * delta <= tau * eps**2 / 4
                    rates += 1
    print(f"PASS: {scalar} scalar Bregman inequalities, {coefficients} rational root bounds, {rates} completion budgets")


if __name__ == "__main__":
    main()
