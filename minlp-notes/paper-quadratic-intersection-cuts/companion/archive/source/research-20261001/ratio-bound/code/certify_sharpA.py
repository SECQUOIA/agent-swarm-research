"""Exact certificate for Theorem B (family A part): in the family
    sbar = (0, 0, eps), p1 = (1, -1, 0), p2 = (1, -2, 0), p3 = (1, 1, 1), costs (1, 1, 1),
no orbit set (family A) containing sbar in its interior contains the simplex T_r with
r = RHO * sqrt(eps) / z_K, for every eps with H := RHO / sqrt(eps) >= H0.

Normalized frame (Lemma N of the note): sbar -> (0,0,1), the vertices of T_r become
P1 = (RHO, -RHO, 1), P2 = (RHO, -2 RHO, 1), P3 = (RHO, RHO, 1 + H), and the orbit sets
containing sbar in their interior are C_X = {s : sym(X M(s)) >= 0} with sym(X) > 0.
Certificate: PSD Y0 != 0, Y1, Y2, Y3 with Y0 + M(P1) Y1 + M(P2) Y2 + M(P3) Y3 = 0.  Then for
such X, 0 = tr(X sum_i M_i Y_i) = sum_i <sym(X M_i), Y_i> and the first term is > 0, so some
sym(X M(P_j)) is not PSD.

Construction: Y1, Y2 rational (from a numerical SDP for the limit H = infinity, rounded);
Y3(H) = [[theta/H^2, sigma(H)/H], [sigma(H)/H, n]] with sigma(H) chosen so that the sum is
symmetric; Y0(H) = -(sum).  Everything is a rational function of u = 1/H and is checked exactly
(sympy) for 0 < u <= 1/H0 by Sturm-type root counting."""
import sympy as sp
import numpy as np
import cvxpy as cp

RHO = sp.Integer(160)
K = 2
NFIX = 0.1          # Y3[1,1] = n
KMAX = 60.0         # bound on |kappa| = |R21 - R12 - RHO n| in the limit SDP (keeps theta small)
H0_CANDIDATES = [2 * 10 ** 5, 5 * 10 ** 5, 10 ** 6, 2 * 10 ** 6, 5 * 10 ** 6, 10 ** 7]


def limit_sdp(rho):
    """H = infinity: maximize the margin of Y0 = -[[R11, R21], [R21, R22 + n]] (R = M1 Y1 + M2 Y2)
    with n = NFIX fixed and |kappa| <= KMAX."""
    M1 = np.array([[1, rho], [-rho, 1.0]])
    M2 = np.array([[1, rho], [-K * rho, 1.0]])
    Y1 = cp.Variable((2, 2), symmetric=True)
    Y2 = cp.Variable((2, 2), symmetric=True)
    t = cp.Variable()
    R = M1 @ Y1 + M2 @ Y2
    Y0 = -cp.bmat([[R[0, 0], R[1, 0]], [R[1, 0], R[1, 1] + NFIX]])
    kap = R[1, 0] - R[0, 1] - rho * NFIX
    cons = [Y1 >> 0, Y2 >> 0, Y0 >> t * np.eye(2), cp.trace(Y0) == 1, cp.abs(kap) <= KMAX]
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    return Y1.value, Y2.value, NFIX, float(t.value)


def rat(x, den=10 ** 6):
    return sp.Rational(int(round(x * den)), den)


