"""Independent checks of Section 2.5 (WALL) of robust-chains.md. No code shared with the note.

u(t) = 1.022 t + 0.189 t^2 + 1.774 t^3 + 1.086 t^4, b = 0.962, f_n = sum u(x_i) + b sum x_i x_{i+1} on [-1,1]^n.
Parts:
  basic   c, min u', m, phi grid min, phi(-1,-1)-m, diagonal; grid DP (3001 points) + coordinate polish for n=2..16
  family  closed-form Delta(s,t) at 40/30 digits; dual bound for the fixed balanced split on H_j (affine shifts)
  a0      a period-2 class-(a0) split: odd bonds b(x+1)(y+1)-b, even bonds H = u(x)+u(y)+bxy-b(x+y);
          checks min H = H(-1,c) (grid + exact critical points), which proves the walls are global minimizers for all even n
  endfrust  u = t^2 + 1.5 t, b = 1.2: DP minimizers, mirror, restricted ends
"""
import sys
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import minimize_scalar, brentq

UC = np.array([0.0, 1.022, 0.189, 1.774, 1.086]); B = 0.962


def u(t, uc=UC):
    return P.polyval(t, uc)


def croot():
    du = P.polyder(UC); f = lambda t: P.polyval(t, du) - 2 * B
    return brentq(f, -1, 1, xtol=1e-15)


def dp(n, uc=UC, b=B, N=3001, restrict=None):
    g = np.linspace(-1, 1, N); ug = u(g, uc)
    V = ug.copy() if restrict is None else np.where(restrict(g), ug, np.inf)
    back = []
    for _ in range(n - 1):
        M = V[:, None] + b * np.outer(g, g)
        j = M.argmin(axis=0); back.append(j); V = M[j, np.arange(N)] + ug
    if restrict is not None:
        V = np.where(restrict(g), V, np.inf)
    k = int(V.argmin()); path = [k]
    for j in reversed(back):
        k = int(j[k]); path.append(k)
    x = g[np.array(path[::-1])]
    return float(V.min()), x


def fval(x, uc=UC, b=B):
    x = np.asarray(x, float); return float(u(x, uc).sum() + b * (x[:-1] * x[1:]).sum())


def polish(x, uc=UC, b=B, sweeps=200):
    x = x.copy()
    for _ in range(sweeps):
        old = fval(x, uc, b)
        for i in range(len(x)):
            def fi(t):
                y = x.copy(); y[i] = t; return fval(y, uc, b)
            r = minimize_scalar(fi, bounds=(-1, 1), method="bounded", options={"xatol": 1e-13})
            if r.fun < fi(x[i]):
                x[i] = r.x
        if old - fval(x, uc, b) < 1e-15:
            break
    return x


