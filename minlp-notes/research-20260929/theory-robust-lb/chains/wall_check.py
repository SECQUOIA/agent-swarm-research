"""Revision 1 of robust-chains.md: the chain WALL (a symmetric uniform chain without (H1)).

  u(t) = 1.022 t + 0.189 t^2 + 1.774 t^3 + 1.086 t^4,   b = 0.962,   f_n = sum_i u(x_i) + b sum_i x_i x_{i+1}
  on [-1,1]^n (the reviewer's example).

Commands (floating point unless stated):
  python3 wall_check.py basic          u' > 0 on [-1,1]; c with u'(c) = 2b; minimizer of phi; grid DP + L-BFGS-B
                                       f*_n against the wall value for n = 2..16; the n/2 wall configurations;
                                       class (a) and (a0) root bounds (column generation lower bounds)
  python3 wall_check.py family         the explicit mean-consistent family on the adjacent-pair box: grid LP
                                       (N = 401), then the closed form with rational s and t, evaluated
                                       with mpmath at 30 digits (c from the cubic u'(c) = 2b at 40 digits)
  python3 wall_check.py classes        class bounds on the adjacent-pair box H_j (n = 6, j = 1, 2) for env
                                       (fixed balanced split), a0, b2, b3, b4, a (column generation)
  python3 wall_check.py bb CLS RULE EPS n    one B&B run (bb_rules.bb), balanced base split -> one JSON line
  python3 wall_check.py endfrust       the chain u = t^2 + 1.5 t, b = 1.2: grid DP minimizers for n = 3..12
"""
import sys
import json
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import linprog, minimize
from scipy import sparse
sys.path.insert(0, "..")
from robust_bb import Family, Relax, PW  # noqa: E402

UC = np.array([0.0, 1.022, 0.189, 1.774, 1.086])
B = 0.962
G = np.linspace(-1, 1, 2001)


def U(t, uc=UC):
    return P.polyval(t, uc)


def c_root():
    r = [z.real for z in np.roots(P.polysub(P.polyder(UC), [2 * B])[::-1]) if abs(z.imag) < 1e-12 and -1 < z.real < 1]
    assert len(r) == 1
    return r[0]


def f_chain(x, uc=UC, b=B):
    x = np.asarray(x, float)
    return float(np.sum(U(x, uc)) + b * np.sum(x[:-1] * x[1:]))


def dp(n, uc=UC, b=B, grid=G, tol=1e-9):
    """Grid DP; returns refined minimum value, minimizer, grid value, and the number of grid end states
    whose DP value is within tol of the grid minimum."""
    uG = U(grid, uc)
    V = uG.copy(); back = []
    for _ in range(1, n):
        M = V[:, None] + b * grid[:, None] * grid[None, :]
        j = np.argmin(M, axis=0); back.append(j)
        V = M[j, np.arange(len(grid))] + uG
    k = int(np.argmin(V)); path = [k]
    for j in reversed(back):
        k = int(j[k]); path.append(k)
    x0 = grid[np.array(path[::-1])]
    r = minimize(lambda x: f_chain(x, uc, b), x0, bounds=[(-1, 1)] * n, method="L-BFGS-B",
                 options={"ftol": 1e-15, "gtol": 1e-12})
    best = (r.fun, r.x) if r.fun < f_chain(x0, uc, b) else (f_chain(x0, uc, b), x0)
    return best[0], best[1], float(V.min())


