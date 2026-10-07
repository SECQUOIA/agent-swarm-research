"""pricing050: independent Lagrangian upper bound with own multipliers and own
certified 1-D minimizations; own exactly feasible primal point.

Model (checked by template matching): max -sum_j c_j x_j, x in [0,10]^50,
rows i: sum_j a_ij x_j exp(g_ij x_j^p_ij) <= r_i.
For mu >= 0 and feasible x:  c.x >= -mu.r + sum_j min_[0,10] F_j,
F_j(x) = c_j x + sum_i mu_i a_ij x exp(g_ij x^p_ij).
Upper bound on the max objective: UB = mu.r - sum_j min F_j.

Certified min F_j (different method from the authors' natural/mean-value B&B):
monotonicity partition.  [0,10] is bisected until on every piece either
F' > 0 (candidate: F(left end)), F' < 0 (candidate: F(right end)), F'' < 0
(concave piece; candidates: both end values), or F'' > 0
(convex piece; candidate: F(c) + min_{d in piece-c} F'(c) d + F''_lo d^2/2).
min F >= min over candidates.  All enclosures in mpmath iv (40 digits);
candidate point values are evaluated at point intervals.
"""
import json
import os
from fractions import Fraction

import mpmath
import numpy as np
from mpmath import iv
from scipy.optimize import minimize

import common

m = common.load("pricing050")
N = 50
o = m["obj"]
assert o["sense"] == "max" and o["constant"] == "0" and o["nl"] is None and not o["quad"]
c = [Fraction(0)] * N
for j, v in o["lin"].items():
    c[j] = -Fraction(v)
assert all(v >= 0 for v in c)
for j in range(N):
    assert m["lb"][j] == "0" and m["ub"][j] == "10"
terms = []  # per row: list of (j, a, g, p) as strings / int
rhs = []
for row in m["cons"]:
    assert row["lb"] == "-INF" and row["constant"] == "0" and not row["lin"] and not row["quad"] and row["nl"][0] == "sum"
    rhs.append(row["ub"])
    tl, seen = [], set()
    for t in row["nl"][1:]:
        assert t[0] == "product" and len(t) == 3 and t[2][0] == "var"
        j, a = t[2][1], t[2][2]
        e = t[1]
        assert e[0] == "exp"
        e = e[1]
        if e[0] == "var":
            assert e[1] == j
            g, p = e[2], 1
        elif e[0] == "product" and e[1][0] == "square":
            assert e[1] == ("square", ("var", j, "1")) and e[2][0] == "num"
            g, p = e[2][1], 2
        else:
            assert e[0] == "product" and e[1] == ("power", ("var", j, "1"), ("num", "3")) and e[2][0] == "num"
            g, p = e[2][1], 3
        assert j not in seen and Fraction(a) < 0 and Fraction(g) < 0
        seen.add(j)
        tl.append((j, a, g, p))
    terms.append(tl)
out = dict(structure="5 rows, every term a_ij x_j exp(g_ij x_j^p), a<0, g<0, p in {1,2,3}; c_j >= 0",
           g_values=sorted({t[2] for tl in terms for t in tl}), rhs=rhs)

# ---------------- float dual optimisation ----------------
A = np.zeros((5, N)); G = np.zeros((5, N)); P = np.ones((5, N)); present = np.zeros((5, N), bool)
for i, tl in enumerate(terms):
    for j, a, g, p in tl:
        A[i, j], G[i, j], P[i, j], present[i, j] = float(a), float(g), p, True
cf = np.array([float(v) for v in c]); rf = np.array([float(v) for v in rhs])
xs = np.linspace(0, 10, 20001)


def rowterm(x):  # shape (5, N, len(x))
    return A[:, :, None] * x[None, None, :] * np.exp(G[:, :, None] * x[None, None, :] ** P[:, :, None])


RT = rowterm(xs)


def dual(mu):
    mu = np.maximum(mu, 0)
    Fv = cf[:, None] * xs[None, :] + np.tensordot(mu, RT, axes=(0, 0))
    return -mu @ rf + Fv.min(axis=1).sum()


best = None
for start in ([1, 1, 1, 1, 1], [0, 0, 0, 3, 2], [0.5] * 5, [2, 0, 0, 2, 2]):
    r = minimize(lambda z: -dual(z), np.array(start, float), method="Nelder-Mead",
                 options=dict(maxiter=20000, xatol=1e-10, fatol=1e-10))
    if best is None or r.fun < best.fun:
        best = r
mu0 = np.maximum(best.x, 0)
print("float dual:", -best.fun, "mu", mu0)