def basic():
    c = croot()
    du = P.polyder(UC); tt = np.linspace(-1, 1, 1000001)
    print(f"c = {c:.12f}; min u' on 1e6+1 points = {P.polyval(tt, du).min():.6f}; u(-1) = {u(-1.0):.6f}")
    phi = lambda x, y: 0.5 * (u(x) + u(y)) + B * x * y
    g = np.linspace(-1, 1, 3001); X, Y = np.meshgrid(g, g, indexing="ij"); Ph = phi(X, Y)
    m = phi(-1.0, c); k = np.unravel_index(Ph.argmin(), Ph.shape)
    print(f"m = phi(-1,c) = {m:.10f}; grid min {Ph.min():.10f} at ({g[k[0]]:.4f},{g[k[1]]:.4f}); phi(-1,-1)-m = {phi(-1.0,-1.0)-m:.6f}; "
          f"min diag - m = {np.diag(Ph).min()-m:.6f}")
    for n in range(2, 17):
        v, x = dp(n); xp = polish(x); fs = fval(xp)
        if n % 2 == 0:
            ref = (n // 2 + 1) * u(-1.0) + (n // 2 - 1) * u(c) + B * (1 - (n - 2) * c)
        else:
            ref = (n + 1) // 2 * u(-1.0) + (n - 1) // 2 * u(c) - B * (n - 1) * c
        print(f"n={n:2d} DP+polish f* = {fs:.12f}, closed form = {ref:.12f}, diff = {fs-ref:+.2e}, x = {np.round(xp,4).tolist()}")


def family():
    import mpmath as mp
    mp.mp.dps = 50
    uc = [mp.mpf(s) for s in ("0", "1.022", "0.189", "1.774", "1.086")]; b = mp.mpf("0.962")
    U = lambda t: sum(cf * t ** i for i, cf in enumerate(uc))
    dU = lambda t: sum(i * cf * t ** (i - 1) for i, cf in enumerate(uc) if i)
    c = mp.findroot(lambda t: dU(t) - 2 * b, mp.mpf("0.3377"))
    phi = lambda x, y: (U(x) + U(y)) / 2 + b * x * y
    m = phi(-1, c)
    def Delta(s, t):
        yb = -s + (1 - s) * c; p = s * (1 + c) / (1 + t)
        assert 0 <= p <= 1 and -1 <= yb <= c and -1 <= t <= c
        # means: middle y-mean = -s + (1-s)c = yb ; middle z-mean = s c - (1-s) ; right mean = p t - (1-p)
        assert abs((s * c - (1 - s)) - (p * t - (1 - p))) < mp.mpf(10) ** -45
        return m + p * phi(-1, -1) - phi(-1, yb) - p * phi(-1, t)
    s = mp.mpf(779) / 10000; t = mp.mpf(467) / 2000
    print("c =", mp.nstr(c, 35))
    print("Delta(779/10000, 467/2000) =", mp.nstr(Delta(s, t), 30))
    print("Delta(31/400, ybar) =", mp.nstr(Delta(mp.mpf(31) / 400, -mp.mpf(31) / 400 + (1 - mp.mpf(31) / 400) * c), 12))
    # optimize over (s,t) in float
    from scipy.optimize import minimize
    cf = float(c)
    def Df(v):
        s, t = v; yb = -s + (1 - s) * cf; p = s * (1 + cf) / (1 + t)
        ph = lambda x, y: 0.5 * (u(x) + u(y)) + B * x * y
        return -(ph(-1.0, cf) + p * ph(-1.0, -1.0) - ph(-1.0, yb) - p * ph(-1.0, t))
    r = minimize(Df, [0.08, 0.2], method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-16, "maxiter": 10000})
    print(f"float optimum of the closed form: s = {r.x[0]:.6f}, t = {r.x[1]:.6f}, Delta = {-r.fun:.10f}")
    # dual bound of the fixed balanced split on H_j: LB >= max over (ly, lz) of
    #   min_y [phi(-1,y) + ly y] + min_{y,z} [phi(y,z) - ly y + lz z] + min_z [phi(z,-1) - lz z]   (y,z in [-1,c])
    ph = lambda x, y: 0.5 * (u(x) + u(y)) + B * x * y
    gy = np.linspace(-1, cf, 4001)
    def min1(fun):
        v = fun(gy); k = int(v.argmin())
        lo, hi = gy[max(k - 1, 0)], gy[min(k + 1, len(gy) - 1)]
        r = minimize_scalar(fun, bounds=(lo, hi), method="bounded", options={"xatol": 1e-14})
        return min(float(v.min()), float(r.fun))
    G2 = np.linspace(-1, cf, 1201); Yg, Zg = np.meshgrid(G2, G2, indexing="ij"); PH = ph(Yg, Zg)
    def min2(ly, lz):
        V = PH - ly * Yg + lz * Zg; k = np.unravel_index(V.argmin(), V.shape)
        from scipy.optimize import minimize as mz
        r = mz(lambda v: ph(v[0], v[1]) - ly * v[0] + lz * v[1], [G2[k[0]], G2[k[1]]], bounds=[(-1, cf), (-1, cf)], method="L-BFGS-B",
               options={"ftol": 1e-16, "gtol": 1e-12})
        return min(float(V.min()), float(r.fun))
    true = ph(-1.0, -1.0) + 2 * ph(-1.0, cf)
    def LB(v):
        ly, lz = v
        return min1(lambda y: ph(-1.0, y) + ly * y) + min2(ly, lz) + min1(lambda z: ph(z, -1.0) - lz * z)
    best = None
    for ly in np.linspace(-0.6, 0.6, 25):
        for lz in np.linspace(-0.6, 0.6, 25):
            val = LB((ly, lz))
            if best is None or val > best[0]:
                best = (val, ly, lz)
    r = minimize(lambda v: -LB(v), [best[1], best[2]], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 4000})
    print(f"fixed balanced split on H_j, dual (affine shifts): best LB - f* = {-r.fun - true:+.9f} at (ly, lz) = ({r.x[0]:.6f}, {r.x[1]:.6f}); "
          f"so the true gap on H_j lies in [Delta_family, {true + r.fun:.9f}]")


