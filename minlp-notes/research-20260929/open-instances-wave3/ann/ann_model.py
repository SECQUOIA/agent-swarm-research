"""Reduced-space model of ann_cumene_tanh (Schweidtmann & Mitsos 2019).

Decoding (all checked by assertions):
  * inputs: x723..x727 (the only variables with finite small boxes);
  * forward order: an equality row with exactly one unknown variable that appears
    linearly (possibly inside a tanh row  v = tanh(u)) determines it; starting from
    the inputs this determines 784 of 794 variables (all but x754, x756,
    x787..x793 and objvar);
  * the remaining rows are bilinear:
        e749: x753*x754 = x747*x748          e750: x754 + x755 + x756 + x778 = 1
        e782-e786: x746*x78k = x729*x7.. - x747*x7..
        e787: x765*x772 + x766*x792 = x760*x763     e788: x792 + x793 = 1
        e790 (objective row): objvar = linear(determined) + sum c * x746*x78k
                                       + c1 * x766*x792 + c2 * x766*x793
    Every feasible point satisfies the products  x746*x78k = RHS(e78k),
    x766*x792 = x760*x763 - x765*x772 and x766*x793 = x766 - x766*x792 (e788
    multiplied by x766).  Substituting these gives objvar = f(inputs) on the
    relaxation R obtained by dropping e749, e750 and the solvability of the
    product rows (x754, x756, x787..x793 are free and appear nowhere else).
  * constraints kept in R: all finite variable bounds of the determined
    variables and the inequality row e789 (x772 >= 0.999).
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
INPUTS = ["x723", "x724", "x725", "x726", "x727"]


def vars_of(t):
    if t is None:
        return set()
    if t[0] == "var":
        return {t[1]}
    if t[0] == "num":
        return set()
    return set().union(*[vars_of(s) for s in t[1:]])


def decode():
    I = osilx.read(os.path.join(OSIL, "ann_cumene_tanh.osil"))
    N, cons = I["names"], I["cons"]
    idx = {n: j for j, n in enumerate(N)}
    for c in cons:
        assert c["constant"] == "0"
    inputs = [idx[v] for v in INPUTS]
    box = [(Fr(I["lb"][j]), Fr(I["ub"][j])) for j in inputs]
    known = set(inputs)
    ops = []
    used = set()
    eqrows = [k for k, c in enumerate(cons) if c["lb"] == c["ub"]]
    changed = True
    while changed:
        changed = False
        for k in eqrows:
            if k in used:
                continue
            c = cons[k]
            vs = set(c["lin"]) | vars_of(c["nl"]) | {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}
            unk = vs - known
            if len(unk) != 1:
                continue
            v = unk.pop()
            if v not in c["lin"] or v in vars_of(c["nl"]) or c["quad"]:
                continue
            if c["nl"] is None:
                terms = [(o, Fr(a)) for o, a in c["lin"].items() if o != v]
                ops.append(("lin", v, Fr(c["lin"][v]), terms, Fr(c["lb"])))
            else:
                t = c["nl"]
                assert t[0] == "negate" and t[1][0] == "tanh" and t[1][1][0] == "var" and t[1][1][2] == "1", t
                assert len(c["lin"]) == 1 and c["lin"][v] == "1" and c["lb"] == "0"
                ops.append(("tanh", v, t[1][1][1]))
            known.add(v)
            used.add(k)
            changed = True
    rest = [cons[k]["name"] for k in eqrows if k not in used]
    assert sorted(rest) == sorted(["e749", "e750", "e782", "e783", "e784", "e785", "e786", "e787", "e788", "e790"]), rest
    und = sorted(N[j] for j in range(len(N)) if j not in known)
    assert und == sorted(["x754", "x756", "x787", "x788", "x789", "x790", "x791", "x792", "x793", "objvar"]), und
    # undetermined variables appear only in the rows listed above
    for v in und:
        j = idx[v]
        rows = [c["name"] for c in cons if j in c["lin"] or any(j in (a, b) for a, b, _ in c["quad"]) or j in vars_of(c["nl"])]
        assert set(rows) <= {"e749", "e750", "e782", "e783", "e784", "e785", "e786", "e787", "e788", "e790"}, (v, rows)
        if v == "objvar":
            assert I["lb"][j] == "-1e20" and I["ub"][j] == "1e20"   # dropped (relaxation)
        else:
            assert I["lb"][j] == "-INF" and I["ub"][j] == "INF"
    byname = {c["name"]: c for c in cons}
    # product definitions: P[(a,b)] = linear combination of products of determined vars
    prod = {}
    for e in ["e782", "e783", "e784", "e785", "e786"]:
        c = byname[e]
        assert not c["lin"] and c["lb"] == c["ub"] == "0" and c["nl"] is None
        q = [(a, b, Fr(cc)) for a, b, cc in c["quad"]]
        unkq = [(a, b, cc) for a, b, cc in q if a in (idx["x787"], idx["x788"], idx["x789"], idx["x790"], idx["x791"]) or
                b in (idx["x787"], idx["x788"], idx["x789"], idx["x790"], idx["x791"])]
        assert len(unkq) == 1
        a, b, cc = unkq[0]
        key = tuple(sorted((a, b)))
        # cc * x_a x_b + sum others = 0  ->  x_a x_b = -(sum others)/cc
        prod[key] = [(p, r, -c2 / cc) for p, r, c2 in q if (p, r, c2) != (a, b, cc)]
        assert all(p in known and r in known for p, r, _ in prod[key])
    c = byname["e787"]
    assert not c["lin"] and c["lb"] == c["ub"] == "0"
    q = [(a, b, Fr(cc)) for a, b, cc in c["quad"]]
    k792 = [(a, b, cc) for a, b, cc in q if idx["x792"] in (a, b)]
    assert len(k792) == 1 and set(k792[0][:2]) == {idx["x766"], idx["x792"]}
    cc = k792[0][2]
    key792 = tuple(sorted((idx["x766"], idx["x792"])))
    prod[key792] = [(p, r, -c2 / cc) for p, r, c2 in q if (p, r, c2) != k792[0]]
    c = byname["e788"]
    assert c["lin"] == {idx["x792"]: "1", idx["x793"]: "1"} and c["lb"] == c["ub"] == "1" and not c["quad"]
    key793 = tuple(sorted((idx["x766"], idx["x793"])))
    # x766*x793 = x766 - x766*x792 (e788 times x766)
    special793 = (idx["x766"], key792)
    # objective row
    c = byname["e790"]
    objv = idx["objvar"]
    assert c["lin"][objv] == "-1" and c["lb"] == c["ub"] and c["nl"] is None
    o = I["obj"]
    assert o["lin"] == {objv: "1"} and o["constant"] == "0" and not o["quad"] and o["nl"] is None and o["sense"] == "min"
    # objvar = -rhs + sum lin (others) + sum quad
    objlin = [(j, Fr(a)) for j, a in c["lin"].items() if j != objv]
    objconst = -Fr(c["lb"])
    objprod = []
    for a, b, cc in c["quad"]:
        key = tuple(sorted((a, b)))
        objprod.append((key, Fr(cc)))
        assert key in prod or key == key793
    assert all(j in known for j, _ in objlin)
    # constraints: finite bounds of determined variables, and e789
    cbounds = []
    for j in known:
        if j in inputs:
            continue
        lo = None if osilx.isinf(I["lb"][j]) else Fr(I["lb"][j])
        hi = None if osilx.isinf(I["ub"][j]) else Fr(I["ub"][j])
        if lo is not None or hi is not None:
            cbounds.append((j, lo, hi))
    ineq = [cc for cc in cons if cc["lb"] != cc["ub"]]
    assert len(ineq) == 1 and ineq[0]["name"] == "e789" and ineq[0]["lin"] == {idx["x772"]: "-1"} and ineq[0]["ub"] == "-.999"
    cbounds.append((idx["x772"], Fr("0.999"), None))
    return dict(I=I, inputs=inputs, box=box, ops=ops, prod=prod, key793=key793, special793=special793,
                objlin=objlin, objconst=objconst, objprod=objprod, cbounds=cbounds, names=N)


def evaluate_objective(D, x, num):
    """objective of R from the determined variables x (dict or list), generic number type."""
    def P(key):
        if key == D["key793"]:
            v766, k792 = D["special793"]
            return x[v766] - P(k792)
        s = num(0)
        for p, r, c in D["prod"][key]:
            s = s + num(c) * x[p] * x[r]
        return s
    f = num(D["objconst"])
    for j, a in D["objlin"]:
        f = f + num(a) * x[j]
    for key, c in D["objprod"]:
        f = f + num(c) * P(key)
    return f
