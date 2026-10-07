"""Do the extra implied bounds used in the runs (all bounds that full-model
propagation tightened, logs/my_implied_TT.json) constrain a period more than
the authors' implied bounds do?

For every period: root FBBT of the period subproblem with
  (A) our bounds restricted to the variables the authors tightened
      (implied_TT.json entries that differ from OSIL), and
  (B) all of our bounds (what the runs used).
Reports the largest amount by which box B is tighter than box A, relative to
the width of A.  If that is ~0, the runs certified the same subproblem as the
authors' (up to our at-least-as-tight values on their variables).
usage: python3 extra_effect.py 9 12 18 24
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys

import vbb2
from vbb2 import vbb

W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
for T in [int(a) for a in sys.argv[1:]]:
    mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
    lam = [[float(v) for v in l] for l in mult["lam"]]
    mine = json.load(open(f"logs/my_implied_{T:02d}.json"))
    I = vbb.vmodel.instance(T)
    m = I["m"]
    idx = {n: i for i, n in enumerate(m["names"])}
    theirs = json.load(open(W2 + f"implied_{T:02d}.json"))["bounds"]
    tvars = [n for n, (a, b) in theirs.items()
             if a > float(m["lb"][idx[n]]) or b < float(m["ub"][idx[n]])]
    restricted = {n: mine[n] for n in tvars}
    worst = []
    for t in range(T):
        PA = vbb2.PeriodF(T, t, lam, float(mult["mu"]), restricted)
        PB = vbb2.PeriodF(T, t, lam, float(mult["mu"]), mine)
        la, ha = PA.fbbt(PA.lo0, PA.hi0)
        lb, hb = PB.fbbt(PB.lo0, PB.hi0)
        rel, arg = 0.0, None
        for j in range(PA.n0):
            w = ha[j] - la[j]
            if not (vbb.fin(w)) or w <= 0:
                continue
            d = max(lb[j] - la[j], ha[j] - hb[j]) / w
            if d > rel:
                rel, arg = d, (PA.names[j], la[j], ha[j], lb[j], hb[j])
        worst.append((rel, t, arg))
    worst.sort(reverse=True)
    print(f"T={T}: authors' tightened variables {len(tvars)}; largest relative tightening "
          f"of B over A per period (top 3): {[(t, f'{r:.2e}') for r, t, a in worst[:3]]}")
    for r, t, a in worst[:3]:
        if r > 1e-6:
            print(f"   period {t}: {a}")
