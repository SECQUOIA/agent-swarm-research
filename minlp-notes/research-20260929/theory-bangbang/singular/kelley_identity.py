"""Exact symbolic checks of the calibration identities on singular arcs.

Setting: xdot = g = a(x) + b(x) u (scalar u), cost int l0(x) + l1(x) u dt,
H = l0 + l1 u + psi^T g, sigma0(x, psi) = l1 + b^T psi, w = -grad_x sigma0.
Total derivative along the extremal flow: D F = F_x g + F_psi (-H_x).

Checks (polynomial identities in x, psi, u, exact, sympy):
 (1) d sigma/dt does not depend on u (order >= 1).
 (2) K_cal := b^T wdot - w^T b_x g + 2 w^T g_x b + b^T H_xx b, which is
     b^T M(t,u*) b for any symmetric P with P b = w along the arc
     (M = Pdot + g_x^T P + P g_x + H_xx), equals -d/du (d^2 sigma/dt^2)
     (Kelley's generalized Legendre-Clebsch quantity), identically.
 (3) The same with P kept symbolic: impose P b = w by solving for some
     entries, P b_dot + Pdot b = w_dot for Pdot, and compare b^T M b.
 (4) Vector control (m = 2): B^T W - W^T B = -(d/du_j sigma_i dot)_{ij}
     antisymmetrized, i.e. tangency P B = W forces Goh's condition.
Random integer polynomial data, several seeds, n = 2 and n = 3.
"""
import random
import sys

import sympy as sp


def randpoly(xs, deg, rng, cmax=3):
    terms = [sp.Integer(1)]
    for d in range(1, deg + 1):
        for mono in sp.itermonomials(xs, d, d):
            terms.append(mono)
    return sum(rng.randint(-cmax, cmax) * t for t in terms)


def check_scalar(n, seed):
    rng = random.Random(seed)
    xs = sp.symbols("x0:%d" % n)
    ps = sp.symbols("p0:%d" % n)
    u = sp.Symbol("u")
    X = sp.Matrix(xs)
    Psi = sp.Matrix(ps)
    a = sp.Matrix([randpoly(xs, 2, rng) for _ in range(n)])
    b = sp.Matrix([randpoly(xs, 2, rng) for _ in range(n)])
    l0 = randpoly(xs, 3, rng)
    l1 = randpoly(xs, 2, rng)
    g = a + b * u
    H = l0 + l1 * u + (Psi.T * g)[0]
    Hx = sp.Matrix([sp.diff(H, xi) for xi in xs])

    def D(F):
        return sp.expand(sum(sp.diff(F, xs[i]) * g[i] for i in range(n))
                         - sum(sp.diff(F, ps[i]) * Hx[i] for i in range(n)))

    sigma = sp.expand(l1 + (b.T * Psi)[0])
    sd = D(sigma)
    ok1 = sp.expand(sp.diff(sd, u)) == 0
    sdd = D(sd)
    KGLC = sp.expand(-sp.diff(sdd, u))
    w = -sp.Matrix([sp.diff(sigma, xi) for xi in xs])
    wdot = sp.Matrix([D(wi) for wi in w])
    bx = b.jacobian(X)
    gx = g.jacobian(X)
    Hxx = sp.hessian(H, xs)
    Kcal = sp.expand((b.T * wdot)[0] - (w.T * bx * g)[0] + 2 * (w.T * gx * b)[0] + (b.T * Hxx * b)[0])
    ok2 = sp.expand(Kcal - KGLC) == 0
    ok2u = sp.expand(sp.diff(Kcal, u)) == 0
    # c1 (u-slope of b^T grad^2_x r b for quadratic S)
    sxx = sp.hessian(sigma, xs)
    c1 = sp.expand(2 * (w.T * bx * b)[0] + (b.T * sxx * b)[0])
    return ok1, ok2, ok2u, len(str(KGLC)), c1 != 0


