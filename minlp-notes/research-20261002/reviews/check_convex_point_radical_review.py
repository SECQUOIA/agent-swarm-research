"""Exact reviewer diagnostics for the two-copy convex quartic amplifier.

This checks the amplifier Hessian under the proved 1/16 base lower bound.
It does not approximate radicals or test an optimization algorithm.
"""

from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path


MU = Q(1, 16)
ETA = Q(1, 192)


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    return sum(
        (-1) ** j * a[0][j]
        * determinant([row[:j] + row[j + 1:] for row in a[1:]])
        for j in range(len(a))
    )


def quadratic(a, v):
    return sum(a[i][j] * v[i] * v[j]
               for i in range(len(v)) for j in range(len(v)))


def hessian(tp, tm, y):
    ap, am = y - 1, y
    return [
        [MU + 2 * ETA * ap * ap, Q(0), 4 * ETA * tp * ap],
        [Q(0), MU + 2 * ETA * am * am, 4 * ETA * tm * am],
        [4 * ETA * tp * ap, 4 * ETA * tm * am,
         2 * ETA * (tp * tp + tm * tm)],
    ]


def run():
    matrices = minors = identities = zero_cases = 0
    t_values = [Q(0), Q(1, 16), Q(1, 2), Q(1)]
    y_values = [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]
    directions = list(product([Q(-1), Q(0), Q(1)], repeat=3))
    for tp, tm, y in product(t_values, t_values, y_values):
        a = hessian(tp, tm, y)
        matrices += 1
        for size in (1, 2, 3):
            for indices in combinations(range(3), size):
                minor = [[a[i][j] for j in indices] for i in indices]
                assert determinant(minor) >= 0
                minors += 1
        for pp, pm, q in directions:
            exact = (
                MU * (pp * pp + pm * pm)
                + 2 * ETA * ((tp * q + 2 * (y - 1) * pp) ** 2
                             + (tm * q + 2 * y * pm) ** 2)
                - 6 * ETA * ((y - 1) ** 2 * pp * pp + y * y * pm * pm)
            )
            value = quadratic(a, [pp, pm, q])
            assert value == exact
            assert value >= (MU - 6 * ETA) * (pp * pp + pm * pm)
            identities += 1
        if tp == tm == 0:
            assert a[2][2] == 0 and determinant(a) == 0
            assert quadratic(a, [Q(0), Q(0), Q(1)]) == 0
            zero_cases += 1

    # The quartic by itself is not convex; the base curvature is essential.
    raw = [[Q(1, 2), Q(1)], [Q(1), Q(1, 2)]]
    assert determinant(raw) == -Q(3, 4)

    # An active amplitude can encode an endpoint while its value penalty is tiny.
    # These are amplifier amplitude fixtures, not computed source optimizers.
    tiny = []
    for bits in (1, 20, 200):
        t = Q(1, 2 ** bits)
        for positive_branch in (True, False):
            tp, tm = (t, Q(0)) if positive_branch else (Q(0), t)
            correct = Q(1) if positive_branch else Q(0)
            wrong = 1 - correct
            penalty = lambda y: ETA * (tp * tp * (y - 1) ** 2 + tm * tm * y * y)
            assert penalty(correct) == 0
            assert penalty(wrong) == ETA * t * t > 0
            assert abs(wrong - correct) == 1
            for error in (Q(-1, 4), Q(0), Q(1, 4)):
                reported = correct + error
                assert (reported > Q(1, 2)) == positive_branch
        tiny.append({"amplitude_bits": bits,
                     "wrong_endpoint_gap": str(ETA * t * t)})

    result = {
        "status": "pass",
        "exact_hessian_matrices": matrices,
        "nonnegative_principal_minors": minors,
        "directional_identities_and_lower_bounds": identities,
        "zero_amplitude_singular_cases": zero_cases,
        "quartic_without_base_negative_determinant": "-3/4",
        "tiny_amplitude_fixtures": tiny,
        "scope": "amplifier only; no numerical radical solver or complexity test",
    }
    output = Path(__file__).with_name("convex-point-radical-review-results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
