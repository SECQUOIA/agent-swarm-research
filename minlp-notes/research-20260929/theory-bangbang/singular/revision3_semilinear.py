"""Round-3 revision check for singular-arcs.md (review
reviews/singular-arcs-confirm-r2.md, item S1).  Symbolic (sympy, exact).

Question: are E2 and catmix outside Felgenhauer's semilinear class
(as read by the round-1 confirmation review: Mayer cost, xdot = f(t,x) + B(t)u
with B independent of the state) "in every gauge"?

Part E2: the gauge F = -k1 x1^2/2 - k2 x1 x2 (the note's gauge: add dF/dt to
  the integrand, subtract F(x_T) - F(x_0) from the terminal cost).  Prints the
  new l0, l1, terminal cost and w, and computes the Kelley quantity
  K = -d/du (sigma'') from the Hamiltonian flow in the old and new
  formulations (not from a second-derivative shortcut).
Part catmix: the reachable set of theta, the sign of b on it, and the
  formulation xi = int_0^theta dtheta'/b plus the gauge dF/dxi = -theta.
  Checks that l1 = 0 and the input column is 1 (so w = 0), that the singular
  point equation is 111 theta^2 - 22 theta + 1 = 0 as in Section 5.2, and that
  the Kelley quantity at theta_s is 2 sqrt(10) as in Section 5.2.
Usage: python3 revision3_semilinear.py
"""
import sympy as sp


def kelley(l0, l1, a, b, xs, ps, u):
    """-d/du of sigma'' along the Hamiltonian flow, for xdot = a + b u,
    running cost l0 + l1 u, H = l0 + l1 u + p.(a + b u), sigma = l1 + p.b."""
    n = len(xs)
    H = l0 + l1 * u + sum(ps[i] * (a[i] + b[i] * u) for i in range(n))
    xdot = [sp.diff(H, p) for p in ps]
    pdot = [-sp.diff(H, x) for x in xs]

    def ddt(e):
        return sum(sp.diff(e, xs[i]) * xdot[i] + sp.diff(e, ps[i]) * pdot[i] for i in range(n))

    sigma = l1 + sum(ps[i] * b[i] for i in range(n))
    s1 = sp.simplify(ddt(sigma))
    assert sp.simplify(sp.diff(s1, u)) == 0, "sigma' contains u"
    s2 = sp.expand(ddt(s1))
    return sigma, s1, s2, sp.simplify(-sp.diff(s2, u))


def part_e2():
    x1, x2, p1, p2, u, k1, k2 = sp.symbols("x1 x2 p1 p2 u k1 k2", real=True)
    Kt = 1 - 2 * k2
    X = sp.Matrix([x1, x2])
    g = sp.Matrix([u, x1 - x2])
    a, b = [0, x1 - x2], [1, 0]
    l0 = (x1 ** 2 + x2 ** 2) / 2
    l1 = k1 * x1 + k2 * x2
    Phi = sp.Rational(1, 2) * ((k2 - k1) * x1 ** 2 + Kt * x2 ** 2)
    F = -k1 * x1 ** 2 / 2 - k2 * x1 * x2
    dF = sp.expand((sp.Matrix([F]).jacobian(X) * g)[0])
    integrand = sp.expand(l0 + l1 * u + dF)
    l1n = sp.expand(integrand.coeff(u, 1))
    l0n = sp.expand(integrand.coeff(u, 0))
    Phin = sp.expand(Phi - F)
    F0 = F.subs({x1: 1, x2: 0})
    print("E2: dF/dt = %s" % dF)
    print("E2: new l1 = %s; new l0 = %s; new l0 - old l0 = %s" % (l1n, sp.factor(l0n), sp.factor(l0n - l0)))
    print("E2: new terminal cost Phi - F(x_T) = %s (contains k1: %s); constant F(x_0) = %s"
          % (Phin, Phin.has(k1), F0))
    # w = -(grad l1 + b_x^T psi); b constant, so w = -grad l1
    print("E2: w in the new gauge = %s (b = e1 constant, so B is state-independent after adding a cost state)"
          % [-sp.diff(l1n, v) for v in (x1, x2)])
    _, _, _, K_old = kelley(l0, l1, a, b, [x1, x2], [p1, p2], u)
    _, _, _, K_new = kelley(l0n, l1n, a, b, [x1, x2], [p1, p2], u)
    print("E2: Kelley quantity -d/du sigma'' : old formulation %s, new formulation %s, 1 - 2 k2 = %s; equal: %s"
          % (K_old, K_new, Kt, sp.simplify(K_old - Kt) == 0 and sp.simplify(K_new - Kt) == 0))
    # the gauge identity itself: integrand difference is exactly dF/dt, so the two costs agree for every control
    print("E2: (new integrand) - (old integrand) - dF/dt = %s" % sp.simplify(integrand - (l0 + l1 * u) - dF))


