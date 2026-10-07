"""hvycrash: identity (objective constant on the feasible set) and an own
exactly feasible point, verified with mpmath interval arithmetic.

Own construction (differs from the authors'): c_k = 0.417 (upper bound) for all
k and theta_50 = 4.2; theta_{k-1} is defined by solving dyn_k (linear in
theta_{k-1}) and r_k = sqrt(-cos theta_k / D_k) solves alg_k.
"""
import json
import os
import sys
from fractions import Fraction

import mpmath
from mpmath import iv

import common

m = common.load("hvycrash")
n, cons = len(m["names"]), m["cons"]
out = {}

# ---------- 1. structure by exact template matching ----------
def D(c):
    return ("sum", ("product", ("var", c, ".486237"), ("var", c, "1")), ("num", "1.62079e-2"))

def t_acc(th, c, r):
    return ("divide", ("product", ("cos", ("var", th, "1")), ("num", "4.37e-3")),
            ("product", D(c), ("var", r, "1"), ("var", r, "1")))

def t_alg(th, c, r):
    return ("sum", ("negate", ("divide", ("num", "1"), ("var", r, "1"))),
            ("negate", ("divide", ("cos", ("var", th, "1")),
                        ("product", D(c), ("var", r, "1"), ("var", r, "1"), ("var", r, "1")))))

def t_dyn(th, c, r):
    return ("sum", ("divide", ("var", c, "4.37e-3"),
                    ("product", ("sum", ("product", ("var", c, ".3"), ("var", c, "1")), ("num", "1e-2")),
                     ("var", r, "1"), ("var", r, "1"))),
            ("negate", ("divide", ("product", ("cos", ("var", th, "1")), ("num", "4.37e-3")),
                        ("product", D(c), ("var", r, "1"), ("var", r, "1"), ("var", r, "1"), ("var", r, "1")))),
            ("var", th, "-.1"))

def varsof(t, acc):
    if t[0] == "var":
        acc.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            varsof(c, acc)
    return acc

stages = {}  # theta index -> dict
for i, row in enumerate(cons):
    assert row["lb"] == "0" and row["ub"] == "0" and row["constant"] == "0" and not row["quad"]
    t = row["nl"]
    # candidate (th, c, r): th = cos argument, c = var with .486237, r = var repeated in product
    th = [u[1] for u in [t] if False]
    found = None
    vs = sorted(varsof(t, set()))
    for th in vs:
        for c in vs:
            for r in vs:
                for kind, f in (("acc", t_acc), ("alg", t_alg), ("dyn", t_dyn)):
                    if f(th, c, r) == t:
                        found = (kind, th, c, r)
    assert found, (i, t)
    kind, th, c, r = found
    st = stages.setdefault(th, {})
    assert kind not in st
    st[kind] = dict(row=i, c=c, r=r, lin=row["lin"])
assert len(stages) == 50 and all(set(s) == {"acc", "alg", "dyn"} for s in stages.values())
for th, s in stages.items():
    assert s["acc"]["c"] == s["alg"]["c"] == s["dyn"]["c"] and s["acc"]["r"] == s["alg"]["r"] == s["dyn"]["r"]
    assert s["alg"]["lin"] == {}
    (tp, cf), = s["dyn"]["lin"].items()
    assert cf == ".1"
    s["thprev"] = tp
# chain theta_0 -> theta_50
prev_of = {th: s["thprev"] for th, s in stages.items()}
first = [th for th in stages if prev_of[th] not in stages]
assert len(first) == 1
theta0 = prev_of[first[0]]
order = [first[0]]
nxt = {v: k for k, v in prev_of.items()}
while order[-1] in nxt:
    order.append(nxt[order[-1]])
assert len(order) == 50
# accumulator chain: acc_k lin = {s_k: -1, s_{k-1}: +1} (first stage: {s_1: -1})
svar = []
for k, th in enumerate(order):
    lin = stages[th]["acc"]["lin"]
    neg = [j for j, v in lin.items() if v == "-1"]
    pos = [j for j, v in lin.items() if v == "1"]
    assert len(neg) == 1 and len(lin) == len(neg) + len(pos)
    if k == 0:
        assert pos == []
    else:
        assert pos == [svar[-1]]
    svar.append(neg[0])
