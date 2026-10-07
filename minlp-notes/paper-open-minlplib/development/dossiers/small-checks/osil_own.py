"""Own minimal OSIL reader/evaluator (ElementTree), independent of osilx.py/common.py."""
import xml.etree.ElementTree as ET
NS = "{os.optimizationservices.org}"
def _t(e): return e.tag.replace(NS, "")
def _els(node):
    out = []
    for el in node:
        mult = int(el.get("mult", "1")); incr = el.get("incr")
        v = el.text.strip()
        if incr is None:
            out += [v] * mult
        else:
            base = int(v); inc = int(incr)
            out += [str(base + k * inc) for k in range(mult)]
    return out
def read(path):
    r = ET.parse(path).getroot()
    vs = r.find(f".//{NS}variables")
    names, lb, ub = [], [], []
    for v in vs:
        names.append(v.get("name")); lb.append(v.get("lb", "0")); ub.append(v.get("ub", "INF"))
    obj = r.find(f".//{NS}obj")
    olin = {int(c.get("idx")): c.text.strip() for c in obj.findall(f"{NS}coef")}
    cons = [dict(name=c.get("name"), lb=c.get("lb", "-INF"), ub=c.get("ub", "INF"), const=c.get("constant", "0"))
            for c in r.find(f".//{NS}constraints")]
    lin = [dict() for _ in cons]
    L = r.find(f".//{NS}linearConstraintCoefficients")
    if L is not None:
        start = [int(s) for s in _els(L.find(f"{NS}start"))]
        idxnode = L.find(f"{NS}colIdx")
        assert idxnode is not None, "row-wise storage expected"
        cols = [int(s) for s in _els(idxnode)]
        vals = _els(L.find(f"{NS}value"))
        for i in range(len(cons)):
            for k in range(start[i], start[i + 1]):
                lin[i][cols[k]] = vals[k]
    nl = {}
    N = r.find(f".//{NS}nonlinearExpressions")
    if N is not None:
        for e in N:
            nl[int(e.get("idx"))] = list(e)[0]
    return dict(names=names, lb=lb, ub=ub, sense=obj.get("maxOrMin"), oconst=obj.get("constant", "0"),
                olin=olin, cons=cons, lin=lin, nl=nl)
def ev(e, x, num, fns):
    t = _t(e)
    if t == "variable":
        return num(e.get("coef", "1")) * x[int(e.get("idx"))]
    if t == "number": return num(e.get("value"))
    ch = [ev(c, x, num, fns) for c in e]
    if t == "sum":
        s = ch[0]
        for c in ch[1:]: s = s + c
        return s
    if t == "product":
        s = ch[0]
        for c in ch[1:]: s = s * c
        return s
    if t == "negate": return -ch[0]
    if t == "minus": return ch[0] - ch[1]
    if t == "plus": return ch[0] + ch[1]
    if t == "times": return ch[0] * ch[1]
    if t == "divide": return ch[0] / ch[1]
    if t == "square": return ch[0] * ch[0]
    if t == "power":
        b, p = e[0], e[1]
        if _t(p) == "number" and p.get("value") in ("2", "3", "4"):
            r = ch[0]
            for _ in range(int(p.get("value")) - 1): r = r * ch[0]
            return r
        return fns["exp"](ch[1] * fns["log"](ch[0]))
    if t in ("ln", "log"): return fns["log"](ch[0])
    if t == "exp": return fns["exp"](ch[0])
    if t == "cos": return fns["cos"](ch[0])
    if t == "sqrt": return fns["sqrt"](ch[0])
    raise ValueError(t)
def objective(m, x, num, fns):
    s = num(m["oconst"])
    for j, c in m["olin"].items(): s = s + num(c) * x[j]
    if -1 in m["nl"]: s = s + ev(m["nl"][-1], x, num, fns)
    return s
def row(m, i, x, num, fns):
    s = num(m["cons"][i]["const"])
    for j, c in m["lin"][i].items(): s = s + num(c) * x[j]
    if i in m["nl"]: s = s + ev(m["nl"][i], x, num, fns)
    return s
