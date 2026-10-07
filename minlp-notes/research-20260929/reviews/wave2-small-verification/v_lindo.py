"""Rigorous existence of exactly feasible points below LINDO's listed dual
bounds (methanol50, rocket100/200/400), by a Krawczyk test (krawczyk.py).

methanol50: kinetic parameters x1502..x1506 fixed at MINLPLib p4's decimals;
  the 3 fixed initial values stay fixed; the other 1497 variables (all free,
  no bounds) solve the 1497 equality rows.  Start: MINLPLib p4 states, own
  double Newton polish.
rocketN: thrust T fixed at the authors' CONOPT values (their polished file).
  Then the mass rows are linear in (step, m): step and m_1..m_{N-1} are computed
  in exact rational arithmetic (all mass rows hold exactly, bounds checked
  exactly).  D_0 = 0 and g_0 = 1 are exact (v_0 = 0, h_0 = 1).  The 4N
  unknowns v_1..N, h_1..N, g_1..N, D_1..N solve the 4N remaining rows.
  Start: the authors' polished states, own double Newton polish.
After the test: bounds of all unknowns are checked on the whole box X, and the
objective (with its constant) is enclosed over X.
"""
import json
import os
import sys
import time
from fractions import Fraction

import mpmath
import numpy as np
from mpmath import iv

import common
import krawczyk

AUTH = os.path.join(common.HERE, "..", "..", "open-instances-wave2", "small")
LINDO = {"methanol50": "0.00802826", "rocket100": "-1.0128319", "rocket200": "-1.01283563", "rocket400": "-1.01283634"}


def read_named(path):
    d = {}
    for line in open(path):
        p = line.split()
        if len(p) == 2:
            d[p[0]] = p[1]
    return d


def setup_methanol(m):
    names = m["names"]
    sol = common.read_sol(os.path.join(common.HERE, "sol", "methanol50.p4.sol"))
    params = [names.index("x%d" % k) for k in range(1502, 1507)]
    fixed = {}
    for j in range(len(names)):
        if m["lb"][j] == m["ub"][j]:
            fixed[j] = m["lb"][j]
    for j in params:
        fixed[j] = sol[names[j]]
        assert Fraction(sol[names[j]]) >= Fraction(m["lb"][j])
    U = [j for j in range(len(names)) if j not in fixed]
    rows = list(range(len(m["cons"])))
    x0 = np.array([float(sol.get(names[j], "0")) for j in U])
    info = dict(params={names[j]: fixed[j] for j in params}, fixed_initial={names[j]: fixed[j] for j in fixed if j not in params})
    # compare with the authors' held parameter values
    auth = read_named(os.path.join(AUTH, "logs", "methanol50.p4.polished.txt"))
    info["params_equal_authors"] = all(Fraction(auth[names[j]]) == Fraction(fixed[j]) for j in params)
    return fixed, U, rows, x0, info


def setup_rocket(m, N):
    names = m["names"]
    step = 0
    v = list(range(1, N + 2)); h = list(range(N + 2, 2 * N + 3)); g = list(range(2 * N + 3, 3 * N + 4))
    ms = list(range(3 * N + 4, 4 * N + 5)); T = list(range(4 * N + 5, 5 * N + 6)); D = list(range(5 * N + 6, 6 * N + 7))
    assert len(names) == 6 * N + 7
    assert (m["lb"][v[0]], m["ub"][v[0]]) == ("0", "0") and (m["lb"][h[0]], m["ub"][h[0]]) == ("1", "1")
    assert (m["lb"][ms[0]], m["ub"][ms[0]]) == ("1", "1") and (m["lb"][ms[-1]], m["ub"][ms[-1]]) == (".6", ".6")
    assert all((m["lb"][j], m["ub"][j]) == ("0", "3.5") for j in T)
    assert all((m["lb"][j], m["ub"][j]) == (".6", "1") for j in ms[1:-1])
    assert all(m["lb"][j] == "1" and m["ub"][j] == "INF" for j in h[1:])
    assert all(m["lb"][j] == "0" and m["ub"][j] == "INF" for j in v[1:] + g + D + [step])
    o = m["obj"]
    assert o["lin"] == {h[-1]: "-1"} and o["constant"] == "0" and o["nl"] is None and not o["quad"]
    auth = read_named(os.path.join(AUTH, "logs", "rocket%d.conopt.polished.txt" % N))
    Tv = [Fraction(auth[names[j]]) for j in T]
    assert all(0 <= t <= Fraction("3.5") for t in Tv)
    # mass rows: {m_i: -1, m_{i+1}: 1}, quad [(step, T_i, c), (step, T_{i+1}, c)]
    massrows = []
    for r, row in enumerate(m["cons"]):
        vs = set(row["lin"]) | {a for q in row["quad"] for a in q[:2]}
        if vs and vs <= set(ms) | set(T) | {step}:
            massrows.append(r)
    assert len(massrows) == N
    coef = None
    S = [Fraction(0)]
    for i in range(N):
        row = [m["cons"][r] for r in massrows if m["cons"][r]["lin"] == {ms[i]: "-1", ms[i + 1]: "1"}]
        assert len(row) == 1
        row = row[0]
        assert row["nl"] is None and row["lb"] == row["ub"] == "0" and row["constant"] == "0"
        qd = sorted((a, b, c) for a, b, c in row["quad"])
        assert [(a, b) for a, b, _ in qd] == [(step, T[i]), (step, T[i + 1])] and qd[0][2] == qd[1][2]
        c = Fraction(qd[0][2])
        S.append(S[-1] + c * (Tv[i] + Tv[i + 1]))
    stepv = (Fraction(1) - Fraction("0.6")) / S[-1]
    mv = [Fraction(1) - stepv * S[i] for i in range(N + 1)]
    assert mv[-1] == Fraction("0.6") and stepv > 0
    assert all(Fraction("0.6") <= x <= 1 for x in mv)
    fixed = {step: stepv}
    for i in range(N + 1):
        fixed[ms[i]] = mv[i]
        fixed[T[i]] = Tv[i]
    fixed[v[0]] = Fraction(0); fixed[h[0]] = Fraction(1); fixed[D[0]] = Fraction(0); fixed[g[0]] = Fraction(1)
    # exact checks of the removed rows: mass rows, D_0 row, g_0 row
    xs = {j: val for j, val in fixed.items()}
    for r in massrows:
        row = m["cons"][r]
        val = sum(Fraction(c) * xs[j] for j, c in row["lin"].items()) + sum(Fraction(c) * xs[a] * xs[b] for a, b, c in row["quad"])
        assert val == 0
    fixrows = []
    for r, row in enumerate(m["cons"]):
        vs = common_vars(row)
        if vs <= set(fixed) and r not in massrows:
            fixrows.append(r)
            xI = [None] * len(names)
            for j in vs:
                xI[j] = krawczyk.fixed_iv(fixed[j])
            val = common.row_value(m, r, xI, common.ivnum, common.IVFNS)
            assert val.a == 0 and val.b == 0, (row["name"], val)
    assert len(fixrows) == 2
    U = v[1:] + h[1:] + g[1:] + D[1:]
    rows = [r for r in range(len(m["cons"])) if r not in massrows and r not in fixrows]
    assert len(rows) == len(U) == 4 * N
    x0 = np.array([float(Fraction(auth[names[j]])) for j in U])
    info = dict(step=str(float(stepv)), T_source="authors' polished CONOPT file (held thrust)",
                n_T_at_bounds=sum(1 for t in Tv if t in (0, Fraction("3.5"))),
                min_mass=str(float(min(mv))), removed_rows_exact=len(massrows) + 2)
    return fixed, U, rows, x0, info


