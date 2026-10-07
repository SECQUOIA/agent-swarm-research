"""Confirmation recheck of the second revision of theory-robust-lb/robust-lower-bound.md.

Written from scratch; shares no code with the authors, the review or the first recheck.
Run: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 check_confirm.py > logs/check_confirm.log

(1) gamma_10 = 0 certificate: positivity of the four defining polynomials by exact
    Bernstein-basis coefficients with subdivision (Fractions), not by root counting.
(2) Corner-box threshold mu0 by a grid plus bounded L-BFGS-B polish, for every parameter
    set of Section 6.5 and of logs/scan_bd.log; ceilings; minimizing mu of scan_bd.log < mu0.
(3) E_d(L) for d = 2..12 with a full Chebyshev basis on [-1, 1] (odd degrees included).
(4) gamma_d by the band LP of Proposition 3.3 (grid lower bound, fine-grid upper bound).
(5) Arithmetic of the uniform cap and of the Theorem 4.3(3) bullets.
"""
from fractions import Fraction as Fr
from math import comb, log, exp
import numpy as np
from scipy.optimize import linprog, minimize

# ------------------------------------------------------------------ (1)
def poly_mul(p, q):
    r = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def poly_add(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]


def poly_scale(p, s):
    return [s * a for a in p]


def compose_affine(p, lo, hi):
    """coefficients in t of p(lo + (hi - lo) t)"""
    res = [Fr(0)]
    base = [Fr(1)]
    lin = [Fr(lo), Fr(hi) - Fr(lo)]
    for a in p:
        res = poly_add(res, poly_scale(base, a))
        base = poly_mul(base, lin)
    return res


def bernstein(p_t):
    n = len(p_t) - 1
    return [sum(Fr(comb(j, k), comb(n, k)) * p_t[k] for k in range(j + 1)) for j in range(n + 1)]


def positive_on(p, lo, hi, depth=0, maxdepth=30):
    """True if p > 0 on [lo, hi] is proved by Bernstein coefficients (with subdivision)."""
    b = bernstein(compose_affine(p, lo, hi))
    if all(c > 0 for c in b):
        return True, 1
    if b[0] <= 0 or b[-1] <= 0 or depth >= maxdepth:
        return False, 1
    mid = (Fr(lo) + Fr(hi)) / 2
    ok1, n1 = positive_on(p, lo, mid, depth + 1, maxdepth)
    ok2, n2 = positive_on(p, mid, hi, depth + 1, maxdepth)
    return ok1 and ok2, n1 + n2


y1, eta, ev = Fr(19, 50), Fr(1, 20), Fr(1, 50)
qc = [Fr(1002795549, 10**9), Fr(419528334, 10**9), Fr(-3338707087, 10**9),
      Fr(4161904633, 10**9), Fr(-1593496982, 10**9)]
q = []
for c in qc:
    q += [c, Fr(0)]
q = q[:-1]                                   # q(y) in powers of y, degree 8
rho = [Fr(0), Fr(0)] + q                     # y^2 q, degree 10
Lout = [-y1**2, 2 * y1]                      # L on [y1, 1]
Uout = poly_add([Fr(0), Fr(0), 1 + ev], poly_scale([y1**2, -2 * y1, Fr(1)], -(1 - eta)))
tests = [("q - 1 on [0, y1]", poly_add(q, [Fr(-1)]), 0, y1),
         ("1 + eps_v - q on [0, y1]", poly_add([1 + ev], poly_scale(q, -1)), 0, y1),
         ("rho - L on [y1, 1]", poly_add(rho, poly_scale(Lout, -1)), y1, 1),
         ("U - rho on [y1, 1]", poly_add(Uout, poly_scale(rho, -1)), y1, 1)]
print("(1) gamma_10 = 0 certificate by exact Bernstein coefficients")


