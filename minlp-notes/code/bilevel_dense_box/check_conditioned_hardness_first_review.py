"""Independent exact rational follower/KKT checks for conditioned SAT encoding.

This small-instance checker does not replace the uniform analytic proof.
"""
from fractions import Fraction as F
from itertools import combinations, product


def solve(matrix, rhs):
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(rhs)
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        value = a[j][j]
        a[j] = [v / value for v in a[j]]
        for i in range(j + 1, n):
            value = a[i][j]
            if value:
                a[i] = [v - value * w for v, w in zip(a[i], a[j])]
    answer = [F(0)] * n
    for i in reversed(range(n)):
        answer[i] = a[i][-1] - sum(a[i][j] * answer[j] for j in range(i + 1, n))
    return answer


def construct(n, clauses):
    size = 3 * n + len(clauses)
    A = [[F(0)] * size for _ in range(size)]
    b0, b1 = [F(0)] * size, [F(0)] * size
    for i in range(n):
        for row in (2 * i, 2 * i + 1):
            b0[row] = -1 if row == 2 * i else -2
            b1[row] = 3 ** (i + 1)
            for j in range(i):
                A[row][2 * j] = -2 * 3 ** (i - j)
                A[row][2 * j + 1] = 2 * 3 ** (i - j)
        A[2 * n + i][2 * i], A[2 * n + i][2 * i + 1] = 2, -2
        b0[2 * n + i] = -1
    for k, clause in enumerate(clauses):
        row = 3 * n + k
        b0[row] = 1 - sum(lit < 0 for lit in clause)
        for lit in clause:
            j, sign = abs(lit) - 1, 1 if lit > 0 else -1
            A[row][2 * j] -= sign
            A[row][2 * j + 1] += sign
    C = 2 * 3 ** n
    M = (1 + size * C) ** size
    theta = F(1, 100 * size * C * M)
    scales = [F(1, 4 * C) * theta ** i for i in range(size)]
    B = [[scales[i] * A[i][j] / scales[j] for j in range(size)] for i in range(size)]
    H = [[F(i == j) - B[i][j] for j in range(size)] for i in range(size)]
    Q = [[sum(H[k][i] * H[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
    assert max(sum(abs(v) for v in row) for row in B) <= F(1, 50)
    assert max(sum(abs(B[i][j]) for i in range(size)) for j in range(size)) <= F(1, 50)
    assert max(abs(v) for row in Q for v in row) <= 2
    ell = [v for _ in range(n) for v in (2, -2)] + [-2] * n + [2] * len(clauses)
    return A, b0, b1, scales, H, Q, ell, C, M, theta


def check(n, clauses, leaders):
    A, b0, b1, scales, H, Q, ell, C, M, theta = construct(n, clauses)
    size = len(scales)
    attempts = 0
    for x in leaders:
        forcing = [F(a) + x * b for a, b in zip(b0, b1)]
        h = []
        for i in range(size):
            h.append(max(F(0), forcing[i] + sum(A[i][j] * h[j] for j in range(i))))
        assert all(0 <= v <= 2 for v in h)
        residual = [h[i] - forcing[i] - sum(A[i][j] * h[j] for j in range(size)) for i in range(size)]
        assert all(0 <= v <= 2 for v in residual)
        rhs = [sum(H[k][i] * scales[k] * forcing[k] for k in range(size)) for i in range(size)]
        seed = {i for i, value in enumerate(h) if value > 0}
        # Enumerate nearest lower/free faces until exact full box KKT holds.
        # A found witness is independently sufficient by positive definiteness.
        follower = None
        for changes in range(size + 1):
            for flips in combinations(range(size), changes):
                free = sorted(seed.symmetric_difference(flips))
                answer = solve([[Q[i][j] for j in free] for i in free], [rhs[i] for i in free])
                u = [F(0)] * size
                for i, value in zip(free, answer):
                    u[i] = value
                attempts += 1
                if not all(0 <= value <= 1 for value in u):
                    continue
                gradient = [sum(Q[i][j] * u[j] for j in range(size)) - rhs[i] for i in range(size)]
                if all((value == 0 and g >= 0) or (value == 1 and g <= 0) or
                       (0 < value < 1 and g == 0) for value, g in zip(u, gradient)):
                    follower = u
                    break
            if follower is not None:
                break
        assert follower is not None
        error = max(abs(follower[i] / scales[i] - h[i]) for i in range(size))
        assert error <= 8 * M * C * theta ** 2
        assert error <= F(1, 16 * size)
        score = sum(a * b for a, b in zip(ell, h))
        value = scales[-1] * sum(ell[i] * follower[i] / scales[i] for i in range(size))
        assert abs(value - scales[-1] * score) <= scales[-1] / 8
        if score == 0:
            assert value <= scales[-1] / 8
        if n == 3 and len(clauses) == 8:
            assert score >= 2
            assert value >= 15 * scales[-1] / 8
    return len(leaders), attempts


def run():
    count = attempts = 0
    unsat = [tuple(sign * (i + 1) for i, sign in enumerate(signs))
             for signs in product((-1, 1), repeat=3)]
    for n, clauses in [(1, []), (2, []), (3, [(1, -2, 3)]), (3, unsat)]:
        leaders = {F(0), F(1), F(1, 2), F(1, 3), F(2, 3)}
        leaders.update(sum(F(2 * bit, 3 ** (i + 1)) for i, bit in enumerate(bits)) +
                       F(1, 2 * 3 ** n) for bits in product((0, 1), repeat=n))
        checked, tried = check(n, clauses, sorted(leaders))
        count += checked
        attempts += tried
        print(f'n={n}, clauses={len(clauses)}: {checked} exact followers passed', flush=True)
    print(f'PASS: {count} exact box KKT/error/gap checks; {attempts} rational active systems.')


if __name__ == '__main__':
    run()
