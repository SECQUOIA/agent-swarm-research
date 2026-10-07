"""Does the track's final zero box Z (from its second Krawczyk step, which used
y = stored centre outside Z) contain my validly derived enclosure Z2?
Inputs: /tmp/lnts_repro_r1/logs/Z_<N>.json and Z1_<N>.json, dumped from a /tmp
copy of the track's lnts_primal.py (the track's folder is not touched). The /tmp
copy was deleted after the run (output kept in compare_author_Z.stdout). To
regenerate: copy lnts_primal.py and osil_iv.py to /tmp/lnts_repro_r1 (with
points/ and logs/), and insert, just before the line
"# z* lies inside the exact decimal box centre +- radius ...", a dump of
[[str(x) for x in ends(Z[k])] for k in range(3)] to logs/Z_<N>.json and of
[[str(x) for x in ends(meet(K[k], X[k]))] for k in range(3)] to logs/Z1_<N>.json;
run it with arguments 50 100 200 400.
Usage: python3 compare_author_Z.py"""
import json
from fractions import Fraction as Fr

from mpmath import iv, mp

import verify_lnts_points as V
import sanity_checks as S

for N in (50, 100, 200, 400):
    st = S.setup(N)
    Vv, obj, C, names, fixedpars, zvars, cen, rad, steps, resid = st
    Xb = [V.mk(V.I(c - r)._mpi_[0], V.I(c + r)._mpi_[1]) for c, r in zip(cen, rad)]
    K, _, _ = V.krawczyk(Vv, C, steps, resid, fixedpars, zvars, [V.I(c) for c in cen], Xb)
    Z1 = [V.meet(K[k], Xb[k]) for k in range(3)]
    y2 = []
    for k in range(3):
        a, b = V.ends(Z1[k])
        m = (a + b) / 2
        y2.append(iv.mpf(mp.mpf(m.numerator) / m.denominator))
    K2, _, _ = V.krawczyk(Vv, C, steps, resid, fixedpars, zvars, y2, Z1)
    Z2 = [V.meet(K2[k], Z1[k]) for k in range(3)]
    A = [[Fr(x) for x in e] for e in json.load(open(f"/tmp/lnts_repro_r1/logs/Z_{N}.json"))]
    A1 = [[Fr(x) for x in e] for e in json.load(open(f"/tmp/lnts_repro_r1/logs/Z1_{N}.json"))]
    inA = all(A[k][0] <= V.ends(Z2[k])[0] and V.ends(Z2[k])[1] <= A[k][1] for k in range(3))
    inA1 = all(A1[k][0] <= V.ends(Z2[k])[0] and V.ends(Z2[k])[1] <= A1[k][1] for k in range(3))
    cen_in_A1 = all(A1[k][0] <= cen[k] <= A1[k][1] for k in range(3))
    # distance of the centre from the zero vs width of the track's Z
    dist = [float(abs(cen[k] - V.ends(Z2[k])[0])) for k in range(3)]
    print(f"lnts{N}: my Z2 inside track Z: {inA}; inside track step-1 box: {inA1}; "
          f"centre inside track step-1 box: {cen_in_A1}; |centre - z*| = {['%.2e' % d for d in dist]}; "
          f"track Z widths = {['%.2e' % float(a[1] - a[0]) for a in A]}")
