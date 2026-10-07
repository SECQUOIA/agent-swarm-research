"""Check the authors' implied bounds (logs/implied_TT.json) with the verifier's
exact FBBT on the full model (all period rows + link rows; horizon row omitted,
which only weakens the propagation), followed by exact-bound OBBT over the
verifier's LP relaxation for the bounds FBBT does not reach.

A bound of theirs is CONFIRMED if the verifier's rigorous bound is at least as
tight.  usage: python3 vimplied.py T [obbt_rounds]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys, json, time
from fractions import Fraction as F
import numpy as np
import vbb

T = int(sys.argv[1])
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 1
P = vbb.Period(T, 0, None, None, full=True)
B = json.load(open(f"{_RESEARCH}/open-instances-wave2/waterno2/logs/implied_{T:02d}.json"))["bounds"]
idx = {n: k for k, n in enumerate(P.names)}
tic = time.time()
lo, hi = P.fbbt(P.lo0, P.hi0, 200)
print(f"FBBT done {time.time()-tic:.0f}s", flush=True)


def unconfirmed(lo, hi):
    out = []
    for n, (a, b) in B.items():
        k = idx[n]
        tl = a > P.lo0[k] and lo[k] < a      # their lower bound is an improvement not yet reached
        th = b < P.hi0[k] and hi[k] > b
        if tl or th:
            out.append((n, k, tl, th))
    return out


U = unconfirmed(lo, hi)
print("improved bounds of theirs:", sum(1 for n, (a, b) in B.items() if a > P.lo0[idx[n]] or b < P.hi0[idx[n]]),
      "not reached by exact FBBT:", len(U))
for n, k, tl, th in U:
    print(f"   {n}: theirs {B[n]}  FBBT [{lo[k]!r}, {hi[k]!r}]")
for r in range(rounds):
    if not U:
        break
    cand = [k for (n, k, tl, th) in U]
    res = P.obbt(lo, hi, cand)
    assert res is not None
    lo, hi = res
    U = unconfirmed(lo, hi)
    print(f"after exact OBBT round {r}: not reached {len(U)}  ({time.time()-tic:.0f}s)", flush=True)
    for n, k, tl, th in U:
        print(f"   {n}: theirs {B[n]}  verifier [{lo[k]!r}, {hi[k]!r}]")
# print level variables (link variables)
import vmodel
I = vmodel.instance(T)
m = I["m"]
for s, lk in enumerate(I["links"]):
    for (i, a, b) in lk:
        for v in (a, b):
            k = idx[m["names"][v]]
            print(f"level {m['names'][v]} (link {m['cons'][i]['name']}, transition {s}): osil [{m['lb'][v]}, {m['ub'][v]}]"
                  f" verifier [{lo[k]:.10f}, {hi[k]:.10f}] theirs {B.get(m['names'][v])}")
# save the verifier's own implied bounds (tighter than OSIL) for use in vbb.py
mine = {}
for k, n in enumerate(P.names[:P.n0]):
    if lo[k] > P.lo0[k] or hi[k] < P.hi0[k]:
        mine[n] = [repr(lo[k]), repr(hi[k])]
json.dump(mine, open(f"logs/my_implied_{T:02d}.json", "w"), indent=0)
print("saved", len(mine), "verifier implied bounds")
