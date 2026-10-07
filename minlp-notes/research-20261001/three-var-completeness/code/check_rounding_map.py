"""Exact check of the rounding map used in note.md, Lemma 2.10.

For a coordinate i, the rounding map is the linear operator

    rho_i(f)(x) = (1 - x_i) f(x)|_{x_i = 0} + x_i f(x)|_{x_i = 1}

on polynomials.  It is the moment counterpart of replacing coordinate i of
every atom by an independent Bernoulli variable with the same mean.

The script checks, in exact arithmetic (sympy):

  1. rho_i maps the span V of the 20 monomials of the disjoint system
     (exponents in {0,1,2}^3 with at most one 2) into V; it fixes every
     monomial except that a factor x_i^2 becomes x_i;
  2. for each of the 27 localizing weights w_{A,B} and each i, and for a
     generic affine L in the free coordinates R (symbolic coefficients),
     rho_i(w_{A,B} L^2) equals
        w_{A,B} L^2                                   if i in A or B,
        w_{A,B+i} L|_{x_i=0}^2 + w_{A+i,B} L|_{x_i=1}^2   if i in R;
     both summands are again generators of the disjoint system;
  3. the functional delta_i (coefficient of x_i^2 in f, with the other
     coordinates set to 0) is nonnegative on every generator and is 1 on
     x_i^2 and 0 on every other monomial of degree at most two.

Together these prove that the disjoint moment relaxation is invariant under
rho_i and under adding diagonal slack (note.md, Lemma 2.10).
"""
from itertools import product

import sympy as sp

X = sp.symbols('x0:3')
MONOS = [e for e in product(range(3), repeat=3) if list(e).count(2) <= 1]


def mono(e):
    return sp.Mul(*[X[j] ** e[j] for j in range(3)])


V_SET = {e for e in MONOS}


def rho(f, i):
    f = sp.expand(f)
    return sp.expand((1 - X[i]) * f.subs(X[i], 0) + X[i] * f.subs(X[i], 1))


def support(f):
    p = sp.Poly(sp.expand(f), *X)
    return {m for m in p.monoms()}


def weight(A, B):
    w = sp.Integer(1)
    for a in A:
        w *= X[a]
    for b in B:
        w *= (1 - X[b])
    return w


def main():
    # 1. monomial action
    for i in range(3):
        for e in MONOS:
            img = rho(mono(e), i)
            e2 = list(e)
            if e2[i] >= 1:
                e2[i] = 1
            assert sp.expand(img - mono(tuple(e2))) == 0
            assert support(img) <= V_SET
    print('1. rho_i maps the 20-monomial space into itself; x_i^2 -> x_i, other monomials fixed')

    # 2. generators
    count = 0
    for status in product((-1, 0, 1), repeat=3):   # -1 free, 0 -> (1-x), 1 -> x
        A = [j for j in range(3) if status[j] == 1]
        B = [j for j in range(3) if status[j] == 0]
        R = [j for j in range(3) if status[j] == -1]
        coef = sp.symbols('c0:4')
        L = coef[0] + sum(coef[1 + j] * X[j] for j in R)
        g = sp.expand(weight(A, B) * L ** 2)
        assert support(g) <= V_SET
        for i in range(3):
            img = rho(g, i)
            if i in A or i in B:
                assert sp.expand(img - g) == 0
            else:
                L0, L1 = L.subs(X[i], 0), L.subs(X[i], 1)
                rhs = weight(A, B + [i]) * L0 ** 2 + weight(A + [i], B) * L1 ** 2
                assert sp.expand(img - rhs) == 0
                # both summands are generators: L0, L1 are affine in R \ {i}
                assert X[i] not in L0.free_symbols and X[i] not in L1.free_symbols
            count += 1
    print('2. rho_i(generator) = sum of generators for all 27 weights and i = 0,1,2 (%d cases)' % count)

    # 3. slack functional
    for i in range(3):
        def delta(f):
            f = sp.expand(f)
            c = sp.Poly(f, X[i]).coeff_monomial(X[i] ** 2)
            return sp.expand(c.subs({X[j]: 0 for j in range(3) if j != i}))
        for e in MONOS:
            val = delta(mono(e))
            want = 1 if e == tuple(2 if j == i else 0 for j in range(3)) else 0
            if sum(e) <= 2:
                assert val == want, (i, e, val)
        for status in product((-1, 0, 1), repeat=3):
            A = [j for j in range(3) if status[j] == 1]
            B = [j for j in range(3) if status[j] == 0]
            R = [j for j in range(3) if status[j] == -1]
            coef = sp.symbols('c0:4')
            L = coef[0] + sum(coef[1 + j] * X[j] for j in R)
            val = delta(weight(A, B) * L ** 2)
            # value is w_{A,B}(0) * (x_i-coefficient of L)^2 >= 0
            expected = weight(A, B).subs({X[j]: 0 for j in range(3)}) * (coef[1 + i] ** 2 if i in R else 0)
            assert sp.expand(val - expected) == 0
            assert weight(A, B).subs({X[j]: 0 for j in range(3)}) >= 0
    print('3. delta_i >= 0 on all generators; delta_i(x_i^2) = 1, delta_i = 0 on other monomials of degree <= 2')
    print('PASS')


if __name__ == '__main__':
    main()
