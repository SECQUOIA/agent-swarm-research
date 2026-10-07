"""Exact check that MINLPLib ann_cumene_exp has the same feasible set and objective as
ann_cumene_tanh (review round 1, M1). Independent of the reviewer's cumene_twin.py.

Claim checked: the two OSIL files are identical except that every nonlinear term
negate(tanh(v)) of ann_cumene_tanh is written as 2/(exp(2v)+1) in ann_cumene_exp, with the
row's lower and upper bounds raised by exactly 1. Since -tanh(v) = 2/(exp(2v)+1) - 1 for all
real v, the two problems have the same feasible set and objective.

Method: the variables, objective, linear and quadratic coefficient blocks are compared as
serialized XML (byte equality). Row bounds are compared as exact rationals (Fraction of the
decimal strings). The structure of each nonlinear expression is compared node by node.

    python3 cumene_twin_exact.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import xml.etree.ElementTree as ET
from fractions import Fraction as F

O = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/%s.osil')
NS = {"o": "os.optimizationservices.org"}


def load(name):
    inst = ET.parse(O % name).getroot().find("o:instanceData", NS)
    return {c.tag.split("}")[1]: c for c in inst}


def tag(e):
    return e.tag.split("}")[1]


def bound(row, k):
    v = row.attrib.get(k)
    return None if v is None else F(v)


t, e = load("ann_cumene_tanh"), load("ann_cumene_exp")
assert list(t) == list(e), "different OSIL sections"
for sec in ("variables", "objectives", "linearConstraintCoefficients", "quadraticCoefficients"):
    assert ET.tostring(t[sec]) == ET.tostring(e[sec]), f"section {sec} differs"
print("variables, bounds, objective, linear and quadratic coefficients: byte-identical")

rows_t, rows_e = list(t["constraints"]), list(e["constraints"])
assert len(rows_t) == len(rows_e)
nl_t = {int(n.attrib["idx"]): n for n in t["nonlinearExpressions"]}
nl_e = {int(n.attrib["idx"]): n for n in e["nonlinearExpressions"]}
assert len(nl_t) == len(t["nonlinearExpressions"]) and len(nl_e) == len(e["nonlinearExpressions"]), "row with two nl parts"
assert set(nl_t) == set(nl_e), "nonlinear rows differ"
assert -1 not in nl_t, "objective has a nonlinear part"

for i, (a, b) in enumerate(zip(rows_t, rows_e)):
    assert a.attrib.get("name") == b.attrib.get("name")
    if i not in nl_t:
        assert a.attrib == b.attrib, ("linear row bounds differ", i)
        continue
    # tanh model: negate(tanh(variable idx=j)) with coefficient 1
    neg = nl_t[i][0]
    assert tag(neg) == "negate" and tag(neg[0]) == "tanh" and len(neg[0]) == 1
    vt = neg[0][0]
    assert tag(vt) == "variable" and F(vt.attrib.get("coef", "1")) == 1
    # exp model: divide(number 2, sum(exp(variable idx=j coef=2), number 1))
    div = nl_e[i][0]
    assert tag(div) == "divide" and len(div) == 2
    two, s = div
    assert tag(two) == "number" and F(two.attrib["value"]) == 2
    assert tag(s) == "sum" and len(s) == 2 and tag(s[0]) == "exp" and tag(s[1]) == "number"
    assert F(s[1].attrib["value"]) == 1 and len(s[0]) == 1
    ve = s[0][0]
    assert tag(ve) == "variable" and ve.attrib["idx"] == vt.attrib["idx"] and F(ve.attrib["coef"]) == 2
    # bounds: exp-model bound = tanh-model bound + 1, exactly (missing bound = infinite on both)
    for k in ("lb", "ub"):
        bt, be = bound(a, k), bound(b, k)
        assert (bt is None and be is None) or (bt is not None and be is not None and be == bt + 1), (i, k, bt, be)
    # the constant attribute, if any, must agree
    assert a.attrib.get("constant") == b.attrib.get("constant"), (i, "constant")

print(f"{len(rows_t)} rows; {len(nl_t)} rows with a nonlinear term; every one is -tanh(v) in the tanh model and "
      "2/(exp(2v)+1) in the exp model with the same variable v, and its bounds are raised by exactly 1 (exact rationals); "
      "all other rows are identical")
