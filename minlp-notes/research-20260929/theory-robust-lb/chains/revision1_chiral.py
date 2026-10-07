"""Revision 1 of robust-chains.md: checks for the chiral chain (Section 4 and Section 5).

  W(x, y) = (a/2)(x^2 + y^2) + b x y + (g/2)(x y^2 - x^2 y),  a = b + ev;  f_k = sum_e W + (a/2)(x_1^2 + x_k^2).

Commands:
  python3 revision1_chiral.py lambda       max over [-1,1]^2 of |d_x W| and |d_y W| (grid of 2001^2 points) against
                                           the closed form a + b + g/2, at several (b, g, ev) with g <= b/2
  python3 revision1_chiral.py analytic     fully analytic bases per variable of Theorem C.3(1):
                                           exp(((k-1) g_inf - a q) / (2 Lambda (k+1))), Lambda = 2a + 2b + g and 2a + 2b + 3g
  python3 revision1_chiral.py leftover     sup_{0<d<=1} ((1-d)/2) exp(mu c d^2) at mu = 2.112 for the separable constants
                                           c in {a, a + (b+g)/2, a + b + g}; all < 1 gives Phi_r(2.112) <= 1 for every r
  python3 revision1_chiral.py corner       exact positive-corner ceiling: on B = prod [s_j, 1] (s_j >= 0) every factor
                                           is nondecreasing, so V(B) = f_k(s) for every class; minimize
                                           mu(s) = sum_j log(2/(1-s_j)) / f_k(s) (multistart L-BFGS-B), compare with the
                                           column-generation lower bound on the optimal box, and print the ceilings
                                           exp(mu0 gamma_k / (k+1)) for the LP gamma_k of logs/chiral_bounds_P{1,2}.log
  python3 revision1_chiral.py sos          sympy: the reviewer's decomposition of the bracket of Proposition C.1 into
                                           SOS + SOS*(1+y) + SOS*(1-x), the end terms, and the quadratic-box variant;
                                           then a numerical order-2 sparse moment relaxation (pair cliques; cvxpy/Clarabel); as a control,
                                           the same relaxation sharing only x_i, x_i^2 between cliques (must show a gap)
Floating point except the sympy identities.
"""
import sys
import json
import numpy as np
from scipy.optimize import minimize

B0, G0, EV0 = 0.6, 0.3, 0.05


def lam():
    xs = np.linspace(-1, 1, 2001)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    for b, g, ev in [(0.6, 0.3, 0.05), (0.6, 0.3, 0.1), (0.6, 0.1, 0.05), (1.0, 0.5, 0.2), (0.4, 0.2, 0.01)]:
        a = b + ev
        dx = a * X + b * Y + 0.5 * g * (Y * Y - 2 * X * Y)
        dy = a * Y + b * X + 0.5 * g * (2 * X * Y - X * X)
        print(f"b={b} g={g} ev={ev}: max|d_x W| = {np.abs(dx).max():.6f}, max|d_y W| = {np.abs(dy).max():.6f}, "
              f"a+b+g/2 = {a + b + g / 2:.6f}; interior Lambda = 2a+2b+g = {2*a + 2*b + g:.4f}, "
              f"window-end Lambda = 2a+b+g/2 = {2*a + b + g/2:.4f}")


def analytic():
    b, g, ev = B0, G0, EV0
    a = b + ev; ginf = (g - ev) ** 2 / (4 * g); q = (g - ev) / (2 * g)
    print(f"g_inf = {ginf:.7f}, q = {q:.6f}, a q = {a*q:.6f}; window gap bound (k-1) g_inf - a q > 0 needs k >= {int(np.floor(a*q/ginf + 1)) + 1}")
    for Lname, L in [("2a+2b+g", 2 * a + 2 * b + g), ("2a+2b+3g", 2 * a + 2 * b + 3 * g)]:
        row = {}
        for k in [7, 8, 10, 15, 20, 30, 50, 100, 1000]:
            gam = (k - 1) * ginf - a * q
            row[k] = round(float(np.exp(gam / (2 * L * (k + 1)))), 5)
        print(f"Lambda = {Lname} = {L:.2f}: fully analytic base per variable by k: {row}; limit exp(g_inf/(2 Lambda)) = {np.exp(ginf/(2*L)):.5f}")
    print(f"with the LP window gap gamma_7 = 0.14772 and Lambda = 2.8: {np.exp(0.14772/(2*2.8*8)):.5f} per variable")


