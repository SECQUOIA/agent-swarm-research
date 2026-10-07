"""Check zk_vec (vectorized, supports <= 2) against core.corner_bound (reference, supports
<= rank P) on random bilinear corners and on LP corners of the McCormick generator.
Usage: python3 check_zk.py SEED NRAND"""
import sys, time
import numpy as np
import mrcore as M
from core import corner_bound, bilinear_quadratic

seed, NR = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)
worst, n, tv, tr = 0.0, 0, 0.0, 0.0
MIS = []


def cmp(side, sbar, P, w, tag):
    global worst, n, tv, tr
    Q, b, c = bilinear_quadratic(side)
    t0 = time.time(); zr, lr = corner_bound(Q, b, c, sbar, P, w, return_point=True); tr += time.time() - t0
    t0 = time.time(); zv, lv = M.zk_vec(side, sbar, P, w, return_point=True); tv += time.time() - t0
    if np.isinf(zr) and np.isinf(zv):
        d = 0.0
    else:
        d = abs(zr - zv) / max(abs(zr), 1e-300)
    worst = max(worst, d); n += 1
    if d > 1e-8:
        g0 = float(sbar @ Q @ sbar + b @ sbar + c)
        qr = float('nan') if lr is None else (lambda s_: s_ @ Q @ s_ + b @ s_ + c)(sbar + P @ lr) / g0
        qv = float('nan') if lv is None else (lambda s_: s_ @ Q @ s_ + b @ s_ + c)(sbar + P @ lv) / g0
        MIS.append((tag, zr, zv, qr, qv))
        print('MISMATCH %s ref %.6g (q/q0 at ref point %.2e)  vec %.6g (q/q0 at vec point %.2e)' % (tag, zr, qr, zv, qv), flush=True)


for t in range(NR):
    side = '+' if rng.random() < 0.5 else '-'
    N = int(rng.integers(2, 31))
    while True:
        sbar = rng.normal(size=3)
        q = sbar[2] - sbar[0] * sbar[1] if side == '+' else sbar[0] * sbar[1] - sbar[2]
        if q > 1e-3:
            break
    P = rng.normal(size=(3, N)) * rng.uniform(0.1, 3, N)
    w = rng.uniform(0, 1, N) ** 3 + 1e-6
    cmp(side, sbar, P, w, 'rand%d' % t)
for k, size in enumerate([(4, 4, 3), (6, 8, 4), (8, 12, 5), (10, 20, 6)]):
    M.E.rng = np.random.default_rng(seed + 100 + k)
    for _ in range(15):
        I = M.E.make_instance(*size)
        out = M.E.solve_lp(I)
        if out is None:
            continue
        bc = M.E.basis_cone(I, *out)
        if bc is None:
            continue
        x, R, w, Ab, rhs, _ = bc
        for e, (i, j) in enumerate(I['pairs']):
            idx = [i, j, I['p'] + e]; sbar = x[idx]
            if abs(sbar[2] - sbar[0] * sbar[1]) < 1e-6:
                continue
            side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
            cmp(side, sbar, R[idx, :], M.floor_pos(w), 'lp%s' % (size,))
print('SUMMARY compared %d  max rel diff %.3e  time vec %.1fs ref %.1fs' % (n, worst, tv, tr))
tol = 1e-7
print('mismatches %d: ref point infeasible (q/q0 > %g) in %d, vec point infeasible in %d'
      % (len(MIS), tol, sum(m[3] > tol for m in MIS), sum(m[4] > tol for m in MIS)))
