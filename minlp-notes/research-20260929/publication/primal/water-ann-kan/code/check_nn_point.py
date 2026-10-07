"""Cross-check of a point file (points/<name>.point.json) with the earlier, separately
written OSIL reader osilx.py and evaluator ev.py (60-digit floating point; evidence only).

The interval midpoints (45 digits) and exact rationals are evaluated on every OSIL row and
bound.  Expected: rows used as definitions and unused rows hold to about 1e-44; the dropped
rows (KAN partition rows) are the only ones with visible residuals; no bound is violated; the
objective lies in the point file's enclosure up to the midpoint rounding.

usage: python3 check_nn_point.py points/<name>.point.json
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../../..'))
import json
import sys

import mpmath as mp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
import ev  # noqa: E402
import osilx  # noqa: E402  (path added by ev)

ev.MPFNS["tanh"] = mp.tanh


def main(path):
    P = json.load(open(path))
    I = ev.load(P["instance"])
    mp.mp.dps = 60
    x = []
    for nm in I["names"]:
        v = P["x"][nm]
        if isinstance(v, str):
            num, _, den = v.partition("/")
            x.append(mp.mpf(int(num)) / (int(den) if den else 1))
        else:
            x.append((mp.mpf(v["lo"]) + mp.mpf(v["hi"])) / 2)
    drop = set(P.get("dropped_rows", []))
    worst = {"kept": (mp.mpf(0), None), "dropped": (mp.mpf(0), None)}
    for c in I["cons"]:
        v = osilx.ev_row(c, x, ev.mpnum, ev.MPFNS)
        viol = mp.mpf(0)
        if not osilx.isinf(c["lb"]):
            viol = max(viol, mp.mpf(c["lb"]) - v)
        if not osilx.isinf(c["ub"]):
            viol = max(viol, v - mp.mpf(c["ub"]))
        k = "dropped" if c["name"] in drop else "kept"
        if viol > worst[k][0]:
            worst[k] = (viol, c["name"])
    bnd = (mp.mpf(0), None)
    for j, nm in enumerate(I["names"]):
        lb, ub = I["lb"][j], I["ub"][j]
        viol = mp.mpf(0)
        if lb is not None and not osilx.isinf(lb):
            viol = max(viol, mp.mpf(lb) - x[j])
        if ub is not None and not osilx.isinf(ub):
            viol = max(viol, x[j] - mp.mpf(ub))
        if viol > bnd[0]:
            bnd = (viol, nm)
    f = ev.objective(I, x)
    lo, hi = mp.mpf(P["objective_lo"]), mp.mpf(P["objective_hi"])
    print(f"{P['instance']}: objective {mp.nstr(f, 35)}; point-file enclosure [{mp.nstr(lo, 35)}, {mp.nstr(hi, 35)}]; "
          f"distance to enclosure {mp.nstr(max(lo - f, f - hi, 0), 3)}")
    print(f"   max violation, kept rows {mp.nstr(worst['kept'][0], 3)} ({worst['kept'][1]}); "
          f"dropped rows ({len(drop)}) {mp.nstr(worst['dropped'][0], 3)} ({worst['dropped'][1]}); "
          f"max bound violation {mp.nstr(bnd[0], 3)} ({bnd[1]})")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
