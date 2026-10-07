"""Revision 2 of robust-chains.md (review round 2).

Commands:
  python3 revision2_chains.py wall    Lemma A.4 (class-(a0) split of WALL for even n >= 4), exact arithmetic:
                                      rational data; u' > 1 > b on [-1,1] and the unique root c of u' = 2b in [-1,1]
                                      (sympy root counting on rational polynomials); the split identity (sympy,
                                      n = 4..30); the sum of the factor minima against the wall value (symbolic n);
                                      min H = H(-1, c) on [-1,1]^2 (analytic for max(x, y) >= 1 - 1/b; exact rational
                                      grid with a Lipschitz bound on [-1,0]^2); min phi = phi(-1, c) by the same method
                                      (used for odd n). Then floating-point cross-checks:
                                      the KKT candidates of H (corners, edges, interior via resultant) and a grid.
  python3 revision2_chains.py sos     sympy: a certificate for the opposite orientation with the ball constraint
                                      2 - x^2 - y^2; then the order-2 sparse moment relaxation of the chiral chain (pair cliques) with
                                      different placements of the box constraints (every clique, one clique per
                                      constraint in either orientation, with and without the ball constraint
                                      2M^2 - x^2 - y^2 per clique, univariate multipliers as in Waki et al. (20),
                                      with and without moment bounds |y_alpha| <= 1); Clarabel and SCS; floating point.
"""
import sys
import json
from fractions import Fraction as Fr


# ----------------------------------------------------------------------------------------------- WALL (exact)
UC = [Fr(0), Fr(1022, 1000), Fr(189, 1000), Fr(1774, 1000), Fr(1086, 1000)]
B = Fr(962, 1000)


def u(t):
    return sum(cf * t ** i for i, cf in enumerate(UC))


def H(x, y):
    return u(x) + u(y) + B * x * y - B * (x + y)