def check_symbolic_P(seed):
    """n = 2, P symbolic: P = [[p11, p12], [p12, p22]], impose P b = w
    (two linear equations), Pdot symbolic with Pdot b = wdot - P bdot."""
    rng = random.Random(seed)
    n = 2
    xs = sp.symbols("x0:2")
    ps = sp.symbols("p0:2")
    u = sp.Symbol("u")
    X = sp.Matrix(xs)
    Psi = sp.Matrix(ps)
    a = sp.Matrix([randpoly(xs, 2, rng) for _ in range(n)])
    b = sp.Matrix([randpoly(xs, 1, rng) for _ in range(n)])
    l0 = randpoly(xs, 2, rng)
    l1 = randpoly(xs, 2, rng)
    g = a + b * u
    H = l0 + l1 * u + (Psi.T * g)[0]
    Hx = sp.Matrix([sp.diff(H, xi) for xi in xs])

    def D(F):
        return sp.expand(sum(sp.diff(F, xs[i]) * g[i] for i in range(n))
                         - sum(sp.diff(F, ps[i]) * Hx[i] for i in range(n)))

    sigma = sp.expand(l1 + (b.T * Psi)[0])
    sdd = D(D(sigma))
    KGLC = sp.expand(-sp.diff(sdd, u))
    w = -sp.Matrix([sp.diff(sigma, xi) for xi in xs])
    p11, p12, p22, q11, q12, q22 = sp.symbols("p11 p12 p22 q11 q12 q22")
    P = sp.Matrix([[p11, p12], [p12, p22]])
    Pd = sp.Matrix([[q11, q12], [q12, q22]])
    solP = sp.solve(list(P * b - w), [p11, p22], dict=True)[0]
    P = P.subs(solP)
    bdot = sp.Matrix([D(bi) for bi in b])
    wdot = sp.Matrix([D(wi) for wi in w])
    solPd = sp.solve(list(Pd * b - (wdot - P * bdot)), [q11, q22], dict=True)[0]
    Pd = Pd.subs(solPd)
    gx = g.jacobian(X)
    Hxx = sp.hessian(H, xs)
    M = Pd + gx.T * P + P * gx + Hxx
    bMb = sp.simplify(sp.together((b.T * M * b)[0]))
    return sp.simplify(bMb - KGLC) == 0


def check_goh(n, seed):
    rng = random.Random(seed)
    xs = sp.symbols("x0:%d" % n)
    ps = sp.symbols("p0:%d" % n)
    us = sp.symbols("u0:2")
    X = sp.Matrix(xs)
    Psi = sp.Matrix(ps)
    a = sp.Matrix([randpoly(xs, 2, rng) for _ in range(n)])
    bs = [sp.Matrix([randpoly(xs, 2, rng) for _ in range(n)]) for _ in range(2)]
    l0 = randpoly(xs, 2, rng)
    l1s = [randpoly(xs, 2, rng) for _ in range(2)]
    g = a + bs[0] * us[0] + bs[1] * us[1]
    H = l0 + l1s[0] * us[0] + l1s[1] * us[1] + (Psi.T * g)[0]
    Hx = sp.Matrix([sp.diff(H, xi) for xi in xs])

    def D(F):
        return sp.expand(sum(sp.diff(F, xs[i]) * g[i] for i in range(n))
                         - sum(sp.diff(F, ps[i]) * Hx[i] for i in range(n)))

    sig = [sp.expand(l1s[i] + (bs[i].T * Psi)[0]) for i in range(2)]
    G = sp.Matrix(2, 2, lambda i, j: sp.expand(sp.diff(D(sig[i]), us[j])))
    W = sp.Matrix.hstack(*[-sp.Matrix([sp.diff(sig[i], xi) for xi in xs]) for i in range(2)])
    B = sp.Matrix.hstack(*bs)
    lhs = sp.expand(B.T * W - W.T * B)
    # G is antisymmetric (control-affine), and B^T W - W^T B = -G - ... check sign
    okG_anti = sp.expand(G + G.T) == sp.zeros(2, 2)
    ok_minus = sp.expand(lhs + G) == sp.zeros(2, 2)
    ok_plus = sp.expand(lhs - G) == sp.zeros(2, 2)
    return okG_anti, ok_minus, ok_plus


if __name__ == "__main__":
    out = []
    for n in (2, 3):
        for seed in range(3):
            r = check_scalar(n, seed)
            out.append(("scalar n=%d seed=%d" % (n, seed), r))
            print("scalar n=%d seed=%d: sigma_dot u-free %s, K_cal == -d_u sigma_ddot %s, "
                  "K_cal u-free %s, len(K) %d, c1 nonzero %s" % ((n, seed) + r), flush=True)
    for seed in range(3):
        r = check_symbolic_P(seed)
        print("symbolic P, n=2 seed=%d: b^T M b == K_GLC: %s" % (seed, r), flush=True)
    for n in (2, 3):
        for seed in range(2):
            r = check_goh(n, seed)
            print("Goh m=2 n=%d seed=%d: G antisymmetric %s, B^T W - W^T B == -G %s, == +G %s"
                  % ((n, seed) + r), flush=True)
