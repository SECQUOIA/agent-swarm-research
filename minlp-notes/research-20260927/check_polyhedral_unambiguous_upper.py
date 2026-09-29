"""Exact finite checks for the unique-mask and LP sign-transfer arguments.

This does not implement PosSLP, GLS LP, or the algebraic separation bound.
It enumerates small rational polytopes, where every cost and vertex is exact.
"""

from itertools import combinations, product

import sympy as sp


def rows_basis(rows):
    chosen = []
    for i, row in enumerate(rows):
        old_rank = sp.Matrix([rows[j] for j in chosen]).rank() if chosen else 0
        if sp.Matrix([rows[j] for j in chosen] + [row]).rank() > old_rank:
            chosen.append(i)
    return chosen


def vertices(rows, rhs):
    dimension = len(rows[0])
    found = set()
    for indices in combinations(range(len(rows)), dimension):
        matrix = sp.Matrix([rows[i] for i in indices])
        if matrix.det() == 0:
            continue
        point = matrix.inv() * sp.Matrix([rhs[i] for i in indices])
        if all(sp.Matrix([row]).dot(point) <= value for row, value in zip(rows, rhs)):
            found.add(tuple(point))
    assert found
    return sorted(found)


def tangent_polytope(rows, selected):
    constraints = [rows[i] for i in selected] + [(1, 0), (-1, 0), (0, 1), (0, -1)]
    rhs = [0] * len(selected) + [1] * 4
    return constraints, rhs, vertices(constraints, rhs)


cases = [
    (
        "redundant normals and zero rows",
        [(1, 0), (2, 0), (0, 1), (0, -1), (0, 0), (0, 0)],
        [0, 0, 0, 0, 0, 1],
        (1, 0),
        (0, 0),
    ),
    (
        "zero gradient on a proper affine space",
        [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)],
        [0, 0, 1, 1, 0],
        (0, 0),
        (0, 0),
    ),
    (
        "skew affine space",
        [(1, 2), (2, 4), (-1, -2), (1, 0), (0, 1)],
        [-1, -2, 1, 1, 1],
        (0, 0),
        (sp.Rational(-1, 5), sp.Rational(-2, 5)),
    ),
    (
        "vertex optimum",
        [(1, 0), (0, 1), (-1, 0), (0, -1)],
        [1, 1, 0, 0],
        (2, 2),
        (1, 1),
    ),
    (
        "empty active set",
        [(1, 0), (-1, 0), (0, 1), (0, -1)],
        [1, 1, 1, 1],
        (0, 0),
        (0, 0),
    ),
    (
        "triangle corner",
        [(-1, 0), (0, -1), (1, 1)],
        [0, 0, 1],
        (2, 0),
        (1, 0),
    ),
]

mask_count = recovery_count = transfer_count = 0
for name, rows, rhs, target_tuple, expected in cases:
    target = sp.Matrix(target_tuple)
    accepted = []
    for mask in product((False, True), repeat=len(rows)):
        mask_count += 1
        selected = [i for i, bit in enumerate(mask) if bit]
        local_basis = rows_basis([rows[i] for i in selected])
        basis = [selected[j] for j in local_basis]
        if basis:
            matrix = sp.Matrix([rows[i] for i in basis])
            point = target - matrix.T * (matrix * matrix.T).inv() * (
                matrix * target - sp.Matrix([rhs[i] for i in basis])
            )
        else:
            point = target
        slacks = [value - sp.Matrix([row]).dot(point) for row, value in zip(rows, rhs)]
        if any(slack != 0 if bit else slack <= 0 for slack, bit in zip(slacks, mask)):
            continue
        gradient = 2 * (point - target)
        _, _, candidates = tangent_polytope(rows, selected)
        if min(gradient.dot(sp.Matrix(v)) for v in candidates) < 0:
            continue
        accepted.append((selected, tuple(point)))
    assert len(accepted) == 1, (name, accepted)
    selected, point = accepted[0]
    assert point == expected, (name, point, expected)

    constraints, bounds, candidates = tangent_polytope(rows, selected)
    # Recover every enumerated vertex solely from all its active rows.
    for v in candidates:
        active = [i for i, (row, value) in enumerate(zip(constraints, bounds))
                  if sp.Matrix([row]).dot(sp.Matrix(v)) == value]
        basis_indices = rows_basis([constraints[i] for i in active])
        assert len(basis_indices) == 2
        basis = [active[j] for j in basis_indices]
        recovered = sp.Matrix([constraints[i] for i in basis]).inv() * sp.Matrix(
            [bounds[i] for i in basis]
        )
        assert tuple(recovered) == v
        recovery_count += 1

    # Uniform perturbation error below gamma/8 preserves whether the
    # approximate LP's optimal vertex has negative true cost. Test every tie.
    for cost_tuple in product((-3, -1, 0, 1, 3), repeat=2):
        cost = sp.Matrix(cost_tuple)
        values = {v: cost.dot(sp.Matrix(v)) for v in candidates}
        nonzero = [abs(value) for value in values.values() if value]
        gamma = min(nonzero) if nonzero else sp.Integer(1)
        for signs in product((-1, 0, 1), repeat=2):
            approximate = cost + sp.Matrix(signs) * gamma / 32
            approx_values = {v: approximate.dot(sp.Matrix(v)) for v in candidates}
            assert all(abs(approx_values[v] - values[v]) <= gamma / 16 for v in candidates)
            approx_min = min(approx_values.values())
            for v in candidates:
                if approx_values[v] == approx_min:
                    assert (values[v] < 0) == (min(values.values()) < 0)
                    transfer_count += 1
    print(f"PASS {name}: unique mask {selected}, minimizer {point}")

print(f"PASS {mask_count} masks, {recovery_count} vertex recoveries, "
      f"{transfer_count} optimal-vertex sign checks including ties")