def sup_corner(mu, c, grid=np.linspace(0, 1, 200001)):
    d = grid[1:]
    v = (1 - d) / 2 * np.exp(mu * c * d * d)
    k = int(np.argmax(v))
    return float(v[k]), float(d[k])


def leftover():
    b, g, ev = B0, G0, EV0; a = b + ev; mu = 2.112
    for name, c in [("a (window of length 1)", a), ("a+(b+g)/2 (window ends)", a + (b + g) / 2), ("a+b+g (interior)", a + b + g)]:
        v, d = sup_corner(mu, c)
        print(f"mu = {mu}, c = {c:.3f} [{name}]: sup_d ((1-d)/2) exp(mu c d^2) = {v:.5f} at d = {d:.4f}")
    # the threshold of mu at which the interior constant reaches 1
    lo, hi = 2.112, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if sup_corner(mid, a + b + g)[0] < 1:
            lo = mid
        else:
            hi = mid
    print(f"the interior supremum stays below 1 for mu < {lo:.4f}")


def fk(s, a, b, g):
    s = np.asarray(s)
    return a * np.sum(s * s) + b * np.sum(s[:-1] * s[1:]) + 0.5 * g * np.sum(s[:-1] * s[1:] * (s[1:] - s[:-1]))


def corner_mu(k, b, g, ev, rng, nstart=40):
    a = b + ev
    def obj(s):
        return np.sum(np.log(2.0 / (1.0 - s))) / fk(s, a, b, g)
    best = (np.inf, None)
    for t in range(nstart):
        s0 = rng.uniform(0.5, 0.95, size=k) if t else np.full(k, 0.8)
        r = minimize(obj, s0, bounds=[(1e-3, 0.999)] * k, method="L-BFGS-B", options={"ftol": 1e-14, "gtol": 1e-10})
        if r.fun < best[0]:
            best = (float(r.fun), r.x)
    return best


