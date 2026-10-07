"""Bounded exact diagnostics for the TU filtered-grid theorem.

Standard library only. This is a small reference prototype, not a benchmark
against production solvers. All optimization and certificate comparisons
use fractions.Fraction. The two-pass DP enforces the original equalities.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path
from time import perf_counter


def solve_linear(rows, rhs, ncols):
    """Unique consistent solution of a possibly overdetermined system."""
    mat = [[Q(v) for v in row] + [Q(b)] for row, b in zip(rows, rhs)]
    pivots = []
    for col in range(ncols):
        pivot = next((r for r in range(len(pivots), len(mat)) if mat[r][col]), None)
        if pivot is None:
            continue
        row = len(pivots)
        mat[row], mat[pivot] = mat[pivot], mat[row]
        scale = mat[row][col]
        mat[row] = [v / scale for v in mat[row]]
        for r in range(len(mat)):
            if r != row and mat[r][col]:
                scale = mat[r][col]
                mat[r] = [v - scale * w for v, w in zip(mat[r], mat[row])]
        pivots.append(col)
    if any(not any(row[:-1]) and row[-1] for row in mat):
        return None
    if len(pivots) != ncols:
        return None
    out = [Q(0)] * ncols
    for r, col in enumerate(pivots):
        out[col] = mat[r][-1]
    return out


def tree_dp(domains, bags, edges, local_functions, local_tests):
    neighbors = [[] for _ in bags]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    tables = []
    for bag, fun, test in zip(bags, local_functions, local_tests):
        table = {}
        for row in product(*(domains[i] for i in bag)):
            point = dict(zip(bag, row))
            if test(point):
                table[row] = fun(point)
        tables.append(table)
    messages, choices = {}, {}

    def separator(a, b):
        return tuple(i for i in bags[a] if i in bags[b])

    def row_cost(a, row, excluded=None):
        point = dict(zip(bags[a], row))
        value = tables[a][row]
        for b in neighbors[a]:
            if b == excluded:
                continue
            incoming = message(b, a)
            key = tuple(point[i] for i in separator(b, a))
            if key not in incoming:
                return None
            value += incoming[key]
        return value

    def message(a, b):
        if (a, b) not in messages:
            values, best = {}, {}
            sep = separator(a, b)
            for row in tables[a]:
                value = row_cost(a, row, b)
                if value is None:
                    continue
                point = dict(zip(bags[a], row))
                key = tuple(point[i] for i in sep)
                if key not in values or value < values[key]:
                    values[key], best[key] = value, row
            messages[a, b], choices[a, b] = values, best
        return messages[a, b]

    beliefs = [{row: row_cost(a, row) for row in table}
               for a, table in enumerate(tables)]
    beliefs = [{row: value for row, value in table.items() if value is not None}
               for table in beliefs]
    if not beliefs[0]:
        return None
    root_row = min(beliefs[0], key=beliefs[0].get)
    value = beliefs[0][root_row]
    point = {}

    def recover(a, row, parent=None):
        local_point = dict(zip(bags[a], row))
        for i, v in local_point.items():
            assert i not in point or point[i] == v
            point[i] = v
        for b in neighbors[a]:
            if b != parent:
                key = tuple(local_point[i] for i in separator(b, a))
                recover(b, choices[b, a][key], a)

    recover(0, root_row)
    marginals = {}
    repeated_comparisons = 0
    for a, bag in enumerate(bags):
        for k, i in enumerate(bag):
            local_marginal = {}
            for row, cost in beliefs[a].items():
                t = row[k]
                if t not in local_marginal or cost < local_marginal[t]:
                    local_marginal[t] = cost
            if i in marginals:
                assert marginals[i] == local_marginal
                repeated_comparisons += len(local_marginal)
            marginals[i] = local_marginal
    return value, point, marginals, sum(map(len, tables)), repeated_comparisons


def uniform_domain(lo, hi, mesh):
    assert (lo / mesh).denominator == (hi / mesh).denominator == 1
    return [mesh * k for k in range(int(lo / mesh), int(hi / mesh) + 1)]


def filter_domains(domains, marginals, upper, error, continuous):
    result, removals = [], 0
    for i, nodes in enumerate(domains):
        good = {v for v, cost in marginals[i].items() if cost - error <= upper}
        if i in continuous:
            kept = [(a, b) for a, b in zip(nodes, nodes[1:]) if a in good or b in good]
            if len(nodes) == 1:
                assert nodes[0] in good
                result.append((nodes[0], nodes[0]))
            else:
                assert kept
                result.append((kept[0][0], kept[-1][1]))
                removals += len(nodes) - 1 - len(kept)
        else:
            labels = [v for v in nodes if v in good]
            assert labels
            result.append(labels)
            removals += len(nodes) - len(labels)
    return result, removals


def network_case(quartic):
    target = [Q(1, 5), Q(2, 5), Q(3, 5), Q(2, 5), Q(1)] if quartic else [Q(2, 5), Q(3, 5), Q(1), Q(0), Q(1)]
    if quartic:
        fun0 = lambda x: sum((x[i] - target[i]) ** 2 for i in (0, 1, 2))
        fun1 = lambda x: (x[3] - target[3]) ** 2 - (x[3] - target[3]) ** 4 + 2 * (1 - x[4])
        L, growth = Q(2), Q(16, 25)
    else:
        fun0 = lambda x: (x[0] - target[0]) ** 2 + (x[1] - target[1]) ** 2 + (x[2] - 1) ** 2 / 10
        fun1 = lambda x: 2 * x[3] - x[3] ** 2 + 2 * (1 - x[4])
        L, growth = Q(2), Q(1, 10)
    objective = lambda x: fun0(x) + fun1(x)
    bags, edges = [(0, 1, 2), (2, 3, 4)], [(0, 1)]
    tests = [lambda x: x[0] + x[1] == x[2], lambda x: x[2] + x[3] == x[4]]
    state = [(Q(0), Q(1))] * 4 + [[Q(0), Q(1)]]
    upper, records = None, []
    marginal_checks = witness_checks = removals = 0
    for j in range(9):
        h = Q(1, 2**j)
        domains = [uniform_domain(*state[i], h) if i < 4 else list(state[i]) for i in range(5)]
        result = tree_dp(domains, bags, edges, [fun0, fun1], tests)
        assert result is not None
        value, point, marginals, table_rows, repeated = result
        assert objective(point) == value
        upper = value if upper is None else min(upper, value)
        assert upper == value
        error = 4 * L * h * h / 8
        assert value - error <= 0 <= upper <= error
        expected = {i: {} for i in range(5)}
        brute_value = None
        for x0, x1, z in product(domains[0], domains[1], domains[4]):
            x2, x3 = x0 + x1, z - x0 - x1
            if x2 not in domains[2] or x3 not in domains[3]:
                continue
            candidate = dict(enumerate((x0, x1, x2, x3, z)))
            cost = objective(candidate)
            assert cost >= growth * sum((candidate[i] - target[i]) ** 2 for i in range(5))
            brute_value = cost if brute_value is None else min(brute_value, cost)
            for i, t in candidate.items():
                if t not in expected[i] or cost < expected[i][t]:
                    expected[i][t] = cost
            witness_checks += 1
        assert value == brute_value and marginals == expected
        marginal_checks += sum(map(len, expected.values())) + repeated
        state, deleted = filter_domains(domains, marginals, upper, error, set(range(4)))
        removals += deleted
        for i in range(4):
            lo, hi = state[i]
            assert lo <= target[i] <= hi
            # Squared form of width <= 2 r_j + 2 h, avoiding irrational math.
            assert max(Q(0), hi - lo - 2 * h) ** 2 <= 4 * error * 2 / growth
        assert target[4] in state[4]
        records.append({"level": j, "largest_coordinate_grid": max(map(len, domains)),
                        "feasible_bag_rows": table_rows, "lower": str(value - error),
                        "upper": str(upper), "binary_labels": [int(z) for z in state[4]]})
    return {"objective": "quartic" if quartic else "quadratic", "levels": records,
            "exact_min_marginal_checks": marginal_checks,
            "feasible_growth_witness_checks": witness_checks, "removed_states_or_cells": removals}


def rounding_checks():
    count, atoms = 0, 0
    for denominator in (3, 5, 7):
        for a in range(denominator + 1):
            for b in range(denominator - a + 1):
                x = [Q(a, denominator), Q(b, denominator), Q(a+b, denominator), Q(denominator-a-b, denominator)]
                h = Q(1, 4)
                intervals = []
                for value in x:
                    k = value // h
                    intervals.append([value] if value / h == k else [k*h, (k+1)*h])
                corners = [v for v in product(*intervals) if v[0] + v[1] == v[2] and v[2]+v[3] == 1]
                mixture = None
                for size in range(1, min(3, len(corners)) + 1):
                    for selection in combinations(corners, size):
                        rows = [[Q(1)] * size] + [[v[i] for v in selection] for i in range(4)]
                        weights = solve_linear(rows, [Q(1)] + x, size)
                        if weights is not None and min(weights) >= 0:
                            mixture = list(zip(weights, selection))
                            break
                    if mixture is not None:
                        break
                assert mixture is not None
                assert sum(w for w, _ in mixture) == 1
                assert all(sum(w*v[i] for w, v in mixture) == x[i] for i in range(4))
                variance = sum(w * sum((v[i]-x[i])**2 for i in range(4)) for w, v in mixture)
                assert variance <= h*h
                count += 1
                atoms += len(mixture)
    # Native z=0 has only the zero feasible flow; rounding preserves it.
    zero_corners = [v for v in product((Q(0), Q(1, 4)), repeat=4)
                    if v[0]+v[1] == v[2] and v[2]+v[3] == 0]
    assert zero_corners == [(Q(0), Q(0), Q(0), Q(0))]
    # Correct full-Hessian error is positive when all diagonal curvatures vanish.
    h = Q(1, 4)
    assert (Q(1, 2) * (2*h*h) - 2*(h/2)**2) == h*h/2
    # Unequal grids break feasible-corner coverage on x_0=x_1.
    assert not [(a, b) for a in (Q(0), Q(1, 2)) for b in (Q(1, 3), Q(1)) if a == b]
    assert all((Q(1, 3) * 2**j).denominator != 1 for j in range(20))
    return {"feasible_mean_preserving_distributions": count, "rounding_atoms": atoms,
            "structural_counterchecks": 3}


def tangent_curvature_checks():
    # x_0+x_1=x_2 has a two-dimensional equality tangent.
    normal = [Q(1), Q(1), Q(-1)]
    projector = [[Q(int(i == j)) - normal[i]*normal[j]/3 for j in range(3)] for i in range(3)]
    base_hessian = [[Q(2 if i == 0 else 4 if i == 1 else -2) if i == j else Q(0)
                     for j in range(3)] for i in range(3)]

    def multiply(left, right):
        return [[sum(left[i][k]*right[k][j] for k in range(3))
                 for j in range(3)] for i in range(3)]

    projected = multiply(multiply(projector, base_hessian), projector)
    curvature = max(sum(abs(v) for v in row) for row in projected)
    assert multiply(projector, projector) == projector
    checks = 0
    for rho in (Q(0), Q(1), Q(10**80)):
        hessian = [[base_hessian[i][j]+2*rho*normal[i]*normal[j]
                    for j in range(3)] for i in range(3)]
        assert multiply(multiply(projector, hessian), projector) == projected
        for a, b in product(range(-2, 3), repeat=2):
            direction = [Q(a), Q(b), Q(a+b)]
            form = sum(direction[i]*hessian[i][j]*direction[j] for i in range(3) for j in range(3))
            assert form <= curvature * sum(v*v for v in direction)
            checks += 1
    return {"projected_hessian_cases": 3, "exact_tangent_direction_checks": checks,
            "common_curvature_bound": str(curvature), "largest_penalty": str(10**80)}


def exact_quadratic_recovery():
    # A continuous unit-capacity conservation equation with non-dyadic optimum.
    fun = lambda x: (3*x[0]-1)**2 + (3*x[1]-2)**2
    test = lambda x: x[0]+x[1] == 1
    R, V = 72**4, (72**4)**2
    state = [(Q(0), Q(1)), (Q(0), Q(1))]
    max_grid = 0
    for j in range(100):
        h = Q(1, 2**j)
        domains = [uniform_domain(*bounds, h) for bounds in state]
        max_grid = max(max_grid, *(len(grid) for grid in domains))
        result = tree_dp(domains, [(0, 1)], [], [fun], [test])
        assert result is not None
        upper, _, marginals, _, _ = result
        error = Q(2*18, 8) * h*h
        lower = upper - error
        assert lower <= 0 <= upper
        state, _ = filter_domains(domains, marginals, upper, error, {0, 1})
        if error < Q(1, 4*V*V) and all(hi-lo < Q(1, 4*R*R) for lo, hi in state):
            value = ((lower+upper)/2).limit_denominator(V)
            candidate = {i: ((lo+hi)/2).limit_denominator(R) for i, (lo, hi) in enumerate(state)}
            assert lower <= value <= upper
            assert all(lo <= candidate[i] <= hi for i, (lo, hi) in enumerate(state))
            assert test(candidate) and fun(candidate) == value == 0
            assert candidate == {0: Q(1, 3), 1: Q(2, 3)}
            return {"levels": j+1, "largest_coordinate_grid": max_grid,
                    "height_bound": R, "optimizer": [str(candidate[i]) for i in range(2)],
                    "objective": str(value), "exact_original_feasibility": True}
    raise AssertionError("Exact recovery did not finish within its explicit limit")


def common_unit_checks():
    unit = Q(10**40)
    objective = lambda x: (3*x[0]/unit-1)**2 + (3*x[1]/unit-2)**2
    feasible = lambda x: x[0]+x[1] == unit
    state = [(Q(0), unit), (Q(0), unit)]
    largest = 0
    for j in range(8):
        mesh = unit / 2**j
        domains = [uniform_domain(*bounds, mesh) for bounds in state]
        largest = max(largest, *(len(nodes) for nodes in domains))
        result = tree_dp(domains, [(0, 1)], [], [objective], [feasible])
        assert result is not None
        upper, point, marginals, _, _ = result
        error = Q(2*18, 8) * mesh*mesh / (unit*unit)
        assert feasible(point) and upper-error <= 0 <= upper
        state, _ = filter_domains(domains, marginals, upper, error, {0, 1})
        assert state[0][0] <= unit/3 <= state[0][1]
        assert state[1][0] <= 2*unit/3 <= state[1][1]
    return {"levels": 8, "physical_capacity": str(unit), "initial_mesh": str(unit),
            "largest_coordinate_grid": largest}


def main():
    started = perf_counter()
    results = {"scope": "finite exact diagnostics; no production-solver performance claim",
               "rounding": rounding_checks(),
               "tangent_curvature": tangent_curvature_checks(),
               "network_cases": [network_case(False), network_case(True)],
               "exact_quadratic_recovery": exact_quadratic_recovery(),
               "common_unit_alignment": common_unit_checks()}
    results["elapsed_seconds"] = round(perf_counter() - started, 6)
    destination = Path(__file__).with_name("tu-filtered-grid-results.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
