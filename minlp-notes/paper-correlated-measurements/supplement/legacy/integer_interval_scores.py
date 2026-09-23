"""Integer upper bounds for local noisy-Markov information arc scores.

Exact rational data are rounded outward once. Each subsequent arc calculation
uses integer interval arithmetic only. This component does not build a design
certificate or validate a tangent reference; its contract is to upper-bound
``(F[t] - sum(b[j]*F[t-ages[j]]))' H (...) / variance``.
"""

from dataclasses import dataclass

from certify_noisy_markov import local_coefficients, matrix, rational


def _positive_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(name + " must be a positive integer")
    return value


def _outward(value, grid):
    value = rational(value) * grid
    return (value.numerator // value.denominator,
            -((-value.numerator) // value.denominator))


def _product(left, right):
    a, b = left
    c, d = right
    values = (a*c, a*d, b*c, b*d)
    return min(values), max(values)


def _square(interval):
    a, b = interval
    return (0 if a <= 0 <= b else min(a*a, b*b), max(a*a, b*b))


@dataclass(frozen=True)
class IntegerPattern:
    """Prepared exact-history coefficients, with their integer denominators."""

    ages: tuple
    coefficients: tuple
    variance_lower: int
    coefficient_grid: int
    score_denominator: int

    def __post_init__(self):
        # Validate once, including direct public construction. Immutable tuples
        # prevent a later list mutation from invalidating these checks.
        if (not isinstance(self.ages, tuple) or not isinstance(self.coefficients, tuple)
                or any(isinstance(age, bool) or not isinstance(age, int) or age <= 0
                       for age in self.ages)
                or len(set(self.ages)) != len(self.ages)
                or len(self.ages) != len(self.coefficients)):
            raise ValueError("Pattern ages and coefficients must be matching immutable tuples")
        for interval in self.coefficients:
            if (not isinstance(interval, tuple) or len(interval) != 2
                    or any(isinstance(x, bool) or not isinstance(x, int) for x in interval)
                    or interval[0] > interval[1]):
                raise ValueError("Pattern coefficients must be ordered integer interval pairs")
        _positive_integer(self.variance_lower, "variance_lower")
        _positive_integer(self.coefficient_grid, "coefficient_grid")
        _positive_integer(self.score_denominator, "score_denominator")


class IntegerIntervalScores:
    """Prepare rational inputs, then return guaranteed integer upper scores.

    ``upper(t, pattern) / score_grid`` is an upper bound for the exact arc
    score. F and symmetric H need only be finite rational matrices. H need not
    be positive semidefinite. A positive variance whose grid floor is zero is
    rejected explicitly; the caller can increase coefficient_grid.
    """

    def __init__(self, F, H, *, feature_grid=10**18,
                 coefficient_grid=10**12, score_grid=10**8):
        self.feature_grid = _positive_integer(feature_grid, "feature_grid")
        self.coefficient_grid = _positive_integer(coefficient_grid, "coefficient_grid")
        self.score_grid = _positive_integer(score_grid, "score_grid")
        F, H = matrix(F), matrix(H)
        self.n, self.p = len(F), len(F[0])
        if len(H) != self.p or any(len(row) != self.p for row in H):
            raise ValueError("F and H dimensions differ")
        if any(H[i][j] != H[j][i] for i in range(self.p) for j in range(i)):
            raise ValueError("H must be exactly symmetric")
        self.features = tuple(tuple(_outward(x, feature_grid) for x in row) for row in F)
        self.weights = tuple(tuple(_outward(x, coefficient_grid) for x in row) for row in H)
        self._base_denominator = coefficient_grid**2 * feature_grid**2

    def prepare(self, ages, coefficients, variance):
        """Round one history pattern outward; coefficients follow ages order."""
        ages, coefficients = tuple(ages), tuple(coefficients)
        if (any(isinstance(age, bool) or not isinstance(age, int) or age <= 0 for age in ages)
                or len(set(ages)) != len(ages) or len(ages) != len(coefficients)):
            raise ValueError("History ages must be distinct positive integers matching coefficients")
        variance = rational(variance)
        variance_lower = _outward(variance, self.coefficient_grid)[0]
        if variance_lower <= 0:
            raise ValueError("Variance grid floor must be positive; increase coefficient_grid")
        return IntegerPattern(ages,
                              tuple(_outward(b, self.coefficient_grid) for b in coefficients),
                              variance_lower, self.coefficient_grid,
                              self._base_denominator * variance_lower)

    def prepare_history(self, ages, rho, latent, nugget):
        """Use the reviewed exact scalar filter for one stationary history."""
        ages = tuple(ages)
        if (any(isinstance(age, bool) or not isinstance(age, int) or age <= 0 for age in ages)
                or tuple(sorted(set(ages), reverse=True)) != ages):
            raise ValueError("Stationary history ages must be distinct, positive, and decreasing")
        rho, latent, nugget = map(rational, (rho, latent, nugget))
        if not -1 < rho < 1 or latent < 0 or nugget <= 0:
            raise ValueError("Require abs(rho)<1, latent>=0, and nugget>0")
        coefficients, variance = local_coefficients(tuple(-age for age in ages), 0,
                                                   rho, latent, nugget)
        return self.prepare(ages, coefficients, variance)

    def upper(self, t, pattern):
        """Return an integer upper score; no rational operations occur here."""
        if isinstance(t, bool) or not isinstance(t, int) or not 0 <= t < self.n:
            raise ValueError("Target index is outside F")
        if not isinstance(pattern, IntegerPattern):
            raise TypeError("Expected a prepared IntegerPattern")
        if (pattern.coefficient_grid != self.coefficient_grid
                or pattern.score_denominator != self._base_denominator * pattern.variance_lower):
            raise ValueError("Pattern and scorer grids differ")
        if any(age > t for age in pattern.ages):
            raise ValueError("History precedes the first row of F")
        adjusted = []
        G = self.coefficient_grid
        for j in range(self.p):
            lower, upper = self.features[t][j]
            lower, upper = lower*G, upper*G
            for age, coefficient in zip(pattern.ages, pattern.coefficients):
                term_lower, term_upper = _product(coefficient, self.features[t-age][j])
                lower -= term_upper
                upper -= term_lower
            adjusted.append((lower, upper))
        quadratic_upper = 0
        for i in range(self.p):
            quadratic_upper += _product(self.weights[i][i], _square(adjusted[i]))[1]
            for j in range(i):
                term = _product(self.weights[i][j], _product(adjusted[i], adjusted[j]))[1]
                quadratic_upper += 2*term
        # The nonnegative clamp also makes division by a lower variance safe
        # when the exact H is indefinite and its exact quadratic is negative.
        numerator = max(0, quadratic_upper) * self.score_grid
        return -((-numerator) // pattern.score_denominator)
