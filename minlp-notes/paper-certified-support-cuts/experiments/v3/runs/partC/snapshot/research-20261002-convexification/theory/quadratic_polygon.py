"""Exact quadratic support over a bounded rational two-dimensional polytope.

The graph coordinates are (1, x, y, x*x, x*y, y*y).  A certificate binds
the original bounds, every affine row, and every objective coefficient.
All arithmetic after input conversion uses fractions.Fraction; floating-point
inputs mean their exact binary values.  There is no numerical tolerance.
"""

from fractions import Fraction
from itertools import combinations
import math


SCHEMA = "quadratic-polygon-support-v1"


def rational(value):
    """Read a finite scalar exactly, rejecting booleans and nonfinite floats."""
    if isinstance(value, bool):
        raise ValueError("a boolean is not a rational coefficient")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("coefficients and bounds must be finite")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("expected a finite rational coefficient") from exc


def _problem(bounds, rows, coefficients):
    if len(bounds) != 2 or any(len(pair) != 2 for pair in bounds):
        raise ValueError("bounds must contain two lower/upper pairs")
    if len(coefficients) != 6:
        raise ValueError("coefficients must be (constant, x, y, xx, xy, yy)")
    if any(len(row) != 3 for row in rows):
        raise ValueError("rows must be (a_x, a_y, rhs)")
    box = tuple(tuple(rational(v) for v in pair) for pair in bounds)
    inequalities = tuple(tuple(rational(v) for v in row) for row in rows)
    quadratic = tuple(rational(v) for v in coefficients)
    return box, inequalities, quadratic


def _cross(origin, a, b):
    return (a[0] - origin[0]) * (b[1] - origin[1]) - (
        a[1] - origin[1]
    ) * (b[0] - origin[0])


def _hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return tuple(points)
    lower, upper = [], []
    for point in points:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(points):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return tuple(lower[:-1] + upper[:-1])


def _rows_with_bounds(bounds, rows):
    (lx, ux), (ly, uy) = bounds
    return rows + ((-1, 0, -lx), (1, 0, ux), (0, -1, -ly), (0, 1, uy))


def _feasible(point, rows):
    x, y = point
    return all(a * x + b * y <= rhs for a, b, rhs in rows)


def polygon_vertices(bounds, rows=()):
    """Return exact CCW vertices, two segment ends, one point, or empty tuple.

    Rows are a_x*x + a_y*y <= rhs.  Equality rows must be supplied in both
    directions.  The box makes the polytope bounded, so every nonempty
    feasible set has a vertex defined by two independent active rows.
    """
    box, inequalities, _ = _problem(bounds, rows, (0,) * 6)
    inequalities = _rows_with_bounds(box, inequalities)
    vertices = []
    for (a, b, rhs), (d, e, other_rhs) in combinations(inequalities, 2):
        determinant = a * e - b * d
        if determinant == 0:
            continue
        point = (
            (rhs * e - b * other_rhs) / determinant,
            (a * other_rhs - rhs * d) / determinant,
        )
        if _feasible(point, inequalities):
            vertices.append(point)
    return _hull(vertices)


def quadratic_value(coefficients, point):
    constant, cx, cy, cxx, cxy, cyy = coefficients
    x, y = point
    return constant + cx * x + cy * y + cxx * x * x + cxy * x * y + cyy * y * y


def _candidates(vertices, coefficients, inequalities):
    if not vertices:
        return ()
    candidates = set(vertices)
    constant, cx, cy, cxx, cxy, cyy = coefficients
    if len(vertices) == 2:
        edges = [(vertices[0], vertices[1])]
    elif len(vertices) > 2:
        edges = zip(vertices, vertices[1:] + vertices[:1])
    else:
        edges = []
    for (x, y), (next_x, next_y) in edges:
        dx, dy = next_x - x, next_y - y
        curvature = cxx * dx * dx + cxy * dx * dy + cyy * dy * dy
        slope = cx * dx + cy * dy + 2 * cxx * x * dx + cxy * (
            x * dy + y * dx
        ) + 2 * cyy * y * dy
        if curvature > 0:
            t = -slope / (2 * curvature)
            if 0 < t < 1:
                candidates.add((x + t * dx, y + t * dy))
    determinant = 4 * cxx * cyy - cxy * cxy
    if len(vertices) >= 3 and cxx > 0 and determinant > 0:
        point = (
            (-2 * cyy * cx + cxy * cy) / determinant,
            (cxy * cx - 2 * cxx * cy) / determinant,
        )
        if _feasible(point, inequalities):
            candidates.add(point)
    return tuple(sorted(candidates))


def _serialized_problem(bounds, rows, coefficients):
    return {
        "bounds": [[str(v) for v in pair] for pair in bounds],
        "rows": [[str(v) for v in row] for row in rows],
        "coefficients": [str(v) for v in coefficients],
    }


def support_quadratic(bounds, rows, coefficients):
    """Return a JSON-serializable exact lower-bound certificate.

    A complete certificate contains an attained minimum, not merely a lower
    estimate.  An empty certificate proves the bounded row domain empty.
    Complexity is O(m^3) exact rational operations for m supplied rows,
    dominated by pairwise intersections checked against every row.
    """
    box, inequalities, quadratic = _problem(bounds, rows, coefficients)
    vertices = polygon_vertices(box, inequalities)
    result = {
        "schema": SCHEMA,
        "problem": _serialized_problem(box, inequalities, quadratic),
        "vertices": [[str(v) for v in point] for point in vertices],
    }
    if not vertices:
        result.update(status="empty", bound=None, minimizer=None, candidates=[])
        return result
    candidates = _candidates(vertices, quadratic, _rows_with_bounds(box, inequalities))
    values = [(quadratic_value(quadratic, point), point) for point in candidates]
    bound, minimizer = min(values)
    result.update(
        status="complete",
        bound=str(bound),
        minimizer=[str(v) for v in minimizer],
        candidates=[
            {"point": [str(v) for v in point], "value": str(value)}
            for value, point in values
        ],
    )
    return result


def replay_quadratic(bounds, rows, coefficients, certificate):
    """Check a certificate against trusted original domain and coefficients.

    Re-enumeration checks both the entire bounded domain and completeness of
    the candidate list.  It is deliberately independent of any floating-point
    direction search or nonlinear optimizer.  It shares the exact geometric
    routines with the producer and is not a formally verified proof checker.
    """
    try:
        return isinstance(certificate, dict) and certificate == support_quadratic(
            bounds, rows, coefficients
        )
    except (TypeError, ValueError, KeyError, ZeroDivisionError, OverflowError):
        return False
