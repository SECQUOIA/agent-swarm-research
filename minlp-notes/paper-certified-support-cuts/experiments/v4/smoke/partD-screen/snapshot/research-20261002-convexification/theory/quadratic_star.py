"""Exact quadratic support on a star with center--leaf affine constraints.

All mixed quadratic terms and all rows must contain at most one leaf besides
the specified center.  Conditional leaf minima are piecewise quadratic in the
center, with rational breakpoints.  This includes box stars as a special case.
"""

from itertools import combinations

try:
    from .quadratic_polygon import polygon_vertices, rational
except ImportError:
    from quadratic_polygon import polygon_vertices, rational


SCHEMA = "quadratic-star-support-v1"


def _normalize(bounds, rows, coefficients, center):
    n = len(bounds)
    if not isinstance(center, int) or isinstance(center, bool) or not 0 <= center < n:
        raise ValueError("center must index one of the variables")
    if any(len(pair) != 2 for pair in bounds):
        raise ValueError("each variable needs finite lower and upper bounds")
    box = tuple(tuple(rational(v) for v in pair) for pair in bounds)
    normalized_rows = []
    for row in rows:
        if len(row) != 2 or len(row[0]) != n:
            raise ValueError("rows must be (coefficient_vector, rhs)")
        a, rhs = tuple(rational(v) for v in row[0]), rational(row[1])
        if sum(v != 0 for i, v in enumerate(a) if i != center) > 1:
            raise ValueError("an affine row may contain at most one leaf")
        normalized_rows.append((a, rhs))
    normalized_coefficients = {}
    for exponent, value in coefficients.items():
        if len(exponent) != n or any(
            not isinstance(e, int) or isinstance(e, bool) or e < 0 for e in exponent
        ) or sum(exponent) > 2:
            raise ValueError("coefficient keys must be quadratic monomial exponents")
        coefficient = rational(value)
        if not coefficient:
            continue
        support = [i for i, e in enumerate(exponent) if e]
        if len(support) == 2 and center not in support:
            raise ValueError("a mixed quadratic term may contain at most one leaf")
        normalized_coefficients[tuple(exponent)] = coefficient
    return box, tuple(normalized_rows), normalized_coefficients


def _polynomial_parts(n, center, coefficients):
    constant, linear, square, cross = rational(0), [rational(0)] * n, [rational(0)] * n, [rational(0)] * n
    for exponent, coefficient in coefficients.items():
        support = [i for i, e in enumerate(exponent) if e]
        if not support:
            constant += coefficient
        elif len(support) == 1:
            i = support[0]
            (linear if exponent[i] == 1 else square)[i] += coefficient
        else:
            leaf = next(i for i in support if i != center)
            cross[leaf] += coefficient
    return constant, linear, square, cross


def _at(line, y):
    return line[0] + line[1] * y


def _active_bounds(lower, upper, y):
    return max(lower, key=lambda line: (_at(line, y), line)), min(
        upper, key=lambda line: (_at(line, y), line)
    )


def _conditional_argmin(y, lower, upper, linear, square, cross):
    """An affine leaf minimizer valid throughout a regime around y."""
    lo, hi = _active_bounds(lower, upper, y)
    if square > 0:
        free = (-linear / (2 * square), -cross / (2 * square))
        if _at(free, y) <= _at(lo, y):
            return lo
        if _at(free, y) >= _at(hi, y):
            return hi
        return free
    lower_value = square * _at(lo, y) ** 2 + (linear + cross * y) * _at(lo, y)
    upper_value = square * _at(hi, y) ** 2 + (linear + cross * y) * _at(hi, y)
    return lo if lower_value <= upper_value else hi


def _root_inside(constant, slope, lo, hi):
    if not slope:
        return []
    root = -constant / slope
    return [root] if lo < root < hi else []


def _leaf_breakpoints(lo, hi, lower, upper, linear, square, cross):
    breaks = {lo, hi}
    lines = lower + upper
    for first, second in combinations(lines, 2):
        breaks.update(_root_inside(first[0] - second[0], first[1] - second[1], lo, hi))
    envelope_breaks = sorted(breaks)
    for left, right in zip(envelope_breaks, envelope_breaks[1:]):
        low, high = _active_bounds(lower, upper, (left + right) / 2)
        if square > 0:
            for bound in (low, high):
                breaks.update(_root_inside(
                    -linear - 2 * square * bound[0],
                    -cross - 2 * square * bound[1], left, right,
                ))
        else:
            breaks.update(_root_inside(
                square * (low[0] + high[0]) + linear,
                square * (low[1] + high[1]) + cross, left, right,
            ))
    return breaks


