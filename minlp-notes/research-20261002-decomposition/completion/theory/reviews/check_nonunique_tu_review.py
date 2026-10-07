"""Independent exact checks of union filtration and omitted integer labels.

This is a small mathematical diagnostic, not a general TU solver. It uses
exhaustive feasible grid assignments rather than the author's tree DP.
"""

from fractions import Fraction as Q
from itertools import product
from math import isqrt

import sympy as sp


def nodes(domain, mesh):
    result = set()
    for lower, upper in domain:
        assert (lower / mesh).denominator == (upper / mesh).denominator == 1
        result.update(lower + i * mesh for i in range(int((upper - lower) / mesh) + 1))
    return sorted(result)


def merge(intervals):
    result = []
    for lower, upper in sorted(intervals):
        if result and lower <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], upper))
        else:
            result.append((lower, upper))
    return result


def contains(domain, value):
    return any(lower <= value <= upper for lower, upper in domain)


def check_union_filtration():
    # Continuous x,t,z, with the TU equality x+t=z. The exact global set is
    # {(0,0,0), (1/2,1/2,1)}. Checking feasible pairs avoids enumerating a
    # cubic Cartesian product; it does not alter the finite minimum.
    optima = [(Q(0), Q(0), Q(0)), (Q(1, 2), Q(1, 2), Q(1))]
    projections = [sorted({s[i] for s in optima}) for i in range(3)]
    domains = [[(Q(0), Q(1))] for _ in range(3)]
    previous_incumbent = None
    largest_states = 0
    disconnected_levels = 0
    witnesses_checked = 0
    # L=12, g=1/6, n_c=3. The theorem's next-grid upper bound is 70.
    square = 4 * 3 * 72
    ceil_root = isqrt(square) + (isqrt(square) ** 2 != square)
    state_bound = 2 * (5 + ceil_root)
    assert state_bound == 70
    for level in range(9):
        mesh = Q(1, 2**level)
        grids = [nodes(domain, mesh) for domain in domains]
        largest_states = max(largest_states, *(len(grid) for grid in grids))
        marginals = [{value: None for value in grid} for grid in grids]
        values = {}
        for x, t in product(grids[0], grids[1]):
            z = x + t
            if z not in marginals[2]:
                continue
            point = (x, t, z)
            objective = (2 * x - z) ** 2 + z * (1 - z) / 4
            values[point] = objective
            for i, value in enumerate(point):
                old = marginals[i][value]
                if old is None or objective < old:
                    marginals[i][value] = objective
        assert values
        if previous_incumbent is not None:
            assert previous_incumbent in values
        incumbent = min(values, key=values.get)
        upper = values[incumbent]
        error = Q(3 * 12, 8) * mesh**2
        assert upper - error <= 0 <= upper <= error
        retained = []
        for i, domain in enumerate(domains):
            passing = {
                value for value, objective in marginals[i].items()
                if objective is not None and objective <= upper + error
            }
            for value in passing:
                # This is the projection distance bound before adding a cell.
                distance = min(abs(value - s) for s in projections[i])
                assert distance**2 <= 54 * mesh**2
                witnesses_checked += 1
            intervals = []
            for lower, end in domain:
                if lower == end:
                    if lower in passing:
                        intervals.append((lower, end))
                    continue
                for index in range(int((end - lower) / mesh)):
                    start = lower + index * mesh
                    stop = start + mesh
                    if start in passing or stop in passing:
                        intervals.append((start, stop))
            retained.append(merge(intervals))
        for optimum in optima:
            assert all(contains(retained[i], optimum[i]) for i in range(3))
        assert all(contains(retained[i], incumbent[i]) for i in range(3))
        assert all(len(nodes(domain, mesh / 2)) <= state_bound for domain in retained)
        if len(retained[2]) > 1:
            disconnected_levels += 1
            assert not contains(retained[2], Q(1, 2))
        domains = retained
        previous_incumbent = incumbent
    assert disconnected_levels >= 4
    # A hull still has 2^8+1 states on the last mesh in the z coordinate.
    assert largest_states < 257
    return largest_states, disconnected_levels, witnesses_checked


def check_missing_integer_labels():
    # Integer z is allowed only in {0,2}. Both allowed slices have optimum 1;
    # optimizing over the analysis interval [0,2] instead would give zero.
    z, x, t, multiplier, integer_multiplier = sp.symbols("z x t lam mu")
    variables = sp.Matrix([z, x, t])
    hessian = sp.diag(2, 2, 0)
    linear = sp.Matrix([-2, -sp.Rational(2, 3), 0])
    objective = (z - 1)**2 + (x - sp.Rational(1, 3))**2
    assert objective.subs({z: 1, x: sp.Rational(1, 3)}) == 0
    solutions_checked = 0
    for allowed_label in (0, 2):
        # The equality normal x+t=1 and the integer-fixing normal suffice.
        normal = sp.Matrix([0, 1, 1]) * multiplier
        normal += sp.Matrix([1, 0, 0]) * integer_multiplier
        equations = list(hessian * variables + linear - normal)
        equations.extend([x + t - 1, z - allowed_label])
        solutions = sp.solve(equations, [z, x, t, multiplier, integer_multiplier], dict=True)
        assert len(solutions) == 1
        solution = solutions[0]
        assert solution[z] in (0, 2)
        assert solution[x] == sp.Rational(1, 3)
        assert solution[t] == sp.Rational(2, 3)
        assert objective.subs(solution) == 1
        solutions_checked += 1
    return solutions_checked


if __name__ == "__main__":
    states, split_levels, witnesses = check_union_filtration()
    recovered = check_missing_integer_labels()
    print(f"PASS: 9 exact union-grid levels, {states} maximum coordinate states, "
          f"{split_levels} disconnected levels, {witnesses} passing projection checks; "
          f"{recovered} recovered slices with omitted integer labels.")