# ---------------- high-precision multipliers ----------------
mpmath.mp.dps = 50
act = [i for i in range(5) if mu0[i] > 1e-6]
print("active rows (by multiplier):", [m["cons"][i]["name"] for i in act])
Ai = [[mpmath.mpf(0)] * N for _ in range(5)]
Gi = [[mpmath.mpf(0)] * N for _ in range(5)]
Pi = [[1] * N for _ in range(5)]
for i, tl in enumerate(terms):
    for j, a, g, p in tl:
        Ai[i][j], Gi[i][j], Pi[i][j] = mpmath.mpf(a), mpmath.mpf(g), p


def Fp(j, x, mu):
    return c[j].numerator / mpmath.mpf(c[j].denominator) + sum(
        mu[k] * Ai[i][j] * mpmath.exp(Gi[i][j] * x ** Pi[i][j]) * (1 + Gi[i][j] * Pi[i][j] * x ** Pi[i][j])
        for k, i in enumerate(act))


def Fv(j, x, mu):
    return c[j].numerator / mpmath.mpf(c[j].denominator) * x + sum(
        mu[k] * Ai[i][j] * x * mpmath.exp(Gi[i][j] * x ** Pi[i][j]) for k, i in enumerate(act))


def argmins(mu):
    xo = []
    muf = np.zeros(5); muf[act] = [float(v) for v in mu]
    Fvals = cf[:, None] * xs[None, :] + np.tensordot(muf, RT, axes=(0, 0))
    for j in range(N):
        k = int(np.argmin(Fvals[j]))
        x = xs[k]
        if k in (0, len(xs) - 1):
            xo.append(mpmath.mpf(x))
            continue
        x = mpmath.findroot(lambda z: Fp(j, z, mu), mpmath.mpf(x))
        xo.append(x)
    return xo


def rows_at(xo):
    return [sum(Ai[i][j] * xo[j] * mpmath.exp(Gi[i][j] * xo[j] ** Pi[i][j]) for j in range(N)) for i in range(5)]


def eqs(*mu):
    xo = argmins(mu)
    rv = rows_at(xo)
    return [rv[i] - mpmath.mpf(rhs[i]) for i in act]


mus = mpmath.findroot(eqs, [mpmath.mpf(float(mu0[i])) for i in act], tol=mpmath.mpf(10) ** -40)
mus = [mus[k] for k in range(len(act))] if len(act) > 1 else [mus]
mu_str = [mpmath.nstr(v, 20) for v in mus]
print("multipliers (20 digits):", dict(zip([m["cons"][i]["name"] for i in act], mu_str)))
xo = argmins([mpmath.mpf(v) for v in mu_str])
out["multipliers"] = dict(zip([m["cons"][i]["name"] for i in act], mu_str))

# ---------------- certified 1-D minima (monotonicity partition) ----------------
iv.dps = 40
muI = [iv.mpf(v) for v in mu_str]
cI = [iv.mpf(v.numerator) / v.denominator for v in c]
tI = {}
for i, tl in enumerate(terms):
    for j, a, g, p in tl:
        tI[(i, j)] = (iv.mpf(a), iv.mpf(g), p)


def xp(X, p):
    r = X
    for _ in range(p - 1):
        r = r * X
    return r


def F_iv(j, X):
    s = cI[j] * X
    for k, i in enumerate(act):
        if (i, j) not in tI:
            continue
        a, g, p = tI[(i, j)]
        s = s + muI[k] * a * X * iv.exp(g * xp(X, p))
    return s


def F1_iv(j, X):
    s = cI[j]
    for k, i in enumerate(act):
        if (i, j) not in tI:
            continue
        a, g, p = tI[(i, j)]
        u = g * xp(X, p)
        s = s + muI[k] * a * iv.exp(u) * (1 + p * u)
    return s


def F2_iv(j, X):
    # d/dx [a e^{g x^p}(1 + p g x^p)] = a e^{u} g p x^{p-1} (1 + p + p u), u = g x^p
    s = iv.mpf(0)
    for k, i in enumerate(act):
        if (i, j) not in tI:
            continue
        a, g, p = tI[(i, j)]
        u = g * xp(X, p)
        xpm1 = xp(X, p - 1) if p > 1 else iv.mpf(1)
        s = s + muI[k] * a * iv.exp(u) * g * p * xpm1 * (1 + p + p * u)
    return s


def certify(j):
    stack = [(mpmath.mpf(0), mpmath.mpf(10))]
    cand = []
    npieces = 0
    while stack:
        lo, hi = stack.pop()
        npieces += 1
        X = iv.mpf([lo, hi])
        d1 = F1_iv(j, X)
        if d1.a > 0:
            cand.append(F_iv(j, iv.mpf(lo)).a)
            continue
        if d1.b < 0:
            cand.append(F_iv(j, iv.mpf(hi)).a)
            continue
        d2 = F2_iv(j, X)
        if d2.b < 0:  # concave piece: minimum at an end point
            cand.append(F_iv(j, iv.mpf(lo)).a)
            cand.append(F_iv(j, iv.mpf(hi)).a)
            continue
        if d2.a > 0 and hi - lo < mpmath.mpf("1e-7"):
            cc = (lo + hi) / 2
            C = iv.mpf(cc)
            fc, gc = F_iv(j, C), F1_iv(j, C)
            h = iv.mpf(d2.a)
            dlo, dhi = iv.mpf(lo) - C, iv.mpf(hi) - C
            # min over d in [dlo, dhi] of gc d + h d^2/2 (h > 0): unconstrained -gc^2/(2h) is a lower bound
            q = -(gc * gc) / (2 * h)
            cand.append((fc + q).a)
            continue
        assert hi - lo > mpmath.mpf("1e-30"), (j, lo, hi)
        mid = (lo + hi) / 2
        stack += [(lo, mid), (mid, hi)]
    return min(cand), npieces


