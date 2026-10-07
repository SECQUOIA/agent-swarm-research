"""Referee checks for the third revision of theory-robust-lb/robust-lower-bound.md.
Shares no code with the authors, the review, the recheck or the confirmation.
Run: OMP_NUM_THREADS=1 python3 check_r1.py > logs/check_r1.log

(1) E_d(L) at y1 = 0.38, d = 2..12: LP in a Legendre basis on a uniform grid (plus Chebyshev
    extrema and the kinks +-y1), lower bound = grid LP value, upper = error of the LP polynomial on
    a 2e6-point grid.  Compare with the rounded-down values printed in Section 3.3.
(2) Class-(a) gap: gamma_2 = min_q [max_s (L - q s) + max_s (q s - U)] (s = y^2; constants cancel,
    odd terms drop by evenness) by a scalar search, against the closed form y1^2 (1-A)/A, for all
    20 parameter sets of logs/scan_bd.log.
(3) Corner-box threshold mu0 = inf ln(8/vol)/g(-a,-b,-c) over boxes [-1,-a]x[-1,-b]x[-1,-c]:
    vectorised 81^3 grid, then Powell polish from the 5 best grid points, and a
    differential-evolution cross-check.  Class-(a) ceilings exp(mu0 gamma_a/3), and mu < mu0 for
    every row of scan_bd.log.
(4) Arithmetic quoted in Sections 3.3, 3.4 and 6.5.
"""
import re
import time
import numpy as np
from numpy.polynomial import legendre as Lg
from scipy.optimize import linprog, minimize, minimize_scalar, differential_evolution

t0 = time.time()


def Lfun(y, y1):
    a = np.abs(y)
    return np.where(a <= y1, a * a, 2 * y1 * a - y1 * y1)


def Ufun(y, y1, eta, ev):
    a = np.abs(y)
    c = 1 + eta + ev
    return c * a * a - eta * a * a - (1 - eta) * np.maximum(a - y1, 0) ** 2


# ------------------------------------------------------------------ (1)
def E_leg(y1, d):
    y = np.unique(np.concatenate([np.linspace(-1, 1, 12001), np.cos(np.linspace(0, np.pi, 3001)), [-y1, y1]]))
    V = Lg.legvander(y, d)
    k = d + 1
    Ly = Lfun(y, y1)
    A = np.vstack([np.hstack([V, -np.ones((len(y), 1))]), np.hstack([-V, -np.ones((len(y), 1))])])
    b = np.concatenate([Ly, -Ly])
    r = linprog(np.r_[np.zeros(k), 1.0], A_ub=A, b_ub=b, bounds=[(None, None)] * k + [(0, None)], method="highs")
    yf = np.linspace(-1, 1, 2_000_001)
    up = np.max(np.abs(Lfun(yf, y1) - Lg.legval(yf, r.x[:k])))
    return r.fun, up


print("(1) E_d(L), y1 = 0.38, Legendre basis, uniform + Chebyshev grid")
claimed = {2: 0.04508, 4: 0.01009, 6: 0.002634, 8: 0.002536, 10: 0.001716, 12: 0.000910}
E = {}
for d in range(2, 13):
    lo, hi = E_leg(0.38, d)
    E[d] = (lo, hi)
    extra = ""
    if d in claimed:
        extra = "  claimed '>= %g': %s" % (claimed[d], "OK (claimed <= grid-LP value)" if claimed[d] <= lo else "NOT a lower bound")
    print("  d = %2d: [%.8f, %.8f] width %.1e  d^2 E_d = %.4f%s" % (d, lo, hi, hi - lo, d * d * lo, extra))
ev = [d * d * E[d][0] for d in range(2, 13, 2)]
od = [d * d * E[d][0] for d in range(3, 12, 2)]
print("  even d: d^2 E_d in [%.4f, %.4f] (argmin d = %d, argmax d = %d)" % (
    min(ev), max(ev), 2 + 2 * int(np.argmin(ev)), 2 + 2 * int(np.argmax(ev))))
print("  odd d:  d^2 E_d in [%.4f, %.4f]" % (min(od), max(od)))
print("  max |E_{2k+1} - E_{2k}| over k = 1..5 (lower bounds): %.1e" % max(abs(E[2 * k + 1][0] - E[2 * k][0]) for k in range(1, 6)))
print("  odd d: d^2 E_d > (d-1)^2 E_{d-1} for all odd d: %s" % all(d * d * E[d][0] > (d - 1) ** 2 * E[d - 1][0] for d in range(3, 12, 2)))


# ------------------------------------------------------------------ scan rows
rows = []
pat = re.compile(r"^(\S+) y1=([\d.]+) eta=([\d.]+) eps=([\d.]+) gamma\(1\)=([\d.]+) .*per-var=([\d.]+) mu=([\d.]+)")
with open("../../theory-robust-lb/logs/scan_bd.log") as fh:
    for line in fh:
        m = pat.match(line)
        if m:
            rows.append((m.group(1), (float(m.group(2)), float(m.group(3)), float(m.group(4))),
                         float(m.group(5)), float(m.group(6)), float(m.group(7))))
sets = sorted({r[1] for r in rows})
print("\nscan_bd.log: %d rows, %d distinct parameter sets" % (len(rows), len(sets)))


# ------------------------------------------------------------------ (2)
def gamma_closed(y1, eta, ev):
    A = 1 + ev - (1 - eta) * (1 - y1) ** 2
    return y1 ** 2 * (1 - A) / A


def gamma2_search(y1, eta, ev):
    y = np.linspace(0, 1, 200001)
    s = y * y
    Lv, Uv = Lfun(y, y1), Ufun(y, y1, eta, ev)

    def G(q):
        return np.max(Lv - q * s) + np.max(q * s - Uv)
    qs = np.linspace(0, 2, 2001)
    q0 = qs[np.argmin([G(q) for q in qs])]
    r = minimize_scalar(G, bounds=(max(q0 - 0.002, 0), q0 + 0.002), method="bounded", options={"xatol": 1e-12})
    return r.fun