o = m["obj"]
assert o["lin"] == {svar[-1]: "1"} and o["constant"] == "0" and o["nl"] is None and not o["quad"]
# bounds
used = set(order) | {theta0} | set(svar) | {stages[t]["alg"]["c"] for t in order} | {stages[t]["alg"]["r"] for t in order}
assert used == set(range(n)), (len(used), n)
for th in order + [theta0]:
    assert (m["lb"][th], m["ub"][th]) == ("0", "6.2831854")
for th in order:
    c, r = stages[th]["alg"]["c"], stages[th]["alg"]["r"]
    assert (m["lb"][c], m["ub"][c]) == ("8e-2", ".417")
    assert (m["lb"][r], m["ub"][r]) == ("-INF", "INF")
for s in svar:
    assert (m["lb"][s], m["ub"][s]) == ("-INF", "INF")
out["structure"] = dict(theta0=m["names"][theta0], theta50=m["names"][order[-1]],
                        objective_var=m["names"][svar[-1]], stages=50,
                        note="all 150 rows matched exact templates; all 201 variables accounted for")
print("structure ok:", out["structure"])

# ---------- 2. identity (exact rational algebra) ----------
# alg: -1/r - cos/(D r^3) = 0, r != 0 (division by r must be defined)  =>  cos/(D r^2) = -1.
# acc: -s_k + s_{k-1} + 4.37e-3 * cos/(D r^2) = 0  =>  s_k = s_{k-1} - 4.37e-3 (same D tree, checked).
# numeric check of the algebra with random rationals: cos/(D r^2) = X, alg residual = -(1/r)(1 + X)
import random
random.seed(1)
for _ in range(5):
    r = Fraction(random.randint(1, 10**6), 10**5) * random.choice([1, -1])
    X = Fraction(random.randint(-10**6, 10**6), 10**5)
    Dv = Fraction(random.randint(1, 10**6), 10**6)
    cosv = X * Dv * r * r
    alg = -1 / r - cosv / (Dv * r ** 3)
    assert alg == -(1 / r) * (1 + X)
obj_identity = -50 * Fraction("4.37e-3")
assert obj_identity == Fraction("-0.2185")
out["identity"] = "objective x%d = s_50 = -50*4.37e-3 = %s exactly at every feasible point" % (svar[-1] + 1, obj_identity)
print(out["identity"])

# ---------- 3. own feasible point, rigorous with iv ----------
iv.dps = 60
mpmath.mp.dps = 60
C = iv.mpf(".417")  # decimal string -> outward enclosure; exact value 0.417 lies inside
Dc = iv.mpf(".486237") * C * C + iv.mpf("1.62079e-2")
Ec = iv.mpf(".3") * C * C + iv.mpf("1e-2")
TH = [None] * 51
TH[50] = iv.mpf("4.2")
R = [None] * 51
checks = []
for k in range(50, 0, -1):
    cth = iv.cos(TH[k])
    assert cth.b < 0, (k, cth)  # cos theta_k < 0 strictly: r_k real and nonzero
    R[k] = iv.sqrt(-cth / Dc)
    A = iv.mpf("4.37e-3") * C / (Ec * R[k] ** 2)
    B = cth * iv.mpf("4.37e-3") / (Dc * R[k] ** 4)
    TH[k - 1] = TH[k] - 10 * (A - B)
for k in range(51):
    assert TH[k].a >= 0 and TH[k].b <= mpmath.mpf("6.2831854"), (k, TH[k])
maxw = max(float(t.delta) for t in TH)
# objective enclosure via acc rows
S = iv.mpf(0)
for k in range(1, 51):
    S = S + iv.cos(TH[k]) * iv.mpf("4.37e-3") / (Dc * R[k] * R[k])
