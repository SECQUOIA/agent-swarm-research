"""Negative control on in-scope periods: target = the authors' SCIP estimate
(value of a point feasible to SCIP's 1e-6 tolerance, 'upper_estimate' in
cert_TT_w1_impl.json) + delta.  vbb2 must not certify; its rigorous bound
should end near (at most about 1e-3 above) the estimate.
usage: python3 control_upper.py T t delta time_limit
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys

import vbb2

W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
T, t, delta, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
r = json.load(open(W2 + f"cert_{T:02d}_w1_impl.json"))["results"][t]
lam = [[float(v) for v in l] for l in mult["lam"]]
P = vbb2.PeriodF(T, t, lam, float(mult["mu"]), json.load(open(f"logs/my_implied_{T:02d}.json")))
est = r["upper_estimate"]
res = vbb2.solve(P, est + delta, 10**8, tl, verbose=False)
b = res["bound_float"]
print(f"T={T} period {t}: SCIP estimate {est!r}, target {est + delta!r} -> status {res['status']}, "
      f"bound {b!r} (bound - estimate = {b - est:.3e}), nodes {res['nodes']}, time {res['time']:.0f}s -> "
      f"{'as expected' if res['status'] != 'certified' and b - est < 1e-2 else 'UNEXPECTED'}", flush=True)
