"""Small exact-rational checkers for three different optimization outputs.

This is a reference checker, not an optimization algorithm. Global convexity
is verified from an explicit even-affine-power decomposition. Every value
bound is obtained from a checked tangent and the supplied bounding box.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import lcm


def rational(value):
    """Accept exact integer, Fraction, or string input; reject binary floats."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction, str)):
        raise TypeError("use an integer, Fraction, or exact rational string")
    return Fraction(value)


def vector(values, n):
    result = tuple(map(rational, values))
    if len(result) != n:
        raise ValueError("wrong vector dimension")
    return result


def dot(left, right):
    if len(left) != len(right):
        raise ValueError("wrong vector dimension")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


@dataclass(frozen=True)
class Polynomial:
    n: int
    terms: tuple

    def __post_init__(self):
        if type(self.n) is not int or self.n <= 0:
            raise ValueError("the checker supports positive dimension")
        collected = {}
        for powers, coefficient in self.terms:
            powers = tuple(powers)
            if len(powers) != self.n or any(type(p) is not int or p < 0 for p in powers):
                raise ValueError("invalid monomial exponents")
            collected[powers] = collected.get(powers, Fraction(0)) + rational(coefficient)
        object.__setattr__(self, "terms", tuple(sorted((p, c) for p, c in collected.items() if c)))

    @property
    def degree(self):
        return max((sum(p) for p, _ in self.terms), default=0)

    def __add__(self, other):
        if self.n != other.n:
            raise ValueError("polynomial dimensions differ")
        return Polynomial(self.n, self.terms + other.terms)

    def scale(self, scalar):
        scalar = rational(scalar)
        return Polynomial(self.n, tuple((p, c * scalar) for p, c in self.terms))

    def __mul__(self, other):
        if self.n != other.n:
            raise ValueError("polynomial dimensions differ")
        return Polynomial(self.n, tuple((tuple(a + b for a, b in zip(p, q)), c * d)
                                        for p, c in self.terms for q, d in other.terms))

    def power(self, exponent):
        if type(exponent) is not int or exponent < 0:
            raise ValueError("power must be a nonnegative integer")
        result = Polynomial(self.n, (((0,) * self.n, 1),))
        base = self
        while exponent:
            if exponent % 2:
                result = result * base
            exponent //= 2
            if exponent:
                base = base * base
        return result

    def evaluate(self, point):
        point = vector(point, self.n)
        return sum((coefficient * _monomial(point, powers) for powers, coefficient in self.terms), Fraction(0))

    def derivative(self, coordinate):
        if type(coordinate) is not int or not 0 <= coordinate < self.n:
            raise ValueError("invalid derivative coordinate")
        terms = []
        for powers, coefficient in self.terms:
            if powers[coordinate]:
                reduced = list(powers)
                reduced[coordinate] -= 1
                terms.append((tuple(reduced), coefficient * powers[coordinate]))
        return Polynomial(self.n, tuple(terms))

    def gradient(self, point):
        return tuple(self.derivative(i).evaluate(point) for i in range(self.n))


def _monomial(point, powers):
    result = Fraction(1)
    for x, exponent in zip(point, powers):
        result *= x ** exponent
    return result


def affine(linear, offset=0):
    linear = tuple(map(rational, linear))
    n = len(linear)
    terms = [((0,) * n, rational(offset))]
    for i, coefficient in enumerate(linear):
        powers = [0] * n
        powers[i] = 1
        terms.append((tuple(powers), coefficient))
    return Polynomial(n, tuple(terms))


@dataclass(frozen=True)
class EvenPower:
    weight: Fraction
    linear: tuple
    offset: Fraction
    exponent: int

    def expand(self, n):
        weight = rational(self.weight)
        if weight < 0 or type(self.exponent) is not int or self.exponent < 2 or self.exponent % 2:
            raise ValueError("convexity factors need a nonnegative weight and positive even power")
        return affine(vector(self.linear, n), self.offset).power(self.exponent).scale(weight)


@dataclass(frozen=True)
class ConvexityCertificate:
    linear: tuple
    offset: Fraction
    powers: tuple

    def expand(self, n):
        polynomial = affine(vector(self.linear, n), self.offset)
        for term in self.powers:
            polynomial = polynomial + term.expand(n)
        return polynomial

    def verify(self, polynomial):
        if self.expand(polynomial.n) != polynomial:
            raise ValueError("convexity decomposition does not equal the supplied polynomial")


