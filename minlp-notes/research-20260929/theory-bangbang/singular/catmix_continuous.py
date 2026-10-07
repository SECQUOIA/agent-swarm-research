"""catmix in the projective coordinate: continuous singular-arc data and the
control curvature of tangential calibrations under several one-step schemes.

Reduction (exact): with m = x1 + x2 and theta = x2/m,
  mdot = -(1-u) theta m,
  thetadot = a(theta) + b(theta) u,  a = theta^2 - theta,  b = 1 - 10 theta - theta^2,
  J + 1 = m(1) = exp(C),  C = int_0^1 (l0 + l1 u) dt,  l0 = -theta, l1 = theta.
So catmix is equivalent (monotone transform) to the 1-D Lagrange problem
min C.  A calibration phi(t, theta) of the reduced problem gives the Mayer
calibration S = m exp(phi), whose residual is S times the reduced residual.

Part 1: exact singular point, u_s, psi_s, w, the tangential curvature
P_s = w/b, the Kelley quantity K = -d/du sigma_ddot, b*w, and the slope c1
of the quadratic-calibration Hessian in u (Section 2 of singular-arcs.md).
Part 2: for a general 1-D problem at a singular point, the per-step control
curvature d^2 rho/du^2 of a tangential calibration, as a series in h, for
explicit Euler and for the exact flow (piecewise-constant control).
Part 3: the same for catmix under Euler-in-theta, Euler-in-x (2-D Euler,
reduced) and the COPS trapezoidal rule (Cayley map in y = Q(u)x, reduced).
"""
import sympy as sp

th, u, h, psi = sp.symbols("theta u h psi", real=True)


def part1():
    a = th ** 2 - th
    b = 1 - 10 * th - th ** 2
    l0, l1 = -th, th
    # singular point: sigma = l1 + b psi = 0, sigma_dot = 0
    psi_s_expr = -l1 / b
    # sigma_dot as function of (theta, psi): psi [a,b] + l1' a - l0' b with [a,b] = b'a - a'b
    brk = sp.diff(b, th) * a - sp.diff(a, th) * b
    sd = psi * brk + sp.diff(l1, th) * a - sp.diff(l0, th) * b
    Fth = sp.simplify(sp.numer(sp.together(sd.subs(psi, psi_s_expr))))
    print("sigma_dot on sigma=0, numerator:", sp.factor(Fth))
    roots = sp.solve(Fth, th)
    print("roots:", roots, [sp.N(r) for r in roots])
    ths = [r for r in roots if 0 < sp.N(r) < 0.1][0]
    ths = sp.nsimplify(ths)
    us = sp.simplify((-a / b).subs(th, ths))
    psis = sp.simplify(psi_s_expr.subs(th, ths))
    w = -(sp.diff(l1, th) + sp.diff(b, th) * psi)
    ws = sp.simplify(w.subs({th: ths, psi: psis}))
    Ps = sp.simplify(ws / b.subs(th, ths))
    # Kelley: sigma_ddot along the extremal flow with control u
    H = l0 + l1 * u + psi * (a + b * u)
    g = a + b * u
    Hth = sp.diff(H, th)

    def D(F):
        return sp.diff(F, th) * g - sp.diff(F, psi) * Hth

    sigma = l1 + b * psi
    sdd = D(D(sigma))
    K = sp.simplify(-sp.diff(sdd, u).subs({th: ths, psi: psis}))
    # c1 = 2 w b' b + b^2 sigma0''
    c1 = sp.simplify((2 * w * sp.diff(b, th) * b + b ** 2 * sp.diff(sigma, th, 2)).subs({th: ths, psi: psis}))
    bs = sp.simplify(b.subs(th, ths))
    # M(u*) = Pdot + 2 g_th P + H_thth; on the stationary arc Pdot = 0, g_th(u*) = a' + b' u*
    Mstar = sp.simplify((2 * (sp.diff(a, th) + sp.diff(b, th) * u) * Ps + sp.diff(H, th, 2)).subs({th: ths, psi: psis, u: us}))
    vals = dict(theta_s=ths, u_s=us, psi_s=psis, b_s=bs, w_s=ws, P_s=Ps, K=K, bw=sp.simplify(bs * ws),
                c1=c1, Mstar=Mstar, Mstar_b2=sp.simplify(Mstar * bs ** 2))
    for k_, v in vals.items():
        print("%-9s = %-45s = %.12g" % (k_, sp.nsimplify(sp.radsimp(v)), float(sp.N(v, 30))))
    # quadratic-class vertex condition: b^2 M(t,u) = K + (u - u_s) c1 at u = 0, 1
    for uv in (0, 1):
        val = K + (uv - us) * c1
        print("K + (u - u_s) c1 at u = %d: %.6g" % (uv, float(sp.N(val))))
    return vals


def lie_series(g, F, order):
    """F(theta(h)) for thetadot = g(theta) (u fixed), up to h^order."""
    out = F
    term = F
    for k in range(1, order + 1):
        term = sp.diff(term, th) * g
        out += h ** k / sp.factorial(k) * term
    return sp.expand(out)


def cost_series(g, ell, order):
    """int_0^h ell(theta(s)) ds up to h^order."""
    out = 0
    term = ell
    for k in range(1, order + 1):
        out += h ** k / sp.factorial(k) * term
        term = sp.diff(term, th) * g
    return sp.expand(out)


