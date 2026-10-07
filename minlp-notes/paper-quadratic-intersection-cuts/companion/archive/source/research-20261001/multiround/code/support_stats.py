"""Support size of the corner minimizer (1 or 2 rays) for every violated term at the root LP
vertex of the cached instances, and whether the best orbit set attains z_K there.
Usage: python3 support_stats.py SIZE [SIZE ...]"""
import sys
import numpy as np
import mrcore as M
from mrloop import load

for size in sys.argv[1:]:
    cnt = {1: 0, 2: 0}; att = 0; n = 0
    for I, zlp, zbil in load('../data/inst_%s.json' % size):
        out = M.E.solve_lp(I)
        bc = None if out is None else M.E.basis_cone(I, *out)
        if bc is None:
            continue
        x, R, w, Ab, rhs, _ = bc
        for e, (i, j) in enumerate(I['pairs']):
            idx = [i, j, I['p'] + e]; sb = x[idx]
            if abs(sb[2] - sb[0] * sb[1]) < 1e-6:
                continue
            side = '+' if sb[2] > sb[0] * sb[1] else '-'
            P = R[idx, :]; wp = M.floor_pos(w)
            zk, lam = M.zk_vec(side, sb, P, wp, return_point=True)
            if not np.isfinite(zk):
                continue
            k = int(np.sum(lam > 1e-9 * max(1.0, lam.max())))
            cnt[min(k, 2)] += 1; n += 1
            al, F, _ = M.orbit_alpha(side, sb, P, wp)
            if al is not None:
                zc = min([wp[q] * al[q] for q in range(len(al)) if np.isfinite(al[q])], default=np.inf)
                att += zc >= (1 - 1e-6) * zk
    print('%s: violated root corners %d; minimizer support 1: %d, support 2: %d (%.1f%%); orbit attains z_K (rel 1e-6): %d'
          % (size, n, cnt[1], cnt[2], 100.0 * cnt[2] / max(n, 1), att), flush=True)
