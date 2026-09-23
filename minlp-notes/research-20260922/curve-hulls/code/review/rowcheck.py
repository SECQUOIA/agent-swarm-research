"""Check that the author's model.build(name, "sub") is the OSiL model with x^2, x^3 replaced by auxiliaries.

At random points x in the variable box (binaries random 0/1), set every auxiliary t from its defining
constraint in the Gurobi model (quadratic def rows and NL def genconstrs, evaluated from Gurobi's stored
expression trees), then evaluate every other row of the Gurobi model and compare with the row value
computed by rbuild.parse (reviewer's OSiL reader).  Also checks row counts, senses, right-hand sides,
the objective, variable bounds, and that each t is a function of exactly one x.  Also compares the
funcs of the saved cuts with the funcs the current model.py selects.
python rowcheck.py <instance>"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import rbuild, model
from gurobipy import GRB

name = sys.argv[1]
P = rbuild.parse(name)
B = model.build(name, "sub")
m = B.m
xs = B.x
assert len(xs) == len(P["V"])
for v, d in zip(xs, P["V"]):
    assert v.LB == d["lb"] and v.UB == d["ub"], (v.VarName, d)
    assert (v.VType == GRB.BINARY) == (d["type"] == "B")

qcs = m.getQConstrs()
defs = [q for q in qcs if q.QCName.startswith("def")]
rows = [q for q in qcs if not q.QCName.startswith("def")]
assert m.NumConstrs == 0 or all(c.ConstrName.startswith("r") for c in m.getConstrs())
lin_rows = m.getConstrs()
gdefs = m.getGenConstrs()
print(name, "QC def", len(defs), "NL def", len(gdefs), "QC rows", len(rows), "lin rows", len(lin_rows),
      "OSiL cons", len(P["cons"]))

# expected (name, sense, rhs) per OSiL row
expected = {}
for i, c in enumerate(P["cons"]):
    r = i + 1
    if c["lb"] == c["ub"]:
        expected[f"r{r}"] = ("=", c["lb"], i)
    else:
        if math.isfinite(c["lb"]):
            expected[f"r{r}lo"] = (">", c["lb"], i)
        if math.isfinite(c["ub"]):
            expected[f"r{r}up"] = ("<", c["ub"], i)
got = {q.QCName: q for q in rows}
gotl = {c.ConstrName: c for c in lin_rows}
assert set(expected) == set(got) | set(gotl), (set(expected) ^ (set(got) | set(gotl)))
for n, (s, rhs, i) in expected.items():
    q = got.get(n)
    sense, grhs = (q.QCSense, q.QCRHS) if q is not None else (gotl[n].Sense, gotl[n].RHS)
    assert sense == s, (n, sense, s)

rng = np.random.default_rng(7)
vidx = {v.index: j for j, v in enumerate(xs)}


def eval_tree(opc, data, parent, val):
    n = len(opc)
    kids = [[] for _ in range(n)]
    for i, p in enumerate(parent):
        if p >= 0:
            kids[p].append(i)

    def ev(i):
        o = opc[i]
        if o == 0:
            return data[i]
        if o == 1:
            return val[data[i].index]
        k = [ev(c) for c in kids[i]]
        if o == 12:
            return k[0] ** k[1]
        if o == 4:
            return float(np.prod(k))
        if o == 2:
            return sum(k)
        if o == 6:
            return -k[0]
        if o == 7:
            return k[0] ** 2
        raise NotImplementedError(o)
    return ev(0)


def lin_val(le, val):
    return le.getConstant() + sum(le.getCoeff(k) * val[le.getVar(k).index] for k in range(le.size()))


def quad_val(qe, val):
    s = lin_val(qe.getLinExpr(), val)
    return s + sum(qe.getCoeff(k) * val[qe.getVar1(k).index] * val[qe.getVar2(k).index] for k in range(qe.size()))


def box(d):
    lo, hi = d["lb"], d["ub"]
    if not math.isfinite(lo):
        lo = (hi if math.isfinite(hi) else 10.0) - 20.0
    if not math.isfinite(hi):
        hi = lo + 20.0
    return lo, hi


maxerr = maxobj = 0.0
auxof = {}
for trial in range(3):
    x = np.array([rng.integers(0, 2) if d["type"] == "B" else rng.uniform(*box(d)) for d in P["V"]], float)
    val = np.zeros(m.NumVars)
    for v, j in vidx.items():
        val[v] = x[j]
    known = set(vidx)
    for g in gdefs:
        res, opc, data, parent = m.getGenConstrNLAdv(g)
        vs = {data[i].index for i in range(len(opc)) if opc[i] == 1}
        assert len(vs) == 1 and vs <= known
        auxof[res.VarName] = xs[vidx[next(iter(vs))]].VarName
        val[res.index] = eval_tree(opc, data, parent, val)
    for q in defs:
        qe = m.getQCRow(q)
        le = qe.getLinExpr()
        assert le.size() == 1 and le.getConstant() == 0 and q.QCSense == "="
        t = le.getVar(0)
        qv = {qe.getVar1(k).index for k in range(qe.size())} | {qe.getVar2(k).index for k in range(qe.size())}
        assert len(qv) == 1 and qv <= known
        auxof[t.VarName] = xs[vidx[next(iter(qv))]].VarName
        val[t.index] = (q.QCRHS - sum(qe.getCoeff(k) * val[qe.getVar1(k).index] * val[qe.getVar2(k).index]
                                      for k in range(qe.size()))) / le.getCoeff(0)
    # every aux value within its bounds (bounds must contain g([l, u]))
    for v in m.getVars():
        if v.index not in known:
            assert v.LB - 1e-12 <= val[v.index] <= v.UB + 1e-12, (v.VarName, v.LB, val[v.index], v.UB)
    for n, (s, rhs, i) in expected.items():
        c = P["cons"][i]
        f = sum(a * x[j] for j, a in c["lin"].items()) + sum(a * x[p] * x[q] for p, q, a in c["quad"]) + \
            sum(x[j] ** 3 for j in c["cube"])
        q = got.get(n)
        g = quad_val(m.getQCRow(q), val) - q.QCRHS if q is not None else lin_val(m.getRow(gotl[n]), val) - gotl[n].RHS
        err = abs(g - (f - rhs)) / (1 + abs(f) + abs(rhs))
        maxerr = max(maxerr, err)
    fo = sum(a * x[j] for j, a in P["objlin"].items())
    go = quad_val(m.getObjective(), val) if hasattr(m.getObjective(), "getLinExpr") else lin_val(m.getObjective(), val)
    maxobj = max(maxobj, abs(fo - go))
    assert m.ModelSense == GRB.MINIMIZE
print("max relative row mismatch", maxerr, "objective mismatch", maxobj)

# aux mapping: every aux t{v}_j is a function of x_v
bad = [t for t, xv in auxof.items() if t[1:].split("_")[0] != xv[1:]]
print("aux defined from a different x than its name says:", bad[:5])

# saved-cut funcs vs current model.py scaling
cuts = json.load(open(os.path.join(HERE, "..", "cuts", f"{name}.json")))
cur = {v: [str(sc.g) for _, _, sc in keep] for v, keep in B.det.sel.items()}
mism = sorted({(c["v"], tuple(c["funcs"]), tuple(cur.get(c["v"], []))) for c in cuts if c["funcs"] != cur.get(c["v"])})
print("cuts whose funcs differ from current model.py:", sum(c["funcs"] != cur.get(c["v"]) for c in cuts), "of", len(cuts),
      "example:", mism[:2])
print("selected vars in current model.py:", len(B.det.sel), "; reviewer selection:", len(rbuild.selected(P)),
      "same set:", set(B.det.sel) == set(rbuild.selected(P)))

# for cuts whose funcs match the current model: t{v}_j at the last random point equals funcs[j](x_v)
worst = 0.0
for c in cuts:
    if c["funcs"] != cur.get(c["v"]):
        continue
    xv = x[c["v"]]
    for j, f in enumerate(c["funcs"]):
        k, p = rbuild.func_multiplier(f)
        worst = max(worst, abs(val[m.getVarByName(f"t{c['v']}_{j}").index] - k * xv ** p))
print("max |t_vj - funcs_j(x_v)| over matching cuts:", worst)
