"""Independent exact-arithmetic checks for the weighted nomination-face proof.

These finite checks exercise its adjoint mechanisms; they do not establish
global optimality or replace the structural proof.
"""

from fractions import Fraction as Q
import random


def solve(matrix, rhs):
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(a)
    for col in range(n):
        pivot = next(row for row in range(col, n) if a[row][col])
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        a[col] = [entry / divisor for entry in a[col]]
        for row in range(n):
            if row != col:
                factor = a[row][col]
                a[row] = [x - factor * y for x, y in zip(a[row], a[col])]
    return [row[-1] for row in a]


def dirichlet(n, edges, boundary, sources):
    free = [v for v in range(n) if v not in boundary]
    index = {v: i for i, v in enumerate(free)}
    matrix = [[Q(0) for _ in free] for _ in free]
    rhs = [sources.get(v, Q(0)) for v in free]
    for u, v, conductance in edges:
        for a, b in ((u, v), (v, u)):
            if a in index:
                i = index[a]
                matrix[i][i] += conductance
                if b in index:
                    matrix[i][index[b]] -= conductance
                else:
                    rhs[i] += conductance * boundary[b]
    values = dict(boundary)
    values.update(zip(free, solve(matrix, rhs)))
    return [values[v] for v in range(n)]


def main():
    rng = random.Random(937126)
    path_cases = level_cases = block_cases = 0
    for interior_count in range(1, 19):
        for _ in range(10):
            n = interior_count + 2
            edges = [(i, i + 1, Q(rng.randint(1, 15), rng.randint(1, 13)))
                     for i in range(n - 1)]
            delta = Q(rng.randint(1, 9), rng.randint(1, 12))
            boundary = {0: Q(rng.randint(-10, 10)),
                        n - 1: Q(rng.randint(-10, 10))}
            h = dirichlet(n, edges, boundary,
                          {v: delta for v in range(1, n - 1)})
            currents = [a * (h[u] - h[v]) for u, v, a in edges]
            assert all(currents[i] - currents[i - 1] == delta
                       for i in range(1, len(currents)))
            # Adjoint increments have signs +, optionally 0, then -.
            signs = [(h[i + 1] > h[i]) - (h[i + 1] < h[i])
                     for i in range(n - 1)]
            assert signs == sorted(signs, reverse=True)
            assert signs.count(0) <= 1
            interior = h[1:-1]
            levels = sorted(set(interior))
            thresholds = levels + [(a + b) / 2
                                    for a, b in zip(levels, levels[1:])]
            thresholds += [min(levels) - 1, max(levels) + 1]
            for threshold in thresholds:
                assert interior.count(threshold) <= 2
                upper = [i for i, value in enumerate(interior)
                         if value > threshold]
                if upper:
                    assert upper == list(range(upper[0], upper[-1] + 1))
                level_cases += 1
            path_cases += 1

    # A subdivided theta block is biconnected and has cycle rank two.
    # Test the strict two-terminal maximum principle with unequal conductances.
    for _ in range(60):
        edges = []
        n = 2
        for _ in range(3):
            vertices = [0]
            for _ in range(rng.randint(1, 4)):
                vertices.append(n)
                n += 1
            vertices.append(1)
            edges.extend((u, v, Q(rng.randint(1, 19), rng.randint(1, 17)))
                         for u, v in zip(vertices, vertices[1:]))
        h = dirichlet(n, edges, {0: Q(1), 1: Q(0)}, {})
        assert all(0 < h[v] < 1 for v in range(2, n))
        source = sum(a * (h[u] - h[v]) for u, v, a in edges if u == 0)
        assert source > 0
        # With any positive prescribed terminal current, the block has
        # positive terminal drop and all interiors remain in its open range.
        scale = Q(2, 7) / source
        assert all(0 < scale * h[v] < scale for v in range(2, n))
        block_cases += 1
    print(f"PASS: {path_cases} exact positive-source paths; "
          f"{level_cases} horizontal-level checks; "
          f"{block_cases} exact biconnected two-terminal blocks")


if __name__ == "__main__":
    main()