out["own_point"] = dict(c="0.417 for all k", theta50="4.2",
                        theta0=str(TH[0]), theta1=str(TH[1]), theta49=str(TH[49]),
                        min_theta=float(min(t.a for t in TH)), max_theta=float(max(t.b for t in TH)),
                        max_cos=float(max(iv.cos(TH[k]).b for k in range(1, 51))),
                        max_theta_enclosure_width=maxw,
                        r_range=[float(min(r.a for r in R[1:])), float(max(r.b for r in R[1:]))],
                        objective_enclosure=[mpmath.nstr(S.a, 25), mpmath.nstr(S.b, 25)])
print(json.dumps(out["own_point"], indent=1))
assert S.a <= mpmath.mpf("-0.2185") <= S.b

# ---------- 4. decimal version of the point: exact-decimal residuals ----------
mpmath.mp.dps = 80
x = [mpmath.mpf(0)] * n
mid = lambda I: (mpmath.mpf(I.a) + mpmath.mpf(I.b)) / 2
x[theta0] = mid(TH[0])
s_acc = mpmath.mpf(0)
for k, th in enumerate(order, start=1):
    st = stages[th]["alg"]
    x[th] = mid(TH[k]); x[st["c"]] = mpmath.mpf(".417"); x[st["r"]] = mid(R[k])
for k, th in enumerate(order, start=1):
    row = cons[stages[th]["acc"]["row"]]
    # s_k = s_{k-1} + term
    st = stages[th]["alg"]
    s_acc = s_acc + mpmath.cos(x[th]) * mpmath.mpf("4.37e-3") / ((mpmath.mpf(".486237") * x[st["c"]] ** 2 + mpmath.mpf("1.62079e-2")) * x[st["r"]] ** 2)
    x[svar[k - 1]] = s_acc
xs = [mpmath.nstr(v, 60) for v in x]
xd = [mpmath.mpf(s) for s in xs]
viol = max(abs(common.row_value(m, i, xd, common.mpnum, common.MPFNS)) for i in range(len(cons)))
objv = common.obj_value(m, xd, common.mpnum, common.MPFNS)
out["own_point_decimal60"] = dict(objective=mpmath.nstr(objv, 30), max_row_violation=mpmath.nstr(viol, 5))
print(out["own_point_decimal60"])

# ---------- 5. MINLPLib points ----------
for p in ("p1", "p2", "p3"):
    sol = common.read_sol(os.path.join(common.HERE, "sol", "hvycrash.%s.sol" % p))
    xv = [mpmath.mpf(sol.get(nm, "0")) for nm in m["names"]]
    vi = [abs(common.row_value(m, i, xv, common.mpnum, common.MPFNS)) for i in range(len(cons))]
    imax = max(range(len(vi)), key=lambda i: vi[i])
    bviol = max([max(mpmath.mpf(m["lb"][j]) - xv[j], xv[j] - mpmath.mpf(m["ub"][j]), 0)
                 for j in range(n) if not common.osilx.isinf(m["ub"][j])] + [0])
    ratio = max(abs(mpmath.cos(xv[th]) / ((mpmath.mpf(".486237") * xv[stages[th]["alg"]["c"]] ** 2 + mpmath.mpf("1.62079e-2")) * xv[stages[th]["alg"]["r"]] ** 2) + 1) for th in order)
    out["minlplib_" + p] = dict(objective=mpmath.nstr(common.obj_value(m, xv, common.mpnum, common.MPFNS), 15),
                                max_row_violation=mpmath.nstr(vi[imax], 3), at=cons[imax]["name"],
                                max_bound_violation=mpmath.nstr(bviol, 3),
                                max_abs_cos_over_Dr2_plus_1=mpmath.nstr(ratio, 3),
                                r50=mpmath.nstr(xv[stages[order[-1]]["alg"]["r"]], 6))
    print(p, out["minlplib_" + p])
json.dump(out, open(os.path.join(common.HERE, "logs", "hvycrash.json"), "w"), indent=1)
open(os.path.join(common.HERE, "logs", "hvycrash_own_point.txt"), "w").write(
    "\n".join("%s %s" % (m["names"][j], xs[j]) for j in range(n)) + "\n")
