"""Exact finite checks of two limitations accompanying the gain scheme.

This does not implement the approximation algorithm or prove its complexity.
"""

from fractions import Fraction as F
from itertools import combinations, product


def solve(matrix, rhs):
    rows = [[F(x) for x in row] + [F(b)] for row, b in zip(matrix, rhs)]
    for j in range(len(rows)):
        pivot = next(i for i in range(j, len(rows)) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [v / scale for v in rows[j]]
        for i in range(len(rows)):
            if i != j:
                scale = rows[i][j]
                rows[i] = [a - scale * b for a, b in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def gain(Q, b, support):
    support = tuple(support)
    if not support:
        return F(0)
    selected_b = [b[i] for i in support]
    x = solve([[Q[i][j] for j in support] for i in support], selected_b)
    return sum((a * z for a, z in zip(selected_b, x)), F(0))


def main():
    reductions = 0
    for n in range(1, 5):
        for weights in product(range(1, 4), repeat=n):
            padded = weights + (0,) * n
            M = max(weights) + 1
            all_supports = [tuple(i for i in range(2 * n) if mask >> i & 1)
                            for mask in range(1 << (2 * n))]
            attainable = {sum(weights[i] for i in range(n) if mask >> i & 1)
                          for mask in range(1 << n)}
            for target in range(sum(weights) + 1):
                feasible = [S for S in all_supports
                            if sum(padded[i] for i in S) <= target
                            and sum(M - padded[i] for i in S) <= n * M - target]
                optimum = max(map(len, feasible))
                assert optimum <= n
                assert (optimum == n) == (target in attainable)
                if optimum == n:
                    epsilon = F(1, 2 * n)
                    assert (1 - epsilon) * optimum > n - 1
                reductions += 1
    greedy_cases = 0
    for L in range(2, 33):
        u = [F(L), F(L), F(0)]
        b = [F(1), F(-1), F(1, L)]
        Q = [[F(i == j) + u[i] * u[j] for j in range(3)] for i in range(3)]
        singleton = [gain(Q, b, [i]) for i in range(3)]
        first = max(range(3), key=lambda i: singleton[i])
        assert first == 2
        second = max((i for i in range(3) if i != first),
                     key=lambda i: gain(Q, b, [first, i]))
        greedy = gain(Q, b, [first, second])
        optimum = max(gain(Q, b, S) for S in combinations(range(3), 2))
        assert gain(Q, b, [0, 1]) == optimum == 2
        assert greedy == F(1, L * L) + F(1, 1 + L * L)
        assert greedy / optimum < F(1, L * L)
        greedy_cases += 1
    print(f"two_budget_reductions={reductions}; greedy_counterexamples={greedy_cases}")
    print("All exact boundary assertions passed.")


if __name__ == "__main__":
    main()
