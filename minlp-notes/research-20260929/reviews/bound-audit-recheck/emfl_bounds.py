"""Two-sided exact bounds on the optimum of an emfl instance (own code for this recheck).

Structure (asserted from the OSIL file by `structure`):
  min sum_k c_k t_k                       c_k >= 0, no constant, no other objective terms
  cone rows   t_k^2 - sum_{w in W_k} w^2 >= 0,   t_k >= 0
  each w is free and appears in exactly one equality row, whose other variables are base
  variables z; so w = a_w . z + e_w with rational a_w, e_w
  base variables z >= 0, no upper bound.

Upper bound. Any rational z >= 0 gives w exactly; t_k := a rational upper bound of |w_k|
(integer square root, 2^-200 resolution) makes every cone row hold. The full OSIL model is then
checked in exact arithmetic (every row, every bound) and the objective is evaluated exactly.

Lower bound (weak duality). For y_k with |y_k| <= c_k and g = sum_k A_k^T y_k >= 0,
every feasible point satisfies
  sum_k c_k t_k >= sum_k c_k |w_k| >= sum_k y_k . w_k = g . z + sum_k y_k . e_k >= sum_k y_k . e_k.
y comes from solving this dual problem (max sum y.e s.t. |y_k| <= c_k(1 - eta), g >= 0) numerically
with Clarabel. The float solution is converted to exact rationals and then repaired exactly:
  1. each y_k is scaled into the ball of radius c_k (1 - eta) if needed;
  2. each negative g_j is set to 0 by changing one component of one cone whose row of A_k has a
     single nonzero, in column j (the cone with the largest norm slack is used);
  3. a final global scale s <= 1 enforces |y_k| <= c_k if step 2 used up the slack
     (scaling keeps g >= 0).
Both dual conditions and the value sum y.e are then checked/evaluated exactly.
Only the conclusions of steps 'exact check' are relied on; Clarabel is a heuristic here.

Usage: python3 emfl_bounds.py name [label=value ...]
"""
import os
import sys
import time
from fractions import Fraction as F
from math import isqrt

import cvxpy as cp
import numpy as np
import scipy.sparse as sp

import qosil
from sssd_exact import fmt

HERE = os.path.dirname(os.path.abspath(__file__))


def sqrt_up(q, bits=200):
    """Rational r >= sqrt(q) with r - sqrt(q) <= 2^-bits / denominator scale (q >= 0 Fraction)."""
    n, d = q.numerator, q.denominator
    v = (n * d) << (2 * bits)
    r = isqrt(v)
    if r * r < v:
        r += 1
    return F(r, d << bits)  # sqrt(n/d) = sqrt(n d)/d


def structure(M):
    assert M.sense == "min" and M.obj_const == 0 and not M.obj_Q
    cones = []  # (row, t, [w...])
    for i in range(M.m):
        if not M.Q[i]:
            continue
        assert not M.A[i] and M.cconst[i] == 0 and M.clb[i] == 0 and M.cub[i] is None
        assert all(a == b for a, b, c in M.Q[i])
        pos = [a for a, b, c in M.Q[i] if c == 1]
        neg = [a for a, b, c in M.Q[i] if c == -1]
        assert len(pos) == 1 and len(pos) + len(neg) == len(M.Q[i]) and len(set(neg)) == len(neg)
        cones.append((i, pos[0], neg))
    T = [t for _, t, _ in cones]
    assert len(set(T)) == len(T)
    Tset = set(T)
    W = {w for _, _, ws in cones for w in ws}
    assert not (W & Tset)
    assert all(M.lb[t] == 0 and M.ub[t] is None and M.type[t] == "C" for t in T)
    assert set(M.obj_lin) <= Tset and all(c >= 0 for c in M.obj_lin.values())
    base = sorted(set(range(M.n)) - Tset - W)
    assert all(M.lb[j] == 0 and M.ub[j] is None and M.type[j] == "C" for j in base)
    assert all(M.lb[w] is None and M.ub[w] is None and M.type[w] == "C" for w in W)
    bset = set(base)
    defn = {}
    for i in range(M.m):
        if M.Q[i]:
            continue
        assert M.clb[i] is not None and M.clb[i] == M.cub[i]
        ws = [j for j in M.A[i] if j in W]
        assert len(ws) == 1 and set(M.A[i]) - {ws[0]} <= bset, M.cname[i]
        w = ws[0]
        assert w not in defn
        a = M.A[i][w]
        defn[w] = ({j: -v / a for j, v in M.A[i].items() if j != w}, (M.cub[i] - M.cconst[i]) / a)
    assert set(defn) == W
    return cones, base, defn


