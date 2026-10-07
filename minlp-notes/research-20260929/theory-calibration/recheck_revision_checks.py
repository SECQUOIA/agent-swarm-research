"""Targeted checks for the second revision of scouting.md (recheck items R2, R4-R6, R8
and the optional items).  Floating point, not certified.  Written by the note's author,
separately from the reviewers' scripts.

A. Symbolic (sympy):
   A1 (R5) Euler Riccati defect for xdot = alpha x + u, l = (u^2 + q x^2)/2:
       F(P(t+h)) - P(t) = h^2 (P - alpha)(alpha P + q) + O(h^3), with the continuous
       Riccati equation Pdot = P^2 - 2 alpha P - q; exact zero for alpha = q = 0.
   A2 (R2) Tilted defect: with s = P - 2e, e = eps exp(-lam t),
       F(s(t+h)) - s(t) = 4 h e (lam/2 - alpha + P - e) + O(h^2).
   A3 (optional, Remark 5.2(c)) r - (x^2+u^2)/4 = (u/2 - x^3)^2 + 3x^2/4, and the
       last-stage residual at x = 0 for U = [-K, K]: h u^2/2 - h^4 u^4/4.
   A4 (optional, Remark 5.2(b)) the coercivity identity for n = 2 states and m = 2
       controls with random polynomial data (the recheck did m = 1).
B. (R2) Tilted scalar LQ: exact threshold h_0 of the transferred family, located by a
   geometric scan plus bisection, using the one-dimensional criterion
   F(s_{t+1}) >= s_t (t = 1..N-1), which is equivalent to PSD stage Hessians.  Compared
   with the leading-order prediction h_0 ~ 4 e(T) m(T) / |K(T)|, where
   m = lam/2 - alpha + P - e and K = (P - alpha)(alpha P + q).  Closed-form P.
C. (R6) Uncorrected sampled field family (Proposition 5.1 family, non-strict S = V) for
   alpha = -2, q = 0, Phi = x^2/2: gap / h.  Stage residuals minimized exactly by
   minimizing over u in closed form (clipped) and then over the piecewise-quadratic
   function of x (own method).  The transferred field family is computed too, as a
   cross-check against the review's c4 numbers.
D. (R4) Check 5.3: differences between the three implementations, read from their logs.
"""

import json
import os
import random
import time

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
out = {}
t_start = time.time()

# ------------------------------------------------------------------ A1, A2
h, al, q, lam, eps, t = sp.symbols("h alpha q lam eps t", real=True)
Pf = sp.Function("P")
Pdot_rule = lambda P: P**2 - 2 * al * P - q


def taylor_next(expr_t, order=3):
    """expr(t+h) as a series in h, using P' = Pdot_rule(P)."""
    terms, d = [], expr_t
    for k in range(order + 1):
        terms.append(d * h**k / sp.factorial(k))
        d = sp.diff(d, t).subs(sp.Derivative(Pf(t), t), Pdot_rule(Pf(t)))
    return sum(terms)


def F_map(Pn):
    return h * q + (1 + al * h) ** 2 * Pn / (1 + h * Pn)


P = Pf(t)
ser = sp.series(F_map(taylor_next(P)) - P, h, 0, 3).removeO()
c1 = sp.simplify(ser.coeff(h, 1))
c2 = sp.factor(sp.simplify(ser.coeff(h, 2)))
out["A1"] = {"h1": str(c1), "h2": str(c2),
             "h2_equals_(P-alpha)(alpha P+q)": bool(sp.simplify(c2 - (P - al) * (al * P + q)) == 0)}
# exact zero for alpha = q = 0: P = 1/(c + T - t) satisfies F(P(t+h)) = P(t)
cc, TT = sp.symbols("c T", positive=True)
Pex = 1 / (cc + TT - t)
out["A1"]["alpha=q=0_exact_zero"] = bool(sp.simplify((Pex.subs(t, t + h) / (1 + h * Pex.subs(t, t + h))) - Pex) == 0)
e = eps * sp.exp(-lam * t)
s = P - 2 * e
ser2 = sp.series(F_map(taylor_next(s, 2)) - s, h, 0, 2).removeO()
d1 = sp.simplify(ser2.coeff(h, 1))
out["A2"] = {"h1": str(sp.factor(d1)),
             "h1_equals_4e(lam/2-alpha+P-e)": bool(sp.simplify(d1 - 4 * e * (lam / 2 - al + P - e)) == 0)}
