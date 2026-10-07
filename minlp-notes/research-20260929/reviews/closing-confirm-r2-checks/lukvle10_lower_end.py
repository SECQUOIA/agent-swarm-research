"""Recompute lo(bound) of reviews/open-instances-verification/v_lukvle10_bnb.py from its
stored per-group lower ends (same formula, lines 298-306), at 64 and 200 bits.
The script prints mpmath.nstr(lo(bound), 16), i.e. rounded to nearest."""
import json, os
import mpmath
from mpmath import iv, mp
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "open-instances-verification")
d = json.load(open(os.path.join(V, "logs", "lukvle10_bnb.json")))
for prec in (64, 200):
    iv.prec = prec; mp.prec = prec
    tot = iv.mpf(0)
    for g in d["groups"]:
        tot += g["count"] * (iv.mpf(g["LB"]) - iv.mpf("1e-18"))
    tot += iv.mpf(d["tail"]["LB"]) - iv.mpf("1e-18")
    b = tot + iv.mpf(d["sum_lam"])  # sum_lam = nstr(lo(s), 20)
    print("prec", prec, "lo(bound) =", mpmath.nstr(b.a, 22))
mp.prec = 200
print("stored string", d["dual_bound"], "minus lo(bound) =", mpmath.nstr(mpmath.mpf(d["dual_bound"]) - b.a, 4))