def corner():
    from polychain import RelaxPoly, poly_class
    from chiral import chain
    b, g, ev = B0, G0, EV0; a = b + ev
    rng = np.random.default_rng(1)
    gam = {}
    for d in (1, 2):
        for line in open(f"logs/chiral_bounds_P{d}.log"):
            r = json.loads(line)
            gam[(d, r["k"])] = (r["gamma_theta"]["1.0"], r["corner_mu0"], r["ceiling_per_var"])
    for k in [4, 5, 6, 7]:
        mu0, s = corner_mu(k, b, g, ev, rng)
        l = s.copy(); u = np.ones(k)
        rel = RelaxPoly(chain(k, b, g, ev), poly_class(2), K=5)
        lo, up, _ = rel.bound(l, u, None, maxit=60, tol=1e-10)
        out = dict(k=k, mu0=round(mu0, 4), s=np.round(s, 4).tolist(), f_k_s=round(float(fk(s, a, b, g)), 6),
                   P2_bound_on_box=(round(lo, 6), round(up, 6)))
        for d in (1, 2):
            g1, old_mu0, old_ceil = gam[(d, k)]
            out[f"P{d}"] = dict(gamma=g1, ceiling_per_var=round(float(np.exp(mu0 * g1 / (k + 1))), 4),
                                old_mu0=old_mu0, old_ceiling=old_ceil)
        print(json.dumps(out), flush=True)
    for k in [10, 20, 50, 100]:
        mu0, s = corner_mu(k, b, g, ev, rng, nstart=6)
        print(json.dumps(dict(k=k, mu0=round(mu0, 4), s_mid=round(float(s[k // 2]), 4), s_end=round(float(s[0]), 4))), flush=True)
    ss = np.linspace(0.01, 0.99, 98001)
    v = np.log(2 / (1 - ss)) / ((a + b) * ss * ss)
    j = int(np.argmin(v))
    print(f"uniform bulk limit: min_s log(2/(1-s)) / ((a+b) s^2) = {v[j]:.4f} at s = {ss[j]:.4f}; "
          f"exp(that * g_inf) = {np.exp(v[j] * (g - ev)**2 / (4*g)):.4f} per variable (heuristic limit)")


def sos():
    import sympy as sp
    x, y, t, b, g, ev = sp.symbols("x y t b g ev", real=True)
    a = b + ev
    W = a / 2 * (x**2 + y**2) + b * x * y + g / 2 * (x * y**2 - x**2 * y)
    h = lambda z: -g / 2 * z**3
    bracket = sp.expand(W + h(x) - h(y))
    dec = ((b / 2 - g) * (x + y)**2 + ev / 2 * (x**2 + y**2)) + g / 2 * (x + y)**2 * (1 + y) + g / 2 * (x + y)**2 * (1 - x)
    print("bracket - [(b/2-g)(x+y)^2 + (ev/2)(x^2+y^2) + (g/2)(x+y)^2(1+y) + (g/2)(x+y)^2(1-x)] =", sp.simplify(bracket - sp.expand(dec)))
    endL = sp.expand(a / 2 * t**2 - h(t)); endR = sp.expand(a / 2 * t**2 + h(t))
    print("(a/2)t^2 - h(t) - [((a-g)/2) t^2 + (g/2) t^2 (1+t)] =", sp.simplify(endL - sp.expand((a - g) / 2 * t**2 + g / 2 * t**2 * (1 + t))))
    print("(a/2)t^2 + h(t) - [((a-g)/2) t^2 + (g/2) t^2 (1-t)] =", sp.simplify(endR - sp.expand((a - g) / 2 * t**2 + g / 2 * t**2 * (1 - t))))
    print("1 + y - [(1+y)^2/2 + (1-y^2)/2] =", sp.simplify(1 + y - ((1 + y)**2 / 2 + (1 - y**2) / 2)))
    # numerical order-2 sparse moment relaxation with pair cliques
    import cvxpy as cp
    bb, gg, ee = B0, G0, EV0; aa = bb + ee
    mons = [(i, j) for d in range(5) for i in range(d + 1) for j in [d - i]]
    for n, boxform, share in [(5, "linear", 4), (8, "linear", 4), (8, "quadratic", 4), (8, "linear", 2)]:
        ys = [{m: (cp.Variable() if m != (0, 0) else 1.0) for m in mons} for _ in range(n - 1)]
        cons = []
        basis2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
        basis1 = [(0, 0), (1, 0), (0, 1)]
        def ent(yv, m):
            return yv[m] if m != (0, 0) else 1.0

        def psd(yv, basis, shift=((1.0, (0, 0)),)):
            k = len(basis)
            Z = cp.Variable((k, k), PSD=True)
            for i, p in enumerate(basis):
                for j, q in enumerate(basis):
                    if j < i:
                        continue
                    m = (p[0] + q[0], p[1] + q[1])
                    cons.append(Z[i, j] == sum(coef * ent(yv, (m[0] + sm[0], m[1] + sm[1])) for coef, sm in shift))
            return Z
        for e in range(n - 1):
            yv = ys[e]
            psd(yv, basis2)
            if boxform == "linear":
                gl = [[(1.0, (0, 0)), (-1.0, (1, 0))], [(1.0, (0, 0)), (1.0, (1, 0))], [(1.0, (0, 0)), (-1.0, (0, 1))], [(1.0, (0, 0)), (1.0, (0, 1))]]
            else:
                gl = [[(1.0, (0, 0)), (-1.0, (2, 0))], [(1.0, (0, 0)), (-1.0, (0, 2))]]
            for gs in gl:
                psd(yv, basis1, gs)
            if e + 1 < n - 1:
                for d in range(1, share + 1):
                    cons.append(yv[(0, d)] == ys[e + 1][(d, 0)])
        obj = 0
        for e in range(n - 1):
            yv = ys[e]
            obj += aa / 2 * (yv[(2, 0)] + yv[(0, 2)]) + bb * yv[(1, 1)] + gg / 2 * (yv[(1, 2)] - yv[(2, 1)])
        obj += aa / 2 * ys[0][(2, 0)] + aa / 2 * ys[-1][(0, 2)]
        prob = cp.Problem(cp.Minimize(obj), cons)
        prob.solve(solver="CLARABEL")
        print(f"sparse moment relaxation, order 2, pair cliques, {boxform} box constraints, univariate moments shared up to degree {share}, n = {n}: status {prob.status}, value {prob.value:.4e} (f* = 0)")


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"lambda": lam, "analytic": analytic, "leftover": leftover, "corner": corner, "sos": sos}[cmd]()
