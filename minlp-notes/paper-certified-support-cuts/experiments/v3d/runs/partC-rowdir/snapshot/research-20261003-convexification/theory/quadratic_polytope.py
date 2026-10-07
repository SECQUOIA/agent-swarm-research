"""Exact rational quadratic support over a bounded rational polytope.

Coefficients are ordered as constant, d linear terms, then quadratic terms
(i, j) with 0 <= i <= j < d in lexicographic order. Rows are d coefficients
followed by the right-hand side of a <= inequality. Floats mean their exact
binary rational values. Equalities are two opposite inequalities.

This is a classical active-face enumeration algorithm, not a polynomial-time
algorithm for variable dimension. It also handles empty and lower-dimensional
domains and singular or indefinite quadratic objectives. Replaying a witness
repeats the exact enumeration against trusted inputs; it shares this module's
arithmetic with the producer and is not a formally verified proof checker.
"""

from fractions import Fraction
from itertools import combinations
from math import comb, isfinite


SCHEMA = "quadratic-polytope-support-v1"


class EnumerationLimitError(ValueError):
    """The full exact enumeration exceeds the caller's work budget."""


def rational(value):
    """Convert a finite rational scalar without a tolerance or decimal round."""
    if isinstance(value, bool):
        raise ValueError("booleans are not rational coefficients")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError("coefficients and bounds must be finite")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("expected a finite rational scalar") from exc


def coefficient_pairs(dimension):
    """Return the upper-triangular monomial order after the linear terms."""
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
        raise ValueError("dimension must be a positive integer")
    return tuple((i, j) for i in range(dimension) for j in range(i, dimension))


def _problem(bounds, rows, coefficients):
    box = tuple(tuple(rational(v) for v in pair) for pair in bounds)
    d = len(box)
    pairs = coefficient_pairs(d)
    if any(len(pair) != 2 for pair in box):
        raise ValueError("bounds must contain lower/upper pairs")
    inequalities = tuple(tuple(rational(v) for v in row) for row in rows)
    if any(len(row) != d + 1 for row in inequalities):
        raise ValueError("each row must contain d coefficients and a right-hand side")
    quadratic = tuple(rational(v) for v in coefficients)
    if len(quadratic) != 1 + d + len(pairs):
        raise ValueError("expected constant, linear, and upper-triangular coefficients")
    return box, inequalities, quadratic


def _rows_with_bounds(bounds, rows):
    d = len(bounds)
    full = list(rows)
    for i, (lower, upper) in enumerate(bounds):
        normal = [Fraction(0)] * d
        normal[i] = Fraction(-1)
        full.append(tuple(normal) + (-lower,))
        normal[i] = Fraction(1)
        full.append(tuple(normal) + (upper,))
    return tuple(full)


def _unique_solution(matrix, rhs):
    """Solve a square rational system; return None unless it is nonsingular."""
    n = len(rhs)
    work = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if work[i][col]), None)
        if pivot is None:
            return None
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [value / divisor for value in work[col]]
        for i in range(col + 1, n):
            multiple = work[i][col]
            if multiple:
                work[i] = [a - multiple * b for a, b in zip(work[i], work[col])]
    result = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        result[i] = work[i][-1] - sum(
            (work[i][j] * result[j] for j in range(i + 1, n)), Fraction(0)
        )
    return tuple(result)


def _feasible(point, rows):
    return all(sum((a * x for a, x in zip(row[:-1], point)), Fraction(0)) <= row[-1]
               for row in rows)


def enumeration_size(dimension, row_count):
    """Count all subsets considered, including the two bounds per variable."""
    coefficient_pairs(dimension)
    if isinstance(row_count, bool) or not isinstance(row_count, int) or row_count < 0:
        raise ValueError("row_count must be a nonnegative integer")
    m = row_count + 2 * dimension
    return sum(comb(m, k) for k in range(dimension + 1))


def _check_budget(required, maximum):
    if maximum is None:
        return
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 0:
        raise ValueError("max_faces must be a nonnegative integer or None")
    if required > maximum:
        raise EnumerationLimitError(f"exact enumeration needs {required} subsets; budget is {maximum}")


