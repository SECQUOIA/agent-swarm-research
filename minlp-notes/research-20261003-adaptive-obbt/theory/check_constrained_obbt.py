#!/usr/bin/env python3
"""Exact, dependency-free checks of the certificates in constrained-obbt.md."""

from fractions import Fraction as Q


def rational(value):
    if not isinstance(value, (int, Q)):
        raise ValueError("certificate data must be integers or Fractions")
    return Q(value)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), Q(0))


def solve(matrix, rhs):
    """Solve a nonsingular square rational system by exact elimination."""
    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("basis must be square")
    work = [[Q(x) for x in row] + [Q(value)]
            for row, value in zip(matrix, rhs, strict=True)]
    for col in range(n):
        pivot = next((j for j in range(col, n) if work[j][col]), None)
        if pivot is None:
            raise ValueError("singular basis")
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for row in range(n):
            if row != col:
                scale = work[row][col]
                work[row] = [x - scale * y
                             for x, y in zip(work[row], work[col], strict=True)]
    return [row[-1] for row in work]


def verify_basis_cell(A, b, E, c, basis, vertices):
    """Verify one affine-RHS basis on the convex hull of parameter vertices.

    Coverage by several proposed cells is a separate proof obligation.
    Return the primal affine map, its dual, and its exact affine value.
    """
    if not vertices:
        raise ValueError("a bounded proposed cell needs vertices")
    A = [[rational(x) for x in row] for row in A]
    b = [rational(x) for x in b]
    E = [[rational(x) for x in row] for row in E]
    c = [rational(x) for x in c]
    vertices = [[rational(x) for x in vertex] for vertex in vertices]
    if not A or not E or not c:
        raise ValueError("LP must have rows and a nonempty objective")
    n, k, m = len(c), len(E[0]), len(A)
    if len(basis) != n or len(set(basis)) != n:
        raise ValueError("invalid basis indices")
    if any(not isinstance(i, int) or not 0 <= i < m for i in basis):
        raise ValueError("basis index outside the row range")
    if len(b) != m or len(E) != m or any(len(r) != n for r in A):
        raise ValueError("invalid LP dimensions")
    if any(len(r) != k for r in E) or any(len(v) != k for v in vertices):
        raise ValueError("invalid parameter dimensions")
    AI = [A[i] for i in basis]
    primal0 = solve(AI, [b[i] for i in basis])
    columns = [solve(AI, [E[i][j] for i in basis]) for j in range(k)]
    dual_basis = solve(list(zip(*AI, strict=True)), c)
    if any(y < 0 for y in dual_basis):
        raise ValueError("dual multiplier is negative")
    dual = [Q(0)] * m
    for i, y in zip(basis, dual_basis, strict=True):
        dual[i] = y
    if any(dot([A[i][j] for i in range(m)], dual) != c[j]
           for j in range(n)):
        raise ValueError("dual equality failed")
    for theta in vertices:
        z = [primal0[j] + sum((columns[t][j] * theta[t] for t in range(k)), Q(0))
             for j in range(n)]
        rhs = [b[i] + dot(E[i], theta) for i in range(m)]
        if any(dot(row, z) > value for row, value in zip(A, rhs, strict=True)):
            raise ValueError("proposed cell exceeds the basis feasibility region")
        if dot(c, z) != dot(dual, rhs):
            raise ValueError("primal-dual equality failed")
    return primal0, columns, dual, (dot(c, primal0), [dot(c, col) for col in columns])


def expect_rejection(callback):
    try:
        callback()
    except ValueError:
        return
    raise AssertionError("invalid certificate was accepted")


