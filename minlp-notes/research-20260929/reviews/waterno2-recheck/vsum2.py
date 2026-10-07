"""Exact sums of the independently re-bounded period values.

For each T, period value used:
  * the authors' B_t if vbb2 certified it (logs/rb_TT_pNN.json, status 'certified');
  * otherwise vbb2's rigorous bound min(B_t, open-node bounds) (weaker);
  * a period with no vbb2 result is reported as missing and the sum is not formed.
Sum = mu*rhs + sum_t value_t in Fraction (mu: exact float from the authors'
multiplier file; rhs: exact decimal of the horizon row), rounded down to
9 decimals.  Also recomputes the authors' sum from their JSON for comparison.
usage: python3 vsum2.py 9 12 18 24
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import os
import sys
from fractions import Fraction as F

from vbb2 import vbb

W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"


def down9(q):
    return F(q.numerator * 10**9 // q.denominator, 10**9)


for T in [int(a) for a in sys.argv[1:]]:
    I = vbb.vmodel.instance(T)
    cert = json.load(open(W2 + f"cert_{T:02d}_w1_impl.json"))
    mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
    assert [[repr(float(v)) for v in l] for l in mult["lam"]] == cert["lam"]
    mu = F(float(mult["mu"]))
    assert mu >= 0 and repr(float(mult["mu"])) == cert["mu"]
    base = mu * I["hrhs"]
    theirs = base + sum(F(r["bound"]) for r in cert["results"])
    assert theirs == F(cert["certified_bound_exact"])
    ours, missing, rows = base, [], []
    for r in cert["results"]:
        t = r["t0"]
        fn = f"logs/rb_{T:02d}_p{t:02d}.json"
        if not os.path.exists(fn):
            missing.append(t)
            rows.append((t, r["bound"], "missing", None, None, None))
            continue
        d = json.load(open(fn))
        assert d["T"] == T and d["t"] == t and float(d["target"]) == r["bound"]
        if d["status"] == "certified":
            assert F(d["bound"]) == F(r["bound"])
            v = F(r["bound"])
        else:
            v = F(d["bound"]) if d["bound"] is not None else None
            assert v is None or v <= F(r["bound"])
        if v is None:
            missing.append(t)
        else:
            ours += v
        rows.append((t, r["bound"], d["status"], None if v is None else float(v), d["nodes"], d["time"]))
    print(f"T={T}: mu*rhs = {float(base):.9f}; authors' exact sum {float(theirs):.12f} "
          f"(rounded down {float(down9(theirs)):.9f})")
    for (t, b, st, v, nd, tm) in rows:
        extra = "" if v is None else f" value used {v!r} (loss {b - v:.3e})" if st != "certified" else ""
        print(f"   period {t:2d}: authors' B_t {b!r:>22} vbb2 {st:9s} nodes {nd} time {tm if tm is None else round(tm)}s{extra}")
    if missing:
        print(f"   NOT all periods bounded (missing {missing}); no sum formed")
    else:
        print(f"   independently certified sum = {ours} = {float(ours):.12f}; rounded down "
              f"{float(down9(ours)):.9f}; equals authors' exact value: {ours == theirs}; "
              f"difference {float(theirs - ours):.3e}")
