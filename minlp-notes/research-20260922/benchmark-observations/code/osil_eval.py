"""Independent OSiL parser and constraint evaluator (written for the benchmark observations).

Numbers are kept as decimal strings and converted by the chosen arithmetic backend:
  - "float":  Python floats
  - "mp":     mpmath mpf at mp.dps digits
  - "exact":  sympy (Rational for data; for quadratic/linear models only)
The model is  min/max  c'x + q_obj(x) + nl_obj(x)
              s.t.     lb_r <= a_r'x + q_r(x) + nl_r(x) + const_r <= ub_r,  lbx <= x <= ubx, integrality.
"""
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

NS = "{os.optimizationservices.org}"


def _t(e):
    return e.tag.replace(NS, "")


def _expand(elparent):
    """Expand <el mult= incr=> lists into python lists of strings/ints."""
    out = []
    for el in elparent:
        mult = int(el.get("mult", "1"))
        incr = el.get("incr")
        v = el.text.strip()
        if incr is None:
            out.extend([v] * mult)
        else:
            v0, d = float(v), float(incr)
            if v0.is_integer() and d.is_integer():
                out.extend([str(int(v0) + k * int(d)) for k in range(mult)])
            else:
                raise ValueError("non-integer incr")
    return out


class Model:
    def __init__(self, path):
        root = ET.parse(path).getroot()
        d = root.find(NS + "instanceData")
        self.name = root.find(NS + "instanceHeader").find(NS + "name").text
        V = d.find(NS + "variables")
        self.vnames, self.vlb, self.vub, self.vtype = [], [], [], []
        for v in V:
            self.vnames.append(v.get("name"))
            t = v.get("type", "C")
            self.vtype.append(t)
            self.vlb.append(v.get("lb", "0"))
            self.vub.append(v.get("ub", "1" if t == "B" else "INF"))
        n = len(self.vnames)
        self.n = n
        O = d.find(NS + "objectives")
        self.objsense, self.objlin, self.objconst = "min", {}, "0"
        if O is not None:
            ob = O.find(NS + "obj")
            self.objsense = ob.get("maxOrMin", "min")
            self.objconst = ob.get("constant", "0")
            for c in ob:
                self.objlin[int(c.get("idx"))] = c.text.strip()
        C = d.find(NS + "constraints")
        self.cnames, self.clb, self.cub, self.cconst = [], [], [], []
        if C is not None:
            for c in C:
                self.cnames.append(c.get("name"))
                self.clb.append(c.get("lb", "-INF"))
                self.cub.append(c.get("ub", "INF"))
                self.cconst.append(c.get("constant", "0"))
        m = len(self.cnames)
        self.m = m
        self.lin = [dict() for _ in range(m)]
        L = d.find(NS + "linearConstraintCoefficients")
        if L is not None:
            start = [int(s) for s in _expand(L.find(NS + "start"))]
            vals = _expand(L.find(NS + "value"))
            ci = L.find(NS + "colIdx")
            if ci is not None:
                idx = [int(s) for s in _expand(ci)]
                for r in range(len(start) - 1):
                    for k in range(start[r], start[r + 1]):
                        self.lin[r][idx[k]] = vals[k]
            else:
                idx = [int(s) for s in _expand(L.find(NS + "rowIdx"))]
                for j in range(len(start) - 1):
                    for k in range(start[j], start[j + 1]):
                        self.lin[idx[k]][j] = vals[k]
        self.quad = defaultdict(list)  # row (-1 = obj) -> [(i,j,coef)]
        Q = d.find(NS + "quadraticCoefficients")
        if Q is not None:
            for q in Q:
                self.quad[int(q.get("idx"))].append(
                    (int(q.get("idxOne")), int(q.get("idxTwo")), q.get("coef", "1")))
        self.nl = {}
        N = d.find(NS + "nonlinearExpressions")
        if N is not None:
            for e in N:
                self.nl[int(e.get("idx"))] = list(e)[0]

    # ---------------- evaluation ----------------
    def _num(self, s, B):
        return B.num(s)

    def _ev(self, e, x, B):
        t = _t(e)
        ch = list(e)
        if t == "variable":
            c = e.get("coef")
            v = x[int(e.get("idx"))]
            return v if c is None else B.num(c) * v
        if t == "number":
            return B.num(e.get("value"))
        if t == "sum":
            s = B.num("0")
            for c in ch:
                s = s + self._ev(c, x, B)
            return s
        if t == "product":
            s = B.num("1")
            for c in ch:
                s = s * self._ev(c, x, B)
            return s
        a = [self._ev(c, x, B) for c in ch]
        if t == "plus": return a[0] + a[1]
        if t == "minus": return a[0] - a[1]
        if t == "times": return a[0] * a[1]
        if t == "divide": return a[0] / a[1]
        if t == "negate": return -a[0]
        if t == "square": return a[0] * a[0]
        if t == "sqrt": return B.sqrt(a[0])
        if t == "sin": return B.sin(a[0])
        if t == "cos": return B.cos(a[0])
        if t == "exp": return B.exp(a[0])
        if t == "ln" or t == "log": return B.log(a[0])
        if t == "power": return B.pow(a[0], a[1])
        if t == "signpower":  # sign(a)|a|^p
            return B.signpower(a[0], a[1])
        raise NotImplementedError(t)

    def row_value(self, r, x, B):
        """Activity of row r (r = -1: objective)."""
        s = B.num("0")
        lin = self.objlin if r == -1 else self.lin[r]
        for j, c in lin.items():
            s = s + B.num(c) * x[j]
        for i, j, c in self.quad.get(r, []):
            s = s + B.num(c) * x[i] * x[j]
        if r in self.nl:
            s = s + self._ev(self.nl[r], x, B)
        s = s + B.num(self.objconst if r == -1 else self.cconst[r])
        return s

    def objective(self, x, B):
        return self.row_value(-1, x, B)

    def check(self, x, B, tol_int=1e-9):
        """Return dict with max absolute violations (backend numbers) and argmax info."""
        res = {"bound": (B.num("0"), None), "row": (B.num("0"), None), "int": (0.0, None)}
        for j in range(self.n):
            lb, ub = self.vlb[j], self.vub[j]
            if lb != "-INF":
                v = B.num(lb) - x[j]
                if v > res["bound"][0]: res["bound"] = (v, self.vnames[j])
            if ub != "INF":
                v = x[j] - B.num(ub)
                if v > res["bound"][0]: res["bound"] = (v, self.vnames[j])
            if self.vtype[j] in ("B", "I"):
                fx = float(x[j]); v = abs(fx - round(fx))
                if v > res["int"][0]: res["int"] = (v, self.vnames[j])
        for r in range(self.m):
            a = self.row_value(r, x, B)
            if self.clb[r] != "-INF":
                v = B.num(self.clb[r]) - a
                if v > res["row"][0]: res["row"] = (v, self.cnames[r])
            if self.cub[r] != "INF":
                v = a - B.num(self.cub[r])
                if v > res["row"][0]: res["row"] = (v, self.cnames[r])
        return res


