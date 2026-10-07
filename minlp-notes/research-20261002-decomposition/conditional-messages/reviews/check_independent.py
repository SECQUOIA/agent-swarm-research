"""Independent exact checks, including coupled and nonconvex cores.

Run from any working directory. This diagnostic is deliberately separate
from the author's generators and exact comparison functions.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mincut_recourse import (Certificate, Quadratic, adaptive_core,
                            detect_flips, exact_core, optimum_denominator_bound,
                            solve_recourse, verify_exact, verify_recourse,
                            verify_search)


def linear_solve(matrix, rhs):
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for column in range(len(rows)):
        pivot = next((i for i in range(column, len(rows)) if rows[i][column]), None)
        if pivot is None:
            return None
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [x / divisor for x in rows[column]]
        for i in range(len(rows)):
            if i != column:
                factor = rows[i][column]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[column])]
    return [row[-1] for row in rows]


def exact_core_faces(model, core_size, bounds):
    """Enumerate residual endpoints and stationary points of all core faces.

    A global box-QP optimizer exists on a minimal face whose free Hessian
    is nonsingular, so singular stationary faces may be skipped.
    """
    best = None
    for residual in product(*(b for b in bounds[core_size:])):
        for status in product((-1, 0, 1), repeat=core_size):
            point = [Q(max(0, a)) for a in status] + list(residual)
            free = [i for i, a in enumerate(status) if a == -1]
            hessian = [[Q(0) for _ in free] for _ in free]
            slope = [model.linear[i] for i in free]
            positions = {i: p for p, i in enumerate(free)}
            for i, p in positions.items():
                hessian[p][p] = 2 * model.diagonal[i]
            for i, j, coefficient in model.edges:
                if i in positions and j in positions:
                    hessian[positions[i]][positions[j]] = coefficient
                    hessian[positions[j]][positions[i]] = coefficient
                elif i in positions:
                    slope[positions[i]] += coefficient * point[j]
                elif j in positions:
                    slope[positions[j]] += coefficient * point[i]
            solution = linear_solve(hessian, [-x for x in slope])
            if solution is None or any(not 0 <= x <= 1 for x in solution):
                continue
            for i, value in zip(free, solution):
                point[i] = value
            value = model.value(point)
            if best is None or value < best:
                best = value
    return best


def run():
    rng = random.Random(920107)
    levels = 0
    for case in range(120):
        k, r = 1 + case % 3, case % 4
        signs = {i: rng.choice((-1, 1)) for i in range(k, k + r)}
        diagonal = tuple(Q(rng.randrange(-6, 10), 3) for _ in range(k))
        diagonal += tuple(Q(-rng.randrange(5), 3) for _ in range(r))
        linear = tuple(Q(rng.randrange(-12, 13), 5) for _ in range(k + r))
        edges = []
        for i in range(k + r):
            for j in range(i + 1, k + r):
                coefficient = Q(rng.randrange(-8, 9), 7)
                if i >= k:
                    coefficient = -abs(coefficient) * signs[i] * signs[j]
                if coefficient:
                    edges.append((i, j, coefficient))
        model = Quadratic(diagonal, linear, tuple(edges), Q(case - 60, 13))
        bounds = [(Q(0), Q(1))] * k + [(Q(-2, 3), Q(7, 4))] * r
        optimum = exact_core_faces(model, k, bounds)
        assert optimum.denominator <= optimum_denominator_bound(model, range(k), bounds)
        detected = detect_flips(model, range(k))
        result = adaptive_core(model, range(k), bounds, detected, Q(1, 64), max_levels=8)
        assert result['complete']
        assert verify_search(model, range(k), bounds, detected, Q(1, 64), result)
        for row in result['trace']:
            assert row['lower'] <= optimum <= row['upper']
            levels += 1

    for case in range(24):
        k, r = 1 + case % 3, 2
        diagonal = tuple(Q(2) for _ in range(k)) + (Q(-1), Q(0))
        linear = tuple(Q(rng.randrange(-5, 6)) for _ in range(k+r))
        edges = []
        for i in range(k+r):
            for j in range(i+1, k+r):
                coefficient = rng.choice((-1, 0, 1)) if i < k else -1
                if coefficient:
                    edges.append((i, j, Q(coefficient)))
        model = Quadratic(diagonal, linear, tuple(edges))
        bounds = [(Q(0), Q(1))]*k + [(Q(-1), Q(2))]*r
        optimum = exact_core_faces(model, k, bounds)
        # Permute every variable and reverse the order of the supplied core.
        ordering = list(range(k+r))
        rng.shuffle(ordering)
        destination = {old: new for new, old in enumerate(ordering)}
        permuted = Quadratic(tuple(diagonal[i] for i in ordering),
                             tuple(linear[i] for i in ordering),
                             tuple((min(destination[i], destination[j]),
                                    max(destination[i], destination[j]), c)
                                   for i, j, c in edges))
        core = tuple(destination[i] for i in reversed(range(k)))
        reordered_bounds = [bounds[i] for i in ordering]
        flips = detect_flips(permuted, core)
        result = exact_core(permuted, core, reordered_bounds, flips, max_levels=24)
        assert result['complete']
        assert result['value'] == optimum
        assert verify_exact(permuted, core, reordered_bounds, flips, result)

    # Supplement: a coupled two-dimensional convex block, including
    # singular Laplacians, and two concave endpoint coordinates.
    for case in range(24):
        weight = Q(1 + case % 4)
        modulus = Q(case % 2)
        diagonal = ((weight+modulus)/2, (weight+modulus)/2,
                    Q(-1), Q(-1, 2))
        edges = [(0, 1, -weight)]
        edges.extend((i, j, -Q(rng.randrange(1, 6), 3))
                     for i in range(4) for j in range(i+1, 4)
                     if (i, j) != (0, 1))
        model = Quadratic(diagonal,
                          tuple(Q(rng.randrange(-5, 9), 3) for _ in range(4)),
                          tuple(edges))
        bounds = [(Q(0), Q(1))]*4
        optimum = exact_core_faces(model, 4, bounds)
        values = {}
        for mask in range(4):
            restricted = bounds[:2] + [(Q(bool(mask & (1 << i))),)*2 for i in range(2)]
            values[mask] = exact_core_faces(model, 2, restricted)
        assert min(values.values()) == optimum
        for left in values:
            for right in values:
                assert values[left] + values[right] >= values[left & right] + values[left | right]
        first = (values[1]-values[0], values[3]-values[1])
        second = (values[3]-values[2], values[2]-values[0])
        weights = {Q(0), Q(1)}
        for i in range(2):
            if first[i] != second[i]:
                crossing = -first[i]/(second[i]-first[i])
                if 0 <= crossing <= 1:
                    weights.add(crossing)
        certificate_bound = max(values[0] + sum(min(Q(0), (1-a)*first[i]+a*second[i])
                                                for i in range(2)) for a in weights)
        assert certificate_bound == optimum

    # Soundness regressions found during independent review.
    n = 2 ** 54
    model = Quadratic((Q(0), Q(0)), (Q(-1), Q(2*n-1)),
                      ((0, 1, Q(-2*(n-1))),))
    flow = {(2, 0): float(n), (0, 2): -float(n),
            (0, 1): Q(n-1), (1, 0): Q(-(n-1)),
            (1, 3): float(n), (3, 1): -float(n)}
    fake = Certificate((Q(0), Q(0)), Q(0), flow, frozenset({2}))
    assert solve_recourse(model, {}, [(0, 1)]*2, {0: 1, 1: 1}).value == -1
    assert not verify_recourse(model, {}, [(0, 1)]*2, {0: 1, 1: 1}, fake)
    try:
        cert = solve_recourse(model, {}, [(0, 1)]*2, {0: 1.0, 1: 1.0})
    except ValueError:
        pass
    else:
        # Explicit rational normalization is also sound.
        assert cert.value == -1
        assert isinstance(cert.value, (int, Q))

    model = Quadratic((Q(0),), (Q(-1),), ())
    bounds = [(Q(1, 3), Q(5, 3))]
    cert = solve_recourse(model, {}, bounds, {0: 1}, iter([0]))
    assert cert.point == (Q(1),) and cert.value == -1
    assert verify_recourse(model, {}, bounds, {0: 1}, cert, iter([0]))
    result = adaptive_core(model, (), bounds, {0: 1}, Q(1, 10), integer_indices=iter([0]))
    assert result['lower'] == result['upper'] == -1
    assert verify_search(model, (), bounds, {0: 1}, Q(1, 10), result, iter([0]))
    print(f'Passed 120 independent coupled-core comparisons and {levels} exact level enclosures; '
          '24 exact-output comparisons with permuted cores; '
          '24 coupled-convex-block submodularity/mixture certificates; '
          'float-flow, float-sign, and one-pass-integrality soundness regressions passed.')


if __name__ == '__main__':
    run()
