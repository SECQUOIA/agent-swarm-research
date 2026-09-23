"""Independent exact diagnostics for the fixed-resource accuracy-bit proof.

Uses Fraction arithmetic, not an optimization solver. These finite checks
supplement the proof; they do not certify the asymptotic algorithm.
"""

from fractions import Fraction as F
from itertools import combinations, product
from random import Random
from math import comb


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def solve(a, b):
    n = len(b)
    m = [[F(x) for x in row] + [F(rhs)] for row, rhs in zip(a, b)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if m[i][j]), None)
        if pivot is None:
            return None
        m[j], m[pivot] = m[pivot], m[j]
        div = m[j][j]
        m[j] = [x / div for x in m[j]]
        for i in range(n):
            if i != j:
                factor = m[i][j]
                m[i] = [x - factor * y for x, y in zip(m[i], m[j])]
    return [row[-1] for row in m]


def rows_with_box(c, b):
    n = len(c[0])
    rows = [list(row) for row in c]
    rhs = list(b)
    for i in range(n):
        for sign, val in [(1, 1), (-1, 0)]:
            rows.append([F(sign if j == i else 0) for j in range(n)])
            rhs.append(F(val))
    return rows, rhs


def primal_feasible(c, b):
    rows, rhs = rows_with_box(c, b)
    n = len(c[0])
    for inds in combinations(range(len(rows)), n):
        z = solve([rows[i] for i in inds], [rhs[i] for i in inds])
        if z is not None and all(dot(row, z) <= v for row, v in zip(rows, rhs)):
            return True
    return False


def ray_feasible(c, b):
    # For k=2 every candidate ray is perpendicular to a column or axis.
    rays = [(F(1), F(0)), (F(0), F(1))]
    for column in zip(*c):
        for sign in [-1, 1]:
            ray = (sign * column[1], -sign * column[0])
            if any(ray) and all(v >= 0 for v in ray):
                rays.append(ray)
    return all(dot(ray, b) >= sum(min(F(0), dot(ray, col)) for col in zip(*c))
               for ray in rays)


def quadratic_optimum(c, b, ell):
    # Enumerate independent active KKT systems for F(z)=||z||^2/2-ell.z.
    rows, rhs = rows_with_box(c, b)
    n = len(ell)
    for size in range(n + 1):
        for inds in combinations(range(len(rows)), size):
            active = [rows[i] for i in inds]
            gram = [[dot(a, a2) for a2 in active] for a in active]
            multipliers = solve(gram, [dot(rows[i], ell) - rhs[i] for i in inds])
            if multipliers is None or any(v < 0 for v in multipliers):
                continue
            z = [ell[j] - sum(m * a[j] for m, a in zip(multipliers, active))
                 for j in range(n)]
            if all(dot(row, z) <= v for row, v in zip(rows, rhs)):
                return z
    return None


def objective(z, ell):
    return dot(z, z) / 2 - dot(z, ell)


def main():
    rng = Random(473918)
    support_checks = residual_checks = bregman_checks = 0
    # Signed and zero columns, rank deficiency, repeated/opposite rows,
    # and boundary feasibility are present in this deterministic family.
    matrices = [
        [[F(0)] * 3, [F(0)] * 3],
        [[F(1), F(-1), F(0)], [F(-1), F(1), F(0)]],
        [[F(1), F(1), F(1)], [F(2), F(2), F(2)]],
    ]
    matrices += [[[F(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(3)]
                  for _ in range(2)] for _ in range(29)]
    for c in matrices:
        for b in product([F(-1), F(0), F(1, 2), F(2)], repeat=2):
            assert primal_feasible(c, b) == ray_feasible(c, b)
            support_checks += 1
        # Generate a feasible RHS, including exact boundary constraints.
        seed = [F(rng.randint(0, 4), 4) for _ in range(3)]
        b = [dot(row, seed) + F(rng.randint(0, 1), 2) for row in c]
        ell = [F(rng.randint(-4, 8), 4) for _ in range(3)]
        optimum = quadratic_optimum(c, b, ell)
        assert optimum is not None
        for lam in product([F(0), F(1, 3), F(2)], repeat=2):
            q = [min(F(1), max(F(0), ell[i] - dot(lam, col)))
                 for i, col in enumerate(zip(*c))]
            residual = [dot(row, q) - val for row, val in zip(c, b)]
            # Exact Euclidean projection is another identity-Hessian QP.
            repaired = quadratic_optimum(c, b, q)
            assert repaired is not None
            gap = objective(repaired, ell) - objective(optimum, ell)
            lipschitz = sum(max(abs(v), abs(F(1) - v)) for v in ell)
            distance = max(abs(a - z) for a, z in zip(repaired, q))
            zeta = abs(dot(lam, residual))
            assert gap >= 0
            assert gap <= lipschitz * distance + zeta
            assert gap >= max(abs(a - z) for a, z in zip(repaired, optimum)) ** 2 / 2
            # Check the weak-dual inequality before feasibility repair.
            assert objective(q, ell) + dot(lam, residual) <= objective(optimum, ell)
            residual_checks += 1
    grid = [F(i, 12) for i in range(13)]
    for degree in range(1, 33):
        for u, v in product(grid, repeat=2):
            divergence = (u ** (degree + 1) - v ** (degree + 1)) / (degree + 1)
            divergence -= v ** degree * (u - v)
            assert divergence >= abs(u - v) ** (degree + 1) / (degree + 1)
            bregman_checks += 1
    signed_checks = 0
    for degree in [1, 3, 5, 9, 17]:
        for center in [F(0), F(1, 3), F(1, 2), F(1)]:
            # Odd translated powers are strictly increasing; for degree>1
            # the derivative vanishes at center, including interior centers.
            scale = (1 - center) ** degree - (-center) ** degree
            coeff = [F(comb(degree, j)) * (-center) ** (degree - j) / scale
                     for j in range(degree + 1)]
            coeff[0] = F(0)
            def marginal(z):
                return sum(a * z ** j for j, a in enumerate(coeff))
            def integral(z):
                return sum(a * z ** (j + 1) / (j + 1) for j, a in enumerate(coeff))
            for u, v in product(grid, repeat=2):
                distance = abs(u - v)
                increment = abs(marginal(u) - marginal(v))
                assert increment >= (distance / (2 * degree)) ** degree / 2
                divergence = integral(u) - integral(v) - marginal(v) * (u - v)
                assert divergence >= distance ** (degree + 1) / (4 * (4 * degree) ** degree)
                signed_checks += 1
    print(f"PASS: {support_checks} exact projection/ray comparisons, "
          f"{residual_checks} exact approximate-dual/repair cases, "
          f"{bregman_checks} directed power-Bregman inequalities, "
          f"{signed_checks} signed-polynomial modulus/Bregman cases")


if __name__ == "__main__":
    main()
