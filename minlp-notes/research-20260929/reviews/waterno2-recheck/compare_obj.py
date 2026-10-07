"""Compare the verifier's period objective (vmodel.period_objective, used by
vbb2) with the authors' rbb.Window.objective, by variable name, at the
authors' certificate multipliers.  The authors' code is only imported, not
modified (run with PYTHONDONTWRITEBYTECODE=1).
usage: python3 compare_obj.py 9 12 18
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
from fractions import Fraction as F

from vbb2 import vbb

W2 = _RESEARCH + "/open-instances-wave2/waterno2/"
sys.path.insert(0, W2)
import period  # noqa: E402  (authors' code)
import rbb     # noqa: E402  (authors' code)

for T in [int(a) for a in sys.argv[1:]]:
    mult = json.load(open(W2 + f"logs/mult_{T:02d}_w1_impl.json"))
    lam = [[float(v) for v in l] for l in mult["lam"]]
    mu = float(mult["mu"])
    D = period.setup(T)
    I = vbb.vmodel.instance(T)
    same = True
    for t in range(T):
        W = rbb.Window(D, t, t + 1)
        c = W.objective(lam, mu)
        theirs = {D["M"]["names"][v]: F(float(c[W.loc[v]])) for v in W.gv if c[W.loc[v]] != 0}
        ours = {I["m"]["names"][v]: a for v, a in vbb.vmodel.period_objective(I, t, lam, mu).items() if a != 0}
        if theirs != ours:
            same = False
            print(f"T={T} period {t}: DIFFERENT", sorted(set(theirs.items()) ^ set(ours.items()))[:6])
    print(f"T={T}: objectives identical for all periods: {same}", flush=True)
