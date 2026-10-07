#!/usr/bin/env python3
"""Exact finite diagnostics of cubic charts and certified approximate DP.

Rational brackets certify every algebraic row value. The sparse DP is
checked against exhaustive rational lower-cost min-marginals. These small
fixtures do not test a smoothed expectation or prove a complexity bound.
"""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from check_sparse_bag_cells import (
    brute_grid, contains, corners, physical_member, refine_cell, round_laws,
    sparse_tree_dp,
)


def square_interval(lo, hi):
    assert lo <= hi
    return (Q(0) if lo <= 0 <= hi else min(lo*lo, hi*hi),
            max(lo*lo, hi*hi))


def root_bracket(rhs, width):
    """Unique root of u+u^3=rhs in [-2,2], with exact sign witnesses."""
    lo, hi = Q(-2), Q(2)
    assert lo+lo**3 <= rhs <= hi+hi**3 and width > 0
    while hi-lo > width:
        mid = (lo+hi)/2
        value = mid+mid**3-rhs
        if value == 0:
            lo = hi = mid
            break
        if value < 0:
            lo = mid
        else:
            hi = mid
    assert lo+lo**3 <= rhs <= hi+hi**3
    return lo, hi


class CubicDynamics:
    # s0=0; retained coordinates are (s1,s2,z0,z1).
    bounds = [(Q(-1), Q(1)), (Q(-1), Q(1)), (Q(0), Q(1)), (Q(0), Q(1))]
    bags = [(0, 2), (0, 1, 3)]
    edges = [(0, 1)]
    integers = frozenset({2, 3})
    optimum = (Q(5, 8), Q(-15, 32), Q(0), Q(0))

    def __init__(self):
        self.costs = None
        self.brackets = 0
        self.nonpoint_brackets = 0
        self.max_denominator_bits = 0

    @staticmethod
    def parameters(bag, row):
        if bag == 0:
            x, z = row
            return x-z/2, Q(1, 2), (x-Q(5, 8))**2+z*z
        x, v, z = row
        return v-x/4-z/2, Q(-1, 2), (v+Q(15, 32))**2+z*z

    def enclosure(self, bag, row, delta, eta=Q(0)):
        rhs, center, exact = self.parameters(bag, row)
        # On [-2,2], derivative of (u-center)^2+eta*u has
        # absolute value at most 5+|eta|. The separate interval terms
        # below obey this same width bound.
        lo, hi = root_bracket(rhs, delta/(5+abs(eta)))
        low, high = square_interval(lo-center, hi-center)
        low += exact+min(eta*lo, eta*hi)
        high += exact+max(eta*lo, eta*hi)
        assert 0 <= high-low <= delta
        self.brackets += 1
        self.nonpoint_brackets += lo != hi
        self.max_denominator_bits = max(
            self.max_denominator_bits,
            *(x.denominator.bit_length() for x in [lo, hi, low, high]))
        return low, high, (lo, hi)

    def value(self, point):
        # This interface is used only by the rational lower-cost DP.
        assert self.costs is not None
        return sum(self.costs[t][tuple(point[i] for i in bag)]
                   for t, bag in enumerate(self.bags))

    def point_enclosure(self, point, delta):
        intervals = [self.enclosure(t, tuple(point[i] for i in bag), delta)
                     for t, bag in enumerate(self.bags)]
        return sum(x[0] for x in intervals), sum(x[1] for x in intervals)


def coordinate_hull(instance, cells):
    result = []
    for i in range(len(instance.bounds)):
        projections = []
        for bag, whitelist in zip(instance.bags, cells):
            if i in bag:
                intervals = [cell[bag.index(i)] for cell in whitelist]
                projections.append((min(a for a, _ in intervals),
                                    max(b for _, b in intervals)))
        result.append((max(a for a, _ in projections),
                       min(b for _, b in projections)))
    return result


def reduced_curvature_lower(root_interval, center):
    """Numerator lower bound for d²[(psi(r)-center)^2]/dr².

    The denominator (1+3u²)^3 is positive. A nonnegative numerator
    therefore certifies nonnegative curvature throughout this interval.
    """
    lo, hi = root_interval
    _, square_hi = square_interval(lo, hi)
    return 2-6*square_hi+min(12*center*lo, 12*center*hi)


