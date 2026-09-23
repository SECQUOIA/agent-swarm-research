"""Independent OSiL reader and plain-float evaluator / feasibility checker (reviewer's code).
Does not use uenv.osil.  Expression nodes are evaluated directly on the XML tree."""
import math, os
import xml.etree.ElementTree as ET
NS = "{os.optimizationservices.org}"

def _f(s):
    s = s.strip()
    return {"INF": math.inf, "-INF": -math.inf}.get(s, None) if s in ("INF", "-INF") else float(s)

def _expand(el):
    out = []
    for e in el:
        mult, incr, val = int(e.get("mult", "1")), float(e.get("incr", "0")), float(e.text)
        out += [val + k * incr for k in range(mult)]
    return out

class Model:
    def __init__(self, name):
        path = os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil")
        data = ET.parse(path).getroot().find(NS + "instanceData")
        self.lb, self.ub, self.vt, self.names = [], [], [], []
        for v in data.find(NS + "variables"):
            t = v.get("type", "C")
            self.vt.append(t); self.names.append(v.get("name"))
            self.lb.append(_f(v.get("lb", "0"))); self.ub.append(_f(v.get("ub", "1" if t == "B" else "INF")))
        assert set(self.vt) <= {"C", "B", "I"}, set(self.vt)
        objs = data.find(NS + "objectives")
        assert objs is not None and len(objs) == 1
        o = objs[0]
        self.sense, self.const = o.get("maxOrMin", "min"), float(o.get("constant", "0"))
        assert float(o.get("weight", "1")) == 1.0
        self.lin = {-1: {}}; self.quad = {-1: []}; self.nl = {}
        for c in o: self.lin[-1][int(c.get("idx"))] = self.lin[-1].get(int(c.get("idx")), 0.0) + float(c.text)
        cons = data.find(NS + "constraints")
        self.rlb, self.rub, self.rconst = [], [], []
        for i, c in enumerate(cons if cons is not None else []):
            self.rlb.append(_f(c.get("lb", "-INF"))); self.rub.append(_f(c.get("ub", "INF"))); self.rconst.append(float(c.get("constant", "0")))
            self.lin[i] = {}; self.quad[i] = []
        lcc = data.find(NS + "linearConstraintCoefficients")
        if lcc is not None:
            start = [int(v) for v in _expand(lcc.find(NS + "start"))]; val = _expand(lcc.find(NS + "value"))
            if lcc.find(NS + "rowIdx") is not None:
                idx = [int(v) for v in _expand(lcc.find(NS + "rowIdx"))]
                for col in range(len(start) - 1):
                    for k in range(start[col], start[col + 1]): self.lin[idx[k]][col] = self.lin[idx[k]].get(col, 0.0) + val[k]
            else:
                idx = [int(v) for v in _expand(lcc.find(NS + "colIdx"))]
                for r in range(len(start) - 1):
                    for k in range(start[r], start[r + 1]): self.lin[r][idx[k]] = self.lin[r].get(idx[k], 0.0) + val[k]
        qc = data.find(NS + "quadraticCoefficients")
        for q in (qc if qc is not None else []):
            self.quad[int(q.get("idx"))].append((int(q.get("idxOne")), int(q.get("idxTwo")), float(q.get("coef", "1"))))
        nle = data.find(NS + "nonlinearExpressions")
        for e in (nle if nle is not None else []):
            assert int(e.get("idx")) not in self.nl
            self.nl[int(e.get("idx"))] = e[0]

    def ev(self, node, x):
        tag = node.tag.replace(NS, "")
        if tag == "number": return float(node.get("value"))
        if tag == "variable": return float(node.get("coef", "1")) * x[int(node.get("idx"))]
        k = [self.ev(c, x) for c in node]
        if tag in ("sum", "plus"): return math.fsum(k)
        if tag == "minus": assert len(k) == 2; return k[0] - k[1]
        if tag == "negate": return -k[0]
        if tag in ("times", "product"): return math.prod(k)
        if tag == "divide": return k[0] / k[1]
        if tag == "power":
            b, p = k
            if b < 0 and p != int(p): raise ValueError(f"negative base {b} with exponent {p}")
            return b ** (int(p) if p == int(p) else p)
        if tag == "square": return k[0] * k[0]
        if tag == "sqrt": return math.sqrt(k[0])
        if tag == "ln": return math.log(k[0])
        if tag == "exp": return math.exp(k[0])
        if tag == "sin": return math.sin(k[0])
        if tag == "cos": return math.cos(k[0])
        if tag == "abs": return abs(k[0])
        raise NotImplementedError(tag)

    def row(self, i, x):
        v = math.fsum(c * x[j] for j, c in self.lin[i].items()) + math.fsum(c * x[a] * x[b] for a, b, c in self.quad[i])
        if i in self.nl: v += self.ev(self.nl[i], x)
        return v + (self.const if i == -1 else self.rconst[i])

    def check(self, x):
        """objective, max abs row violation (and relative to row activity scale), max bound violation, max integrality violation."""
        out = {"obj": self.row(-1, x), "row": 0.0, "row_rel": 0.0, "bound": 0.0, "int": 0.0, "worst_row": None}
        for i in range(len(self.rlb)):
            a = self.row(i, x)
            viol = max(self.rlb[i] - a, a - self.rub[i], 0.0)
            scale = max(1.0, max((abs(c * x[j]) for j, c in self.lin[i].items()), default=0.0))
            if viol > out["row"]: out["row"], out["worst_row"] = viol, i
            out["row_rel"] = max(out["row_rel"], viol / scale)
        for j, v in enumerate(x):
            out["bound"] = max(out["bound"], self.lb[j] - v, v - self.ub[j])
            if self.vt[j] != "C": out["int"] = max(out["int"], abs(v - round(v)))
        return out
