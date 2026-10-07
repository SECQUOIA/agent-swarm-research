#!/usr/bin/env python3
"""Exact fallback fixtures for expected-smoothed-qp.md.

This exercises the existing exponential stationary-face oracle, not the
polynomial convex-QP algorithm or the expected-time theorem. The expected
values follow directly by completing a square or evaluating endpoints.
"""

from fractions import Fraction as Q

from check_negative_inertia_qp import FaceQP


def main():
    box = ((1, 0), (-1, 0), (0, 1), (0, -1))
    fixtures = (
        (
            "zero objective, continuum",
            ((0, 0), (0, 0)), (0, 0), box, (1, 0, 1, 0), Q(0),
        ),
        (
            "singular ambient Hessian, optimal edge",
            ((2, 0), (0, 0)), (-1, 0), box, (1, 0, 1, 0), Q(-1, 4),
        ),
        (
            "lower-dimensional segment, fractional unique optimum",
            ((2, 0), (0, -2)), (-1, 0), box, (1, 0, 0, 0), Q(-1, 4),
        ),
        (
            "concave endpoint tie",
            ((-2,),), (0,), ((1,), (-1,)), (1, 1), Q(-1),
        ),
        (
            "redundant equalities",
            ((0, 0), (0, 0)), (1, 0),
            ((1, 0), (-1, 0), (2, 0), (0, 1), (0, -1)),
            (Q(1, 3), Q(-1, 3), Q(2, 3), 1, 0), Q(1, 3),
        ),
    )
    for name, matrix, linear, constraints, rhs, expected in fixtures:
        matrix = tuple(tuple(map(Q, row)) for row in matrix)
        constraints = tuple(tuple(map(Q, row)) for row in constraints)
        linear = tuple(map(Q, linear))
        rhs = tuple(map(Q, rhs))
        oracle = FaceQP(matrix, constraints, rhs)
        value, point = oracle.solve(linear)
        assert isinstance(value, Q) and all(isinstance(x, Q) for x in point)
        assert value == expected, (name, value, expected)
        print(f"{name}: optimum={value}, witness={tuple(map(str, point))}")
    print("PASS: 5 exact-rational active-subset fallback fixtures")


if __name__ == "__main__":
    main()
