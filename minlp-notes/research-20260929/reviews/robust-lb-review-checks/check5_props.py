"""Referee check 5: Propositions 2.1, 2.3, 2.4 numerically, and a two-sided bracket on E_d(L).
Usage: python3 check5_props.py > logs/check5_props.log"""
import itertools
import warnings
import numpy as np
from scipy.optimize import linprog, minimize

warnings.simplefilter("ignore")
rng = np.random.default_rng(7)

# ---------------- Proposition 2.1: balanced-split factors nonnegative when kappa + |b| <= 1 ----------------
g = np.linspace(-1, 1, 801)
X, Y = np.meshgrid(g, g, indexing="ij")
u = lambda t, k: t ** 2 - k * t ** 4
worst = np.inf
for k in (0.0, 0.1, 0.5, 0.9, 1.0):
    for b in (1 - k, -(1 - k)):
        inner = 0.5 * u(X, k) + 0.5 * u(Y, k) + b * X * Y
        end = u(X, k) + 0.5 * u(Y, k) + b * X * Y
        worst = min(worst, inner.min(), end.min())
print("Prop 2.1: min over grid of balanced-split factors (kappa in {0,.1,.5,.9,1}, |b| = 1-kappa): %.3e" % worst)
k, b = 0.1, 0.95   # violates kappa + |b| <= 1 (the condition is sufficient; b = 0.85 still gives >= 0)
print("  control kappa=0.1, b=0.95: min interior factor %.4f (negative expected)" %
      (0.5 * u(X, k) + 0.5 * u(Y, k) + b * X * Y).min())

# ---------------- Proposition 2.3: inf over class-(a) splits of summed centred chords ----------------
def factor_chord_max(al, bb, be, d1, d2, M=161):
    v1 = np.linspace(-d1, d1, M); v2 = np.linspace(-d2, d2, M)
    V1, V2 = np.meshgrid(v1, v2, indexing="ij")
    return np.max(-(al * V1 ** 2 + 2 * bb * V1 * V2 + be * V2 ** 2) / 2)

for trial in range(4):
    n = 4
    D = rng.uniform(-0.5, 3.0, n)                      # unary curvatures (quadratic u_i), any sign
    B = rng.uniform(-1.5, 1.5, n - 1)
    lo = rng.uniform(-1, 0, n); hi = lo + rng.uniform(0.3, 2, n)
    p = lo + rng.uniform(0.2, 0.8, n) * (hi - lo)
    d = np.minimum(p - lo, hi - p)
    H = np.diag(D) + np.diag(B, 1) + np.diag(B, -1)
    # right side: sup over v in prod[-d_i, d_i] of -(1/2) v'Hv  (brute force grid with signs)
    grids = [np.linspace(-di, di, 41) for di in d]
    best = -np.inf
    for v in itertools.product(*grids):
        v = np.array(v); best = max(best, -0.5 * v @ H @ v)
    # left side: minimise over interior alphas (alpha_1 = D_1 fixed, beta_n = D_n fixed)
    def Gam(a):
        al = [D[0], a[0], a[1]]; be = [D[1] - a[0], D[2] - a[1], D[3]]
        return sum(factor_chord_max(al[e], B[e], be[e], d[e], d[e + 1]) for e in range(3))
    res = min((minimize(Gam, x0, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-9, maxiter=4000))
               for x0 in (np.zeros(2), D[1:3] / 2, D[1:3], rng.normal(size=2))), key=lambda r: r.fun)
    # f(p) - min_A f for the quadratic f = sum D_i t^2/2 + sum B_e t_e t_{e+1} (grid)
    fmin = np.inf
    gg = [np.linspace(lo[i], hi[i], 25) for i in range(n)]
    for x in itertools.product(*gg):
        x = np.array(x); fmin = min(fmin, 0.5 * x @ H @ x)
    fp = 0.5 * p @ H @ p
    print("Prop 2.3 trial %d: inf_r Gamma_r = %.5f ; sup_v chord of f = %.5f ; f(p) - min_A f >= %.5f"
          % (trial, res.fun, best, fp - fmin))

