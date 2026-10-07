"""Independent checks of the revised chiral-chain numbers (Sections 4.3, 4.6, 5) of robust-chains.md.
W(x,y) = (a/2)(x^2+y^2) + b x y + (g/2)(x y^2 - x^2 y), a = b + ev; f_k = sum W + (a/2)(x_1^2 + x_k^2)."""
import sys
import numpy as np
from scipy.optimize import minimize, brentq

b, g, ev = 0.6, 0.3, 0.05; a = b + ev


def identities():
    import sympy as sp
    x, y, t, B, Gm, E = sp.symbols("x y t b g ev", real=True)
    A = B + E
    W = A / 2 * (x**2 + y**2) + B * x * y + Gm / 2 * (x * y**2 - x**2 * y)
    h = lambda z: -Gm / 2 * z**3
    lhs = sp.expand(W + h(x) - h(y))
    rhs = (B / 2 - Gm) * (x + y)**2 + E / 2 * (x**2 + y**2) + Gm / 2 * (x + y)**2 * (1 + y) + Gm / 2 * (x + y)**2 * (1 - x)
    print("C.5 bracket identity residual:", sp.expand(lhs - rhs))
    print("C.1 bracket identity residual:", sp.expand(lhs - ((x + y)**2 * (B / 2 + Gm / 2 * (y - x)) + E / 2 * (x**2 + y**2))))
    print("end terms:", sp.expand(A / 2 * t**2 - h(t) - ((A - Gm) / 2 * t**2 + Gm / 2 * t**2 * (1 + t))),
          sp.expand(A / 2 * t**2 + h(t) - ((A - Gm) / 2 * t**2 + Gm / 2 * t**2 * (1 - t))))
    # quadratic-box variant: (x+y)^2 (1+y) = (x+y)^2 (1+y)^2/2 + (x+y)^2 (1-y^2)/2
    print("quadratic-box variant residual:", sp.expand((x + y)**2 * (1 + y) - ((x + y)**2 * (1 + y)**2 / 2 + (x + y)**2 * (1 - y**2) / 2)))
    # telescoping for n = 6: f_6 = sum brackets + ends
    X = sp.symbols("x1:7")
    f6 = sum(W.subs({x: X[i], y: X[i + 1]}, simultaneous=True) for i in range(5)) + A / 2 * (X[0]**2 + X[5]**2)
    tel = sum(lhs.subs({x: X[i], y: X[i + 1]}, simultaneous=True) for i in range(5)) + (A / 2 * X[0]**2 - h(X[0])) + (A / 2 * X[5]**2 + h(X[5]))
    print("telescoping residual (n = 6):", sp.expand(f6 - tel))


def lam():
    xs = np.linspace(-1, 1, 1601); X, Y = np.meshgrid(xs, xs, indexing="ij")
    for (bb, gg, ee) in [(0.6, 0.3, 0.05), (0.6, 0.3, 0.29), (1.0, 0.5, 0.01), (0.5, 0.05, 0.02)]:
        aa = bb + ee
        dx = (aa - gg * Y) * X + Y * (bb + gg / 2 * Y); dy = (aa + gg * X) * Y + X * (bb - gg / 2 * X)
        print(f"(b,g,ev)=({bb},{gg},{ee}): max|dxW|={np.abs(dx).max():.6f} max|dyW|={np.abs(dy).max():.6f} a+b+g/2={aa+bb+gg/2:.6f}")


