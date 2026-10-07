"""Exact small diagnostics for the mixed submodular recourse theorem.

The general SFM algorithm is not implemented here. Independent active-face
enumeration checks the endpoint/convex reduction on small rational boxes.
"""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import random


def solve_linear(matrix, rhs):
    n = len(rhs)
    rows = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            return None
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [v / scale for v in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [v - scale * w for v, w in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def value(matrix, linear, point, constant=Q(0)):
    return constant + sum(b * x for b, x in zip(linear, point)) + sum(
        matrix[i][j] * point[i] * point[j] / 2
        for i in range(len(point))
        for j in range(len(point))
    )


def full_face_minimum(matrix, linear, bounds, constant=Q(0)):
    n = len(linear)
    best = None
    for face in product((-1, 0, 1), repeat=n):
        free = [i for i, side in enumerate(face) if side == 0]
        fixed = [i for i, side in enumerate(face) if side != 0]
        point = [bounds[i][side == 1] if side else Q(0)
                 for i, side in enumerate(face)]
        if free:
            block = [[matrix[i][j] for j in free] for i in free]
            rhs = [-linear[i] - sum(matrix[i][j] * point[j] for j in fixed)
                   for i in free]
            sol = solve_linear(block, rhs)
            if sol is None:
                continue
            for i, val in zip(free, sol):
                point[i] = val
            if any(not bounds[i][0] <= point[i] <= bounds[i][1] for i in free):
                continue
        current = value(matrix, linear, point, constant)
        if best is None or current < best:
            best = current
    assert best is not None
    return best


def scalar_completion(matrix, linear, bounds, label, constant=Q(0)):
    """First coordinates are fixed; last coordinate is convex continuous."""
    m = len(label)
    lo, hi = bounds[m]
    slope = linear[m] + sum(matrix[m][i] * label[i] for i in range(m))
    diag = matrix[m][m]
    assert diag >= 0
    point = list(label)
    if diag:
        point.append(min(hi, max(lo, -slope / diag)))
    else:
        point.append(lo if slope >= 0 else hi)
    gradient = slope + diag * point[-1]
    assert lo <= point[-1] <= hi
    if lo < hi:
        assert ((point[-1] == lo and gradient >= 0)
                or (point[-1] == hi and gradient <= 0)
                or (lo < point[-1] < hi and gradient == 0))
    return value(matrix, linear, point, constant), point


def endpoint_values(matrix, linear, bounds, signs, constant=Q(0)):
    m = len(linear) - 1
    values, points = {}, {}
    for mask in range(1 << m):
        label = [bounds[i][bool(mask & (1 << i)) ^ (signs[i] < 0)]
                 for i in range(m)]
        values[mask], points[mask] = scalar_completion(
            matrix, linear, bounds, label, constant)
    return values, points


def greedy(values, permutation):
    result = [Q(0)] * len(permutation)
    mask = 0
    for i in permutation:
        nxt = mask | (1 << i)
        result[i] = values[nxt] - values[mask]
        mask = nxt
    return result


def check_fixture():
    matrix = [[Q(-2), Q(-3, 2), Q(-1, 2)],
              [Q(-3, 2), Q(-2), Q(-1, 2)],
              [Q(-1, 2), Q(-1, 2), Q(2)]]
    linear = [Q(2), Q(2), Q(-1, 2)]
    bounds = [(Q(0), Q(1))] * 3
    values, points = endpoint_values(matrix, linear, bounds, [1] * 3, Q(1, 16))
    assert list(values.values()) == [Q(0), Q(13, 16), Q(13, 16), Q(0)]
    bases = [greedy(values, perm) for perm in ((0, 1), (1, 0))]
    mixture = [(bases[0][i] + bases[1][i]) / 2 for i in range(2)]
    assert mixture == [0, 0]
    lower = values[0] + sum(min(Q(0), w) for w in mixture)
    assert lower == min(values.values()) == 0
    assert all(sum(min(Q(0), w) for w in base) == -Q(13, 16)
               for base in bases)
    assert points[0][-1] == Q(1, 4) and points[3][-1] == Q(3, 4)
    assert full_face_minimum(matrix, linear, bounds, Q(1, 16)) == 0
    # Wrong averaging weights sum to one but lose equality, so fail closure.
    altered = [(3 * bases[0][i] + bases[1][i]) / 4 for i in range(2)]
    assert values[0] + sum(min(Q(0), w) for w in altered) < 0
    return {"values": [str(values[i]) for i in range(4)],
            "mixture": [str(w) for w in mixture],
            "optimal_labels": [0, 3], "certificate_value": str(lower)}


def main():
    rng = random.Random(2026100217)
    cases = 60
    inequalities = queries = mixed_cases = 0
    singular_cases = 0
    for case in range(cases):
        m = 2 + case % 3
        n = m + 1
        matrix = [[Q(0) for _ in range(n)] for _ in range(n)]
        signs = [rng.choice((-1, 1)) for _ in range(n)]
        for i in range(m):
            matrix[i][i] = -Q(rng.randint(0, 4), rng.randint(1, 3))
        matrix[m][m] = Q(0) if case % 10 == 0 else Q(rng.randint(1, 4))
        singular_cases += matrix[m][m] == 0
        for i in range(n):
            for j in range(i):
                coeff = -Q(rng.randint(0, 4), rng.randint(1, 3))
                matrix[i][j] = matrix[j][i] = signs[i] * signs[j] * coeff
        linear = [Q(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(n)]
        bounds = []
        for i in range(n):
            lo = Q(rng.randint(-4, 2), 3)
            hi = lo + Q(rng.randint(1, 8), 4)
            bounds.append((lo, hi))
        values, _ = endpoint_values(matrix, linear, bounds, signs)
        queries += len(values)
        assert min(values.values()) == full_face_minimum(matrix, linear, bounds)
        for a in values:
            for b in values:
                assert values[a] + values[b] >= values[a & b] + values[a | b]
                inequalities += 1
        # Effective integer bounds in D; C stays continuous.
        int_bounds = [(Q(rng.randint(-2, 0)), Q(rng.randint(1, 3)))
                      for _ in range(m)] + [bounds[-1]]
        int_values, _ = endpoint_values(matrix, linear, int_bounds, signs)
        lattice_best = min(scalar_completion(matrix, linear, int_bounds, label)[0]
                           for label in product(*(range(int(lo), int(hi) + 1)
                                                  for lo, hi in int_bounds[:-1])))
        assert min(int_values.values()) == lattice_best
        mixed_cases += 1
    fixture = check_fixture()
    # Guard the continuous PSD contract: first-order conditions alone fail.
    indefinite = [[Q(1), Q(-2)], [Q(-2), Q(1)]]
    assert value(indefinite, [Q(0)] * 2, [Q(0)] * 2) == 0
    assert value(indefinite, [Q(0)] * 2, [Q(1)] * 2) == -1
    # A convex integer variable cannot use the continuous value oracle.
    assert min((Q(x) - Q(1, 2)) ** 2 for x in (0, 1)) == Q(1, 4)
    result = {"status": "passed", "seed": 2026100217,
              "rational_box_qp_cases": cases, "conditional_queries": queries,
              "submodular_inequalities": inequalities,
              "singular_convex_block_cases": singular_cases,
              "mixed_integer_endpoint_cases": mixed_cases,
              "nontrivial_certificate_fixture": fixture,
              "guards": ["PSD assumption", "continuous convex block",
                         "certificate equality after altered weights"],
              "scope": "Small exact diagnostics; no general SFM implementation"}
    out = Path(__file__).with_name("mixed-submodular-results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