def common_vars(row):
    vs = set(row["lin"]) | {a for q in row["quad"] for a in q[:2]}
    if row["nl"] is not None:
        stack = [row["nl"]]
        while stack:
            t = stack.pop()
            if t[0] == "var":
                vs.add(t[1])
            elif t[0] != "num":
                stack.extend(t[1:])
    return vs


def main(name, rho):
    t0 = time.time()
    mpmath.mp.prec = 300  # exact copies of interval endpoints in comparisons below
    m = common.load(name)
    if name == "methanol50":
        fixed, U, rows, x0, info = setup_methanol(m)
    else:
        fixed, U, rows, x0, info = setup_rocket(m, int(name[6:]))
    iv.dps = 40
    xt, res = krawczyk.newton_polish(m, rows, U, x0, fixed, iters=3)
    r = rho * np.maximum(1.0, np.abs(xt))
    kt, X_iv = krawczyk.test(m, rows, U, xt, r, fixed)
    out = dict(name=name, n=len(U), info=info, polish_residual=res, rho=rho, krawczyk=kt)
    # bounds over X and objective enclosure
    names = m["names"]
    bad = []
    minmargin = mpmath.inf
    for k, j in enumerate(U):
        lb, ub = m["lb"][j], m["ub"][j]
        if lb != "-INF":
            mg = mpmath.mpf((X_iv[k] - iv.mpf(lb)).a)
            if mg < minmargin:
                minmargin, argmg = mg, names[j]
            if mg < 0:
                bad.append(names[j])
        if ub != "INF" and mpmath.mpf((iv.mpf(ub) - X_iv[k]).a) < 0:
            bad.append(names[j])
    out["bounds_ok_on_X"] = not bad
    out["bound_violations"] = bad[:10]
    out["min_lower_bound_margin_on_X"] = [mpmath.nstr(minmargin, 4), argmg if minmargin < mpmath.inf else None]
    xI = [None] * len(names)
    for j, v in fixed.items():
        xI[j] = krawczyk.fixed_iv(v)
    for k, j in enumerate(U):
        xI[j] = X_iv[k]
    fobj = common.obj_value(m, xI, common.ivnum, common.IVFNS)
    out["objective_enclosure"] = [mpmath.nstr(mpmath.mpf(fobj.a), 17), mpmath.nstr(mpmath.mpf(fobj.b), 17)]
    out["objective_constant"] = m["obj"]["constant"]
    out["lindo_listed_dual"] = LINDO[name]
    out["below_lindo_rigorously"] = bool(mpmath.mpf(fobj.b) < mpmath.mpf(LINDO[name])) and kt["ok"] and not bad
    out["margin_to_lindo"] = mpmath.nstr(mpmath.mpf(LINDO[name]) - mpmath.mpf(fobj.b), 6)
    out["sec"] = round(time.time() - t0, 1)
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(common.HERE, "logs", "krawczyk_%s.json" % name), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 1e-9)
