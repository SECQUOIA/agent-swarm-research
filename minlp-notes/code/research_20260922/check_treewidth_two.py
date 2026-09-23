"""Exact, small-instance checks of the two indicator-QP reductions.

Enumerates support patterns and solves their strictly convex QPs in Fraction
arithmetic. This checks examples and formulas, not the universal reductions,
spectral proofs, complexity statements, or novelty. No solver is used.
"""

from fractions import Fraction as F
from itertools import product


def solve(a, b):
    n = len(b)
    aug = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [v / scale for v in aug[j]]
        for i in range(n):
            if i != j:
                scale = aug[i][j]
                aug[i] = [v - scale * w for v, w in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def build(a, target, theta, bounded):
    n = len(a)
    q = [[F(0) for _ in range(2 * n)] for _ in range(2 * n)]
    h = [F(0)] * (2 * n)
    lam = [F(0)] * (2 * n)
    constant = F(0)

    def square(row, rhs, weight=F(1)):
        nonlocal constant
        for i, x in row.items():
            h[i] += weight * rhs * x
            for j, y in row.items():
                q[i][j] += weight * x * y
        constant += weight * rhs * rhs

    if bounded:
        magnitude = sum(a)
        b = [F(ai, magnitude) * theta ** (i + 1) for i, ai in enumerate(a)]
        endpoint = F(target, magnitude) * theta**n
        baseline = F(4)
        for i in range(n):
            q[2 * i][2 * i] += 1
            h[2 * i] += 1
            lam[2 * i] = lam[2 * i + 1] = F(1)
            row = {2 * i + 1: F(1), 2 * i: -b[i]}
            rhs = baseline
            if i:
                row[2 * i - 1] = -theta
                rhs *= 1 - theta
            square(row, rhs)
        square({2 * n - 1: F(1)}, baseline + endpoint, theta**2)
        gap = None
    else:
        gap = theta**2 * (1 - theta**2) / (1 + theta**4)
        for i, ai in enumerate(a):
            amplitude = F(ai) * theta ** (-(n - i))
            q[2 * i][2 * i] += 1
            h[2 * i] += amplitude
            lam[2 * i] = amplitude**2
            lam[2 * i + 1] = gap / (4 * n)
            row = {2 * i + 1: F(1), 2 * i: -theta}
            if i:
                row[2 * i - 1] = -theta
            square(row, F(0))
        square({2 * n - 1: F(1)}, F(target), theta**2)
    return q, h, lam, constant, gap


def check(a, target, theta, bounded):
    q, h, lam, constant, gap = build(a, target, theta, bounded)
    n = len(a)
    dim = 2 * n
    # Gershgorin bounds and the stated interleaved bandwidth.
    for i in range(dim):
        off = sum(abs(q[i][j]) for j in range(dim) if i != j)
        assert q[i][i] - off >= 1 - 3 * theta
        assert q[i][i] + off <= 1 + 3 * theta + 2 * theta**2
        assert all(q[i][j] == 0 for j in range(dim) if abs(i - j) > 2)
        if not bounded:
            assert q[i][i] == 1 + theta**2
    if bounded:
        assert 2 * max(map(abs, h)) <= 9
        assert all(v == 1 for v in lam)

    best, best_mask = None, None
    for mask in product((0, 1), repeat=dim):
        indices = [i for i, bit in enumerate(mask) if bit]
        values = solve([[q[i][j] for j in indices] for i in indices],
                       [h[i] for i in indices])
        obj = constant + sum(lam[i] for i in indices)
        obj -= sum(h[i] * x for i, x in zip(indices, values))
        if best is None or obj < best:
            best, best_mask = obj, mask
        if bounded and not all(mask[2 * i + 1] for i in range(n)):
            off_states = sum(not mask[2 * i + 1] for i in range(n))
            assert obj >= n + ((1 - 3 * theta) * 16 - 1) * off_states
    yes = any(sum(ai * zi for ai, zi in zip(a, bits)) == target
              for bits in product((0, 1), repeat=n))
    if bounded:
        assert (best == n) == yes
        assert all(best_mask[2 * i + 1] for i in range(n))
        assert best <= n + theta**2
    elif yes:
        assert best <= gap / 4
    else:
        assert best > gap
    return 2**dim


def main():
    checked = 0
    cases = [([2, 3, 6], 5), ([2, 3, 6], 7), ([2, 4, 7], 6),
             ([2, 4, 7], 8), ([1, 3, 5, 9], 7), ([1, 3, 5, 9], 6)]
    for theta in (F(1, 10), F(1, 20)):
        for a, target in cases:
            for bounded in (False, True):
                checked += check(a, target, theta, bounded)
    # The first Hessian is independent of encoded SUBSET SUM data.
    assert build([1, 2, 3], 4, F(1, 10), False)[0] == \
        build([13, 27, 49], 62, F(1, 10), False)[0]
    print(f"PASS: 24 rational instances, {checked} support QPs; "
          "gaps, all-on states, spectra, bandwidth, fixed-Hessian identity")


if __name__ == "__main__":
    main()
