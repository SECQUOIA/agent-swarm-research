"""recA verification: exact checks of statements changed or renamed in W3.

1. lem:cr-cell (bag-cell interpolation, per-coordinate L_i, effective width):
   F(x) >= min_{corners v of C} V_B(v) - e_B(C) for random nonconvex box QPs
   with one continuous outside coordinate (V_B computed exactly) and an
   integer coordinate in the bag.
2. prop:cv-ladder identity in the renamed variables
   z^2 + phi_M - 1/20 = t^2 + M rho_1^2 + rho_2^2 + alpha_1/5, and the bounds
   alpha_1^2 <= 2 rho_2^2 + 8 t^2, alpha_2^2 <= 3(rho_1^2+rho_2^2+t^2).
3. ex:cv-fm table (responses, values, B^T C B, piece second derivatives).
4. eq:cv-energy on random one-leaf certificates (box, interior response).
5. ex:cr-star32 numbers and prop:star(A) corner minimum formula.
6. prop:cv-limit SOS identity and critical points y_c, x_c.
"""
from fractions import Fraction as Fr
import itertools, random
import sympy as sp

random.seed(11)


def check_cr_cell(trials=400):
    # coordinates: 0 continuous in [0,2], 1 integer in {0,..,3}, 2 continuous in [0,1] (outside)
    bad = 0
    for _ in range(trials):
        H = [[0] * 3 for _ in range(3)]
        for i in range(3):
            H[i][i] = random.randint(-4, 6)
            for j in range(i + 1, 3):
                H[i][j] = H[j][i] = random.randint(-5, 5)
        b = [random.randint(-6, 6) for _ in range(3)]
        H2 = H[2][2]

        def F(x):
            return sum(Fr(H[i][j], 2) * x[i] * x[j] for i in range(3) for j in range(3)) + sum(
                b[i] * x[i] for i in range(3))

        def VB(v0, v1):
            # min over y in [0,1] of F(v0,v1,y): quadratic a y^2 + c y + d
            a = Fr(H2, 2)
            c = H[0][2] * v0 + H[1][2] * v1 + b[2]
            cands = [Fr(0), Fr(1)]
            if a > 0:
                y = -c / (2 * a)
                if 0 <= y <= 1:
                    cands.append(y)
            return min(F([v0, v1, y]) for y in cands)

        L = [max(H[0][0], 0), max(H[1][1], 0)]
        # random bag cell: continuous [a0,b0] in [0,2], integer [a1,b1] in {0..3}
        a0 = Fr(random.randint(0, 8), 4)
        b0 = a0 + Fr(random.randint(0, 8 - int(4 * a0)), 4)
        a1 = random.randint(0, 3)
        b1 = random.randint(a1, 3)
        w0 = b0 - a0
        w1 = 0 if b1 - a1 == 1 else b1 - a1
        e = Fr(L[0], 8) * w0 ** 2 + Fr(L[1], 8) * w1 ** 2
        cmin = min(VB(u, v) for u in (a0, b0) for v in (a1, b1))
        for _ in range(6):
            x0 = a0 + (b0 - a0) * Fr(random.randint(0, 16), 16)
            x1 = random.randint(a1, b1)
            y = Fr(random.randint(0, 16), 16)
            if F([x0, x1, y]) < cmin - e:
                bad += 1
    return bad


