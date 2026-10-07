"""Independent exact review of whole intervals in constrained-star evidence.

Unlike the producer, this diagnostic does not construct envelope switches or
project polygons by vertices.  It projects using lower/upper line pairs and
checks every proposed conditional rule against all feasible stationary and
endpoint rules on their entire parameter intervals.  This is a targeted
review diagnostic, not a general public certificate format or formal proof.
"""

from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "theory"))
from quadratic_star import support_star


def restrict(interval, constant, slope):
    """Intersect an interval with constant + slope*y <= 0 exactly."""
    if interval is None:
        return None
    lo, hi = interval
    if slope > 0:
        hi = min(hi, -constant / slope)
    elif slope < 0:
        lo = max(lo, -constant / slope)
    elif constant > 0:
        return None
    return (lo, hi) if lo <= hi else None


def polynomial_at(coefficients, y):
    return sum(v * y**i for i, v in enumerate(coefficients))


def minimum(polynomial, interval):
    lo, hi = interval
    candidates = [lo, hi]
    if polynomial[2] > 0:
        candidate = -polynomial[1] / (2 * polynomial[2])
        if lo <= candidate <= hi:
            candidates.append(candidate)
    return min((polynomial_at(polynomial, y), y) for y in candidates)


def parts(coefficients, n, center):
    constant = Q(0)
    linear, square, cross = [Q(0)] * n, [Q(0)] * n, [Q(0)] * n
    for powers, raw_coefficient in coefficients.items():
        coefficient = Q(raw_coefficient)
        active = [i for i, power in enumerate(powers) if power]
        if not active:
            constant += coefficient
        elif len(active) == 1:
            i = active[0]
            if powers[i] == 1:
                linear[i] += coefficient
            else:
                assert powers[i] == 2
                square[i] += coefficient
        else:
            assert len(active) == 2 and center in active
            leaf = next(i for i in active if i != center)
            assert powers[leaf] == powers[center] == 1
            cross[leaf] += coefficient
    return constant, linear, square, cross


def pair_rows(bounds, rows, center, leaf):
    # Triple means ay*y + ax*x <= rhs, including both source-variable bounds.
    original = [(Q(0), Q(-1), -bounds[leaf][0]), (Q(0), Q(1), bounds[leaf][1])]
    for coefficients, rhs in rows:
        if coefficients[leaf]:
            assert all(not value or i in (center, leaf) for i, value in enumerate(coefficients))
            original.append((coefficients[center], coefficients[leaf], rhs))
    return original


def bound_lines(rows):
    lower, upper = [], []
    for center_coeff, leaf_coeff, rhs in rows:
        rule = (rhs / leaf_coeff, -center_coeff / leaf_coeff)
        (lower if leaf_coeff < 0 else upper).append(rule)
    return lower, upper


def project(bounds, rows, center):
    # Fourier--Motzkin elimination of each independent scalar leaf.
    if any(lo > hi for lo, hi in bounds):
        return None
    interval = bounds[center]
    for coefficients, rhs in rows:
        if not any(v for i, v in enumerate(coefficients) if i != center):
            interval = restrict(interval, -rhs, coefficients[center])
    for leaf in range(len(bounds)):
        if leaf == center:
            continue
        lower, upper = bound_lines(pair_rows(bounds, rows, center, leaf))
        for lower_rule in lower:
            for upper_rule in upper:
                interval = restrict(interval, lower_rule[0] - upper_rule[0], lower_rule[1] - upper_rule[1])
    return interval


def feasible_rule_interval(rule, rows, interval):
    intercept, slope = rule
    for center_coeff, leaf_coeff, rhs in rows:
        interval = restrict(interval, leaf_coeff * intercept - rhs, center_coeff + leaf_coeff * slope)
    return interval


def conditional_polynomial(rule, linear, square, cross):
    intercept, slope = rule
    return (
        square * intercept**2 + linear * intercept,
        2 * square * intercept * slope + linear * slope + cross * intercept,
        square * slope**2 + cross * slope,
    )