def part2():
    """generic 1-D data as polynomials of degree 3 in e = theta - theta_s with
    symbolic Taylor coefficients; singular point conditions imposed."""
    e = th
    A = sp.symbols("aa0:4")
    B = sp.symbols("bb0:4")
    L0 = sp.symbols("lz0:4")
    L1 = sp.symbols("lo0:4")
    a = sum(A[i] * e ** i / sp.factorial(i) for i in range(4))
    b = sum(B[i] * e ** i / sp.factorial(i) for i in range(4))
    l0 = sum(L0[i] * e ** i / sp.factorial(i) for i in range(4))
    l1 = sum(L1[i] * e ** i / sp.factorial(i) for i in range(4))
    ps = -L1[0] / B[0]
    us = -A[0] / B[0]
    w = -(L1[1] + B[1] * ps)
    P = w / B[0]
    # sigma_dot = 0 at the point: psi [a,b] + l1' a - l0' b = 0 -> solve for L0[1]
    brk0 = B[1] * A[0] - A[1] * B[0]
    sd0 = ps * brk0 + L1[1] * A[0] - L0[1] * B[0]
    L01 = sp.solve(sd0, L0[1])[0]
    # Kelley K = -d_u sigma_ddot at the point
    H = l0 + l1 * u + psi * (a + b * u)
    g = a + b * u
    Hth = sp.diff(H, th)

    def D(F):
        return sp.diff(F, th) * g - sp.diff(F, psi) * Hth

    sigma = l1 + b * psi
    K = sp.simplify(-sp.diff(D(D(sigma)), u).subs({th: 0, psi: ps}).subs(L0[1], L01))
    print("generic 1-D: K =", K)
    # tangential calibration phi = psi_s e + P e^2/2 + C3 e^3/6 (time-invariant part)
    C3 = sp.Symbol("C3")
    phi = ps * e + P * e ** 2 / 2 + C3 * e ** 3 / 6
    ell = l0 + l1 * u
    res = {}
    # Euler: rho = h ell + phi(theta + h g) - phi(theta)
    rhoE = h * ell + phi.subs(th, th + h * g) - phi
    # exact flow
    rhoX = cost_series(g, ell, 5) + lie_series(g, phi, 5) - phi
    for name, rho in (("Euler", rhoE), ("exact flow", rhoX)):
        ruu = sp.diff(rho, u, 2).subs({th: 0}).subs(u, us).subs(L0[1], L01)
        ser = sp.series(sp.expand(ruu), h, 0, 5).removeO()
        c2 = sp.simplify(ser.coeff(h, 2))
        c3 = sp.simplify(ser.coeff(h, 3))
        c4 = sp.simplify(ser.coeff(h, 4))
        res[name] = (c2, c3, c4)
        print("%s: d2rho/du2 = h^2 [%s] + h^3 [%s] + h^4 [...]" % (name, sp.factor(c2), sp.factor(c3)))
        print("   h^2 coefficient minus b*w:", sp.simplify(c2 - B[0] * w))
        print("   h^3 coefficient / K:", sp.simplify(c3 / K))
    return res


def part3(vals):
    ths, us, psis, Ps = vals["theta_s"], vals["u_s"], vals["psi_s"], vals["P_s"]
    a = th ** 2 - th
    b = 1 - 10 * th - th ** 2
    g = a + b * u
    C3 = sp.Symbol("C3")
    e = th - ths
    phi = psis * e + Ps * e ** 2 / 2 + C3 * e ** 3 / 6
    schemes = {}
    # Euler in theta (reduced Lagrange problem)
    schemes["Euler-theta"] = h * (-th + th * u) + phi.subs(th, th + h * g) - phi
    # exact flow
    schemes["exact flow"] = cost_series(g, -th + th * u, 5) + lie_series(g, phi, 5) - phi
    # Euler in x (2-D), reduced: m' = m (1 - h(1-u)theta), theta' as below
    mfac = 1 - h * (1 - u) * th
    thn = (th + h * (u * (1 - 11 * th) - (1 - u) * th)) / mfac
    schemes["Euler-x"] = sp.log(mfac) + phi.subs(th, thn) - phi
    # trapezoid (Cayley in y), reduced
    Am = sp.Matrix([[-u, 10 * u], [u, -10 * u - (1 - u)]])
    I2 = sp.eye(2)
    Cm = (I2 - h / 2 * Am).inv() * (I2 + h / 2 * Am)
    yv = sp.Matrix([1 - th, th])
    z = Cm * yv
    cfac = z[0] + z[1]
    thc = z[1] / cfac
    schemes["trapezoid (Cayley)"] = sp.log(cfac) + phi.subs(th, thc) - phi
    for name, rho in schemes.items():
        ruu = sp.diff(rho, u, 2)
        f = sp.lambdify((h, C3), ruu.subs({th: ths, u: us}), "mpmath")
        import mpmath as mp
        mp.mp.dps = 40
        # fit series coefficients numerically: evaluate at small h
        hs = [mp.mpf(2) ** (-k) for k in range(12, 16)]
        vals_h = [f(hh, 0) for hh in hs]
        c2 = [v / hh ** 2 for v, hh in zip(vals_h, hs)]
        # Richardson for c2 and c3
        c2lim = 2 * c2[-1] - c2[-2]
        c3est = (c2[-1] - c2lim) / hs[-1]
        dC3 = f(hs[-1], 1) - f(hs[-1], 0)
        print("%-20s d2rho/du2 ~ h^2 * %.10f + h^3 * %.6f   (C3 sensitivity at h=2^-15: %.2e)"
              % (name, float(c2lim), float(c3est), float(dC3)))


if __name__ == "__main__":
    print("== Part 1: catmix singular point (reduced problem) ==")
    vals = part1()
    print("\n== Part 2: generic 1-D singular point ==")
    part2()
    print("\n== Part 3: catmix schemes ==")
    part3(vals)
