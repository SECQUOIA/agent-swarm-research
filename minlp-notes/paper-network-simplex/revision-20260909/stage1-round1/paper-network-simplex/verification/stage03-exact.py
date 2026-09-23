"""Independent exact finite checks of the Stage 3 geometric and cut formulas.

Uses vertex intersections for theta polygons, exhaustive bounded integer
matrices for integral transportation data, and all source/sink cuts. No LP
solver or production separator is imported. Integer transportation feasibility
is equivalent to real feasibility for these integral capacities and targets.
"""

from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import random


def theta_checks(rng):
    nonempty = 0
    for _ in range(160):
        lower = [F(rng.randint(-3, 2), rng.choice((1, 2))) for _ in range(3)]
        upper = [a + F(rng.randint(-1, 4), rng.choice((1, 2))) for a in lower]
        # Normals are s, t, and s+t, with both signed bound orientations.
        rows = [(1, 0, upper[0]), (-1, 0, -lower[0]),
                (0, 1, upper[1]), (0, -1, -lower[1]),
                (1, 1, upper[2]), (-1, -1, -lower[2])]
        vertices = set()
        for (a, b, c), (d, e, f) in combinations(rows, 2):
            determinant = a * e - b * d
            if determinant:
                s, t = (c * e - b * f) / determinant, (a * f - c * d) / determinant
                if all(i * s + j * t <= k for i, j, k in rows):
                    vertices.add((s, t))
        predicted = (all(a <= b for a, b in zip(lower, upper))
                     and lower[0] + lower[1] <= upper[2]
                     and lower[2] <= upper[0] + upper[1])
        assert predicted == bool(vertices)
        if not predicted:
            continue
        a = [max(lower[0], lower[2] - upper[1]),
             max(lower[1], lower[2] - upper[0]),
             max(lower[2], lower[0] + lower[1])]
        b = [min(upper[0], upper[2] - lower[1]),
             min(upper[1], upper[2] - lower[0]),
             min(upper[2], upper[0] + upper[1])]
        values = [(s, t, s + t) for s, t in vertices]
        assert a == [min(v[i] for v in values) for i in range(3)]
        assert b == [max(v[i] for v in values) for i in range(3)]
        nonempty += 1
    return nonempty


def transportation_checks(rng):
    feasible_count = negative_rows = 0
    for _ in range(100):
        k, n = rng.randint(2, 4), rng.randint(1, 3)
        witness = [[0 for _ in range(n)] for _ in range(k)]
        for j in range(n):
            for i in range(k - 1):
                witness[i][j] = rng.randint(-1, 1)
            witness[-1][j] = -sum(witness[i][j] for i in range(k - 1))
        lower = [[0] * n for _ in range(k)]
        upper = [[0] * n for _ in range(k)]
        for i, j in product(range(k), range(n)):
            width = rng.randint(0, 1)
            lower[i][j] = witness[i][j] - rng.randint(0, width)
            upper[i][j] = lower[i][j] + width
        delta = [sum(row) for row in witness]
        i, h = rng.sample(range(k), 2)
        perturbation = rng.randint(0, 3)
        delta[i] += perturbation
        delta[h] -= perturbation
        rhs = {}
        for mask in range(1 << k):
            inside = [i for i in range(k) if mask >> i & 1]
            outside = [i for i in range(k) if not mask >> i & 1]
            rhs[mask] = sum(min(sum(upper[i][j] for i in inside),
                                -sum(lower[i][j] for i in outside)) for j in range(n))
        predicted = all(sum(delta[i] for i in range(k) if mask >> i & 1) <= bound
                        for mask, bound in rhs.items())
        candidates = product(*(range(lower[i][j], upper[i][j] + 1)
                               for i in range(k) for j in range(n)))
        feasible = any(all(sum(w[i * n + j] for i in range(k)) == 0 for j in range(n))
                       and all(sum(w[i * n:(i + 1) * n]) == delta[i] for i in range(k))
                       for w in candidates)
        assert predicted == feasible
        feasible_count += feasible
        r = [delta[i] - sum(lower[i]) for i in range(k)]
        c = [-sum(lower[i][j] for i in range(k)) for j in range(n)]
        cap = [[upper[i][j] - lower[i][j] for j in range(n)] for i in range(k)]
        assert sum(r) == sum(c)
        if min(r) < 0:
            negative_rows += 1
            assert not predicted
            continue
        total = sum(r)
        minimum_cut = total
        for mask in range(1 << k):
            inside = [i for i in range(k) if mask >> i & 1]
            outside = [i for i in range(k) if not mask >> i & 1]
            minimized = sum(r[i] for i in outside) + sum(
                min(sum(cap[i][j] for i in inside), c[j]) for j in range(n))
            explicit = min(sum(r[i] for i in outside)
                           + sum(c[j] for j in range(n) if cmask >> j & 1)
                           + sum(cap[i][j] for i in inside for j in range(n)
                                 if not cmask >> j & 1)
                           for cmask in range(1 << n))
            assert minimized == explicit
            minimum_cut = min(minimum_cut, explicit)
        assert (minimum_cut == total) == feasible
    return feasible_count, negative_rows


def joint_state_check():
    aggregate = (F(1, 3),) * 3
    explicit = (F(0), F(0), F(1, 3))
    complement = tuple(a - e for a, e in zip(aggregate, explicit))
    assert sum(explicit) == F(1, 3) and sum(complement) == F(2, 3)
    assert min(complement) >= 0
    joint_residual = tuple(a - 2 * e for a, e in zip(aggregate, explicit))
    assert joint_residual[2] == -F(1, 3)
    assert sum(aggregate[:2]) - (1 - F(2, 3)) == F(1, 3)


if __name__ == "__main__":
    rng = random.Random(741809)
    nonempty = theta_checks(rng)
    feasible, negative_rows = transportation_checks(rng)
    joint_state_check()
    result = {"status": "PASS", "theta_domains": 160,
              "nonempty_theta_domains": nonempty, "transportation_models": 100,
              "feasible_transportation_models": feasible,
              "negative_row_models": negative_rows, "joint_theta_violation": "1/3"}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
