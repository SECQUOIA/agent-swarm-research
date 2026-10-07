# pure relative bound differences |a-b|/|a| (a = MINLPLib bound), using cmp_camshape's parser
import sys
sys.argv = ['x']
from cmp_camshape import parse_gms, D
from fractions import Fraction as F
for N, q in (('100', '2738'), ('200', '2480'), ('400', '2703'), ('800', '3177')):
    A, loA, upA = parse_gms(D + f'minlplib/camshape{N}.gms')
    B, loB, upB = parse_gms(D + f'qplib/QPLIB_{q}.gms')
    mp = lambda v: 'objvar' if v == 'objvar' else 'x%d' % (int(v[1:]) - 1)
    loBm = {mp(v): c for v, c in loB.items()}; upBm = {mp(v): c for v, c in upB.items()}
    worst = (0, None); worst_abs = (0, None); nup = 0
    for da, db, k in ((loA, loBm, 'lo'), (upA, upBm, 'up')):
        for v, a in da.items():
            b = db[v]
            if k == 'up': nup += 1
            if a != 0:
                r = abs(a - b) / abs(a)
                if r > worst[0]: worst = (r, (v, k, float(a), float(b)))
            if abs(a - b) > worst_abs[0]: worst_abs = (abs(a - b), (v, k, float(a), float(b)))
    print(f'camshape{N}/QPLIB_{q}: {len(loA)} lower, {nup} upper bounds compared; max pure rel diff {float(worst[0]):.3e} at {worst[1]}; max abs diff {float(worst_abs[0]):.3e} at {worst_abs[1]}')
