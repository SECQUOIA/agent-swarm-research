#!/usr/bin/env python3
"""Targeted exact checks of aligned bag-cell pruning and convex closure.

The sparse tree DP is the algorithm under test. Exhaustive allowed-node and
active-face enumeration are independent small-instance verification oracles.
No timing or smoothed-complexity conclusion is drawn from these examples.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from random import Random


@dataclass
class Instance:
    name: str
    hessian: list[list[Q]]
    linear: list[Q]
    constant: Q
    bounds: list[tuple[Q, Q]]
    bags: list[tuple[int, ...]]
    edges: list[tuple[int, int]]
    extra_optima: list[tuple[Q, ...]]
    stages: int = 5
    integers: frozenset[int] = frozenset()

    def value(self, x):
        n = len(x)
        return self.constant + sum(self.linear[i] * x[i] for i in range(n)) + sum(
            self.hessian[i][j] * x[i] * x[j] / 2
            for i in range(n) for j in range(n)
        )


def unique_linear_solution(matrix, rhs, count):
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    pivots = []
    for col in range(count):
        pivot = next((i for i in range(len(pivots), len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        pos = len(pivots)
        rows[pos], rows[pivot] = rows[pivot], rows[pos]
        divisor = rows[pos][col]
        rows[pos] = [x / divisor for x in rows[pos]]
        for i in range(len(rows)):
            if i != pos and rows[i][col]:
                multiplier = rows[i][col]
                rows[i] = [x - multiplier * y for x, y in zip(rows[i], rows[pos])]
        pivots.append(col)
    if len(pivots) != count or any(not any(row[:count]) and row[count] for row in rows):
        return None
    result = [Q(0)] * count
    for row, col in enumerate(pivots):
        result[col] = rows[row][count]
    return result


def exact_box_oracle(instance, bounds=None):
    """Minimum-face stationarity gives an exact small-instance value oracle."""
    bounds = instance.bounds if bounds is None else bounds
    n = len(bounds)
    candidates = set()
    continuous = [i for i in range(n) if i not in instance.integers]
    integer_indices = sorted(instance.integers)
    integer_domains = []
    for i in integer_indices:
        lo, hi = bounds[i]
        assert lo.denominator == hi.denominator == 1
        integer_domains.append(range(int(lo), int(hi) + 1))
    statuses = [([0] if bounds[i][0] == bounds[i][1] else [-1, 0, 1])
                for i in continuous]
    faces = 0
    for integers, status in product(product(*integer_domains), product(*statuses)):
        faces += 1
        fixed = {i: Q(value) for i, value in zip(integer_indices, integers)}
        fixed.update({i: bounds[i][side] for i, side in zip(continuous, status) if side >= 0})
        free = [i for i, side in zip(continuous, status) if side == -1]
        matrix = [[instance.hessian[i][j] for j in free] for i in free]
        rhs = [-instance.linear[i] - sum(instance.hessian[i][j] * x for j, x in fixed.items())
               for i in free]
        solution = unique_linear_solution(matrix, rhs, len(free))
        if solution is None:
            continue
        point = [fixed.get(i, Q(0)) for i in range(n)]
        for i, value in zip(free, solution):
            point[i] = value
        if all(lo <= x <= hi for x, (lo, hi) in zip(point, bounds)):
            candidates.add(tuple(point))
    assert candidates
    optimum = min(map(instance.value, candidates))
    optima = sorted(x for x in candidates if instance.value(x) == optimum)
    return optimum, optima, faces


def is_psd(matrix):
    a = [list(row) for row in matrix]
    while a:
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        pivot = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if pivot is None:
            return all(value == 0 for row in a for value in row)
        remaining = [i for i in range(len(a)) if i != pivot]
        d = a[pivot][pivot]
        a = [[a[i][j] - a[i][pivot] * a[pivot][j] / d for j in remaining]
             for i in remaining]
    return True


def corners(cell):
    return product(*[sorted(set(interval)) for interval in cell])


def contains(cell, row):
    return all(lo <= x <= hi for x, (lo, hi) in zip(row, cell))


def physical_member(instance, cells, point):
    if any(Q(point[i]).denominator != 1 for i in instance.integers):
        return False
    return all(any(contains(cell, tuple(point[i] for i in bag)) for cell in whitelist)
               for bag, whitelist in zip(instance.bags, cells))


def refine_cell(cell, h, integer_positions=()):
    intervals = []
    for position, (lo, hi) in enumerate(cell):
        if position in integer_positions and h <= 1:
            assert lo.denominator == hi.denominator == 1
            assert lo == hi or (h == 1 and hi - lo == 1)
            intervals.append([(value, value) for value in sorted({lo, hi})])
            continue
        cut = lo + h / 2
        intervals.append([(lo, cut), (cut, hi)] if cut < hi else [(lo, hi)])
    return list(product(*intervals))


def make_rows_and_costs(instance, cells):
    rows = [sorted({tuple(row) for cell in whitelist for row in corners(cell)})
            for whitelist in cells]
    terms = [[] for _ in instance.bags]
    n = len(instance.bounds)
    for i in range(n):
        owner = next(t for t, bag in enumerate(instance.bags) if i in bag)
        terms[owner].append((i, i, instance.hessian[i][i] / 2))
        terms[owner].append((i, None, instance.linear[i]))
    for i in range(n):
        for j in range(i + 1, n):
            if instance.hessian[i][j]:
                owner = next(t for t, bag in enumerate(instance.bags) if i in bag and j in bag)
                terms[owner].append((i, j, instance.hessian[i][j]))
    costs = []
    for t, (bag, table) in enumerate(zip(instance.bags, rows)):
        local = {}
        for row in table:
            assignment = dict(zip(bag, row))
            value = instance.constant if t == 0 else Q(0)
            value += sum(coefficient * assignment[i] * (assignment[j] if j is not None else 1)
                         for i, j, coefficient in terms[t])
            local[row] = value
        costs.append(local)
    return rows, costs


def sparse_tree_dp(instance, rows, costs):
    """Two directed sparse passes; every join is a separator-key lookup."""
    count = len(instance.bags)
    neighbors = [[] for _ in range(count)]
    for a, b in instance.edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    separators = {(a, b): tuple(sorted(set(instance.bags[a]) & set(instance.bags[b])))
                  for a in range(count) for b in neighbors[a]}
    positions = {(a, b): tuple(instance.bags[a].index(i) for i in separators[a, b])
                 for a in range(count) for b in neighbors[a]}

    def key(a, b, row):
        return tuple(row[i] for i in positions[a, b])

    messages = {}
    arguments = {}
    row_visits = 0

    def send(a, parent):
        nonlocal row_visits
        if (a, parent) in messages:
            return messages[a, parent]
        children = [b for b in neighbors[a] if b != parent]
        for b in children:
            send(b, a)
        result, arg = {}, {}
        for row in rows[a]:
            row_visits += 1
            value = costs[a][row]
            for b in children:
                incoming = messages[b, a].get(key(a, b, row))
                if incoming is None:
                    break
                value += incoming
            else:
                separator = key(a, parent, row)
                if separator not in result or value < result[separator]:
                    result[separator], arg[separator] = value, row
        messages[a, parent], arguments[a, parent] = result, arg
        return result

    for a in range(count):
        for b in neighbors[a]:
            send(a, b)
    marginals = []
    for a in range(count):
        marginal = {}
        for row in rows[a]:
            row_visits += 1
            value = costs[a][row]
            for b in neighbors[a]:
                incoming = messages[b, a].get(key(a, b, row))
                if incoming is None:
                    break
                value += incoming
            else:
                marginal[row] = value
        marginals.append(marginal)
    assert marginals[0]
    root_row = min(marginals[0], key=lambda row: (marginals[0][row], row))
    optimum = marginals[0][root_row]
    point = {}

    def recover(a, parent, row):
        for i, x in zip(instance.bags[a], row):
            assert i not in point or point[i] == x
            point[i] = x
        for b in neighbors[a]:
            if b != parent:
                recover(b, a, arguments[b, a][key(a, b, row)])

    recover(0, -1, root_row)
    answer = tuple(point[i] for i in range(len(instance.bounds)))
    assert instance.value(answer) == optimum
    return optimum, answer, marginals, row_visits


def brute_grid(instance, rows, costs):
    domains = [set() for _ in instance.bounds]
    for bag, table in zip(instance.bags, rows):
        for row in table:
            for i, value in zip(bag, row):
                domains[i].add(value)
    sets = list(map(set, rows))
    marginals = [{} for _ in rows]
    witnesses = [{} for _ in rows]
    feasible = []
    examined = 0
    for point in product(*[sorted(values) for values in domains]):
        examined += 1
        local = [tuple(point[i] for i in bag) for bag in instance.bags]
        if not all(row in allowed for row, allowed in zip(local, sets)):
            continue
        value = sum(cost[row] for row, cost in zip(local, costs))
        feasible.append(point)
        for t, row in enumerate(local):
            if row not in marginals[t] or value < marginals[t][row]:
                marginals[t][row], witnesses[t][row] = value, point
    assert feasible
    return min(marginals[0].values()), marginals, witnesses, feasible, examined


def round_laws(instance, point, h):
    laws = []
    for i, (x, (lo, hi)) in enumerate(zip(point, instance.bounds)):
        if i in instance.integers:
            assert x.denominator == 1
            if h < 1:
                laws.append([(x, Q(1))])
                continue
        index = (x - lo) / h
        if x == hi or index.denominator == 1:
            laws.append([(x, Q(1))])
        else:
            left = lo + (index.numerator // index.denominator) * h
            right = min(left + h, hi)
            laws.append([(left, (right - x) / (right - left)),
                         (right, (x - left) / (right - left))])
    return laws


def gradient_closure(instance, cells, fixed, optimum, known_optima):
    hull = []
    for i in range(len(instance.bounds)):
        bag_hulls = []
        for bag, whitelist in zip(instance.bags, cells):
            if i in bag:
                projections = [cell[bag.index(i)] for cell in whitelist]
                bag_hulls.append((min(a for a, _ in projections), max(b for _, b in projections)))
        hull.append((max(a for a, _ in bag_hulls), min(b for _, b in bag_hulls)))
        assert hull[-1][0] <= hull[-1][1]
    assert all(all(a <= x <= b for x, (a, b) in zip(point, hull)) for point in known_optima)
    fixed = dict(fixed)
    for i in instance.integers:
        if hull[i][0] == hull[i][1]:
            assert hull[i][0].denominator == 1
            fixed[i] = hull[i][0]
    assert all(all(point[i] == value for i, value in fixed.items()) for point in known_optima)
    gradient_checks = 0
    while True:
        for i, value in fixed.items():
            hull[i] = (value, value)
        additions = {}
        for i in range(len(hull)):
            if i in fixed or i in instance.integers:
                continue
            lower = upper = instance.linear[i]
            for coefficient, (lo, hi) in zip(instance.hessian[i], hull):
                lower += coefficient * (lo if coefficient >= 0 else hi)
                upper += coefficient * (hi if coefficient >= 0 else lo)
            gradient_checks += 1
            if lower > 0:
                additions[i] = instance.bounds[i][0]
            elif upper < 0:
                additions[i] = instance.bounds[i][1]
        if not additions:
            break
        fixed.update(additions)
        assert all(all(point[i] == value for i, value in fixed.items()) for point in known_optima)
    free = [i for i in range(len(hull)) if i not in fixed]
    all_integers_fixed = instance.integers.issubset(fixed)
    psd = all_integers_fixed and is_psd([[instance.hessian[i][j] for j in free] for i in free])
    if psd:
        face = [(fixed[i], fixed[i]) if i in fixed else bounds
                for i, bounds in enumerate(instance.bounds)]
        value, solutions, _ = exact_box_oracle(instance, face)
        assert value == optimum
        candidate = solutions[0]
        for i in free:
            gradient = instance.linear[i] + sum(instance.hessian[i][j] * candidate[j]
                                                for j in range(len(candidate)))
            lo, hi = instance.bounds[i]
            if candidate[i] == lo:
                assert gradient >= 0
            elif candidate[i] == hi:
                assert gradient <= 0
            else:
                assert gradient == 0
    return fixed, psd, gradient_checks


def check_instance(instance):
    optimum, optima, faces = exact_box_oracle(instance)
    known = sorted(set(optima + instance.extra_optima))
    assert all(instance.value(x) == optimum for x in known)
    n = len(instance.bounds)
    curvature = max(Q(0), *[instance.hessian[i][i] for i in range(n)])
    assert curvature > 0
    scale = max(hi - lo for lo, hi in instance.bounds)
    if instance.integers:
        initial_mesh = Q(1)
        while initial_mesh < scale:
            initial_mesh *= 2
        scale = initial_mesh
    cells = [{tuple(instance.bounds[i] for i in bag)} for bag in instance.bags]
    incumbent = instance.value(tuple(lo for lo, _ in instance.bounds))
    fixed = {}
    rng = Random(113)
    record = {"name": instance.name, "variables": n, "integer_variables": sorted(instance.integers),
              "optimum": str(optimum),
              "oracle_faces": faces, "sampled_optima": len(known), "stages": []}
    discarded = []
    for stage in range(instance.stages):
        h = scale / (2 ** stage)
        for bag, whitelist in zip(instance.bags, cells):
            for cell in whitelist:
                for i, (lo, hi) in zip(bag, cell):
                    if i in instance.integers:
                        assert lo.denominator == hi.denominator == 1
                        if h < 1:
                            assert lo == hi
        error = n * curvature * h * h / 8
        assert all(physical_member(instance, cells, point) for point in known)
        rows, costs = make_rows_and_costs(instance, cells)
        minimum, point, margins, visits = sparse_tree_dp(instance, rows, costs)
        brute_min, brute_margins, witnesses, feasible, examined = brute_grid(instance, rows, costs)
        assert minimum == brute_min and margins == brute_margins
        assert physical_member(instance, cells, point)
        incumbent = min(incumbent, minimum)
        lower = minimum - error
        assert lower <= optimum <= incumbent
        assert incumbent - lower <= error
        assert minimum - optimum <= error
        assert all(bound is None or bound > old_upper >= incumbent >= lower
                   for bound, old_upper in discarded)
        conditional = []
        for whitelist, marginal in zip(cells, margins):
            table = {}
            for cell in whitelist:
                values = [marginal[row] for row in corners(cell) if row in marginal]
                table[cell] = min(values) - error if values else None
            conditional.append(table)
        samples = list(known)
        for _ in range(min(12, len(feasible))):
            node = rng.choice(feasible)
            chosen = [rng.choice(sorted(cell for cell in whitelist
                                        if contains(cell, tuple(node[i] for i in bag))))
                      for bag, whitelist in zip(instance.bags, cells)]
            point_sample = []
            for i in range(n):
                intervals = [cell[bag.index(i)] for bag, cell in zip(instance.bags, chosen) if i in bag]
                lo, hi = max(a for a, _ in intervals), min(b for _, b in intervals)
                value = (2 * lo + hi) / 3
                if i in instance.integers:
                    value = Q(value.numerator // value.denominator)
                point_sample.append(value)
            samples.append(tuple(point_sample))
        atoms = 0
        for sample in samples:
            assert physical_member(instance, cells, sample)
            expectation = Q(0)
            for law in product(*round_laws(instance, sample, h)):
                rounded = tuple(value for value, _ in law)
                weight = Q(1)
                for _, probability in law:
                    weight *= probability
                assert physical_member(instance, cells, rounded)
                assert all(tuple(rounded[i] for i in bag) in margin
                           for bag, margin in zip(instance.bags, margins))
                expectation += weight * instance.value(rounded)
                atoms += 1
            assert expectation <= instance.value(sample) + error
            for bag, table in zip(instance.bags, conditional):
                for cell, bound in table.items():
                    if contains(cell, tuple(sample[i] for i in bag)):
                        assert bound is not None and bound <= instance.value(sample)
        retained = []
        witness_count = removed = 0
        for t, table in enumerate(conditional):
            keep = set()
            for cell, bound in table.items():
                if bound is not None and bound <= incumbent:
                    keep.add(cell)
                    corner = min((row for row in corners(cell) if row in margins[t]),
                                 key=lambda row: margins[t][row])
                    witness = witnesses[t][corner]
                    assert instance.value(witness) - optimum <= 2 * error
                    witness_count += 1
                else:
                    discarded.append((bound, incumbent))
                    removed += 1
            assert keep
            retained.append(keep)
        assert all(physical_member(instance, retained, x) for x in known)
        old_fixed = set(fixed)
        fixed, closed, gradient_checks = gradient_closure(instance, retained, fixed, optimum, known)
        new_fixed = set(fixed) - old_fixed
        record["stages"].append({"stage": stage, "mesh": str(h), "error_bound": str(error),
                                 "bag_rows": sum(map(len, rows)), "dp_row_visits": visits,
                                 "brute_assignments_examined": examined,
                                 "allowed_assignments": len(feasible),
                                 "min_marginals_checked": sum(map(len, margins)),
                                 "rounding_atoms": atoms, "retained_cells": witness_count,
                                 "removed_cells": removed, "gradient_intervals": gradient_checks,
                                 "new_endpoint_fixes": len(new_fixed - instance.integers),
                                 "new_integer_fixes": len(new_fixed & instance.integers),
                                 "psd_face_closed": closed})
        if closed:
            record["closure_stage"] = stage
            break
        cells = [{child for cell in whitelist
                  for child in refine_cell(cell, h, {k for k, i in enumerate(bag) if i in instance.integers})}
                 for bag, whitelist in zip(instance.bags, retained)]
    record["fixed_coordinates"] = {str(i): str(value) for i, value in fixed.items()}
    return record


def from_shifted(name, hessian, center, bounds, bags, edges, stages=5):
    n = len(bounds)
    linear = [-sum(hessian[i][j] * center[j] for j in range(n)) for i in range(n)]
    constant = sum(hessian[i][j] * center[i] * center[j] / 2 for i in range(n) for j in range(n))
    return Instance(name, hessian, linear, constant, bounds, bags, edges, [], stages)


def instances():
    # Unique nonconvex boundary optimum; the last gradient is not initially
    # sign-definite, so pruning must tighten the hull before convex closure.
    h = [[Q(1), Q(1, 10), Q(0)], [Q(1, 10), Q(1), Q(1, 10)],
         [Q(0), Q(1, 10), Q(-1, 2)]]
    center = [Q(3, 10), Q(2, 5), Q(0)]
    one = from_shifted("nonconvex_boundary_closure", h, center, [(Q(0), Q(1))] * 3,
                       [(0, 1), (1, 2)], [(0, 1)])
    one.linear[2] += Q(2, 5)
    one.extra_optima = [tuple(center)]

    # A continuum of tied optima on each of two disconnected components.
    two = Instance("flat_and_disconnected_ties",
                   [[Q(2), Q(-2), Q(0)], [Q(-2), Q(2), Q(0)],
                    [Q(0), Q(0), Q(-1, 4)]],
                   [Q(0), Q(0), Q(1, 8)], Q(0), [(Q(0), Q(1))] * 3,
                   [(0, 1), (1, 2)], [(0, 1)],
                   [(t, t, z) for t in [Q(1, 3), Q(2, 5)] for z in [Q(0), Q(1)]], 5)

    # Two-step stable recurrence: all diagonal curvatures are positive,
    # while four binary choices give four exact global optimizers.
    size = 4
    h3 = [[Q(0) for _ in range(size)] for _ in range(size)]
    b3 = [Q(0)] * size
    for t in range(2):
        coefficients = {t: Q(1), 2 + t: Q(-1, 2)}
        if t:
            coefficients[t - 1] = Q(-1, 2)
        for i, a in coefficients.items():
            for j, b in coefficients.items():
                h3[i][j] += 2 * a * b
        h3[2 + t][2 + t] -= Q(1, 4)
        b3[2 + t] += Q(1, 8)
    three = Instance("positive_diagonal_binary_ties", h3, b3, Q(0),
                     [(Q(0), Q(1))] * size, [(0, 2), (0, 1, 3)], [(0, 1)], [], 5)

    # Unequal rational widths exercise clipped, nested physical intervals.
    size = 5
    h4 = [[Q(0) for _ in range(size)] for _ in range(size)]
    for i in range(size - 1):
        h4[i][i] = Q(1)
    h4[-1][-1] = Q(-1, 2)
    for i in range(size - 1):
        h4[i][i + 1] = h4[i + 1][i] = Q(1, 20)
    center4 = [Q(1, 5), Q(3, 10), Q(2, 5), Q(3, 5), Q(0)]
    four = from_shifted("unequal_clipped_five_variables", h4, center4,
                        [(Q(-1, 2), Q(3, 4)), (Q(0), Q(1)), (Q(-1, 4), Q(3, 4)),
                         (Q(0), Q(7, 8)), (Q(0), Q(3, 4))],
                        [(0, 1), (1, 2), (2, 3), (3, 4)], [(0, 1), (1, 2), (2, 3)])
    four.linear[-1] += Q(2, 5)
    four.extra_optima = [tuple(center4)]

    # A degree-three decomposition node exercises sparse joins across
    # several children; the objective is convex but has a flat direction.
    size = 5
    h5 = [[Q(0) for _ in range(size)] for _ in range(size)]
    for i in range(1, size):
        h5[0][0] += 2
        h5[i][i] += 2
        h5[0][i] = h5[i][0] = Q(-2)
    five = Instance("branching_convex_flat_closure", h5, [Q(0)] * size, Q(0),
                    [(Q(0), Q(1))] * size,
                    [(0, 1), (0, 2), (0, 3), (0, 4)], [(0, 1), (0, 2), (0, 3)],
                    [(Q(1, 3),) * size], 3)
    return [one, two, three, four, five]


def check_boundary_only_intersection():
    """Opposite closed cells meet only on a shared-coordinate boundary."""
    instance = from_shifted(
        "boundary_only_intersection",
        [[Q(2), Q(0), Q(0)], [Q(0), Q(2), Q(0)], [Q(0), Q(0), Q(2)]],
        [Q(1, 4), Q(1, 2), Q(1, 4)], [(Q(0), Q(1))] * 3,
        [(0, 1), (1, 2)], [(0, 1)],
    )
    cells = [{((Q(0), Q(1, 2)), (Q(0), Q(1, 2)))},
             {((Q(1, 2), Q(1)), (Q(0), Q(1, 2)))}]
    rows, costs = make_rows_and_costs(instance, cells)
    minimum, _, margins, _ = sparse_tree_dp(instance, rows, costs)
    brute_minimum, brute_margins, _, feasible, _ = brute_grid(instance, rows, costs)
    assert minimum == brute_minimum and margins == brute_margins
    unavailable = sum(len(table) - len(marginal) for table, marginal in zip(rows, margins))
    assert unavailable == 4 and len(feasible) == 4
    sample = (Q(1, 3), Q(1, 2), Q(1, 4))
    assert physical_member(instance, cells, sample)
    expectation = Q(0)
    atoms = 0
    for law in product(*round_laws(instance, sample, Q(1, 2))):
        point = tuple(value for value, _ in law)
        weight = Q(1)
        for _, probability in law:
            weight *= probability
        assert point[1] == Q(1, 2) and physical_member(instance, cells, point)
        expectation += weight * instance.value(point)
        atoms += 1
    assert atoms == 4 and expectation <= instance.value(sample) + Q(3, 16)
    return {"status": "passed", "infeasible_bag_rows": unavailable,
            "allowed_assignments": len(feasible), "boundary_preserving_rounding_atoms": atoms}


def main():
    records = [check_instance(instance) for instance in instances()]
    stage_records = [stage for record in records for stage in record["stages"]]
    total_keys = ["bag_rows", "dp_row_visits", "brute_assignments_examined", "allowed_assignments",
                  "min_marginals_checked", "rounding_atoms", "retained_cells", "removed_cells",
                  "gradient_intervals", "new_endpoint_fixes"]
    report = {"status": "passed", "scope": "exact finite examples; no expectation or performance claim",
              "instances": len(records), "stages": len(stage_records),
              "totals": {key: sum(stage[key] for stage in stage_records) for key in total_keys},
              "closure_cases": sum("closure_stage" in record for record in records),
              "boundary_fixture": check_boundary_only_intersection(),
              "records": records}
    destination = Path(__file__).with_name("sparse-bag-cell-check-results.json")
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["status", "instances", "stages", "closure_cases", "totals", "boundary_fixture"]}))


if __name__ == "__main__":
    main()
