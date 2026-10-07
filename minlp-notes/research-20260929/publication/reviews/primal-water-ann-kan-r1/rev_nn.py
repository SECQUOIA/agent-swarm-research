"""Reviewer's independent check of the ann_cumene_tanh and KAN points (own OSIL reader rosil.py,
own rational interval arithmetic rint.py; no author code, no mpmath, no floating point).

Existence argument checked here: with the inputs fixed at exact rationals (and, for KAN, the
binaries fixed at the author's 0/1 values), repeatedly pick an equality row in which exactly one
variable is still unknown, that variable does not occur inside a nonlinear expression or a
square term, and its total coefficient (linear coefficient plus bilinear partners) is provably
nonzero; define the variable as the unique solution of that row.  The real point defined this
way satisfies every row used as a definition exactly.  Every other row (unused equalities exactly;
inequalities by exact or interval evaluation), every variable bound and integrality are then
checked.  KAN: the partition-of-unity rows (sum of continuous variables with coefficients 1 = 1)
are dropped, as in the relaxation R of wave 3.
usage: python3 rev_nn.py <instance>
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import json
import sys
import time
from fractions import Fraction as Fr

import rint
import rosil
from rint import V

PTS = _REPRO_ROOT + "/research-20260929/publication/primal/water-ann-kan/points"
W3 = _REPRO_ROOT + "/research-20260929/open-instances-wave3"


def dual_bound(name):
    if name == "ann_cumene_tanh":
        return Fr(-3386.5402291369187)  # reviews/ann-extension-review.md line 1 (binary64 value as stored)
    return Fr(json.load(open(f"{W3}/logs/{name}.result.json"))["dual_bound"])


def short(q, d=34):
    from decimal import Decimal, getcontext
    getcontext().prec = d
    return str(Decimal(q.numerator) / Decimal(q.denominator))


def main(name):
    t0 = time.time()
    M = rosil.load(name)
    N, n = M["names"], M["n"]
    idx = {nm: j for j, nm in enumerate(N)}
    P = json.load(open(f"{PTS}/{name}.point.json"))
    isbin = [t in ("B", "I") for t in M["vtype"]]
    # ---- inputs, cross-checked against the original sources
    inputs = {idx[k]: Fr(v) for k, v in P["inputs"].items()}
    if name == "ann_cumene_tanh":
        sol = {}
        for line in open(f"{W3}/sol/ann_cumene_tanh.wave3.sol"):
            p = line.split()
            if len(p) == 2:
                sol[p[0]] = p[1]
        src_ok = all(Fr(sol[N[j]]) == q for j, q in inputs.items())
        print(f"{name}: inputs {[N[j] for j in inputs]} equal the decimals in wave3.sol: {src_ok}")
    else:
        u = json.load(open(f"{W3}/logs/{name}.result.json"))["u"]
        src_ok = [Fr(x) for x in u] == list(inputs.values())
        print(f"{name}: inputs {[N[j] for j in inputs]} equal the binary64 u of result.json: {src_ok}")
    assert src_ok
    fixed = {j: V.num(q) for j, q in inputs.items()}
    for j in range(n):
        if isbin[j]:
            s = P["x"][N[j]]
            assert s in ("0", "1"), (N[j], s)
            fixed[j] = V.num(Fr(s))
    nbin = sum(isbin)
    # ---- rows dropped by R (KAN only)
    drop = set()
    if name.startswith("kan"):
        for r, c in enumerate(M["cons"]):
            if (c["lb"] == 1 and c["ub"] == 1 and not c["quad"] and c["nl"] is None and c["const"] == 0
                    and c["lin"] and all(a == 1 for a in c["lin"].values()) and not any(isbin[j] for j in c["lin"])):
                drop.add(r)
        dropped_names = sorted(M["cons"][r]["name"] for r in drop)
        print(f"partition rows (continuous vars, coefficients 1, rhs 1) dropped: {len(drop)}; "
              f"same set as the author's 'dropped_rows': {set(dropped_names) == set(P['dropped_rows'])}")
    print(f"{n} variables ({nbin} binaries fixed at the author's 0/1 values), {len(M['cons'])} rows")
    # ---- forward definitions
    X = [None] * n
    for j, v in fixed.items():
        X[j] = v
    rv = [rosil.row_vars(c) for c in M["cons"]]
    nlv = [rosil.tree_vars(c["nl"]) if c["nl"] is not None else set() for c in M["cons"]]
    eqrows = [r for r, c in enumerate(M["cons"]) if c["lb"] is not None and c["lb"] == c["ub"] and r not in drop]
    used = {}
    order = []
    progress = True
    while progress:
        progress = False
        for r in eqrows:
            if r in used:
                continue
            unk = [j for j in rv[r] if X[j] is None]
            if len(unk) != 1:
                continue
            v = unk[0]
            c = M["cons"][r]
            if v in nlv[r] or any(i == v and j == v for i, j, _ in c["quad"]):
                continue
            coef = V.num(c["lin"].get(v, 0))
            rest = V.num(c["const"])
            for j, a in c["lin"].items():
                if j != v:
                    rest = rest + V.num(a) * X[j]
            for i, j, a in c["quad"]:
                if i == v or j == v:
                    coef = coef + V.num(a) * X[j if i == v else i]
                else:
                    rest = rest + V.num(a) * X[i] * X[j]
            if c["nl"] is not None:
                rest = rest + rosil.eval_tree(c["nl"], X, V)
            if (coef.is_exact() and coef.q == 0) or (not coef.is_exact() and coef.contains0()):
                continue
            X[v] = V.div(V.num(c["lb"]) - rest, coef)
            used[r] = v
            order.append(r)
            progress = True
    und = [N[j] for j in range(n) if X[j] is None]
    print(f"forward definitions: {len(used)} equality rows used; undetermined variables: {len(und)} {und[:8]}")
    assert not und
    # the author's defined_by map, for comparison only
    auth = {nm: v["defined_by"] for nm, v in P["x"].items() if isinstance(v, dict)}
    mine = {N[v]: M["cons"][r]["name"] for r, v in used.items()}
    diff = [k for k in auth if mine.get(k) != auth[k]]
    print(f"definition rows agree with the author's 'defined_by' for {len(auth) - len(diff)} of {len(auth)} interval-valued variables")
    # ---- remaining rows
    neq_exact = 0
    nin = 0
    min_margin = None
    fails = []
    for r, c in enumerate(M["cons"]):
        if r in drop or r in used:
            continue
        body = rosil.eval_body(c, X, V)
        if c["lb"] is not None and c["lb"] == c["ub"]:
            if body.is_exact() and body.q == c["lb"]:
                neq_exact += 1
            else:
                fails.append((c["name"], "unused equality not exact"))
            continue
        nin += 1
        for side in ("lb", "ub"):
            b = c[side]
            if b is None:
                continue
            m = (body.lo - b) if side == "lb" else (b - body.hi)
            if m < 0:
                fails.append((c["name"], side, float(m)))
            elif not body.is_exact() and (min_margin is None or m < min_margin[0]):
                min_margin = (m, c["name"] + " " + side)
    print(f"unused equality rows holding exactly: {neq_exact}; inequality rows checked: {nin}; "
          f"smallest margin of an interval-valued inequality: "
          f"{float(min_margin[0]) if min_margin else None:.3e} ({min_margin[1] if min_margin else ''}); failures: {fails[:5]}")
    assert not fails
    # ---- bounds and integrality
    bfail = []
    zero_margin = []
    for j in range(n):
        for side in ("lb", "ub"):
            b = M[side][j]
            if b is None:
                continue
            m = (X[j].lo - b) if side == "lb" else (b - X[j].hi)
            if m < 0:
                bfail.append((N[j], side, float(m)))
            elif m == 0:
                zero_margin.append((N[j], side, "exact" if X[j].is_exact() else "interval"))
    zi = [z for z in zero_margin if z[2] == "interval"]
    print(f"variable bounds: failures {bfail[:5]} ({len(bfail)}); bounds met with equality: {len(zero_margin)} "
          f"(of which interval-valued: {len(zi)} {zi[:5]})")
    # a zero margin of an interval value is still a proof (lb <= lo <= x, or x <= hi <= ub)
    for nm, side, _ in zi:
        j = idx[nm]
        print(f"   zero-margin interval value {nm} ({side}): enclosure [{float(X[j].lo)!r}, {float(X[j].hi)!r}]")
    assert not bfail
    assert all(X[j].is_exact() and X[j].q in (0, 1) for j in range(n) if isbin[j])
    print(f"integrality: {nbin} binaries exactly 0/1")
    # ---- objective
    o = M["obj"]
    assert o["sense"] == "min"
    f = rosil.eval_body(dict(const=o["const"], lin=o["lin"], quad=o["quad"], nl=o["nl"]), X, V)
    dual = dual_bound(name)
    gap = f.hi - dual
    print(f"objective enclosure [{short(f.lo, 40)}, {short(f.hi, 40)}], width {float(f.hi - f.lo):.2e}")
    alo, ahi = Fr(P["objective_lo"]), Fr(P["objective_hi"])
    print(f"author's objective enclosure [{short(alo)}, {short(ahi)}] contains mine: {alo <= f.lo and f.hi <= ahi}; "
          f"intersects: {not (f.hi < alo or ahi < f.lo)}")
    print(f"dual bound {float(dual)!r} = {dual}; rigorous gap (upper end - dual) = {float(gap):.6e} "
          f"(exact upper bound {short(gap, 20)}); gap/|dual| = {float(gap / abs(dual)):.4e}; "
          f"gap/|primal| <= {float(gap / abs(f.lo if f.lo.__abs__() < f.hi.__abs__() else f.hi)):.4e}")
    # ---- consistency of every variable with the author's point file
    bad = 0
    for j in range(n):
        a = P["x"][N[j]]
        if isinstance(a, str):
            ok = X[j].lo <= Fr(a) <= X[j].hi
        else:
            lo, hi = Fr(a["lo"]), Fr(a["hi"])
            ok = not (X[j].hi < lo or hi < X[j].lo)
        bad += not ok
    print(f"author's stored values consistent with my enclosures (intersect): {n - bad} of {n}")
    print(f"time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main(sys.argv[1])
