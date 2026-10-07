"""Rigorous two-sided bounds for MINLPLib instances that are sums of weighted Euclidean
norms of affine functions (the emfl* facility-location instances).

Structure (asserted from the OSIL file, nothing assumed):
  * cone rows    t_k^2 - sum_{w in W_k} w^2 >= 0   (lb 0, ub INF, quadratic terms only),
                 t_k has lower bound 0, so the row is t_k >= ||w_k||;
  * every w occurs in exactly one cone row and in exactly one equality row, with
    coefficient +-1, whose other variables are "base" variables (in no cone row);
  * every other row is an equality over base variables and w's handled above, or a
    singleton equality fixing a w;
  * objective  sum_k c_k t_k  with c_k >= 0; t_k occurs nowhere else.
Then w = a_w . x + e_w (exact rationals) and the problem is  min_x sum_k c_k ||A_k x + e_k||.

Upper bound: any base point x (the listed point's base values, or a numerical optimum);
  w exact, t_k := sqrt(sum w^2) rounded up to a rational with t_k^2 >= sum w^2 checked
  exactly. This is an exactly feasible point; its objective is an exact rational.
Base variables are free or >= 0.
Lower bound (weak duality): for y_k with ||y_k|| <= c_k and sum_k A_k^T y_k = 0,
  sum_k c_k t_k >= sum_k c_k ||w_k|| >= sum_k y_k . w_k = sum_k y_k . e_k.
  y comes from a numerical solve of the dual SOCP; it is corrected exactly (rational
  least-norm correction) so that sum_k A_k^T y_k = 0 holds exactly, then scaled by a
  rational s <= 1 so that every ||y_k|| <= c_k holds; both are checked exactly.

Usage: python3 cert_socp.py <instance> [<point tag> ...]
"""
import json
import math
import os
import sys
from fractions import Fraction

import cvxpy as cp
import numpy as np

import audit_eval as A
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))


def structure(m):
    names = m["names"]
    cones, cone_of = [], {}
    for r, row in enumerate(m["cons"]):
        if row["quad"] and not row["lin"] and row["nl"] is None:
            assert row["lb"] == "0" and row["ub"] == "INF" and row["constant"] == "0", row["name"]
            pos = [a for a, b, c in row["quad"] if Fraction(c) > 0]
            neg = [a for a, b, c in row["quad"] if Fraction(c) < 0]
            assert all(a == b for a, b, c in row["quad"])
            assert len(pos) == 1 and all(Fraction(c) in (1, -1) for a, b, c in row["quad"]), row["name"]
            t = pos[0]
            assert Fraction(m["lb"][t]) == 0
            cones.append((r, t, neg))
            for w in neg:
                assert w not in cone_of
                cone_of[w] = len(cones) - 1
    tvars = {t for _, t, _ in cones}
    o = m["obj"]
    assert o["nl"] is None and not o["quad"] and Fraction(o["constant"]) == 0 and o["sense"] == "min"
    assert set(o["lin"]) <= tvars and all(Fraction(c) >= 0 for c in o["lin"].values())
    wvars = set(cone_of)
    base = sorted(set(range(len(names))) - wvars - tvars)
    defs = {}  # w -> (dict base->coef, const) with w = sum coef*x + const
    const_w = {}
    for r, row in enumerate(m["cons"]):
        if row in [m["cons"][c[0]] for c in []]:
            pass
        if any(r == c[0] for c in cones):
            continue
        assert row["lb"] == row["ub"] and not row["quad"] and row["nl"] is None, row["name"]
        ws = [j for j in row["lin"] if j in wvars]
        assert not (set(row["lin"]) & tvars)
        assert len(ws) == 1, (row["name"], ws)
        w = ws[0]
        cw = Fraction(row["lin"][w])
        assert cw in (1, -1) and w not in defs
        rhs = Fraction(row["lb"]) - Fraction(row["constant"])
        defs[w] = ({j: -Fraction(c) / cw for j, c in row["lin"].items() if j != w}, rhs / cw)
    assert set(defs) == wvars, (len(defs), len(wvars))
    for w, (a, e) in defs.items():
        assert set(a) <= set(base)
    for j in base:  # free or nonnegative base variables (G y = 0 is dual feasible for both)
        assert m["lb"][j] in ("-INF", "0") and m["ub"][j] == "INF", names[j]
    for w in wvars:
        assert m["lb"][w] == "-INF" and m["ub"][w] == "INF"
    c = {t: Fraction(o["lin"].get(t, "0")) for _, t, _ in cones}
    return cones, defs, base, c


