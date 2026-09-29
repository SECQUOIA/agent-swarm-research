"""Independent exact checks for the rational sparse certificate review.

Finite regression checks only: this does not verify the general theorem or
implement the ellipsoid algorithm.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial, lcm


def monomials(n, r):
    return [a for a in product(range(r + 1), repeat=n) if sum(a) <= r]


def add_poly(target, source, scale=F(1)):
    for exponent, coefficient in source.items():
        target[exponent] += scale * coefficient
        if target[exponent] == 0:
            del target[exponent]


def term(n, alpha, subset):
    answer = defaultdict(F)
    for flags in product((0, 1), repeat=len(subset)):
        exponent = list(alpha)
        for index, flag in zip(subset, flags):
            exponent[index] += 2 * flag
        answer[tuple(exponent)] += (-1) ** sum(flags)
    return answer


def local_blocks(n, r):
    return {
        subset: monomials(n, r - len(subset))
        for size in range(n + 1)
        for subset in combinations(range(n), size)
    }


def identity_terms(n, alpha, subset):
    terms = [(alpha, subset)]
    for i in range(n):
        for j in range(alpha[i]):
            terms.append((alpha[:i] + (j,) + (0,) * (n - i - 1), (i,)))
    for position, i in enumerate(subset):
        exponent = list(alpha)
        exponent[i] += 1
        terms.append((tuple(exponent), subset[:position]))
    return terms


def positive_definite(matrix):
    """Exact LDL pivots, suitable here because all tested matrices are PD."""
    residual = [row[:] for row in matrix]
    for i in range(len(residual)):
        pivot = residual[i][i]
        if pivot <= 0:
            return False
        for j in range(i + 1, len(residual)):
            for k in range(i + 1, len(residual)):
                residual[j][k] -= residual[j][i] * residual[i][k] / pivot
    return True


def uniform_moment(exponent, subset):
    answer = F(1)
    for i, a in enumerate(exponent):
        if a % 2:
            return F(0)
        answer *= F(2, (a + 1) * (a + 3)) if i in subset else F(1, a + 1)
    return answer


identity_count = 0
ordinary_count = 0
moment_count = 0
for n in range(1, 4):
    for r in range(n, 5):
        blocks = local_blocks(n, r)
        dimension = sum(map(len, blocks.values()))
        diagonal = defaultdict(int)
        for subset, basis in blocks.items():
            for alpha in basis:
                certificate = defaultdict(F)
                entries = identity_terms(n, alpha, subset)
                assert len(entries) == 1 + sum(alpha) + len(subset) <= r + 1
                for exponent, generator in entries:
                    assert exponent in blocks[generator]
                    diagonal[generator, exponent] += 1
                    add_poly(certificate, term(n, tuple(2 * x for x in exponent), generator))
                assert certificate == {(0,) * n: F(1)}
                identity_count += 1
        assert all(diagonal[subset, alpha] >= 1 for subset, basis in blocks.items() for alpha in basis)
        assert sum(diagonal.values()) <= dimension * (r + 1)

        ordinary = {subset: basis for subset, basis in blocks.items() if len(subset) <= 1}
        ordinary_diagonal = defaultdict(int)
        for subset, basis in ordinary.items():
            for alpha in basis:
                certificate = defaultdict(F)
                for exponent, generator in identity_terms(n, alpha, subset):
                    assert generator in ordinary and exponent in ordinary[generator]
                    ordinary_diagonal[generator, exponent] += 1
                    add_poly(certificate, term(n, tuple(2 * x for x in exponent), generator))
                assert certificate == {(0,) * n: F(1)}
                ordinary_count += 1
        ordinary_dimension = sum(map(len, ordinary.values()))
        assert all(ordinary_diagonal[subset, alpha] >= 1
                   for subset, basis in ordinary.items() for alpha in basis)
        assert sum(ordinary_diagonal.values()) <= ordinary_dimension * (r + 1)

        # A smaller subset keeps exact elimination quick while checking every
        # generator type and both parity-zero and nonzero moment entries.
        if r == n:
            largest = max(map(len, blocks.values()))
            q0 = factorial(2 * r + 3) ** (2 * n)
            lower = F(1, q0 ** largest * largest ** (largest - 1))
            for subset, basis in blocks.items():
                matrix = [[uniform_moment(tuple(x + y for x, y in zip(a, b)), subset)
                           for b in basis] for a in basis]
                assert all((q0 * entry).denominator == 1 for row in matrix for entry in row)
                assert positive_definite(matrix)
                for i in range(len(matrix)):
                    matrix[i][i] -= lower
                assert positive_definite(matrix)
                moment_count += 1


# Two overlapping bags, global coefficient collection, and round/correct.
bag_count = 0
for r in (2, 3):
    bags = ((0, 1), (1, 2))
    blocks = []
    for bag in bags:
        for subset, basis in local_blocks(len(bag), r).items():
            blocks.append((bag, subset, basis))
    dimension = sum(len(basis) for _, _, basis in blocks)
    variables = [(block, i, j) for block, (_, _, basis) in enumerate(blocks)
                 for i in range(len(basis)) for j in range(i, len(basis))]
    diagonal = defaultdict(int)
    for block, (bag, subset, basis) in enumerate(blocks):
        for alpha in basis:
            for exponent, generator in identity_terms(len(bag), alpha, subset):
                target = next(i for i, (b, s, _) in enumerate(blocks) if b == bag and s == generator)
                position = blocks[target][2].index(exponent)
                diagonal[target, position] += 1

    columns = []
    pivots = {}
    for coordinate, (block, i, j) in enumerate(variables):
        bag, subset, basis = blocks[block]
        local = term(len(bag), tuple(x + y for x, y in zip(basis[i], basis[j])), subset)
        column = defaultdict(F)
        for exponent, coefficient in local.items():
            global_exponent = [0] * 3
            for index, power in zip(bag, exponent):
                global_exponent[index] = power
            column[tuple(global_exponent)] += coefficient * (1 if i == j else 2)
        assert len(column) <= 2 ** len(bag)
        assert all(abs(c) <= 2 for c in column.values())
        columns.append(column)
        if not subset:
            exponent, coefficient = next(iter(column.items()))
            pivots.setdefault(exponent, (coordinate, coefficient))

    def coefficient_map(values):
        answer = defaultdict(F)
        for value, column in zip(values, columns):
            add_poly(answer, column, value)
        return answer

    assert set(pivots) == set().union(*(column.keys() for column in columns))
    assert len({position for position, _ in pivots.values()}) == len(pivots)
    tau = F(2, 7)
    eta = tau / dimension
    # Rank-one PSD terms plus the explicit full-interior constant certificate.
    exact = [F((i + 1) * (j + 1), 91) +
             (tau * diagonal[block, i] / dimension if i == j else 0)
             for block, i, j in variables]
    polynomial = coefficient_map(exact)
    bound = eta / (2 ** 5 * len(variables))
    h = F(1)
    while h > bound:
        h /= 2
    rounded = [h * (value // h) for value in exact]
    residual = polynomial.copy()
    add_poly(residual, coefficient_map(rounded), F(-1))
    for exponent, coefficient in residual.items():
        coordinate, scale = pivots[exponent]
        rounded[coordinate] += coefficient / scale
    assert coefficient_map(rounded) == polynomial
    for block, (_, _, basis) in enumerate(blocks):
        matrix = [[F(0) for _ in basis] for _ in basis]
        for coordinate, (owner, i, j) in enumerate(variables):
            if owner == block:
                matrix[i][j] = matrix[j][i] = rounded[coordinate]
        for i in range(len(matrix)):
            matrix[i][i] -= eta / 2
        assert positive_definite(matrix)
    bag_count += 1


# The original denominator sentence missed division by two at a pivot.
bits = 8
input_denominator = 2 ** 100
corrected_entry = F(1, 2 * input_denominator)
old_bound = lcm(2 ** (bits + 1), input_denominator)
new_bound = 2 * lcm(2 ** bits, input_denominator)
assert old_bound % corrected_entry.denominator != 0
assert new_bound % corrected_entry.denominator == 0

print(f"PASS: {identity_count} diagonal identities; {moment_count} exact moment bounds; "
      f"{bag_count} overlapping-bag round/correct certificates; denominator regression; "
      f"{ordinary_count} ordinary-module identities.")
