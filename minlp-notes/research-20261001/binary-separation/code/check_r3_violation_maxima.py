"""Exact checks of R3-m1 and the even-set convention in R3-o2.

Build the cut distances directly from Corollaries 1 and 10. Enumerate all
hypermetric violators with the existing exact ellipsoid routine, all odd
clique vectors by brute force, and all clique subsets at the switched point.
Only the linear algebra and ellipsoid enumeration are shared with the main
check script; the distances and inequality evaluations are computed here.
"""

from fractions import Fraction as F
from itertools import combinations, product

from check_binary_separation import ellipsoid_points, ldl_rev, quad, solve


def distances(q, sets):
    n, p, m = len(sets), 3 * q, q - 2
    N = 8 * n + 2 * p + 1
    g, nodes = n + 1, n + m + 2
    scale = 8 * q * N
    # Integer edge values of scale * epsilon * d~ (epsilon = 1/N).
    d = {}
    for i, S in enumerate(sets, 1):
        d[0, i] = 8 * q * (4 + len(S))
        d[i, g] = 2 * q * (2 * p + 15)
        for j in range(i + 1, n + 1):
            d[i, j] = 8 * q * (8 + len(S ^ sets[j - 1]))
    d[0, g] = 2 * q * (2 * p - 1)
    for o in range(g + 1, nodes):
        d[0, o] = 1
        for u in range(1, g + 1):
            d[u, o] = d[0, u] + 1
        for v in range(o + 1, nodes):
            d[o, v] = 2
    U = set(range(g, nodes))
    switched = {e: scale - v if ((e[0] in U) != (e[1] in U)) else v
                for e, v in d.items()}
    return N, scale, nodes, U, d, switched


def Q(b, d):
    return sum(b[i] * b[j] * v for (i, j), v in d.items())


def check_instance(label, q, sets):
    n, p, m = len(sets), 3 * q, q - 2
    covers = [C for C in combinations(range(n), q)
              if set().union(*(sets[i] for i in C)) == set(range(p))]
    N, scale, nodes, U, d, switched = distances(q, sets)
    # Recover the correlation matrix from the cut distances, without using
    # the note's formula for the violating vectors to restrict the search.
    M = [[F(d[0, i], scale) if i == j else
          F(d[0, i] + d[0, j] - d[min(i, j), max(i, j)], 2 * scale)
          for j in range(1, nodes)] for i in range(1, nodes)]
    assert ldl_rev(M) is not None
    center = solve(M, [M[i][i] / 2 for i in range(nodes - 1)])
    hyp = {}
    for z in ellipsoid_points(M, center, quad(M, center)):
        b = (1 - sum(z),) + z
        value = Q(b, d)
        assert value > 0
        hyp[b] = value

    # Exhaust all {0,+-1} vectors, including odd sums other than +-1.
    odd, pure = {}, {}
    for b in product((-1, 0, 1), repeat=nodes):
        sigma = sum(b)
        if sigma % 2 == 0:
            continue
        violation = Q(b, d) - scale * (sigma * sigma - 1) // 4
        if violation > 0:
            odd[b] = violation
            if sigma == 1:
                pure[b] = violation
    assert odd == {**pure, **{tuple(-a for a in b): v for b, v in pure.items()}}
    assert pure == {b: v for b, v in hyp.items() if all(abs(a) <= 1 for a in b)}

    expected_pure, expected_max_pure, expected_max_hyp = set(), set(), set()
    for C in covers:
        base = tuple(int(i in C) for i in range(n)) + (-1,)
        bstar = (0,) + base + (-1,) * m
        assert Q(bstar, d) == 2 * (q + 2)
        expected_pure.add(bstar)
        for j in range(m):
            w = tuple(0 if i == j else -1 for i in range(m))
            b = (-1,) + base + w
            assert Q(b, d) == 2 * (q + 3)
            expected_pure.add(b)
            expected_max_pure.add(b)
        for w in product((0, 1), repeat=m):
            expected_max_hyp.add((2 - q - sum(w),) + base + w)
    assert set(pure) == expected_pure
    assert {b for b, v in pure.items() if v == max(pure.values(), default=0)} == expected_max_pure
    assert {b for b, v in hyp.items() if v == max(hyp.values(), default=0)} == expected_max_hyp

    # Exhaust all subsets under both the odd-only and all-subsets conventions.
    clique, even_count = {}, 0
    for r in range(1, nodes + 1):
        for S in combinations(range(nodes), r):
            b = tuple(int(i in S) for i in range(nodes))
            violation = Q(b, switched) - scale * (r * r // 4)
            if r % 2 == 0:
                even_count += 1
                assert violation < 0  # Nonempty even members are psd inequalities.
            elif violation > 0:
                clique[frozenset(S)] = violation
    assert set(clique) == {frozenset({i + 1 for i in C} | U) for C in covers}
    assert bool(hyp) == bool(odd) == bool(clique) == bool(covers)
    maxima = (max(clique.values(), default=0), max(odd.values(), default=0),
              max(hyp.values(), default=0))
    assert maxima == ((2 * (q + 2), 2 * (q + 3), 4 * q) if covers else (0, 0, 0))
    values = tuple(F(v, scale) for v in maxima)
    print(f"{label}: q={q}, n={n}, p={p}, N={N}, covers={covers}")
    print(f"  max (18) at d''={values[0]}; max odd clique / pure at eps*d~={values[1]}; "
          f"max hypermetric at eps*d~={values[2]}")
    print(f"  all hypermetric violators={len(hyp)}; pure={len(pure)}; "
          f"maximizing pure={len(expected_max_pure)}; even nonempty subsets strictly satisfied={even_count}")


def main():
    print("R3 exact violation checks: Fraction arithmetic; complete hypermetric ellipsoid enumeration;")
    print("all {0,+-1} odd clique vectors; all switched clique subsets, including even sizes.")
    for q in (3, 4, 5):
        partition = [frozenset(range(3 * i, 3 * i + 3)) for i in range(q)]
        check_instance("partition cover", q, partition)
        missing = partition[:-1] + [frozenset({0, 3 * q - 3, 3 * q - 2})]
        check_instance("missing last element (no cover)", q, missing)
    check_instance("two covers", 3, [frozenset(S) for S in
                   ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                    (0, 3, 6), (1, 4, 7), (2, 5, 8))])
    print("7 instances (4 yes, 3 no); q in {3,4,5}; ALL R3 VIOLATION CHECKS PASSED")


if __name__ == "__main__":
    main()
