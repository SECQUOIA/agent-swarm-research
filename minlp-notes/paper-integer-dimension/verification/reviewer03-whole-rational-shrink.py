"""Exact finite checks of the rational shrinking-coordinate construction.

This does not implement the imported nc-rank algorithm. The examples have
matching elementary scalar-rank and shrunk-subspace certificates.
"""
from itertools import product
from random import Random
import sympy as s

rng = Random(3103)
counts = dict(systems=0, domain_vertices=0, output_error_checks=0)


def columns(vectors, rows):
    return s.Matrix.hstack(*vectors) if vectors else s.zeros(rows, 0)


for nz, nq in [(2, 1), (3, 1), (2, 2), (3, 2)]:
    n = nz + 1 + nq
    rank = 2 + nq
    S = s.eye(n)
    for i in range(n):
        for j in range(i):
            S[i, j] = s.Rational(rng.randint(-3, 3), rng.randint(1, 3))
    inverse = S.inv()
    blocks = []
    for output in range(3):
        H = s.zeros(n)
        H[0, nz] = H[nz, 0] = 1
        for i in range(nz + 1, n):
            H[i, i] = (-1) ** (i + output) * (output + 1)
        if output:
            for i in range(nz):
                H[i, nz] = H[nz, i] = s.Rational(rng.randint(-3, 3), 2)
            H[nz, nz] = output
            H[nz, n - 1] = H[n - 1, nz] = s.Rational(output, 3)
        blocks.append(H)
    assert blocks[0].rank() == rank
    hs = [inverse.T * H * inverse for H in blocks]
    U = S[:, :nz]
    V = columns(s.Matrix.hstack(*(H * U for H in hs)).columnspace(), n)
    assert U.cols - V.cols == n - rank
    Z = U * columns((V.T * U).nullspace(), U.cols)
    W = V * columns((U.T * V).nullspace(), V.cols)
    Q = columns(s.Matrix.hstack(Z, W).T.nullspace(), n)
    T = s.Matrix.hstack(Z, W, Q)
    assert T.det() != 0 and 2 * W.cols + Q.cols == rank
    for H in hs:
        transformed = T.T * H * T
        assert transformed[:Z.cols, :Z.cols] == s.zeros(Z.cols)
        assert transformed[:Z.cols, Z.cols + W.cols:] == s.zeros(Z.cols, Q.cols)
    lower = s.Matrix([s.Rational(-i - 2, i + 3) for i in range(n)])
    upper = s.Matrix([s.Rational(i + 3, i + 2) for i in range(n)])
    Ti = T.inv()
    vl = s.Matrix([sum(min(Ti[i,j]*lower[j], Ti[i,j]*upper[j]) for j in range(n)) for i in range(n)])
    vu = s.Matrix([sum(max(Ti[i,j]*lower[j], Ti[i,j]*upper[j]) for j in range(n)) for i in range(n)])
    widths = vu - vl
    assert all(width > 0 for width in widths)
    A = T * s.diag(*widths)
    c = T * vl
    for choices in product([0, 1], repeat=n):
        x = s.Matrix([upper[i] if choices[i] else lower[i] for i in range(n)])
        y = A.inv() * (x - c)
        assert all(0 <= t <= 1 for t in y)
        assert c + A*y == x
        counts['domain_vertices'] += 1
    # The graph convention is q=x^T H x/2, hence off-diagonal coefficients H_it.
    gs = [A.T * H * A for H in hs]
    coeffs = [{(i,j): (G[i,j]/2 if i == j else G[i,j]) for i in range(n) for j in range(i,n)} for G in gs]
    C = max(sum(abs(v) for v in cs.values()) for cs in coeffs)
    b = 0
    while C > 4 * 2**b:
        b += 1
    for k in [0, 1, 4, 9]:
        K = k + b
        depths = [0] * Z.cols + [K] * W.cols + [(K+1)//2] * Q.cols
        delta = [s.Rational(1, 2**d) for d in depths]
        assert sum(depths) <= s.Rational(rank,2)*(k+b) + s.Rational(n,2)
        for cs in coeffs:
            for (i,j), value in cs.items():
                if value:
                    assert delta[i] * delta[j] <= s.Rational(1, 2**K)
        for trial in range(12):
            # Arbitrary residuals; all McCormick/square endpoint choices obey
            # the pairwise quarter-product bound, including depth-zero axes.
            residual = [delta[i] * s.Rational(rng.randint(0, 12), 12) for i in range(n)]
            errors = {}
            for i in range(n):
                for j in range(i,n):
                    u, v = residual[i], residual[j]
                    if i == j:
                        lo, hi = max(0, 2*delta[i]*u-delta[i]**2), delta[i]*u
                    else:
                        lo = max(0, delta[j]*u+delta[i]*v-delta[i]*delta[j])
                        hi = min(delta[j]*u, delta[i]*v)
                    e = (lo if rng.randint(0,1) else hi) - u*v
                    assert abs(e) <= delta[i]*delta[j]/4
                    errors[i,j] = e
            for cs in coeffs:
                error = sum(value * errors[pair] for pair,value in cs.items())
                assert abs(error) <= C*s.Rational(1,2**K)/4 <= s.Rational(1,2**k)
                counts['output_error_checks'] += 1
    counts['systems'] += 1

print('PASS', counts)
