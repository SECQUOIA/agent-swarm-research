"""Independent OSIL reader and forward propagation for the MINLPLib KAN models
(reviewer code, lit-network round 1; written from the OSiL format, not from the
author's or wave-3 code).

Given values for the Rosenbrock input variables (the variables with bounds
[-2.048, 2.048]), every other variable is computed at 60 significant digits by
repeatedly solving an equality row that has exactly one unknown appearing
affinely.  Binary one-hot groups are chosen by testing every member against the
inequality rows that link the group to known variables.  Sum-to-one rows over
continuous variables (the partition-of-unity rows) are never used to propagate;
they are only evaluated at the end.
"""
import sys
import xml.etree.ElementTree as ET
import mpmath as mp

mp.mp.dps = 60
NS = "{os.optimizationservices.org}"
INF = mp.inf


def num(s):
    return mp.mpf(s)


def expand(parent):
    """Expand <el mult incr> lists."""
    out = []
    for el in parent.findall(NS + "el"):
        mult = int(el.get("mult", "1"))
        incr = el.get("incr")
        v = el.text.strip()
        if incr is None:
            out += [v] * mult
        else:
            base, inc = mp.mpf(v), mp.mpf(incr)
            out += [str(base + k * inc) for k in range(mult)]
    return out


def read(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + "instanceData")
    V = []
    for v in d.find(NS + "variables").findall(NS + "var"):
        V.append(dict(name=v.get("name"), type=v.get("type", "C"),
                      lb=num(v.get("lb", "0")), ub=num(v.get("ub", "INF")) if v.get("ub") not in (None, "INF") else INF))
        if v.get("lb") == "-INF":
            V[-1]["lb"] = -INF
    o = d.find(NS + "objectives").find(NS + "obj")
    obj = dict(const=num(o.get("constant", "0")), lin={int(c.get("idx")): num(c.text) for c in o.findall(NS + "coef")})
    C = []
    for c in d.find(NS + "constraints").findall(NS + "con"):
        lb = c.get("lb"); ub = c.get("ub")
        C.append(dict(name=c.get("name"), lb=num(lb) if lb not in (None, "-INF") else -INF,
                      ub=num(ub) if ub not in (None, "INF") else INF, const=num(c.get("constant", "0")),
                      lin={}, quad=[], nl=None))
    L = d.find(NS + "linearConstraintCoefficients")
    if L is not None:
        start = [int(mp.nint(mp.mpf(s))) for s in expand(L.find(NS + "start"))]
        if L.find(NS + "colIdx") is not None:  # row-major
            idx = [int(mp.nint(mp.mpf(s))) for s in expand(L.find(NS + "colIdx"))]
            val = expand(L.find(NS + "value"))
            for r in range(len(start) - 1):
                for k in range(start[r], start[r + 1]):
                    C[r]["lin"][idx[k]] = C[r]["lin"].get(idx[k], 0) + num(val[k])
        else:  # column-major
            idx = [int(mp.nint(mp.mpf(s))) for s in expand(L.find(NS + "rowIdx"))]
            val = expand(L.find(NS + "value"))
            for col in range(len(start) - 1):
                for k in range(start[col], start[col + 1]):
                    C[idx[k]]["lin"][col] = C[idx[k]]["lin"].get(col, 0) + num(val[k])
    Q = d.find(NS + "quadraticCoefficients")
    if Q is not None:
        for q in Q.findall(NS + "qTerm"):
            r = int(q.get("idx")); assert r >= 0
            C[r]["quad"].append((int(q.get("idxOne")), int(q.get("idxTwo")), num(q.get("coef", "1"))))
    N = d.find(NS + "nonlinearExpressions")
    if N is not None:
        for nl in N.findall(NS + "nl"):
            r = int(nl.get("idx")); assert r >= 0 and C[r]["nl"] is None
            C[r]["nl"] = list(nl)[0]
    return V, obj, C


def tag(e):
    return e.tag.replace(NS, "")


def nlvars(e, acc):
    if tag(e) == "variable":
        acc.add(int(e.get("idx")))
    for ch in e:
        nlvars(ch, acc)
    return acc