def main():
    instance = CubicDynamics()
    # The zero objective is achieved at the displayed point with controls
    # (1/2,-1/2); the sum of retained squares proves point growth g>=1.
    for bag, coordinates in enumerate(instance.bags):
        row = tuple(instance.optimum[i] for i in coordinates)
        rhs, center, exact = instance.parameters(bag, row)
        assert center+center**3 == rhs and exact == 0

    # Full-real-hull brackets include fractional native-integer coordinates.
    real_hull_cases = 0
    for previous, following, mode in product(
            [Q(-1), Q(-1, 3), Q(1)],
            [Q(-1), Q(1, 5), Q(1)], [Q(0), Q(1, 2), Q(1)]):
        rhs = following-previous/4-mode/2
        assert -10 <= rhs <= 10
        for precision in [4, 13, 31]:
            lo, hi = root_bracket(rhs, Q(1, 2**precision))
            assert hi-lo <= Q(1, 2**precision)
            # q_u=1+3u² >=1 throughout the entire dependent interval.
            assert 1+3*lo*lo >= 1 and 1+3*hi*hi >= 1
            real_hull_cases += 1

    # This queried inverse is irrational: the rational-root candidates
    # for 4u³+4u-1 are +/-1,+/-1/2,+/-1/4, and none is a root.
    for candidate in [Q(sign, denominator)
                      for sign in [-1, 1] for denominator in [1, 2, 4]]:
        assert 4*candidate**3+4*candidate-1 != 0
    irrational_lo, irrational_hi = root_bracket(Q(1, 4), Q(1, 2**40))
    assert irrational_lo < irrational_hi

    # For centers +/-1/2, the reduced scalar second derivative is
    # (2-6u²+12*center*u)/(1+3u²)^3 <=7/2. Thus the largest retained
    # diagonal is <=2+(7/2)(1+1/16)=183/32<6.
    L = Q(6)
    assert 2+Q(7, 2)*Q(17, 16) < L
    cells = [[tuple(instance.bounds[i] for i in bag)] for bag in instance.bags]
    upper = None
    records = []
    counts = {name: 0 for name in [
        'min_marginals', 'retained_witnesses', 'removed_cells',
        'rounding_atoms', 'growth_checks', 'strict_row_intervals']}
    closure_stage = None
    for stage in range(9):
        h = Q(2, 2**stage)
        error = len(instance.bounds)*L*h*h/8
        delta = error/len(instance.bags)
        rows = [sorted({tuple(row) for cell in whitelist for row in corners(cell)})
                for whitelist in cells]
        intervals = [{row: instance.enclosure(t, row, delta)
                      for row in table} for t, table in enumerate(rows)]
        costs = [{row: interval[0] for row, interval in table.items()}
                 for table in intervals]
        instance.costs = costs
        counts['strict_row_intervals'] += sum(
            low < high for table in intervals for low, high, _ in table.values())
        lower, witness, marginals, _ = sparse_tree_dp(instance, rows, costs)
        exact, brute_marginals, brute_witnesses, _, _ = brute_grid(instance, rows, costs)
        assert lower == exact and marginals == brute_marginals
        counts['min_marginals'] += sum(map(len, marginals))
        total_error = delta*len(instance.bags)
        assert total_error == error
        upper = lower+total_error if upper is None else min(upper, lower+total_error)
        assert 0 <= upper <= 2*error and lower <= error
        recovered_upper = sum(intervals[t][tuple(witness[i] for i in bag)][1]
                              for t, bag in enumerate(instance.bags))
        assert recovered_upper <= lower+total_error

        kept = [[] for _ in cells]
        for t, whitelist in enumerate(cells):
            for cell in whitelist:
                candidates = [(marginals[t][tuple(row)], tuple(row))
                              for row in corners(cell) if tuple(row) in marginals[t]]
                if not candidates:
                    counts['removed_cells'] += 1
                    continue
                value, row = min(candidates)
                if value-error > upper:
                    counts['removed_cells'] += 1
                    continue
                kept[t].append(cell)
                point = brute_witnesses[t][row]
                assert contains(cell, row) and instance.value(point) == value
                true_upper = sum(intervals[b][tuple(point[i] for i in bag)][1]
                                 for b, bag in enumerate(instance.bags))
                assert true_upper <= value+total_error <= 4*error
                norm2 = sum((x-a)**2 for x, a in zip(point, instance.optimum))
                # Every interval lower value includes its exact retained
                # square and a nonnegative control-square lower bound.
                assert norm2 <= value <= true_upper
                counts['retained_witnesses'] += 1
                counts['growth_checks'] += 1
        assert physical_member(instance, kept, instance.optimum)

        expected_upper = Q(0)
        for choices in product(*round_laws(instance, instance.optimum, h)):
            point = tuple(value for value, _ in choices)
            probability = Q(1)
            for _, weight in choices:
                probability *= weight
            assert physical_member(instance, cells, point)
            _, point_upper = instance.point_enclosure(point, error/64)
            expected_upper += probability*point_upper
            counts['rounding_atoms'] += 1
        assert expected_upper <= error

        hull = coordinate_hull(instance, kept)
        integer_fixed = all(hull[i] == (Q(0), Q(0)) for i in instance.integers)
        numerator_lowers = None
        if integer_fixed:
            xlo, xhi = hull[0]
            vlo, vhi = hull[1]
            rhs_ranges = [(xlo, xhi), (vlo-xhi/4, vhi-xlo/4)]
            root_ranges = [(root_bracket(lo, Q(1, 2**20))[0],
                            root_bracket(hi, Q(1, 2**20))[1])
                           for lo, hi in rhs_ranges]
            numerator_lowers = [reduced_curvature_lower(interval, center)
                                for interval, center in zip(root_ranges, [Q(1, 2), Q(-1, 2)])]
            if min(numerator_lowers) >= 0:
                # The reduced Hessian equals 2I plus two nonnegative
                # rank-one terms. This certifies a strongly convex patch
                # for the true algebraic objective, not the row costs.
                closure_stage = stage
        records.append({'stage': stage, 'h': str(h), 'rows': sum(map(len, rows)),
                        'retained_cells': sum(map(len, kept)), 'upper': str(upper),
                        'integer_fixed': integer_fixed,
                        'curvature_numerators': None if numerator_lowers is None
                        else list(map(str, numerator_lowers))})
        if closure_stage is not None:
            break
        cells = [[child for cell in whitelist for child in refine_cell(
            cell, h, tuple(k for k, i in enumerate(bag) if i in instance.integers))]
                 for bag, whitelist in zip(instance.bags, kept)]
    assert closure_stage is not None and counts['removed_cells'] > 0
    assert counts['strict_row_intervals'] > 0 and instance.nonpoint_brackets > 0

    # Nonzero dependent-coordinate noise is evaluated on the same graph;
    # tight refinements must overlap the coarser certified value intervals.
    noisy_cases = 0
    for eta, x, z in product([Q(-2, 7), Q(3, 11)],
                             [Q(-2, 3), Q(1, 4), Q(7, 8)], [Q(0), Q(1, 2), Q(1)]):
        coarse = instance.enclosure(0, (x, z), Q(1, 2**10), eta)
        fine = instance.enclosure(0, (x, z), Q(1, 2**24), eta)
        assert max(coarse[0], fine[0]) <= min(coarse[1], fine[1])
        assert coarse[2][0] <= fine[2][0] <= fine[2][1] <= coarse[2][1]
        noisy_cases += 1

    report = {'status': 'passed', 'scope': 'finite exact cubic-chart checks only',
              'stages': len(records), 'closure_stage': closure_stage,
              'full_real_hull_brackets': real_hull_cases,
              'noisy_value_refinements': noisy_cases,
              'root_brackets': instance.brackets,
              'nonpoint_root_brackets': instance.nonpoint_brackets,
              'max_denominator_bits': instance.max_denominator_bits,
              'counts': counts, 'records': records}
    Path(__file__).with_name('smoothed-implicit-graph-check-results.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'records'}))


if __name__ == '__main__':
    main()