def objective(coefficients, point):
    result = Q(0)
    for powers, coefficient in coefficients.items():
        term = Q(coefficient)
        for value, exponent in zip(point, powers):
            term *= value**exponent
        result += term
    return result


def check_feasible(point, bounds, rows):
    assert len(point) == len(bounds)
    assert all(lo <= value <= hi for value, (lo, hi) in zip(point, bounds))
    assert all(sum(a * v for a, v in zip(coefficients, point)) <= rhs for coefficients, rhs in rows)


def check(bounds, rows, coefficients, center, certificate):
    """Check each returned piece over its entire interval using exact algebra."""
    bounds = tuple(tuple(Q(v) for v in pair) for pair in bounds)
    rows = tuple((tuple(Q(v) for v in a), Q(rhs)) for a, rhs in rows)
    n = len(bounds)
    expected_domain = project(bounds, rows, center)
    if expected_domain is None:
        assert certificate["status"] == "empty"
        return 0
    assert certificate["status"] == "complete"
    assert tuple(map(Q, certificate["center_interval"])) == expected_domain
    constant, linear, square, cross = parts(coefficients, n, center)
    previous_right = expected_domain[0]
    attained_bounds = []
    comparisons = 0
    assert certificate["pieces"]
    for piece in certificate["pieces"]:
        interval = tuple(map(Q, piece["interval"]))
        left, right = interval
        assert left == previous_right and left <= right <= expected_domain[1]
        if expected_domain[0] != expected_domain[1]:
            assert left < right
        previous_right = right
        raw_rules = piece["leaf_rules"]
        rules = {i: (Q(p), Q(r)) for i, p, r in raw_rules}
        assert len(rules) == len(raw_rules) == n - 1
        assert set(rules) == set(range(n)) - {center}
        aggregate = [constant, linear[center], square[center]]
        for leaf, chosen in rules.items():
            original_rows = pair_rows(bounds, rows, center, leaf)
            assert feasible_rule_interval(chosen, original_rows, interval) == interval
            chosen_polynomial = conditional_polynomial(chosen, linear[leaf], square[leaf], cross[leaf])
            for degree in range(3):
                aggregate[degree] += chosen_polynomial[degree]
            lower, upper = bound_lines(original_rows)
            alternatives = lower + upper
            if square[leaf] > 0:
                alternatives.append((-linear[leaf] / (2 * square[leaf]), -cross[leaf] / (2 * square[leaf])))
            for alternative in alternatives:
                valid_interval = feasible_rule_interval(alternative, original_rows, interval)
                if valid_interval is None:
                    continue
                other = conditional_polynomial(alternative, linear[leaf], square[leaf], cross[leaf])
                difference = [a - b for a, b in zip(other, chosen_polynomial)]
                assert minimum(difference, valid_interval)[0] >= 0
                comparisons += 1
        assert tuple(map(Q, piece["polynomial"])) == tuple(aggregate)
        exact_bound, _ = minimum(aggregate, interval)
        assert Q(piece["bound"]) == exact_bound
        point = list(map(Q, piece["minimizer"]))
        assert left <= point[center] <= right
        assert all(point[i] == rule[0] + rule[1] * point[center] for i, rule in rules.items())
        check_feasible(point, bounds, rows)
        assert objective(coefficients, point) == exact_bound
        attained_bounds.append(exact_bound)
    assert previous_right == expected_domain[1]
    if expected_domain[0] == expected_domain[1]:
        assert len(certificate["pieces"]) == 1
    assert Q(certificate["bound"]) == min(attained_bounds)
    point = list(map(Q, certificate["minimizer"]))
    check_feasible(point, bounds, rows)
    assert objective(coefficients, point) == Q(certificate["bound"])
    return comparisons