def check_ladder():
    t, a1, a2, M, z, y1, y2 = sp.symbols('t alpha1 alpha2 M z y1 y2')
    a = sp.Rational(1, 5)
    phi = M * (y1 + y2 - z) ** 2 + (y1 - 2 * z + sp.Rational(1, 2)) ** 2
    lhs = (z ** 2 + phi - sp.Rational(1, 20)).subs({z: t + a, y1: a1, y2: a2 + a})
    r1 = a1 + a2 - t
    r2 = a1 - 2 * t
    rhs = t ** 2 + M * r1 ** 2 + r2 ** 2 + a1 / 5
    ok1 = sp.expand(lhs - rhs) == 0
    # alpha1 = rho2 + 2t, alpha2 = rho1 - rho2 - t
    ok2 = sp.expand(a1 - (r2 + 2 * t)) == 0 and sp.expand(a2 - (r1 - r2 - t)) == 0
    R1, R2, T = sp.symbols('R1 R2 T')
    g1 = sp.expand(2 * R2 ** 2 + 8 * T ** 2 - (R2 + 2 * T) ** 2)  # = (R2-2T)^2 >= 0
    g2 = sp.expand(3 * (R1 ** 2 + R2 ** 2 + T ** 2) - (R1 - R2 - T) ** 2)
    ok3 = sp.simplify(g1 - (R2 - 2 * T) ** 2) == 0
    ok4 = sp.simplify(g2 - ((R1 + R2) ** 2 + (R1 + T) ** 2 + (R2 - T) ** 2)) == 0
    # 41/4 / (1/12) = 123 ; 2 + 1/16 = 33/16
    ok5 = sp.Rational(41, 4) / sp.Rational(1, 12) == 123 and 2 + sp.Rational(1, 16) == sp.Rational(33, 16)
    return ok1 and ok2 and ok3 and ok4 and ok5


def check_fm():
    M, z = sp.symbols('M z', positive=True)
    C = sp.Matrix([[2 * M + 2, 2 * M], [2 * M, 2 * M]])
    Gam = sp.Matrix([-2 * M - 4, -2 * M])
    c = sp.Matrix([1, 0])
    y1, y2 = sp.symbols('y1 y2')
    phi = M * (y1 + y2 - z) ** 2 + (y1 - 2 * z + sp.Rational(1, 2)) ** 2
    # check C, Gamma, c
    yv = sp.Matrix([y1, y2])
    quad = (yv.T * C * yv / 2)[0] + (yv.T * Gam)[0] * z + (c.T * yv)[0]
    retained = M * z ** 2 + (2 * z - sp.Rational(1, 2)) ** 2
    ok = sp.expand(phi - quad - retained) == 0
    pieces = [
        (sp.Matrix([0, z]), (sp.Rational(1, 2) - 2 * z) ** 2, 2 * M, 8),
        (sp.Matrix([2 * z - sp.Rational(1, 2), sp.Rational(1, 2) - z]), 0, 2 * M + 8, 0),
        (sp.Matrix([((M + 2) * z - sp.Rational(1, 2)) / (M + 1), 0]), M * (z - sp.Rational(1, 2)) ** 2 / (M + 1),
         2 * (M + 2) ** 2 / (M + 1), 2 * M / (M + 1)),
    ]
    for resp, val, btcb, d2 in pieces:
        v = phi.subs({y1: resp[0], y2: resp[1]})
        ok &= sp.simplify(v - val) == 0
        B = sp.diff(resp, z)
        ok &= sp.simplify((B.T * C * B)[0] - btcb) == 0
        ok &= sp.simplify(sp.diff(val, z, 2) - d2) == 0
        ok &= sp.simplify(2 * M + 8 - btcb - d2) == 0
    ok &= sp.simplify(2 * (M + 2) ** 2 / (M + 1) - 2 * M - (2 * (M + 2) ** 2 - 2 * M * (M + 1)) / (M + 1)) == 0
    return ok


def check_energy(trials=200):
    # one-leaf certificate with interior unconstrained response: E empty, W = R^n,
    # B = -C^{-1} Gamma; (B^T C B)_jj = -min_d (d^T C d + 2 d^T Gamma e_j)
    bad = 0
    for _ in range(trials):
        n, k = 2, 2
        A = sp.Matrix(n, n, lambda i, j: random.randint(-3, 3))
        C = A.T * A + sp.eye(n)
        Gam = sp.Matrix(n, k, lambda i, j: random.randint(-4, 4))
        B = -C.inv() * Gam
        for j in range(k):
            d = sp.Matrix(sp.symbols('d0:%d' % n))
            f = (d.T * C * d)[0] + 2 * (d.T * Gam[:, j])[0]
            sol = sp.solve([sp.diff(f, di) for di in d], list(d), dict=True)[0]
            mn = f.subs(sol)
            if sp.simplify((B.T * C * B)[j, j] + mn) != 0:
                bad += 1
    return bad


