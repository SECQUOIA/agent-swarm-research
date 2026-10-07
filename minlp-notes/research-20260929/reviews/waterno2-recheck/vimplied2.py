"""Implied bounds for waterno2_T, derived independently of the authors' implied.py.

Model: all period rows and all link rows of the full problem (the horizon row
is left out, which only weakens the result).  Steps:
  1. outward-rounded FBBT (vbb2.PeriodF, full=True), up to 200 rounds;
  2. OBBT on the tank-3 link level variables (both ends of every transition):
     min / max of the variable over vbb.py's LP relaxation, with the bound
     evaluated exactly (Fraction) from the HiGHS dual vector; FBBT after each.
Every bound is valid for every feasible point of the full problem, so it may
be added to each period subproblem.  All bounds tighter than the OSIL bounds
are saved to logs/my_implied_TT.json.  The authors' implied bounds
(implied_TT.json) are compared: 'confirmed' = ours at least as tight.
usage: python3 vimplied2.py T [obbt_rounds]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
import time

import vbb2
from vbb2 import vbb

T = int(sys.argv[1])
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
tic = time.time()
P = vbb2.PeriodF(T, 0, None, None, full=True)
idx = {n: k for k, n in enumerate(P.names)}
I = vbb.vmodel.instance(T)
m = I["m"]
lo, hi = P.fbbt(P.lo0, P.hi0, 200)
print(f"T={T}: {P.n0} vars, {len(P.aux)} monomials, {len(P.rows)} rows; FBBT {time.time()-tic:.0f}s", flush=True)
tank3 = []
for s, lk in enumerate(I["links"]):
    (i, a, b) = lk[2]
    tank3 += [idx[m["names"][a]], idx[m["names"][b]]]
for r in range(rounds):
    res = P.obbt(lo, hi, tank3)
    assert res is not None
    lo, hi = res
    print(f"OBBT round {r} done ({time.time()-tic:.0f}s)", flush=True)
for s, lk in enumerate(I["links"]):
    for k, (i, a, b) in enumerate(lk):
        for v in (a, b):
            j = idx[m["names"][v]]
            if lo[j] > P.lo0[j] or hi[j] < P.hi0[j]:
                print(f"  transition {s} tank {k+1} {m['names'][v]}: osil [{m['lb'][v]}, {m['ub'][v]}] "
                      f"ours [{lo[j]!r}, {hi[j]!r}]")
B = json.load(open(_RESEARCH + "/open-instances-wave2/waterno2/logs/"
                   f"implied_{T:02d}.json"))["bounds"]
imp = conf = 0
for n, (a, b) in B.items():
    j = idx[n]
    for side, theirs, ours, osil in (("lo", a, lo[j], P.lo0[j]), ("hi", b, hi[j], P.hi0[j])):
        if (side == "lo" and theirs > osil) or (side == "hi" and theirs < osil):
            imp += 1
            ok = ours >= theirs if side == "lo" else ours <= theirs
            conf += ok
            print(f"  authors' {n} {side} {theirs!r}: ours {ours!r} -> {'confirmed' if ok else 'NOT reached'}")
print(f"authors' bounds tighter than OSIL: {imp}; confirmed (ours at least as tight): {conf}")
mine = {n: [repr(lo[k]), repr(hi[k])] for k, n in enumerate(P.names[:P.n0])
        if lo[k] > P.lo0[k] or hi[k] < P.hi0[k]}
json.dump(mine, open(f"logs/my_implied_{T:02d}.json", "w"), indent=0)
print(f"saved {len(mine)} bounds tighter than OSIL to logs/my_implied_{T:02d}.json ({time.time()-tic:.0f}s)")
