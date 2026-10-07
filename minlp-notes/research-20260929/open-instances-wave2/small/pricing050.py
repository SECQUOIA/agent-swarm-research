"""pricing050: rigorous upper bound (maximization) by Lagrangian relaxation of the 5 rows.

Min form: min c.x, x in [0,10]^50, h_i(x) = sum_j psi_ij(x_j) <= r_i, psi_ij(x) = a_ij x exp(g_ij x^p_ij).
For mu >= 0 and every feasible x:  c.x >= c.x + sum_i mu_i (h_i(x) - r_i)
                                         >= -mu.r + sum_j min_{[0,10]} F_j,
F_j(x) = c_j x + sum_i mu_i psi_ij(x). Each 1-D minimum is certified by an interval
branch and bound in mpmath.iv (natural extension and mean-value form). The maximization
objective of the file is -c.x, so  max <= mu.r - sum_j m_j.

Multipliers and primal: Kelley cutting planes on a grid, then Newton (50 digits) on the
KKT system of the Lagrangian minimizers with rows e5, e6 active.

Usage: python3 pricing050.py
"""
import os
import sys
import time
from fractions import Fraction

import mpmath as mp
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402
import ia  # noqa: E402
import pricing050_model as pm  # noqa: E402
from ia import AD  # noqa: E402