print("A1", out["A1"])
print("A2", out["A2"])

# ------------------------------------------------------------------ A3
x, u, K = sp.symbols("x u K", real=True)
r = u**2 / 2 + x**6 + x**2 - x**3 * u  # l + S_x g, S = -x^4/4, g = u
last = h * u**2 / 2 + (-(h * u) ** 4 / 4) - 0  # h l(0,u) + S(T, h u) - S(T-h, 0)
out["A3"] = {"identity": bool(sp.expand(r - (x**2 + u**2) / 4 - ((u / 2 - x**3) ** 2 + sp.Rational(3, 4) * x**2)) == 0),
             "last_stage_residual_x0": str(sp.expand(last)),
             "nonneg_iff_h^3u^2<=2": bool(sp.simplify(sp.factor(last) - h * u**2 / 4 * (2 - h**3 * u**2)) == 0)}
print("A3", out["A3"])

# ------------------------------------------------------------------ A4
random.seed(11)
x1, x2, u1, u2 = sp.symbols("x1 x2 u1 u2", real=True)
xi1, xi2, et1, et2 = sp.symbols("xi1 xi2 eta1 eta2", real=True)
Z = [x1, x2, u1, u2]
mon = [1, x1, x2, u1, u2, x1 * x2, x1**2, u1 * u2, x2 * u1, x1 * u2, x1**2 * u1, x2**3, u2**2 * x1]
rp = lambda: sum(sp.Rational(random.randint(-4, 4), random.randint(1, 3)) * m for m in mon)
Ssym = sum(sp.Rational(random.randint(-4, 4), 2) * m * (1 + random.randint(-2, 2) * t + random.randint(-2, 2) * t**2)
           for m in [x1, x2, x1 * x2, x1**2, x2**2, x1**3, x1 * x2**2, x2**4])
lsym = rp() + t * rp()
g = sp.Matrix([rp(), rp()])
Sx = sp.Matrix([sp.diff(Ssym, x1), sp.diff(Ssym, x2)])
rr = lsym + sp.diff(Ssym, t) + (Sx.T * g)[0]
p1, p2 = sp.symbols("p1 p2")
HH = sp.hessian(lsym + p1 * g[0] + p2 * g[1], Z).subs({p1: Sx[0], p2: Sx[1]})
Pm = sp.hessian(Ssym, [x1, x2])
Pdot_m = Pm.diff(t) + Pm.diff(x1) * g[0] + Pm.diff(x2) * g[1]
xiv, etv = sp.Matrix([xi1, xi2]), sp.Matrix([et1, et2])
xidot = g.jacobian([x1, x2]) * xiv + g.jacobian([u1, u2]) * etv
zeta = sp.Matrix([xi1, xi2, et1, et2])
lhs = (zeta.T * sp.hessian(rr, Z) * zeta)[0]
rhs = (zeta.T * HH * zeta)[0] + (xiv.T * Pdot_m * xiv)[0] + 2 * (xiv.T * Pm * xidot)[0]
out["A4"] = {"identity_n2_m2_time_dependent_l": sp.expand(lhs - rhs) == 0}
print("A4", out["A4"])

# ------------------------------------------------------------------ B
T, X0, UMAX = 1.0, 1.0, 5.0


def P_closed(case, tt):
    if case == 1:  # alpha = -2, q = 0, phiT = 1: 1/P = -1/4 + (5/4) e^{4(T-t)}
        return 1.0 / (-0.25 + 1.25 * np.exp(4.0 * (T - tt)))
    # alpha = 1, q = 1, phiT = 0: P = 1 - sqrt2 tanh(sqrt2 (t - c)), P(T) = 0
    c = T - np.arctanh(1 / np.sqrt(2)) / np.sqrt(2)
    return 1.0 - np.sqrt(2) * np.tanh(np.sqrt(2) * (tt - c))


CASES = {1: (-2.0, 0.0, 1.0), 2: (1.0, 1.0, 0.0)}
for cs, (a_, q_, _) in CASES.items():  # closed forms solve the Riccati equation
    tt = np.linspace(0, T, 2001)
    Pv = P_closed(cs, tt)
    dP = np.gradient(Pv, tt, edge_order=2)
    assert np.max(np.abs(dP - (Pv**2 - 2 * a_ * Pv - q_))[5:-5]) < 1e-5, cs


