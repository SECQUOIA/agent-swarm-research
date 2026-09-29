"""Exact small checks for the conditional degree-23 residual obstruction."""

from itertools import combinations_with_replacement, product

import sympy as sp


def monomial_exponents(variable_count, degree):
    for indices in combinations_with_replacement(range(variable_count), degree):
        exponents = [0] * variable_count
        for index in indices:
            exponents[index] += 1
        yield tuple(exponents)


def evaluation_matrix(points, degree):
    return sp.Matrix(
        [
            [sp.prod(c**e for c, e in zip(point, exponent))
             for exponent in monomial_exponents(len(point), degree)]
            for point in points
        ]
    )


def main():
    cube = [(1, *signs, 0, 0) for signs in product((-1, 1), repeat=3)]
    extra = (0, 0, 0, 0, 1, 0)
    residual = [*cube, extra]
    cube_hilbert = [evaluation_matrix(cube, d).rank() for d in range(6)]
    residual_hilbert = [evaluation_matrix(residual, d).rank() for d in range(6)]
    assert cube_hilbert == [1, 4, 7, 8, 8, 8]
    assert residual_hilbert == [1, 5, 8, 9, 9, 9]
    residual_h = [residual_hilbert[0]] + [
        residual_hilbert[i] - residual_hilbert[i - 1] for i in range(1, 6)
    ]
    assert residual_h == [1, 4, 3, 1, 0, 0]
    linked_h = [int(sp.binomial(5, i)) - residual_h[5 - i] for i in range(6)]
    assert linked_h == [1, 5, 9, 7, 1, 0]
    assert sum(linked_h) == 23

    dependence = evaluation_matrix(residual, 2).T.nullspace()
    assert len(dependence) == 1
    assert dependence[0][-1] == 0
    assert all(c != 0 for c in dependence[0][:-1])
    assert [point[4] ** 2 for point in residual] == [0] * 8 + [1]

    feasible = [(length, v) for length in range(1, 10) for v in range(1, 10)
                if 2 * v <= length <= 2 ** (v - 1)]
    assert feasible == [(8, 4)]

    # A basis for B = Q[t3,t4,t5]/(t3^2,t4^2,t5^2) is indexed by masks.
    # beta(a,b) is the t3*t4*t5 coefficient of a*b, induced by q=t1*t2.
    masks = list(range(8))
    gram = sp.Matrix([[int((i & j) == 0 and (i | j) == 7)
                       for j in masks] for i in masks])
    assert gram.det() != 0
    linear_indices = [0, 1, 2, 4]
    assert gram.extract(linear_indices, linear_indices) == sp.zeros(4)
    # Multiplication by q in the full 32-dimensional square-zero algebra.
    multiplier = sp.zeros(32)
    for mask in range(32):
        if mask & 3 == 0:
            multiplier[mask | 3, mask] = 1
    assert multiplier.rank() == 8

    print("Residual Hilbert function:", residual_hilbert)
    print("Linked h-vector:", linked_h, "degree", sum(linked_h))
    print("Quadratic relation: support exactly the eight cube points")
    print("Lengths at most nine allowed by both inequalities:", feasible)
    print("Nonreduced pairing: rank 8, isotropic linear dimension 4")


if __name__ == "__main__":
    main()
