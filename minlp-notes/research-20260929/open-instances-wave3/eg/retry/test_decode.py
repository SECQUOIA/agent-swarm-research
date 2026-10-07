"""Cross-check of the decoding: at random points, every OSIL row evaluated at 50 digits by
osilx/ev (decimal-preserving, generic expression evaluator) must lie in the enclosures of the
rows computed by the bounding code (interval path egtm.Model.point and fast path
egfast.Fast.natural at a point), after mapping  row = objvar - g_k  (objective rows, with
objvar = 0) and  row = -g_k  (side rows).

    python3 test_decode.py [npoints]
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import os
import sys

import mpmath as mp
import numpy as np

import egfast

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "open-instances-wave2", "small"))
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import ev  # noqa: E402
import osilx  # noqa: E402

npts = int(sys.argv[1]) if len(sys.argv) > 1 else 10
for name in ("eg_int_s", "eg_disc_s", "eg_disc2_s"):
    F = egfast.Fast(name)
    I = ev.load(name)
    names = I["names"]
    objv = names.index("objvar")
    rng = np.random.default_rng(3)
    worst = 0.0
    bad = 0
    for _ in range(npts):
        x = F.lo_in + rng.random(F.d) * (F.hi_in - F.lo_in)
        x[F.isint] = np.round(x[F.isint])
        g1 = F.point(x[None])
        g2 = F.natural(x[None], x[None])
        xx = []
        it = iter(x)
        for j in range(len(names)):
            xx.append(mp.mpf(0) if j == objv else mp.mpf(float(next(it))))
        with mp.workdps(50):
            for k, c in enumerate(I["cons"]):
                v = osilx.ev_row(c, xx, ev.mpnum, ev.MPFNS)       # = -g_k (objvar = 0)
                gk = -v
                for G in (g1, g2):
                    lo, hi = G.lo[0, k], G.hi[0, k]
                    if not (mp.mpf(lo) <= gk <= mp.mpf(hi)):
                        bad += 1
                    worst = max(worst, float(mp.mpf(hi) - mp.mpf(lo)))
    print(f"{name}: {npts} points x 28 rows x 2 enclosures, {bad} misses, widest enclosure {worst:.2e}")
