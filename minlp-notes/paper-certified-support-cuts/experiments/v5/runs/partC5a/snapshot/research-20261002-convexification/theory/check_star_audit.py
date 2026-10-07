"""Independent exact face-enumeration audit for constrained quadratic stars."""

from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from copy import deepcopy
import random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from quadratic_star import support_star, replay_star


def linear_solve(matrix, rhs):
    n = len(rhs)
    a = [list(map(F, row)) + [F(value)] for row, value in zip(matrix, rhs)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        value = a[col][col]
        a[col] = [v / value for v in a[col]]
        for row in range(n):
            if row != col:
                value = a[row][col]
                if value:
                    a[row] = [v - value * w for v, w in zip(a[row], a[col])]
    return [row[-1] for row in a]


def value(c, point):
    answer = F(0)
    for exponent, coefficient in c.items():
        term = F(coefficient)
        for x, e in zip(point, exponent):
            term *= x ** e
        answer += term
    return answer


def full_space_oracle(bounds, rows, c):
    n = len(bounds)
    a_rows = [(tuple(map(F, a)), F(rhs)) for a, rhs in rows]
    for i, (lo, hi) in enumerate(bounds):
        a = [F(0)] * n
        a[i] = F(1)
        a_rows.append((tuple(a), F(hi)))
        a[i] = F(-1)
        a_rows.append((tuple(a), -F(lo)))
    H = [[F(0)] * n for _ in range(n)]
    gradient = [F(0)] * n
    for exponent, coefficient in c.items():
        coefficient = F(coefficient)
        support = [i for i, e in enumerate(exponent) if e]
        if sum(exponent) == 1:
            gradient[support[0]] += coefficient
        elif sum(exponent) == 2:
            if len(support) == 1:
                H[support[0]][support[0]] += 2 * coefficient
            else:
                i, j = support
                H[i][j] += coefficient
                H[j][i] += coefficient
    candidates = []
    for k in range(n + 1):
        for active in combinations(a_rows, k):
            matrix = [H[i] + [a[i] for a, _ in active] for i in range(n)]
            matrix += [list(a) + [F(0)] * k for a, _ in active]
            rhs = [-v for v in gradient] + [b for _, b in active]
            solution = linear_solve(matrix, rhs)
            if solution is None:
                continue
            x = solution[:n]
            if all(sum(ai * xi for ai, xi in zip(a, x)) <= b for a, b in a_rows):
                candidates.append((value(c, x), x))
    return min(candidates) if candidates else None


def check(bounds, rows, c, center):
    expected = full_space_oracle(bounds, rows, c)
    got = support_star(bounds, rows, c, center)
    if expected is None:
        assert got['status'] == 'empty', (bounds, rows, c, got)
        return 0, 0
    assert got['status'] == 'complete'
    assert F(got['bound']) == expected[0], (bounds, rows, c, expected, got)
    x = list(map(F, got['minimizer']))
    assert all(F(lo) <= xi <= F(hi) for xi, (lo, hi) in zip(x, bounds))
    assert all(sum(F(ai) * xi for ai, xi in zip(a, x)) <= F(b) for a, b in rows)
    assert value(c, x) == F(got['bound'])
    for piece in got['pieces']:
        lo, hi = map(F, piece['interval'])
        for numerator in (0, 1, 2, 3, 4):
            y = lo + F(numerator, 4) * (hi - lo)
            point = [F(0)] * len(bounds)
            point[center] = y
            for i, intercept, slope in piece['leaf_rules']:
                point[i] = F(intercept) + F(slope) * y
            assert all(F(low) <= xi <= F(high) for xi, (low, high) in zip(point, bounds))
            assert all(sum(F(ai) * xi for ai, xi in zip(a, point)) <= F(b) for a, b in rows)
            polynomial = list(map(F, piece['polynomial']))
            assert value(c, point) == polynomial[0] + polynomial[1] * y + polynomial[2] * y*y
    assert replay_star(bounds, rows, c, center, got)
    return 1, len(got['pieces'])

def main():
    rng = random.Random(20261002)
    count = feasible = pieces = 0
    for n, trials in ((3, 120), (4, 35)):
        for trial in range(trials):
            center = trial % n
            bounds = [(F(-2), F(3)) for _ in range(n)]
            if trial % 17 == 0:
                i = (trial // 17) % n
                bounds[i] = (F(1, 3), F(1, 3))
            rows = []
            for j in range(2 * n):
                a = [F(0)] * n
                leaf = rng.choice([i for i in range(n) if i != center])
                a[center] = F(rng.randint(-3, 3))
                a[leaf] = F(rng.randint(-3, 3))
                rows.append((a, F(rng.randint(-4, 7), rng.randint(1, 3))))
            if trial % 19 == 0:
                a = [F(0)] * n
                a[center] = 1
                leaf = next(i for i in range(n) if i != center)
                a[leaf] = -1
                rows += [(a, F(0)), ([-v for v in a], F(0))]
            c = {(0,) * n: F(rng.randint(-3, 3), 2)}
            for i in range(n):
                for degree in (1, 2):
                    e = [0] * n
                    e[i] = degree
                    c[tuple(e)] = F(rng.randint(-5, 5), rng.randint(1, 3))
                if i != center:
                    e = [0] * n
                    e[i] = e[center] = 1
                    c[tuple(e)] = F(rng.randint(-5, 5), rng.randint(1, 3))
            yes, npieces = check(bounds, rows, c, center)
            count += 1
            feasible += yes
            pieces += npieces
    print(f'{count} random constrained stars: {feasible} feasible, {count-feasible} empty; {pieces} returned pieces checked at both ends and three interior points')

    # Designed crossing envelopes on both sides of zero, with positive and
    # negative curvature leaves, one linear leaf, and a nonzero center index.
    bounds = ((-2, 2), (-1, 1), (-2, 2), (-2, 2))
    center = 1
    rows = [((1, 1, 0, 0), 1), ((1, -1, 0, 0), 1),
            ((-1, 2, 0, 0), 1), ((-1, -2, 0, 0), 1),
            ((0, 1, 1, 0), 1), ((0, -1, 1, 0), 1),
            ((0, 1, -1, 0), 1), ((0, -1, -1, 0), 1),
            ((0, 1, 0, 1), 1), ((0, -1, 0, -1), 1)]
    c = {(2, 0, 0, 0): F(3, 2), (1, 1, 0, 0): -2,
         (0, 0, 2, 0): -1, (0, 1, 1, 0): 3,
         (0, 0, 0, 1): F(1, 2), (0, 1, 0, 1): -3,
         (0, 2, 0, 0): 2, (0, 1, 0, 0): F(2, 3)}
    check(bounds, rows, c, center)
    got = support_star(bounds, rows, c, center)
    print('Designed crossing-envelope mixed-curvature star:', got['bound'], got['minimizer'], len(got['pieces']), 'pieces')

    # Input binding and completeness attacks.
    attacks = []
    for path, replacement in [(('bound',), '-10000'), (('problem', 'center'), 0),
                              (('problem', 'bounds'), [['-2', '3']]*4),
                              (('center_interval',), ['0', '0'])]:
        forged = deepcopy(got)
        cursor = forged
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        attacks.append(forged)
    for key in ('pieces',):
        forged = deepcopy(got)
        forged[key].pop()
        attacks.append(forged)
    for attack in attacks:
        assert not replay_star(bounds, rows, c, center, attack)
    assert not replay_star(bounds, rows[:-1], c, center, got)
    new_c = dict(c)
    new_c[(0, 0, 0, 0)] = 1
    assert not replay_star(bounds, rows, new_c, center, got)
    print('7 certificate/trusted-input tampering checks rejected')


if __name__ == "__main__":
    main()