print("\n(2) class-(a) gap: scalar search vs closed form y1^2 (1-A)/A")
gam_a = {}
worst = 0
for p in sets:
    gs, gc = gamma2_search(*p), gamma_closed(*p)
    gam_a[p] = gc
    worst = max(worst, abs(gs - gc))
    print("  %-20s search %.7f  closed %.7f" % (p, gs, gc))
print("  max |search - closed| = %.1e" % worst)


# ------------------------------------------------------------------ (3)
def gad(y1, eta, ev):
    b, bp, c = 2 * y1, 2 * eta + 2 * (1 - eta) * (1 - y1), 1 + eta + ev
    z1, k = 2 * eta * y1 / bp, 2 * (1 - eta) * y1

    def u(z):
        z = np.abs(z)
        return np.where(z <= z1, bp ** 2 * z ** 2 / (4 * eta), (bp * z + k) ** 2 / 4 - (1 - eta) * y1 ** 2)

    def gneg(a, bb, cc):  # g at (-a, -bb, -cc)
        return y1 ** 2 * a ** 2 + b * a * bb + c * bb ** 2 + u(cc) + bp * bb * cc
    return gneg


def mu0_of(p, seed=1):
    gneg = gad(*p)

    def obj(v):
        a, bb, cc = v
        if min(v) < 0 or max(v) >= 1:
            return 1e9
        val = gneg(a, bb, cc)
        if val <= 0:
            return 1e9
        return float(np.log(8 / ((1 - a) * (1 - bb) * (1 - cc))) / val)
    t = np.linspace(0.005, 0.985, 81)
    A, B, Cc = np.meshgrid(t, t, t, indexing="ij")
    vals = np.log(8 / ((1 - A) * (1 - B) * (1 - Cc))) / gneg(A, B, Cc)
    idx = np.argsort(vals.ravel())[:5]
    best = (np.inf, None)
    for i in idx:
        x0 = np.array([A.ravel()[i], B.ravel()[i], Cc.ravel()[i]])
        r = minimize(obj, x0, method="Powell", options={"xtol": 1e-10, "ftol": 1e-13, "maxiter": 20000})
        if r.fun < best[0]:
            best = (r.fun, r.x)
    de = differential_evolution(obj, [(0, 0.99)] * 3, seed=seed, tol=1e-12, maxiter=400, polish=True)
    return best[0], best[1], de.fun


print("\n(3) corner-box mu0 (grid + Powell; differential evolution cross-check), class-(a) ceilings")
authors = {}
with open("../../theory-robust-lb/logs/revision3_checks.log") as fh:
    for line in fh:
        m = re.match(r"^\s+\(([\d.]+), ([\d.]+), ([\d.]+)\)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", line)
        if m:
            authors[(float(m.group(1)), float(m.group(2)), float(m.group(3)))] = (float(m.group(4)), float(m.group(6)))
mu0 = {}
for p in sets:
    m, x, mde = mu0_of(p)
    mu0[p] = m
    cap = np.exp(m * gam_a[p] / 3)
    au = authors.get(p, (np.nan, np.nan))
    print("  %-20s mu0 %.5f (DE %.5f)  box -(%.3f, %.3f, %.3f)  ceiling(a)/var %.4f | authors mu0 %.4f ceiling %.4f" % (
        p, m, mde, *x, cap, *au))
ref = (0.38, 0.05, 0.02)
caps = {p: np.exp(mu0[p] * gam_a[p] / 3) for p in sets}
nonref = [(caps[p], p) for p in sets if p != ref]
print("  reference: mu0 %.4f, ceiling %.4f per variable" % (mu0[ref], caps[ref]))
print("  19 non-reference sets: class-(a) ceilings %.4f (%s) .. %.4f (%s)" % (min(nonref)[0], min(nonref)[1], max(nonref)[0], max(nonref)[1]))
print("  max |mu0 - authors' mu0| = %.1e" % max(abs(mu0[p] - authors[p][0]) for p in sets))
cls_at = {}
for cls, p, g, base, mu in rows:
    cls_at.setdefault(p, set()).add(cls)
print("  classes run at (0.38, 0.005, 0.002): %s" % sorted(cls_at[(0.38, 0.005, 0.002)]))
marg = []
for cls, p, g, base, mu in rows:
    marg.append((mu0[p] - mu, cls, p, mu, mu0[p]))
print("  all 26 rows mu < mu0: %s; smallest margin %.3f at %s %s (mu %.3f, mu0 %.4f)" % (all(m[0] > 0 for m in marg), *min(marg)))

# ------------------------------------------------------------------ (4)
print("\n(4) arithmetic")
w = 0.02 + 0.05 * (1 - 0.38) ** 2
print("  band width eps_v + eta (1-y1)^2 = %.5f; 2 E_2 - width = %.5f (> 0.0509: %s)" % (w, 2 * E[2][0] - w, 2 * E[2][0] - w > 0.0509))
for lab, p, g in [("b4 ref", ref, 0.00777), ("b4 0.30", (0.30, 0.005, 0.002), 0.0247), ("b6 ref", ref, 0.00237), ("b6 0.50", (0.50, 0.005, 0.002), 0.0073)]:
    print("  %-8s exp(mu0 gamma/3) = %.4f" % (lab, np.exp(mu0[p] * g / 3)))
print("  4 ln 64 = %.4f; 2 * 4 ln 64 = %.3f" % (4 * np.log(64), 8 * np.log(64)))
print("\ntotal time %.1f s" % (time.time() - t0))
