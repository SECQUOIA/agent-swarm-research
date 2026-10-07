#!/usr/bin/env python3
"""Exact small-instance simplex DP and tangential-closure diagnostic."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from check_sparse_bag_cells import contains, corners, refine_cell, sparse_tree_dp


class Instance:
    bounds = [(Q(0), Q(1))] * 5
    bags = [(0, 1, 4), (2, 3, 4)]
    edges = [(0, 1)]
    integers = frozenset({4})

    @staticmethod
    def local(bag, row):
        x, y, z = row
        if bag == 0:
            u, slack = x-Q(1, 3), 1-x-y
            return u*u+u**4+slack-slack*slack/4+(z-1)**2/2+u*(z-1)/4
        u = x-Q(1, 4)
        return u*u+u**4+y+y*y+(z-1)**2/2+y*(z-1)/2

    def value(self, point):
        return sum(self.local(t, tuple(point[i] for i in bag))
                   for t, bag in enumerate(self.bags))


def feasible_corners(cell):
    return [tuple(row) for row in corners(cell) if row[0]+row[1] <= 1]


def brute_pairs(rows, costs):
    margins = [{row: None for row in table} for table in rows]
    witnesses = [{}, {}]
    best = None
    points = []
    for left, right in product(*rows):
        if left[2] != right[2]:
            continue
        point = (left[0], left[1], right[0], right[1], left[2])
        value = costs[0][left]+costs[1][right]
        best = value if best is None else min(best, value)
        points.append((point, value))
        for t, row in enumerate((left, right)):
            if margins[t][row] is None or value < margins[t][row]:
                margins[t][row] = value
                witnesses[t][row] = point
    margins = [{r: v for r, v in table.items() if v is not None} for table in margins]
    assert best is not None
    return best, margins, witnesses, points


def block_round(point, cell):
    """Exact pairwise law used only to witness the convex combination."""
    lower = tuple(interval[0] for interval in cell)
    widths = tuple(hi-lo for lo, hi in cell)
    p = tuple((v-lo)/width if width else Q(0)
              for v, lo, width in zip(point, lower, widths))

    def recurse(values):
        fractional = [i for i, v in enumerate(values) if 0 < v < 1]
        if not fractional:
            return [(values, Q(1))]
        if len(fractional) == 1:
            i = fractional[0]
            result = []
            for bit in (0, 1):
                out = list(values)
                out[i] = Q(bit)
                result.append((tuple(out), values[i] if bit else 1-values[i]))
            return result
        i, j = fractional[:2]
        plus = min(1-values[i], values[j])
        minus = min(values[i], 1-values[j])
        result = []
        for delta, probability in ((plus, minus/(plus+minus)),
                                   (-minus, plus/(plus+minus))):
            out = list(values)
            out[i] += delta
            out[j] -= delta
            result.extend((atom, probability*weight) for atom, weight in recurse(tuple(out)))
        return result

    law = [(tuple(lo+width*v for lo, width, v in zip(lower, widths, atom)), weight)
           for atom, weight in recurse(p)]
    assert sum(weight for _, weight in law) == 1
    assert all(sum(atom) <= 1 for atom, _ in law)
    assert all(sum(weight*atom[i] for atom, weight in law) == point[i] for i in range(2))
    return law


def hull(instance, cells):
    answer = []
    for i in range(5):
        projections = []
        for bag, whitelist in zip(instance.bags, cells):
            if i in bag:
                pos = bag.index(i)
                vertices = [row[pos] for cell in whitelist for row in feasible_corners(cell)]
                projections.append((min(vertices), max(vertices)))
        answer.append((max(lo for lo, _ in projections), min(hi for _, hi in projections)))
    return answer


def main():
    instance = Instance()
    optimum = (Q(1, 3), Q(2, 3), Q(1, 4), Q(0), Q(1))
    L, M1, T, g0 = Q(9), Q(9), Q(18), Q(1, 4)
    cells = [[tuple(instance.bounds[i] for i in bag)] for bag in instance.bags]
    upper = None
    counts = dict(marginals=0, compatible_assignments=0, retained_witnesses=0,
                  removed_cells=0, rounding_atoms=0, growth_checks=0)
    records = []
    closure = None
    for stage in range(11):
        h = Q(1, 2**stage)
        rows = [sorted({row for cell in whitelist for row in feasible_corners(cell)})
                for whitelist in cells]
        costs = [{row: instance.local(t, row) for row in table} for t, table in enumerate(rows)]
        value, _, margins, _ = sparse_tree_dp(instance, rows, costs)
        brute, exact_margins, witnesses, assignments = brute_pairs(rows, costs)
        assert value == brute and margins == exact_margins
        counts['marginals'] += sum(map(len, margins))
        counts['compatible_assignments'] += len(assignments)
        upper = value if upper is None else min(upper, value)
        error = 5*L*h*h/8
        assert 0 <= upper <= value <= error
        kept = [[] for _ in cells]
        for t, whitelist in enumerate(cells):
            for cell in whitelist:
                eligible = [(margins[t][row], row) for row in feasible_corners(cell)
                            if row in margins[t]]
                if not eligible:
                    counts['removed_cells'] += 1
                    continue
                cost, row = min(eligible)
                if cost-error <= upper:
                    kept[t].append(cell)
                    point = witnesses[t][row]
                    assert instance.value(point) == cost <= 2*error
                    counts['retained_witnesses'] += 1
                else:
                    counts['removed_cells'] += 1
        for bag, whitelist in zip(instance.bags, kept):
            assert any(contains(cell, tuple(optimum[i] for i in bag)) for cell in whitelist)
        chosen = [next(cell for cell in whitelist
                       if contains(cell, tuple(optimum[i] for i in bag)))
                  for bag, whitelist in zip(instance.bags, cells)]
        laws = [block_round(optimum[:2], chosen[0][:2]),
                block_round(optimum[2:4], chosen[1][:2])]
        expected = Q(0)
        for (left, pl), (right, pr) in product(*laws):
            point = left+right+(Q(1),)
            assert all(any(contains(cell, tuple(point[i] for i in bag)) for cell in whitelist)
                       for bag, whitelist in zip(instance.bags, cells))
            expected += pl*pr*instance.value(point)
            counts['rounding_atoms'] += 1
        assert expected <= error
        for point, cost in assignments[::max(1, len(assignments)//40)]:
            norm2 = sum((x-a)**2 for x, a in zip(point, optimum))
            assert cost >= Q(7, 24)*norm2
            counts['growth_checks'] += 1
        bounds = hull(instance, kept)
        midpoint = [(lo+hi)/2 for lo, hi in bounds]
        radius = max((hi-lo)/2 for lo, hi in bounds)
        z_fixed = bounds[4] == (Q(1), Q(1))
        gy = -1+(1-midpoint[0]-midpoint[1])/2
        gb = 1+2*midpoint[3]+(midpoint[4]-1)/2
        budget_fixed = z_fixed and gy+M1*radius < 0
        zero_fixed = z_fixed and gb-M1*radius > 0
        pd = False
        if budget_fixed and zero_fixed:
            low = max(bounds[0][0], 1-bounds[1][1])
            high = min(bounds[0][1], 1-bounds[1][0])
            x = (low+high)/2
            a = sum(bounds[2])/2
            r = max((high-low)/2, (bounds[2][1]-bounds[2][0])/2)
            margin1 = 2+12*(x-Q(1, 3))**2-2*(T*r+g0)
            margin2 = 2+12*(a-Q(1, 4))**2-(T*r+g0)
            pd = min(margin1, margin2) > 0
            if pd:
                assert Q(-1, 2) < 0  # Full ambient Hessian has a negative y diagonal.
                closure = stage
        records.append(dict(stage=stage, rows=sum(map(len, rows)), retained=sum(map(len, kept)),
                            integer_fixed=z_fixed, budget_fixed=budget_fixed,
                            zero_fixed=zero_fixed, tangent_pd=pd))
        if pd:
            break
        cells = [sorted({child for cell in whitelist for child in refine_cell(cell, h, (2,))
                         if child[0][0]+child[1][0] <= 1}) for whitelist in kept]
    assert closure is not None
    result = dict(status='passed', scope='finite exact simplex DP/closure diagnostic',
                  closure_stage=closure, counts=counts, stages=records)
    Path(__file__).with_name('simplex-sparse-dp-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'stages'}))


if __name__ == '__main__':
    main()