def sqrt_up(q, digits=40):
    """rational s >= sqrt(q) (q >= 0 rational), close to it"""
    if q == 0:
        return Fraction(0)
    s = Fraction(math.isqrt(q.numerator * 10 ** (2 * digits) // q.denominator) + 1, 10 ** digits)
    while s * s < q:
        s += Fraction(1, 10 ** digits)
    return s


def primal_value(m, S, xb):
    """exactly feasible completion of base values xb (dict j->Fraction); exact objective"""
    cones, defs, base, c = S
    val = Fraction(0)
    full = dict(xb)
    for r, t, ws in cones:
        q = Fraction(0)
        for w in ws:
            a, e = defs[w]
            full[w] = sum((coef * xb[j] for j, coef in a.items()), Fraction(0)) + e
            q += full[w] ** 2
        full[t] = sqrt_up(q)
        assert full[t] ** 2 >= q and full[t] >= 0
        val += c[t] * full[t]
    return val, full


def check_full_point(m, full):
    """independent exact check of all rows and bounds of the OSIL model at `full`"""
    x = [full[j] for j in range(len(m["names"]))]
    for row in m["cons"]:
        v = V.row_frac(row, x)
        assert V.row_ok_frac(row, v), row["name"]
    for j in range(len(x)):
        if m["lb"][j] != "-INF":
            assert x[j] >= Fraction(m["lb"][j])
        if m["ub"][j] != "INF":
            assert x[j] <= Fraction(m["ub"][j])
    return True


def solve_numeric(S):
    cones, defs, base, c = S
    bi = {j: k for k, j in enumerate(base)}
    x = cp.Variable(len(base))
    terms, cons_list = [], []
    for r, t, ws in cones:
        Ak = np.zeros((len(ws), len(base)))
        ek = np.zeros(len(ws))
        for i, w in enumerate(ws):
            a, e = defs[w]
            for j, coef in a.items():
                Ak[i, bi[j]] = float(coef)
            ek[i] = float(e)
        terms.append(float(c[t]) * cp.norm(Ak @ x + ek, 2))
    prob = cp.Problem(cp.Minimize(sum(terms)))
    prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10, max_iter=500)
    return x.value, prob.value


def dual_bound(S, xstar, eps=Fraction(1, 10 ** 9)):
    cones, defs, base, c = S
    bi = {j: k for k, j in enumerate(base)}
    # numerical multipliers from the dual SOCP: max sum y.e  s.t. ||y_k|| <= c_k, G y = 0
    keys = [(k, w) for k, (r, t, ws) in enumerate(cones) for w in ws]
    kpos = {kk: i for i, kk in enumerate(keys)}
    G = np.zeros((len(base), len(keys)))
    evec = np.zeros(len(keys))
    for col, (k, w) in enumerate(keys):
        for j, coef in defs[w][0].items():
            G[bi[j], col] = float(coef)
        evec[col] = float(defs[w][1])
    yv = cp.Variable(len(keys))
    cons = [G @ yv == 0]
    for k, (r, t, ws) in enumerate(cones):
        cons.append(cp.norm(yv[[kpos[(k, w)] for w in ws]], 2) <= float(c[t]))
    dprob = cp.Problem(cp.Maximize(evec @ yv), cons)
    dprob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10, max_iter=500)
    y = {kk: float(yv.value[i]) for i, kk in enumerate(keys)}
    # exact: least-norm rational correction to G y = 0, then scale y by s <= 1 so that every
    # ||s y_k|| <= c_k (scaling keeps G y = 0)
    Y = {kk: Fraction(y[kk]).limit_denominator(10 ** 16) for kk in keys}
    zero = {k for k, (r, t, ws) in enumerate(cones) if c[t] == 0}
    for kk in keys:
        if kk[0] in zero:
            Y[kk] = Fraction(0)  # ||y_k|| <= 0 forces y_k = 0
    Gf = {}
    for col, (k, w) in enumerate(keys):
        if k in zero:
            continue
        for j, coef in defs[w][0].items():
            Gf.setdefault(bi[j], {})[col] = coef
    nb = len(base)
    res = [sum((Gf.get(i, {}).get(col, 0) * Y[keys[col]] for col in Gf.get(i, {})), Fraction(0)) for i in range(nb)]
    M = [[sum((Gf.get(i, {}).get(col, 0) * Gf.get(l, {}).get(col, 0) for col in Gf.get(i, {})), Fraction(0))
          for l in range(nb)] for i in range(nb)]
    z = solve_exact(M, res)
    for col, kk in enumerate(keys):
        d = sum((Gf.get(i, {}).get(col, 0) * z[i] for i in range(nb)), Fraction(0))
        Y[kk] -= d
    for i in range(nb):
        assert sum((Gf.get(i, {}).get(col, 0) * Y[keys[col]] for col in Gf.get(i, {})), Fraction(0)) == 0
    rho = Fraction(0)
    for k, (r, t, ws) in enumerate(cones):
        q = sum((Y[(k, w)] ** 2 for w in ws), Fraction(0))
        if q == 0:
            continue
        assert c[t] > 0, "multiplier on a zero-weight cone"
        rho = max(rho, q / c[t] ** 2)
    scale = Fraction(1) if rho <= 1 else 1 / sqrt_up(rho, 30)
    for kk in keys:
        Y[kk] *= scale
    for k, (r, t, ws) in enumerate(cones):  # exact final check
        assert sum((Y[(k, w)] ** 2 for w in ws), Fraction(0)) <= c[t] ** 2
    lb = sum((Y[(k, w)] * defs[w][1] for k, (r, t, ws) in enumerate(cones) for w in ws), Fraction(0))
    return lb, float(rho)