@dataclass(frozen=True)
class Domain:
    lower: tuple
    upper: tuple
    inequalities: tuple = ()  # Additional pairs (normal, upper bound).

    def __post_init__(self):
        lower = tuple(map(rational, self.lower))
        upper = vector(self.upper, len(lower))
        if not lower or any(a > b for a, b in zip(lower, upper)):
            raise ValueError("invalid nonempty bounding intervals")
        inequalities = tuple((vector(row, len(lower)), rational(rhs)) for row, rhs in self.inequalities)
        object.__setattr__(self, "lower", lower)
        object.__setattr__(self, "upper", upper)
        object.__setattr__(self, "inequalities", inequalities)

    @property
    def n(self):
        return len(self.lower)

    def require_feasible(self, point):
        point = vector(point, self.n)
        if any(not lo <= x <= hi for x, lo, hi in zip(point, self.lower, self.upper)):
            raise ValueError("candidate is outside the bounding box")
        if any(dot(row, point) > rhs for row, rhs in self.inequalities):
            raise ValueError("candidate violates a polyhedral constraint")
        return point


@dataclass(frozen=True)
class Problem:
    objective: Polynomial
    convexity: ConvexityCertificate
    domain: Domain

    def verify(self):
        if self.objective.n != self.domain.n:
            raise ValueError("objective and domain dimensions differ")
        self.convexity.verify(self.objective)


@dataclass(frozen=True)
class Witness:
    point: tuple
    tangent_anchor: tuple


@dataclass(frozen=True)
class ValueReport:
    value: Fraction
    lower_bound: Fraction
    gap_bound: Fraction


def value_report(problem, witness):
    """Prove 0 <= f(x)-min_P f <= gap_bound using a box tangent bound.

    The anchor need not be feasible: verified global convexity makes its
    tangent valid everywhere. No asserted optimum or lower bound is accepted.
    """
    problem.verify()
    x = problem.domain.require_feasible(witness.point)
    anchor = vector(witness.tangent_anchor, problem.domain.n)
    gradient = problem.objective.gradient(anchor)
    support = tuple(lo if g >= 0 else hi for g, lo, hi in
                    zip(gradient, problem.domain.lower, problem.domain.upper))
    lower = problem.objective.evaluate(anchor) + dot(gradient, tuple(s - a for s, a in zip(support, anchor)))
    value = problem.objective.evaluate(x)
    return ValueReport(value, lower, value - lower)


def verify_value_gap(problem, witness, tolerance):
    tolerance = rational(tolerance)
    if tolerance < 0:
        raise ValueError("value tolerance must be nonnegative")
    report = value_report(problem, witness)
    if report.gap_bound > tolerance:
        raise ValueError("tangent does not certify the requested objective gap")
    return report


def gradient_coefficient_rows(polynomial):
    """Return the nonzero rows F_beta with (grad f(x))_i=sum_beta F_beta,i x^beta."""
    rows = {}
    for powers, coefficient in polynomial.terms:
        for i, exponent in enumerate(powers):
            if exponent:
                beta = list(powers)
                beta[i] -= 1
                row = rows.setdefault(tuple(beta), [Fraction(0)] * polynomial.n)
                row[i] += coefficient * exponent
    return tuple(tuple(rows[beta]) for beta in sorted(rows) if any(rows[beta]))


def rank_and_kernel(rows, n):
    """Exact rational row reduction; kernel vectors are given in original coordinates."""
    if type(n) is not int or n <= 0:
        raise ValueError("positive column count required")
    matrix = [list(vector(row, n)) for row in rows]
    pivots = []
    for column in range(n):
        next_row = next((i for i in range(len(pivots), len(matrix)) if matrix[i][column]), None)
        if next_row is None:
            continue
        pivot = len(pivots)
        matrix[pivot], matrix[next_row] = matrix[next_row], matrix[pivot]
        divisor = matrix[pivot][column]
        matrix[pivot] = [entry / divisor for entry in matrix[pivot]]
        for i, row in enumerate(matrix):
            if i != pivot:
                multiplier = row[column]
                matrix[i] = [entry - multiplier * value for entry, value in zip(row, matrix[pivot])]
        pivots.append(column)
    basis = []
    for free in (i for i in range(n) if i not in pivots):
        direction = [Fraction(0)] * n
        direction[free] = Fraction(1)
        for row, pivot in enumerate(pivots):
            direction[pivot] = -matrix[row][free]
        basis.append(tuple(direction))
    return len(pivots), tuple(basis)


