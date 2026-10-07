"""Reviewer r2: exact check of Proposition 6 for eps = 1/16, xi_r = 7(1 - 2^-r) (limit 7 < 2/sqrt(eps) = 8),
box X = 9, Y = 1, W = 2.  For each round: the vertex (xi,0,1) is the unique LP optimum of the current
LP (checked by solving the exact 3x3 dual system for the tight rows and testing strict positivity,
and primal feasibility of all rows); the steps of C_a along the cone rays are exact boundary points;
the resulting cut equals x/xi' + xi' y/4 >= 1."""
from fractions import Fraction as Fr
eps = Fr(1, 16); X, Y, W = Fr(9), Fr(1), Fr(2)
xi = [7 * (1 - Fr(1, 2**r)) for r in range(31)]
c = (eps, Fr(1), Fr(1))
def solve3(A, b):  # exact Gaussian elimination
    M = [list(A[i]) + [b[i]] for i in range(3)]
    for k in range(3):
        p = next(i for i in range(k, 3) if M[i][k] != 0); M[k], M[p] = M[p], M[k]
        for i in range(3):
            if i != k and M[i][k] != 0:
                f = M[i][k] / M[k][k]; M[i] = [M[i][j] - f * M[k][j] for j in range(4)]
    return [M[i][3] / M[i][i] for i in range(3)]
cuts = []  # (g, h): g x + h y >= 1
ok = True
for r in range(30):
    x = (xi[r], Fr(0), Fr(1))
    rows = [((0, 1, 0), 0), ((0, 0, 1), 1)] + [((g, h, 0), 1) for g, h in cuts]  # rows a.x >= b
    rows += [((1, 0, 0), 0), ((-1, 0, 0), -X), ((0, -1, 0), -Y), ((0, 0, -1), -W)]
    for a, b in rows:
        ok &= sum(ai * xi_ for ai, xi_ in zip(a, x)) >= b
    tight = [(a, b) for a, b in rows if sum(ai * xi_ for ai, xi_ in zip(a, x)) == b]
    if r == 0:
        assert len(tight) == 3
    else:
        assert len(tight) == 3, (r, tight)
    # dual: sum_i y_i a_i = c, y > 0 strictly => unique optimum
    A = [[tight[i][0][j] for i in range(3)] for j in range(3)]
    y = solve3(A, list(c)); ok &= all(v > 0 for v in y)
    # rays of the basis cone: columns of inverse of tight-row matrix
    T = [list(t[0]) for t in tight]
    rays = [solve3(T, [Fr(int(i == k)) for i in range(3)]) for k in range(3)]
    a_ = 2 / xi[r + 1]
    def g(p): return p[2] - (a_ * p[0] + p[1] / a_) ** 2 / 4   # C_a = {g >= 0}
    ok &= g(x) > 0
    inv = []
    for d in rays:
        # g(x + t d) is quadratic in t: find coefficients exactly
        g0 = g(x); g1 = g([x[i] + d[i] for i in range(3)]); gm = g([x[i] - d[i] for i in range(3)])
        A2 = (g1 + gm) / 2 - g0; A1 = (g1 - gm) / 2
        if A2 == 0 and A1 >= 0:
            inv.append(Fr(0)); continue
        # concave (A2 <= 0): positive root of A2 t^2 + A1 t + g0 = 0; must be rational here
        disc = A1 * A1 - 4 * A2 * g0
        n, m = disc.numerator, disc.denominator
        import math
        sn, sm = math.isqrt(n), math.isqrt(m); assert sn * sn == n and sm * sm == m
        s = Fr(sn, sm); roots = [(-A1 + s) / (2 * A2), (-A1 - s) / (2 * A2)] if A2 != 0 else [-g0 / A1]
        t = min(v for v in roots if v > 0); inv.append(1 / t)
    # cut sum inv_k lam_k >= 1 with lam = T (p - x)  ->  in x-space
    coef = [sum(inv[k] * T[k][j] for k in range(3)) for j in range(3)]
    rhs = 1 + sum(coef[j] * x[j] for j in range(3))
    ok &= coef[2] == 0 and coef[0] / rhs == 1 / xi[r + 1] and coef[1] / rhs == xi[r + 1] / 4
    cuts.append((coef[0] / rhs, coef[1] / rhs))
    ok &= x[2] - x[0] * x[1] == 1
print('rounds 0-29 verified:', ok, ' LP value after 30 rounds:', float(eps * xi[30] + 1), ' z* =', float(1 + 2 * Fr(1, 4)))