def analytic():
    ginf = (g - ev)**2 / (4 * g); q = (g - ev) / (2 * g); L = 2 * a + 2 * b + g
    print(f"g_inf={ginf:.7f} q={q:.6f} aq={a*q:.6f} Lambda={L}")
    for k in [7, 8, 10, 15, 20, 30, 50, 100]:
        print(f"k={k}: analytic base {np.exp(((k-1)*ginf - a*q)/(2*L*(k+1))):.5f}; with Lambda=3.4: {np.exp(((k-1)*ginf - a*q)/(2*3.4*(k+1))):.5f}")
    print(f"limit exp(g_inf/(2 Lambda)) = {np.exp(ginf/(2*L)):.5f}")
    for k, gam in [(4, 0.01154), (5, 0.05027), (6, 0.09756), (7, 0.14772)]:
        print(f"P2 k={k}: transport base with LP gap {np.exp(gam/(2*L*(k+1))):.5f}")
    for k, gam in [(6, 0.17975), (7, 0.22046)]:
        print(f"P1 k={k}: transport base with LP gap {np.exp(gam/(2*L*(k+1))):.5f}")
    print(f"1/0.8314 = {1/0.8314:.4f}; per variable (k=7) {(1/0.83139)**(1/8):.5f}")


def leftover():
    # sup_{0<d<=1} (1-d)/2 exp(M d^2), M = mu c: critical points solve 2 M d (1-d) = 1
    def sup(M):
        cands = [0.5]
        disc = 1 - 2 / M
        if disc >= 0:
            for d in ((1 + np.sqrt(disc)) / 2, (1 - np.sqrt(disc)) / 2):
                if 0 < d <= 1:
                    cands.append((1 - d) / 2 * np.exp(M * d * d))
        return max(cands)
    mu = 2.112
    for name, cc in [("a", a), ("a+(b+g)/2", a + (b + g) / 2), ("a+b+g", a + b + g)]:
        print(f"mu={mu} c={cc:.3f} [{name}]: sup = {sup(mu*cc):.5f}")
    mstar = brentq(lambda m: sup(m * (a + b + g)) - 1, 2.2, 2.5, xtol=1e-12)
    print(f"interior sup reaches 1 at mu = {mstar:.5f}; at that mu the end constant gives {sup(mstar*(a+(b+g)/2)):.4f}")
    # window bookkeeping: pins at multiples of k+1 that are <= n
    bad = 0
    for k in range(1, 12):
        for n in range(1, 200):
            pins = list(range(k + 1, n + 1, k + 1))
            idx = [i for i in range(1, n + 1) if i not in pins]
            runs = []; cur = []
            for i in idx:
                if cur and i != cur[-1] + 1:
                    runs.append(cur); cur = []
                cur.append(i)
            if cur:
                runs.append(cur)
            G = (n + 1) // (k + 1); r = n - G * (k + 1)
            full = sum(1 for R in runs if len(R) == k); short = [len(R) for R in runs if len(R) != k]
            exp_short = [r] if 1 <= r <= k - 1 else []
            if full != G or short != exp_short:
                bad += 1
    print(f"window bookkeeping G = floor((n+1)/(k+1)), leftover r = n - G(k+1) in [1,k-1]: mismatches over k<=11, n<200: {bad}")


def fk(s):
    s = np.asarray(s)
    return a * np.sum(s * s) + b * np.sum(s[:-1] * s[1:]) + 0.5 * g * np.sum(s[:-1] * s[1:] * (s[1:] - s[:-1]))