class FloatB:
    import math as _m
    num = staticmethod(lambda s: float(s) if not isinstance(s, float) else s)
    sqrt = staticmethod(_m.sqrt); sin = staticmethod(_m.sin); cos = staticmethod(_m.cos)
    exp = staticmethod(_m.exp); log = staticmethod(_m.log)
    pow = staticmethod(lambda a, b: a ** b)
    signpower = staticmethod(lambda a, p: (1 if a >= 0 else -1) * abs(a) ** p)


def mp_backend(dps=60):
    import mpmath
    mpmath.mp.dps = dps

    class MPB:
        num = staticmethod(lambda s: mpmath.mpf(s))
        sqrt = staticmethod(mpmath.sqrt); sin = staticmethod(mpmath.sin); cos = staticmethod(mpmath.cos)
        exp = staticmethod(mpmath.exp); log = staticmethod(mpmath.log)
        pow = staticmethod(lambda a, b: a ** b)
        signpower = staticmethod(lambda a, p: mpmath.sign(a) * abs(a) ** p)
    return MPB


def exact_backend():
    import sympy

    class EB:
        num = staticmethod(lambda s: sympy.Rational(s) if isinstance(s, str) else s)
        sqrt = staticmethod(sympy.sqrt); sin = staticmethod(sympy.sin); cos = staticmethod(sympy.cos)
        exp = staticmethod(sympy.exp); log = staticmethod(sympy.log)
        pow = staticmethod(lambda a, b: a ** b)
        signpower = staticmethod(lambda a, p: sympy.sign(a) * abs(a) ** p)
    return EB


if __name__ == "__main__":
    M = Model(sys.argv[1])
    print(M.name, M.n, "vars", M.m, "rows", len(M.nl), "nl", sum(len(v) for v in M.quad.values()), "qterms")
