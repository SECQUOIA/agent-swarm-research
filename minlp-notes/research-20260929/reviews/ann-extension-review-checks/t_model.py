"""Cross-check: the verifier's decoder (annv, used by annx) and the authors' decoder (ann_model via
ann_tm) define the same relaxation R: same input box, same constraint bounds, same objective values."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
sys.dont_write_bytecode = True
import numpy as np, mpmath as mp
from fractions import Fraction as Fr
import annx
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/ann")
import ann_model as am
Dv = annx.Model().D
Da = am.decode()
print("same inputs/box:", Dv["inputs"] == Da["inputs"], Dv["box"] == Da["box"])
cv = sorted((j, lo, hi) for j, lo, hi in Dv["cb"])
ca = sorted((j, lo, hi) for j, lo, hi in Da["cbounds"])
print("same constraint bounds:", cv == ca, len(cv), len(ca))
print("same forward ops:", [tuple(o[:2]) for o in Dv["ops"]] == [tuple(o[:2]) for o in Da["ops"]] and all(
    (o[0] == "tanh" and o[2] == p[2]) or (o[0] == "lin" and o[2] == p[2] and sorted(o[3]) == sorted(p[3]) and o[4] == p[4])
    for o, p in zip(Dv["ops"], Da["ops"])))
rng = np.random.default_rng(4)
lo0 = np.array([float(a) for a, b in Dv["box"]]); hi0 = np.array([float(b) for a, b in Dv["box"]])
mx = 0
with mp.workdps(50):
    q = lambda F: mp.mpf(F.numerator) / F.denominator
    for _ in range(20):
        u = lo0 + (hi0 - lo0) * rng.random(5)
        x = annx.annv.forward_mp(Dv, [mp.mpf(float(v)) for v in u])
        fv = annx.annv.fobj(Dv, x, q)
        fa = am.evaluate_objective(Da, x, lambda c: q(Fr(c)) if not isinstance(c, (int,)) else mp.mpf(c))
        mx = max(mx, abs(fv - fa))
print("max |f_verifier - f_authors| at 20 random points (50 digits):", mp.nstr(mx, 3))
