"""Exact checks of new retained-hull/core-output contracts.

This is a small fixture diagnostic, not a general recourse or algebraic
fallback implementation. Existing lower-bound/count tests are separate.
"""

from fractions import Fraction as Q
from itertools import product


def run_fixture(name, centers, weights, growth, keep_exact_old=False):
    k = len(weights)
    curvature = Q(3)  # bounds all fixture core diagonal curvatures
    retained = [(0,) * k]
    incumbent = None
    incumbent_core = None
    counts = dict(stages=0, old=0, outputs=0, wide=0)

    def value(v):
        return min(
            sum(w * (x - a) ** 2 for w, x, a in zip(weights, v, center))
            for center in centers
        )

    for j in range(7):
        size = 2**j
        h = Q(1, size)
        e = k * curvature * h * h / 8
        if j:
            cells = [
                tuple(2 * i + bit for i, bit in zip(cell, bits))
                for cell in retained
                for bits in product((0, 1), repeat=k)
            ]
        else:
            cells = retained
        rows = []
        improved = False
        for cell in cells:
            vertices = [
                tuple(Q(i + bit, size) for i, bit in zip(cell, bits))
                for bits in product((0, 1), repeat=k)
            ]
            lower = []
            for v in vertices:
                # A feasible squared residual error; exact initial output
                # makes an old incumbent win on a boundary fixture.
                residual = Q(0) if keep_exact_old and j == 0 else e / (1 + e)
                error = residual**2
                assert error <= e
                upper = value(v) + error
                lower.append(upper - e)
                if incumbent is None or upper < incumbent:
                    incumbent = upper
                    incumbent_core = v
                    improved = True
            rows.append((cell, min(lower) - e))

        retained = [cell for cell, lower in rows if lower <= incumbent]
        assert retained

        def contained(v):
            return any(
                all(Q(i, size) <= x <= Q(i + 1, size) for i, x in zip(cell, v))
                for cell in retained
            )

        assert contained(incumbent_core), (name, j, "lost incumbent")
        assert all(contained(a) for a in centers), (name, j, "lost optimum")
        lo = tuple(min(Q(cell[i], size) for cell in retained) for i in range(k))
        hi = tuple(max(Q(cell[i] + 1, size) for cell in retained) for i in range(k))
        diameter_sq = sum((b - a) ** 2 for a, b in zip(lo, hi))
        if growth:
            D = 4 * k + k * k * curvature / growth
            assert diameter_sq <= (D * h) ** 2

        # All fixture centers are true global cores. With zero-weight
        # directions they also include the extreme points of the fiber.
        selected_core = min(centers)
        for q in range(1, 5):
            eps = Q(1, 2**q)
            if 2 * e <= eps and diameter_sq <= eps**2:
                assert sum((x - a) ** 2 for x, a in zip(incumbent_core, selected_core)) <= eps**2
                assert incumbent <= 2 * e <= eps
                counts["outputs"] += 1
            elif diameter_sq > eps**2:
                counts["wide"] += 1
        counts["stages"] += 1
        counts["old"] += int(j > 0 and not improved)

    if keep_exact_old:
        assert counts["old"] == 6
    if len(centers) > 1:
        assert counts["outputs"] == 0
    else:
        assert counts["outputs"] > 0
    return counts


fixtures = [
    ("old endpoint", [(Q(0),)], (Q(1),), Q(1), True),
    ("interior", [(Q(1, 3), Q(2, 3))], (Q(1), Q(1)), Q(1), False),
    ("tied endpoints", [(Q(0),), (Q(1),)], (Q(1),), None, False),
    ("flat fiber", [(Q(0), Q(0)), (Q(0), Q(1))], (Q(1), Q(0)), None, False),
    ("flat objective", [(Q(0),), (Q(1),)], (Q(0),), None, False),
]
totals = dict(stages=0, old=0, outputs=0, wide=0)
for fixture in fixtures:
    counts = run_fixture(*fixture)
    for key, value in counts.items():
        totals[key] += value

budgets = 0
for k, B, Cg, Ca, sigma in product((1, 2, 5), (2, 17), (1, 31), (1, 23), (Q(1, 8), Q(5))):
    M = 1
    while M < max(2, 2 * B * max(Cg, Ca)):
        M *= 2
    g0 = sigma / (2 * k * B)
    assert k * g0 / sigma + Q(Cg, M) <= Q(1, B)
    assert Q(Ca * B, M) <= Q(1, 2)
    budgets += 1

print(f"PASS: {len(fixtures)} fixtures, {totals}, {budgets} exact combined-law budgets.")