for name, p, lo, hi in tests:
    ok, pieces = positive_on(p, lo, hi)
    xs = np.linspace(float(lo), float(hi), 200001)
    fmin = np.min(np.polyval([float(a) for a in p[::-1]], xs))
    print("  %-26s positive on closed interval: %s (%d Bernstein pieces); float min on a fine grid %.3e"
          % (name, ok, pieces, fmin))


# ------------------------------------------------------------------ gadget
def gadget(y1, eta, ev):
    b, bp, c = 2 * y1, 2 * eta + 2 * (1 - eta) * (1 - y1), 1 + eta + ev
    z1, k = 2 * eta * y1 / bp, 2 * (1 - eta) * y1

    def u(z):
        z = np.abs(z)
        return np.where(z <= z1, bp**2 * z**2 / (4 * eta), (bp * z + k)**2 / 4 - (1 - eta) * y1**2)

    def g(x, yy, z):
        return y1**2 * x**2 + b * x * yy + c * yy**2 + u(z) + bp * yy * z
    A = 1 + ev - (1 - eta) * (1 - y1)**2
    return g, y1**2 * (1 - A) / A, c


# ------------------------------------------------------------------ (2)
def mu0(y1, eta, ev):
    g, gam, _ = gadget(y1, eta, ev)
    t = np.linspace(0, 0.98, 50)
    A, B, C = np.meshgrid(t, t, t, indexing="ij")
    val = np.log(8 / ((1 - A) * (1 - B) * (1 - C))) / g(-A, -B, -C)
    i = np.unravel_index(np.argmin(val), val.shape)
    x0 = np.array([t[i[0]], t[i[1]], t[i[2]]])
    f = lambda v: float(np.log(8 / np.prod(1 - v)) / g(-v[0], -v[1], -v[2]))
    r = minimize(f, x0, method="L-BFGS-B", bounds=[(0, 0.995)] * 3, options={"ftol": 1e-14, "gtol": 1e-10})
    return r.fun, r.x, gam


print("\n(2) corner-box threshold mu0 = min ln(8/vol)/g(vertex) over [-1,-a]x[-1,-b]x[-1,-c]")
g, gam, _ = gadget(0.38, 0.05, 0.02)
V = float(g(-0.48, -0.873, -0.813))
vol8 = 0.52 * 0.127 * 0.187 / 8
print("  reference box -(0.48, 0.873, 0.813): V = g(vertex) = %.6f; (vol/8) exp(mu V) at mu = 2.3, 2.4, 2.5: %s"
      % (V, ", ".join("%.4f" % (vol8 * exp(m * V)) for m in (2.3, 2.4, 2.5))))
xs = np.linspace(-1, -0.48, 27); ys = np.linspace(-1, -0.873, 27); zs = np.linspace(-1, -0.813, 27)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
print("  grid min of g on that box %.6f (equals the vertex value if >= V - 1e-12: %s)"
      % (g(X, Y, Z).min(), g(X, Y, Z).min() >= V - 1e-12))

