"""Check that MINLPLib ann_cumene_exp is ann_cumene_tanh with -tanh(v) rewritten as
2/(exp(2v)+1) - 1 (the constant moved into the row bounds), using the reviewer's OSIL reader.
Compares variables, bounds, objective, linear and quadratic coefficients exactly (decimal
strings parsed at 60 digits), and the structure of every nonlinear term."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])
_PUBLIC_HOME = str(_PublicPath.home())

import sys
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/lit-network-r1'))
import mpmath as mp
import osil_eval as oe

P = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/%s.osil')
Vt, ot, Ct = oe.read(P % "ann_cumene_tanh")
Ve, oe_, Ce = oe.read(P % "ann_cumene_exp")
assert len(Vt) == len(Ve) and len(Ct) == len(Ce)
assert all(a["lb"] == b["lb"] and a["ub"] == b["ub"] and a["type"] == b["type"] for a, b in zip(Vt, Ve)), "variable bounds differ"
assert ot["lin"] == oe_["lin"] and ot["const"] == oe_["const"], "objective differs"
nl_rows = 0
for r, (a, b) in enumerate(zip(Ct, Ce)):
    assert a["lin"] == b["lin"], ("lin", r)
    assert sorted(a["quad"]) == sorted(b["quad"]), ("quad", r)
    if a["nl"] is None:
        assert b["nl"] is None and a["lb"] == b["lb"] and a["ub"] == b["ub"] and a["const"] == b["const"], ("row", r)
        continue
    nl_rows += 1
    # tanh form: negate(tanh(variable v, coef 1)); exp form: divide(2, sum(exp(variable v coef 2), 1))
    ta = a["nl"]; tb = b["nl"]
    assert oe.tag(ta) == "negate" and oe.tag(list(ta)[0]) == "tanh", ("tanh form", r)
    va = list(list(ta)[0])[0]
    assert oe.tag(va) == "variable" and va.get("coef", "1") == "1"
    assert oe.tag(tb) == "divide"
    n2, s = list(tb)
    assert oe.tag(n2) == "number" and mp.mpf(n2.get("value")) == 2 and oe.tag(s) == "sum"
    e, one = list(s)
    assert oe.tag(e) == "exp" and oe.tag(one) == "number" and mp.mpf(one.get("value")) == 1
    vb = list(e)[0]
    assert oe.tag(vb) == "variable" and mp.mpf(vb.get("coef")) == 2 and vb.get("idx") == va.get("idx"), ("arg", r)
    # -tanh(v) = 2/(exp(2v)+1) - 1, so exp-row bounds must equal tanh-row bounds + 1
    for k in ("lb", "ub"):
        assert (a[k] == b[k] == mp.inf) or (a[k] == b[k] == -mp.inf) or (a[k] + 1 == b[k]), ("bound shift", r, k, a[k], b[k])
    assert a["const"] == b["const"]
print(f"identical up to the tanh rewrite: {len(Vt)} variables, {len(Ct)} rows, {nl_rows} tanh rows; "
      "every tanh row's bounds shifted by exactly +1 in the exp model")
# spot check the identity numerically at 60 digits
for x in ("-3.7", "-0.2", "0", "1.3", "9.5"):
    x = mp.mpf(x)
    assert abs(-mp.tanh(x) - (2 / (mp.exp(2 * x) + 1) - 1)) < mp.mpf(10) ** -55
print("identity -tanh(x) = 2/(exp(2x)+1) - 1 spot-checked at 60 digits")
