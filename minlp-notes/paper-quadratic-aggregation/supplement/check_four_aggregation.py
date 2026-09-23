"""Exact finite checks for the credited four-necessary PDLC example.

Uses rational arithmetic in Q(sqrt(2)) and Q(sqrt(5)), with no numerical
sign decisions or third-party dependency. These checks do not establish
the universal perturbation/limit theorem, its external input, or novelty.
"""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Radical:
    """An exact number a + b sqrt(d), for the nonsquares d=2 or d=5."""

    a: F
    b: F
    d: int

    def __post_init__(self):
        assert self.d in (2, 5)
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    def coerce(self, value):
        if isinstance(value, Radical):
            assert value.d == self.d
            return value
        return Radical(F(value), F(0), self.d)

    def __add__(self, other):
        other = self.coerce(other)
        return Radical(self.a + other.a, self.b + other.b, self.d)

    __radd__ = __add__

    def __neg__(self):
        return Radical(-self.a, -self.b, self.d)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        return Radical(
            self.a * other.a + self.d * self.b * other.b,
            self.a * other.b + self.b * other.a,
            self.d,
        )

    __rmul__ = __mul__

    def sign(self):
        """Compare exactly by squaring only nonnegative quantities."""
        if not self.b:
            return (self.a > 0) - (self.a < 0)
        if not self.a:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        difference = self.a * self.a - self.d * self.b * self.b
        comparison = (difference > 0) - (difference < 0)
        return comparison if self.a > 0 else -comparison


def values(s, rho):
    return (-s * s + 1 + rho, s * s + 5 * s - 4 + rho, -s - rho)


def ray_values(s, rho):
    a, b, c = values(s, rho)
    return a, b, a + c, b + c


def sign(value):
    if isinstance(value, Radical):
        return value.sign()
    return (value > 0) - (value < 0)


def equal(left, right):
    return sign(left - right) == 0


# Coefficients in the independent monomials (s^2, s, rho, 1).
rows = ((-1, 0, 1, 1), (1, 5, 1, -4), (0, -1, -1, 0))
weights = (-7, -3, -15)
assert tuple(sum(w * row[j] for w, row in zip(weights, rows))
             for j in range(4)) == (4, 0, 5, 5)
assert values(-3, 4) == (-4, -6, -1)

alpha = Radical(F(-1, 2), F(-1, 2), 5)
beta = Radical(F(-2), F(-2), 2)
assert equal(alpha * alpha + alpha - 1, 0)
assert equal(beta * beta + 4 * beta - 4, 0)
assert alpha.sign() == beta.sign() == -1

witnesses = ((-2, 3), (-4, 8), (alpha, 0), (beta, 0))
expected = (
    (0, -7, -1, -8),
    (-7, 0, -11, -4),
    (alpha, 4 * alpha - 3, 0, 3 * alpha - 3),
    (4 * beta - 3, beta, 3 * beta - 3, 0),
)
for designated, ((s, rho), target) in enumerate(zip(witnesses, expected)):
    actual = ray_values(s, rho)
    assert rho >= 0
    assert all(equal(a, b) for a, b in zip(actual, target))
    assert all(sign(a) == (0 if j == designated else -1)
               for j, a in enumerate(actual))

# The four-ray cone decomposition identity as a coefficient identity in
# (a,b,c,t), rather than a sample of multipliers.
rays = ((1, 0, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1))
coefficient_rows = ((1, 0, 0, -1), (0, 1, -1, 1),
                    (0, 0, 0, 1), (0, 0, 1, -1))
assert tuple(tuple(sum(ray[j] * coeff[k]
                       for ray, coeff in zip(rays, coefficient_rows))
                   for k in range(4)) for j in range(3)) == (
    (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)
)

print("PASS: PDLC polynomial identity, strict feasible point, four exact")
print("radical/rational witness slack vectors, and ray decomposition identity.")