def repair(yf, act, groups, Ar, E, c, nb, eta):
    """Exact repair of a float dual vector; returns (exact lower bound, diagnostics)."""
    Y = [F(float(v)) for v in yf]
    r = len(Y)
    val0 = sum((Y[p] * E[p] for p in range(r)), F(0))
    shrink = F(1) - eta
    n_proj = 0
    for k in act:
        idx = groups[k]
        nrm = sqrt_up(sum((Y[p] * Y[p] for p in idx), F(0)))
        cap = c[k] * shrink
        if nrm > cap:
            s = cap / nrm
            for p in idx:
                Y[p] *= s
            n_proj += 1
    val1 = sum((Y[p] * E[p] for p in range(r)), F(0))

    def gvec():
        g = [F(0)] * nb
        for p in range(r):
            if Y[p]:
                for j, v in Ar[p].items():
                    g[j] += v * Y[p]
        return g

    g = gvec()
    neg = [j for j in range(nb) if g[j] < 0]
    gmin = min(g)
    for j in neg:
        best = None
        for k in act:
            for p in groups[k]:
                if list(Ar[p]) == [j]:
                    sl = c[k] ** 2 - sum((Y[q] * Y[q] for q in groups[k]), F(0))
                    if best is None or sl > best[0]:
                        best = (sl, p)
        assert best is not None, f"no single-column row for z_{j}"
        p = best[1]
        Y[p] += -g[j] / Ar[p][j]
    g = gvec()
    assert all(v >= 0 for v in g)
    val2 = sum((Y[p] * E[p] for p in range(r)), F(0))
    s = F(1)
    for k in act:
        nrm = sqrt_up(sum((Y[p] * Y[p] for p in groups[k]), F(0)))
        if nrm > c[k]:
            s = min(s, c[k] / nrm)
    if s < 1:
        Y = [s * v for v in Y]
    # exact checks of the certificate
    ok_norm, ok_g, LB = check_cert(Y, act, groups, Ar, E, c, nb)
    assert ok_norm and ok_g, (ok_norm, ok_g)
    info = (f"float value {float(val0):.16g}; {n_proj} cones scaled into radius c_k(1 - eta) (value {float(val1):.16g}); "
            f"{len(neg)} negative g_j fixed, min g before {float(gmin):.3g} (value {float(val2):.16g}); "
            f"global scale 1 - {float(1 - s):.3g}; checked exactly: |y_k| <= c_k, g >= 0")
    return LB, info, Y


def check_cert(Y, act, groups, Ar, E, c, nb):
    """Exact check of a dual certificate: returns (all |y_k| <= c_k, g >= 0, sum y.e)."""
    g = [F(0)] * nb
    for p, yp in enumerate(Y):
        if yp:
            for j, v in Ar[p].items():
                g[j] += v * yp
    ok_g = all(v >= 0 for v in g)
    ok_norm = all(sum((Y[p] * Y[p] for p in groups[k]), F(0)) <= c[k] ** 2 for k in act)
    return ok_norm, ok_g, sum((Y[p] * E[p] for p in range(len(Y))), F(0))