def exact_tilted(cs, N, eps_, lam_):
    alpha, qq, _ = CASES[cs]
    hh = T / N
    tt = hh * np.arange(N + 1)
    s_ = P_closed(cs, tt) - 2 * eps_ * np.exp(-lam_ * tt)
    A = 1 + alpha * hh
    Fv = hh * qq + A * A * s_[2:] / (1 + hh * s_[2:])  # stages t = 1..N-1 use s_{t+1}
    return bool(np.all(Fv - s_[1:-1] >= -1e-15 * np.maximum(1.0, np.abs(s_[1:-1]))))


def threshold(cs, eps_, lam_, Nmax=400000):
    Ns = np.unique(np.round(np.geomspace(4, Nmax, 220)).astype(int))
    ok = [exact_tilted(cs, int(N), eps_, lam_) for N in Ns]
    bad = [int(N) for N, o in zip(Ns, ok) if not o]
    if not bad:
        return None, True
    lo = max(bad)
    later = [int(N) for N, o in zip(Ns, ok) if o and N > lo]
    if not later:
        return lo, False
    hi = min(later)
    monotone = all(o for N, o in zip(Ns, ok) if N > lo)
    while hi - lo > 1:  # bisection inside the bracket (assumes monotonicity there)
        mid = (lo + hi) // 2
        if exact_tilted(cs, mid, eps_, lam_):
            hi = mid
        else:
            lo = mid
    return lo, monotone


rowsB = []
for cs, lams in ((1, (1.0, 2.0, 4.0, 8.0)), (2, (4.0, 6.0, 8.0))):
    alpha, qq, _ = CASES[cs]
    PT = float(P_closed(cs, np.array([T]))[0])
    for lam_ in lams:
        for eps_ in (0.5, 0.1, 0.02):
            eT = eps_ * np.exp(-lam_ * T)
            Nbad, mono = threshold(cs, eps_, lam_)
            pred = 4 * eT * (lam_ / 2 - alpha + PT - eT) / abs((PT - alpha) * (alpha * PT + qq))
            rec = {"case": cs, "alpha": alpha, "q": qq, "lam": lam_, "eps": eps_,
                   "last_inexact_N": Nbad, "grid_monotone_above": mono,
                   "h0": (T / Nbad) if Nbad else None,
                   "h0_over_epsexp": (T / Nbad / eT) if Nbad else None,
                   "leading_order_h0_over_epsexp": pred / eT,
                   "h0_over_leading_order": (T / Nbad / pred) if Nbad else None}
            rowsB.append(rec)
            print("B", json.dumps(rec))
out["B"] = rowsB

# ------------------------------------------------------------------ C
def lq_kkt(alpha, qq, phiT, N):
    hh = T / N
    A = 1 + hh * alpha
    Pd = np.empty(N + 1)
    Pd[N] = phiT
    for k in range(N - 1, -1, -1):
        Pd[k] = hh * qq + A * A * Pd[k + 1] / (1 + hh * Pd[k + 1])
    xk = np.empty(N + 1)
    uk = np.empty(N)
    xk[0] = X0
    for k in range(N):
        uk[k] = -A * Pd[k + 1] / (1 + hh * Pd[k + 1]) * xk[k]
        xk[k + 1] = A * xk[k] + hh * uk[k]
    lo, hi = np.empty(N + 1), np.empty(N + 1)
    lo[0] = hi[0] = X0
    for k in range(N):
        lo[k + 1] = min(A * lo[k], A * hi[k]) - hh * UMAX
        hi[k + 1] = max(A * lo[k], A * hi[k]) + hh * UMAX
    assert np.max(np.abs(uk)) < UMAX
    return hh, A, xk, uk, Pd * xk, lo, hi


