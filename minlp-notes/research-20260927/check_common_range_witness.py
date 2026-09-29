"""Exact stress checks for the rational-QP fiber recovery argument.

Enumerating low-dimensional active sets here is an independent verifier for
the examples, not the proposed polynomial-time QP implementation. These
checks do not verify algebraic genericity, KLL, or asymptotic complexity.
"""

from itertools import combinations
from math import isqrt

import sympy as sp


def nonnegative(value):
    value = sp.simplify(value)
    answer = value.is_nonnegative
    assert answer is not None, value
    return answer


def squared_norm(vector):
    return sp.expand(vector.dot(vector))


def project(matrix, rhs, center):
    """Certify a Euclidean projection by exact feasible KKT candidates."""
    candidates = []
    for size in range(matrix.cols + 1):
        for rows in combinations(range(matrix.rows), size):
            if not rows:
                point = center
            else:
                active = matrix[list(rows), :]
                gram = active * active.T
                if gram.det() == 0:
                    continue
                multipliers = gram.inv() * (active * center - rhs[list(rows), :])
                if not all(nonnegative(value) for value in multipliers):
                    continue
                point = center - active.T * multipliers
            if all(nonnegative(value) for value in rhs - matrix * point):
                candidates.append(point.applyfunc(sp.simplify))
    assert candidates
    first = candidates[0]
    assert all(point == first for point in candidates)
    return first


def main():
    matrix = sp.Matrix([[-1, 0], [0, -1], [-1, -1]])
    zero = sp.zeros(2, 1)
    radical = sp.sqrt(2)
    # These cases cover an inactive sum row, a corner optimum, and an
    # optimum in the relative interior of the sum facet.
    shifts = [0, sp.Rational(1, 2), 1, sp.Rational(5, 4),
              sp.Rational(3, 2), 2, 4]
    count = 0
    active_patterns = set()
    for shift in shifts:
        rhs = sp.Matrix([-radical, -1, -radical - shift])
        optimum = project(matrix, rhs, zero)
        assert nonnegative(25 - squared_norm(optimum))
        for bits in range(2, 15):
            scale = 2**bits
            error = sp.Rational(1, scale)
            lower_radical = sp.Rational(isqrt(2 * scale * scale), scale)
            outward_rhs = sp.Matrix([-lower_radical, -1, -lower_radical - shift])
            assert all(nonnegative(value) for value in outward_rhs - rhs)
            assert all(nonnegative(value) for value in rhs + sp.ones(3, 1) * error
                       - outward_rhs)

            relaxed = project(matrix, outward_rhs, zero)
            assert all(value.is_Rational for value in relaxed)
            assert nonnegative(squared_norm(optimum) - squared_norm(relaxed))
            repaired = project(matrix, rhs, relaxed)

            # H=4 is a conservative bound for this one fixed matrix.
            zeta = 4 * error
            assert nonnegative(zeta**2 - squared_norm(repaired - relaxed))
            excess = squared_norm(repaired) - squared_norm(optimum)
            assert nonnegative(excess - squared_norm(repaired - optimum))
            assert nonnegative(10 * zeta + zeta**2 - excess)
            active_patterns.add(tuple(i for i, residual in
                                      enumerate(outward_rhs - matrix * relaxed)
                                      if residual == 0))
            count += 1
    assert len(active_patterns) >= 3

    # The two-stage point is feasible but need not minimize the original
    # Euclidean norm: x2 >= (x1-2)^2 has projected u*=x1=0, then v*=4.
    canonical = sp.Matrix([0, 4])
    closer = sp.Matrix([1, 1])
    for point in [canonical, closer]:
        assert nonnegative(point[1] - (point[0] - 2)**2)
    assert squared_norm(closer) < squared_norm(canonical)

    # An affine fiber does not enlarge the nonlinear coordinate's field.
    # The opposite squared SOC bounds below force u=sqrt(2); v>=u+1
    # has minimum-norm solution v=1+sqrt(2).
    u, v = radical, 1 + radical
    assert 2 - u**2 == 0 and 2*u**2 - 4 == 0
    assert v - u - 1 == 0
    symbol = sp.Symbol("T")
    assert sp.minimal_polynomial(v, symbol) == symbol**2 - 2*symbol - 1
    print(f"PASS: {count} exact outward-QP cases; "
          f"{len(active_patterns)} active patterns; "
          "canonical-point distinction and unchanged quadratic field")


if __name__ == "__main__":
    main()
