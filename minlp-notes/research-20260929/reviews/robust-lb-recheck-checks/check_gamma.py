"""Recheck of Proposition 3.3 at the reference parameters, written without the authors' code.

(1) Brute-force check of the partial minima L = -min_x g1 and U = c y^2 + min_z g2 (Lemma 3.1).
(2) gamma_d for d = 2..12 by the PRIMAL moment LP on y (two measures on a grid whose Chebyshev
    moments of order <= d agree), refined by an exchange step.  The grid value is a lower bound on
    gamma_d.  The LP duals give a polynomial shift r; the exact piecewise evaluation of
    max(L - r) + max(r - U) (critical points of each polynomial piece) is an upper bound.
(3) E_d(L) bracketed the same way; checks gamma_d <= 2 E_d and gamma_{2k+1} = gamma_{2k}.
(4) Exact rational certificate for gamma_10 = 0: an even polynomial rho = y^2 q(y) of degree 10
    with L <= rho <= U on [-1,1], verified by Sturm root counting in exact arithmetic (sympy).
"""
import numpy as np
from numpy.polynomial import chebyshev as C, polynomial as P
from scipy.optimize import linprog
import sympy as sp

y1, eta, epsv = 0.38, 0.05, 0.02
b, bp, c = 2 * y1, 2 * eta + 2 * (1 - eta) * (1 - y1), 1 + eta + epsv
z1, k = 2 * eta * y1 / bp, 2 * (1 - eta) * y1


def u(z):
    z = np.abs(z)
    return np.where(z <= z1, bp ** 2 * z ** 2 / (4 * eta), (bp * z + k) ** 2 / 4 - (1 - eta) * y1 ** 2)


def Lf(y):
    a = np.abs(y)
    return np.where(a <= y1, y * y, 2 * y1 * a - y1 * y1)


def Uf(y):
    a = np.abs(y)
    return -eta * y * y - (1 - eta) * np.maximum(a - y1, 0) ** 2 + c * y * y


# pieces on which L and U are polynomials (monomial coefficients, low to high)
PIECES = [(-1.0, -y1, [-y1 * y1, -2 * y1, 0.0], [-(1 - eta) * y1 ** 2, -2 * (1 - eta) * y1, c - eta - (1 - eta)]),
          (-y1, y1, [0.0, 0.0, 1.0], [0.0, 0.0, c - eta]),
          (y1, 1.0, [-y1 * y1, 2 * y1, 0.0], [-(1 - eta) * y1 ** 2, 2 * (1 - eta) * y1, c - eta - (1 - eta)])]


def exact_max(poly_fn_on_piece):
    """max over [-1,1] of a function that is a polynomial (numpy Polynomial) on each piece."""
    best, arg = -np.inf, None
    for (a, bb, cl, cu) in PIECES:
        p = poly_fn_on_piece(cl, cu)
        cands = [a, bb] + [r.real for r in p.deriv().roots() if abs(r.imag) < 1e-9 and a < r.real < bb]
        for t in cands:
            v = p(t)
            if v > best:
                best, arg = v, t
    return best, arg