def wall():
    import sympy as sp
    t, x, y = sp.symbols("t x y", real=True)
    us = sum(sp.Rational(cf.numerator, cf.denominator) * t ** i for i, cf in enumerate(UC))
    bs = sp.Rational(B.numerator, B.denominator)
    du = sp.diff(us, t)
    # (1) u' > 1 > b on [-1,1]: u' - 1 has no root in [-1,1] and is positive at 0
    p1 = sp.Poly(du - 1, t)
    n1 = p1.count_roots(-1, 1)
    print(f"(1) u'(t) - 1 = {sp.expand(du - 1)}: real roots in [-1,1]: {n1}; value at 0: {(du - 1).subs(t, 0)} "
          f"-> u' > 1 > b = {bs} on [-1,1]: {n1 == 0 and (du - 1).subs(t, 0) > 0}")
    crit = [r for r in sp.Poly(sp.diff(du, t), t).real_roots() if -1 <= r <= 1]
    mins = [(du.subs(t, r)) for r in crit] + [du.subs(t, -1), du.subs(t, 1)]
    print(f"    exact min of u' on [-1,1] (critical points of u' and endpoints) = {sp.N(min(mins, key=lambda v: sp.N(v, 30)), 12)}")
    # (2) u' - 2b has exactly one root c in [-1,1], u'(-1) < 2b < u'(1)
    p2 = sp.Poly(du - 2 * bs, t)
    n2 = p2.count_roots(-1, 1)
    roots = [r for r in p2.real_roots() if -1 <= r <= 1]
    c = roots[0]
    print(f"(2) u'(t) - 2b: real roots in [-1,1]: {n2}; u'(-1) - 2b = {(du - 2*bs).subs(t, -1)}, u'(1) - 2b = {(du - 2*bs).subs(t, 1)}; "
          f"c = {sp.N(c, 40)}")
    print("    so u(t) - 2bt is strictly decreasing on [-1, c] and strictly increasing on [c, 1]; its unique minimizer is c")
    cr = Fr(3377232, 10 ** 7)
    Hc_upper = H(Fr(-1), cr)
    Hc = sp.N((us.subs(t, -1) + us.subs(t, c) - 2 * bs * c + bs), 40)
    print(f"    H(-1, c) = u(-1) + u(c) - 2bc + b = {Hc}; rational upper bound H(-1, {cr}) = {float(Hc_upper):.15f} "
          f"(>= H(-1, c) because c minimizes H(-1, .))")
    # (3) the split identity for even n
    ok = True
    for n in range(4, 31, 2):
        X = sp.symbols(f"x1:{n + 1}", real=True)
        U = lambda z: us.subs(t, z)
        f = sum(U(z) for z in X) + bs * sum(X[i] * X[i + 1] for i in range(n - 1))
        facs = [U(X[0]) + bs * X[1] * (X[0] + 1)]
        for e in range(2, n - 1):  # bond e joins X[e-1], X[e]
            xa, xb = X[e - 1], X[e]
            if e % 2 == 0:
                facs.append(U(xa) + U(xb) + bs * xa * xb - bs * (xa + xb))
            else:
                facs.append(bs * (xa + 1) * (xb + 1) - bs)
        facs.append(U(X[-1]) + bs * X[-2] * (X[-1] + 1))
        assert len(facs) == n - 1
        ok = ok and sp.expand(sum(facs) - f) == 0
    print(f"(3) split identity sum(factors) - f_n == 0 for n = 4, 6, ..., 30: {ok}")
    # (4) sum of the factor minima against the wall value, symbolic in n
    N, U1, Uc, bb, cc = sp.symbols("n u_m1 u_c b c")
    m = (U1 + Uc) / 2 - bb * cc
    phi11 = U1 + bb
    Hmin = U1 + Uc - 2 * bb * cc + bb
    summin = 2 * U1 - bb * (N / 2 - 2) + (N / 2 - 1) * Hmin
    wallv = (N - 2) * m + phi11 + U1
    print(f"(4) [2u(-1) - b(n/2 - 2) + (n/2 - 1) H(-1,c)] - [(n-2) m + phi(-1,-1) + u(-1)] = {sp.simplify(summin - wallv)}")
    # (5) min H on [-1,0]^2 by an exact rational grid with a Lipschitz bound
    #     |d_x H| = |u'(x) + b(y - 1)| <= sum_i i |u_i| + 2b <= 13 on [-1,1]^2; same for d_y.
    Lbound = sum(i * abs(cf) for i, cf in enumerate(UC)) + 2 * B
    assert Lbound <= 13
    K = 200
    h = Fr(1, K)
    grid = [Fr(-1) + i * h for i in range(K + 1)]
    uv = {g: u(g) for g in grid}
    best = None
    for gx in grid:
        for gy in grid:
            v = uv[gx] + uv[gy] + B * gx * gy - B * (gx + gy)
            if best is None or v < best[0]:
                best = (v, gx, gy)
    err = 13 * (h / 2) * 2
    x0 = 1 - 1 / B
    print(f"(5) R = [-1, x0]^2 with x0 = 1 - 1/b = {x0} = {float(x0):.6f} lies in [-1,0]^2. Exact grid on [-1,0]^2, step 1/{K}: "
          f"min H = {float(best[0]):.10f} at ({best[1]}, {best[2]}); Lipschitz error <= 13 h = {float(err):.4f}; "
          f"lower bound on [-1,0]^2 = {float(best[0] - err):.6f}; minus the upper bound on H(-1,c): "
          f"{float(best[0] - err - Hc_upper):.6f} > 0: {best[0] - err > Hc_upper}")
    # (6) min phi = phi(-1, c) (odd n, Proposition A.1), same method: 2 phi = u(x) + u(y) + 2bxy.
    #     For x >= -1/(2b): d_y (2 phi) = u'(y) + 2bx > 1 + 2bx >= 0, so 2 phi(x, y) >= 2 phi(x, -1)
    #     = u(x) - 2bx + u(-1) >= u(c) - 2bc + u(-1) = 2 phi(c, -1); likewise for y. Remaining square
    #     [-1, -1/(2b))^2 lies in [-1, -1/2]^2: exact grid, |d_x (2 phi)| = |u'(x) + 2by| <= 13.
    x1 = -1 / (2 * B)
    grid6 = [Fr(-1) + i * h for i in range(K // 2 + 1)]
    best6 = min((uv[gx] + uv[gy] + 2 * B * gx * gy, gx, gy) for gx in grid6 for gy in grid6)
    twom_upper = u(Fr(-1)) + u(cr) - 2 * B * cr
    print(f"(6) 2 phi on [-1, x1]^2, x1 = -1/(2b) = {x1} = {float(x1):.6f} <= -1/2. Exact grid on [-1,-1/2]^2, step 1/{K}: "
          f"min 2phi = {float(best6[0]):.10f} at ({best6[1]}, {best6[2]}); lower bound {float(best6[0] - err):.6f}; "
          f"minus the upper bound 2 phi(-1, {cr}) >= 2m: {float(best6[0] - err - twom_upper):.6f} > 0: {best6[0] - err > twom_upper}")
    print(f"    so min phi = m = phi(-1, c) = {sp.N((us.subs(t, -1) + us.subs(t, c)) / 2 - bs * c, 30)} (proved)")
    # floating-point cross-checks: KKT candidates of H on [-1,1]^2 and a fine grid
    import numpy as np
    from numpy.polynomial import polynomial as P
    ucf = np.array([float(v) for v in UC]); bf = float(B)
    Hf = lambda X, Y: P.polyval(X, ucf) + P.polyval(Y, ucf) + bf * X * Y - bf * (X + Y)
    du_f = P.polyder(ucf)
    cand = [(sx, sy) for sx in (-1.0, 1.0) for sy in (-1.0, 1.0)]
    for side in (-1.0, 1.0):  # edges x = side: d_y H = u'(y) + b(side - 1) = 0
        for r in np.roots(P.polyadd(du_f, [bf * (side - 1)])[::-1]):
            if abs(r.imag) < 1e-12 and -1 < r.real < 1:
                cand += [(side, r.real), (r.real, side)]
    xs_, ys_ = sp.symbols("xs ys")
    ex = sp.diff(us, t).subs(t, xs_) + bs * (ys_ - 1)
    ey = sp.diff(us, t).subs(t, ys_) + bs * (xs_ - 1)
    res = sp.Poly(sp.resultant(ex, ey, ys_), xs_)
    for r in res.nroots(n=30, maxsteps=200):
        if abs(sp.im(r)) < 1e-20 and -1 < sp.re(r) < 1:
            xr = float(sp.re(r))
            for yr in np.roots(P.polyadd(du_f, [bf * (xr - 1)])[::-1]):
                if abs(yr.imag) < 1e-9 and -1 < yr.real < 1 and abs(P.polyval(xr, du_f) + bf * (yr.real - 1)) < 1e-8:
                    cand.append((xr, yr.real))
    vals = sorted({(round(float(Hf(a, b_)), 10), round(a, 6), round(b_, 6)) for a, b_ in cand})
    print("    float cross-check, KKT candidates of H (value, x, y), lowest five:", vals[:5])
    print(f"    float: second-lowest candidate value - min = {vals[2][0] - vals[0][0]:.4f} (the two lowest are the mirror pair)"
          if abs(vals[0][0] - vals[1][0]) < 1e-9 else "    float: mirror pair not found")
    g = np.linspace(-1, 1, 4001)
    Xg, Yg = np.meshgrid(g, g, indexing="ij")
    Hg = Hf(Xg, Yg)
    k = np.unravel_index(np.argmin(Hg), Hg.shape)
    print(f"    float: grid 4001^2 on [-1,1]^2: min H = {Hg[k]:.10f} at ({g[k[0]]:.4f}, {g[k[1]]:.4f}); H(-1,c) = {float(Hc):.10f}")


# ----------------------------------------------------------------------------------------- moment relaxations
def sos():
    import cvxpy as cp
    import sympy as sp
    # exact: certificate for the opposite orientation with the ball constraint 2 - x^2 - y^2 (M = 1)
    x, y, b, g, ev = sp.symbols("x y b g ev", real=True)
    a = b + ev
    W = a / 2 * (x**2 + y**2) + b * x * y + g / 2 * (x * y**2 - x**2 * y)
    h = lambda z: -g / 2 * z**3
    dec = ((b / 2 - g) * (x + y)**2 + ev / 2 * (x**2 + y**2)) + g / 4 * (x + y)**2 * ((1 + y)**2 + (1 - x)**2) \
        + g / 4 * (x + y)**2 * (2 - x**2 - y**2)
    print("sympy: W + h(x) - h(y) - [(b/2-g)(x+y)^2 + (ev/2)(x^2+y^2) + (g/4)(x+y)^2((1+y)^2 + (1-x)^2) "
          "+ (g/4)(x+y)^2 (2 - x^2 - y^2)] =", sp.simplify(sp.expand(W + h(x) - h(y) - dec)))
    bb, gg, ee = 0.6, 0.3, 0.05
    aa = bb + ee
    mons = [(i, d - i) for d in range(5) for i in range(d + 1)]
    basis2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
    basis1 = [(0, 0), (1, 0), (0, 1)]

    def build(n, scheme, ball=None, ybound=False):
        ys = [{m: (cp.Variable() if m != (0, 0) else 1.0) for m in mons} for _ in range(n - 1)]
        cons = []

        def ent(yv, m):
            return yv[m]

        def loc(yv, basis, g):  # localizing matrix of the polynomial g = [(coef, mon)] w.r.t. basis
            k = len(basis)
            Z = cp.Variable((k, k), PSD=True)
            for i, p in enumerate(basis):
                for j, q in enumerate(basis):
                    if j < i:
                        continue
                    mm = (p[0] + q[0], p[1] + q[1])
                    cons.append(Z[i, j] == sum(cf * ent(yv, (mm[0] + s[0], mm[1] + s[1])) for cf, s in g))
        one = [(1.0, (0, 0))]
        for e in range(n - 1):
            loc(ys[e], basis2, one)
            if e + 1 < n - 1:
                for d in range(1, 5):
                    cons.append(ys[e][(0, d)] == ys[e + 1][(d, 0)])
            if ball is not None:
                loc(ys[e], basis1, [(2 * ball ** 2, (0, 0)), (-1.0, (2, 0)), (-1.0, (0, 2))])
            if ybound:
                for m in mons:
                    if m != (0, 0):
                        cons += [ys[e][m] <= 1, ys[e][m] >= -1]

        # variable i (1-based) is coordinate 0 of clique i (if i <= n-1) and coordinate 1 of clique i-1 (if i >= 2)
        def where(i, side):  # clique index (0-based) and coordinate for variable i, side 'L' = clique (i-1,i), 'R' = (i,i+1)
            if side == "L" and i >= 2:
                return i - 2, 1
            if side == "R" and i <= n - 1:
                return i - 1, 0
            return (i - 1, 0) if i <= n - 1 else (i - 2, 1)

        def lin(sign, coord):  # 1 + sign * x_coord
            return [(1.0, (0, 0)), (float(sign), (1, 0) if coord == 0 else (0, 1))]

        def quad(coord):
            return [(1.0, (0, 0)), (-1.0, (2, 0) if coord == 0 else (0, 2))]
        for i in range(1, n + 1):
            if scheme in ("every", "every_quad"):
                for side in ("L", "R"):
                    if (side == "L" and i >= 2) or (side == "R" and i <= n - 1):
                        e, co = where(i, side)
                        if scheme == "every":
                            loc(ys[e], basis1, lin(-1, co)); loc(ys[e], basis1, lin(+1, co))
                        else:
                            loc(ys[e], basis1, quad(co))
            elif scheme in ("match", "opp"):
                # match: 1 - x_i in clique (i, i+1), 1 + x_i in clique (i-1, i)  (the orientation of the certificate)
                # opp:   1 - x_i in clique (i-1, i), 1 + x_i in clique (i, i+1)
                sm, sp_ = ("R", "L") if scheme == "match" else ("L", "R")
                e, co = where(i, sm); loc(ys[e], basis1, lin(-1, co))
                e, co = where(i, sp_); loc(ys[e], basis1, lin(+1, co))
            elif scheme in ("one_quad_R", "one_quad_L"):
                e, co = where(i, "R" if scheme == "one_quad_R" else "L")
                loc(ys[e], basis1, quad(co))
            elif scheme in ("uni", "uni_quad"):
                e, co = where(i, "R")
                ub = [(0, 0), (1, 0)] if co == 0 else [(0, 0), (0, 1)]
                if scheme == "uni":
                    loc(ys[e], ub, lin(-1, co)); loc(ys[e], ub, lin(+1, co))
                else:
                    loc(ys[e], ub, quad(co))
            else:
                raise ValueError(scheme)
        obj = 0
        for e in range(n - 1):
            yv = ys[e]
            obj += aa / 2 * (yv[(2, 0)] + yv[(0, 2)]) + bb * yv[(1, 1)] + gg / 2 * (yv[(1, 2)] - yv[(2, 1)])
        obj += aa / 2 * ys[0][(2, 0)] + aa / 2 * ys[-1][(0, 2)]
        return cp.Problem(cp.Minimize(obj), cons)

    runs = [
        ("every", None, False, "linear box constraints localized in every clique containing the variable (Prop. C.5)"),
        ("match", None, False, "linear, one clique per constraint, orientation of the certificate (1-x_i in (i,i+1), 1+x_i in (i-1,i))"),
        ("opp", None, False, "linear, one clique per constraint, opposite orientation (1-x_i in (i-1,i), 1+x_i in (i,i+1))"),
        ("opp", 1.0, False, "opposite orientation + ball 2 - x^2 - y^2 per clique"),
        ("opp", 1.01, False, "opposite orientation + ball 2M^2 - x^2 - y^2 per clique, M = 1.01"),
        ("opp", 1.1, False, "opposite orientation + ball 2M^2 - x^2 - y^2 per clique, M = 1.1"),
        ("opp", 2.0, False, "opposite orientation + ball 2M^2 - x^2 - y^2 per clique, M = 2"),
        ("opp", 10.0, False, "opposite orientation + ball 2M^2 - x^2 - y^2 per clique, M = 10"),
        ("uni", None, False, "linear, univariate multipliers (Waki et al. (20))"),
        ("uni", None, True, "linear, univariate multipliers + moment bounds |y_alpha| <= 1"),
        ("every_quad", None, False, "1 - x_i^2 localized in every clique containing x_i (Prop. C.5)"),
        ("one_quad_R", None, False, "1 - x_i^2 in one clique: (i,i+1) (last variable: (n-1,n))"),
        ("one_quad_L", None, False, "1 - x_i^2 in one clique: (i-1,i) (first variable: (1,2))"),
        ("uni_quad", None, False, "1 - x_i^2 with univariate multipliers"),
        ("uni_quad", None, True, "1 - x_i^2 with univariate multipliers + |y_alpha| <= 1"),
    ]
    which = sys.argv[2:] or ["5", "8"]
    for n in [int(v) for v in which]:
        for scheme, ball, yb, label in runs:
            out = dict(n=n, scheme=scheme, ball_M=ball, ybound=yb, label=label)
            for solver, kw in (("CLARABEL", {}), ("SCS", dict(eps=1e-8, max_iters=200000))):
                prob = build(n, scheme, ball, yb)
                try:
                    prob.solve(solver=solver, **kw)
                    out[solver] = (prob.status, None if prob.value is None else float(f"{prob.value:.6g}"))
                except Exception as exc:  # noqa: BLE001
                    out[solver] = ("error", str(exc)[:80])
            print(json.dumps(out), flush=True)


if __name__ == "__main__":
    {"wall": wall, "sos": sos}[sys.argv[1]]()