def check_cutoff_cells():
    # Columns are x,y. Row 7 is the objective cutoff y <= U.
    A = [[-1, 0], [0, -1], [1, 0], [0, 1], [1, -1], [4, -1], [1, 0], [0, 1]]
    b = list(map(Q, [0, 0, 3, 4, 1, 7])) + [Q(5, 2), Q(0)]
    E = [[Q(0)] for _ in A]
    E[7] = [Q(1)]
    c = [Q(1), Q(0)]
    cells = [(Q(0), Q(1), [4, 7], Q(1), Q(1)),
             (Q(1), Q(3), [5, 7], Q(7, 4), Q(1, 4)),
             (Q(3), Q(4), [6, 7], Q(5, 2), Q(0))]
    # Exact interval coverage of [0,4], including shared boundaries.
    assert cells[0][0] == 0 and cells[-1][1] == 4
    assert all(left[1] == right[0] for left, right in zip(cells, cells[1:]))
    for lo, hi, basis, intercept, slope in cells:
        _, _, dual, affine = verify_basis_cell(A, b, E, c, basis, [[lo], [hi]])
        assert affine == (intercept, [slope])
        assert dual[7] == slope
        # A stored dual remains an upper envelope at all interval endpoints,
        # including outside its own primal feasibility interval.
        for U in [Q(0), Q(1, 2), Q(1), Q(2), Q(3), Q(4)]:
            h = min(1 + U, Q(7, 4) + U / 4, Q(5, 2))
            assert h <= intercept + slope * U
    expect_rejection(lambda: verify_basis_cell(A, b, E, c, [6, 7], [[Q(2)], [Q(4)]]))
    expect_rejection(lambda: verify_basis_cell(A, b, E, c, [0, 7], [[Q(0)], [Q(1)]]))
    expect_rejection(lambda: verify_basis_cell(A, b, E, c, [2, 6], [[Q(0)], [Q(1)]]))
    # Floating residual arithmetic used to accept (1,1) despite the last row
    # requiring 10^16+1 <= 10^16. Exact input enforcement prevents that claim.
    expect_rejection(lambda: verify_basis_cell(
        [[1, 0], [0, 1], [1e16, 1]], [1, 1, 10**16], [[0], [0], [0]],
        [1, 0], [0, 1], [[0]]))
    expect_rejection(lambda: verify_basis_cell(
        [[1, 0], [0, 1], [10**16, 1]], [1, 1, 10**16], [[0], [0], [0]],
        [1, 0], [0, 1], [[0]]))
    witness = [Q(5, 2), Q(3)]
    assert all(dot(row, witness) <= value for row, value in zip(A[:-1], b[:-1], strict=True))
    assert witness[1] == 3
    assert min(Q(3), Q(9, 4), Q(5, 2)) == Q(9, 4)
    assert Q(7, 4) + Q(1, 2) / 4 == Q(15, 8)
    assert min(Q(3, 2), Q(15, 8), Q(5, 2)) == Q(3, 2)
    print("PASS cutoff basis cells, exact coverage, dual envelopes, and retained witness")
    print("PASS rejection of infeasible cells, negative multipliers, singular bases, and float data")


def check_contraction_cells():
    # Rows: x>=0, x<=r, normalized tangent 1, normalized tangent 2.
    A = [[Q(-1)], [Q(1)], [Q(1)], [Q(1)]]
    b = [Q(0), Q(0), Q(0), Q(3, 8)]
    E = [[Q(0)], [Q(1)], [Q(1, 4)], [Q(1, 16)]]
    low = verify_basis_cell(A, b, E, [Q(1)], [2], [[Q(0)], [Q(2)]])
    high = verify_basis_cell(A, b, E, [Q(1)], [3], [[Q(2)], [Q(8)]])
    assert low[3] == (Q(0), [Q(1, 4)])
    assert high[3] == (Q(3, 8), [Q(1, 16)])
    assert max(abs(low[3][1][0]), abs(high[3][1][0])) == Q(1, 4)
    r = Q(8)
    trajectory = [r]
    for _ in range(3):
        r = min(r / 4, r / 16 + Q(3, 8))
        trajectory.append(r)
    assert trajectory == [Q(8), Q(7, 8), Q(7, 32), Q(7, 128)]
    assert trajectory[1] / trajectory[0] < trajectory[2] / trajectory[1]
    # The certified M=1/4 residual-tail bound at r1 exceeds the true remainder r1.
    residual = trajectory[0] - trajectory[1]
    assert Q(1, 4) * residual / (1 - Q(1, 4)) >= trajectory[1]
    print("PASS changing active tangent, uniform derivative bound, and exact trajectory")