def polytope_vertices(bounds, rows=(), *, max_faces=None):
    """Return sorted exact vertices, or () for an empty bounded domain.

    A segment returns its endpoints and a point domain returns that point.
    Every vertex of a bounded d-dimensional ambient domain has d independent
    active normals, including when the feasible set has smaller dimension.
    """
    bounds, rows = tuple(bounds), tuple(rows)
    d = len(bounds)
    count = 1 + d + len(coefficient_pairs(d))
    box, inequalities, _ = _problem(bounds, rows, (0,) * count)
    full = _rows_with_bounds(box, inequalities)
    _check_budget(comb(len(full), d), max_faces)
    vertices = set()
    for indices in combinations(range(len(full)), d):
        chosen = [full[i] for i in indices]
        point = _unique_solution([row[:-1] for row in chosen], [row[-1] for row in chosen])
        if point is not None and _feasible(point, full):
            vertices.add(point)
    return tuple(sorted(vertices))


def quadratic_value(coefficients, point):
    """Evaluate coefficients in the documented monomial order exactly."""
    point = tuple(rational(v) for v in point)
    coefficients = tuple(rational(v) for v in coefficients)
    d = len(point)
    pairs = coefficient_pairs(d)
    if len(coefficients) != 1 + d + len(pairs):
        raise ValueError("coefficient count does not match point dimension")
    return coefficients[0] + sum(
        (coefficients[1 + i] * point[i] for i in range(d)), Fraction(0)
    ) + sum(
        (value * point[i] * point[j] for value, (i, j) in zip(coefficients[1 + d:], pairs)),
        Fraction(0),
    )


def _hessian(coefficients, d):
    result = [[Fraction(0)] * d for _ in range(d)]
    for value, (i, j) in zip(coefficients[1 + d:], coefficient_pairs(d)):
        result[i][j] = result[j][i] = 2 * value if i == j else value
    return result


def _stationary(hessian, linear, full, active):
    d, k = len(linear), len(active)
    rows = [full[i] for i in active]
    matrix = [list(hessian[i]) + [row[i] for row in rows] for i in range(d)]
    matrix.extend(list(row[:-1]) + [Fraction(0)] * k for row in rows)
    rhs = [-value for value in linear] + [row[-1] for row in rows]
    solution = _unique_solution(matrix, rhs)
    return None if solution is None else solution[:d]


def support_quadratic(bounds, rows, coefficients, *, max_faces=None):
    """Compute an attained exact minimum and replayable enumeration witness.

    The algorithm considers each subset of at most d affine rows (bounds
    included), solves its bordered stationarity system if nonsingular, and
    retains feasible solutions. A minimum belongs to this candidate set even
    when the ambient Hessian or feasible domain is singular. It never relies
    on numerical rank decisions or constraint qualifications.

    A max_faces budget is checked before enumeration. Exceeding it raises
    EnumerationLimitError and yields no lower-bound claim. The caller should
    impose a small dimension and work budget when using this in a solver.
    """
    box, inequalities, quadratic = _problem(bounds, rows, coefficients)
    d = len(box)
    full = _rows_with_bounds(box, inequalities)
    required = enumeration_size(d, len(inequalities))
    _check_budget(required, max_faces)
    hessian = _hessian(quadratic, d)
    candidates = {}
    counts = {"subsets": required, "singular": 0, "infeasible": 0, "feasible": 0}
    for k in range(d + 1):
        for active in combinations(range(len(full)), k):
            point = _stationary(hessian, quadratic[1:1 + d], full, active)
            if point is None:
                counts["singular"] += 1
            elif not _feasible(point, full):
                counts["infeasible"] += 1
            else:
                counts["feasible"] += 1
                candidates.setdefault(point, active)
    values = [(quadratic_value(quadratic, point), point, active)
              for point, active in sorted(candidates.items())]
    result = {
        "schema": SCHEMA,
        "problem": {
            "bounds": [[str(v) for v in pair] for pair in box],
            "rows": [[str(v) for v in row] for row in inequalities],
            "coefficients": [str(v) for v in quadratic],
        },
        "enumeration": counts,
        "candidates": [
            {"point": [str(v) for v in point], "value": str(value), "active": list(active)}
            for value, point, active in values
        ],
    }
    if values:
        bound, minimizer, _ = min(values)
        result.update(status="complete", bound=str(bound), minimizer=[str(v) for v in minimizer])
    else:
        result.update(status="empty", bound=None, minimizer=None)
    return result


def replay_quadratic(bounds, rows, coefficients, certificate, *, max_faces=None):
    """Recompute the full witness using trusted inputs, not certificate inputs.

    Altered coefficients, rows, domain bounds, omitted candidates, changed
    face counts, and an incorrect optimum are rejected. A checker may bound
    its own work with max_faces; a budget failure returns False.
    """
    try:
        return isinstance(certificate, dict) and certificate == support_quadratic(
            bounds, rows, coefficients, max_faces=max_faces
        )
    except (TypeError, ValueError, KeyError, IndexError, ZeroDivisionError, OverflowError):
        return False
