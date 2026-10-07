"""Rerun egbb.py with the S.lo > 0 guard of BB.dual_value and count how often it could act.

Same arguments as egbb.py.  Before each call of BB.dual_value, this wrapper recomputes the
enclosure S of sum_obj y_k exactly as dual_value does and counts the calls with S.lo <= 0
(a superset of the calls where the guard returns -inf; the old code divided by S.lo there
when the combined value was negative).  It only reads; the search itself is unchanged.
At the end it prints the counts and the smallest S.lo and float sum seen.

    python3 check_guard.py <egbb.py arguments>
"""
import numpy as np

import egbb
import egtm
from egtm import NI

_orig = egbb.BB.dual_value
_st = dict(calls=0, sum_not_pos=0, slo_not_pos=0, min_sum=np.inf, min_slo=np.inf)


def _counted(self, n, y, tags, *rest):
    isobj = np.array([t[0] == "obj" for t in tags], dtype=bool)
    ys = y[isobj]
    _st["calls"] += 1
    s = float(ys.sum())
    if not s > 0:
        _st["sum_not_pos"] += 1          # dual_value returns -inf before the division
    else:
        slo = float(egtm.isum(NI(ys), axis=-1).lo)
        _st["min_sum"] = min(_st["min_sum"], s)
        _st["min_slo"] = min(_st["min_slo"], slo)
        if not slo > 0:
            _st["slo_not_pos"] += 1
    return _orig(self, n, y, tags, *rest)


egbb.BB.dual_value = _counted

if __name__ == "__main__":
    egbb.main()
    print(f"guard check: dual_value calls {_st['calls']}, float sum <= 0: {_st['sum_not_pos']}, "
          f"S.lo <= 0: {_st['slo_not_pos']}, smallest float sum {_st['min_sum']!r}, "
          f"smallest S.lo {_st['min_slo']!r}", flush=True)