def a0():
    c = croot()
    H = lambda x, y: u(x) + u(y) + B * x * y - B * (x + y)
    Hc = H(-1.0, c)
    g = np.linspace(-1, 1, 4001); X, Y = np.meshgrid(g, g, indexing="ij"); V = H(X, Y)
    k = np.unravel_index(V.argmin(), V.shape)
    print(f"H(-1,c) = {Hc:.12f}; grid (4001^2) min H = {V.min():.12f} at ({g[k[0]]:.4f},{g[k[1]]:.4f}); min H - H(-1,c) on grid = {V.min()-Hc:+.3e}")
    # exact-ish: all critical points of H in the box, edges and corners (sympy, exact rationals, real roots isolated)
    import sympy as sp
    x, y = sp.symbols("x y")
    uc = [sp.Rational(0), sp.Rational(1022, 1000), sp.Rational(189, 1000), sp.Rational(1774, 1000), sp.Rational(1086, 1000)]
    b = sp.Rational(962, 1000)
    us = lambda t: sum(cf * t ** i for i, cf in enumerate(uc))
    Hs = sp.expand(us(x) + us(y) + b * x * y - b * (x + y))
    cands = []
    for xv in (-1, 1):
        for yv in (-1, 1):
            cands.append((sp.Integer(xv), sp.Integer(yv)))
    for fixed in (-1, 1):
        for var, other in ((y, x), (x, y)):
            h1 = sp.Poly(sp.diff(Hs.subs(other, fixed), var), var)
            for r in sp.real_roots(h1):
                if -1 <= r <= 1:
                    cands.append((sp.Integer(fixed), r) if other == x else (r, sp.Integer(fixed)))
    Hx = sp.Poly(sp.diff(Hs, x), x, y); Hy = sp.Poly(sp.diff(Hs, y), x, y)
    res = sp.Poly(sp.resultant(Hx.as_expr(), Hy.as_expr(), y), x)
    nint = 0
    for rx in sp.real_roots(res):
        if not (-1 <= rx <= 1):
            continue
        rxf = sp.Float(sp.N(rx, 40), 40)
        py = sp.Poly(sp.N(Hy.as_expr().subs(x, rxf), 40), y)
        for ry in py.nroots(n=30):
            if abs(sp.im(ry)) < 1e-20 and -1 <= sp.re(ry) <= 1:
                if abs(sp.N(Hx.as_expr().subs({x: rxf, y: sp.re(ry)}), 30)) < 1e-15:
                    cands.append((rxf, sp.re(ry))); nint += 1
    vals = sorted((float(sp.N(Hs.subs({x: a, y: bb}), 30)), float(sp.N(a)), float(sp.N(bb))) for a, bb in cands)
    print(f"candidates (corners, edge critical points, {nint} interior critical points): smallest values:")
    for v in vals[:6]:
        print(f"   H = {v[0]:.12f} at ({v[1]:.6f}, {v[2]:.6f}); minus H(-1,c) = {v[0]-Hc:+.3e}")
    # odd bond G = b(x+1)(y+1) - b >= -b trivially; end factors u(x1) + b x2 (x1+1) >= u(-1) iff u' >= b on [-1,1]
    du = P.polyder(UC); tt = np.linspace(-1, 1, 1000001)
    print(f"end factor condition: min u' - b = {P.polyval(tt, du).min() - B:.6f} > 0")
    for n in range(4, 17, 2):
        lb = 2 * u(-1.0) - (n // 2 - 2) * B + (n // 2 - 1) * Hc
        ref = (n // 2 + 1) * u(-1.0) + (n // 2 - 1) * u(c) + B * (1 - (n - 2) * c)
        print(f"n={n}: sum of factor minima of this (a0) split = {lb:.12f}; wall value = {ref:.12f}; diff = {lb-ref:+.1e}")


def endfrust():
    uc = np.array([0.0, 1.5, 1.0]); b = 1.2
    for n in range(3, 13):
        v, x = dp(n, uc, b); xp = polish(x, uc, b); fs = fval(xp, uc, b)
        vr, xr = dp(n, uc, b, restrict=lambda g: g <= -0.9)
        xrp = xr  # grid value is an upper bound of the restricted optimum; also polish within the restriction
        print(f"n={n:2d} f* = {fs:.8f} x = {np.round(xp,4).tolist()} mirror diff = {fval(xp[::-1],uc,b)-fs:+.1e}; "
              f"both ends <= -0.9 (grid DP): {vr - fs:+.6f}")


if __name__ == "__main__":
    {"basic": basic, "family": family, "a0": a0, "endfrust": endfrust}[sys.argv[1]]()
