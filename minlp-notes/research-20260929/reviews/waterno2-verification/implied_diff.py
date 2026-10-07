"""List implied bounds (authors' logs/implied_TT.json) that are tighter than the OSIL bounds."""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys, json
sys.path.insert(0, _RESEARCH + "/reviews/open-instances-verification")
import osilx
from fractions import Fraction as F
from vstruct import analyse
T = int(sys.argv[1])
m, out, sigs, order, per, rows_in, pid, links, hor = analyse(T)
pos = {c: t for t, c in enumerate(order)}
B = json.load(open(f"{_RESEARCH}/open-instances-wave2/waterno2/logs/implied_{T:02d}.json"))
idx = {n: i for i, n in enumerate(m["names"])}
cnt = 0
for n, (a, b) in B["bounds"].items():
    v = idx[n]
    lo = -10**30 if m["lb"][v].upper() == "-INF" else F(m["lb"][v])
    hi = 10**30 if m["ub"][v].upper() in ("INF", "+INF") else F(m["ub"][v])
    tl, th = F(a) > lo, F(b) < hi
    if tl or th:
        cnt += 1
        print(f"{n:6s} period {pos[pid[v]]} osil [{m['lb'][v]}, {m['ub'][v]}] implied [{a!r}, {b!r}]" + (" LO" if tl else "") + (" HI" if th else ""))
print("tighter:", cnt, "of", len(B["bounds"]))
