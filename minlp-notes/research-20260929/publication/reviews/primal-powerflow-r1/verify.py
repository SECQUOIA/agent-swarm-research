"""Reviewer's independent check of the powerflow primal-point files.

    python3 verify.py <name> [radius]

Uses only: the cached OSIL file (read by osil_read.py), the author's point file
points/<name>.json (fixed rationals, free-variable centres, list of rows of the
square system S with sides), and dyadic outward-rounded interval arithmetic
(dyiv.py).  No mpmath, no osilx, no pfmodel.

Proof steps:
  0. model checks: all variables continuous with bounds (-inf, +inf); objective is
     min, weight 1, no nl part.
  1. structure: free/fixed partition, |S| = #free, sides finite.
  2. Krawczyk test (norm-free componentwise form) for G(y) = [row_i(y, z) - side_i]_{i in S}
     on X = [c - r, c + r] with the exact rational centre c, z = exact fixed values:
        K_i = c_i - (C G(c))_i + sum_t (I - C J(X))_it [-r, r]
     C = float64 inverse of the midpoint of J(X) (point matrix, exact dyadic).
     K_i inside (c_i - r, c_i + r) for all i => unique zero of G in X.
  3. every row: in S (holds with equality at its side, side within [lb, ub]),
     or all variables fixed and polynomial -> exact rational check,
     or interval enclosure over X strictly inside the bounds; equality rows must
     be in S or exact.
  4. objective enclosure over X; gap to the dual in exact rationals.
Plus evidence-level diagnostics on MINLPLib's p1 point.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import json
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import dyiv as V
import osil_read

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
PTS = _REPRO_ROOT + "/research-20260929/publication/primal/powerflow/points"
SOL = _REPRO_ROOT + "/research-20260929/open-instances-wave3/sol"
# duals copied from open-instances-summary.md lines 35-37
DUAL = {"powerflow0030p": Fr("576.8934122988004"),
        "powerflow0039p": Fr("41869.05148485014"),
        "powerflow0039r": Fr("41869.05148327243")}


# ---------- forward-mode interval evaluation: returns (value, {var: derivative}) ----------
def _gadd(g, h, scale=None):
    out = dict(g)
    for j, d in h.items():
        if scale is not None:
            d = V.mul(scale, d)
        out[j] = V.add(out[j], d) if j in out else d
    return out


class Evaluator:
    def __init__(self, x, want_grad):
        self.x = x                # list of intervals
        self.g = want_grad
        self.cache = {}

    def const(self, q):
        if q not in self.cache:
            self.cache[q] = V.of_frac(q)
        return self.cache[q]

    def tree(self, t):
        op = t[0]
        if op == "num":
            return self.const(t[1]), {}
        if op == "var":
            j, c = t[1], t[2]
            cc = self.const(c)
            return V.mul(cc, self.x[j]), ({j: cc} if self.g else {})
        kids = [self.tree(k) for k in t[1:]]
        if op == "sum":
            v, g = kids[0]
            for kv, kg in kids[1:]:
                v = V.add(v, kv)
                if self.g:
                    g = _gadd(g, kg)
            return v, g
        if op == "product":
            v, g = kids[0]
            for kv, kg in kids[1:]:
                if self.g:
                    g = _gadd({j: V.mul(d, kv) for j, d in g.items()}, kg, scale=v)
                v = V.mul(v, kv)
            return v, g
        if op == "square":
            (u, ug), = kids
            two_u = V.add(u, u)
            return V.mul(u, u), ({j: V.mul(two_u, d) for j, d in ug.items()} if self.g else {})
        if op == "sin":
            (u, ug), = kids
            cu = V.cos(u) if self.g else None
            return V.sin(u), ({j: V.mul(cu, d) for j, d in ug.items()} if self.g else {})
        if op == "cos":
            (u, ug), = kids
            su = V.neg(V.sin(u)) if self.g else None
            return V.cos(u), ({j: V.mul(su, d) for j, d in ug.items()} if self.g else {})
        raise NotImplementedError(op)

    def body(self, c):
        v = self.const(c["constant"])
        g = {}
        for j, a in c["lin"].items():
            ca = self.const(a)
            v = V.add(v, V.mul(ca, self.x[j]))
            if self.g:
                g = _gadd(g, {j: ca})
        for i, j, a in c["quad"]:
            ca = self.const(a)
            v = V.add(v, V.mul(ca, V.mul(self.x[i], self.x[j])))
            if self.g:
                g = _gadd(g, {i: V.mul(ca, self.x[j])})
                g = _gadd(g, {j: V.mul(ca, self.x[i])})
        if c["nl"] is not None:
            tv, tg = self.tree(c["nl"])
            v = V.add(v, tv)
            if self.g:
                g = _gadd(g, tg)
        return v, g


def exact_poly(c, xq):
    """exact rational value of a row body without nl part"""
    assert c["nl"] is None
    v = c["constant"] + sum(a * xq[j] for j, a in c["lin"].items())
    v += sum(a * xq[i] * xq[j] for i, j, a in c["quad"])
    return v


def fmt(q, digits, up):
    s = 10 ** digits
    n = (q * s).__ceil__() if up else (q * s).__floor__()
    sg = "-" if n < 0 else ""
    n = abs(n)
    return f"{sg}{n // s}.{n % s:0{digits}d}"


def main(name, radius=None):
    t0 = time.time()
    M = osil_read.read(os.path.join(OSIL, name + ".osil"))
    names, cons, obj = M["names"], M["cons"], M["obj"]
    n = len(names)
    # ---- 0. model checks
    assert all(t == "C" for t in M["vtype"]), "integer variables present"
    assert all(a is None for a in M["lb"]) and all(b is None for b in M["ub"]), "variable bounds present"
    assert obj["sense"] == "min" and Fr(obj["weight"]) == 1 and obj["nl"] is None
    idx = {v: j for j, v in enumerate(names)}
    byname = {c["name"]: c for c in cons}
    assert len(byname) == len(cons)
    P = json.load(open(os.path.join(PTS, name + ".json")))
    fixed = {idx[v]: Fr(d["value"]) for v, d in P["fixed"].items()}
    cen = {idx[v]: Fr(s) for v, s in P["free"].items()}
    r = Fr(radius if radius else P["radius"])
    S = [(d["row"], d["side"]) for d in P["system"]]
    # ---- 1. structure
    assert set(fixed).isdisjoint(cen) and set(fixed) | set(cen) == set(range(n))
    assert len(S) == len(cen) == len({a for a, _ in S})
    for rn, side in S:
        c = byname[rn]
        b = c[side]
        assert b is not None
        assert (c["lb"] is None or c["lb"] <= b) and (c["ub"] is None or b <= c["ub"])
    free = sorted(cen)
    col = {j: t for t, j in enumerate(free)}
    m = len(free)
    print(f"{name}: n = {n}, rows = {len(cons)}, free = {m}, fixed = {len(fixed)}, |S| = {len(S)}, r = {r}")
    # interval data: point enclosures of the exact values, box X
    xc = [None] * n
    X = [None] * n
    for j in range(n):
        if j in fixed:
            xc[j] = X[j] = V.of_frac(fixed[j])
        else:
            xc[j] = V.of_frac(cen[j])
            X[j] = (V.of_frac(cen[j] - r)[0], V.of_frac(cen[j] + r)[1])
    # ---- 2. Krawczyk
    Ec, EX = Evaluator(xc, False), Evaluator(X, True)
    Gc, JX = [], []
    for rn, side in S:
        c = byname[rn]
        v, _ = Ec.body(c)
        Gc.append(V.sub(v, V.of_frac(c[side])))
        _, g = EX.body(c)
        assert set(g) == V_rowvars(c), rn
        JX.append({col[j]: d for j, d in g.items() if j in col})
    Jmid = np.zeros((m, m))
    for i, row in enumerate(JX):
        for t, d in row.items():
            Jmid[i, t] = float(Fr(d[0] + d[1], 2 * V.ONE))
    C = np.linalg.inv(Jmid)
    print(f"  cond(Jmid) = {np.linalg.cond(Jmid):.3e}")
    # exact dyadic integers of C at scale 2^P  (floats with exponent >= -P are exact)
    Ci = []
    for i in range(m):
        rowi = []
        for k in range(m):
            q = Fr(float(C[i, k]))
            sc = q * V.ONE
            assert sc.denominator == 1, "C entry not representable at scale 2^P"
            rowi.append(int(sc))
        Ci.append(rowi)
    # columns of J(X)
    Jcol = [[] for _ in range(m)]
    for k, row in enumerate(JX):
        for t, d in row.items():
            Jcol[t].append((k, d))
    worst = Fr(0)
    maxS = Fr(0)
    for i in range(m):
        ci = Ci[i]
        # (C G(c))_i at scale 2^(2P), exact accumulation of point*interval products
        lo = hi = 0
        for k in range(m):
            a = ci[k]
            g = Gc[k]
            if a >= 0:
                lo += a * g[0]
                hi += a * g[1]
            else:
                lo += a * g[1]
                hi += a * g[0]
        CG = (Fr(lo, V.ONE * V.ONE), Fr(hi, V.ONE * V.ONE))
        # S_i = sum_t mag((I - C J(X))_it), upper bound, scale 2^(2P)
        Ssum = 0
        for t in range(m):
            lo = hi = 0
            for k, d in Jcol[t]:
                a = ci[k]
                if a >= 0:
                    lo += a * d[0]
                    hi += a * d[1]
                else:
                    lo += a * d[1]
                    hi += a * d[0]
            # entry = delta - [lo, hi]
            dlt = V.ONE * V.ONE if i == t else 0
            Ssum += max(abs(dlt - lo), abs(dlt - hi))
        Sq = Fr(Ssum, V.ONE * V.ONE)
        maxS = max(maxS, Sq)
        # K_i - c_i in [-CG_hi - r Sq, -CG_lo + r Sq]; need strictly inside (-r, r)
        up = -CG[0] + r * Sq
        dn = -CG[1] - r * Sq
        assert up < r and dn > -r, f"Krawczyk fails at {names[free[i]]}"
        worst = max(worst, up / r, -dn / r)
    print(f"  Krawczyk OK: K(X) in int(X) for all {m}; max |K_i - c_i|/r <= {float(worst):.3e}; "
          f"||I - C J(X)||_inf <= {float(maxS):.3e} (< 1: C and all J in J(X) nonsingular, zero unique)")
    # ---- 3. every row
    inS = dict(S)
    xq = {j: fixed[j] for j in fixed}
    n_s = n_ex = n_iv = 0
    minmg = None
    Ex = Evaluator(X, False)
    for c in cons:
        lb, ub = c["lb"], c["ub"]
        if c["name"] in inS:
            n_s += 1
            continue
        vs = V_rowvars(c)
        if vs <= set(fixed) and c["nl"] is None:
            v = exact_poly(c, xq)
            assert (lb is None or lb <= v) and (ub is None or v <= ub), f"exact check fails {c['name']}"
            n_ex += 1
            continue
        assert not (lb is not None and lb == ub), f"equality row {c['name']} neither in S nor exact"
        v, _ = Ex.body(c)
        a, b = V.lo_frac(v), V.hi_frac(v)
        mg = min(([a - lb] if lb is not None else []) + ([ub - b] if ub is not None else []))
        assert mg > 0, f"row {c['name']} fails over X: [{float(a)}, {float(b)}] vs {lb}, {ub}"
        n_iv += 1
        if minmg is None or mg < minmg[0]:
            minmg = (mg, c["name"])
    assert n_s + n_ex + n_iv == len(cons)
    print(f"  rows: {n_s} in S, {n_ex} exact, {n_iv} interval (min margin {float(minmg[0]):.4e} at {minmg[1]})")
    # ---- 4. objective
    ov = Ex.const(obj["constant"])
    for j, a in obj["lin"].items():
        ov = V.add(ov, V.mul(Ex.const(a), X[j]))
    for i, j, a in obj["quad"]:
        ov = V.add(ov, V.mul(Ex.const(a), V.mul(X[i], X[j])))
    olo, ohi = V.lo_frac(ov), V.hi_frac(ov)
    dual = DUAL[name]
    gap = ohi - dual
    print(f"  objective in [{fmt(olo, 22, False)}, {fmt(ohi, 22, True)}]; dual {float(dual)!r} < obj lo: {dual < olo}")
    print(f"  gap <= {fmt(gap, 15, True)}  rel <= {fmt(gap / dual, 15, True)}")
    # ---- p1 diagnostics (evidence; exact rational evaluation where polynomial, intervals otherwise)
    p1 = {}
    for line in open(os.path.join(SOL, name + ".p1.sol")):
        p = line.split()
        if len(p) == 2:
            p1[p[0]] = p[1]
    unknown = set(p1) - set(names)
    p1x = [V.of_frac(Fr(p1.get(v, "0"))) for v in names]
    Ep = Evaluator(p1x, False)
    worstv = (Fr(0), None)
    for c in cons:
        v, _ = Ep.body(c)
        a, b = V.lo_frac(v), V.hi_frac(v)
        viol = max([Fr(0)] + ([c["lb"] - a] if c["lb"] is not None else []) + ([b - c["ub"]] if c["ub"] is not None else []))
        if viol > worstv[0]:
            worstv = (viol, c["name"])
    pv = Ep.const(obj["constant"])
    for j, a in obj["lin"].items():
        pv = V.add(pv, V.mul(Ep.const(a), p1x[j]))
    for i, j, a in obj["quad"]:
        pv = V.add(pv, V.mul(Ep.const(a), V.mul(p1x[i], p1x[j])))
    print(f"  p1: entries {len(p1)} (unknown names {sorted(unknown)}), max row violation ~ {float(worstv[0]):.3e} at {worstv[1]}; "
          f"obj(p1) ~ {fmt(V.lo_frac(pv), 16, False)}; obj(centre) - obj(p1) ~ {float(olo - V.lo_frac(pv)):.3e}")
    mv = max(abs(cen[j] - Fr(p1.get(names[j], "0"))) for j in free)
    fx = [names[j] for j in fixed if fixed[j] != Fr(p1.get(names[j], "0"))]
    print(f"  max |centre - p1| over free vars = {float(mv):.3e}; fixed vars differing from p1: "
          + ", ".join(f"{v}({float(fixed[idx[v]] - Fr(p1.get(v, '0'))):.1e})" for v in fx))
    print(f"  time {time.time() - t0:.1f} s")


def V_rowvars(c):
    return osil_read.row_vars(c)


if __name__ == "__main__":
    main(*sys.argv[1:])