# ---------------- Proposition 2.4: edge-concave factors -> balanced envelope bound = min_A f ----------------
def env_bound_lp(ufun, B, lo, hi, M=13):
    """Balanced fixed split; primal LP over an M x M grid per factor with mean consistency (upper bound on
    LB_r) and the dual lower bound from grid minima (approximate)."""
    n = len(lo)
    pts, cost = [], []
    for e in range(n - 1):
        xs = np.linspace(lo[e], hi[e], M); ys = np.linspace(lo[e + 1], hi[e + 1], M)
        P = np.array([(x, y) for x in xs for y in ys])
        wa = 1.0 if e == 0 else 0.5; wc = 1.0 if e == n - 2 else 0.5
        pts.append(P); cost.append(wa * ufun[e](P[:, 0]) + wc * ufun[e + 1](P[:, 1]) + B[e] * P[:, 0] * P[:, 1])
    m = len(pts[0]); N = m * (n - 1)
    A = np.zeros((n - 1 + n - 2, N)); rhs = np.zeros(n - 1 + n - 2); rhs[:n - 1] = 1
    for e in range(n - 1):
        A[e, e * m:(e + 1) * m] = 1
    for i in range(1, n - 1):
        A[n - 1 + i - 1, (i - 1) * m:i * m] = pts[i - 1][:, 1]
        A[n - 1 + i - 1, i * m:(i + 1) * m] = -pts[i][:, 0]
    r = linprog(np.concatenate(cost), A_eq=A, b_eq=rhs, bounds=(0, None), method="highs")
    return r.fun

for trial in range(4):
    n = 4
    a = rng.uniform(0.2, 2, n); c3 = rng.uniform(-1, 1, n)
    ufun = [(lambda t, a=a[i], c=c3[i]: -a * t ** 2 + c * t - 0.3 * t ** 4) for i in range(n)]   # concave
    B = rng.uniform(-1.5, 1.5, n - 1)
    lo = rng.uniform(-1, 0, n); hi = lo + rng.uniform(0.3, 1.5, n)
    f = lambda x: sum(ufun[i](x[i]) for i in range(n)) + sum(B[e] * x[e] * x[e + 1] for e in range(n - 1))
    fmin = min(f(np.array(v)) for v in itertools.product(*[(lo[i], hi[i]) for i in range(n)]))
    ub = env_bound_lp(ufun, B, lo, hi)
    print("Prop 2.4 trial %d: grid-LP value of balanced envelope bound %.6f vs min over vertices of f %.6f" % (trial, ub, fmin))
# (a positive-gap control for the envelope LP is the gadget's fixed balanced split, gap 0.1255: check2)

# ---------------- E_d(L): lower bound (grid LP) and upper bound (sup error of the grid-optimal polynomial) ----------------
def Ed_bracket(y1, d, M=6001):
    y = np.linspace(-1, 1, M)
    L = lambda t: np.where(np.abs(t) <= y1, t * t, 2 * y1 * np.abs(t) - y1 * y1)
    V = np.polynomial.legendre.legvander(y, d)
    k = V.shape[1]
    Aub = np.vstack([np.hstack([-V, -np.ones((M, 1))]), np.hstack([V, -np.ones((M, 1))])])
    bub = np.concatenate([-L(y), L(y)])
    c = np.zeros(k + 1); c[-1] = 1
    r = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * k + [(0, None)], method="highs")
    yf = np.linspace(-1, 1, 2_000_001)
    err = np.max(np.abs(L(yf) - np.polynomial.legendre.legval(yf, r.x[:k])))
    return r.fun, err

for d in (2, 4, 6, 8, 10, 12):
    lo_, hi_ = Ed_bracket(0.38, d)
    print("E_%d(L), y1 = 0.38: in [%.5f, %.5f]" % (d, lo_, hi_))
print("band width eps_v + eta (1-y1)^2 = %.5f at the reference parameters" % (0.02 + 0.05 * 0.62 ** 2))
