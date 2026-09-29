"""Exact, topic-specific checks for the quintic tower's quadratic space.

Uses only integer and rational arithmetic. Finite checks support, but do not
replace, the uniform proofs in tower-quadratic-vanishing-space.md.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations_with_replacement
from math import comb


def add(*polynomials):
    result = defaultdict(int)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] += coefficient
    return {m: c for m, c in result.items() if c}


def scale(polynomial, coefficient):
    return {m: coefficient * c for m, c in polynomial.items() if coefficient * c}


def multiply(left, right):
    result = defaultdict(int)
    for m, a in left.items():
        for n, b in right.items():
            result[tuple(sorted(m + n))] += a * b
    return {m: c for m, c in result.items() if c}


def variable(index):
    return {(index,): 1}


def tower_relations(k):
    relations = []
    for gate in range(k):
        x, y, z = (variable(3 * gate + offset) for offset in range(3))
        b = {(): 2} if gate == 0 else variable(3 * (gate - 1))
        r1 = add(multiply(x, x), scale(y, -1))
        r2 = add(multiply(x, y), scale(z, -1))
        r3 = add(multiply(y, z), scale(b, -1))
        extra_r = add(multiply(y, y), scale(multiply(x, z), -1))
        extra_s = add(multiply(z, z), scale(multiply(b, x), -1))
        assert extra_r == add(multiply(x, r2), scale(multiply(y, r1), -1))
        assert extra_s == add(multiply(x, r3), scale(multiply(z, r2), -1))
        relations.extend((r1, r2, extra_r, r3, extra_s))
    return relations


def sparse_rank(rows):
    """Ordinary exact row elimination; uses no proposed pivot pattern."""
    pivots = {}
    for original in rows:
        row = {key: Fraction(value) for key, value in original.items() if value}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                coefficient = row[pivot]
                pivots[pivot] = {key: value / coefficient for key, value in row.items()}
                break
            factor = row[pivot]
            for key, value in pivots[pivot].items():
                new_value = row.get(key, 0) - factor * value
                if new_value:
                    row[key] = new_value
                else:
                    row.pop(key, None)
    return len(pivots)


def reduced_evaluation(monomial, k):
    exponent = sum((index % 3 + 1) * 5 ** (k - index // 3 - 1) for index in monomial)
    quotient, remainder = divmod(exponent, 5**k)
    return remainder, 2**quotient


def check_tower(k):
    monomials = [()]
    monomials.extend((index,) for index in range(3 * k))
    monomials.extend(combinations_with_replacement(range(3 * k), 2))
    assert len(monomials) == comb(3 * k + 2, 2)
    evaluations = {monomial: reduced_evaluation(monomial, k) for monomial in monomials}
    rank = len({remainder for remainder, _ in evaluations.values()})
    assert len(monomials) - rank == 5 * k
    relations = tower_relations(k)
    for relation in relations:
        evaluation = defaultdict(int)
        for monomial, coefficient in relation.items():
            remainder, factor = evaluations[monomial]
            evaluation[remainder] += coefficient * factor
        assert all(value == 0 for value in evaluation.values())
    assert sparse_rank(relations) == 5 * k
    if k >= 2:
        # A genuine size-three collision, including the wrap-around factor.
        assert evaluations[(0,)] == evaluations[(4, 5)]
        remainder, factor = evaluations[(0,)]
        assert evaluations[(2, 2)] == (remainder, 2 * factor)
    return rank


def local_product_determinant():
    x, y, z = (variable(index) for index in range(3))
    local = [multiply(x, x), multiply(x, y),
             add(multiply(y, y), scale(multiply(x, z), -1)),
             multiply(y, z), multiply(z, z)]
    monomials = list(combinations_with_replacement(range(3), 4))
    products = [multiply(a, b) for a, b in combinations_with_replacement(local, 2)]
    matrix = [[Fraction(product.get(m, 0)) for m in monomials] for product in products]
    determinant = Fraction(1)
    for column in range(15):
        pivot = next(row for row in range(column, 15) if matrix[row][column])
        if pivot != column:
            matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
            determinant *= -1
        coefficient = matrix[column][column]
        determinant *= coefficient
        for row in range(column + 1, 15):
            factor = matrix[row][column] / coefficient
            for j in range(column, 15):
                matrix[row][j] -= factor * matrix[column][j]
    assert abs(determinant) == 1
    return determinant


def main():
    cases = list(range(1, 33)) + [64, 100]
    for k in cases:
        check_tower(k)
    print(f"PASS: exact evaluation ranks, rational basis ranks, and affine identities for {len(cases)} cases k=1..32,64,100")
    print(f"PASS: local 15-product determinant = {local_product_determinant()}")
    for k in range(1, 13):
        relations = tower_relations(k)
        products = [multiply(a, b) for a, b in combinations_with_replacement(relations, 2)]
        assert sparse_rank(products) == comb(5 * k + 1, 2)
    print("PASS: full tower pair-product ranks for k=1..12")


if __name__ == "__main__":
    main()