def corpus():
    # Affine envelope crossings and all signs, including exact endpoint ties.
    bounds = ((-1, 1), (-2, 2), (-2, 2), (-2, 2))
    rows = [((1, -1, 0, 0), 0), ((-1, -1, 0, 0), 0),
            ((1, 1, 0, 0), 2), ((-1, 1, 0, 0), 2),
            ((1, 0, -1, 0), 0), ((-1, 0, 1, 0), 0)]
    for curvature in (-1, 0, 1):
        yield bounds, rows, {(0, 2, 0, 0): curvature, (1, 1, 0, 0): Q(2, 3),
                             (0, 0, 2, 0): -1, (0, 0, 0, 2): 1,
                             (1, 0, 0, 1): -1}, 0
    # Empty projection, singleton center projection, fixed leaf, identically tied leaf.
    yield ((0, 1), (0, 1), (0, 1)), [((1, 1, 0), 0), ((-1, 0, 1), -1)], {}, 0
    yield ((0, 1), (0, 1), (0, 1)), [((1, 1, 0), Q(1, 2)), ((-1, 0, 1), Q(-1, 2))], {(0, 2, 0): -1}, 0
    yield ((0, 1), (Q(2, 3), Q(2, 3))), [], {(0, 2): -1, (1, 1): 1}, 0
    yield ((-1, 1), (0, 1)), [], {(0, 1): 1, (0, 2): -1}, 0
    yield ((-1, 1),), [], {(0,): Q(7, 3), (2,): 2}, 0
    rng = random.Random(140291)
    for trial in range(80):
        n = rng.randint(2, 6)
        center = rng.randrange(n)
        bounds = [(-2, 2)] * n
        coefficients = {(0,) * n: Q(rng.randint(-2, 2), 3)}
        for i in range(n):
            for degree in (1, 2):
                exponent = [0] * n
                exponent[i] = degree
                coefficients[tuple(exponent)] = Q(rng.randint(-4, 4), rng.randint(1, 4))
            if i != center:
                exponent = [0] * n
                exponent[i] = exponent[center] = 1
                coefficients[tuple(exponent)] = Q(rng.randint(-5, 5), rng.randint(1, 3))
        rows = []
        for leaf in range(n):
            if leaf == center:
                continue
            for _ in range(rng.randint(2, 6)):
                row = [0] * n
                row[center], row[leaf] = rng.randint(-4, 4), rng.choice((-3, -2, -1, 1, 2, 3))
                rows.append((tuple(row), Q(rng.randint(1, 5), rng.randint(1, 3))))
            if trial % 9 == 0:
                row = [0] * n
                row[center], row[leaf] = 1, -2
                rows.extend([(tuple(row), 0), (tuple(-v for v in row), 0)])
        if trial % 11 == 0:
            bounds[center] = (0, 0)
        yield bounds, rows, coefficients, center


def main():
    count = empty = pieces = comparisons = 0
    last_case = None
    for bounds, rows, coefficients, center in corpus():
        result = support_star(bounds, rows, coefficients, center)
        comparisons += check(bounds, rows, coefficients, center, result)
        count += 1
        empty += result["status"] == "empty"
        pieces += len(result["pieces"])
        if len(result["pieces"]) > 1:
            last_case = (bounds, rows, coefficients, center, result)
    assert last_case is not None
    bounds, rows, coefficients, center, result = last_case
    mutations = []
    changed = deepcopy(result)
    changed["pieces"].pop(0)
    mutations.append(changed)
    changed = deepcopy(result)
    changed["pieces"][0]["polynomial"][0] = str(Q(changed["pieces"][0]["polynomial"][0]) - 1)
    mutations.append(changed)
    changed = deepcopy(result)
    changed["pieces"][0]["leaf_rules"][0][1] = "1000"
    mutations.append(changed)
    for changed in mutations:
        try:
            check(bounds, rows, coefficients, center, changed)
        except AssertionError:
            pass
        else:
            raise AssertionError("independent interval check accepted a mutation")
    sources = ["theory/README.md", "theory/quadratic_star.py", "theory/quadratic_polygon.py"]
    print(json.dumps({
        "status": "passed", "cases": count, "empty_cases": empty,
        "entire_intervals_checked": pieces,
        "feasible_alternative_comparisons": comparisons,
        "rejected_mutations": len(mutations),
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources},
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
