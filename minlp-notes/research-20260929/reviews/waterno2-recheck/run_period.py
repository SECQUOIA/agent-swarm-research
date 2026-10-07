"""Re-bound one period of waterno2_T at the authors' multipliers with vbb2.

target = the authors' certified per-period value B_t (cert_TT_w1_impl.json).
'certified' means vbb2 proved phi_t >= B_t; otherwise the result is the
rigorous bound min(B_t, open-node bounds).
usage: python3 run_period.py T t time_limit [extra_bounds.json]
writes logs/rb_TT_pNN.json
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
import time

import vbb2

W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
T, t, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
extra_file = sys.argv[4] if len(sys.argv) > 4 else None
mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
cert = json.load(open(W2 + f"cert_{T:02d}_w1_impl.json"))
assert [[repr(float(v)) for v in l] for l in mult["lam"]] == cert["lam"]
assert repr(float(mult["mu"])) == cert["mu"] and float(mult["mu"]) >= 0
r = cert["results"][t]
assert (r["t0"], r["t1"]) == (t, t + 1) and r["status"] == "certified"
target = float(r["bound"])
lam = [[float(v) for v in l] for l in mult["lam"]]
extra = json.load(open(extra_file)) if extra_file else None
P = vbb2.PeriodF(T, t, lam, float(mult["mu"]), extra)
print(f"T={T} period {t}: {P.n0} vars, {len(P.aux)} monomials, {len(P.rows)} rows, "
      f"target {target!r}, extra bounds {extra_file}", flush=True)
tic = time.time()
res = vbb2.solve(P, target, 10**8, tl)
res.update(T=T, t=t, target=repr(target), extra=extra_file, wall=time.time() - tic)
print("RESULT", json.dumps(res), flush=True)
json.dump(res, open(f"logs/rb_{T:02d}_p{t:02d}.json", "w"), indent=1)