def main():
    y1, y2, nn, t = limit_sdp(float(RHO))
    print('limit SDP margin (min eigenvalue)', t)
    shift = sp.Rational(1, 10 ** 6)                          # keeps the rounded Y1, Y2 positive definite
    Y1 = sp.Matrix([[rat(y1[0, 0]), rat(y1[0, 1])], [rat(y1[0, 1]), rat(y1[1, 1])]]) + shift * sp.eye(2)
    Y2 = sp.Matrix([[rat(y2[0, 0]), rat(y2[0, 1])], [rat(y2[0, 1]), rat(y2[1, 1])]]) + shift * sp.eye(2)
    n = sp.nsimplify(nn)
    rho = RHO
    M1 = sp.Matrix([[1, rho], [-rho, 1]])
    M2 = sp.Matrix([[1, rho], [-K * rho, 1]])
    R = M1 * Y1 + M2 * Y2
    sig_inf = R[1, 0] - R[0, 1] - rho * n
    theta = sp.nsimplify(2 * (sig_inf ** 2 + 1) / n)          # theta * n >= 2 (sig_inf^2 + 1)
    u = sp.symbols('u', positive=True)                        # u = 1/H
    H = 1 / u
    sigma = sig_inf + rho * theta * u ** 2
    Y3 = sp.Matrix([[theta * u ** 2, sigma * u], [sigma * u, n]])
    M3 = sp.Matrix([[1 + H, rho], [rho, 1]])
    T = sp.simplify(R + M3 * Y3)
    asym = sp.simplify(T[0, 1] - T[1, 0])
    Y0 = -sp.Matrix([[T[0, 0], T[1, 0]], [T[1, 0], T[1, 1]]])
    checks = {}
    checks['Y1 PD'] = Y1[0, 0] > 0 and Y1.det() > 0
    checks['Y2 PD'] = Y2[0, 0] > 0 and Y2.det() > 0
    checks['sum symmetric (identically in u)'] = sp.simplify(asym) == 0
    def positive_on(expr, u0):
        """expr (rational in u) > 0 for all u in (0, u0]"""
        num, den = sp.fraction(sp.together(sp.expand(expr)))
        num, den = sp.Poly(sp.expand(num), u), sp.Poly(sp.expand(den), u)
        ok = True
        for poly in (num, den):
            # no root in [0, u0] and positive (same sign) at u0: then sign is constant on (0, u0]
            nroots = poly.count_roots(0, u0)
            ok = ok and nroots == 0
        return ok and (num.eval(u0) * den.eval(u0) > 0)
    H0 = None
    for Hc in H0_CANDIDATES:
        u0 = sp.Rational(1, Hc)
        if positive_on(theta * n - sigma ** 2, u0) and positive_on(Y0[0, 0], u0) and positive_on(Y0.det(), u0):
            H0 = sp.Integer(Hc)
            break
    if H0 is None:
        print('no H0 candidate works'); return
    u0 = 1 / H0
    checks['Y3: theta*u^2 * n - (sigma*u)^2 > 0 on (0, 1/H0]'] = positive_on(theta * n - sigma ** 2, u0)
    checks['Y3[1,1] = n > 0'] = n > 0
    checks['Y0[0,0] > 0 on (0, 1/H0]'] = positive_on(Y0[0, 0], u0)
    checks['det Y0 > 0 on (0, 1/H0]'] = positive_on(Y0.det(), u0)
    # identity check at a random rational u
    uu = sp.Rational(1, 123457)
    Ms = [sp.eye(2), M1, M2, M3.subs(u, uu)]
    Ys = [Y0.subs(u, uu), Y1, Y2, Y3.subs(u, uu)]
    checks['sum_i M_i Y_i = 0 at u = 1/123457'] = sp.simplify(sum((Mi * Yi for Mi, Yi in zip(Ms, Ys)), sp.zeros(2, 2))) == sp.zeros(2, 2)
    print('RHO =', RHO, ' H0 =', H0, ' (eps0 = (RHO/H0)^2 =', (RHO / H0) ** 2, ')')
    print('Y1 =', Y1.tolist())
    print('Y2 =', Y2.tolist())
    print('n =', n, ' theta =', theta, ' sigma_inf =', sig_inf)
    print('Y0(H = infinity) =', Y0.subs(u, 0).tolist())
    for k, v in checks.items():
        print(k, ':', 'PASS' if v else 'FAIL')
    print('ALL PASS' if all(checks.values()) else 'SOME FAIL')


if __name__ == '__main__':
    main()