def _integer_rows(rows):
    denominator = lcm(*(entry.denominator for row in rows for entry in row))
    return denominator, tuple(tuple(int(denominator * entry) for entry in row) for row in rows)


def error_bound(problem):
    """Return (D, Gamma) for dist(x,argmin f) <= Gamma * gap**(1/D), gap<=1.

    Constants follow global-point/sparse-coefficient-degree-extension.md.
    The problem's convexity certificate and all coefficient/domain data are
    checked or read here; no caller-supplied effective constant is trusted.
    """
    problem.verify()
    f, domain = problem.objective, problem.domain
    n, degree = f.n, max(2, f.degree)
    radius = max(Fraction(1), *(abs(x) for x in domain.lower + domain.upper))
    k = radius + 2
    v = sum((abs(coefficient) * k ** sum(powers) for powers, coefficient in f.terms), Fraction(0))
    g = sum((abs(coefficient) * sum(powers) * k ** (sum(powers) - 1)
             for powers, coefficient in f.terms if sum(powers)), Fraction(0))
    h = max(Fraction(1), 2 * v + 2 * g * (1 + radius))
    interpolation = (degree + 1) * degree ** degree
    derivative = (degree + 1) * degree ** (degree + 1)
    c_star = 1 + derivative * (h + 3 ** degree * interpolation)
    r = degree - 1
    coefficient_interpolation = (r + 1) * 2 ** r * r ** r
    rows = gradient_coefficient_rows(f)
    denominator, integer_rows = _integer_rows(rows)
    height = max((1, *(abs(entry) for row in integer_rows for entry in row)))
    for normal, _ in domain.inequalities:
        _, scaled = _integer_rows((normal,))
        height = max(height, *(abs(entry) for row in scaled for entry in row))
    # The box normals have height one. Constraint right-hand sides do not
    # enter the RHS-uniform Hoffman constant.
    gamma = max(Fraction(1), (n * height) ** (n - 1) * denominator * max(1, len(rows))
                * coefficient_interpolation ** n * c_star)
    return degree, gamma


def _point_tolerance(tolerance):
    tolerance = rational(tolerance)
    if not 0 < tolerance <= 1:
        raise ValueError("point tolerance must be in (0,1]")
    return tolerance


def verify_distance_to_set(problem, witness, tolerance):
    """Prove distance <= tolerance to some optimizer; no fixed selection is claimed."""
    tolerance = _point_tolerance(tolerance)
    degree, gamma = error_bound(problem)
    return verify_value_gap(problem, witness, min(Fraction(1), (tolerance / gamma) ** degree))


def minimum_norm_parameters(problem, tolerance):
    tolerance = _point_tolerance(tolerance)
    degree, gamma = error_bound(problem)
    radius = max(Fraction(1), sum((max(abs(lo), abs(hi)) for lo, hi in
                                  zip(problem.domain.lower, problem.domain.upper)), Fraction(0)))
    tau = tolerance ** (2 * degree - 2) / (2 * 8 ** (degree - 1) * radius ** degree * gamma ** degree)
    eta = tau * tolerance ** 2 / 4
    return tau, eta


def regularize(problem, tau):
    problem.verify()
    tau = rational(tau)
    if tau <= 0:
        raise ValueError("regularization must be positive")
    extra = []
    for i in range(problem.objective.n):
        direction = tuple(int(j == i) for j in range(problem.objective.n))
        extra.append(EvenPower(tau, direction, 0, 2))
    certificate = ConvexityCertificate(problem.convexity.linear, problem.convexity.offset,
                                      tuple(problem.convexity.powers) + tuple(extra))
    return Problem(certificate.expand(problem.objective.n), certificate, problem.domain)


def verify_minimum_norm(problem, witness, tolerance):
    """Prove distance <= tolerance to the fixed minimum-Euclidean-norm optimizer.

    The witness's tangent is for f + tau*||x||^2. The returned ValueReport
    therefore concerns that regularized objective, not the original f.
    """
    tau, eta = minimum_norm_parameters(problem, tolerance)
    return verify_value_gap(regularize(problem, tau), witness, eta)
