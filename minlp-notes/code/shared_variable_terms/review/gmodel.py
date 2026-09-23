"""Reviewer's Gurobi builder from the reviewer's OSiL reader (osil_eval.Model); links use the note's link_detect.detect."""
import math, os, sys
from pathlib import Path
D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D)); sys.path.insert(0, str(D.parent / "univariate_envelopes")); sys.path.insert(0, str(Path(__file__).resolve().parent))
import gurobipy as gp
from gurobipy import GRB, nlfunc
from osil_eval import Model, NS

def gexpr(node, x):
    tag = node.tag.replace(NS, "")
    if tag == "number": return float(node.get("value"))
    if tag == "variable":
        c = float(node.get("coef", "1")); return x[int(node.get("idx"))] if c == 1.0 else c * x[int(node.get("idx"))]
    k = [gexpr(c, x) for c in node]
    if tag in ("sum", "plus"):
        out = k[0]
        for c in k[1:]: out = out + c
        return out
    if tag == "minus": return k[0] - k[1]
    if tag == "negate": return -1.0 * k[0]
    if tag in ("times", "product"):
        out = k[0]
        for c in k[1:]: out = out * c
        return out
    if tag == "divide": return k[0] / k[1]
    if tag == "power": return k[0] ** k[1]
    if tag == "square": return k[0] ** 2
    if tag == "ln": return nlfunc.log(k[0])
    if tag in ("sin", "cos", "exp", "sqrt"): return getattr(nlfunc, tag)(k[0])
    raise NotImplementedError(tag)

def detect(name):
    from uenv.osil import read_osil
    import link_detect
    inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    return link_detect.detect(inst)

def build(name, linked=False):
    M = Model(name)
    m = gp.Model(); m.Params.OutputFlag = 0
    inf = lambda v: (GRB.INFINITY if v == math.inf else -GRB.INFINITY if v == -math.inf else v)
    x = [m.addVar(lb=inf(l), ub=inf(u), vtype={"B": GRB.BINARY, "I": GRB.INTEGER}.get(t, GRB.CONTINUOUS)) for l, u, t in zip(M.lb, M.ub, M.vt)]
    for i in [-1, *range(len(M.rlb))]:
        e = gp.QuadExpr()
        for j, c in M.lin[i].items(): e += c * x[j]
        for a, b, c in M.quad[i]: e += c * x[a] * x[b]
        if i in M.nl:
            z = m.addVar(lb=-GRB.INFINITY); m.addGenConstrNL(z, gexpr(M.nl[i], x)); e += z
        if i == -1:
            m.setObjective(e + M.const, GRB.MINIMIZE if M.sense == "min" else GRB.MAXIMIZE); continue
        e += M.rconst[i]
        if M.rlb[i] == M.rub[i]: m.addConstr(e == M.rlb[i])
        else:
            if math.isfinite(M.rlb[i]): m.addConstr(e >= M.rlb[i])
            if math.isfinite(M.rub[i]): m.addConstr(e <= M.rub[i])
    trig, pw = detect(name)
    if linked:
        for v in trig:
            s = m.addVar(lb=-1, ub=1); c = m.addVar(lb=-1, ub=1)
            m.addGenConstrNL(s, nlfunc.sin(x[v])); m.addGenConstrNL(c, nlfunc.cos(x[v])); m.addConstr(s * s + c * c == 1)
        for v, ps_ in pw.items():
            lo, hi = M.lb[v], M.ub[v]; ref = min(ps_, key=abs); tv = {}
            for p in ps_:
                a, b = sorted((lo ** p, hi ** p)); tv[p] = m.addVar(lb=a, ub=b); m.addGenConstrNL(tv[p], x[v] ** p)
            for p in ps_:
                if p != ref: m.addGenConstrNL(tv[p], tv[ref] ** (p / ref))
    return M, m, x, trig, pw