def check_star():
    ok = True
    h, m, eps = Fr(1, 2), 32, Fr(1, 16)
    om = m * h * h / 4 - 1 - eps
    ok &= om == Fr(15, 16)
    G = [Fr(0), Fr(1, 2), Fr(1)]

    def leafmin(x):
        return min(y * y - h * x * y for y in G)

    VG = {x: x * x + om * x + m * leafmin(x) for x in G}
    ok &= [VG[x] for x in G] == [0, Fr(23, 32), Fr(31, 16)]
    corners = sorted(x * x + om * x + (y * y - h * x * y) + (m - 1) * leafmin(x) for x in (Fr(1, 2), Fr(1)) for y in (Fr(0), Fr(1, 2)))
    ok &= corners == [Fr(23, 32), Fr(27, 32), Fr(31, 16), Fr(31, 16)]
    ok &= 2 * 2 * h * h / 8 == Fr(1, 8) and (1 + m) * 2 * h * h / 8 == Fr(33, 16)
    ok &= min(corners) == (1 - h) * (m * h * h / 4 - h - eps)
    # grid error at x=1: m * dist(1/4, G)^2 = 2 = 31/16 - (-1/16)
    ok &= VG[Fr(1)] - (-1 + Fr(15, 16)) == m * Fr(1, 16)
    # general family (A): corner minimum formula for several (j, m, eps)
    for j in (1, 2, 3):
        hh = Fr(1, 2 ** j)
        GG = [hh * i for i in range(2 ** j + 1)]
        for mm in (int(4 / hh ** 2) + 1, int(4 / hh ** 2) + 7):
            for ee in (Fr(1, 64), Fr(1, 10)):
                if mm * hh * hh <= 4 * (1 + ee):
                    continue
                oo = mm * hh * hh / 4 - 1 - ee
                lm = lambda x: min(y * y - hh * x * y for y in GG)
                cm = min(x * x + oo * x + (y * y - hh * x * y) + (mm - 1) * lm(x)
                         for x in (1 - hh, Fr(1)) for y in (Fr(0), hh))
                ok &= cm == (1 - hh) * (mm * hh * hh / 4 - hh - ee)
    return ok


def check_limit():
    x1, x2, M, y = sp.symbols('xi1 xi2 M y')
    lhs = sp.Rational(3, 4) * x1 ** 2 - sp.Rational(9, 4) * x1 * x2 + sp.Rational(7, 4) * x2 ** 2
    rhs = sp.Rational(3, 4) * (x1 - sp.Rational(3, 2) * x2) ** 2 + sp.Rational(1, 16) * x2 ** 2
    ok = sp.expand(lhs - rhs) == 0
    x = sp.symbols('x')
    FM = M * (x - y) ** 2 - sp.Rational(1, 8) * (x + y - 2) ** 2 + 2 * (y - 1)
    ok &= sp.simplify(sp.diff(FM, x).subs(x, 2) - (2 * M * (2 - y) - y / 4)) == 0
    ok &= sp.simplify(sp.diff(FM, y).subs(y, 1) - (2 - (2 * M + sp.Rational(1, 4)) * (x - 1))) == 0
    ok &= sp.simplify(FM.subs(y, 1) - (M - sp.Rational(1, 8)) * (x - 1) ** 2) == 0
    ok &= FM.subs({x: 2, y: 2}) == sp.Rational(3, 2)
    return ok


if __name__ == '__main__':
    r = check_cr_cell()
    print('lem:cr-cell violations:', r)
    print('ladder identity and bounds:', check_ladder())
    print('ex:cv-fm table:', check_fm())
    print('energy formula violations:', check_energy(60))
    print('star numbers:', check_star())
    print('cv-limit:', check_limit())