def check_equality_example():
    # Use Q(sqrt(2)) as rational pairs a+b*sqrt(2); no numerical roots.
    def add(x, y):
        return (x[0] + y[0], x[1] + y[1])

    def mul(x, y):
        return (x[0] * y[0] + 2 * x[1] * y[1],
                x[0] * y[1] + x[1] * y[0])

    q = (Q(-1), Q(1))
    polynomial = add(add(mul((Q(2), Q(0)), mul(q, q)),
                         mul((Q(4), Q(0)), q)), (Q(-2), Q(0)))
    assert polynomial == (0, 0)
    # Rational isolation identifies sqrt(2)-1 as the nonnegative root.
    def polynomial_at(t):
        return 2 * t * t + 4 * t - 2

    assert polynomial_at(Q(2, 5)) < 0 < polynomial_at(Q(5, 12))
    for r in [Q(1, 4), Q(1), Q(3, 2)]:
        # At diagonal endpoints the unconstrained relaxation is exactly zero.
        assert r * r + r * r - 2 * r * r + 2 * r * abs(r - r) == 0
        U = 4 * r * r
        # The positive-cutoff fixed-point equation is exact at U=4r^2.
        assert 2 * r * r + 4 * r * r - 2 * r * r == U
    print("PASS equality-induced rate in Q(sqrt(2)) and exact positive-cutoff floor")


def check_indistinguishable_histories():
    for N in [2, 8, 32]:
        a, delta, q = Q(1, 2), Q(1, 2 * N), Q(1, 4)
        b = a - delta

        def stall(s):
            return min(s, max(b, s - delta))

        def shrink(s):
            if s <= b:
                return q * s
            if s <= a:
                return q * b + (b - q * b) * (s - b) / (a - b)
            return s - delta

        # Exact affine-piece endpoint checks establish monotonicity and F<=id.
        for function in [stall, shrink]:
            nodes = sorted(set([Q(0), b, a, Q(1)]))
            values = [function(s) for s in nodes]
            assert all(0 <= v <= s for s, v in zip(nodes, values, strict=True))
            assert values == sorted(values)
        left = right = Q(1)
        for _ in range(N + 1):
            left, right = stall(left), shrink(right)
            assert left == right
        assert left == b
        assert stall(left) == b and shrink(right) == q * b
    print("PASS identical finite histories with incompatible eventual outcomes")


def check_nonlinear_repair():
    a, b, kappa, L, mu = Q(1, 64), Q(1, 4), Q(1), Q(165, 256), Q(63, 64)
    q_squared = 4 * (a + L * kappa * b) / mu
    assert q_squared == Q(181, 252) < Q(7, 8)**2
    assert Q(7, 8) + 2 * kappa * b * Q(1, 8) == Q(15, 16)
    assert (2 + Q(1, 16)) * (Q(1, 4) + Q(1, 16)) == L
    assert 1 - Q(1, 4) / 16 == mu
    # Coefficients of the global identity 1/4-s(1-s)=(s-1/2)^2.
    assert [Q(1, 4), Q(-1), Q(1)] == [Q(-1, 2)**2, 2 * Q(-1, 2), Q(1)]
    count = 0
    for ell in [Q(-1, 4), Q(-1, 32), Q(0)]:
        for upper in [Q(0), Q(1, 32), Q(1, 4)]:
            for v in [Q(0), Q(1, 4096), Q(1, 16)]:
                width = max(upper - ell, v)
                for x in [ell, (ell + upper) / 2, upper]:
                    secant = (ell + upper) * x - ell * upper
                    assert secant - x*x == (upper - x) * (x - ell)
                    assert secant - x*x <= (upper - ell)**2 / 4
                    if x*x > min(v, secant):
                        continue
                    for y in [x*x, (x*x + min(v, secant))/2, min(v, secant)]:
                        envelope = min(upper*y, ell*y + v*x - ell*v)
                        assert 0 <= envelope - x*y <= (upper - ell)*v/4
                        f = x*x + y*y - x*y/16
                        phi = x*x + y*y - envelope/16
                        repaired_f = x*x + x**4 - x**3/16
                        residual = y - x*x
                        assert 0 <= x*x <= y <= v
                        assert residual <= b * width**2
                        assert phi >= f - a * width**2
                        assert repaired_f <= f + L * residual
                        assert repaired_f >= mu * max(abs(x), x*x)**2
                        count += 1
    print(f"PASS nonlinear graph repair constants and {count} exact boundary/interior checks")


if __name__ == "__main__":
    check_cutoff_cells()
    check_contraction_cells()
    check_equality_example()
    check_nonlinear_repair()
    check_indistinguishable_histories()
    print("All constrained OBBT certificate checks passed (exact rational arithmetic).")