def solve_exact(M, b):
    n = len(b)
    Aug = [row[:] + [b[i]] for i, row in enumerate(M)]
    rank_rows = []
    r = 0
    piv_cols = []
    for col in range(n):
        p = next((i for i in range(r, n) if Aug[i][col] != 0), None)
        if p is None:
            continue
        Aug[r], Aug[p] = Aug[p], Aug[r]
        pv = Aug[r][col]
        Aug[r] = [v / pv for v in Aug[r]]
        for i in range(n):
            if i != r and Aug[i][col] != 0:
                f = Aug[i][col]
                Aug[i] = [a - f * bb for a, bb in zip(Aug[i], Aug[r])]
        piv_cols.append(col)
        r += 1
    for i in range(r, n):
        assert Aug[i][n] == 0, "inconsistent stationarity system"
    z = [Fraction(0)] * n
    for i, col in enumerate(piv_cols):
        z[col] = Aug[i][n]
    return z


def main(name, tags):
    m = A.load(name)
    S = structure(m)
    cones, defs, base, c = S
    out = dict(name=name, n_cones=len(cones), n_base=len(base))
    xs, val = solve_numeric(S)
    out["numerical_optimum"] = val
    lb, worst = dual_bound(S, xs)
    out["rigorous_lower_bound"] = str(float(lb))
    out["lower_bound_30_digits_rounded_down"] = str((lb.numerator * 10 ** 30) // lb.denominator) + "e-30"
    out["max_norm_ratio_sq"] = worst
    xb = {j: Fraction(float(xs[k])) if m["lb"][j] == "-INF" else max(Fraction(0), Fraction(float(xs[k])))
          for k, j in enumerate(base)}
    ub, full = primal_value(m, S, xb)
    check_full_point(m, full)
    out["rigorous_upper_bound_from_numerical_optimum"] = str(float(ub))
    out["gap"] = float(ub - lb)
    for tag in tags:
        vals = A.read_sol(os.path.join(HERE, "sol", tag + ".sol"))
        xb = {j: Fraction(vals.get(m["names"][j], "0")) for j in base}
        v, full = primal_value(m, S, xb)
        check_full_point(m, full)
        out["repaired_" + tag] = str(float(v))
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, "logs", f"cert_socp_{name}.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