def gamma_d(d, M=801, rounds=30):
    grid = set(np.cos(np.linspace(0, np.pi, M)).tolist()) | {y1, -y1, 0.0}
    for it in range(rounds):
        y = np.array(sorted(grid)); m = len(y)
        T = C.chebvander(y, d)[:, 1:]                     # T_1..T_d
        # variables w1 (m), w2 (m); min sum w1 (-L) + sum w2 U
        cost = np.concatenate([-Lf(y), Uf(y)])
        Aeq = np.zeros((2 + d, 2 * m)); Aeq[0, :m] = 1; Aeq[1, m:] = 1
        Aeq[2:, :m] = T.T; Aeq[2:, m:] = -T.T
        beq = np.zeros(2 + d); beq[:2] = 1
        res = linprog(cost, A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
        lb_grid = res.fun                                 # >= LB_true, so -lb_grid <= gamma_d
        ck = res.eqlin.marginals[2:]
        # reduced costs: -L - sum ck T_k >= a1 and U + sum ck T_k >= a2  ->  r = -sum ck T_k
        r_cheb = np.concatenate([[0.0], -ck])
        r_poly = C.Chebyshev(r_cheb).convert(kind=P.Polynomial)
        m1, a1 = exact_max(lambda cl, cu: P.Polynomial(cl) - r_poly)      # max (L - r)
        m2, a2 = exact_max(lambda cl, cu: r_poly - P.Polynomial(cu))      # max (r - U)
        up = m1 + m2
        lo = -lb_grid
        if up - lo < 1e-11:
            break
        grid |= {float(a1), float(a2), float(-a1), float(-a2)}
    return lo, up, it + 1


def E_d(d, M=801, rounds=40):
    grid = set(np.cos(np.linspace(0, np.pi, M)).tolist()) | {y1, -y1}
    for it in range(rounds):
        y = np.array(sorted(grid)); m = len(y)
        V = C.chebvander(y, d); kk = V.shape[1]
        A = np.vstack([np.hstack([-V, -np.ones((m, 1))]), np.hstack([V, -np.ones((m, 1))])])
        rhs = np.concatenate([-Lf(y), Lf(y)])
        cc = np.zeros(kk + 1); cc[-1] = 1
        res = linprog(cc, A_ub=A, b_ub=rhs, bounds=[(None, None)] * kk + [(0, None)], method="highs")
        lo = res.fun
        rp = C.Chebyshev(res.x[:kk]).convert(kind=P.Polynomial)
        m1, a1 = exact_max(lambda cl, cu: P.Polynomial(cl) - rp)
        m2, a2 = exact_max(lambda cl, cu: rp - P.Polynomial(cl))
        up = max(m1, m2)
        if up - lo < 1e-11:
            break
        grid |= {float(a1), float(a2)}
    return lo, up


def certificate_d10():
    """Max-margin even q of degree 8 in the band for rho = y^2 q; then exact verification."""
    y = np.concatenate([np.linspace(1e-4, y1, 2000), np.linspace(y1, 1, 4000)])
    s = 1 - y1 / y
    lowq = np.where(y <= y1, 1.0, 1 - s ** 2)
    upq = np.where(y <= y1, 1 + epsv, 1 + epsv - (1 - eta) * s ** 2)
    V = np.stack([y ** (2 * j) for j in range(5)], axis=1)         # q = sum a_j y^{2j}, j = 0..4
    m = len(y)
    # variables a_0..a_4, t; max t:  V a - lowq >= t,  upq - V a >= t
    A = np.vstack([np.hstack([-V, np.ones((m, 1))]), np.hstack([V, np.ones((m, 1))])])
    rhs = np.concatenate([-lowq, upq])
    cc = np.zeros(6); cc[-1] = -1
    res = linprog(cc, A_ub=A, b_ub=rhs, bounds=[(None, None)] * 6, method="highs")
    a, margin = res.x[:5], res.x[5]
    # exact check with rational coefficients
    Y = sp.symbols("y")
    Y1, ETA, EPS = sp.Rational(19, 50), sp.Rational(1, 20), sp.Rational(1, 50)
    aq = [sp.Rational(int(round(ai * 10 ** 9)), 10 ** 9) for ai in a]
    q = sum(aq[j] * Y ** (2 * j) for j in range(5))
    checks = [("q - 1 on [0, y1]", q - 1, 0, Y1),
              ("1 + eps_v - q on [0, y1]", 1 + EPS - q, 0, Y1),
              ("y^2 q - (2 y1 y - y1^2) on [y1, 1]", sp.expand(Y ** 2 * q - 2 * Y1 * Y + Y1 ** 2), Y1, 1),
              ("U - y^2 q on [y1, 1]", sp.expand((1 + EPS) * Y ** 2 - (1 - ETA) * (Y - Y1) ** 2 - Y ** 2 * q), Y1, 1)]
    out = []
    for name, expr, lo, hi in checks:
        poly = sp.Poly(expr, Y)
        nroots = poly.count_roots(lo, hi)                           # exact (Sturm), closed interval
        mid = expr.subs(Y, (sp.Rational(lo) + sp.Rational(hi)) / 2)
        mn = min(float(expr.subs(Y, t)) for t in np.linspace(float(lo), float(hi), 2001))
        out.append((name, nroots, mid > 0, mn))
    return a, margin, aq, out


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    ys = rng.uniform(-1, 1, 4000)
    xs = np.linspace(-1, 1, 20001); zs = np.linspace(-1, 1, 20001)
    eL = max(abs(-np.min(y1 * y1 * xs ** 2 + b * xs * yy) - Lf(yy)) for yy in ys[:400])
    eU = max(abs(c * yy * yy + np.min(u(zs) + bp * yy * zs) - Uf(yy)) for yy in ys[:400])
    print("(1) partial minima vs brute force (400 random y, 20001-point grids): |L err| <= %.1e, |U err| <= %.1e" % (eL, eU))
    print("    max(U - L) on 2e5 points = %.6f  (claimed eps_v + eta (1-y1)^2 = %.6f)"
          % (np.max(Uf(np.linspace(-1, 1, 200001)) - Lf(np.linspace(-1, 1, 200001))), epsv + eta * (1 - y1) ** 2))
    print("(2)-(3) gamma_d by primal moment LP [grid lower, exact-evaluation upper]; E_d(L) likewise")
    res = {}
    for d in range(2, 13):
        glo, gup, its = gamma_d(d)
        elo, eup = E_d(d)
        res[d] = (glo, gup, elo, eup)
        print("  d=%2d  gamma_d in [%.8f, %.8f] (%d rounds)   E_d in [%.8f, %.8f]   2E_d - gamma_d >= %.2e   2E_d - 0.0392 = %+.5f"
              % (d, glo, gup, its, elo, eup, 2 * elo - gup, 2 * elo - (epsv + eta * (1 - y1) ** 2)))
    for kk in range(1, 6):
        print("  gamma_%d - gamma_%d: upper-bound difference %.1e" % (2 * kk + 1, 2 * kk, res[2 * kk + 1][1] - res[2 * kk][1]))
    print("(4) exact certificate for gamma_10 = 0")
    a, margin, aq, out = certificate_d10()
    print("  LP margin in the q-band: %.6f; q(y) = sum a_j y^(2j), a = %s" % (margin, np.array2string(a, precision=9)))
    print("  rational coefficients (denominator 1e9):", [str(t) for t in aq])
    for name, nroots, midpos, mn in out:
        print("  %-38s roots in closed interval: %d; positive at midpoint: %s; min on 2001 points %.3e" % (name, nroots, midpos, mn))