def part_catmix():
    th, u, p = sp.symbols("theta u p", real=True)
    a = th ** 2 - th
    b = 1 - 10 * th - th ** 2
    l0, l1 = -th, th
    print("catmix: thetadot at theta = 1/11: %s; at theta = 0: %s"
          % (sp.factor((a + b * u).subs(th, sp.Rational(1, 11))), sp.factor((a + b * u).subs(th, 0))))
    print("catmix: b(0) = %s, b(1/11) = %s, b' = %s (< 0 on [0, 1/11]); roots of b: %s"
          % (b.subs(th, 0), b.subs(th, sp.Rational(1, 11)), sp.diff(b, th), sp.solve(b, th)))
    # formulation (xi, gauge): xi' (theta) = 1/b, xidot = a/b + u; dF/dxi = -theta.
    # Written in theta as the coordinate, with d/dxi = b d/dtheta.
    at = a / b                        # drift in xi
    l0n = sp.simplify(l0 + (-th) * at)  # l0 + F_xi * drift
    l1n = sp.simplify(l1 + (-th) * 1)   # l1 + F_xi * 1
    print("catmix (xi, gauge): input column 1; l1 = %s; l0 = %s" % (l1n, sp.factor(l0n)))
    # Hamiltonian in xi with costate q: H = l0n + q (at + u); sigma = q.
    # d/dt of a function e(theta, q): e_theta * thetadot + e_q * qdot, with
    # thetadot = b (at + u) and qdot = -dH/dxi = -b dH/dtheta.
    q = sp.symbols("q", real=True)
    H = l0n + q * (at + u)
    thdot = sp.simplify(b * (at + u))
    qdot = sp.simplify(-b * sp.diff(H, th))

    def ddt(e):
        return sp.diff(e, th) * thdot + sp.diff(e, q) * qdot

    s1 = sp.simplify(ddt(q))
    s2 = sp.simplify(ddt(s1))
    num = sp.factor(sp.numer(sp.together(s1.subs(q, 0))))
    print("catmix (xi, gauge): sigma' on sigma = q = 0 has numerator %s" % num)
    ths = (11 - sp.sqrt(10)) / 111
    K = sp.nsimplify(sp.simplify(-sp.diff(s2, u).subs({q: 0, th: ths})))
    print("catmix (xi, gauge): K = -d/du sigma'' at theta_s = (11 - sqrt(10))/111, q = 0: %s = %.12f (2 sqrt(10) = %.12f)"
          % (sp.radsimp(K), float(K), float(2 * sp.sqrt(10))))
    # the same in the theta formulation of the note, sigma = l1 + b psi
    psi = sp.symbols("psi", real=True)
    _, s1t, s2t, Kt = kelley(l0, l1, [a], [b], [th], [psi], u)
    psis = sp.Rational(5, 52) - 7 * sp.sqrt(10) / 65
    print("catmix (theta, note's formulation): K at (theta_s, psi_s) = %s"
          % sp.radsimp(sp.simplify(Kt.subs({th: ths, psi: psis}))))


if __name__ == "__main__":
    part_e2()
    part_catmix()
