"""Exact bookkeeping check for the apex construction (note.md, Theorem 4.2).

Hahn-series monomials eps^a with a in Q^5 are tracked by exponent vectors.
The Bodirsky-Kummer-Thom functional enters only through symbols
f(2e_i + 2e_j); the check confirms that

  * every coefficient of q is one real number times one monomial eps^a,
  * L_f(q)(xi) = eps^{4 e_1} * sum_{i,j} H_ij f(2 e_i + 2 e_j),
  * the evaluation point xi has strictly positive exponents in the
    lexicographic order whose first coordinate dominates (so 0 < xi_k < 1),
  * q has positive square coefficients and only the monomials allowed by
    the complete graph K_4 (apex construction for a graph G uses the same
    formula with M supported on G + apex).

It also checks Horn copositivity on a fine rational grid of the simplex
(a sanity check only; copositivity of the Horn matrix is classical).
"""

from fractions import Fraction
from itertools import product

import sympy as sp

H = [[1, -1, 1, 1, -1],
     [-1, 1, -1, 1, 1],
     [1, -1, 1, -1, 1],
     [1, 1, -1, 1, -1],
     [-1, 1, 1, -1, 1]]


def e(i):
    return tuple(2 if j == i else 0 for j in range(5))  # 2 e_i


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def lex_positive(a):
    for x in a:
        if x != 0:
            return x > 0
    return False


def main():
    fsym = {}
    # q(x1..x4) = sum_{i,j} H_ij (eps^{2e_i} u_i)(eps^{2e_j} u_j),
    # u_0 = 1 (constant), u_k = x_k.  Index 0 of H is the constant.
    coeffs = {}  # monomial in x (exponent tuple of length 4) -> list of (real, eps exponent)
    for i in range(5):
        for j in range(5):
            mono = [0, 0, 0, 0]
            if i > 0:
                mono[i - 1] += 1
            if j > 0:
                mono[j - 1] += 1
            coeffs.setdefault(tuple(mono), []).append((H[i][j], add(e(i), e(j))))
    # each coefficient is a single eps-monomial (both orders of (i,j) give the same exponent)
    for mono, terms in coeffs.items():
        assert len({t[1] for t in terms}) == 1, mono
    # positive square coefficients
    for k in range(4):
        mono = tuple(2 if j == k else 0 for j in range(4))
        assert sum(t[0] for t in coeffs[mono]) == 1
    # evaluation point xi_k = eps^{2e_0 - 2e_k}
    xi = [add(e(0), neg(e(k))) for k in range(1, 5)]
    assert all(lex_positive(a) for a in xi)
    # L_f(q)(xi): coefficient eps^a gets factor f(a); then multiply by xi^mono
    total = {}
    for mono, terms in coeffs.items():
        for real, a in terms:
            expo = a
            for k in range(4):
                for _ in range(mono[k]):
                    expo = add(expo, xi[k])
            key = a
            fsym.setdefault(key, sp.Symbol('f_' + '_'.join(map(str, key))))
            total.setdefault(expo, 0)
            total[expo] += real * fsym[key]
    assert list(total) == [tuple([4, 0, 0, 0, 0])], total.keys()
    target = sum(H[i][j] * fsym[add(e(i), e(j))] for i in range(5) for j in range(5))
    assert sp.expand(total[(4, 0, 0, 0, 0)] - target) == 0
    # Horn copositivity on a rational grid of the simplex (sanity check)
    N = 12
    worst = None
    for c in product(range(N + 1), repeat=5):
        if sum(c) != N:
            continue
        v = sum(H[i][j] * c[i] * c[j] for i in range(5) for j in range(5))
        worst = v if worst is None else min(worst, v)
    assert worst >= 0
    print("PASS: coefficients are single eps-monomials; xi in (0,1)^4 (lex order);")
    print("      L_f(q)(xi) = eps^(4 e_1) * sum_ij H_ij f(2e_i+2e_j);")
    print("      Horn form nonnegative on the grid of mesh 1/%d (minimum %s)." % (N, worst))


if __name__ == "__main__":
    main()