LOG = open(os.path.join(ev.HERE, "logs", "pricing050.log"), "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


I, cF, rows = pm.parse()
n, m = 50, 5
c = np.array([float(v) for v in cF])
r = np.array([float(R["r"]) for R in rows])
A = np.zeros((m, n))
P = np.ones((m, n))
G = np.zeros((m, n))
for i, R in enumerate(rows):
    for j, (a, p, g) in R["terms"].items():
        A[i, j], P[i, j], G[i, j] = float(a), p, float(g)

# ---------------- multipliers: Kelley on a grid ----------------
xg = np.linspace(0, 10, 20001)
PSI = np.array([[A[i, j] * xg * np.exp(G[i, j] * xg ** P[i, j]) for j in range(n)] for i in range(m)])


def Lgrid(mu):
    F = c[:, None] * xg[None, :] + np.einsum("i,ijk->jk", mu, PSI)
    k = np.argmin(F, axis=1)
    return -mu @ r + F[np.arange(n), k].sum(), -r + PSI[:, np.arange(n), k].sum(axis=1)


cuts, mu, best = [], np.ones(m), -np.inf
for it in range(500):
    v, s = Lgrid(mu)
    if v > best:
        best, bestmu = v, mu.copy()
    cuts.append((v, s, mu.copy()))
    Aub = np.array([np.concatenate([[1.0], -sk]) for vk, sk, mk in cuts])
    bub = np.array([vk - sk @ mk for vk, sk, mk in cuts])
    res = linprog(np.concatenate([[-1.0], np.zeros(m)]), A_ub=Aub, b_ub=bub, bounds=[(None, None)] + [(0, 50)] * m, method="highs")
    mu = res.x[1:]
    if -res.fun - best < 1e-8:
        break
say(f"Kelley: {it} iterations, grid dual {best:.10f}, mu = {bestmu}")
act = [i for i in range(m) if bestmu[i] > 1e-6]
say("rows with positive multiplier:", [f"e{i + 2}" for i in act])

# ---------------- Newton on the KKT system (50 digits) ----------------
mp.mp.dps = 50
xs0 = np.array([xg[np.argmin(c[j] * xg + bestmu @ PSI[:, j, :])] for j in range(n)])
inner = [j for j in range(n) if xs0[j] > 1e-3]
at0 = [j for j in range(n) if j not in inner]
assert all(xs0[j] < 10 - 1e-3 for j in inner)
Amp = [[mp.mpf(rows[i]["terms"][j][0]) if j in rows[i]["terms"] else mp.mpf(0) for j in range(n)] for i in range(m)]
Gmp = [[mp.mpf(rows[i]["terms"][j][2]) if j in rows[i]["terms"] else mp.mpf(0) for j in range(n)] for i in range(m)]
cmp_ = [mp.mpf(v.numerator) / v.denominator for v in cF]


def psi(i, j, x):
    return Amp[i][j] * x * mp.exp(Gmp[i][j] * x ** int(P[i, j]))


def dpsi(i, j, x):
    p = int(P[i, j])
    return Amp[i][j] * mp.exp(Gmp[i][j] * x ** p) * (1 + Gmp[i][j] * p * x ** p)


def Fk(z):
    x = [mp.mpf(0)] * n
    for k, j in enumerate(inner):
        x[j] = z[k]
    mus = z[len(inner):]
    out = [cmp_[j] + sum(mus[q] * dpsi(i, j, x[j]) for q, i in enumerate(act)) for j in inner]
    out += [sum(psi(i, j, x[j]) for j in range(n)) - mp.mpf(rows[i]["r"]) for i in act]
    return out


z = [mp.mpf(xs0[j]) for j in inner] + [mp.mpf(bestmu[i]) for i in act]
nz = len(z)
for it in range(40):
    Fz = Fk(z)
    res = max(abs(v) for v in Fz)
    if res < mp.mpf("1e-45"):
        break
    J = mp.matrix(nz, nz)
    h = mp.mpf("1e-22")
    for col in range(nz):
        zz = list(z)
        zz[col] += h
        Fc = Fk(zz)
        for row in range(nz):
            J[row, col] = (Fc[row] - Fz[row]) / h
    dz = mp.lu_solve(J, mp.matrix([-v for v in Fz]))
    z = [z[k] + dz[k] for k in range(nz)]
say(f"Newton: {it} iterations, residual {mp.nstr(max(abs(v) for v in Fk(z)), 3)}")
xstar = [mp.mpf(0)] * n
for k, j in enumerate(inner):
    xstar[j] = z[k]
mustar = [mp.mpf(0)] * m
for q, i in enumerate(act):
    mustar[i] = z[len(inner) + q]
say("mu* =", [mp.nstr(v, 20) for v in mustar])
assert all(v >= 0 for v in mustar)
fstar = sum(cmp_[j] * xstar[j] for j in range(n))
say("KKT point: min-form objective", mp.nstr(fstar, 20), "; max-form", mp.nstr(-fstar, 20))

# ---------------- exactly feasible primal point ----------------
# round to 17 digits; rows e5,e6 may be violated by ~1e-14; increase one x_j (c_j > 0) whose psi
# terms decrease (more negative) in both active rows, until both rows hold with margin.
xr = [mp.mpf(mp.nstr(v, 17)) for v in xstar]


def rowvals(x):
    return [sum(psi(i, j, x[j]) for j in range(n)) - mp.mpf(rows[i]["r"]) for i in range(m)]


viol = max(rowvals(xr))
if viol > 0:
    cand = [j for j in inner if cF[j] > 0 and all(dpsi(i, j, xr[j]) < -1 for i in act)]
    jb = min(cand, key=lambda j: cmp_[j] / min(-dpsi(i, j, xr[j]) for i in act))
    slope = min(-dpsi(i, j_, xr[j_]) for i in act for j_ in [jb])
    xr[jb] = mp.mpf(mp.nstr(xr[jb] + 4 * viol / slope + mp.mpf("1e-15"), 17))
    say(f"repair: x{jb + 2} increased by {mp.nstr(4 * viol / slope + mp.mpf('1e-15'), 3)} (rounding violation {mp.nstr(viol, 3)})")
xs = [mp.nstr(v, 17) for v in xr]
rp = ev.evaluate(I, xs, dps=50)
say(f"primal point: max-form obj {mp.nstr(rp['obj'], 20)}, max row viol {mp.nstr(rp['row_viol'], 3)}, "
    f"bound viol {mp.nstr(rp['bound_viol'], 3)}, row slacks {[mp.nstr(v, 3) for v in rowvals([mp.mpf(s) for s in xs])]}")
with open(os.path.join(ev.HERE, "logs", "pricing050_primal.txt"), "w") as fo:
    for j, nm in enumerate(I["names"]):
        fo.write(f"{nm} {xs[j]}\n")
r1 = ev.eval_sol("pricing050.p1")
say(f"MINLPLib p1: obj {mp.nstr(r1['obj'], 20)}, max row viol {mp.nstr(r1['row_viol'], 3)} ({r1['worst_row']})")

# ---------------- rigorous dual ----------------
iv = mp.iv
iv.dps = 30
mud = [float(v) for v in mustar]                   # exact binary multipliers used in the bound
assert all(v >= 0 for v in mud)
muI = [iv.mpf(v) for v in mud]


def F_iv(j, X):
    """interval AD (value, derivative) of F_j over the interval X."""
    x = AD(X, (iv.mpf(1),))
    s = x * iv.mpf(cF[j].numerator)
    for i in range(m):
        if mud[i] == 0 or j not in rows[i]["terms"]:
            continue
        a, p, g = rows[i]["terms"][j]
        xp = x
        for _ in range(p - 1):
            xp = xp * x
        e = ia.ad_exp(xp * iv.mpf(g), iv.exp)
        s = s + (x * e) * (iv.mpf(a) * muI[i])
    return s


def min1d(j, tol=1e-13):
    ub = mp.inf
    stack = [(mp.mpf(0), mp.mpf(10))]
    leaves_lb = mp.inf
    nbox = 0
    while stack:
        lo, hi = stack.pop()
        nbox += 1
        X = iv.mpf([lo, hi])
        s = F_iv(j, X)
        mid = (lo + hi) / 2
        fm = F_iv(j, iv.mpf(mid)).v
        ub = min(ub, mp.mpf(fm.b))
        mv = fm + s.g[0] * (X - iv.mpf(mid))
        lb = max(mp.mpf(s.v.a), mp.mpf(mv.a))
        if lb >= ub - tol:
            leaves_lb = min(leaves_lb, lb)
            continue
        if hi - lo < mp.mpf("1e-14"):
            leaves_lb = min(leaves_lb, lb)
            continue
        stack += [(lo, mid), (mid, hi)]
    return leaves_lb, ub, nbox


t0 = time.time()
total = iv.mpf(0)
for i in range(m):
    total = total - iv.mpf(mud[i]) * iv.mpf(rows[i]["r"])
mins = []
nb = 0
for j in range(n):
    lb, ub, nbox = min1d(j)
    nb += nbox
    mins.append((lb, ub))
    total = total + iv.mpf(lb)
L = mp.mpf(total.a)
gapsum = sum(u - l for l, u in mins)
say(f"1-D B&B: {nb} boxes in {time.time() - t0:.1f} s; sum of (ub - lb) over variables {mp.nstr(gapsum, 3)}")
say(f"Lagrangian lower bound (min form): {mp.nstr(L, 17)}")
say(f"RIGOROUS UPPER BOUND (max form, pricing050): {mp.nstr(-L, 17)}")
say(f"primal (max form) {mp.nstr(rp['obj'], 17)}; gap {mp.nstr(-L - rp['obj'], 3)}")
