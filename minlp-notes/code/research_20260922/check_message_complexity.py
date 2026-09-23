"""Exact targeted checks for the scalar Bellman-message construction.

The support QPs are assembled from the original residual rows and solved by
rational Gaussian elimination, independently of the claimed value formula.
This is finite-instance evidence, not a proof of the asymptotic lower bound.
"""

from fractions import Fraction as F
from itertools import product


def solve(matrix, rhs):
    a = [list(row) + [b] for row, b in zip(matrix, rhs)]
    n = len(a)
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        p = a[j][j]
        a[j] = [v / p for v in a[j]]
        for i in range(n):
            if i != j:
                p = a[i][j]
                a[i] = [u - p * v for u, v in zip(a[i], a[j])]
    return [row[-1] for row in a]


def direct_value(theta, b, z, terminal):
    n = len(z)
    variables = [("x", i) for i in range(n) if z[i]]
    variables += [("s", i) for i in range(n - 1)]
    indices = {v: j for j, v in enumerate(variables)}
    rows, constants = [], []

    def add(coefficients, constant):
        rows.append([F(coefficients.get(v, 0)) for v in variables])
        constants.append(F(constant))

    for i in range(n):
        if z[i]:
            add({("x", i): 1}, -1)
        coefficients = {("x", i): -b[i], ("s", i): 1}
        if i:
            coefficients[("s", i - 1)] = -theta
        add(coefficients, terminal if i == n - 1 else 0)
    size = len(indices)
    matrix = [[sum(row[i] * row[j] for row in rows)
               for j in range(size)] for i in range(size)]
    rhs = [-sum(row[i] * c for row, c in zip(rows, constants))
           for i in range(size)]
    optimum = solve(matrix, rhs)
    return sum((sum(a * x for a, x in zip(row, optimum)) + c) ** 2
               for row, c in zip(rows, constants))


def main():
    qps, centers_checked, neighborhoods = 0, 0, 0
    for theta in (F(1, 10), F(1, 20)):
        for n in range(1, 6):
            total = 2 ** n - 1
            b = [F(2 ** i, total) * theta ** (i + 1) for i in range(n)]
            w = [theta ** (n - i - 1) for i in range(n)]
            h = theta ** n / total
            cap = (1 + theta ** 2) / (1 - theta ** 2)
            pieces = []
            for z in product((0, 1), repeat=n):
                center = sum(wi * bi * zi for wi, bi, zi in zip(w, b, z))
                denominator = sum(wi ** 2 for wi in w)
                denominator += sum((wi * bi) ** 2 * zi
                                   for wi, bi, zi in zip(w, b, z))
                assert 1 <= denominator <= cap < 2
                pieces.append((z, center, denominator))
                points = {F(0), F(1), F(1, 2), center,
                          max(F(0), center - h / 3), center + h / 3}
                for t in points:
                    expected = (t - center) ** 2 / denominator
                    assert direct_value(theta, b, z, t) == expected
                    qps += 1
            assert sorted(c for _, c, _ in pieces) == [k * h for k in range(2 ** n)]
            for z, center, denominator in pieces:
                others = [(c, d) for zz, c, d in pieces if zz != z]
                assert min((center - c) ** 2 / d for c, d in others) >= h ** 2 / cap
                centers_checked += 1
                for t in (max(F(0), center - h / 3), center + h / 3):
                    assert (t - center) ** 2 / denominator < min(
                        (t - c) ** 2 / d for c, d in others)
                    neighborhoods += 1
            max_center = theta ** n
            max_denominator = next(d for _, c, d in pieces if c == max_center)
            for k in range(2 * total + 1):
                t = k * h / 2
                value = min((t - c) ** 2 / d for _, c, d in pieces)
                assert 0 <= value <= h ** 2 / 4
            for t in (max_center, (1 + max_center) / 2, F(1)):
                assert min((t - c) ** 2 / d for _, c, d in pieces) == (
                    t - max_center) ** 2 / max_denominator
    print(f"PASS: {qps} exact support QPs, {centers_checked} centers, "
          f"{neighborhoods} neighborhood endpoints; n=1..5, theta=1/10,1/20")


if __name__ == "__main__":
    main()
