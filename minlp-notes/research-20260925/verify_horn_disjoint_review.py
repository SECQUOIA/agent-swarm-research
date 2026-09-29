"""Independent Fraction/LDL check of the five-variable Horn witness.

Only the 3^5 disjoint-multiplier LMIs are checked. No SDP solver is used.
"""

from fractions import Fraction as F
from itertools import combinations, product


N = 5
EPS = F(1, 10**6)
DELTA = F(1, 100)


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def coefficient(power):
    support = [i for i, degree in enumerate(power) if degree]
    repeated = [i for i, degree in enumerate(power) if degree == 2]
    assert max(power) <= 2 and len(repeated) <= 1
    if repeated:
        return F(1 if len(support) == 1 else 40)
    if len(support) == 0:
        return F(1)
    if len(support) == 1:
        return F(1, 10)
    if len(support) == 2:
        i, j = support
        return F(13, 20) if (i - j) % 5 in (1, 4) else F(1, 10)
    return F(1)


def pivot_check(matrix):
    """Exact unpivoted symmetric elimination; positive pivots imply PD."""
    a = [row[:] for row in matrix]
    pivots = []
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot > 0, (k, pivot, matrix)
        pivots.append(pivot)
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return min(pivots)


def entry(row, col, fixed_ones, fixed_zeros):
    # Congruence by diag(1, eps^-1, ...) and division by eps^|I|
    # leave just eps^|T| multiplying each complement-expansion term.
    total = F(0)
    for selected in subsets(fixed_zeros):
        power = [0] * N
        for i in (*fixed_ones, *selected):
            power[i] += 1
        if row is not None:
            power[row] += 1
        if col is not None:
            power[col] += 1
        total += (-EPS) ** len(selected) * coefficient(power)
    return total


def main():
    count = 0
    min_pivot = None
    max_perturbation = F(0)
    entry_bound = 40 * ((1 + EPS) ** N - 1)
    norm_bound = 6 * entry_bound
    assert norm_bound < F(144, 100000)
    assert norm_bound < DELTA
    for status in product(range(3), repeat=N):
        ones = [i for i, state in enumerate(status) if state == 1]
        zeros = [i for i, state in enumerate(status) if state == 2]
        rows = [None] + [i for i, state in enumerate(status) if state == 0]
        actual = [[entry(i, j, ones, zeros) for j in rows] for i in rows]
        leading = [[entry(i, j, ones, ()) for j in rows] for i in rows]
        shifted = [row[:] for row in leading]
        for i in range(len(rows)):
            shifted[i][i] -= DELTA
        pivot_check(shifted)
        pivot = pivot_check(actual)
        min_pivot = pivot if min_pivot is None else min(min_pivot, pivot)
        for i in range(len(rows)):
            for j in range(len(rows)):
                perturbation = abs(actual[i][j] - leading[i][j])
                assert perturbation <= entry_bound
                max_perturbation = max(max_perturbation, perturbation)
        count += 1
    objective = N * EPS**2 + 2 * EPS**2 * (-5 * F(13, 20) + 5 * F(1, 10))
    assert objective == -EPS**2 / 2
    print(f"Passed {count} exact positive-definiteness checks.")
    print(f"Passed {count} exact limiting eigenvalue lower-bound checks (> 1/100).")
    print(f"Smallest exact LDL pivot: {min_pivot}")
    print(f"Largest entry perturbation: {max_perturbation}")
    print(f"Uniform spectral perturbation bound: {norm_bound}")
    print(f"Horn objective: {objective}")


if __name__ == "__main__":
    main()