def ev(e, x):
    t = tag(e)
    ch = list(e)
    if t == "variable":
        return num(e.get("coef", "1")) * x[int(e.get("idx"))]
    if t == "number":
        return num(e.get("value"))
    if t == "negate":
        return -ev(ch[0], x)
    if t == "divide":
        return ev(ch[0], x) / ev(ch[1], x)
    if t == "sum":
        return mp.fsum(ev(c, x) for c in ch)
    if t == "exp":
        return mp.exp(ev(ch[0], x))
    if t == "tanh":
        return mp.tanh(ev(ch[0], x))
    if t == "times":
        return ev(ch[0], x) * ev(ch[1], x)
    if t == "plus":
        return ev(ch[0], x) + ev(ch[1], x)
    if t == "minus":
        return ev(ch[0], x) - ev(ch[1], x)
    if t == "product":
        p = mp.mpf(1)
        for c in ch:
            p *= ev(c, x)
        return p
    if t == "square":
        return ev(ch[0], x) ** 2
    if t == "power":
        return ev(ch[0], x) ** ev(ch[1], x)
    if t == "ln":
        return mp.log(ev(ch[0], x))
    raise ValueError(t)


def body(c, x):
    s = c["const"] + mp.fsum(a * x[j] for j, a in c["lin"].items())
    s += mp.fsum(a * x[i] * x[j] for i, j, a in c["quad"])
    if c["nl"] is not None:
        s += ev(c["nl"], x)
    return s


def rowvars(c):
    s = set(c["lin"])
    for i, j, _ in c["quad"]:
        s.add(i); s.add(j)
    if c["nl"] is not None:
        nlvars(c["nl"], s)
    return s


def viol(c, val):
    return max(c["lb"] - val if c["lb"] != -INF else 0, val - c["ub"] if c["ub"] != INF else 0, 0)


def propagate(V, C, fixed):
    n = len(V)
    x = [None] * n
    for j, v in fixed.items():
        x[j] = v
    vs = [rowvars(c) for c in C]
    eqrows = [r for r, c in enumerate(C) if c["lb"] == c["ub"]]
    binv = {j for j, v in enumerate(V) if v["type"] in ("B", "I")}

    def is_partition(r):
        c = C[r]
        return (not c["quad"] and c["nl"] is None and c["lb"] == 1 and all(a == 1 for a in c["lin"].values())
                and not (set(c["lin"]) & binv))

    def is_onehot(r):
        c = C[r]
        return (not c["quad"] and c["nl"] is None and c["lb"] == 1 and all(a == 1 for a in c["lin"].values())
                and set(c["lin"]) <= binv)

    part = {r for r in eqrows if is_partition(r)}
    groups = [sorted(C[r]["lin"]) for r in eqrows if is_onehot(r)]
    ingroup = {j: g for g in groups for j in g}
    assert set(ingroup) == binv, "every binary is in exactly one one-hot group"
    ambiguous = []
    changed = True
    while changed:
        changed = False
        for r in eqrows:
            if r in part:
                continue
            unk = [j for j in vs[r] if x[j] is None]
            if len(unk) != 1 or unk[0] in binv:
                continue
            j = unk[0]
            c = C[r]
            if c["nl"] is not None and j in nlvars(c["nl"], set()):
                continue
            if any(i == j and k == j for i, k, _ in c["quad"]):
                continue
            x[j] = mp.mpf(0); g0 = body(c, x)
            x[j] = mp.mpf(1); g1 = body(c, x)
            x[j] = (c["lb"] - g0) / (g1 - g0)
            changed = True
        # binaries
        for g in groups:
            if x[g[0]] is not None:
                continue
            gs = set(g)
            rows = [r for r in range(len(C)) if vs[r] & gs and r not in eqrows]
            others = set().union(*[vs[r] for r in rows]) - gs
            if any(x[j] is None for j in others):
                continue
            best = []
            for k in g:
                for j in g:
                    x[j] = mp.mpf(1 if j == k else 0)
                worst = max(viol(C[r], body(C[r], x)) for r in rows)
                best.append((worst, k))
            best.sort()
            feas = [k for w, k in best if w == 0]
            if len(feas) != 1:
                ambiguous.append((g, best[:3]))
            k = best[0][1]
            for j in g:
                x[j] = mp.mpf(1 if j == k else 0)
            changed = True
    return x, part, ambiguous


def report(V, obj, C, x, part):
    assert all(v is not None for v in x), [V[j]["name"] for j, v in enumerate(x) if v is None][:10]
    f = obj["const"] + mp.fsum(a * x[j] for j, a in obj["lin"].items())
    vp = max((viol(C[r], body(C[r], x)), C[r]["name"]) for r in part) if part else (0, None)
    vo = max((viol(C[r], body(C[r], x)), C[r]["name"]) for r in range(len(C)) if r not in part)
    vb = max((max(V[j]["lb"] - x[j] if V[j]["lb"] != -INF else 0, x[j] - V[j]["ub"] if V[j]["ub"] != INF else 0, 0),
              V[j]["name"]) for j in range(len(V)))
    return f, vp, vo, vb
