"""Exact recomputation of the certified Lagrangian sums from the authors' JSON
files: mu*rhs + sum_t B_t in Fraction arithmetic (rhs = exact decimal of the
horizon row, B_t = the stored doubles)."""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json, sys
from fractions import Fraction as F
import vmodel
W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
for T in [int(a) for a in sys.argv[1:]]:
    I = vmodel.instance(T)
    d = json.load(open(W2 + f"cert_{T:02d}_w1_impl.json"))
    mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
    assert [[repr(float(v)) for v in l] for l in mult["lam"]] == d["lam"] and repr(float(mult["mu"])) == d["mu"]
    mu = F(float(d["mu"]))
    assert mu >= 0
    assert d["windows"] == [[t, t + 1] for t in range(T)]
    assert all(r["status"] == "certified" and r["bound"] == r["target"] for r in d["results"])
    tot = mu * I["hrhs"] + sum(F(r["bound"]) for r in d["results"])
    same = tot == F(d["certified_bound_exact"])
    down9 = F(tot.numerator * 10**9 // tot.denominator, 10**9)
    print(f"T={T}: horizon rhs {I['hrhs']} ({I['hname']}), mu {float(mu)!r}, mu*rhs = {float(mu*I['hrhs']):.9f}, "
          f"sum = {float(tot):.12f}, rounded down 9 dp = {down9} = {float(down9):.9f}, "
          f"equals stored exact: {same}, stored rounded {d['certified_bound_rounded_down']}")