def stage_min(Hyy, Hyv, Hvv, gy, gv, ylo, yhi):
    """min over [ylo,yhi] x [-UMAX,UMAX] of 0.5(Hyy y^2 + 2Hyv y v + Hvv v^2) + gy y + gv v,
    with Hvv > 0: minimize over v by clipping, then over y on each piece."""
    f = lambda y, v: 0.5 * (Hyy * y * y + 2 * Hyv * y * v + Hvv * v * v) + gy * y + gv * v
    vstar = lambda y: np.clip(-(Hyv * y + gv) / Hvv, -UMAX, UMAX)
    cand = [ylo, yhi]
    if Hyv != 0:  # breakpoints where the unclipped v* hits +-UMAX
        cand += [(-Hvv * vb - gv) / Hyv for vb in (-UMAX, UMAX)]
    schur = Hyy - Hyv * Hyv / Hvv  # interior piece: m(y) = 0.5 schur y^2 + (gy - Hyv gv/Hvv) y + c
    if schur > 0:
        cand.append(-(gy - Hyv * gv / Hvv) / schur)
    if Hyy > 0:  # clipped pieces
        cand += [-(gy + Hyv * vb) / Hyy for vb in (-UMAX, UMAX)]
    ys = np.array([c for c in cand if ylo <= c <= yhi])
    return float(np.min(f(ys, vstar(ys))))


def lq_family_gap(N, kind):
    alpha, qq, phiT = CASES[1]
    hh, A, xk, uk, pk, lo, hi = lq_kkt(alpha, qq, phiT, N)
    tt = hh * np.arange(N + 1)
    s2 = P_closed(1, tt)
    s1 = pk - s2 * xk if kind == "transferred" else np.zeros(N + 1)
    gap = 0.0
    for k in range(N):
        Hyy = hh * qq + s2[k + 1] * A * A - s2[k]
        Hyv = s2[k + 1] * A * hh
        Hvv = hh + s2[k + 1] * hh * hh
        gy = s1[k + 1] * A - s1[k]
        gv = s1[k + 1] * hh
        f = lambda y, v: 0.5 * (Hyy * y * y + 2 * Hyv * y * v + Hvv * v * v) + gy * y + gv * v
        at = f(xk[k], uk[k])
        if k == 0:  # x_0 fixed: minimize over v only
            m = f(X0, float(np.clip(-(Hyv * X0 + gv) / Hvv, -UMAX, UMAX)))
        else:
            m = stage_min(Hyy, Hyv, Hvv, gy, gv, lo[k], hi[k])
        gap += at - min(m, at)
    # terminal residual Phi - S_N = (phiT - s2_N) y^2/2 - s1_N y with phiT = P(T): linear
    cN, bN = phiT - s2[N], s1[N]
    fN = lambda y: 0.5 * cN * y * y - bN * y
    gap += fN(xk[N]) - min(fN(lo[N]), fN(hi[N]), fN(xk[N]))
    return gap


rowsC = []
for N in (10, 20, 40, 80, 160, 320, 640):
    gu = lq_family_gap(N, "uncorrected")
    gt = lq_family_gap(N, "transferred")
    rec = {"N": N, "uncorrected_field_gap": gu, "uncorrected_gap_over_h": gu * N,
           "transferred_field_gap": gt}
    rowsC.append(rec)
    print("C", json.dumps(rec))
out["C"] = rowsC

# ------------------------------------------------------------------ D
own = {r_["N"]: r_ for r_ in json.load(open(os.path.join(HERE, "logs", "revision_checks.json")))["B"]}
rev = {r_["N"]: r_ for r_ in json.load(open(os.path.join(
    ROOT, "reviews", "calibration-review-checks", "logs", "c2_transfer_theorem.json")))["B"]}
rch = {r_["N"]: r_ for r_ in json.load(open(os.path.join(
    ROOT, "reviews", "calibration-recheck-checks", "logs", "r3_check53.json")))}
rowsD = []
for N in (10, 20, 40, 80):
    rec = {"N": N}
    for fam, kr, kc in (("transferred", "transferred", "gap_transferred"),
                        ("uncorrected", "sampled_no_correction", "gap_uncorrected"),
                        ("costate", "costate_affine", "gap_costate")):
        a_ = own[N][fam + "_gap"]
        b_ = rev[N]["families"][kr]["gap"]
        c_ = rch[N][kc]
        rec[fam] = {"author_minus_review": a_ - b_, "author_minus_recheck": a_ - c_,
                    "review_minus_recheck": b_ - c_}
    rowsD.append(rec)
    print("D", json.dumps(rec))
out["D"] = rowsD

out["runtime_s"] = time.time() - t_start
with open(os.path.join(HERE, "logs", "recheck_revision_checks.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("runtime_s", out["runtime_s"])