scan = """a 0.38 0.050 0.005 0.08129 2.231
a 0.38 0.010 0.020 0.08142 2.266
a 0.30 0.010 0.005 0.08311 2.201
a 0.30 0.050 0.005 0.07682 2.165
a 0.30 0.010 0.020 0.07826 2.194
a 0.38 0.010 0.005 0.08685 2.273
a 0.30 0.050 0.020 0.07231 2.158
a 0.38 0.050 0.020 0.07612 2.224
b4 0.30 0.005 0.002 0.02474 2.252
b4 0.30 0.020 0.002 0.02284 2.238
b4 0.38 0.005 0.002 0.01869 2.331
b4 0.38 0.020 0.002 0.01693 2.315
a 0.45 0.010 0.020 0.07855 2.310
a 0.45 0.010 0.005 0.08452 2.317
a 0.45 0.050 0.020 0.07390 2.265
a 0.45 0.050 0.005 0.07968 2.271
b4 0.50 0.005 0.002 0.00853 2.397
b4 0.50 0.020 0.002 0.00734 2.377
b6 0.30 0.005 0.002 0.00637 2.267
b6 0.30 0.020 0.002 0.00486 2.252
b6 0.38 0.020 0.002 0.00474 2.322
b6 0.38 0.005 0.002 0.00493 2.339
b6 0.50 0.005 0.002 0.00734 2.398
b6 0.50 0.020 0.002 0.00690 2.378
a 0.38 0.050 0.100 0.05211 2.192
a 0.38 0.050 0.200 0.02857 2.149"""
cache = {}
print("  class  (y1, eta, eps_v)        mu0     box upper corner         class-(a) ceiling/var   row gamma  row ceiling/var  row mu  row mu < mu0")
worst_a = []
for line in scan.splitlines():
    cl, a1, a2, a3, gr, mr = line.split()
    p = (float(a1), float(a2), float(a3))
    if p not in cache:
        cache[p] = mu0(*p)
    m0, box, ga = cache[p]
    gr, mr = float(gr), float(mr)
    ca = exp(m0 * ga / 3)
    worst_a.append((p, ca))
    print("  %-5s %-22s %.4f  -(%.3f, %.3f, %.3f)   %.4f                 %.5f    %.4f           %.3f   %s"
          % (cl, p, m0, *box, ca, gr, exp(m0 * gr / 3), mr, mr < m0))
for p in [(0.50, 0.005, 0.002)]:
    if p not in cache:
        cache[p] = mu0(*p)
    m0, box, ga = cache[p]
    print("  (extra) %-22s mu0 %.4f class-(a) ceiling/var %.4f" % (p, m0, exp(m0 * ga / 3)))
vals = sorted(exp(v[0] * v[2] / 3) for k, v in cache.items() if k != (0.38, 0.05, 0.02))
print("  class-(a) ceilings over all non-reference parameter sets above: %.4f .. %.4f" % (vals[0], vals[-1]))
sec65 = [(0.38, 0.01, 0.005), (0.38, 0.05, 0.1), (0.38, 0.05, 0.2), (0.30, 0.01, 0.005),
         (0.45, 0.01, 0.005), (0.30, 0.005, 0.002), (0.50, 0.005, 0.002)]
vals = sorted(exp(cache[p][0] * cache[p][2] / 3) for p in sec65)
print("  class-(a) ceilings over the seven sets of Section 6.5 / the recheck: %.4f .. %.4f" % (vals[0], vals[-1]))


# ------------------------------------------------------------------ (3)
def Lfun(y, y1):
    a = np.abs(y)
    return np.where(a <= y1, a**2, 2 * y1 * a - y1**2)


def Ufun(y, y1, eta, ev):
    a = np.abs(y)
    return (1 + ev) * a**2 - (1 - eta) * np.maximum(a - y1, 0)**2


def cheb(y, d):
    return np.polynomial.chebyshev.chebvander(y, d)


def E_d(y1, d, n=6001):
    ygrid = np.cos(np.linspace(0, np.pi, n))
    M = cheb(ygrid, d)
    Lv = Lfun(ygrid, y1)
    m = d + 1
    A_ub = np.block([[M, -np.ones((n, 1))], [-M, -np.ones((n, 1))]])
    r = linprog(np.r_[np.zeros(m), 1.0], A_ub=A_ub, b_ub=np.r_[Lv, -Lv],
                bounds=[(None, None)] * m + [(0, None)], method="highs")
    yf = np.linspace(-1, 1, 400001)
    up = np.max(np.abs(Lfun(yf, y1) - cheb(yf, d) @ r.x[:m]))
    return r.x[-1], up


print("\n(3) E_d(L), full Chebyshev basis of degree d on [-1,1] (grid-LP lower bound, fine-grid upper bound)")
Eref = {}
for d in range(2, 13):
    lo, up = E_d(0.38, d)
    Eref[d] = up
    print("  y1 = 0.38, d = %2d: E_d in [%.8f, %.8f]; d^2 E_d = %.4f" % (d, lo, up, d * d * up))
