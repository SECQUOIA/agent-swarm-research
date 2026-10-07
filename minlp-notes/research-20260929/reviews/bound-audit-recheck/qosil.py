"""Minimal OSiL reader for linear/quadratic instances, with exact Fractions (own code for this recheck).

Scope: <variables>, one <objective> (linear part, constant, weight 1), <constraints> (lb, ub,
constant), <linearConstraintCoefficients> (row- or column-major, mult/incr expanded),
<quadraticCoefficients>. Any other instanceData child (nonlinear expressions, SOS, cones, ...)
raises an error, so a model this reader does not fully understand is rejected.

Row i value:  const_i + sum_j A[i][j] x_j + sum_(a,b,c) c x_a x_b
Objective:    obj_const + sum_j c_j x_j + sum_(a,b,c) c x_a x_b      (qTerm idx = -1)
Bounds: OSiL defaults lb = 0, ub = +INF; binaries are intersected with [0, 1].
"""
import xml.etree.ElementTree as ET
from fractions import Fraction as F

NS = "{os.optimizationservices.org}"
KNOWN = {"variables", "objectives", "constraints", "linearConstraintCoefficients", "quadraticCoefficients"}


def _bound(s, default):
    if s is None:
        return default
    s = s.strip()
    if s.lstrip("+").upper() in ("INF", "INFINITY"):
        return "+inf"
    if s.upper() in ("-INF", "-INFINITY"):
        return "-inf"
    return F(s)


def _array(node):
    out = []
    for el in node:
        assert el.tag == NS + "el", el.tag
        mult = int(el.get("mult", "1"))
        incr = F(el.get("incr", "0"))
        v = F(el.text.strip())
        out.extend(v + k * incr for k in range(mult))
    return out


class Model:
    def __init__(self, path):
        root = ET.parse(path).getroot()
        data = root.find(NS + "instanceData")
        for ch in data:
            assert ch.tag[len(NS):] in KNOWN, "unsupported OSiL element " + ch.tag
        # variables
        self.name, self.lb, self.ub, self.type = [], [], [], []
        vs = data.find(NS + "variables")
        for v in vs:
            t = v.get("type", "C")
            assert t in ("C", "B", "I"), t
            lb = _bound(v.get("lb"), F(0))
            ub = _bound(v.get("ub"), "+inf")
            assert lb != "+inf" and ub != "-inf"
            if t == "B":
                lb = F(0) if lb == "-inf" else max(lb, F(0))
                ub = F(1) if ub == "+inf" else min(ub, F(1))
            self.name.append(v.get("name"))
            self.lb.append(None if lb == "-inf" else lb)
            self.ub.append(None if ub == "+inf" else ub)
            self.type.append(t)
        self.n = len(self.name)
        assert self.n == int(vs.get("numberOfVariables"))
        self.index = {nm: j for j, nm in enumerate(self.name)}
        # objective
        objs = list(data.find(NS + "objectives"))
        assert len(objs) == 1
        ob = objs[0]
        self.sense = ob.get("maxOrMin", "min").lower()
        assert self.sense in ("min", "max")
        assert F(ob.get("weight", "1")) == 1
        self.obj_const = F(ob.get("constant", "0"))
        self.obj_lin = {}
        for c in ob:
            assert c.tag == NS + "coef"
            j = int(c.get("idx"))
            self.obj_lin[j] = self.obj_lin.get(j, F(0)) + F(c.text.strip())
        # constraints
        self.cname, self.clb, self.cub, self.cconst = [], [], [], []
        cs = data.find(NS + "constraints")
        for c in (cs if cs is not None else []):
            lb = _bound(c.get("lb"), "-inf")
            ub = _bound(c.get("ub"), "+inf")
            self.cname.append(c.get("name"))
            self.clb.append(None if lb == "-inf" else lb)
            self.cub.append(None if ub == "+inf" else ub)
            self.cconst.append(F(c.get("constant", "0")))
        self.m = len(self.cname)
        # linear coefficients
        self.A = [dict() for _ in range(self.m)]
        lc = data.find(NS + "linearConstraintCoefficients")
        if lc is not None:
            start = [int(s) for s in _array(lc.find(NS + "start"))]
            val = _array(lc.find(NS + "value"))
            assert len(val) == int(lc.get("numberOfValues"))
            if lc.find(NS + "rowIdx") is not None:  # column-major
                idx = [int(s) for s in _array(lc.find(NS + "rowIdx"))]
                assert len(start) == self.n + 1
                for j in range(self.n):
                    for k in range(start[j], start[j + 1]):
                        self.A[idx[k]][j] = self.A[idx[k]].get(j, F(0)) + val[k]
            else:  # row-major
                idx = [int(s) for s in _array(lc.find(NS + "colIdx"))]
                assert len(start) == self.m + 1
                for i in range(self.m):
                    for k in range(start[i], start[i + 1]):
                        self.A[i][idx[k]] = self.A[i].get(idx[k], F(0)) + val[k]
        # quadratic terms
        self.Q = [[] for _ in range(self.m)]
        self.obj_Q = []
        qc = data.find(NS + "quadraticCoefficients")
        if qc is not None:
            terms = list(qc)
            assert len(terms) == int(qc.get("numberOfQuadraticTerms"))
            for q in terms:
                i = int(q.get("idx"))
                t = (int(q.get("idxOne")), int(q.get("idxTwo")), F(q.get("coef", "1")))
                (self.obj_Q if i == -1 else self.Q[i]).append(t)

    # ------------------------------------------------------------ exact evaluation
    def row(self, i, x):
        v = self.cconst[i]
        for j, a in self.A[i].items():
            v += a * x[j]
        for a, b, c in self.Q[i]:
            v += c * x[a] * x[b]
        return v

    def objective(self, x):
        v = self.obj_const
        for j, a in self.obj_lin.items():
            v += a * x[j]
        for a, b, c in self.obj_Q:
            v += c * x[a] * x[b]
        return v

    def violations(self, x):
        """Exact list of (amount > 0, kind, name) over all rows, bounds and integrality."""
        out = []
        for j in range(self.n):
            if self.lb[j] is not None and x[j] < self.lb[j]:
                out.append((self.lb[j] - x[j], "lb", self.name[j]))
            if self.ub[j] is not None and x[j] > self.ub[j]:
                out.append((x[j] - self.ub[j], "ub", self.name[j]))
            if self.type[j] in ("B", "I") and x[j].denominator != 1:
                out.append((abs(x[j] - round(x[j])), "int", self.name[j]))
        for i in range(self.m):
            r = self.row(i, x)
            if self.clb[i] is not None and r < self.clb[i]:
                out.append((self.clb[i] - r, "row lb", self.cname[i]))
            if self.cub[i] is not None and r > self.cub[i]:
                out.append((r - self.cub[i], "row ub", self.cname[i]))
        return out


def read_sol(path, M):
    """MINLPLib .sol file ('name value' lines). Returns (x, missing names, unknown names)."""
    x = [None] * M.n
    unknown = []
    for line in open(path):
        p = line.split()
        if len(p) < 2 or p[0].startswith("#"):
            continue
        if p[0] in M.index:
            x[M.index[p[0]]] = F(p[1])
        else:
            unknown.append(p[0])
    missing = [M.name[j] for j in range(M.n) if x[j] is None]
    return x, missing, unknown
