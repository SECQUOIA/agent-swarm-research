"""Exact, small-fixture diagnostics for convex-cubic-polytope-point-oracle.md.

Run: python3 -B research-20261002/new-direction/check_convex_cubic_polytope.py
This is not a general LP, projection, or convex optimization implementation.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product


COUNTS = Counter()


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def rank(rows, n):
    a = [list(map(F, row)) for row in rows]
    pivot = 0
    for j in range(n):
        k = next((k for k in range(pivot, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        scale = a[pivot][j]
        a[pivot] = [v / scale for v in a[pivot]]
        for k in range(pivot + 1, len(a)):
            scale = a[k][j]
            a[k] = [v - scale * w for v, w in zip(a[k], a[pivot])]
        pivot += 1
    return pivot


def solve(a, b):
    """Square nonsingular rational systems only; None means singular."""
    n = len(b)
    rows = [list(map(F, row)) + [F(rhs)] for row, rhs in zip(a, b)]
    for j in range(n):
        k = next((k for k in range(j, n) if rows[k][j]), None)
        if k is None:
            return None
        rows[j], rows[k] = rows[k], rows[j]
        scale = rows[j][j]
        rows[j] = [v / scale for v in rows[j]]
        for k in range(n):
            if k != j:
                scale = rows[k][j]
                rows[k] = [v - scale * w for v, w in zip(rows[k], rows[j])]
    return tuple(row[-1] for row in rows)


def feasible(x, rows, rhs):
    return all(dot(a, x) <= b for a, b in zip(rows, rhs))


def vertices(rows, rhs, n):
    """Enumerate bases of the bounded fixtures, including degenerate ones."""
    result = set()
    for ids in combinations(range(len(rows)), n):
        x = solve([rows[i] for i in ids], [rhs[i] for i in ids])
        if x is not None and feasible(x, rows, rhs):
            result.add(x)
    return sorted(result)


TRIANGLE = [(1, 0), (0, 1), (-1, -1)]
RHS = [1, 1, 0]
CENTER = (F(1, 2), F(1, 2))
RHO = F(1, 2)
RADIUS = F(3)


def hull_checks():
    fixtures = [
        # name, rows, rhs, dimension, universal row indices, affine rank
        ("triangle", TRIANGLE, RHS, 2, set(), 0),
        ("implied singleton", [(-1, 0), (0, -1), (1, 1)],
         [0, 0, 0], 2, {0, 1, 2}, 2),
        ("redundant tight rows", [(-1, 0), (0, -1), (1, 1), (2, 2),
                                  (0, 0), (0, 0)],
         [0, 0, 0, 0, 0, 1], 2, {0, 1, 2, 3, 4}, 2),
        ("implied line", [(-1, 0, 0), (0, -1, 0), (1, 1, 0),
                           (0, 0, -1), (0, 0, 1), (2, 2, 0)],
         [0, 0, 0, 0, 1, 0], 3, {0, 1, 2, 5}, 2),
        ("shifted singleton", [(1,), (-1,), (2,), (0,)],
         [F(1, 3), F(-1, 3), F(2, 3), 2], 1, {0, 1, 2}, 1),
        ("zero-dimensional", [(), ()], [0, 1], 0, {0}, 0),
    ]
    for name, rows, rhs, n, expected, expected_rank in fixtures:
        verts = vertices(rows, rhs, n)
        assert verts, name
        tight = {i for i, (a, b) in enumerate(zip(rows, rhs))
                 if max(F(b) - dot(a, x) for x in verts) == 0}
        assert tight == expected, name
        assert rank([rows[i] for i in tight], n) == expected_rank
        assert rank([sub(x, verts[0]) for x in verts], n) == n - expected_rank
        average = tuple(sum(x[j] for x in verts) / len(verts) for j in range(n))
        for i, (a, b) in enumerate(zip(rows, rhs)):
            assert (dot(a, average) == b) == (i in tight)
            COUNTS["universal-row classifications"] += 1
        COUNTS["affine-hull fixtures"] += 1
    assert not vertices([()], [-1], 0)
    COUNTS["infeasible zero-row guards"] += 1
    # Every triangle row is active somewhere; none is universally tight.
    assert all(any(dot(a, v) == b for v in vertices(TRIANGLE, RHS, 2))
               for a, b in zip(TRIANGLE, RHS))
    COUNTS["active-versus-universal guards"] += 1


def triangle_checks():
    verts = vertices(TRIANGLE, RHS, 2)
    assert set(verts) == {(F(1), F(1)), (F(1), F(-1)), (F(-1), F(1))}
    lp_rows = [tuple(a) + (sum(map(abs, a)),) for a in TRIANGLE]
    lp_rows += [(0, 0, -1), (0, 0, 1)]
    lp_rhs = RHS + [0, 1]
    lp_verts = vertices(lp_rows, lp_rhs, 3)
    assert max(x[2] for x in lp_verts) == RHO
    assert CENTER + (RHO,) in lp_verts
    assert all((F(b) - dot(a, CENTER)) ** 2 >= RHO**2 * norm2(a)
               for a, b in zip(TRIANGLE, RHS))
    lo = tuple(min(v[j] for v in verts) for j in range(2))
    hi = tuple(max(v[j] for v in verts) for j in range(2))
    assert lo == (-1, -1) and hi == (1, 1)
    assert max(1, sum(max(abs(lo[j] - CENTER[j]), abs(hi[j] - CENTER[j]))
                      for j in range(2))) == RADIUS
    COUNTS["inball LP vertices"] += len(lp_verts)
    beta = 1 + RADIUS / RHO
    points = [x for x in product([F(i, 4) for i in range(-4, 5)], repeat=2)
              if feasible(x, TRIANGLE, RHS)]
    for x in points:
        reflected = tuple(c - RHO / RADIUS * (u - c) for u, c in zip(x, CENTER))
        assert norm2(sub(x, CENTER)) <= RADIUS**2
        assert norm2(sub(reflected, CENTER)) <= RHO**2
        assert feasible(reflected, TRIANGLE, RHS)
        # H(x)=6(x+y) 11': scalar checks certify the entire PSD ordering.
        hx, hc, hr = 6 * sum(x), 6 * sum(CENTER), 6 * sum(reflected)
        assert 0 <= hx <= beta * hc
        assert hc == (RHO * hx + RADIUS * hr) / (RHO + RADIUS)
        COUNTS["reflection and Hessian-domination points"] += 1
    # The coordinate bounding box includes (-1,-1), where H has a negative ray.
    assert 6 * sum(lo) * (1 + 1)**2 < 0
    COUNTS["convex-on-polytope-only guards"] += 1
    return points


def repair_checks(points):
    for bar in points:
        for step in (F(1, 100), F(1, 4), F(2)):
            for direction in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)):
                offset = tuple(step * d for d in direction)
                delta = sum(map(abs, offset))
                u = tuple(a + d for a, d in zip(bar, offset))
                repaired = tuple((RHO * a + delta * c) / (RHO + delta)
                                 for a, c in zip(u, CENTER))
                assert norm2(offset) <= delta**2
                assert feasible(repaired, TRIANGLE, RHS)
                assert norm2(sub(repaired, bar)) <= (delta * (1 + RADIUS / RHO))**2
                # |partial_j (x+y)^3| <=12 on the bounding box. The L1 bound
                # avoids irrational Euclidean Lipschitz constants.
                assert abs(sum(repaired)**3 - sum(bar)**3) <= 12 * sum(map(abs, sub(repaired, bar)))
                COUNTS["exact homothety and objective-repair checks"] += 1
    outside = (F(-1), F(0))
    clipped = tuple(min(F(1), max(F(-1), v)) for v in outside)
    assert clipped == outside and not feasible(clipped, TRIANGLE, RHS)
    assert norm2(sub(outside, (F(-1, 2), F(1, 2)))) == F(1, 2)
    COUNTS["coordinate-clipping failure guards"] += 1


def slice_distance2(u, a, t):
    candidates = []
    for row, b in zip(TRIANGLE, RHS):
        x = solve([a, row], [t, b])
        if x is not None and feasible(x, TRIANGLE, RHS):
            candidates.append(x)
    candidates = sorted(set(candidates))
    assert candidates
    left, right = candidates[0], candidates[-1]
    direction = sub(right, left)
    if not norm2(direction):
        return norm2(sub(u, left)), True
    alpha = dot(sub(u, left), direction) / norm2(direction)
    clipped = min(F(1), max(F(0), alpha))
    projection = tuple(x + clipped * d for x, d in zip(left, direction))
    assert feasible(projection, TRIANGLE, RHS) and dot(a, projection) == t
    return norm2(sub(u, projection)), clipped in (0, 1)


def hoffman_checks(points):
    for a, targets in [((1, 1), [F(0), F(1, 3), F(1), F(2)]),
                       ((2, -1), [F(-3), F(-1, 2), F(1), F(3)]),
                       ((3, 2), [F(-1), F(0), F(7, 3), F(5)])]:
        for t in targets:
            for u in points:
                distance2, boundary = slice_distance2(u, a, t)
                for redundant in (False, True):
                    # A consists of a, or a and 2a. B is the integer triangle.
                    cstar = max(1, max(map(abs, a)) * (2 if redundant else 1))
                    residual2 = (dot(a, u) - t)**2 * (5 if redundant else 1)
                    assert distance2 <= (2 * cstar)**2 * residual2
                    COUNTS["general-row Hoffman bounds"] += 1
                COUNTS["Hoffman endpoint projections"] += int(boundary)


def original_norm_checks():
    def embed(u):
        return (-1 + 2*u[0] + u[1], u[0], u[1])

    optimum = (F(1, 3), F(1, 6))
    parameter_minimum = (F(0), F(0))
    assert norm2(embed(optimum)) == F(1, 6)
    assert norm2(embed(parameter_minimum)) == 1
    assert norm2(parameter_minimum) < norm2(optimum)
    # V'V=[[5,2],[2,2]] is positive definite; its stationary point is feasible.
    gram = [[5, 2], [2, 2]]
    assert solve(gram, [2, 1]) == optimum and 5*2 - 2*2 > 0
    for u in product([F(i, 12) for i in range(13)], repeat=2):
        if sum(u) > 1:
            continue
        d = sub(u, optimum)
        squared = dot(d, tuple(dot(row, d) for row in gram))
        assert norm2(embed(u)) - F(1, 6) == squared >= 0
        # W=sum|V_ij|=5 transports reduced distances to original ones.
        assert norm2(sub(embed(u), embed(optimum))) <= 25 * norm2(d)
        COUNTS["nonorthogonal original-norm checks"] += 1
    COUNTS["parameter-norm failure guards"] += 1


if __name__ == "__main__":
    hull_checks()
    triangle_points = triangle_checks()
    repair_checks(triangle_points)
    hoffman_checks(triangle_points)
    original_norm_checks()
    print("PASS")
    for name, count in COUNTS.items():
        print(f"  {count} {name}")
    print("Scope: rational bounded fixtures, enumerated small LP bases, explicit")
    print("line-slice projections and explicit optimizer sets; no general solver,")
    print("convexity recognition, cubic-identity duplication, or project-wide checks.")
