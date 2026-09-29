"""Finite exact tests of VI violator locality and every-basis rank bounds.

All maps here are nonsymmetric strongly monotone affine maps in three
variables. Every full polyhedron contains zero, so every subset is feasible.
This does not implement Clarkson sampling or prove its runtime.
"""

from itertools import combinations

import sympy as sp


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        for chosen in combinations(items, size):
            yield frozenset(chosen)


def solve_vi(rows, rhs, matrix, target, selected):
    n = matrix.rows
    for support in subsets(selected):
        indices = sorted(support)
        if not indices:
            point = target
            multipliers = sp.zeros(0, 1)
        else:
            active = sp.Matrix([rows[i] for i in indices])
            if active.rank() != len(indices):
                continue
            system = matrix.row_join(active.T).col_join(
                active.row_join(sp.zeros(len(indices)))
            )
            vector = (matrix * target).col_join(sp.Matrix([rhs[i] for i in indices]))
            solution = system.inv() * vector
            point = solution[:n, :]
            multipliers = solution[n:, :]
        if any(value < 0 for value in multipliers):
            continue
        if any(sp.Matrix([rows[i]]).dot(point) > rhs[i] for i in selected):
            continue
        return tuple(point)
    raise AssertionError("No support passed on a known feasible subset")


matrix = sp.Matrix([[2, 1, 0], [-1, 2, 1], [0, -1, 2]])
assert matrix + matrix.T == 4 * sp.eye(3)
assert matrix != matrix.T
cases = [
    (
        "rank one in three variables",
        [(1, 0, 0), (2, 0, 0), (-1, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0)],
        [0, 0, 1, 1, 0, 1],
        sp.Matrix([2, 1, -1]),
        1,
    ),
    (
        "rank two in three variables",
        [(1, 0, 0), (0, 1, 0), (1, 1, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 0)],
        [0, 0, 1, 1, 1, 0],
        sp.Matrix([1, 2, -1]),
        2,
    ),
]

total_locality = total_bases = 0
for name, rows, rhs, target, rank in cases:
    assert sp.Matrix(rows).rank() == rank
    assert all(value >= 0 for value in rhs)  # zero satisfies the full system
    ground = frozenset(range(len(rows)))
    all_sets = list(subsets(ground))
    points = {selected: solve_vi(rows, rhs, matrix, target, selected) for selected in all_sets}
    violators = {
        selected: frozenset(i for i in ground
                            if sp.Matrix([rows[i]]).dot(sp.Matrix(points[selected])) > rhs[i])
        for selected in all_sets
    }
    locality = 0
    for larger in all_sets:
        assert not larger & violators[larger]
        for smaller in subsets(larger):
            if not larger & violators[smaller]:
                assert points[larger] == points[smaller]
                assert violators[larger] == violators[smaller]
                locality += 1
    bases = [selected for selected in all_sets
             if all(violators[proper] != violators[selected]
                    for proper in subsets(selected) if proper != selected)]
    assert all(len(basis) <= rank for basis in bases)
    assert max(map(len, bases)) == rank
    for selected in all_sets:
        determining = [basis for basis in bases
                       if basis <= selected and violators[basis] == violators[selected]]
        assert determining
        assert all(points[basis] == points[selected] for basis in determining)
    for basis in bases:
        if violators[basis] == violators[ground]:
            assert points[basis] == points[ground]
    print(f"PASS {name}: {len(all_sets)} subsets, {locality} locality implications, "
          f"{len(bases)} bases, maximum basis size {rank}")
    total_locality += locality
    total_bases += len(bases)

print(f"PASS {total_locality} exact locality implications and {total_bases} minimal bases")
