"""Phase 2 (proof): check a stored point file against the OSIL model.

    python3 certify.py <name> [radius]     (default: the radius stored in the point file)

Reads only points/<name>.json and the cached OSIL file.  The point file gives
  - fixed variables: exact rationals p/q;
  - free variables: a decimal centre c (read as an exact rational);
  - the square system S: one (row, side) per free variable; the row must hold
    with equality at that side (side = lb for equality rows).
Proof steps (mpmath iv, outward rounding; all comparisons in exact rationals):
  1. Structure: free and fixed partition the variables, |S| = #free, sides valid.
  2. Krawczyk test on X = [c - r, c + r] (r = radius, 1e-45 in the stored files):
        K = c - C F(c) + (I - C J(X)) (X - c),
     C a float64 approximate inverse of J(c) (exact binary numbers, any C is
     valid), F(c) and J(X) interval enclosures (forward-mode differentiation in
     iv).  K inside the open box X proves a unique x* in X with F(x*) = 0.
  3. Every OSIL row:
       - rows of S hold at x* by step 2;
       - rows whose variables are all fixed and which are linear: exact rational check;
       - all other rows: interval enclosure over X must lie inside [lb, ub].
  4. Objective enclosure over X; rigorous gap to the dual bound (exact rationals).
Assumption: mpmath's iv arithmetic encloses +, -, *, /, sin, cos and decimal
string conversion correctly (outward rounding).
"""
import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np
from mpmath import iv, mp

import pfmodel as pm

HERE = os.path.dirname(os.path.abspath(__file__))
# our rigorous dual bounds (open-instances-summary.md; displayed values are valid bounds)
DUAL = {"powerflow0030p": "576.8934122988004",
        "powerflow0039p": "41869.05148485014",
        "powerflow0039r": "41869.05148327243"}


def fdec(q, digits, up):
    """decimal string of q rounded down (up=False) or up (up=True) at `digits` decimals"""
    s = 10 ** digits
    n = (q * s).__floor__() if not up else (q * s).__ceil__()
    sign = "-" if n < 0 else ""
    n = abs(n)
    return f"{sign}{n // s}.{n % s:0{digits}d}"