def main(name, checks):
    t0 = time.time()
    M = qosil.Model(os.path.join(HERE, "data", name + ".osil"))
    cones, base, defn = structure(M)
    nb = len(base)
    bidx = {j: k for k, j in enumerate(base)}
    c = [M.obj_lin.get(t, F(0)) for _, t, _ in cones]
    act = [k for k in range(len(cones)) if c[k] > 0]
    print(f"{name}: {M.n} variables, {M.m} rows, {len(cones)} cones ({len(act)} with c_k > 0), {nb} base variables z >= 0")
    # sparse float data for the active cones
    rows, cols, vals, e, owner = [], [], [], [], []
    r = 0
    for k in act:
        for w in cones[k][2]:
            coef, ew = defn[w]
            for j, v in coef.items():
                rows.append(r)
                cols.append(bidx[j])
                vals.append(float(v))
            e.append(float(ew))
            owner.append(k)
            r += 1
    A = sp.csr_matrix((vals, (rows, cols)), shape=(r, nb))
    e = np.array(e)
    # ---------------- numerical primal (heuristic)
    z = cp.Variable(nb, nonneg=True)
    tv = cp.Variable(len(act))
    cons, pos = [], 0
    for q, k in enumerate(act):
        m = len(cones[k][2])
        cons.append(cp.SOC(tv[q], A[pos:pos + m] @ z + e[pos:pos + m]))
        pos += m
    cw = np.array([float(c[k]) for k in act])
    P = cp.Problem(cp.Minimize(cw @ tv), cons)
    P.solve(solver="CLARABEL", tol_gap_abs=1e-13, tol_gap_rel=1e-13, tol_feas=1e-13, max_iter=400)
    print(f"  numerical primal: {P.value!r} ({P.status})")
    # ---------------- upper bound: exactly feasible point
    x = [F(0)] * M.n
    for j, v in zip(base, z.value):
        x[j] = max(F(0), F(float(v)))
    for w, (coef, ew) in defn.items():
        x[w] = ew + sum((v * x[j] for j, v in coef.items()), F(0))
    for _, t, ws in cones:
        x[t] = sqrt_up(sum((x[w] * x[w] for w in ws), F(0)))
    viol = M.violations(x)
    assert not viol, viol[:3]
    UB = M.objective(x)
    print(f"  upper bound: exactly feasible point (all {M.m} rows, {M.n} bounds checked exactly), objective {fmt(UB, 16)}")
    # ---------------- numerical dual (heuristic)
    eta = 1e-11
    y = cp.Variable(r)
    dcons, pos = [], 0
    for q, k in enumerate(act):
        m = len(cones[k][2])
        dcons.append(cp.SOC(cp.Constant(cw[q] * (1 - eta)), y[pos:pos + m]))
        pos += m
    dcons.append(A.T @ y >= 0)
    D = cp.Problem(cp.Maximize(e @ y), dcons)
    D.solve(solver="CLARABEL", tol_gap_abs=1e-13, tol_gap_rel=1e-13, tol_feas=1e-13, max_iter=400)
    print(f"  numerical dual:   {D.value!r} ({D.status})")
    # ---------------- candidate y from the primal solve's cone multipliers (sign fixed by value)
    Yp = []
    for con in cons:
        Yp.extend(-np.ravel(con.dual_value[1]))
    Yp = np.array(Yp)
    if abs(float(e @ Yp) - P.value) > abs(float(-e @ Yp) - P.value):
        Yp = -Yp
    # ---------------- exact data of the active cones
    groups, pos = {}, 0
    for q, k in enumerate(act):
        m = len(cones[k][2])
        groups[k] = list(range(pos, pos + m))
        pos += m
    Ar, E = [], []
    for k in act:
        for w in cones[k][2]:
            Ar.append({bidx[j]: v for j, v in defn[w][0].items()})
            E.append(defn[w][1])
    best = None
    for label, yf in (("dual SOCP solved directly", y.value), ("multipliers of the primal solve", Yp)):
        for eta in (F(1, 10**11), F(1, 10**12), F(1, 10**13), F(1, 10**14)):
            LB, info, Y = repair(yf, act, groups, Ar, E, c, nb, eta)
            print(f"  lower bound from {label}, eta = {float(eta):.0e}: {fmt(LB, 16)}  [{info}]")
            if best is None or LB > best[0]:
                best = (LB, Y)
    LB, Ybest = best
    assert LB <= UB
    print(f"  EXACT OPTIMUM in [{fmt(LB, 13)}, {fmt(UB + F(1, 10**13), 13)}] (outward-rounded), gap {float(UB - LB):.3g}")
    print(f"  time {time.time() - t0:.0f} s")
    for ch in checks:
        lbl, _, val = ch.partition("=")
        v = F(val)
        where = "<= LB (valid as a dual bound; not attainable as an objective value)" if v <= LB else \
            ("in [LB, UB]" if v <= UB else ">= UB")
        print(f"    {lbl} {val}: {where}; LB - value = {float(LB - v):.4g}, UB - value = {float(UB - v):.4g}")
    return LB, UB, dict(Y=Ybest, act=act, groups=groups, Ar=Ar, E=E, c=c, nb=nb)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
