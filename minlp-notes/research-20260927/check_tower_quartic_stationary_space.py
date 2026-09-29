"""Exact local and finite tower first-jet checks; no numerical roots."""

from itertools import combinations_with_replacement
from math import comb

import sympy as sp

from check_tower_quadratic_vanishing_space import reduced_evaluation, sparse_rank


def check_local_blocks():
    b = sp.symbols("b")
    monomials = [m for d in range(4) for m in combinations_with_replacement(range(3), d)]
    expected = [5, 5 * b, -5 * b, -5 * b, -5 * b]
    for residue in range(5):
        columns = [m for m in monomials if sum(i + 1 for i in m) % 5 == residue]
        assert len(columns) == 4
        matrix = sp.zeros(4)
        for column, monomial in enumerate(columns):
            quotient, remainder = divmod(sum(i + 1 for i in monomial), 5)
            assert remainder == residue
            matrix[0, column] = b**quotient
            for index in set(monomial):
                derivative = list(monomial)
                derivative.remove(index)
                quotient, remainder = divmod(sum(i + 1 for i in derivative), 5)
                assert remainder == (residue - index - 1) % 5
                matrix[index + 1, column] = monomial.count(index) * b**quotient
        assert sp.expand(matrix.det() - expected[residue]) == 0
    print("PASS: five symbolic first-jet determinants 5, 5b, -5b, -5b, -5b")


def first_jet_kernel_dimension(k, maximum_degree):
    columns = []
    for degree in range(maximum_degree + 1):
        for monomial in combinations_with_replacement(range(3 * k), degree):
            remainder, factor = reduced_evaluation(monomial, k)
            column = {(-1, remainder): factor}
            for index in set(monomial):
                derivative = list(monomial)
                derivative.remove(index)
                remainder, factor = reduced_evaluation(derivative, k)
                column[(index, remainder)] = monomial.count(index) * factor
            columns.append(column)
    return len(columns) - sparse_rank(columns)


def main():
    check_local_blocks()
    for k in range(1, 6):
        cubic = first_jet_kernel_dimension(k, 3)
        quartic = first_jet_kernel_dimension(k, 4)
        assert cubic == 0
        assert quartic == comb(5 * k + 1, 2)
        print(f"PASS: k={k}, stationary cubic dimension={cubic}, quartic dimension={quartic}")


if __name__ == "__main__":
    main()
