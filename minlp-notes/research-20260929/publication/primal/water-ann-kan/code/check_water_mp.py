"""Cross-check of the waterno2 point files with the earlier, separately written OSIL reader
(osilx.py via ev.py), in 60-digit floating point (evidence only; the proof is the exact check).

Each symbol w_k is evaluated as the root of A w^2 + B w + C in (lo, hi); every OSIL row and
bound is evaluated at 60 digits.  Expected: violations around 1e-55 or below.

usage: python3 check_water_mp.py points/waterno2_TT.exact.json ...
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../../../..'))
import json
import sys
from fractions import Fraction as Fr

import mpmath as mp

sys.path.insert(0, _RESEARCH + "/open-instances-wave2/small")
import ev  # noqa: E402
import osilx  # noqa: E402


def q(s):
    f = Fr(s)
    return mp.mpf(f.numerator) / f.denominator


def main(path):
    mp.mp.dps = 60
    P = json.load(open(path))
    I = ev.load(P["instance"])
    W = {}
    for k, s in P["symbols"].items():
        A, B, C, lo, hi = (q(s[f]) for f in ("A", "B", "C", "lo", "hi"))
        d = mp.sqrt(B * B - 4 * A * C)
        r = [(-B + d) / (2 * A), (-B - d) / (2 * A)]
        r = [t for t in r if lo < t < hi]
        assert len(r) == 1
        W[int(k)] = r[0]
    x = []
    for nm in I["names"]:
        v = P["x"][nm]
        x.append(q(v) if isinstance(v, str) else q(v["c0"]) + q(v["c1"]) * W[int(v["w"])])
    worst, wr = mp.mpf(0), None
    for c in I["cons"]:
        v = osilx.ev_row(c, x, ev.mpnum, ev.MPFNS)
        viol = mp.mpf(0)
        if not osilx.isinf(c["lb"]):
            viol = max(viol, mp.mpf(c["lb"]) - v)
        if not osilx.isinf(c["ub"]):
            viol = max(viol, v - mp.mpf(c["ub"]))
        if viol > worst:
            worst, wr = viol, c["name"]
    bnd, bn = mp.mpf(0), None
    for j, nm in enumerate(I["names"]):
        lb, ub = I["lb"][j], I["ub"][j]
        viol = mp.mpf(0)
        if lb is not None and not osilx.isinf(lb):
            viol = max(viol, mp.mpf(lb) - x[j])
        if ub is not None and not osilx.isinf(ub):
            viol = max(viol, x[j] - mp.mpf(ub))
        if viol > bnd:
            bnd, bn = viol, nm
    f = ev.objective(I, x)
    print(f"{P['instance']}: objective (osilx, 60 digits) {mp.nstr(f, 30)}; point file {mp.nstr(q(P['objective']), 30)}; "
          f"max row violation {mp.nstr(worst, 3)} ({wr}); max bound violation {mp.nstr(bnd, 3)} ({bn})")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
