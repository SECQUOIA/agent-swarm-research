#!/usr/bin/env python3
"""Exact finite checks for atomic moment tails and discrepancy endpoints.

These checks do not implement CAD, geometric coarea, or either recursive DP.
They enumerate noise outcomes and compare rational probabilities directly.
"""

from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import comb, factorial


def vc_dimension(labels, m):
    return max(len(coords)
               for r in range(m + 1)
               for coords in combinations(range(m), r)
               if len({tuple(z[i] for i in coords) for z in labels}) == 2 ** r)


def check_atomic_moments():
    outcomes = moment_bounds = vc_bounds = rank_bounds = informative = 0
    rank_nontrivial = rank_nonzero = 0
    for m, ngrid in ((1, 16), (2, 16), (3, 8)):
        cube = tuple(product((0, 1), repeat=m))
        families = [s for r in range(1, len(cube) + 1)
                    for s in combinations(cube, r)] if m <= 2 else [
                        cube, cube[:3], cube[1:6], cube[::2], cube[1::2]]
        grid = tuple(F(-1) + F(2 * j, ngrid - 1) for j in range(ngrid))
        for family in families:
            for kind in range(2):
                offset = {z: (F(sum(z)) if kind == 0 else
                              F(sum((i + 1) * z[i] for i in range(m))
                                - 3 * z[0] * z[-1], 7)) for z in family}
                for tolerance in (F(0), F(1, 100)):
                    moment_sum = {p: 0 for p in (1, 2, 3)}
                    vc_events = {r: 0 for r in range(1, m + 1)}
                    rank_events = {r: 0 for r in range(1, m + 1)}
                    for xi in product(grid, repeat=m):
                        costs = {z: offset[z] + sum(x * a for x, a in zip(xi, z))
                                 for z in family}
                        minimum = min(costs.values())
                        labels = [z for z in family if costs[z] <= minimum + tolerance]
                        size, dim = len(labels), vc_dimension(labels, m)
                        for p in moment_sum:
                            moment_sum[p] += size ** p
                        for r in vc_events:
                            vc_events[r] += dim >= r
                            rank_events[r] += size >= 2 ** (r - 1) + 1
                        outcomes += 1
                    for p, total in moment_sum.items():
                        bound = (1 + (m + 1) ** p * (tolerance + F(1, ngrid))) ** m
                        assert F(total, ngrid ** m) <= bound
                        informative += bound < len(family) ** p
                        moment_bounds += 1
                    for r in vc_events:
                        bound = comb(m, r) * (tolerance + F(1, ngrid)) ** r
                        assert F(vc_events[r], ngrid ** m) <= bound
                        vc_bounds += 1
                        rank_bound = (comb(m, r) * 2 ** (r * (r + 1))
                                      * (factorial(r) * tolerance + F(1, ngrid)) ** r)
                        assert F(rank_events[r], ngrid ** m) <= rank_bound
                        rank_bounds += 1
                        rank_nontrivial += rank_bound < 1
                        rank_nonzero += rank_bound < 1 and rank_events[r] > 0
    assert informative > 0
    return (outcomes, moment_bounds, vc_bounds, rank_bounds, informative,
            rank_nontrivial, rank_nonzero)


def check_discrepancy():
    half_lines = intervals = 0
    for ngrid in range(2, 33):
        grid = tuple(F(j, ngrid - 1) for j in range(ngrid))
        thresholds = sorted(set(grid + tuple((a + b) / 2
                                            for a, b in zip(grid, grid[1:]))
                                + (F(-1), F(2))))

        def continuous_cdf(t):
            return max(F(0), min(F(1), t))

        for t in thresholds:
            for closed in (False, True):
                discrete = F(sum(x <= t if closed else x < t for x in grid), ngrid)
                assert abs(discrete - continuous_cdf(t)) <= F(1, ngrid)
                half_lines += 1
        # Distinct endpoints and singletons, with all four endpoint conventions.
        for a, b in combinations_with_replacement(thresholds, 2):
            for left, right in product((False, True), repeat=2):
                mass = F(sum((x >= a if left else x > a)
                             and (x <= b if right else x < b) for x in grid), ngrid)
                length = continuous_cdf(b) - continuous_cdf(a)
                assert abs(mass - length) <= F(2, ngrid)
                intervals += 1
    return half_lines, intervals


if __name__ == '__main__':
    (outcomes, moments, vc, rank, informative,
     rank_nontrivial, rank_nonzero) = check_atomic_moments()
    half_lines, intervals = check_discrepancy()
    print(f'PASS: {moments} atomic moment bounds ({informative} below the trivial '
          f'cardinality bound); {vc} VC tails; {rank} affine-rank tails '
          f'({rank_nontrivial} with bound < 1; {rank_nonzero} of these have '
          f'nonzero event probability); {outcomes} exact noise outcomes')
    print(f'PASS: {half_lines} open/closed half-line and {intervals} interval '
          'discrepancy comparisons')
