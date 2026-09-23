"""Exact arithmetic checks for the exploratory quadratic-conflict example.

Run with any Python >=3.10. This validates the displayed rational calculations;
it does not establish novelty or the performance of a separation algorithm.
"""

from fractions import Fraction as F


def g1(x: F, y: F) -> F:
    return x * x + 2 * x * y - F(3, 50)


def g2(x: F, y: F) -> F:
    return 2 * y * y - x * y - F(9, 100)


def ell1(x: F, y: F) -> F:
    return F(4, 5) * x + F(2, 5) * y - F(9, 50)


def ell2(x: F, y: F) -> F:
    return -x + F(3, 5) * y + F(3, 100)


def aggregate(x: F, y: F) -> F:
    return 2 * x * x + 3 * x * y + 2 * y * y - F(21, 100)


def main() -> None:
    x = y = F(1, 5)
    square_x = square_y = F(1, 25)
    product = F(0)

    # Feasibility in the entire termwise convex relaxation on [0,1]^2.
    assert x * x <= square_x <= x
    assert y * y <= square_y <= y
    assert max(F(0), x + y - 1) <= product <= min(x, y)
    assert square_x + 2 * product <= F(3, 50)
    assert 2 * square_y - product <= F(9, 100)

    # Positive definite aggregate, with a rational DD/SOS certificate.
    assert F(2) > abs(F(3, 2))
    assert F(2) * F(2) - F(3, 2) ** 2 == F(7, 4)
    assert aggregate(x, y) == F(7, 100)
    assert 2 * g1(x, y) + g2(x, y) == aggregate(x, y)
    assert aggregate(x, y) == (
        F(1, 2) * x * x + F(1, 2) * y * y
        + F(3, 2) * (x + y) ** 2 - F(21, 100)
    )

    # Explicit lower estimators are justified by these polynomial identities.
    # Each right side is nonnegative for x,y in [1/5,1].
    for x_check in (F(1, 5), F(2, 5), F(1)):
        for y_check in (F(1, 5), F(3, 5), F(1)):
            assert g1(x_check, y_check) - ell1(x_check, y_check) == (
                (x_check - F(1, 5)) ** 2
                + 2 * (x_check - F(1, 5)) * (y_check - F(1, 5))
            )
            assert g2(x_check, y_check) - ell2(x_check, y_check) == (
                2 * (y_check - F(1, 5)) ** 2
                + (1 - y_check) * (x_check - F(1, 5))
            )
            assert aggregate(x_check, y_check) == 2 * g1(x_check, y_check) + g2(x_check, y_check)
    # The note proves the identities algebraically; the above points are checks.
    # The aggregate affine coefficients are positive, so its box minimum is
    # attained at the lower endpoints without any numerical optimizer.
    assert F(3, 5) > 0 and F(7, 5) > 0
    assert 2 * ell1(x, y) + ell2(x, y) == F(7, 100)
    assert 2 * ell1(x, y) + ell2(x, y) == (
        F(3, 5) * x + F(7, 5) * y - F(33, 100)
    )

    # Tangent: (7/5)(x+y) <= 49/100, or x+y <= 7/20.
    assert F(49, 100) / F(7, 5) == F(7, 20)
    assert x + y > F(7, 20)
    assert g1(F(0), F(0)) < 0 and g2(F(0), F(0)) < 0
    assert g1(F(1, 5), F(0)) <= 0 and g2(F(1, 5), F(0)) <= 0
    assert g1(F(0), F(1, 5)) <= 0 and g2(F(0), F(1, 5)) <= 0
    # Exact two-row repair LP solution, including its break-point continuity.
    a_star = F(5, 7)
    q_xx, q_yy = a_star, 2 * (1 - a_star)
    q_xy = a_star - (1 - a_star) / 2
    assert q_xx >= abs(q_xy) and q_yy >= abs(q_xy)
    assert (31 * F(5, 9) - 17) / 20 == (11 * F(5, 9) - 5) / 100
    assert (11 * a_star - 5) / 100 == F(1, 35)
    assert a_star * ell1(x, y) + (1 - a_star) * ell2(x, y) == F(1, 35)
    print("quadratic_conflict_example=ok; rational margin=7/100; tangent=x+y<=7/20")


if __name__ == "__main__":
    main()
