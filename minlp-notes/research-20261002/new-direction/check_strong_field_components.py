"""Exact component-optimality and finite-law cost checks; no floating point."""

from fractions import Fraction as Q
from itertools import product
from math import prod


def solve(a, b):
    n = len(b)
    rows = [[Q(v) for v in row] + [Q(rhs)] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((j for j in range(col, n) if rows[j][col]), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        for j in range(n):
            if j != col:
                scale = rows[j][col]
                rows[j] = [v - scale * w for v, w in zip(rows[j], rows[col])]
    return [row[-1] for row in rows]


def value(h, b, x):
    return sum(bi * xi for bi, xi in zip(b, x)) + sum(
        Q(1, 2) * h[i][j] * x[i] * x[j]
        for i in range(len(x)) for j in range(len(x)))


def enumerate_qp(h, b, bounds, integer):
    states = [list(range(int(lo), int(hi) + 1)) if is_integer
              else [lo, None, hi]
              for (lo, hi), is_integer in zip(bounds, integer)]
    best = None
    for configuration in product(*states):
        x = list(configuration)
        free = [i for i, v in enumerate(x) if v is None]
        fixed = [i for i, v in enumerate(x) if v is not None]
        sub = [[h[i][j] for j in free] for i in free]
        rhs = [-b[i] - sum(h[i][j] * x[j] for j in fixed) for i in free]
        answer = solve(sub, rhs)
        if answer is None:
            continue
        for i, coordinate in zip(free, answer):
            x[i] = coordinate
        if any(not lo <= xi <= hi for xi, (lo, hi) in zip(x, bounds)):
            continue
        candidate = value(h, b, x)
        if best is None or candidate < best[0]:
            best = candidate, x
    assert best is not None
    return best


def derivative_ranges(h, b, bounds):
    ranges = []
    for i in range(len(b)):
        pairs = [(h[i][j] * lo, h[i][j] * hi)
                 for j, (lo, hi) in enumerate(bounds)]
        ranges.append((b[i] + sum(min(pair) for pair in pairs),
                       b[i] + sum(max(pair) for pair in pairs)))
    return ranges


def components(h, bad):
    remaining = set(bad)
    result = []
    while remaining:
        todo = [remaining.pop()]
        found = []
        while todo:
            i = todo.pop()
            found.append(i)
            neighbors = [j for j in remaining if h[i][j]]
            remaining.difference_update(neighbors)
            todo.extend(neighbors)
        result.append(sorted(found))
    return result


def component_qp(h, b, bounds, integer, noise):
    ranges = derivative_ranges(h, b, bounds)
    point = [None] * len(b)
    bad = []
    for i, ((low, high), gamma) in enumerate(zip(ranges, noise)):
        if gamma > -low:
            point[i] = bounds[i][0]
        elif gamma < -high:
            point[i] = bounds[i][1]
        else:
            bad.append(i)
    fixed = [i for i, x in enumerate(point) if x is not None]
    for component in components(h, bad):
        sub_h = [[h[i][j] for j in component] for i in component]
        sub_b = [b[i] + noise[i] + sum(h[i][j] * point[j] for j in fixed)
                 for i in component]
        _, sub_x = enumerate_qp(sub_h, sub_b, [bounds[i] for i in component],
                                [integer[i] for i in component])
        for i, coordinate in zip(component, sub_x):
            point[i] = coordinate
    return value(h, [bi + gi for bi, gi in zip(b, noise)], point), point


def optimality_checks():
    unit = [(Q(0), Q(1))] * 3
    fixtures = [
        ([[2, -1, 0], [-1, 2, -1], [0, -1, 2]], [0, 0, 0], unit, [False]*3),
        ([[-2, 1, 0], [1, 2, -1], [0, -1, -2]], [0, 0, 0], unit, [False]*3),
        ([[1]*3 for _ in range(3)], [-1, -1, -1], unit, [False]*3),
        ([[0]], [0], [(Q(-1), Q(1))], [False]),
        ([[2, -1, 0], [-1, -1, 1], [0, 1, 2]], [0, 1, -1],
         [(Q(0), Q(1)), (Q(0), Q(1)), (Q(0), Q(2))], [False, True, True]),
        ([[2, Q(1, 3), 0], [Q(1, 3), 0, -1], [0, -1, -2]],
         [Q(1, 2), 0, Q(-1, 3)],
         [(Q(-1), Q(1, 2)), (Q(0), Q(2)), (Q(-1), Q(1))], [False, True, False]),
    ]
    draws = 0
    for h, b, bounds, integer in fixtures:
        for noise in product(map(Q, [-3, -1, 1, 3]), repeat=len(b)):
            got, x = component_qp(h, b, bounds, integer, noise)
            want, _ = enumerate_qp(h, [bi+gi for bi, gi in zip(b, noise)],
                                    bounds, integer)
            assert got == want
            assert all(lo <= xi <= hi for xi, (lo, hi) in zip(x, bounds))
            draws += 1
    # Degenerate Hessians and continuum of minimizers are included explicitly.
    assert enumerate_qp([[1, 1], [1, 1]], [-1, -1], unit[:2], [False]*2)[0] == Q(-1, 2)
    assert enumerate_qp([[0, 0], [0, 0]], [0, 0], unit[:2], [False]*2)[0] == 0
    return draws


def probability_checks():
    fixtures = [
        (4, [(0, 1), (1, 2), (2, 3)], [3]*4),
        (4, [(i, j) for i in range(4) for j in range(i)], [3]*4),
        (6, [(0, j) for j in range(1, 6)], [3, 2, 7, 3, 2, 5]),
    ]
    patterns = 0
    for n, edges, weights in fixtures:
        h = [[Q(2 * (i == j)) for j in range(n)] for i in range(n)]
        for i, j in edges:
            h[i][j] = h[j][i] = -Q(1, 2)
        sigma, count = Q(100000), 256
        b = [-sigma] * n
        bounds = [(Q(0), Q(max(1, a - 1))) for a in weights]
        ranges = derivative_ranges(h, b, bounds)
        noise = [-sigma + 2 * sigma * k / (count - 1) for k in range(count)]
        probabilities = [Q(sum(-hi <= g <= -lo for g in noise), count)
                         for lo, hi in ranges]
        assert probabilities == [Q(1, count)] * n  # Endpoint atoms remain bad.
        beta = max(a*q for a, q in zip(weights, probabilities))
        degree = max(sum(bool(h[i][j]) for j in range(n) if i != j) for i in range(n))
        assert 4 * degree * beta < 1
        expectation = Q(0)
        for bits in product([False, True], repeat=n):
            probability = prod(q if bit else 1-q for bit, q in zip(bits, probabilities))
            cost = sum(prod(weights[i] for i in component)
                       for component in components(h, [i for i, bit in enumerate(bits) if bit]))
            expectation += probability * cost
            patterns += 1
        bound = sum(a*q for a, q in zip(weights, probabilities)) / (1 - 4*degree*beta)
        assert expectation <= bound
    return patterns


if __name__ == "__main__":
    draws = optimality_checks()
    patterns = probability_checks()
    print(f"PASS: {draws} exact same-draw optimizer comparisons, "
          f"{patterns} weighted bad-site patterns, 3 exact expected-cost bounds, "
          "2 singular-Hessian fixtures")
