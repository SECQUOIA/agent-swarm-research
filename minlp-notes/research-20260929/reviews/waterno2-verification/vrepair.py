"""Construct an EXACTLY feasible rational point near a nearly feasible point of a
period subproblem of waterno2_06 (the cheaper points of scip_check.py).

Method: binaries are fixed to their (integral) values.  Unknown variables are
determined one at a time from equality rows in which they are the only unknown
and appear linearly (all other monomials of the row being known), solved in
exact rational arithmetic.  When no such row exists, one unknown variable is
'seeded' with its value from the given point, rounded to `digits` decimals and
clipped to its bounds.  At the end every row and bound is checked exactly.
usage: python3 vrepair.py t [digits]
"""
import json
import sys
from fractions import Fraction as F

import scip_check as sc
import vmodel
from scip_diag import load_point

t = int(sys.argv[1])
digits = int(sys.argv[2]) if len(sys.argv) > 2 else 10
m, I = sc.m, sc.I
x0 = load_point(t)
V = I["per_vars"][t]
rows = [(i, vmodel.poly(m["cons"][i])) for i in I["per_rows"][t]]


def lb(v):
    return None if m["lb"][v].upper() == "-INF" else F(m["lb"][v])


def ub(v):
    return None if m["ub"][v].upper() in ("INF", "+INF") else F(m["ub"][v])


known = {}
for v in V:
    if m["vt"][v] == "B":
        known[v] = F(round(x0[v]))
    elif lb(v) is not None and lb(v) == ub(v):
        known[v] = lb(v)
eqrows = [(i, p, F(m["cons"][i]["lb"])) for i, p in rows if m["cons"][i]["lb"] == m["cons"][i]["ub"]]
# implied equalities: after substituting the fixed binaries (and fixed variables),
# two inequality rows may bound the same linear form from both sides with equal
# values (e.g. the big-M head rows of a running pump: x279 - x447 in [0, 0]).
groups = {}
for i, p in rows:
    c = m["cons"][i]
    if c["lb"] == c["ub"]:
        continue
    const, rest = F(0), {}
    for mono, a in p.items():
        if all(v in known for v in mono):
            val = a
            for v in mono:
                val *= known[v]
            const += val
        else:
            rest[mono] = a
    if not rest:
        continue
    lead = rest[min(rest)]
    key = tuple(sorted((mono, a / lead) for mono, a in rest.items()))
    lo_ = None if c["lb"].upper() == "-INF" else (F(c["lb"]) - const) / lead
    hi_ = None if c["ub"].upper() in ("INF", "+INF") else (F(c["ub"]) - const) / lead
    if lead < 0:
        lo_, hi_ = hi_, lo_
    g = groups.setdefault(key, [None, None, []])
    if lo_ is not None:
        g[0] = lo_ if g[0] is None else max(g[0], lo_)
    if hi_ is not None:
        g[1] = hi_ if g[1] is None else min(g[1], hi_)
    g[2].append(c["name"])
for key, (lo_, hi_, names) in groups.items():
    if lo_ is not None and lo_ == hi_:
        eqrows.append(("+".join(names), {mono: a for mono, a in key}, lo_))
        print("implied equality from rows", names, "value", lo_)
used = set()
seeded = []


def try_solve():
    progress = True
    while progress:
        progress = False
        for i, p, rhs in eqrows:
            if i in used:
                continue
            unk = {v for mono in p for v in mono if v not in known}
            if len(unk) != 1:
                continue
            u = unk.pop()
            const, coef, ok = F(0), F(0), True
            for mono, a in p.items():
                k = mono.count(u)
                if k == 0:
                    val = a
                    for v in mono:
                        val *= known[v]
                    const += val
                elif k == 1:
                    val = a
                    for v in mono:
                        if v != u:
                            val *= known[v]
                    coef += val
                else:
                    ok = False
            if not ok or coef == 0:
                continue
            known[u] = (rhs - const) / coef
            used.add(i)
            progress = True


def priority(v):
    # seed arguments of nonlinear monomials first (flows, speeds)
    nl = any(len(mono) > 1 and v in mono for _, p in rows for mono in p)
    return (0 if nl else 1, v)


def implied_interval(u):
    """Exact interval for u from all rows in which u is the only unknown and
    appears linearly (plus its own bounds)."""
    lo_, hi_ = lb(u), ub(u)
    for i, p in rows:
        if not any(u in mono for mono in p):
            continue
        if any(v not in known and v != u for mono in p for v in mono):
            continue
        const, coef = F(0), F(0)
        lin = True
        for mono, a in p.items():
            k = mono.count(u)
            val = a
            for v in mono:
                if v != u:
                    val *= known[v]
            if k == 0:
                const += val
            elif k == 1:
                coef += val
            else:
                lin = False
        if not lin or coef == 0:
            continue
        c = m["cons"][i]
        L = None if c["lb"].upper() == "-INF" else (F(c["lb"]) - const) / coef
        U = None if c["ub"].upper() in ("INF", "+INF") else (F(c["ub"]) - const) / coef
        if coef < 0:
            L, U = U, L
        if L is not None:
            lo_ = L if lo_ is None else max(lo_, L)
        if U is not None:
            hi_ = U if hi_ is None else min(hi_, U)
    return lo_, hi_


OFFS = {}
if len(sys.argv) > 3:
    for kv in sys.argv[3].split(","):
        k, v = kv.split("=")
        OFFS[k] = F(v)
try_solve()
while len(known) < len(V):
    u = min((v for v in V if v not in known), key=priority)
    val = F(format(x0[u], f".{digits}f")) + OFFS.get(m["names"][u], 0)  # exact decimal rounding
    for tie in (sys.argv[4].split(",") if len(sys.argv) > 4 else []):
        a_, b_, r_ = tie.split(":")  # seed a_ = r_ * value(b_)   (e.g. equal flows of identical pumps)
        if m["names"][u] == a_:
            vb = [v for v in V if m["names"][v] == b_][0]
            val = F(r_) * known[vb]
    lo_, hi_ = implied_interval(u)
    if lo_ is not None:
        val = max(val, lo_)
    if hi_ is not None:
        val = min(val, hi_)
    known[u] = val
    seeded.append(m["names"][u])
    try_solve()

x = [F(0)] * len(m["names"])
for v, val in known.items():
    x[v] = val
import veval  # noqa: E402
e = veval.evaluate(m, x, rows=I["per_rows"][t], vars_=V)
obj = vmodel.period_objective(I, t, sc.LAM, sc.MU)
val = sum(a * x[v] for v, a in obj.items())
print(f"period {t}: seeded {len(seeded)} variables {seeded}")
print(f"   exact: max row violation {e['maxrow']} ({e['row']}), max bound violation {e['maxbnd']} ({e['bvar']}), "
      f"binaries integral {e['int_ok']}")
print(f"   Lagrangian value (exact) = {float(val):.12f}; value of the SCIP point "
      f"{float(sum(a * F(x0[v]) for v, a in obj.items())):.12f}")
print(f"   EXACTLY FEASIBLE: {e['maxrow'] == 0 and e['maxbnd'] == 0 and e['int_ok']}")
import os  # noqa: E402
json.dump({m["names"][v]: str(known[v]) for v in V},
          open(os.environ.get("WV_OUT", f"logs/exact_point_p{t}.json"), "w"))
