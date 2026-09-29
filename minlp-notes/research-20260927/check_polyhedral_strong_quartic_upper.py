"""Exact boundary-case checks for the active-support oracle argument.

This does not implement PosSLP or prove the complexity classification.
"""

import sympy as sp


x, y = sp.symbols("x y")
variables = sp.Matrix([x, y])
objective = (x - 1)**2 + y*y + y**4
gradient = sp.Matrix([sp.diff(objective, x), sp.diff(objective, y)])


def parameterize(rows, right):
    if not rows.rows:
        return sp.zeros(2, 1), sp.eye(2)
    assert rows.rank() == rows.rows
    pivots = list(rows.rref()[1])
    free = [j for j in range(2) if j not in pivots]
    B = rows[:, pivots]
    N = rows[:, free]
    base = sp.zeros(2, 1)
    Z = sp.zeros(2, len(free))
    restricted_base = B.inv() * right
    restricted_linear = -B.inv() * N
    for i, j in enumerate(pivots):
        base[j] = restricted_base[i]
        for ell in range(len(free)):
            Z[j, ell] = restricted_linear[i, ell]
    for ell, j in enumerate(free):
        Z[j, ell] = 1
    assert rows * base == right
    assert rows * Z == sp.zeros(rows.rows, len(free))
    assert Z.T*Z - sp.eye(len(free)) == restricted_linear.T*restricted_linear
    return base, Z


def verify(A, b, support, candidate):
    selected = A[list(support), :] if support else sp.zeros(0, 2)
    rhs = b[list(support), :] if support else sp.zeros(0, 1)
    if selected.rank() != len(support):
        return False
    _, Z = parameterize(selected, rhs)
    assert selected*candidate == rhs
    grad = gradient.subs(dict(zip(variables, candidate)))
    assert Z.T*grad == sp.zeros(Z.cols, 1), "candidate must be its affine restriction's minimizer"
    multipliers = -(selected*selected.T).inv()*selected*grad if support else sp.zeros(0, 1)
    primal = all(value >= 0 for value in b - A*candidate)
    dual = all(value >= 0 for value in multipliers)
    stationarity = grad + selected.T*multipliers == sp.zeros(2, 1)
    return primal and dual and stationarity


def main():
    # This polyhedron has y=0, so strict feasibility of all inequalities fails.
    # Its optimal point (0,0) has redundant and zero-multiplier active rows.
    A = sp.Matrix([[1, 0], [2, 0], [0, 1], [0, -1], [1, 0], [-1, 0]])
    b = sp.Matrix([0, 0, 0, 0, 1, 1])
    assert verify(A, b, (0,), sp.Matrix([0, 0]))
    assert verify(A, b, (1,), sp.Matrix([0, 0]))
    assert not verify(A, b, (0, 1), sp.Matrix([0, 0]))
    assert not verify(A, b, (), sp.Matrix([1, 0]))
    assert not verify(A, b, (2,), sp.Matrix([1, 0]))
    assert verify(A, b, (0, 2), sp.Matrix([0, 0]))  # zero-dimensional restriction

    # A feasible restriction minimizer can have the wrong multiplier sign.
    A2 = sp.Matrix([[1, 0], [0, 1], [0, -1]])
    b2 = sp.Matrix([2, 0, 0])
    assert not verify(A2, b2, (0,), sp.Matrix([2, 0]))
    assert verify(A2, b2, (), sp.Matrix([1, 0]))

    # The free-coordinate construction preserves mu even for a skew basis.
    base, Z = parameterize(sp.Matrix([[2, -5]]), sp.Matrix([7]))
    t = sp.symbols("t")
    restricted = sp.expand(objective.subs({x: base[0] + Z[0]*t, y: base[1] + Z[1]*t}))
    assert sp.expand(sp.diff(restricted, t, 2) - 2*(Z.T*Z)[0] - 12*t*t) == 0
    assert (Z.T*Z)[0] >= 1

    # A radial strongly convex quartic still has complex critical components.
    radial = (x*x + y*y)**2 + x*x + y*y
    for variable in (x, y):
        assert sp.expand(sp.diff(radial, variable) - 2*variable*(1 + 2*x*x + 2*y*y)) == 0
    print("PASS: lower-dimensional and redundant faces, empty/zero-dimensional supports, primal rejection, dual-sign rejection, preserved curvature, complex critical component")


if __name__ == "__main__":
    main()
