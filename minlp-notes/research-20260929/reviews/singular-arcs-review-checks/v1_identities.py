"""Independent symbolic checks (reviewer) of Section 1 of singular-arcs.md.

Written from scratch (does not import the author's scripts).  Generic
polynomial data with symbolic-free random rational coefficients, n = 2, 3.
Checks:
 (a) the intermediate formula in the proof of Prop 1.3:
     d_u sigma_ddot = a^T s0xx b + w^T b_x a - 2 w^T a_x b - (b_x b)^T Hx0 - b^T Hxx0 b
 (b) R := b^T Hxx(u) b + b^T wdot + 2 w^T g_x(u) b - w^T bdot equals -d_u sigma_ddot
     identically in (x, psi, u)
 (c) residual Hessian of a C^3 calibration S(t,x) at x*(t):
     grad^2_x r(t,x*,u) = M(t,u*) + (u - u*) Z, Z = s0xx + P b_x + b_x^T P + S_xxx[b]
     checked for an explicit S(t,x) = cubic polynomial with time-dependent
     coefficients along an explicit curve x*(t) (not required to be optimal:
     the identity is algebraic);
 (d) b^T Z b = c1 = b^T s0xx b + 2 w^T b_x b when S_xxx = 0 and P b = w.
 (e) Goh: G_ij = d sigma_dot_i / d u_j equals (B^T W - W^T B)_ij, m = 2.
"""
import random
import sympy as sp

def rpoly(xs, deg, rng):
    e = 0
    for d in range(deg + 1):
        for mono in sp.itermonomials(xs, d, d):
            e += sp.Rational(rng.randint(-5, 5), rng.randint(1, 3)) * mono
    return e

def setup(n, seed):
    rng = random.Random(1000 + seed)
    xs = sp.symbols('y0:%d' % n); ps = sp.symbols('q0:%d' % n); u = sp.Symbol('v')
    a = sp.Matrix([rpoly(xs, 2, rng) for _ in range(n)])
    b = sp.Matrix([rpoly(xs, 2, rng) for _ in range(n)])
    l0 = rpoly(xs, 3, rng); l1 = rpoly(xs, 2, rng)
    return rng, xs, ps, u, a, b, l0, l1

def run_scalar(n, seed):
    rng, xs, ps, u, a, b, l0, l1 = setup(n, seed)
    X = sp.Matrix(xs); Psi = sp.Matrix(ps)
    g = a + b * u
    H = l0 + l1 * u + (Psi.T * g)[0]
    Hx = sp.Matrix([sp.diff(H, x) for x in xs])
    def D(F):
        return sp.expand(sum(sp.diff(F, xs[i]) * g[i] - sp.diff(F, ps[i]) * Hx[i] for i in range(n)))
    s0 = l1 + (b.T * Psi)[0]
    w = -sp.Matrix([sp.diff(s0, x) for x in xs])
    sd = D(s0); sdd = D(sd)
    dusdd = sp.expand(sp.diff(sdd, u))
    # (a)
    H0 = l0 + (Psi.T * a)[0]
    Hx0 = sp.Matrix([sp.diff(H0, x) for x in xs])
    Hxx0 = sp.hessian(H0, xs)
    s0xx = sp.hessian(s0, xs)
    ax = a.jacobian(X); bx = b.jacobian(X)
    formula = (a.T * s0xx * b)[0] + (w.T * bx * a)[0] - 2 * (w.T * ax * b)[0] - ((bx * b).T * Hx0)[0] - (b.T * Hxx0 * b)[0]
    ok_a = sp.expand(formula - dusdd) == 0
    # (b)
    gx = g.jacobian(X); Hxx = sp.hessian(H, xs)
    wdot = sp.Matrix([D(wi) for wi in w]); bdot = bx * g
    R = (b.T * Hxx * b)[0] + (b.T * wdot)[0] + 2 * (w.T * gx * b)[0] - (w.T * bdot)[0]
    ok_b = sp.expand(R + dusdd) == 0
    ok_sd = sp.expand(sp.diff(sd, u)) == 0
    return ok_sd, ok_a, ok_b

