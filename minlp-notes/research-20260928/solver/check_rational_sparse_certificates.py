"""Targeted exact checks for rational-sparse-certificates.md.

These finite rational checks support, but do not replace, the general proof.
They do not implement or test an ellipsoid SDP solver.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial, lcm


def monomials(k, degree):
    return sorted(
        (a for a in product(range(degree + 1), repeat=k) if sum(a) <= degree),
        key=lambda a: (sum(a), a),
    )


def subsets(indices):
    return [s for size in range(len(indices) + 1) for s in combinations(indices, size)]


def add_term(poly, exponent, coefficient):
    poly[exponent] += coefficient
    if not poly[exponent]:
        del poly[exponent]


def weighted_monomial(alpha, generators):
    result = defaultdict(F)
    for chosen in subsets(generators):
        exponent = list(alpha)
        for i in chosen:
            exponent[i] += 2
        add_term(result, tuple(exponent), F((-1) ** len(chosen)))
    return dict(result)


def source_terms(alpha, generators):
    terms = [(generators, alpha)]
    for i, power in enumerate(alpha):
        for j in range(power):
            beta = alpha[:i] + (j,) + (0,) * (len(alpha) - i - 1)
            terms.append(((i,), beta))
    for q, i in enumerate(generators):
        beta = list(alpha)
        beta[i] += 1
        terms.append((generators[:q], tuple(beta)))
    return terms


def block_indices(k, r):
    return [
        (generators, monomials(k, r - len(generators)))
        for generators in subsets(tuple(range(k)))
        if len(generators) <= r
    ]


def diagonal_constant(k, r, ordinary=False):
    values = defaultdict(int)
    sources = 0
    for generators, basis in block_indices(k, r):
        if ordinary and len(generators) > 1:
            continue
        for alpha in basis:
            sources += 1
            terms = source_terms(alpha, generators)
            assert len(terms) == 1 + sum(alpha) + len(generators)
            assert len(set(terms)) == len(terms)
            expansion = defaultdict(F)
            for target_generators, beta in terms:
                assert sum(beta) + len(target_generators) <= r
                assert not ordinary or len(target_generators) <= 1
                values[target_generators, beta] += 1
                for exp, value in weighted_monomial(tuple(2 * a for a in beta), target_generators).items():
                    add_term(expansion, exp, value)
            assert dict(expansion) == {(0,) * k: F(1)}
    assert min(values.values()) == 1
    assert max(values.values()) <= sources
    assert sum(values.values()) <= sources * (r + 1)
    return sources, values


def uniform_moment(alpha, generators):
    value = F(1)
    for i, a in enumerate(alpha):
        if a % 2:
            return F(0)
        value *= F(2, (a + 1) * (a + 3)) if i in generators else F(1, a + 1)
    return value


def is_psd(matrix):
    remaining = [list(row) for row in matrix]
    while remaining:
        if any(remaining[i][i] < 0 for i in range(len(remaining))):
            return False
        pivot = next((i for i in range(len(remaining)) if remaining[i][i] > 0), None)
        if pivot is None:
            return all(value == 0 for row in remaining for value in row)
        rest = [i for i in range(len(remaining)) if i != pivot]
        diagonal = remaining[pivot][pivot]
        remaining = [
            [remaining[i][j] - remaining[i][pivot] * remaining[pivot][j] / diagonal for j in rest]
            for i in rest
        ]
    return True


def global_exponent(local, bag, n):
    result = [0] * n
    for i, a in zip(bag, local):
        result[i] = a
    return tuple(result)


def coefficient_map(blocks, matrices, n):
    result = defaultdict(F)
    for (bag, generators, basis), matrix in zip(blocks, matrices):
        for i, alpha in enumerate(basis):
            for j, beta in enumerate(basis):
                if not matrix[i][j]:
                    continue
                exponent = tuple(a + b for a, b in zip(alpha, beta))
                for local, value in weighted_monomial(exponent, generators).items():
                    add_term(result, global_exponent(local, bag, n), value * matrix[i][j])
    return dict(result)


def subtract_poly(first, second):
    result = defaultdict(F, first)
    for exponent, value in second.items():
        add_term(result, exponent, -value)
    return dict(result)


def zero_matrices(blocks):
    return [[[F(0) for _ in basis] for _ in basis] for _, _, basis in blocks]


def correction(blocks, poly, n, r):
    matrices = zero_matrices(blocks)
    for exponent, coefficient in poly.items():
        support = {i for i, a in enumerate(exponent) if a}
        block_index = next(i for i, (bag, generators, _) in enumerate(blocks) if not generators and support <= set(bag))
        bag, _, basis = blocks[block_index]
        local = tuple(exponent[i] for i in bag)
        alpha = []
        capacity = r
        for a in local:
            chosen = min(a, capacity)
            alpha.append(chosen)
            capacity -= chosen
        beta = tuple(a - b for a, b in zip(local, alpha))
        i, j = basis.index(tuple(alpha)), basis.index(beta)
        if i == j:
            matrices[block_index][i][j] += coefficient
        else:
            matrices[block_index][i][j] += coefficient / 2
            matrices[block_index][j][i] += coefficient / 2
    assert coefficient_map(blocks, matrices, n) == poly
    return matrices


def main():
    identities = 0
    for k in range(1, 4):
        for r in range(5):
            count, _ = diagonal_constant(k, r)
            identities += count

    ordinary_identities = 0
    for k in range(1, 5):
        for r in range(1, 4):
            count, _ = diagonal_constant(k, r, ordinary=True)
            ordinary_identities += count

    moment_blocks = 0
    for k, r in [(1, 3), (2, 2), (3, 2)]:
        specs = block_indices(k, r)
        largest = max(len(basis) for _, basis in specs)
        q0 = factorial(2 * r + 3) ** (2 * k)
        bound = F(1, q0**largest * largest ** (largest - 1))
        for generators, basis in specs:
            matrix = [[uniform_moment(tuple(a + b for a, b in zip(alpha, beta)), generators) for beta in basis] for alpha in basis]
            assert all((q0 * value).denominator == 1 for row in matrix for value in row)
            shifted = [[value - (bound if i == j else 0) for j, value in enumerate(row)] for i, row in enumerate(matrix)]
            assert is_psd(shifted)
            moment_blocks += 1

    n, r, w = 3, 2, 2
    bags = [(0, 1), (1, 2)]
    blocks = [(bag, generators, basis) for bag in bags for generators, basis in block_indices(len(bag), r)]
    D = sum(len(basis) for _, _, basis in blocks)
    V = sum(len(basis) * (len(basis) + 1) // 2 for _, _, basis in blocks)
    H = zero_matrices(blocks)
    for index, (bag, generators, basis) in enumerate(blocks):
        _, counts = diagonal_constant(len(bag), r)
        for i, alpha in enumerate(basis):
            H[index][i][i] = F(counts[generators, alpha], D)
    assert coefficient_map(blocks, H, n) == {(0,) * n: F(1)}
    tau = F(1, 7)
    eta = tau / D
    witness = [[[tau * value for value in row] for row in matrix] for matrix in H]
    for index, (_, generators, basis) in enumerate(blocks):
        if generators:
            continue
        vector = [F(1, 3) if sum(alpha) == 0 else F((-1) ** i, i + 5) if sum(alpha) == 1 else F(0) for i, alpha in enumerate(basis)]
        for i in range(len(basis)):
            for j in range(len(basis)):
                witness[index][i][j] += vector[i] * vector[j]
    p = coefficient_map(blocks, witness, n)
    h = F(1)
    while h > eta / (2 ** (w + 3) * V):
        h /= 2
    rounded = [[[round(value / h) * h for value in row] for row in matrix] for matrix in witness]
    residual = subtract_poly(p, coefficient_map(blocks, rounded, n))
    repair = correction(blocks, residual, n, r)
    exact = [[[value + repair[b][i][j] for j, value in enumerate(row)] for i, row in enumerate(matrix)] for b, matrix in enumerate(rounded)]
    assert coefficient_map(blocks, exact, n) == p
    assert all(is_psd([[value - (eta / 2 if i == j else 0) for j, value in enumerate(row)] for i, row in enumerate(matrix)]) for matrix in exact)

    all_monomials = {global_exponent(alpha, bag, n) for bag in bags for alpha in monomials(len(bag), 2 * r)}
    for exponent in all_monomials:
        correction(blocks, {exponent: F(1)}, n, r)

    # Off-diagonal correction divides an input coefficient by two, including
    # when its denominator has more powers of two than the rounding grid.
    B, input_denominator = 3, 2**10
    repaired_entry = F(1, input_denominator) / 2
    assert lcm(2 ** (B + 1), input_denominator) % repaired_entry.denominator != 0
    assert 2 * lcm(2**B, input_denominator) % repaired_entry.denominator == 0

    print(f"PASS: {identities} exact telescoping identities; {moment_blocks} rational moment lower-bound checks.")
    print(f"PASS: {ordinary_identities} exact telescoping identities restricted to ordinary quadratic-module blocks.")
    print(f"PASS: all {len(all_monomials)} global monomial right-inverse checks for two overlapping bags.")
    print(f"PASS: exact rational rounding/correction identity and PSD margins (D={D}, V={V}, dyadic denominator={h.denominator}).")
    print("PASS: corrected denominator bound handles input denominators with larger powers of two than the rounding grid.")
    print("Limits: finite examples only; no ellipsoid implementation, complexity benchmark, Lean proof, or project-wide checks.")


if __name__ == "__main__":
    main()