def _domain(bounds, rows, center):
    lo, hi = bounds[center]
    if any(lower > upper for lower, upper in bounds):
        return None
    leaves = [i for i in range(len(bounds)) if i != center]
    leaf_rows = {i: [] for i in leaves}
    for a, rhs in rows:
        support = [i for i in leaves if a[i]]
        if support:
            i = support[0]
            leaf_rows[i].append((a[center], a[i], rhs))
        elif a[center] > 0:
            hi = min(hi, rhs / a[center])
        elif a[center] < 0:
            lo = max(lo, rhs / a[center])
        elif rhs < 0:
            return None
    if lo > hi:
        return None
    envelopes, projections = {}, {}
    for i in leaves:
        polygon = polygon_vertices(((lo, hi), bounds[i]), leaf_rows[i])
        if not polygon:
            return None
        left, right = min(p[0] for p in polygon), max(p[0] for p in polygon)
        projections[i] = (left, right)
        lower = [(bounds[i][0], rational(0))]
        upper = [(bounds[i][1], rational(0))]
        for ay, ax, rhs in leaf_rows[i]:
            line = (rhs / ax, -ay / ax)
            (lower if ax < 0 else upper).append(line)
        envelopes[i] = (tuple(sorted(set(lower))), tuple(sorted(set(upper))))
    lo = max([lo] + [pair[0] for pair in projections.values()])
    hi = min([hi] + [pair[1] for pair in projections.values()])
    return None if lo > hi else (lo, hi, envelopes)


def _bound_polynomial(lo, hi, polynomial):
    constant, linear, square = polynomial
    candidates = [lo, hi]
    if square > 0:
        stationary = -linear / (2 * square)
        if lo < stationary < hi:
            candidates.append(stationary)
    return min((constant + linear * y + square * y * y, y) for y in candidates)


def support_star(bounds, rows, coefficients, center=0):
    """Certify the exact minimum, with all scalars interpreted rationally.

    ``coefficients`` maps exponent tuples to coefficients; ``rows`` contains
    ``(a_vector, rhs)`` for a_vector*x <= rhs.  All nonzero mixed monomials and
    all rows must be supported on the center plus at most one leaf.  The
    returned JSON-compatible certificate includes original-input binding,
    the complete rational center partition, conditional minimizers, and an
    attained global minimum.  No discretization or numerical root finder is
    used.  Unsupported coupling raises ValueError rather than being dropped.
    """
    box, normalized_rows, polynomial = _normalize(bounds, rows, coefficients, center)
    n = len(box)
    result = {
        "schema": SCHEMA,
        "problem": {
            "bounds": [[str(v) for v in pair] for pair in box],
            "rows": [[[str(v) for v in a], str(rhs)] for a, rhs in normalized_rows],
            "coefficients": [[list(exponent), str(value)] for exponent, value in sorted(polynomial.items())],
            "center": center,
        },
    }
    domain = _domain(box, normalized_rows, center)
    if domain is None:
        result.update(status="empty", bound=None, minimizer=None, pieces=[])
        return result
    lo, hi, envelopes = domain
    constant, linear, square, cross = _polynomial_parts(n, center, polynomial)
    leaves = [i for i in range(n) if i != center]
    breaks = {lo, hi}
    for i, (lower, upper) in envelopes.items():
        breaks.update(_leaf_breakpoints(lo, hi, lower, upper, linear[i], square[i], cross[i]))
    breaks = sorted(breaks)
    intervals = list(zip(breaks, breaks[1:])) if lo < hi else [(lo, hi)]
    pieces, attained = [], []
    for left, right in intervals:
        midpoint = (left + right) / 2
        leaf_rules = {
            i: _conditional_argmin(midpoint, *envelopes[i], linear[i], square[i], cross[i])
            for i in leaves
        }
        value_polynomial = [constant, linear[center], square[center]]
        for i, (intercept, slope) in leaf_rules.items():
            value_polynomial[0] += linear[i] * intercept + square[i] * intercept * intercept
            value_polynomial[1] += linear[i] * slope + 2 * square[i] * intercept * slope + cross[i] * intercept
            value_polynomial[2] += square[i] * slope * slope + cross[i] * slope
        bound, y = _bound_polynomial(left, right, value_polynomial)
        point = [rational(0)] * n
        point[center] = y
        for i in leaves:
            point[i] = _at(leaf_rules[i], y)
        attained.append((bound, point))
        pieces.append({
            "interval": [str(left), str(right)],
            "leaf_rules": [[i, str(leaf_rules[i][0]), str(leaf_rules[i][1])] for i in leaves],
            "polynomial": [str(v) for v in value_polynomial],
            "bound": str(bound),
            "minimizer": [str(v) for v in point],
        })
    bound, minimizer = min(attained)
    result.update(
        status="complete", bound=str(bound), minimizer=[str(v) for v in minimizer],
        center_interval=[str(lo), str(hi)], pieces=pieces,
    )
    return result


def replay_star(bounds, rows, coefficients, center, certificate):
    """Replay exact partition and objective binding against trusted inputs."""
    try:
        return isinstance(certificate, dict) and certificate == support_star(
            bounds, rows, coefficients, center
        )
    except (TypeError, ValueError, KeyError, AttributeError, ZeroDivisionError, OverflowError):
        return False
