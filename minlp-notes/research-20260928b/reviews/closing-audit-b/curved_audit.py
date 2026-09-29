"""Closing audit (b), item 3: Proposition 3.14 of face-exact-node-complexity.md.

psi(s) = -s - s^2/2, c0 = 3/4, D = x1 - x2 - c0, f = max_{s in [-1,2]} (D - psi(s))(y - s) on [0,1]^3,
termwise McCormick on x1*y and -x2*y.  Own code, written from the statement.
"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, brentq

rng = np.random.default_rng(20260929)
psi = lambda s: -s - s ** 2 / 2
c0 = 0.75


def f_exact(D, y):
    """max over s in [-1,2] of h(s) = (D - psi(s))(y - s): cubic in s; check endpoints and
    stationary points (h'(s) = -D + y - 2 s + s y - 1.5 s^2 = 0)."""
    h = lambda s: (D - psi(s)) * (y - s)
    best = max(h(-1.0), h(2.0))
    # -1.5 s^2 + (y - 2) s + (y - D) = 0
    A, Bq, Cq = -1.5, y - 2.0, y - D
    disc = Bq * Bq - 4 * A * Cq
    if disc >= 0:
        for r in ((-Bq + np.sqrt(disc)) / (2 * A), (-Bq - np.sqrt(disc)) / (2 * A)):
            if -1 <= r <= 2:
                best = max(best, h(r))
    return best


def f_grid(D, y, K=30001):
    s = np.linspace(-1, 2, K)
    return np.max((D - psi(s)) * (y - s))


def G(D, y):
    return f_exact(D, y) - D * y


# (1) closed form vs grid
pts = rng.random((2000, 3))
err = max(abs(f_exact(p[0] - p[1] - c0, p[2]) - f_grid(p[0] - p[1] - c0, p[2])) for p in pts[:300])
print("(1) closed-form max vs 30001-point grid, 300 points: max |diff| = %.2e" % err)

# (2) f >= 0 on random points; growth ratio f/delta^2
P = rng.random((200000, 3))
Dv = P[:, 0] - P[:, 1] - c0
fv = np.array([f_exact(d, y) for d, y in zip(Dv, P[:, 2])])
dl = Dv - psi(P[:, 2])
print("(2) min f over 200000 random points = %.3e; min f/delta^2 = %.4f (claimed >= 1/12 = 0.0833)"
      % (fv.min(), np.min(fv / dl ** 2)))
# growth ratio on a fine (delta, y) grid over the admissible range
worst = 1e9
for y in np.linspace(0, 1, 201):
    for d in np.linspace(-1.75, 1.75, 351):
        if abs(d) < 1e-9:
            continue
        Dd = psi(y) + d
        if -1.75 <= Dd <= 0.25:
            worst = min(worst, f_exact(Dd, y) / d ** 2)
print("    grid over (y, delta) with D in [-1.75, 0.25]: min f/delta^2 = %.4f" % worst)
# the proof's witness s = y - delta/8 gives >= delta^2/8 (1 - 2.22/8)
print("    |psi'| on [-0.219, 1.219] <= %.4f; (1 - 2.22/8)/8 = %.4f >= 1/12 = %.4f" %
      (1 + 1.219, (1 - 2.22 / 8) / 8, 1 / 12))

# (3) f = 0 on Sigma
ys = rng.random(5000); ts = rng.random(5000)
x1 = ts + psi(ys) + c0
ok = (x1 >= 0) & (x1 <= 1)
fs = np.array([f_exact(psi(y), y) for y in ys[ok]])
print("(3) f on Sigma (%d points): max |f| = %.2e" % (ok.sum(), np.abs(fs).max()))

# (4) convexity of G by midpoint tests on the (D, y) range of the box
Dr = rng.uniform(-1.75, 0.25, (20000, 2)); yr = rng.uniform(0, 1, (20000, 2))
viol = 0; worstv = 0
for (Da, Db), (ya, yb) in zip(Dr, yr):
    lhs = G((Da + Db) / 2, (ya + yb) / 2); rhs = (G(Da, ya) + G(Db, yb)) / 2
    worstv = max(worstv, lhs - rhs)
    viol += lhs > rhs + 1e-12
print("(4) convexity of G: %d violations in 20000 midpoint tests (max lhs-rhs = %.2e)" % (viol, worstv))

# (5) A = int_0^1 (1 - |psi(y) + c0|) dy
A_num = quad(lambda y: 1 - abs(psi(y) + c0), 0, 1, points=[np.sqrt(2.5) - 1])[0]
y0 = np.sqrt(2.5) - 1
Pp = lambda y: 0.75 * y - y ** 2 / 2 - y ** 3 / 6
A_cf = 1 - (2 * Pp(y0) - Pp(1))
print("(5) A = %.6f (quadrature), %.6f (closed form, root y0 = %.4f); row lengths in [%.3f, %.3f]" %
      (A_num, A_cf, y0, 1 - 0.75, 1.0))


# (6) row-slice inequality Gamma_C(p) >= ell * d_y on random boxes, with exact McCormick gaps
def mc_gap(c, xi, xl, xu, yj, yl, yu):
    if c > 0:
        return c * min((xi - xl) * (yj - yl), (xu - xi) * (yu - yj))
    return -c * min((xi - xl) * (yu - yj), (xu - xi) * (yj - yl))


tested = 0; minratio = np.inf; viol = 0; valid_viol = 0
while tested < 20000:
    b1 = np.sort(rng.random(2)); b2 = np.sort(rng.random(2)); by = np.sort(rng.random(2))
    y = rng.uniform(by[0], by[1])
    sh = psi(y) + c0
    tlo = max(b2[0], b1[0] - sh); thi = min(b2[1], b1[1] - sh)
    if thi <= tlo:
        continue
    ell = thi - tlo; t = (tlo + thi) / 2
    p = (t + sh, t, y)
    gam = mc_gap(1, p[0], b1[0], b1[1], y, by[0], by[1]) + mc_gap(-1, p[1], b2[0], b2[1], y, by[0], by[1])
    dy = min(y - by[0], by[1] - y)
    tested += 1
    if dy > 0:
        minratio = min(minratio, gam / (ell * dy))
    viol += gam < ell * dy * (1 - 1e-12)
    # f(p) = 0 check
    valid_viol += abs(f_exact(p[0] - p[1] - c0, y)) > 1e-12
print("(6) row slices: %d random boxes/rows, violations of Gamma >= ell*d_y: %d, min ratio %.6f; f(p) != 0: %d"
      % (tested, viol, minratio, valid_viol))

# (7) area bound 2 int_0^{w/2} min(1, eps/d) dd <= 2 eps (1 + ln(1/(2 eps)))
for eps in (0.3, 0.1, 1e-3, 1e-6):
    for w in (1.0, 0.5, 0.01):
        lhs = 2 * quad(lambda d: min(1.0, eps / d) if d > 0 else 1.0, 0, w / 2, points=[eps] if eps < w / 2 else None)[0]
        rhs = 2 * eps * (1 + np.log(1 / (2 * eps)))
        assert lhs <= rhs * (1 + 1e-9), (eps, w, lhs, rhs)
print("(7) per-box area bound 2 int min(1, eps/d) <= 2 eps (1 + ln(1/(2 eps))) holds on the test grid")

# (8) Theorem 3.6 (p = 2) bound: 4 (12 eta)^(1/4) / (9 (eps + eta)), max over eta
for eps in (1e-2, 1e-6):
    r = minimize_scalar(lambda e: -4 * (12 * e) ** 0.25 / (9 * (eps + e)), bounds=(0, 1), method="bounded",
                        options={"xatol": 1e-14})
    print("(8) eps = %g: argmax eta/eps = %.4f (claimed 1/3), max * eps^(3/4) = %.5f (claimed 0.471; sqrt2/3 = %.5f)"
          % (eps, r.x / eps, -r.fun * eps ** 0.75, np.sqrt(2) / 3))
# best line approximation of psi over a y-interval of length W: sup-error W^2/16 -> W <= 4 sqrt(w) is tight
for W in (0.1, 0.5, 1.0):
    ygrid = np.linspace(0, W, 4001)
    # minimax line fit of -y^2/2 (the linear part of psi is irrelevant): error W^2/16
    best = min(np.max(np.abs(-ygrid ** 2 / 2 - (sl * ygrid + ic))) for sl in np.linspace(-W, 0, 801)
               for ic in np.linspace(-W ** 2 / 8, W ** 2 / 8, 41))
    print("    minimax line error for psi over length %.1f: %.5f (W^2/16 = %.5f)" % (W, best, W ** 2 / 16))

# (9) lower bound vs 0.471 eps^(-3/4)
LB = lambda e: A_cf / (2 * e * (1 + np.log(1 / (2 * e))))
UB = lambda e: np.sqrt(2) / 3 * e ** -0.75
for e in (1e-4, 1e-5, 1e-6, 1e-10, 1e-16):
    print("(9) eps = %.0e: row-slice LB = %.4g, Thm 3.6 (p=2) bound = %.4g, ratio %.3f" % (e, LB(e), UB(e), LB(e) / UB(e)))
ec = brentq(lambda le: np.log(LB(10 ** le)) - np.log(UB(10 ** le)), -8, -3)
print("    crossover at eps = 10^%.3f" % ec)
print("    Summary constant A/2 = %.4f (note: 0.307)" % (A_cf / 2))
