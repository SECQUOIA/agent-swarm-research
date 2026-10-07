"""Exact upper bound on z_orbit / z_K for a corner with w = 1 (note, Section 7.3).

The vertices v_j = sbar + p_j are rounded to rationals (denominator <= DEN).  Then, in exact
arithmetic:  z_K >= z_lo  because det > 0 on T_{z_lo} = conv{sbar, sbar + z_lo p_j} (face
enumeration, exact_tools.min_det_over_simplex);  z_orbit <= z_up  by a rational positive definite
dual certificate on the vertices of T_{z_up}.  Hence z_orbit / z_K <= z_up / z_lo.  The
non-degeneracy margins of the rounded corner are computed separately by rounded_margins.py.
Usage: python3 certify_ratio.py RECORDS.jsonl [DEN]   (records with keys sbar, V)
"""
import sys
import json
from fractions import Fraction as Fr
import numpy as np
import exact_tools as ex
from minor_core import zK, FamilySolver, precondition

src = sys.argv[1]
DEN = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 4
for line in open(src):
    r = json.loads(line)
    if 'V' not in r:
        continue
    sb = tuple(Fr(x).limit_denominator(DEN) for x in r['sbar'])
    V = [tuple(Fr(x).limit_denominator(DEN) for x in v) for v in r['V']]
    P = [ex.add(v, sb, 1, -1) for v in V]
    sbn = np.array([float(x) for x in sb])
    Pn = np.array([[float(P[j][i]) for j in range(4)] for i in range(4)])
    zk = zK(sbn, Pn, np.ones(4))
    zlo = Fr(int(np.floor(zk * (1 - 1e-6) * 10 ** 8)), 10 ** 8)
    Tz = [sb] + [tuple(sb[c] + zlo * P[j][c] for c in range(4)) for j in range(4)]
    m, _ = ex.min_det_over_simplex(Tz)
    okL = m > 0
    sI, PI = precondition(sbn, Pn)
    c_, h_, _ = FamilySolver('orbit', sI, PI, np.ones(4)).best(zk, iters=40)
    zup = None
    for du in (1e-6, 1e-5, 1e-4, 1e-3):
        z = Fr(int(np.ceil((c_ + du * zk) * 10 ** 7)), 10 ** 7)
        if ex.upper_certificate(ex.ORBIT_BASIS, sb, [list(p) for p in P], [Fr(1)] * 4, z)[0]:
            zup = z
            break
    print(json.dumps(dict(start=r.get('start'), zK_numeric=zk, zK_lower_exact=str(zlo), zK_lower_ok=bool(okL),
                          orbit_numeric=c_ / zk, orbit_upper_exact=str(zup) if zup else None,
                          ratio_upper_exact=float(zup / zlo) if (zup and okL) else None)), flush=True)
