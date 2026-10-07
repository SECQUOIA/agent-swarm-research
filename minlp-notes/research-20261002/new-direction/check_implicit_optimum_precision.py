"""Exact finite witnesses for implicit-optimum-precision-obstruction.md.

The note supplies proofs for all dimensions. These checks supplement those
proofs; they do not establish universal claims by sampling.
"""

from fractions import Fraction as Q
from itertools import product
from random import Random


def positive_definite(matrix):
    """Exact symmetric elimination; positive pivots certify positive definiteness."""
    a = [row[:] for row in matrix]
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot > 0
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot


def check():
    rng = Random(20261002)
    configurations = 0
    sign_boxes = 0
    for n in (1, 2, 3, 5, 8):
        a = [Q(1, 4)]
        for i in range(1, n + 1):
            a.append(a[-1] ** 2 / 4)
        for i, ai in enumerate(a):
            m = 4 * 2**i - 2
            assert ai == Q(1, 2**m)
            assert ai.denominator.bit_length() == m + 1
            assert 0 < ai < Q(1, 2)
        assert a[-1] - a[-2] ** 2 / 8 == a[-1] / 2
        assert (a[-1] - a[-2] ** 2 / 8) / 4 == a[-1] / 8

        for sample in range(24):
            # Include both full-box corners and the exact optimizer.
            x = ([Q(0)] * (n + 1) if sample == 0 else
                 [Q(1, 2)] * (n + 1) if sample == 1 else
                 a[:] if sample == 2 else
                 [Q(rng.randrange(17), 32) for _ in a])
            y = Q(rng.randrange(17), 32)
            r = [x[0] - Q(1, 4)] + [
                x[i] - x[i - 1] ** 2 / 4 for i in range(1, n + 1)
            ]
            e = [xi - ai for xi, ai in zip(x, a)]
            assert r[0] == e[0]
            for i in range(1, n + 1):
                assert r[i] == e[i] - (x[i - 1] + a[i - 1]) * e[i - 1] / 4
            value = sum(ri**2 for ri in r)
            error = sum(ei**2 for ei in e)
            assert value >= Q(9, 16) * error

            size = n + 1
            jac = [[Q(i == j) for j in range(size)] for i in range(size)]
            for i in range(1, size):
                jac[i][i - 1] = -x[i - 1] / 2
            hess = [[2 * sum(jac[k][i] * jac[k][j] for k in range(size))
                     for j in range(size)] for i in range(size)]
            for i in range(n):
                hess[i][i] -= r[i + 1]
            for i in range(size):
                assert hess[i][i] == (2 + 3 * x[i] ** 2 / 4 - x[i + 1]
                                     if i < n else 2)
                assert hess[i][i] <= Q(35, 16)
                for j in range(i + 1, size):
                    assert hess[i][j] == (-x[i] if j == i + 1 else 0)
            positive_definite([[hess[i][j] - (Q(5, 8) if i == j else 0)
                                for j in range(size)] for i in range(size)])

            h = x[n] - x[n - 1] ** 2 / 8
            assert h == (x[n] + r[n]) / 2
            augmented = value + y**2 + y * h / 4
            assert augmented >= Q(15, 16) * (value + y**2)
            assert augmented >= Q(135, 256) * (error + y**2)
            # The stronger identity also checks the Young-inequality step.
            assert augmented - Q(15, 16) * (value + y**2) == (
                sum(ri**2 for ri in r[:-1]) + (y + r[-1]) ** 2
            ) / 16 + y * x[n] / 8

            perturb = [[Q(0) for _ in range(size + 1)] for _ in range(size + 1)]
            perturb[n - 1][n - 1] = -y / 16
            perturb[n - 1][size] = perturb[size][n - 1] = -x[n - 1] / 16
            perturb[n][size] = perturb[size][n] = Q(1, 4)
            assert max(sum(map(abs, row)) for row in perturb) <= Q(9, 32)
            full = [row + [Q(0)] for row in hess] + [[Q(0)] * size + [Q(2)]]
            for i in range(size + 1):
                for j in range(size + 1):
                    full[i][j] += perturb[i][j]
                assert full[i][i] <= Q(35, 16)
            positive_definite([[full[i][j] - (Q(11, 32) if i == j else 0)
                                for j in range(size + 1)] for i in range(size + 1)])
            configurations += 1

        # Tight, sign-valid boxes and boundary-touching, sign-invalid boxes.
        # Only the last two coordinates enter the derivative on the active face.
        for previous in ((a[-2], a[-2]), (a[-2] / 2, a[-2]),
                         (a[-2], 2 * a[-2])):
            for terminal in ((Q(0), a[-1]), (a[-1] / 2, a[-1]),
                             (a[-1], 2 * a[-1])):
                lower = (terminal[0] - previous[1] ** 2 / 8) / 4
                corners = [(v - u**2 / 8) / 4 for u, v in product(previous, terminal)]
                assert lower == min(corners)
                if lower >= 0:
                    ell = terminal[0]
                    assert 0 < a[-1] / 2 <= ell <= a[-1]
                    assert ell.denominator >= 2 ** (4 * 2**n - 2)
                sign_boxes += 1

    assert Q(35, 16) / Q(9, 16) == Q(35, 9)
    assert Q(35, 16) / Q(135, 256) == Q(112, 27)
    print(f"PASS: {configurations} exact configurations, {sign_boxes} sign boxes, "
          "five recurrence horizons, and both conditioning ratios.")


if __name__ == "__main__":
    check()