ev_ = [d * d * Eref[d] for d in range(2, 13, 2)]
od_ = [d * d * Eref[d] for d in range(3, 13, 2)]
print("  d^2 E_d over even d = 2..12: %.4f .. %.4f; over odd d = 3..11: %.4f .. %.4f" % (min(ev_), max(ev_), min(od_), max(od_)))
lo, up = E_d(0.30, 4)
print("  y1 = 0.30, d = 4: E_4 in [%.6f, %.6f]" % (lo, up))
E4_03 = up


# ------------------------------------------------------------------ (4)
def gamma_d(y1, eta, ev, d, n=6001):
    """inf over even rho in P_d of max(L - rho) + max(rho - U) on [0,1]."""
    yg = 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    yg = np.unique(np.r_[yg, y1])
    M = np.stack([yg**(2 * j) for j in range(d // 2 + 1)], axis=1)
    m = M.shape[1]
    Lv, Uv = Lfun(yg, y1), Ufun(yg, y1, eta, ev)
    N = len(yg)
    # variables: coeffs (m), s1, s2 ; L - M a <= s1 ; M a - U <= s2
    A_ub = np.block([[-M, -np.ones((N, 1)), np.zeros((N, 1))], [M, np.zeros((N, 1)), -np.ones((N, 1))]])
    r = linprog(np.r_[np.zeros(m), 1.0, 1.0], A_ub=A_ub, b_ub=np.r_[-Lv, Uv],
                bounds=[(None, None)] * (m + 2), method="highs")
    yf = np.linspace(0, 1, 400001)
    Mf = np.stack([yf**(2 * j) for j in range(m)], axis=1)
    pr = Mf @ r.x[:m]
    up = np.max(Lfun(yf, y1) - pr) + np.max(pr - Ufun(yf, y1, eta, ev))
    return r.fun, up


print("\n(4) gamma_d by the band LP of Proposition 3.3 (grid lower bound, fine-grid upper bound)")
for p, d in [((0.38, 0.05, 0.02), 2), ((0.38, 0.05, 0.02), 4), ((0.38, 0.05, 0.02), 6), ((0.38, 0.05, 0.02), 8),
             ((0.38, 0.05, 0.02), 10), ((0.30, 0.005, 0.002), 4), ((0.50, 0.005, 0.002), 6)]:
    lo, up = gamma_d(*p, d)
    print("  %-20s d = %2d: gamma_d in [%.6f, %.6f]" % (p, d, max(lo, 0.0), up))

# ------------------------------------------------------------------ (5)
print("\n(5) arithmetic")
print("  4 ln 64 = %.4f; 2 * 4 ln 64 = %.4f (<= 33.3: %s)" % (4 * log(64), 8 * log(64), 8 * log(64) <= 33.3))
print("  reference: exp(2.4 gamma_4 = 2.4*0.00777) = %.4f per gadget; exp(2.4 gamma_6) = %.4f" % (exp(2.4 * 0.00777), exp(2.4 * 0.00237)))
print("  y1 = 0.30: exp(2.4 * 2 E_4 / 3) = %.4f per variable; exp(mu0 * 0.0247 / 3) with mu0 = %.4f: %.4f"
      % (exp(2.4 * 2 * E4_03 / 3), cache[(0.30, 0.005, 0.002)][0], exp(cache[(0.30, 0.005, 0.002)][0] * 0.0247 / 3)))
for name, base, gg, p in [("b4 ref", 1.0109, 0.00777, (0.38, 0.05, 0.02)), ("b4 0.30", 1.0480, 0.02474, (0.30, 0.005, 0.002)),
                          ("b6 ref", 1.0044, 0.00237, (0.38, 0.05, 0.02)), ("b6 0.50", 1.0134, 0.00734, (0.50, 0.005, 0.002))]:
    m0 = cache[p][0]
    print("  %-8s ceiling exp(mu0 gamma/3) = %.4f per variable; computed base %.4f per variable" % (name, exp(m0 * gg / 3), base**(1 / 3)))