mins, pieces = [], 0
for j in range(N):
    mn, npc = certify(j)
    mins.append(mn); pieces += npc
lagsum = sum(iv.mpf(v) for v in mins)
muR = sum(muI[k] * iv.mpf(rhs[i]) for k, i in enumerate(act))
UB = muR - lagsum  # max objective <= mu.r - sum min F_j
# width of certificate: compare with point values at the argmins
ptsum = sum(Fv(j, xo[j], [mpmath.mpf(v) for v in mu_str]) for j in range(N))
out["certificate"] = dict(pieces=pieces, upper_bound=mpmath.nstr(mpmath.mpf(UB.b), 20),
                          sum_minF_certified=mpmath.nstr(mpmath.mpf(lagsum.a), 25),
                          sum_F_at_argmins=mpmath.nstr(ptsum, 25),
                          slack_certified_vs_point=mpmath.nstr(ptsum - mpmath.mpf(lagsum.a), 4))
print("certificate:", out["certificate"])

# ---------------- own exactly feasible primal ----------------
xd = [Fraction(mpmath.nstr(v, 25)) if v > 0 else Fraction(0) for v in xo]
xd = [min(max(v, Fraction(0)), Fraction(10)) for v in xd]


def rows_iv(xv):
    XI = [iv.mpf(v.numerator) / v.denominator for v in xv]
    res = []
    for i, tl in enumerate(terms):
        s = iv.mpf(0)
        for j, a, g, p in tl:
            s = s + iv.mpf(a) * XI[j] * iv.exp(iv.mpf(g) * xp(XI[j], p))
        res.append(s)
    return res


# nudge: pick the variable whose increase lowers both active rows the most, raise it until rows hold with margin
rv = rows_iv(xd)
viol = [mpmath.mpf(rv[i].b) - mpmath.mpf(rhs[i]) for i in range(5)]
nud = None
if max(viol) >= 0:
    best_j, best_s = None, None
    for j in range(N):
        if xd[j] <= 0 or xd[j] >= 10:
            continue
        der = [mpmath.mpf(Ai[i][j] * mpmath.exp(Gi[i][j] * mpmath.mpf(float(xd[j])) ** Pi[i][j]) *
                          (1 + Gi[i][j] * Pi[i][j] * mpmath.mpf(float(xd[j])) ** Pi[i][j])) for i in act]
        if all(d < 0 for d in der):
            sc = max(der)  # least negative
            if best_s is None or sc < best_s:
                best_j, best_s = j, sc
    delta = Fraction(mpmath.nstr(-max(viol) * 10 / best_s, 3)) + Fraction(1, 10 ** 20)
    xd[best_j] += delta
    nud = (m["names"][best_j], float(delta))
    rv = rows_iv(xd)
slack = [mpmath.mpf(rhs[i]) - mpmath.mpf(rv[i].b) for i in range(5)]
assert min(slack) > 0 and all(0 <= v <= 10 for v in xd)
objp = -sum(c[j] * xd[j] for j in range(N))
out["own_primal"] = dict(objective_exact=str(float(objp)), objective_20=mpmath.nstr(mpmath.mpf(objp.numerator) / objp.denominator, 20),
                         min_row_slack=mpmath.nstr(min(slack), 3), nudge=nud)
print("own primal:", out["own_primal"])
out["gap"] = mpmath.nstr(mpmath.mpf(UB.b) - mpmath.mpf(objp.numerator) / objp.denominator, 4)
print("gap UB - primal:", out["gap"])
# MINLPLib p1
sol = common.read_sol(os.path.join(common.HERE, "sol", "pricing050.p1.sol"))
xp1 = [Fraction(sol.get(nm, "0")) for nm in m["names"]]
rv1 = rows_iv(xp1)
out["minlplib_p1"] = dict(objective=float(-sum(c[j] * xp1[j] for j in range(N))),
                          max_row_violation=float(max(mpmath.mpf(rv1[i].b) - mpmath.mpf(rhs[i]) for i in range(5))))
print("p1:", out["minlplib_p1"])
json.dump(out, open(os.path.join(common.HERE, "logs", "pricing050.json"), "w"), indent=1)
