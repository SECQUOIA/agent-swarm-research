"""Exact-rational regression checks for the prescribed integer-noise theorem.

Small domains permit independent enumeration of original optima and exact
minimization of every quadratic well on each processed auxiliary cell.
These deterministic checks do not estimate an expected running time.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
from math import prod


@dataclass(frozen=True)
class Case:
    name: str
    terms: tuple
    bounds: tuple
    rows: tuple
    alpha: Q = Q(1)
    sigmas: tuple = (Q(1),)


def polynomial(coefficients, x):
    answer = Q(0)
    for coefficient in reversed(coefficients):
        answer = answer * x + coefficient
    return answer


def coordinate(coefficients, bounds, shift):
    lower, upper = bounds

    def value(z):
        return polynomial(coefficients, z) - shift * z

    left, right = lower, upper
    while left < right:
        middle = (left + right) // 2
        if value(middle + 1) - value(middle) >= 0:
            right = middle
        else:
            left = middle + 1
    assert left == lower or value(left) <= value(left - 1)
    assert left == upper or value(left) <= value(left + 1)
    return left


def projection(case, point):
    return tuple(sum(t * x for t, x in zip(row, point)) for row in case.rows)


def original(case, point, noise):
    projected = projection(case, point)
    return (sum(polynomial(g, x) for g, x in zip(case.terms, point))
            - case.alpha * sum(t * t for t in projected) / 2
            + sum(d * t for d, t in zip(noise, projected)))


def denominator(case):
    rationals = [case.alpha, *case.sigmas]
    rationals.extend(c for term in case.terms for c in term)
    rationals.extend(t for row in case.rows for t in row)
    common = prod(Q(value).denominator for value in rationals)
    return 2 * common**3


def parameters(case):
    lower, widths = [], []
    for row, sigma in zip(case.rows, case.sigmas):
        row_low = sum(min(t * lo, t * hi) for t, (lo, hi) in zip(row, case.bounds))
        row_high = sum(max(t * lo, t * hi) for t, (lo, hi) in zip(row, case.bounds))
        lower.append(row_low - sigma / case.alpha)
        widths.append(row_high - row_low + 2 * sigma / case.alpha)
    d0 = denominator(case)
    threshold = max(Q(2), len(case.rows) * case.alpha * max(widths)**2 * d0)
    size, levels = 2, 1
    while size < threshold:
        size *= 2
        levels += 1
    assert size == 2**levels
    assert size == 2 or size // 2 < threshold
    return tuple(lower), tuple(widths), d0, size, levels


def check_solver(case, indices, counts):
    lower, widths, d0, size, terminal = parameters(case)
    rank = len(case.rows)
    noise = tuple(-sigma + 2 * sigma * k / (size - 1)
                  for sigma, k in zip(case.sigmas, indices))
    points = tuple(product(*(range(lo, hi + 1) for lo, hi in case.bounds)))
    values = {x: original(case, x, noise) for x in points}
    optimum = min(values.values())
    counts["tied_draws"] += sum(v == optimum for v in values.values()) > 1
    for value in values.values():
        assert (d0 * (size - 1) * value).denominator == 1
        counts["lattice_values"] += 1
    shift = sum(d * d for d in noise) / (2 * case.alpha)
    auxiliary_optimum = optimum - shift
    centers = {x: tuple(t - d / case.alpha
                        for t, d in zip(projection(case, x), noise)) for x in points}

    def oracle(a):
        witness = tuple(coordinate(g, bounds, case.alpha * sum(row[j] * ai
                            for row, ai in zip(case.rows, a)))
                        for j, (g, bounds) in enumerate(zip(case.terms, case.bounds)))
        value = (values[witness]
                 + case.alpha * sum((ai - c)**2 for ai, c in zip(a, centers[witness])) / 2
                 - shift)
        brute = min(values[x] + case.alpha * sum((ai - c)**2
                    for ai, c in zip(a, centers[x])) / 2 - shift for x in points)
        assert value == brute
        assert values[witness] <= value + shift
        return value, witness

    def cell_minimum(lo, hi):
        return min(values[x] + case.alpha * sum(
            (c - min(b, max(a, c)))**2
            for a, b, c in zip(lo, hi, centers[x])) / 2 - shift for x in points)

    retained = [tuple(0 for _ in widths)]
    previous = (1,) * rank
    incumbent = witness = None
    for level in range(terminal + 1):
        counts["levels"] += 1
        target = max(widths) / 2**level
        divisions = []
        for width in widths:
            pieces = 1
            while width / pieces > target:
                pieces *= 2
            assert pieces <= 2**level <= size
            divisions.append(pieces)
        steps = tuple(w / m for w, m in zip(widths, divisions))
        correction = case.alpha * sum(h * h for h in steps) / 8
        if level:
            children = []
            for index in retained:
                choices = [(2 * pos, 2 * pos + 1) if new == 2 * old else (pos,)
                           for pos, new, old in zip(index, divisions, previous)]
                children.extend(product(*choices))
            retained = children
        bounds = []
        for index in retained:
            lo = tuple(a + pos * h for a, pos, h in zip(lower, index, steps))
            hi = tuple(a + h for a, h in zip(lo, steps))
            corner_values = []
            for mask in product((0, 1), repeat=rank):
                corner = tuple(a + bit * h for a, bit, h in zip(lo, mask, steps))
                value, point = oracle(corner)
                corner_values.append(value)
                if incumbent is None or value < incumbent:
                    incumbent, witness = value, point
                counts["corner_calls"] += 1
            bound = min(corner_values) - correction
            assert bound <= cell_minimum(lo, hi)
            bounds.append((index, bound, min(corner_values)))
            counts["processed_cells"] += 1
        survivors = [(index, bound, corner) for index, bound, corner in bounds
                     if bound <= incumbent]
        assert survivors
        certified_lower = min(bound for _, bound, _ in survivors)
        assert certified_lower <= auxiliary_optimum <= incumbent
        assert incumbent - certified_lower <= correction
        assert all(corner <= auxiliary_optimum + 2 * correction
                   for _, _, corner in survivors)
        assert certified_lower + shift <= optimum <= values[witness] <= incumbent + shift
        assert values[witness] - optimum <= correction
        retained = [index for index, _, _ in survivors]
        previous = divisions

    assert correction <= Q(1, 8 * d0 * size) < Q(1, 2 * d0 * (size - 1))
    assert values[witness] == optimum
    counts["draws"] += 1


def main():
    counts = dict(oracle_cases=0, wide_interval_cases=0, rational_lattice_values=0, fixtures=0, draws=0,
                  tied_draws=0, levels=0, processed_cells=0, corner_calls=0,
                  lattice_values=0)
    # Canonical convex quartics and affine/singleton degeneracies.
    for quartic, quadratic, linear, bounds, shift in product(
            (0, 1), (0, 2), (-3, 0, 3), ((-3, 2), (0, 0), (-1, 3)),
            (Q(-5, 3), Q(0), Q(7, 2))):
        coefficients = (Q(1, 3), linear, quadratic, 0, quartic)
        candidate = coordinate(coefficients, bounds, shift)
        assert polynomial(coefficients, candidate) - shift * candidate == min(
            polynomial(coefficients, z) - shift * z
            for z in range(bounds[0], bounds[1] + 1))
        counts["oracle_cases"] += 1
    # General convex-on-domain polynomials, including cubic and negative quadratic terms.
    for coefficients, bounds in (((1, -4, 6, -4, 1), (-2, 3)),
                                  ((0, 0, -1, 0, 1), (1, 3)),
                                  ((0, 0, 0, 1), (0, 3)),
                                  ((0, 0, 0, -1), (-3, 0))):
        for shift in (Q(-4), Q(0), Q(4), Q(11, 3)):
            candidate = coordinate(coefficients, bounds, shift)
            assert polynomial(coefficients, candidate) - shift * candidate == min(
                polynomial(coefficients, z) - shift * z
                for z in range(bounds[0], bounds[1] + 1))
            counts["oracle_cases"] += 1

    center = 2**80
    assert coordinate((center**2, -2 * center, 1), (-2**100, 2**100), Q(0)) == center
    counts["wide_interval_cases"] += 1

    # Rational base denominators are checked without generating a huge auxiliary grid.
    rational = Case("rational_lattice", ((Q(1, 3), Q(2, 5), Q(1, 7)), (0, 0, 0, 0, Q(1, 2))),
                    ((-1, 1), (0, 2)), ((Q(1, 2), Q(-2, 5)), (Q(-1, 3), Q(1, 4))),
                    Q(2, 3), (Q(3, 7), Q(2, 5)))
    d0 = denominator(rational)
    for size in (2, 4, 8):
        for indices in product(range(size), repeat=2):
            noise = tuple(-s + 2 * s * k / (size - 1)
                          for s, k in zip(rational.sigmas, indices))
            for point in product(range(-1, 2), range(3)):
                assert (d0 * (size - 1) * original(rational, point, noise)).denominator == 1
                counts["rational_lattice_values"] += 1

    fixtures = (
        Case("rank_one_endpoint_tie", ((0,),), ((0, 2),), ((1,),)),
        Case("rank_one_cubic_quartic", ((1, -4, 6, -4, 1),), ((0, 2),), ((-1,),)),
        Case("rank_two_signed", ((0, 0, 1), (0, 0, 0, 0, 1)),
             ((0, 1), (0, 1)), ((1, -1), (-1, -1)), sigmas=(Q(1), Q(1))),
        Case("rank_two_constant_row", ((0, 0, 0, 1), (0,)),
             ((0, 2), (1, 1)), ((1, 1), (0, 1)), sigmas=(Q(1), Q(1))),
        Case("rank_two_zero_row", ((1, -4, 6, -4, 1),),
             ((0, 2),), ((1,), (0,)), sigmas=(Q(1), Q(1))),
        Case("rank_two_all_constant", ((0, 0, 0, 0, -1), (0,)),
             ((2, 2), (-2, 2)), ((1, 0), (0, 0)), sigmas=(Q(1), Q(1))),
        Case("rank_one_minimum_grid", ((1, -2, 1),), ((0, 2),), ((0,),), alpha=Q(4)),
    )
    for case in fixtures:
        _, _, d0, size, _ = parameters(case)
        assert d0 == 2 and size <= 64
        if case.name == "rank_one_endpoint_tie":
            draws = product(range(size), repeat=1)
        else:
            draws = product(sorted({0, size // 2, size - 1}), repeat=len(case.rows))
        before = counts["draws"]
        for indices in draws:
            check_solver(case, indices, counts)
        print(f"PASS: {case.name}: M={size}, draws={counts['draws'] - before}")
        counts["fixtures"] += 1
    assert counts["tied_draws"] > 0
    print(json.dumps({"status": "passed", **counts}, indent=2))


if __name__ == "__main__":
    main()
