#!/usr/bin/env python3
"""Exact finite diagnostics for nonlinear-subspace and face elimination.

These checks do not implement the FPT algorithm or prove its bit bound.
They exercise rank extraction, rank loss on faces, affine quadratic
elimination, and the shared sign/equality threshold mechanism.
"""
from fractions import Fraction
from itertools import product

import sympy as s


def nonlinear_rows(f, xs):
    r = sum(c * s.prod(x**a for x, a in zip(xs, mon))
            for mon, c in s.Poly(f, *xs).terms() if sum(mon) >= 3)
    grads = [s.Poly(s.diff(r, x), *xs) for x in xs]
    monoms = sorted(set().union(*(set(g.monoms()) for g in grads)))
    matrix = s.Matrix([[g.coeff_monomial(mon) for g in grads] for mon in monoms])
    return s.Matrix.vstack(*matrix.rowspace()) if matrix.rank() else s.zeros(0, len(xs))


def eliminate(f, xs, U, base, Z):
    d = Z.cols
    if d == 0:
        return 0, 0
    W_cols = (U * Z).nullspace()
    W = s.Matrix.hstack(*W_cols) if W_cols else s.zeros(d, 0)
    columns = list(W_cols)
    T_cols = []
    for j in range(d):
        e = s.eye(d)[:, j]
        if s.Matrix.hstack(*(columns + [e])).rank() > len(columns):
            columns.append(e)
            T_cols.append(e)
    T = s.Matrix.hstack(*T_cols) if T_cols else s.zeros(d, 0)
    rank = T.cols
    assert rank == (U * Z).rank() <= U.rows
    t = s.Matrix(s.symbols(f't0:{rank}')) if rank else s.zeros(0, 1)
    w = s.Matrix(s.symbols(f'w0:{W.cols}')) if W.cols else s.zeros(0, 1)
    x = base + Z * (T * t + W * w)
    expression = s.expand(f.subs(dict(zip(xs, x)), simultaneous=True))
    if W.cols:
        H = s.hessian(expression, list(w))
        assert not set().union(*(v.free_symbols for v in H))
        assert H.is_positive_definite
        residual = s.Matrix([s.diff(expression, v) for v in w])
        linear = residual.subs({v: 0 for v in w})
        w_star = -H.inv() * linear
        assert all(s.expand(v) == 0 for v in residual.subs(dict(zip(w, w_star))))
        reduced_x = x.subs(dict(zip(w, w_star)))
        phi = s.expand(expression.subs(dict(zip(w, w_star))))
    else:
        reduced_x, phi = x, expression
    assert s.expand(f.subs(dict(zip(xs, reduced_x)), simultaneous=True) - phi) == 0
    assert all(s.Poly(v, *list(t)).total_degree() <= 1 for v in reduced_x) if rank else True
    assert s.Poly(phi, *list(t)).total_degree() <= 4 if rank else not phi.free_symbols
    if rank:
        D = reduced_x.jacobian(t)
        assert D.rank() == rank
        assert s.simplify(U * reduced_x - U * (base + Z * T * t)) == s.zeros(U.rows, 1)
    return rank, W.cols


def main():
    xs = s.symbols('x0:3')
    x = s.Matrix(xs)
    Q = s.Matrix([[5, 1, 2], [1, 4, 1], [2, 1, 6]])
    assert Q.is_positive_definite
    q = (x.T * Q * x)[0] / 2 + (s.Matrix([1, -2, 3]).T * x)[0]
    directions = [s.zeros(0, 3), s.Matrix([[1, 2, -1]]),
                  s.Matrix([[1, 2, -1], [0, 1, 1]]), s.eye(3)]
    faces = [s.eye(3), s.Matrix([[1, 0], [0, 1], [1, -1]]),
             s.Matrix([[1], [2], [0]]), s.zeros(3, 0),
             s.Matrix([[2, -1], [-1, 0], [0, -1]])]
    counts = {'polynomials': 0, 'faces': 0, 'rank_drops': 0, 'eliminated_directions': 0}
    for supplied in directions:
        f = s.expand(q + sum(v**4 for v in supplied * x))
        U = nonlinear_rows(f, xs)
        assert U.rank() == supplied.rank()
        for shift in [s.zeros(3, 1), s.Matrix([s.Rational(1, 3), -2, 1])]:
            translated = s.expand(f.subs(dict(zip(xs, x + shift)), simultaneous=True))
            translated_U = nonlinear_rows(translated, xs)
            assert translated_U.rows == U.rows
            assert s.Matrix.vstack(U, translated_U).rank() == U.rows
            counts['polynomials'] += 1
            for Z in faces:
                rank, removed = eliminate(translated, xs, translated_U,
                                          s.Matrix([1, -1, s.Rational(2, 3)]), Z)
                counts['faces'] += 1
                counts['rank_drops'] += rank < U.rows
                counts['eliminated_directions'] += removed
    sign_checks = 0
    gamma = Fraction(1, 32)
    for alpha, error in product([Fraction(0), -3*gamma, -gamma, gamma, 3*gamma],
                                [-gamma/8, Fraction(0), gamma/8]):
        estimate = alpha + error
        answer = 0 if abs(estimate) < gamma/2 else (1 if estimate > 0 else -1)
        actual = 0 if not alpha else (1 if alpha > 0 else -1)
        assert answer == actual
        sign_checks += 1
    print(f'PASS: {counts}; {sign_checks} exact sign/equality margin checks')


if __name__ == '__main__':
    main()