def corner():
    rng = np.random.default_rng(12345)
    # sanity: monotonicity => factor minima at the lower corner, random positive corner boxes
    worst = 0.0
    tt = np.linspace(0, 1, 201)
    for _ in range(200):
        s = rng.uniform(0, 1, 2)
        X, Y = np.meshgrid(np.linspace(s[0], 1, 101), np.linspace(s[1], 1, 101), indexing="ij")
        Wv = a / 2 * (X**2 + Y**2) + b * X * Y + g / 2 * (X * Y**2 - X**2 * Y)
        w0 = a / 2 * (s[0]**2 + s[1]**2) + b * s[0] * s[1] + g / 2 * (s[0] * s[1]**2 - s[0]**2 * s[1])
        worst = min(worst, Wv.min() - w0)
    print(f"W on positive corner boxes: min over box - value at lower corner >= {worst:.2e} (200 random boxes)")
    # mu0 by a different optimizer: s = 1 - exp(-z) parametrization, Powell + BFGS, random starts
    for k in [4, 5, 6, 7, 10, 20]:
        def obj(z):
            s = 1 - np.exp(-np.abs(z))
            return np.sum(np.log(2.0 / (1.0 - s))) / fk(s)
        best = np.inf; bs = None
        nst = 30 if k <= 7 else 8
        for t in range(nst):
            z0 = -np.log(1 - rng.uniform(0.3, 0.97, size=k))
            r = minimize(obj, z0, method="Powell", options={"xtol": 1e-10, "ftol": 1e-13, "maxiter": 200000})
            r = minimize(obj, r.x, method="BFGS", options={"gtol": 1e-11})
            if r.fun < best:
                best = r.fun; bs = 1 - np.exp(-np.abs(r.x))
        out = f"k={k}: mu0 = {best:.4f}, s = {np.round(bs, 4).tolist() if k <= 7 else ('mid', round(float(bs[k//2]), 4), 'end', round(float(bs[0]), 4))}"
        gam = {4: (0.01154, 0.07558), 5: (0.05027, 0.1122), 6: (0.09756, 0.17975), 7: (0.14772, 0.22046)}
        if k in gam:
            out += f"; ceilings per variable: P2 {np.exp(best*gam[k][0]/(k+1)):.4f}, P1 {np.exp(best*gam[k][1]/(k+1)):.4f}"
        print(out, flush=True)
    ss = np.linspace(0.5, 0.99, 490001); v = np.log(2 / (1 - ss)) / ((a + b) * ss**2); j = v.argmin()
    print(f"uniform bulk: min = {v[j]:.4f} at s = {ss[j]:.4f}; exp(min * g_inf) = {np.exp(v[j]*(g-ev)**2/(4*g)):.4f}")


def sdp():
    """Own order-2 sparse moment relaxation (pair cliques, linear box constraints localized in every clique)."""
    import cvxpy as cp
    for n in (5, 7):
        mons = [(i, j) for d in range(5) for i in range(d + 1) for j in [d - i]]
        Y = [dict((m, cp.Variable()) for m in mons if m != (0, 0)) for _ in range(n - 1)]
        def y(e, m):
            return 1.0 if m == (0, 0) else Y[e][m]
        cons = []
        b2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]; b1 = [(0, 0), (1, 0), (0, 1)]
        for e in range(n - 1):
            M = cp.bmat([[y(e, (p[0] + q[0], p[1] + q[1])) if True else 0 for q in b2] for p in b2])
            cons.append(M >> 0)
            for lin in [((1, (0, 0)), (1, (1, 0))), ((1, (0, 0)), (-1, (1, 0))), ((1, (0, 0)), (1, (0, 1))), ((1, (0, 0)), (-1, (0, 1)))]:
                L = cp.bmat([[sum(cf * y(e, (p[0] + q[0] + sh[0], p[1] + q[1] + sh[1])) for cf, sh in lin) for q in b1] for p in b1])
                cons.append(L >> 0)
            if e < n - 2:
                for d in range(1, 5):
                    cons.append(Y[e][(0, d)] == Y[e + 1][(d, 0)])
        obj = sum(a / 2 * (y(e, (2, 0)) + y(e, (0, 2))) + b * y(e, (1, 1)) + g / 2 * (y(e, (1, 2)) - y(e, (2, 1))) for e in range(n - 1))
        obj = obj + a / 2 * y(0, (2, 0)) + a / 2 * y(n - 2, (0, 2))
        pr = cp.Problem(cp.Minimize(obj), cons); pr.solve(solver="CLARABEL")
        print(f"n={n}: own order-2 sparse moment relaxation value {pr.value:.3e} ({pr.status})")


if __name__ == "__main__":
    {"identities": identities, "lam": lam, "analytic": analytic, "leftover": leftover, "corner": corner, "sdp": sdp}[sys.argv[1]]()
