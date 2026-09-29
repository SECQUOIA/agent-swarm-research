"""Targeted exact checks for free-frontier.md; standard library only.

This enumerates tiny support QPs as a verification oracle. It does not implement
the polynomial submodular oracle used in the theorem.
"""

from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
from random import Random


def solve(a, b):
    n = len(b)
    rows = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [v / scale for v in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [v - scale * w for v, w in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def quad(q, x):
    return dot(x, [dot(row, x) for row in q])


def optimum(q, b, c, stieltjes=False):
    """Exact nonnegative unbounded-coordinate on/off minimum."""
    n = len(b)
    best = None
    for z in product((0, 1), repeat=n):
        support = [i for i in range(n) if z[i]]
        # Stieltjes inverse positivity applies when the test b_i are positive.
        faces = [support] if stieltjes and all(v >= 0 for v in b) else [
            [i for i, on in zip(support, active) if on]
            for active in product((0, 1), repeat=len(support))
        ]
        for active in faces:
            x = [F(0)] * n
            if active:
                vals = solve([[q[i][j] for j in active] for i in active],
                             [b[i] for i in active])
                if any(v < 0 for v in vals):
                    continue
                for i, val in zip(active, vals):
                    x[i] = val
            if any(dot(q[i], x) - b[i] < 0 for i in support if i not in active):
                continue
            value = quad(q, x) - 2 * dot(b, x) + dot(c, z)
            if best is None or value < best[0]:
                best = value, x, z
    assert best is not None
    return best


def grid(dplus, epsilon, mu):
    ratio = dplus / (epsilon * mu)
    m = max(1, isqrt(ratio.numerator // ratio.denominator))
    while m * m < ratio:
        m += 1
    return sorted({r for j in range(1, m + 1)
                   for r in (F(j * j, m * m), F(m * m, j * j))})


def majorant(q, edges, ratios):
    out = [row[:] for row in q]
    for (i, j), ratio in zip(edges, ratios):
        beta = q[i][j]
        out[i][i] += beta * ratio
        out[j][j] += beta / ratio
        out[i][j] = out[j][i] = F(0)
    return out


def main():
    rng = Random(20260927)
    geometry = instances = modified = 0
    sizes = set()
    for n, bad_count, count in ((3, 1, 12), (4, 1, 8), (3, 2, 4)):
        for _ in range(count):
            pairs = list(combinations(range(n), 2))
            rng.shuffle(pairs)
            edges = sorted(pairs[:bad_count])
            q = [[F(0) for _ in range(n)] for _ in range(n)]
            for i, j in pairs:
                q[i][j] = q[j][i] = F(rng.randint(1, 3), 10) * (
                    1 if (i, j) in edges else -1)
            for i in range(n):
                # Exact Gershgorin certificate Q >= I.
                q[i][i] = 1 + sum(abs(q[i][j]) for j in range(n) if j != i)
            b = [F(rng.randint(1, 5), 2) for _ in range(n)]
            if instances % 3 == 0:
                b[0] = -b[0]
            c = [F(rng.randint(-2, 12), 4) for _ in range(n)]
            mu, epsilon = F(1), F(1, (4, 16, 64)[instances % 3])
            dplus = max(sum(max(q[i][j], F(0)) for j in range(n) if j != i)
                        for i in range(n))
            ratios = grid(dplus, epsilon, mu)
            sizes.add(len(ratios))
            exact, xstar, _ = optimum(q, b, c)
            assert dot(xstar, xstar) <= dot(b, b) / (mu * mu)
            upper = None
            primal = None
            for choice in product(ratios, repeat=bad_count):
                qr = majorant(q, edges, choice)
                assert all(qr[i][j] <= 0 for i in range(n) for j in range(n)
                           if i != j)
                val, x, z = optimum(qr, b, c, stieltjes=True)
                original = quad(q, x) - 2 * dot(b, x) + dot(c, z)
                assert original <= val
                if upper is None or val < upper:
                    upper, primal = val, original
                modified += 1
            assert exact <= primal <= upper <= exact + epsilon * dot(b, b) / mu
            for _ in range(40):
                x = [F(0) if rng.randrange(5) == 0 else
                     F(rng.randint(1, 8)) * F(2) ** rng.randint(-12, 12)
                     for _ in range(n)]
                selected = []
                for i, j in edges:
                    selected.append(min(ratios, key=lambda r:
                                        r * x[i] ** 2 + x[j] ** 2 / r
                                        - 2 * x[i] * x[j]))
                qr = majorant(q, edges, selected)
                error = quad(qr, x) - quad(q, x)
                assert 0 <= error <= epsilon * mu * dot(x, x)
                geometry += 1
            instances += 1
    print(f"PASS: {instances} exact tiny optimization instances, "
          f"{modified} Stieltjes support-enumeration solves, "
          f"{geometry} rational square-grid checks; grid sizes {sorted(sizes)}.")


if __name__ == "__main__":
    main()
