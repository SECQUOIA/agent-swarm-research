"""Reviewer's independent OSiL reader and Gurobi builder for the waterno2 family.

Supports only what waterno2_* contains: linear terms, quadratic terms, and nonlinear expressions
of the form power(variable, number).  Anything else raises.  Does not import model.py or curvehull.py.

build(name, mode): mode "orig" keeps x^3 as a general NL constraint; mode "sub" introduces, for every
non-binary variable with finite bounds that has both a diagonal x^2 term and an x^3 term,
y = x^2 (quadratic equality) and z = x^3 (NL equality) with exact bounds, and replaces
c*x^2 -> c*y and x^3 -> z everywhere.  add_cuts adds saved author cuts, translated to (x, y, z).
"""
import math
import os
import re
import xml.etree.ElementTree as ET
from fractions import Fraction

import gurobipy as gp
from gurobipy import GRB

NS = "{os.optimizationservices.org}"
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/{}.osil")


def parse(name):
    root = ET.parse(OSIL.format(name)).getroot().find(NS + "instanceData")
    V = []
    for v in root.find(NS + "variables"):
        t = v.get("type", "C")
        lb = v.get("lb", "0")
        ub = v.get("ub", "1" if t == "B" else "INF")
        V.append(dict(name=v.get("name"), type=t, lb_s=lb, ub_s=ub,
                      lb=float(lb.replace("-INF", "-inf")), ub=float(ub.replace("INF", "inf"))))
    obj = root.find(NS + "objectives")[0]
    assert obj.get("maxOrMin", "min") == "min" and obj.get("constant") is None
    objlin = {int(c.get("idx")): float(c.text) for c in obj}
    cons = []
    for c in root.find(NS + "constraints"):
        assert c.get("constant") is None
        cons.append(dict(name=c.get("name"), lb=float(c.get("lb", "-INF").replace("-INF", "-inf")),
                         ub=float(c.get("ub", "INF").replace("INF", "inf")), lin={}, quad=[], cube=[]))
    L = root.find(NS + "linearConstraintCoefficients")

    def expand(el, cast):
        out = []
        for e in el:
            m, inc = int(e.get("mult", "1")), e.get("incr")
            for k in range(m):
                out.append(cast(e.text) + (k * cast(inc) if inc else 0))
        return out
    start = expand(L.find(NS + "start"), int)
    val = expand(L.find(NS + "value"), float)
    colmajor = L.find(NS + "colIdx") is None
    idx = expand(L.find(NS + ("rowIdx" if colmajor else "colIdx")), int)
    for a in range(len(start) - 1):
        for k in range(start[a], start[a + 1]):
            r, j = (idx[k], a) if colmajor else (a, idx[k])
            assert j not in cons[r]["lin"]
            cons[r]["lin"][j] = val[k]
    objquad = []
    for q in root.find(NS + "quadraticCoefficients"):
        r = int(q.get("idx"))
        term = (int(q.get("idxOne")), int(q.get("idxTwo")), float(q.get("coef", "1")))
        (objquad if r == -1 else cons[r]["quad"]).append(term)
    objcube = []
    for nl in root.find(NS + "nonlinearExpressions"):
        r = int(nl.get("idx"))
        e = nl[0]
        assert e.tag == NS + "power" and e[0].tag == NS + "variable" and e[1].tag == NS + "number", ET.tostring(e)
        assert e[0].get("coef") in (None, "1")
        p = float(e[1].get("value"))
        assert p == 3.0
        (objcube if r == -1 else cons[r]["cube"]).append(int(e[0].get("idx")))
    return dict(V=V, objlin=objlin, objquad=objquad, objcube=objcube, cons=cons)


def selected(P):
    """Variables with a diagonal square term and a cube term, non-binary, finite bounds."""
    sq = {i for c in P["cons"] for i, j, _ in c["quad"] if i == j} | {i for i, j, _ in P["objquad"] if i == j}
    cu = {i for c in P["cons"] for i in c["cube"]} | set(P["objcube"])
    out = []
    for v in sorted(sq & cu):
        d = P["V"][v]
        if d["type"] != "B" and math.isfinite(d["lb"]) and math.isfinite(d["ub"]) and d["lb"] < d["ub"]:
            out.append(v)
    return out


def build(name, mode="orig", threads=1, P=None):
    P = P or parse(name)
    m = gp.Model(name)
    m.Params.OutputFlag = 0
    m.Params.Threads = threads
    m.Params.NonConvex = 2
    m.Params.MIPGap = 1e-4
    x = [m.addVar(lb=d["lb"], ub=d["ub"], vtype=GRB.BINARY if d["type"] == "B" else
                  (GRB.INTEGER if d["type"] == "I" else GRB.CONTINUOUS), name=d["name"]) for d in P["V"]]
    y, z, cubevar = {}, {}, {}
    if mode == "sub":
        for v in selected(P):
            l, u = P["V"][v]["lb"], P["V"][v]["ub"]
            ylo = 0.0 if l <= 0 <= u else min(l * l, u * u)
            y[v] = m.addVar(lb=ylo, ub=max(l * l, u * u), name=f"y_{v}")
            z[v] = m.addVar(lb=l ** 3, ub=u ** 3, name=f"z_{v}")
            m.addQConstr(y[v] == x[v] * x[v], name=f"defy_{v}")
            m.addGenConstrNL(z[v], x[v] ** 3, name=f"defz_{v}")

    def cube(v):
        if v in z:
            return z[v]
        if v not in cubevar:
            w = m.addVar(lb=-GRB.INFINITY, name=f"w_{v}")
            m.addGenConstrNL(w, x[v] ** 3)
            cubevar[v] = w
        return cubevar[v]

    def expr(lin, quad, cubes):
        e = gp.QuadExpr()
        for j, c in lin.items():
            e += c * x[j]
        for i, j, c in quad:
            e += c * y[i] if (i == j and i in y) else c * x[i] * x[j]
        for v in cubes:
            e += cube(v)
        return e

    m.setObjective(expr(P["objlin"], P["objquad"], P["objcube"]), GRB.MINIMIZE)
    for c in P["cons"]:
        e = expr(c["lin"], c["quad"], c["cube"])
        if c["lb"] == c["ub"]:
            m.addConstr(e == c["lb"], name=c["name"])
        else:
            if math.isfinite(c["lb"]):
                m.addConstr(e >= c["lb"], name=c["name"] + "_lo")
            if math.isfinite(c["ub"]):
                m.addConstr(e <= c["ub"], name=c["name"] + "_up")
    m.update()
    return m, x, y, z, P


FUNC = re.compile(r"^(?:(\d+)\*)?t\*\*([23])$")


def func_multiplier(s):
    """'8*t**3' -> (8, 3); 't**2' -> (1, 2).  Anything else raises."""
    mm = FUNC.match(s.strip())
    assert mm, s
    return int(mm.group(1) or 1), int(mm.group(2))


def add_cuts(m, x, y, z, cuts):
    """Author cut: c0 + c[0] x + sum_j c[j] g_j(x) >= 0 with g_j = k_j x^p_j; here g_j -> k_j * (y or z)."""
    for c in cuts:
        v = c["v"]
        e = gp.LinExpr(c["c"][0], x[v])
        for cj, f in zip(c["c"][1:], c["funcs"]):
            k, p = func_multiplier(f)
            e += cj * k * (y[v] if p == 2 else z[v])
        m.addLConstr(e, GRB.GREATER_EQUAL, -c["c0"])
    m.update()
