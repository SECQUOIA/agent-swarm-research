"""Exact diagnostics for the second fixed-resource proof audit.

The proof, not these finite cases, supplies the universal guarantees.
Run with standard-library Python; all inequalities use Fraction arithmetic.
"""

from fractions import Fraction as F
from itertools import combinations, product
from math import comb, factorial, gcd


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def clip(x):
    return min(F(1), max(F(0), x))


def projection(q, rows, rhs):
    """Independent two-dimensional projection by faces of a bounded polygon."""
    def feasible(p):
        return all(dot(a, p) <= b for a, b in zip(rows, rhs))

    candidates = [q] if feasible(q) else []
    for a, b in zip(rows, rhs):
        norm = dot(a, a)
        if norm:
            scale = (dot(a, q) - b) / norm
            p = tuple(qi - scale * ai for qi, ai in zip(q, a))
            if feasible(p):
                candidates.append(p)
    for i, j in combinations(range(len(rows)), 2):
        a, c = rows[i], rows[j]
        determinant = a[0] * c[1] - a[1] * c[0]
        if determinant:
            p = ((rhs[i] * c[1] - a[1] * rhs[j]) / determinant,
                 (a[0] * rhs[j] - rhs[i] * c[0]) / determinant)
            if feasible(p):
                candidates.append(p)
    assert candidates
    return min(candidates, key=lambda p: sum((pi - qi) ** 2 for pi, qi in zip(p, q)))


def bregman_checks():
    grid = [F(i, 8) for i in range(9)]
    coefficient_sets = [tuple([F(0)] * (p - 1) + [F(1)]) for p in range(1, 13)]
    coefficient_sets += [(F(1, 2**30), F(0), F(3), F(0), F(2**20)),
                         (F(2**20), F(0), F(0), F(1, 2**30))]
    count = 0
    for a in coefficient_sets:
        degree = len(a)
        for u, v in product(grid, repeat=2):
            divergence = sum(aj * ((u ** (j + 1) - v ** (j + 1)) / (j + 1)
                                   - v ** j * (u - v))
                             for j, aj in enumerate(a, 1))
            bound = sum(a) * abs(u - v) ** (degree + 1) / (degree + 1)
            assert divergence >= bound, (a, u, v)
            count += 1
    return count


def signed_bregman_checks():
    """Monotone polynomials with negative coefficients and interior flat points."""
    count = 0
    grid = [F(i, 8) for i in range(9)]
    for degree, center in product([3, 5, 7], [F(1, 2), F(1, 3)]):
        scale = (1 - center) ** degree - (-center) ** degree
        a = [F(comb(degree, j)) * (-center) ** (degree - j) / scale
             for j in range(1, degree + 1)]
        assert sum(a) == 1
        for u, v in product(grid, repeat=2):
            s = abs(u - v)
            marginal_gap = abs(sum(aj * (u ** j - v ** j) for j, aj in enumerate(a, 1)))
            assert marginal_gap >= (s / (2 * degree)) ** degree / 2
            divergence = sum(aj * ((u ** (j + 1) - v ** (j + 1)) / (j + 1)
                                   - v ** j * (u - v))
                             for j, aj in enumerate(a, 1))
            assert divergence >= s ** (degree + 1) / (4 * (4 * degree) ** degree)
            count += 1
    return count


def residual_checks():
    count = repaired = degenerate = 0
    columns = [((1, 1), (-1, -1), (1, -2), (2, 2)),
               ((1, -2), (-1, 2), (-2, -1), (3, -6)),
               ((F(1, 7), F(-2, 3)), (F(-1, 7), F(2, 3)),
                (0, 0), (F(3, 7), -2))]
    stars = [(F(1, 4), F(3, 4)), (F(0), F(1, 2)), (F(1), F(0)),
             (F(0), F(0)), (F(1), F(1)), (F(2, 3), F(1, 3))]
    for raw_c, g, star in product(columns, [(F(1), F(1)), (F(1, 16), F(8))], stars):
        c = [tuple(map(F, row)) for row in raw_c]
        b = [dot(row, star) + (F(1, 3) if j == 2 else F(0)) for j, row in enumerate(c)]
        lam_star = (F(1), F(0), F(0), F(1, 2))
        box_normals = [F(-1, 3) if z == 0 else F(1, 5) if z == 1 else F(0) for z in star]
        ell = [g[i] * star[i] + sum(c[j][i] * lam_star[j] for j in range(4))
               + box_normals[i] for i in range(2)]
        assert tuple(clip((ell[i] - sum(c[j][i] * lam_star[j] for j in range(4))) / g[i])
                     for i in range(2)) == star
        rows = c + [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]
        rhs = b + [F(1), F(1), F(0), F(0)]
        denominator = 1
        for row in c:
            for a in row:
                denominator = denominator * a.denominator // gcd(denominator, a.denominator)
        m = max(1, *(abs(denominator * a) for row in rows for a in row))
        v_bound = factorial(2) * (1 + 2 * m * m) ** 2
        k_bound = denominator * 8 * m * v_bound
        gbar = 1 + max(g[i] + abs(ell[i]) for i in range(2))
        lipschitz = 2 * gbar
        mu = min(g) / 2

        def objective(z):
            return sum(g[i] * z[i] ** 2 / 2 - ell[i] * z[i] for i in range(2))

        trials = [lam_star, (F(0),) * 4, (F(2), F(1), F(0), F(0)),
                  (F(0), F(0), F(1), F(0)),
                  (F(1) + F(1, 1024), F(0), F(0), F(1, 2)),
                  (F(1), F(0), F(0), F(1, 2) - F(1, 1024))]
        for lam in trials:
            q = tuple(clip((ell[i] - sum(c[j][i] * lam[j] for j in range(4))) / g[i])
                      for i in range(2))
            residual = [dot(row, q) - bj for row, bj in zip(c, b)]
            delta = max(F(0), *residual)
            zeta = abs(dot(lam, residual))
            y = projection(q, rows, rhs)
            distance = max(abs(qi - yi) for qi, yi in zip(q, y))
            repaired += distance > 0
            degenerate += sum(dot(row, y) == bj for row, bj in zip(rows, rhs)) > 2
            assert distance <= k_bound * delta
            assert objective(q) + dot(lam, residual) <= objective(star)
            gap = objective(y) - objective(star)
            assert 0 <= gap <= lipschitz * distance + zeta
            assert mu * max(abs(yi - si) for yi, si in zip(y, star)) ** 2 <= gap
            leftover = max(F(0), max(abs(qi - si) for qi, si in zip(q, star)) - k_bound * delta)
            assert mu * leftover ** 2 <= lipschitz * k_bound * delta + zeta
            count += 1
    return count, repaired, degenerate


if __name__ == "__main__":
    bregman = bregman_checks()
    signed = signed_bregman_checks()
    residual, repaired, degenerate = residual_checks()
    print(f"PASS: {bregman} exact Bregman inequalities; {residual} residual transfers; "
          f"{repaired} nonzero repairs; {degenerate} degenerate projected faces; "
          f"{signed} signed-polynomial modulus and Bregman cases.")
