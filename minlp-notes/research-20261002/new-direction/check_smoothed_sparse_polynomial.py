#!/usr/bin/env python3
"""Exact targeted quartic checks; no probabilistic or performance claim."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from check_sparse_bag_cells import (
    brute_grid, contains, corners, physical_member, refine_cell, round_laws,
    sparse_tree_dp,
)


class Quartic:
    bounds = [(Q(0), Q(1)), (Q(0), Q(1, 4)), (Q(0), Q(1))]
    bags = [(0, 1), (1, 2)]
    edges = [(0, 1)]
    integers = frozenset({2})

    @staticmethod
    def local(bag, row):
        if bag == 0:
            x, y = row
            u = x-Q(1, 3)
            return u*u+u**4+2*y-y*y+u*y
        y, z = row
        return (z-1)**2+y*(z-1)

    def value(self, point):
        return sum(self.local(t, tuple(point[i] for i in bag))
                   for t, bag in enumerate(self.bags))


def tables(instance, cells):
    rows = [sorted({tuple(row) for cell in whitelist for row in corners(cell)})
            for whitelist in cells]
    costs = [{row: instance.local(t, row) for row in table}
             for t, table in enumerate(rows)]
    return rows, costs


def coordinate_hull(instance, cells):
    hull = []
    for i in range(len(instance.bounds)):
        projections = []
        for bag, whitelist in zip(instance.bags, cells):
            if i in bag:
                intervals = [cell[bag.index(i)] for cell in whitelist]
                projections.append((min(a for a, _ in intervals), max(b for _, b in intervals)))
        hull.append((max(a for a, _ in projections), min(b for _, b in projections)))
    return hull


def main():
    instance = Quartic()
    optimum = (Q(1, 3), Q(0), Q(1))
    assert instance.value(optimum) == 0
    # Analytic growth proof: |u y| <= u²/4+y² and
    # |(z-1)y| <= (z-1)²/4+y², while 2y-3y² >= 3y²/4.
    # H_xx <= 22/3, H_yy=-2, H_zz=2; take L=8, M1=9, T=16.
    L, M1, T, g0 = Q(8), Q(9), Q(16), Q(1, 2)
    cells = [[tuple(instance.bounds[i] for i in bag)] for bag in instance.bags]
    upper = None
    counts = {name: 0 for name in ['min_marginals', 'rounding_atoms', 'retained_witnesses',
                                   'removed_cells', 'growth_points', 'pd_patches']}
    records = []
    closure_stage = None
    for stage in range(9):
        h = Q(1, 2**stage)
        rows, costs = tables(instance, cells)
        grid_min, witness, marginals, _ = sparse_tree_dp(instance, rows, costs)
        exact, brute_marginals, brute_witnesses, feasible, _ = brute_grid(instance, rows, costs)
        assert exact == grid_min and brute_marginals == marginals
        counts['min_marginals'] += sum(map(len, marginals))
        upper = grid_min if upper is None else min(upper, grid_min)
        error = 3*L*h*h/8
        assert 0 <= upper <= grid_min <= error
        kept = [[] for _ in cells]
        for t, whitelist in enumerate(cells):
            for cell in whitelist:
                values = [(marginals[t][tuple(row)], tuple(row))
                          for row in corners(cell) if tuple(row) in marginals[t]]
                if not values:
                    counts['removed_cells'] += 1
                    continue
                value, row = min(values)
                if value-error <= upper:
                    kept[t].append(cell)
                    assert value <= 2*error
                    full_witness = brute_witnesses[t][row]
                    assert instance.value(full_witness) == value and contains(cell, row)
                    counts['retained_witnesses'] += 1
                else:
                    counts['removed_cells'] += 1
        assert physical_member(instance, kept, optimum)
        # Rounding of the off-grid optimizer uses the allowed whitelist.
        expectation = Q(0)
        for choices in product(*round_laws(instance, optimum, h)):
            point = tuple(v for v, _ in choices)
            weight = Q(1)
            for _, probability in choices:
                weight *= probability
            assert physical_member(instance, cells, point)
            expectation += weight*instance.value(point)
            counts['rounding_atoms'] += 1
        assert expectation <= error
        # Independent sampled checks of growth, including integer labels.
        for point in feasible[::max(1, len(feasible)//50)]:
            norm2 = sum((x-a)**2 for x, a in zip(point, optimum))
            assert instance.value(point) >= Q(3, 4)*norm2
            counts['growth_points'] += 1
        hull = coordinate_hull(instance, kept)
        midpoint = [(a+b)/2 for a, b in hull]
        radius = max((b-a)/2 for a, b in hull)
        y_gradient = 2-2*midpoint[1]+midpoint[0]-Q(1, 3)+midpoint[2]-1
        integer_fixed = hull[2] == (Q(1), Q(1))
        active_fixed = integer_fixed and y_gradient-M1*radius > 0
        pd_margin = None
        if active_fixed:
            c = midpoint[0]
            r = (hull[0][1]-hull[0][0])/2
            pd_margin = 2+12*(c-Q(1, 3))**2-T*r-g0
            if pd_margin > 0:
                counts['pd_patches'] += 1
                closure_stage = stage
                # Full continuous Hessian is indefinite everywhere:
                # its y diagonal is -2. Active elimination is essential.
                assert Q(-2) < 0
                for x in [hull[0][0], c, hull[0][1]]:
                    assert 2+12*(x-Q(1, 3))**2 >= g0
        records.append({'stage': stage, 'h': str(h), 'rows': sum(map(len, rows)),
                        'retained_cells': sum(map(len, kept)),
                        'integer_fixed': integer_fixed, 'active_fixed': active_fixed,
                        'pd_margin': None if pd_margin is None else str(pd_margin)})
        if closure_stage is not None:
            break
        cells = [[child for cell in whitelist for child in refine_cell(
            cell, h, tuple(k for k, i in enumerate(bag) if i in instance.integers))]
                 for bag, whitelist in zip(instance.bags, kept)]
    assert closure_stage is not None

    # Explicit mixed quartic term: sequential semiconcavity must work even
    # though independent rounding no longer cancels the cross-term error.
    cross_cases = 0
    for left in [Q(0), Q(1, 4), Q(1, 2)]:
        for width in [Q(1, 8), Q(1, 4)]:
            for fractions in product([Q(1, 3), Q(1, 2), Q(2, 3)], repeat=2):
                point = tuple(left+width*t for t in fractions)
                expected = Q(0)
                for bits in product([0, 1], repeat=2):
                    atom = tuple(left+width*b for b in bits)
                    probability = Q(1)
                    for b, t in zip(bits, fractions):
                        probability *= t if b else 1-t
                    expected += probability*atom[0]**2*atom[1]**2
                # On [0,1]^2 both diagonal second derivatives <=2.
                assert expected <= point[0]**2*point[1]**2+width**2/2
                cross_cases += 1
    report = {'status': 'passed', 'scope': 'finite exact quartic checks only',
              'stages': len(records), 'closure_stage': closure_stage,
              'quartic_cross_rounding_cases': cross_cases, 'counts': counts, 'records': records}
    Path(__file__).with_name('smoothed-sparse-polynomial-check-results.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}))


if __name__ == '__main__':
    main()
