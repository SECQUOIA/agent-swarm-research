"""Profile the previous verifier's vbb.py on one period (time-limited)."""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys, json, cProfile, pstats
sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vbb
T, t, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
cert = json.load(open(W2 + f"cert_{T:02d}_w1_impl.json"))
lam = [[float(v) for v in l] for l in mult["lam"]]
P = vbb.Period(T, t, lam, float(mult["mu"]))
target = cert["results"][t]["bound"]
cProfile.run("res = vbb.solve(P, target, 10**6, tl, verbose=False)", "/tmp/prof_vbb.out")
print(res)
pstats.Stats("/tmp/prof_vbb.out").sort_stats("cumulative").print_stats(25)
