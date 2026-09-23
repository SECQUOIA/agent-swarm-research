"""Exact small-degree checks for the fixed-data separator obstruction."""

from fractions import Fraction as Q


def moment(measure, degree):
    return sum(weight * point**degree for point, weight in measure)


def abs_expectation(measure):
    return sum(weight * abs(point) for point, weight in measure)


def check(degree, nu, mu, expected_gap):
    assert all(weight >= 0 for _, weight in nu + mu)
    assert moment(nu, 0) == moment(mu, 0) == 1
    assert all(moment(nu, j) == moment(mu, j) for j in range(degree + 1))
    gap = abs_expectation(mu) - abs_expectation(nu)
    assert gap == expected_gap
    print(f"degree {degree}: exact matched moments and gap {gap}")


check(1, [(Q(0), Q(1))], [(Q(-1), Q(1, 2)), (Q(1), Q(1, 2))], Q(1))
nu = [(Q(-1), Q(1, 8)), (Q(0), Q(3, 4)), (Q(1), Q(1, 8))]
mu = [(Q(-1, 2), Q(1, 2)), (Q(1, 2), Q(1, 2))]
for k in (2, 3):
    check(k, nu, mu, Q(1, 4))

# The exact quadratic error identity supplies the matching analytic upper
# bound: for 0 <= s <= 1, (s-1/2)^2 is between 0 and 1/4.
for s, expected in [(Q(0), Q(1, 8)), (Q(1, 2), Q(-1, 8)), (Q(1), Q(1, 8))]:
    assert s * s + Q(1, 8) - s == (s - Q(1, 2)) ** 2 - Q(1, 8) == expected
print("quadratic error identity checked at all three extrema")