def wall_configs(n, c):
    """x^(j), j = 1..n/2 (n even): the (-1,-1) bond at (2j-1, 2j); c-sites: i even < 2j or i odd > 2j."""
    out = []
    for j in range(1, n // 2 + 1):
        x = np.array([c if ((i % 2 == 0 and i < 2 * j) or (i % 2 == 1 and i > 2 * j)) else -1.0 for i in range(1, n + 1)])
        out.append(x)
    return out


def basic():
    du = P.polyder(UC)
    fine = np.linspace(-1, 1, 400001)
    print(f"min u' on [-1,1] (grid of 400001 points) = {P.polyval(fine, du).min():.6f} > b = {B}: u is increasing, "
          f"u'(t) - b > 0, min u = u(-1) = {U(-1.0):.6f}")
    c = c_root()
    phi = lambda x, y: 0.5 * (U(x) + U(y)) + B * x * y
    g = np.linspace(-1, 1, 2001); X, Y = np.meshgrid(g, g, indexing="ij"); Pm = phi(X, Y)
    k = np.unravel_index(np.argmin(Pm), Pm.shape)
    m = phi(-1.0, c)
    print(f"c = {c:.12f} (u'(c) = 2b); m = phi(-1, c) = {m:.10f}; grid min phi = {Pm[k]:.10f} at ({g[k[0]]:.3f}, {g[k[1]]:.3f}); "
          f"phi(-1,-1) - m = {phi(-1.0, -1.0) - m:.6f}; best diagonal value - m = {np.min(np.diag(Pm)) - m:.6f}")
    for n in range(2, 17):
        fs, xs, vg = dp(n)
        if n % 2 == 0:
            ws = wall_configs(n, c)
            vals = [f_chain(x) for x in ws]
            ref = (n // 2 + 1) * U(-1.0) + (n // 2 - 1) * U(c) + B * (1 - (n - 2) * c)
            msg = (f"walls: {len(ws)} configurations, values - closed form in [{min(vals)-ref:+.1e}, {max(vals)-ref:+.1e}], "
                   f"DP/L-BFGS-B f* - wall value = {fs - ref:+.2e}")
        else:
            ref = ((n + 1) // 2) * U(-1.0) + ((n - 1) // 2) * U(c) - B * (n - 1) * c
            msg = f"alternating (-1, c, ..., -1): DP/L-BFGS-B f* - its value = {fs - ref:+.2e}"
        out = dict(n=n, fstar=round(fs, 10), x=np.round(xs, 4).tolist(), note=msg)
        if n >= 3:
            fam = Family([PW.poly(UC)] * n, [B] * (n - 1))
            for cls in ("env", "a0", "a"):
                rel = Relax(fam, cls, "balanced", K=7)
                lo, up, _ = rel.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=150, tol=1e-10)
                out[f"rootgap_{cls}"] = (round(ref - up, 7), round(ref - lo, 7))
        print(json.dumps(out), flush=True)


def family():
    c = c_root()
    phi = lambda x, y: 0.5 * (U(x) + U(y)) + B * x * y
    m = phi(-1.0, c); true = phi(-1.0, -1.0) + 2 * m
    for N in (401,):
        g = np.linspace(-1, c, N)
        Y, Z = np.meshgrid(g, g, indexing="ij")
        sub = phi(-1.0, Y) + phi(Y, Z) + phi(Z, -1.0)
        cost = np.concatenate([phi(-1.0, g), phi(Y, Z).ravel(), phi(g, -1.0)])
        nA, nB = N, N * N
        A = sparse.lil_matrix((5, 2 * N + nB))
        A[0, :nA] = 1; A[1, nA:nA + nB] = 1; A[2, nA + nB:] = 1
        A[3, :nA] = g; A[3, nA:nA + nB] = -Y.ravel()
        A[4, nA:nA + nB] = Z.ravel(); A[4, nA + nB:] = -g
        res = linprog(cost, A_eq=A.tocsr(), b_eq=[1, 1, 1, 0, 0], bounds=(0, None), method="highs")
        print(f"grid N={N} on [-1,c]^2: min of the 3-factor sum - (phi(-1,-1)+2m) = {sub.min() - true:+.2e}; "
              f"mean-consistent LP value - (phi(-1,-1)+2m) = {res.fun - true:+.8f}", flush=True)
    # closed form: middle s*delta(-1,c) + (1-s)*delta(c,-1); left factor delta at ybar = -s + (1-s) c;
    # right factor (1-p) delta(-1) + p delta(t), p = s (1+c)/(1+t), so that its mean is zbar = s c - (1-s).
    def gap(s, t, c=c):
        ybar = -s + (1 - s) * c; p = s * (1 + c) / (1 + t)
        val = phi(-1.0, ybar) + m + (1 - p) * phi(-1.0, -1.0) + p * phi(t, -1.0)
        return true - val
    r = minimize(lambda v: -gap(*v), [0.078, 0.234], method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-15})
    print(f"closed form (float): best (s, t) = ({r.x[0]:.6f}, {r.x[1]:.6f}), gap = {-r.fun:.10f}; with t = ybar and s = 31/400: {gap(31/400, -31/400 + (1 - 31/400) * c):.10f}")
    import mpmath as mp
    mp.mp.dps = 40
    uc = [mp.mpf(str(v)) for v in UC]
    Um = lambda t: sum(cf * t ** i for i, cf in enumerate(uc))
    bm = mp.mpf(str(B))
    cm = mp.findroot(lambda t: sum(i * cf * t ** (i - 1) for i, cf in enumerate(uc) if i > 0) - 2 * bm, mp.mpf(c))
    phim = lambda x, y: (Um(x) + Um(y)) / 2 + bm * x * y
    mm = phim(-1, cm); truem = phim(-1, -1) + 2 * mm
    s = mp.mpf(779) / 10000; t = mp.mpf(467) / 2000
    ybar = -s + (1 - s) * cm; p = s * (1 + cm) / (1 + t)
    val = phim(-1, ybar) + mm + (1 - p) * phim(-1, -1) + p * phim(t, -1)
    mp.mp.dps = 30
    print(f"exact data, s = 779/10000, t = 467/2000: c = {mp.nstr(cm, 30)}; residual of u'(c) - 2b = {mp.nstr(sum(i * cf * cm ** (i - 1) for i, cf in enumerate(uc) if i > 0) - 2 * bm, 3)}")
    print(f"  ybar = {mp.nstr(ybar, 20)} in [-1, c]: {(-1 <= ybar <= cm)}; t in [-1, c]: {(-1 <= t <= cm)}; p = {mp.nstr(p, 20)} in [0,1]: {(0 <= p <= 1)}")
    print(f"  means: middle z-mean - right mean = {mp.nstr((s * cm - (1 - s)) - ((1 - p) * (-1) + p * t), 3)}")
    print(f"  family value - (phi(-1,-1) + 2m) = {mp.nstr(val - truem, 30)}")
    print(f"  phi(-1, ybar) below the chord between -1 and c by {mp.nstr(s * phim(-1, -1) + (1 - s) * mm - phim(-1, ybar), 6)}")


def classes():
    c = c_root()
    n = 6
    ws = wall_configs(n, c)
    fam = Family([PW.poly(UC)] * n, [B] * (n - 1))
    fs = f_chain(ws[0])
    for j in (0, 1):
        x1, x2 = ws[j], ws[j + 1]
        l = np.minimum(x1, x2); u = np.maximum(x1, x2)
        out = dict(n=n, box=f"H_{j+1}", l=np.round(l, 4).tolist(), u=np.round(u, 4).tolist())
        for cls in ("env", "a0", "b2", "b3", "b4", "a"):
            rel = Relax(fam, cls, "balanced", K=9)
            lo, up, _ = rel.bound(l, u, None, maxit=200, tol=1e-10)
            out[cls] = (round(fs - up, 7), round(fs - lo, 7))
        print("gap f* - LB on the adjacent-pair box, bracket (from fooling, from split):", json.dumps(out), flush=True)


def endfrust():
    uc = np.array([0.0, 1.5, 1.0]); b = 1.2
    phi = lambda x, y: 0.5 * (U(x, uc) + U(y, uc)) + b * x * y
    g = np.linspace(-1, 1, 2001); X, Y = np.meshgrid(g, g, indexing="ij"); Pm = phi(X, Y)
    k = np.unravel_index(np.argmin(Pm), Pm.shape)
    print(f"u = t^2 + 1.5 t, b = 1.2: min phi = {Pm[k]:.6f} at ({g[k[0]]:.3f}, {g[k[1]]:.3f})")
    for n in range(3, 13):
        fs, xs, vg = dp(n, uc, b)
        # best value among configurations whose frustration is not at an end: force both ends to be in the
        # -1 phase region (x_1 <= -0.9 and x_n <= -0.9) by a restricted DP
        uG = U(G, uc)
        V = np.where(G <= -0.9, uG, np.inf);
        for _ in range(1, n):
            M = V[:, None] + b * G[:, None] * G[None, :]
            V = M.min(axis=0) + uG
        Vr = np.where(G <= -0.9, V, np.inf).min()
        mirror = f_chain(xs[::-1], uc, b) - fs
        print(json.dumps(dict(n=n, fstar=round(fs, 8), x=np.round(xs, 4).tolist(), mirror_value_minus_fstar=round(mirror, 10),
                              best_with_both_ends_le_m09_minus_fstar=round(float(Vr - fs), 6))), flush=True)


def run_bb(cls, rule, eps, n):
    from bb_rules import bb
    c = c_root()
    if n % 2 == 0:
        fs = min(f_chain(x) for x in wall_configs(n, c))
    else:
        fs = f_chain(np.array([-1.0 if i % 2 == 1 else c for i in range(1, n + 1)]))
    fam = Family([PW.poly(UC)] * n, [B] * (n - 1))
    r = bb(fam, cls, eps, fs, rule=rule, base="balanced", timelimit=3000)
    print(json.dumps(dict(family="WALL", cls=cls, rule=rule, eps=eps, n=n, fstar=fs, **r)), flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "basic":
        basic()
    elif cmd == "family":
        family()
    elif cmd == "classes":
        classes()
    elif cmd == "endfrust":
        endfrust()
    elif cmd == "bb":
        run_bb(sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]))
