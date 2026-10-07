"""Reviewer's own reading of the pindyck OSIL (independent of pindyck.py / pindyck_global.py).

Reads the OSIL with own_osil.py, asserts the recursion structure row by row, and exports
exact data:  CT[t] (right sides of the demand rows, t = 0..15), DELTA[t] (objective weights,
decimal strings), KAPSTR (the exponent coefficient), and helpers
  states(p, mp)  -> full 116-vector x (mpmath numbers) from prices p via the recursion
                    (s_t solved by Newton at the working precision)
  rows_resid(x)  -> max |row residual| and max bound violation, evaluated from the OSIL trees.
"""
import os
from fractions import Fraction as Fr

import mpmath as mp

import own_osil

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/pindyck.osil")
I = own_osil.read(OSIL)
T = 16
nm = {v: j for j, v in enumerate(I["names"])}


def X(k):
    return nm[f"x{k}"]


P = [X(t) for t in range(1, 17)]            # prices
TD = [X(17 + t) for t in range(17)]         # td_0..td_16
S = [X(34 + t) for t in range(17)]          # s_0..s_16
CS = [X(51 + t) for t in range(17)]         # cs_0..cs_16
D = [None] + [X(67 + t) for t in range(1, 17)]
R = [X(84 + t) for t in range(17)]
REV = [None] + [X(100 + t) for t in range(1, 17)]

assert len(I["names"]) == 116 and len(I["cons"]) == 96
fixed = {TD[0]: ("18", "18"), S[0]: ("6.5", "6.5"), CS[0]: ("0", "0"), R[0]: ("500", "500")}
for j in range(116):
    b = (I["lb"][j], I["ub"][j])
    if j in fixed:
        assert b == fixed[j], (j, b)
    elif j in REV[1:]:
        assert b == ("-INF", "INF"), (j, b)
    else:
        assert b == ("0", "INF"), (j, b)

KAPSTR = "-.142857142857143"
CT = []
for t in range(1, 17):
    c = I["cons"][t - 1]
    assert c["lb"] == c["ub"] and c["nl"] is None and c["constant"] == "0"
    assert c["lin"] == {P[t - 1]: ".13", TD[t - 1]: "-.87", TD[t]: "1"}
    CT.append(c["lb"])
    c = I["cons"][15 + t]
    assert c["lb"] == c["ub"] == "0" and c["lin"] == {S[t - 1]: "-.75", S[t]: "1"}
    assert c["nl"] == ("negate", ("product", ("power", ("num", "1.02"), ("var", CS[t], KAPSTR)),
                                  ("sum", ("num", "1.1"), ("var", P[t - 1], ".1")))), c["nl"]
    c = I["cons"][31 + t]
    assert c["lb"] == c["ub"] == "0" and c["nl"] is None and c["lin"] == {S[t]: "-1", CS[t - 1]: "-1", CS[t]: "1"}
    c = I["cons"][47 + t]
    assert c["lb"] == c["ub"] == "0" and c["nl"] is None and c["lin"] == {TD[t]: "-1", S[t]: "1", D[t]: "1"}
    c = I["cons"][63 + t]
    assert c["lb"] == c["ub"] == "0" and c["nl"] is None and c["lin"] == {D[t]: "1", R[t - 1]: "-1", R[t]: "1"}
    c = I["cons"][79 + t]
    assert c["lb"] == c["ub"] == "0" and c["lin"] == {REV[t]: "1"}
    assert c["nl"] == ("product", ("sum", ("negate", ("divide", ("num", "2.5e2"), ("var", R[t], "1"))),
                                   ("var", P[t - 1], "1")), ("var", D[t], "-1")), c["nl"]
o = I["obj"]
assert o["sense"] == "min" and o["constant"] == "0" and o["nl"] is None
assert set(o["lin"]) == set(REV[1:])
DELTA = []
for t in range(1, 17):
    s = o["lin"][REV[t]]
    assert s.startswith("-")
    DELTA.append(s[1:])
CTq = [Fr(c) for c in CT]
DELTAq = [Fr(d) for d in DELTA]


def states(p, ctx=mp):
    """x (list of 116 ctx numbers) from prices p (ctx numbers), exact recursion
    (s_t: Newton on s - a - b exp(-K s) = 0 at the working precision)."""
    K = -ctx.mpf(KAPSTR) * ctx.log(ctx.mpf("1.02"))
    x = [ctx.mpf(0)] * 116
    td, s, cs, Rv = ctx.mpf(18), ctx.mpf("6.5"), ctx.mpf(0), ctx.mpf(500)
    x[TD[0]], x[S[0]], x[CS[0]], x[R[0]] = td, s, cs, Rv
    for t in range(1, 17):
        pt = p[t - 1]
        x[P[t - 1]] = pt
        td = ctx.mpf(".87") * td - ctx.mpf(".13") * pt + ctx.mpf(CT[t - 1])
        a = ctx.mpf(".75") * s
        b = (ctx.mpf("1.1") + ctx.mpf(".1") * pt) * ctx.exp(-K * cs)
        y = a + b
        for _ in range(200):
            f = y - a - b * ctx.exp(-K * y)
            y = y - f / (1 + K * b * ctx.exp(-K * y))
        s = y
        cs = cs + s
        d = td - s
        Rv = Rv - d
        x[TD[t]], x[S[t]], x[CS[t]], x[D[t]], x[R[t]] = td, s, cs, d, Rv
        x[REV[t]] = (pt - 250 / Rv) * d
    return x


def rows_resid(x, ctx=mp):
    worst = ctx.mpf(0)
    for c in I["cons"]:
        v = own_osil.row_value(c, x, ctx)
        lo, hi = ctx.mpf(c["lb"]), ctx.mpf(c["ub"])
        worst = max(worst, lo - v, v - hi)
    bw = ctx.mpf(0)
    for j in range(116):
        if I["lb"][j] != "-INF":
            bw = max(bw, ctx.mpf(I["lb"][j]) - x[j])
        if I["ub"][j] != "INF":
            bw = max(bw, x[j] - ctx.mpf(I["ub"][j]))
    return worst, bw


def objective(x, ctx=mp):
    return own_osil.obj_value(I["obj"], x, ctx)
