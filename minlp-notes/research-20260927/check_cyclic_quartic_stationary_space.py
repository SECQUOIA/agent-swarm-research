"""Exact low-degree spaces at the cyclic algebraic singleton.

Ranks are over QQ. Evaluation splits by powers of a, a**d=2.
No floating-point field arithmetic or sample algebraic approximations occur.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations_with_replacement


def monomials(n, degree):
    result = []
    for k in range(degree + 1):
        for indices in combinations_with_replacement(range(n), k):
            exponent = [0] * n
            for j in indices:
                exponent[j] += 1
            result.append(tuple(exponent))
    return result


def rank_sparse(columns):
    pivots = {}
    for column in columns:
        v = {i: Fraction(c) for i, c in column.items() if c}
        while v:
            pivot = min(v)
            if pivot not in pivots:
                scale = v[pivot]
                pivots[pivot] = {i: c / scale for i, c in v.items()}
                break
            scale = v[pivot]
            for i, c in pivots[pivot].items():
                value = v.get(i, Fraction(0)) - scale * c
                if value:
                    v[i] = value
                elif i in v:
                    del v[i]
    return len(pivots)


def analyze(n):
    degree = (2**(n+1)-(-1)**(n+1))//3
    powers = [((-2)**i-1)//3 for i in range(1, n+1)]

    def evaluation(exponent):
        quotient, remainder = divmod(sum(i*j for i, j in zip(exponent, powers)), degree)
        return remainder, Fraction(2)**quotient

    monos2 = monomials(n, 2)
    buckets2 = defaultdict(list)
    for e in monos2:
        residue, coefficient = evaluation(e)
        buckets2[residue].append((e, coefficient))
    quadratics = []
    for bucket in buckets2.values():
        base, coefficient = bucket[0]
        for exponent, value in bucket[1:]:
            quadratics.append({exponent: Fraction(1), base: -value/coefficient})

    monos4 = monomials(n, 4)
    buckets4 = defaultdict(list)
    for e in monos4:
        residue, _ = evaluation(e)
        buckets4[residue].append(e)
    # Multiply derivative equation j by p_j. Each monomial then has
    # evaluation coefficient e_j times its ordinary evaluation value.
    # Nonzero column scalings do not change each residue block's rank.
    stationary_dimension = sum(
        len(bucket) - rank_sparse([
            {0: 1, **{j+1: e[j] for j in range(n) if e[j]}}
            for e in bucket
        ]) for bucket in buckets4.values()
    )

    product_columns = defaultdict(list)
    for i, left in enumerate(quadratics):
        for right in quadratics[i:]:
            product = defaultdict(Fraction)
            for e, ec in left.items():
                for f, fc in right.items():
                    product[tuple(a+b for a, b in zip(e, f))] += ec*fc
            product = {e: c for e, c in product.items() if c}
            if product:
                residues = {evaluation(e)[0] for e in product}
                assert len(residues) == 1
                product_columns[next(iter(residues))].append(product)
    product_dimension = sum(rank_sparse(columns) for columns in product_columns.values())
    assert product_dimension <= stationary_dimension
    return n, degree, len(quadratics), product_dimension, stationary_dimension


if __name__ == "__main__":
    print("n, field degree, dim I2, dim I2-products, stationary quartic dimension")
    for n in range(2, 17):
        print(*analyze(n), sep=", ", flush=True)