def main(name, radius=None):
    iv.dps = 80
    mp.dps = 30
    I = pm.load(name)
    cons, names = I["cons"], I["names"]
    nv = len(names)
    idx = {v: j for j, v in enumerate(names)}
    byname = {c["name"]: c for c in cons}
    P = json.load(open(os.path.join(HERE, "points", f"{name}.json")))
    fixed = {idx[v]: Fr(d["value"]) for v, d in P["fixed"].items()}
    centre = {idx[v]: Fr(s) for v, s in P["free"].items()}
    S = [(d["row"], d["side"]) for d in P["system"]]
    radius = radius or P["radius"]
    r = Fr(radius)
    # ---- 1. structure
    assert set(fixed) | set(centre) == set(range(nv)) and not set(fixed) & set(centre)
    assert len(S) == len(centre) and len({rn for rn, _ in S}) == len(S)
    for rn, side in S:
        c = byname[rn]
        assert side in ("lb", "ub") and c[side + "F"] is not None
        assert c["lbF"] is None or c["ubF"] is None or c["lbF"] <= c["ubF"]   # equality at a side satisfies the row
    free = sorted(centre)
    col = {j: t for t, j in enumerate(free)}
    m = len(free)
    eqrows = [c["name"] for c in cons if c["lbF"] is not None and c["lbF"] == c["ubF"]]
    print(f"{name}: {nv} variables ({m} free, {len(fixed)} fixed), {len(cons)} rows "
          f"({len(eqrows)} equalities), |S| = {len(S)}, radius {radius}")
    # ---- interval data
    num = pm.ctx_num(iv)
    xfix = {j: pm.iv_of_frac(iv, q) for j, q in fixed.items()}
    xc = [None] * nv
    X = [None] * nv
    lo, hi = {}, {}
    for j in range(nv):
        if j in fixed:
            xc[j] = X[j] = xfix[j]
        else:
            lo[j], hi[j] = centre[j] - r, centre[j] + r
            xc[j] = pm.iv_of_frac(iv, centre[j])
            a, b = pm.iv_of_frac(iv, lo[j]), pm.iv_of_frac(iv, hi[j])
            X[j] = iv.mpf([a.a, b.b])
    # ---- 2. Krawczyk
    Fc, JX, Jc = [], [], np.zeros((m, m))
    xf = [mp.mpf(fixed[j].numerator) / fixed[j].denominator if j in fixed else mp.mpf(centre[j].numerator) / centre[j].denominator
          for j in range(nv)]
    numf = pm.ctx_num(mp)
    for i, (rn, side) in enumerate(S):
        c = byname[rn]
        Fc.append(pm.ev_row(c, xc, iv, num).v - num(c[side]))
        d = pm.ev_row(c, X, iv, num)
        JX.append({col[j]: g for j, g in d.g.items() if j in col})
        for j, g in pm.ev_row(c, xf, mp, numf).g.items():
            if j in col:
                Jc[i, col[j]] += float(g)
    C = np.linalg.inv(Jc)
    print(f"  cond(J(c)) = {np.linalg.cond(Jc):.3e}; max |C| row sum = {np.abs(C).sum(1).max():.3e}")
    Civ = [[iv.mpf(float(C[i, k])) for k in range(m)] for i in range(m)]
    # M = I - C J(X), dense interval matrix, built column by column from sparse J(X)
    Jcols = [dict() for _ in range(m)]
    for k, rowd in enumerate(JX):
        for t, g in rowd.items():
            Jcols[t][k] = g
    M = [[None] * m for _ in range(m)]
    for t in range(m):
        ent = list(Jcols[t].items())
        for i in range(m):
            s = iv.mpf(0)
            Ci = Civ[i]
            for k, g in ent:
                s += Ci[k] * g
            M[i][t] = (iv.mpf(1) if i == t else iv.mpf(0)) - s
    dX = [X[free[t]] - xc[free[t]] for t in range(m)]   # encloses X - c
    worst = Fr(0)   # largest |K - c| / r over components (must be < 1)
    for i in range(m):
        j = free[i]
        CF = iv.mpf(0)
        for k in range(m):
            CF += Civ[i][k] * Fc[k]
        s = iv.mpf(0)
        for t in range(m):
            s += M[i][t] * dX[t]
        K = xc[j] - CF + s
        a, b = pm.iv_ends(K)
        assert lo[j] < a and b < hi[j], f"Krawczyk inclusion fails for {names[j]}"
        worst = max(worst, (b - centre[j]) / r, (centre[j] - a) / r)
    print(f"  Krawczyk: K(X) inside int(X) for all {m} components; max |K - c|/r = {float(worst):.3e}")
    # ---- 3. all rows
    inS = dict(S)
    n_sys = n_exact = n_iv = 0
    min_margin = None
    for c in cons:
        if c["name"] in inS:
            n_sys += 1
            continue
        lb, ub = c["lbF"], c["ubF"]
        if all(j in fixed for j in c["vars"]) and c["nl"] is None and not c["quad"]:
            v = Fr(c["constant"]) + sum(Fr(a) * fixed[j] for j, a in c["lin"].items())
            assert (lb is None or lb <= v) and (ub is None or v <= ub), f"row {c['name']} fails exactly"
            n_exact += 1
            continue
        assert not (lb is not None and lb == ub), f"equality row {c['name']} neither in S nor exact"
        a, b = pm.iv_ends(pm.ev_row(c, X, iv, num).v)
        mg = min(([a - lb] if lb is not None else []) + ([ub - b] if ub is not None else []))
        assert mg > 0, f"row {c['name']} not proved: enclosure [{float(a)}, {float(b)}], bounds {lb}, {ub}"
        n_iv += 1
        if min_margin is None or mg < min_margin[0]:
            min_margin = (mg, c["name"])
    print(f"  rows: {n_sys} in S (hold at x*), {n_exact} exact rational checks on fixed variables, "
          f"{n_iv} interval checks (smallest margin {float(min_margin[0]):.4e} at {min_margin[1]})")
    # ---- 4. objective and gap
    oa, ob = pm.iv_ends(pm.ev_obj(I, X, iv, num))
    dual = Fr(DUAL[name])
    gap = ob - dual
    print(f"  objective enclosure: [{fdec(oa, 22, False)}, {fdec(ob, 22, True)}] (width {float(ob - oa):.2e})")
    print(f"  dual bound {DUAL[name]} ; rigorous gap (obj upper end - dual) <= {fdec(gap, 15, True)} "
          f"; relative to the dual <= {fdec(gap / dual * 10**9, 6, True)}e-9")
    print(f"  RESULT {name}: PROVED exactly feasible point exists in the stored box")
    return dict(obj_lo=oa, obj_hi=ob, gap=gap)


if __name__ == "__main__":
    main(*sys.argv[1:])
