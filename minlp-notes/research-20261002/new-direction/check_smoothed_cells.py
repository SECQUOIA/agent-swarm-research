"""Exact-rational checks for the semiconcave cell algorithm.

Fixtures are lower envelopes of quadratic wells. Their global and cell
minima are known by independent minimization of each separable well.
"""

from fractions import Fraction as Q
from itertools import product
import json


def check_case(widths, wells, tilt, levels):
    k = len(widths)
    alpha = Q(2)
    lower = tuple(-w / 2 for w in widths)
    upper = tuple(w / 2 for w in widths)
    bits = tuple(product((0, 1), repeat=k))

    def value(x):
        return min(
            offset + alpha / 2 * sum((v - a) ** 2 for v, a in zip(x, center))
            for center, offset in wells
        ) + sum(c * v for c, v in zip(tilt, x))

    def true_min(lo, hi):
        candidates = []
        for center, offset in wells:
            x = tuple(
                min(b, max(a, v - c / alpha))
                for a, b, v, c in zip(lo, hi, center, tilt)
            )
            candidates.append(
                offset
                + alpha / 2 * sum((v - a) ** 2 for v, a in zip(x, center))
                + sum(c * v for c, v in zip(tilt, x))
            )
        return min(candidates)

    optimum = true_min(lower, upper)
    previous_m = [1] * k
    active = [tuple(0 for _ in widths)]
    incumbent = None
    counts = {"processed_cells": 0, "corner_calls": 0, "full_grid_nodes": 0}

    for level in range(levels + 1):
        target = max(widths) / 2**level
        m = []
        for width in widths:
            pieces = 1
            while width / pieces > target:
                pieces *= 2
            m.append(pieces)
        spacing = tuple(w / pieces for w, pieces in zip(widths, m))
        correction = alpha * sum(h * h for h in spacing) / 8
        if level:
            children = []
            for index in active:
                choices = [
                    (2 * pos, 2 * pos + 1) if new == 2 * old else (pos,)
                    for pos, new, old in zip(index, m, previous_m)
                ]
                children.extend(product(*choices))
            active = children

        bounds = []
        for index in active:
            lo = tuple(a + pos * h for a, pos, h in zip(lower, index, spacing))
            hi = tuple(a + h for a, h in zip(lo, spacing))
            corners = [tuple(a + bit * h for a, bit, h in zip(lo, mask, spacing))
                       for mask in bits]
            corner_min = min(map(value, corners))
            incumbent = corner_min if incumbent is None else min(incumbent, corner_min)
            bound = corner_min - correction
            assert bound <= true_min(lo, hi)
            bounds.append((index, bound, corner_min))
            counts["processed_cells"] += 1
            counts["corner_calls"] += len(corners)

        survivors = [(index, bound, v) for index, bound, v in bounds
                     if bound <= incumbent]
        assert survivors
        certified_lower = min(bound for _, bound, _ in survivors)
        assert certified_lower <= optimum <= incumbent
        assert incumbent - certified_lower <= correction
        assert incumbent - optimum <= correction
        assert all(v <= optimum + 2 * correction for _, _, v in survivors)

        near = 0
        axes = [tuple(a + pos * h for pos in range(pieces + 1))
                for a, h, pieces in zip(lower, spacing, m)]
        for point in product(*axes):
            counts["full_grid_nodes"] += 1
            near += value(point) <= optimum + 2 * correction
        assert len(survivors) <= 2**k * near
        active = [index for index, _, _ in survivors]
        previous_m = m

    return counts


def main():
    totals = {"cases": 0, "levels": 0, "processed_cells": 0,
              "corner_calls": 0, "full_grid_nodes": 0}
    for k in range(1, 5):
        widths = (Q(2), Q(3, 4), Q(1, 8), Q(5, 4))[:k]
        wells = [
            (tuple(w / 5 for w in widths), Q(0)),
            (tuple((-1) ** i * w / 3 for i, w in enumerate(widths)), Q(1, 32)),
            (tuple(-w / 4 for w in widths), Q(0)),
        ]
        for tilt in product((Q(-3, 2), Q(1, 2)), repeat=k):
            result = check_case(widths, wells, tilt, levels=3)
            totals["cases"] += 1
            totals["levels"] += 4
            for key, count in result.items():
                totals[key] += count
    print(json.dumps({"status": "passed", **totals}, indent=2))


if __name__ == "__main__":
    main()
