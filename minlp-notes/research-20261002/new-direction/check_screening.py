"""Exact finite checks for screening-percolation.md; no asymptotic claim."""

from fractions import Fraction as F
from itertools import combinations
import random


def solve(matrix, rhs):
    n = len(rhs)
    work = [[F(x) for x in row] + [F(rhs[i])]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if work[i][col])
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for i in range(n):
            if i != col:
                scale = work[i][col]
                work[i] = [a - scale * b
                           for a, b in zip(work[i], work[col])]
    return [work[i][-1] for i in range(n)]


def support_solution(q, b, penalties, support):
    x = solve([[q[i][j] for j in support] for i in support],
              [b[i] for i in support])
    value = sum((penalties[i] - b[i] * xi
                 for i, xi in zip(support, x)), F(0))
    return value, x


def optimize(q, b, penalties, vertices):
    best, best_support, best_x = F(0), [], []
    for mask in range(1 << len(vertices)):
        support = [i for j, i in enumerate(vertices) if mask >> j & 1]
        value, x = support_solution(q, b, penalties, support)
        if value < best:
            best, best_support, best_x = value, support, x
    return best, best_support, best_x


def components(q, retained):
    unseen = set(retained)
    result = []
    while unseen:
        component = [unseen.pop()]
        for i in component:
            fresh = {j for j in unseen if q[i][j]}
            unseen -= fresh
            component.extend(sorted(fresh))
        result.append(sorted(component))
    return result


def main():
    rng = random.Random(20261002)
    instances = support_bounds = screened = split_instances = 0
    for n in range(2, 9):
        for trial in range(10):
            q = [[F(0) for _ in range(n)] for _ in range(n)]
            degree = [0] * n
            edges = list(combinations(range(n), 2))
            rng.shuffle(edges)
            for i, j in edges:
                if degree[i] < 3 and degree[j] < 3 and rng.randrange(3):
                    q[i][j] = q[j][i] = F(rng.choice([-2, -1, 1, 2]), 7)
                    degree[i] += 1
                    degree[j] += 1
            for i in range(n):
                q[i][i] = 1 + sum(abs(q[i][j]) for j in range(n))
            b = [F(rng.randrange(-5, 6), 3) for _ in range(n)]
            penalties = [F(rng.randrange(0, 50), 4) for _ in range(n)]
            comparison = [[q[i][i] if i == j else -abs(q[i][j])
                           for j in range(n)] for i in range(n)]
            r = solve(comparison, [abs(x) for x in b])
            limits = [q[i][i] * r[i] ** 2 for i in range(n)]
            retained = [i for i in range(n) if penalties[i] <= limits[i]]
            screened += n - len(retained)

            for mask in range(1 << n):
                support = [i for i in range(n) if mask >> i & 1]
                _, x = support_solution(q, b, penalties, support)
                assert all(abs(xi) <= r[i] for i, xi in zip(support, x))
                support_bounds += 1
                # Independently test the stationary-ellipsoid equality.
                assert sum(xi * q[i][j] * xj
                           for i, xi in zip(support, x)
                           for j, xj in zip(support, x)) == sum(
                               b[i] * xi for i, xi in zip(support, x))

            full = optimize(q, b, penalties, list(range(n)))[0]
            parts = components(q, retained)
            split_instances += len(parts) > 1
            screened_opt = sum((optimize(q, b, penalties, part)[0]
                                for part in parts), F(0))
            assert full == screened_opt
            instances += 1

    # An equality at the threshold must survive safe screening.
    q, b, penalties = [[F(1)]], [F(1)], [F(1)]
    retained = [i for i in range(1) if penalties[i] <= q[i][i] * b[i] ** 2]
    assert retained == [0]
    assert support_solution(q, b, penalties, [0])[0] == 0
    assert optimize(q, b, penalties, [0])[0] == 0

    # Negative penalties retain a coordinate even when its optimizer is zero.
    q, b, penalties = [[F(1)]], [F(0)], [F(-1)]
    retained = [i for i in range(1) if penalties[i] <= q[i][i] * b[i] ** 2]
    assert retained == [0]
    assert optimize(q, b, penalties, retained) == (F(-1), [0], [F(0)])

    # Exact rational PGF supersolution for degree 3, p=1/10, a=21/10.
    p, a, upper = F(1, 10), F(21, 10), F(4)
    assert a * (1 - p + p * upper) ** 2 <= upper
    h = a
    for _ in range(8):
        h = a * (1 - p + p * h) ** 2
        assert h <= upper

    # Ordinary subcriticality does not suffice for the enumeration moment.
    p = F(1, 5)
    assert 2 * p < 1
    assert 2 * p * (1 - p) > F(1, 4)
    h = F(2)
    for _ in range(10):
        h = 2 * (1 - p + p * h) ** 2
    assert h > 1000

    # Heterogeneous certificate on a cycle, checked against all 16 outcomes.
    probabilities = [F(1, 100), F(1, 2), F(1, 100), F(1, 2)]
    neighbors = [{1, 3}, {0, 2}, {1, 3}, {0, 2}]
    a = F(21, 10)
    branch = {(v, u): F(4) if v % 2 == 0 else F(11, 5)
              for v in range(4) for u in neighbors[v]}
    root_bounds = []
    for v in range(4):
        root_bound = a
        for w in neighbors[v]:
            root_bound *= 1 - probabilities[w] + probabilities[w] * branch[w, v]
        root_bounds.append(root_bound)
        for u in neighbors[v]:
            rhs = a
            for w in neighbors[v] - {u}:
                rhs *= 1 - probabilities[w] + probabilities[w] * branch[w, v]
            assert rhs <= branch[v, u]
    moments = [F(0)] * 4
    cycle = [[F(int(w in neighbors[v])) for w in range(4)] for v in range(4)]
    for mask in range(16):
        retained = [v for v in range(4) if mask >> v & 1]
        probability = F(1)
        for v in range(4):
            probability *= probabilities[v] if v in retained else 1 - probabilities[v]
        for component in components(cycle, retained):
            for v in component:
                moments[v] += probability * a ** len(component)
    assert all(moments[v] <= probabilities[v] * root_bounds[v] for v in range(4))

    # A fixed-active center induces a nonzero leaf-to-leaf interaction.
    q = [[F(2), F(1, 3), F(1, 4)],
         [F(1, 3), F(1), F(0)],
         [F(1, 4), F(0), F(1)]]
    assert q[1][2] == 0
    assert q[1][2] - q[1][0] * q[0][2] / q[0][0] == -F(1, 24)
    print(f"PASS: {instances} optimization instances; "
          f"{support_bounds} exact support bounds; {screened} screened "
          f"coordinates; {split_instances} instances with several components.")
    print("PASS: threshold retention, signed zero activation, PGF "
          "supersolution and divergence, heterogeneous cycle certificate, "
          "and active-mediator counterexample.")


if __name__ == "__main__":
    main()
