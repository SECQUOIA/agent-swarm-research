"""Exact finite checks for integer-structure-exploration.md.

Uses only the Python standard library. These checks verify the displayed
rank-one identities and the optimal-parameter matroid greedy implication.
They do not implement arrangement enumeration or prove the general theorem.
"""

from fractions import Fraction as F
from itertools import product
from random import Random


def solve(matrix, rhs):
    """Small exact linear solve, independent of the closed-form identities."""
    n = len(rhs)
    rows = [[F(x) for x in row] + [F(rhs[i])] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def positive_update_checks():
    instances = supports = 0
    for n in range(1, 5):
        for weights in product(range(1, 4), repeat=n):
            tau2 = F(1, (2 * n * max(weights)) ** 2)
            # Independent include-or-exclude dynamic program from the note.
            best_square_sum = {0: 0}
            for weight in weights:
                new = dict(best_square_sum)
                for total, square_sum in best_square_sum.items():
                    new[total + weight] = max(new.get(total + weight, -1), square_sum + weight**2)
                best_square_sum = new
            for target in range(1, sum(weights) + 1):
                instances += 1
                values = []
                for bits in product((0, 1), repeat=n):
                    supports += 1
                    chosen = [i for i in range(n) if bits[i]]
                    total = sum(weights[i] for i in chosen)
                    square_sum = sum(weights[i] ** 2 for i in chosen)
                    denominator = 1 + tau2 * square_sum
                    x = [F(0)] * n
                    for i in chosen:
                        x[i] = 1 + tau2 * weights[i] * (target - total) / denominator
                        assert F(3, 4) <= x[i] <= F(5, 4)
                    residual = sum(weights[i] * x[i] for i in range(n)) - target
                    for i in chosen:
                        assert x[i] - 1 + tau2 * weights[i] * residual == 0
                    value = sum((x[i] - bits[i]) ** 2 for i in range(n)) + tau2 * residual**2
                    formula = tau2 * (target - total) ** 2 / denominator
                    assert value == formula
                    assert (value == 0) == (target == total)
                    if target != total:
                        assert value >= tau2 / (1 + F(1, 4 * n))
                    values.append(value)
                dynamic_value = min(
                    tau2 * (target - total) ** 2 / (1 + tau2 * square_sum)
                    for total, square_sum in best_square_sum.items()
                )
                assert dynamic_value == min(values)
    return instances, supports


def matroid_checks():
    rng = Random(20260925)
    n, rank = 6, 2
    total_supports = 0
    for _ in range(40):
        loading = [[F(rng.randint(-1, 1)) for _ in range(rank)] for _ in range(n)]
        linear = [F(rng.randint(-4, 4)) for _ in range(n)]
        costs = [F(rng.randint(-2, 4), 7) for _ in range(n)]
        # ||U||_2^2 <= ||U||_F^2 <= 12 < 24 proves positive definiteness.
        q = [[F(24 * (i == j)) - sum(loading[i][k] * loading[j][k] for k in range(rank))
              for j in range(n)] for i in range(n)]

        def independent(chosen):
            return all(sum(i in chosen for i in (2 * block, 2 * block + 1)) <= 1 for block in range(3))

        for bases in (False, True):
            candidates = []
            for bits in product((0, 1), repeat=n):
                chosen = tuple(i for i in range(n) if bits[i])
                if not independent(chosen) or (bases and len(chosen) != 3):
                    continue
                total_supports += 1
                active = solve([[q[i][j] for j in chosen] for i in chosen], [linear[i] for i in chosen])
                x = [F(0)] * n
                for i, value in zip(chosen, active):
                    x[i] = value
                value = sum(costs[i] - linear[i] * x[i] for i in chosen)
                candidates.append((value, chosen, x))
            optimum, _, optimum_x = min(candidates)
            y = [sum(loading[i][k] * optimum_x[i] for i in range(n)) for k in range(rank)]
            gains = [costs[i] - (linear[i] + sum(loading[i][k] * y[k] for k in range(rank))) ** 2 / 24
                     for i in range(n)]
            selected = []
            for i in sorted(range(n), key=lambda j: (gains[j], j)):
                if (bases or gains[i] < 0) and independent(selected + [i]):
                    selected.append(i)
            selected = tuple(sorted(selected))
            selected_value = next(value for value, chosen, _ in candidates if chosen == selected)
            assert selected_value == optimum
            envelope = sum(t * t for t in y) + sum(gains[i] for i in selected)
            assert envelope == optimum
    return total_supports


def main():
    instances, supports = positive_update_checks()
    matroid_supports = matroid_checks()
    print(f"PASS: {instances} positive-update instances; {supports} exact support checks; dynamic-program values agree")
    print(f"PASS: 40 signed rank-two instances, independent-set and basis variants; {matroid_supports} exact support solves")


if __name__ == "__main__":
    main()
