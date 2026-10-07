"""Recheck the corner bounds z_K stored in the earlier note's exp_mccormick records against
zk_fast (which guards the antiparallel-ray cancellation found in core.two_ray).

Regenerates the HiGHS corners exactly as exp_mccormick.py does (same seeding and skips), and for
the trials present in the JSON records compares the stored zK with zk_fast and core.corner_bound.
Usage: python3 recheck_note_zK.py SEED NTRIALS RECORDS.json [p npairs nlin]"""
import os, sys, json
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)
import exp_mccormick as E
from core import corner_bound, bilinear_quadratic, qval
import zk_fast as Z

seed, T, recf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
SIZE = tuple(int(a) for a in sys.argv[4:7]) if len(sys.argv) > 6 else (4, 4, 3)
recs = {r['trial']: r for r in json.load(open(recf))['records']}
E.rng = np.random.default_rng(seed)
worst = 0.0; n = 0; nanti = 0
for trial in range(T):
    I = E.make_instance(*SIZE)
    if trial not in recs:
        continue
    h, A, bb = E.solve_lp(I)
    x, R, w, Ab, rhs, zlp = E.basis_cone(I, h, A, bb)
    p = I['p']
    viol = [(abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
    vmax, e = max(viol)
    i, j = I['pairs'][e]; idx = [i, j, p + e]
    sbar = x[idx]; side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
    Q, bq, cq = bilinear_quadratic(side); P = R[idx, :]
    wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))
    zc = corner_bound(Q, bq, cq, sbar, P, wpos)
    Qr, br, cr, sr, Pr, rho, _ = Z.reduce_space(Q, bq, cq, sbar, P)
    zf, arg = Z.zK_upto2(Qr, br, cr, sr, Pr, wpos)
    Pn = P / np.linalg.norm(P, axis=0)
    anti = int(np.sum(np.triu(Pn.T @ Pn < -1 + 1e-12, 1)))
    nanti += anti > 0
    rel = abs(zf - recs[trial]['zK']) / recs[trial]['zK']
    worst = max(worst, rel); n += 1
    if rel > 1e-6 or abs(zc - zf) > 1e-6 * zf:
        print('trial', trial, 'stored zK', recs[trial]['zK'], 'core now', zc, 'zk_fast', zf, 'support', arg, 'antiparallel pairs', anti)
print('records', n, 'corners with antiparallel projected rays', nanti, 'max rel |zk_fast - stored zK|', worst)