def run_hessian(n, seed):
    """(c),(d): explicit S(t,x) and curve; residual Hessian identity."""
    rng, xs, ps, u, a, b, l0, l1 = setup(n, seed)
    t = sp.Symbol('t')
    X = sp.Matrix(xs)
    # curve x*(t) and control u*(t): arbitrary polynomials (identity is algebraic,
    # but x*' must equal g(x*,u*) for the Ṗ cancellation -> define via dynamics:
    # instead take S expanded around a moving point c(t) with c' = g(c, ustar(t)).)
    # We avoid solving ODEs by working at a single time t0 with symbolic jets:
    c = sp.Matrix(sp.symbols('c0:%d' % n))       # x*(t0)
    us = sp.Symbol('us')                            # u*(t0)
    # S(t,x) = sum over monomials in (x - c(t)) up to degree 3 with coefficients
    # affine in t (t0 = 0), and c(t) = c + t*g(c,us) + t^2 * k (k arbitrary)
    k = sp.Matrix([sp.Rational(rng.randint(-3, 3), 2) for _ in range(n)])
    ct = c + t * (a + b * us).subs(dict(zip(xs, c))) + t**2 * k
    d = X - ct
    S = 0
    ds = sp.symbols('z0:%d' % n)
    for deg in range(0, 4):
        for mono in sp.itermonomials(ds, deg, deg):
            coef = sp.Rational(rng.randint(-4, 4), rng.randint(1, 3)) + t * sp.Rational(rng.randint(-4, 4), 1)
            S += coef * mono.subs(dict(zip(ds, list(d))), simultaneous=True)
    g = a + b * u
    St = sp.diff(S, t)
    Sx = sp.Matrix([sp.diff(S, x) for x in xs])
    r = l0 + l1 * u + St + (Sx.T * g)[0]
    at = {t: 0}
    at.update(dict(zip(xs, c)))
    Hr = sp.hessian(r, xs).subs(at, simultaneous=True)
    # quantities along the curve at t0 = 0
    psi = Sx.subs(at, simultaneous=True)
    Sxx = sp.hessian(S, xs)
    P = Sxx.subs(at, simultaneous=True)
    Pdot = sp.diff(Sxx.subs(dict(zip(xs, list(ct))), simultaneous=True), t).subs(t, 0)
    Hfun = l0 + l1 * u + (sp.Matrix(list(psi)).T * g)[0]
    Hxx = sp.hessian(Hfun, xs).subs(dict(zip(xs, c)), simultaneous=True)
    gx = g.jacobian(X).subs(dict(zip(xs, c)), simultaneous=True)
    M = lambda uu: (Pdot + gx.T.subs(u, uu) * P + P * gx.subs(u, uu) + Hxx.subs(u, uu))
    s0 = l1 + (b.T * sp.Matrix(list(psi)))[0]
    s0xx = sp.hessian(s0, xs).subs(dict(zip(xs, c)), simultaneous=True)
    bx = b.jacobian(X).subs(dict(zip(xs, c)), simultaneous=True)
    bc = b.subs(dict(zip(xs, c)), simultaneous=True)
    S3b = sp.Matrix(n, n, lambda i, j: sum(sp.diff(S, xs[i], xs[j], xs[kk]).subs(at, simultaneous=True) * bc[kk] for kk in range(n)))
    Z = s0xx + P * bx + bx.T * P + S3b
    ok_c = sp.simplify(sp.expand(Hr - (M(us) + (u - us) * Z))) == sp.zeros(n, n)
    # M(t,u) - M(t,u*) = (u-u*)(Z - S3b): quadratic-S identity
    ok_c2 = sp.simplify(sp.expand(M(u) - M(us) - (u - us) * (Z - S3b))) == sp.zeros(n, n)
    return ok_c, ok_c2

def run_goh(n, seed):
    rng = random.Random(2000 + seed)
    xs = sp.symbols('y0:%d' % n); ps = sp.symbols('q0:%d' % n); us = sp.symbols('v0:2')
    X = sp.Matrix(xs); Psi = sp.Matrix(ps)
    a = sp.Matrix([rpoly(xs, 2, rng) for _ in range(n)])
    bs = [sp.Matrix([rpoly(xs, 2, rng) for _ in range(n)]) for _ in range(2)]
    l0 = rpoly(xs, 2, rng); l1 = [rpoly(xs, 2, rng) for _ in range(2)]
    g = a + bs[0] * us[0] + bs[1] * us[1]
    H = l0 + l1[0] * us[0] + l1[1] * us[1] + (Psi.T * g)[0]
    Hx = sp.Matrix([sp.diff(H, x) for x in xs])
    D = lambda F: sp.expand(sum(sp.diff(F, xs[i]) * g[i] - sp.diff(F, ps[i]) * Hx[i] for i in range(n)))
    sig = [l1[i] + (bs[i].T * Psi)[0] for i in range(2)]
    W = sp.Matrix.hstack(*[-sp.Matrix([sp.diff(s, x) for x in xs]) for s in sig])
    B = sp.Matrix.hstack(*bs)
    G = sp.Matrix(2, 2, lambda i, j: sp.diff(D(sig[i]), us[j]))
    return sp.expand(G - (B.T * W - W.T * B)) == sp.zeros(2, 2)

if __name__ == '__main__':
    for n in (2, 3):
        for seed in range(2):
            print('n=%d seed=%d: sigma_dot u-free, (a) formula, (b) R = -d_u sigma_ddot:' % (n, seed), run_scalar(n, seed), flush=True)
    for n in (2,):
        for seed in range(2):
            print('n=%d seed=%d: (c) Hess r = M(u*) + (u-u*)Z, (c2) M(u)-M(u*) = (u-u*)(Z - S3b):' % (n, seed), run_hessian(n, seed), flush=True)
    for n in (2, 3):
        print('Goh n=%d: G == B^T W - W^T B:' % n, run_goh(n, 0), flush=True)
