"""Third revision: checks for the confirmation recheck (reviews/recheck-robust-lb-confirm.md).
Run: OMP_NUM_THREADS=1 python3 revision3_checks.py > logs/revision3_checks.log

(1) E_d(L) at y1 = 0.38 for every d = 2..12 (odd degrees included), full Chebyshev basis:
    grid-LP lower bound and the fine-grid error of the LP polynomial; d^2 E_d for even and odd d.
(2) Corner-box threshold mu0 for all distinct parameter sets of logs/scan_bd.log (the second
    revision computed it for 8 of them), the check "minimizing mu < mu0" for every row, and the
    class-(a) ceiling exp(mu0 gamma_a / 3) per variable for every set.
The gadget and the mu0 search are the same as in revision2_checks.py.
"""
import re
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog, minimize


# ---------------------------------------------------------------- (1)
def L_of(y, y1):
    return np.where(np.abs(y) <= y1, y * y, 2 * y1 * np.abs(y) - y1 * y1)


def E_full(y1, d, M=4001, Mf=400001):
    y = np.cos(np.linspace(0, np.pi, M))
    V = C.chebvander(y, d)
    k = V.shape[1]
    A = np.vstack([np.hstack([-V, -np.ones((M, 1))]), np.hstack([V, -np.ones((M, 1))])])
    b = np.concatenate([-L_of(y, y1), L_of(y, y1)])
    r = linprog(np.r_[np.zeros(k), 1.0], A_ub=A, b_ub=b, bounds=[(None, None)] * k + [(0, None)], method="highs")
    yf = np.linspace(-1, 1, Mf)
    err = np.max(np.abs(L_of(yf, y1) - C.chebval(yf, r.x[:k])))
    return r.fun, err


print("(1) E_d(L) at y1 = 0.38, full Chebyshev basis (grid-LP lower bound, fine-grid error of the LP polynomial)")
E = {}
for d in range(2, 13):
    lo, hi = E_full(0.38, d)
    E[d] = (lo, hi)
    print("  d = %2d: E_d in [%.8f, %.8f]  width %.1e  d^2 E_d = %.4f" % (d, lo, hi, hi - lo, d * d * lo))
ev = [d * d * E[d][0] for d in range(2, 13, 2)]
od = [d * d * E[d][0] for d in range(3, 13, 2)]
print("  d^2 E_d over even d = 2..12: %.4f .. %.4f; over odd d = 3..11: %.4f .. %.4f" % (min(ev), max(ev), min(od), max(od)))
print("  max |E_{2k+1} - E_{2k}| (lower bounds), k = 1..5: %.1e" % max(abs(E[2 * k + 1][0] - E[2 * k][0]) for k in range(1, 6)))


# ---------------------------------------------------------------- (2)
def gadget(y1, eta, ev):
    b, bp, c = 2 * y1, 2 * eta + 2 * (1 - eta) * (1 - y1), 1 + eta + ev
    z1, k = 2 * eta * y1 / bp, 2 * (1 - eta) * y1

    def u(z):
        z = abs(z)
        return bp**2 * z**2 / (4 * eta) if z <= z1 else (bp * z + k)**2 / 4 - (1 - eta) * y1**2

    def g(x, yy, z):
        return y1**2 * x**2 + b * x * yy + c * yy**2 + u(z) + bp * yy * z
    A = 1 + ev - (1 - eta) * (1 - y1)**2
    return g, y1**2 * (1 - A) / A


def mu0_corner(y1, eta, ev, seed=0):
    """min over boxes [-1,-a]x[-1,-b]x[-1,-c] of ln(8/vol)/g(-a,-b,-c)."""
    g, gam = gadget(y1, eta, ev)

    def obj(v):
        a_, b_, c_ = np.clip(v, 0, 0.999)
        return np.log(8 / ((1 - a_) * (1 - b_) * (1 - c_))) / g(-a_, -b_, -c_)
    rng = np.random.default_rng(seed)
    best = None
    for s in list(rng.uniform(0, 0.95, (40, 3))) + [np.array([0.5, 0.87, 0.81])]:
        r = minimize(obj, s, method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-10, "maxiter": 4000})
        if best is None or r.fun < best.fun:
            best = r
    return best.fun, gam


rows = []
pat = re.compile(r"^(\S+) y1=([\d.]+) eta=([\d.]+) eps=([\d.]+) gamma\(1\)=([\d.]+) .* per-var=([\d.]+) mu=([\d.]+)")
with open("logs/scan_bd.log") as fh:
    for line in fh:
        m = pat.match(line)
        if m:
            rows.append((m.group(1), (float(m.group(2)), float(m.group(3)), float(m.group(4))),
                         float(m.group(5)), float(m.group(6)), float(m.group(7))))
sets = sorted({r[1] for r in rows})
mu0 = {p: mu0_corner(*p) for p in sets}
print("\n(2) corner-box mu0 for all %d distinct parameter sets of logs/scan_bd.log (%d rows)" % (len(sets), len(rows)))
print("  %-20s %-8s %-11s %-18s" % ("(y1, eta, eps_v)", "mu0", "gamma_a", "class-(a) ceiling/var"))
for p in sets:
    m0, gam = mu0[p]
    print("  %-20s %.4f   %.5f     %.4f" % (p, m0, gam, np.exp(m0 * gam / 3)))
print("  rows: class, parameters, row gamma, computed base/var, minimizing mu, mu0, mu < mu0, row ceiling/var")
margins = []
for cls, p, gam, base, mu in rows:
    m0 = mu0[p][0]
    margins.append((m0 - mu, cls, p))
    print("  %-3s %-20s %.5f  %.5f  %.3f  %.4f  %s  %.4f" % (cls, p, gam, base, mu, m0, mu < m0, np.exp(m0 * gam / 3)))
print("  all rows mu < mu0: %s; smallest margin mu0 - mu = %.3f (%s %s)" % (all(x[0] > 0 for x in margins), *min(margins)))
ref = (0.38, 0.05, 0.02)
seven = [(0.38, 0.01, 0.005), (0.38, 0.05, 0.1), (0.38, 0.05, 0.2), (0.30, 0.01, 0.005),
         (0.45, 0.01, 0.005), (0.30, 0.005, 0.002), (0.50, 0.005, 0.002)]
cap = {p: np.exp(mu0[p][0] * mu0[p][1] / 3) for p in sets}
s7 = [cap[p] for p in seven]
sall = [cap[p] for p in sets if p != ref]
print("  class-(a) ceiling at the reference set: %.4f per variable" % cap[ref])
print("  class-(a) ceilings, seven non-reference sets of Section 6.5: %.4f .. %.4f" % (min(s7), max(s7)))
print("  class-(a) ceilings, all %d non-reference sets of scan_bd.log: %.4f .. %.4f (max at %s)"
      % (len(sall), min(sall), max(sall), max((cap[p], p) for p in sets if p != ref)[1]))
