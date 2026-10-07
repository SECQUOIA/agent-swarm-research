"""Compare fastorbit.best_orbit (Clarabel direct) with the original cvxpy implementation
core.best_orbit_bound on LP corners of the 6x8 McCormick generator (all violated terms).
Usage: python3 check_fastorbit.py SEED NINST"""
import sys, time
import numpy as np
import fastorbit as FO
import exp_mccormick as E
from core import corner_bound, best_orbit_bound, bilinear_quadratic
from bilinear import step_A

seed, NI = int(sys.argv[1]), int(sys.argv[2])
E.rng = np.random.default_rng(seed)
worst_cert, worst_coef, n, t_old, t_new = 0.0, 0.0, 0, 0.0, 0.0
for k in range(NI):
    I = E.make_instance(6, 8, 4)
    out = E.solve_lp(I)
    if out is None:
        continue
    bc = E.basis_cone(I, *out)
    if bc is None:
        continue
    x, R, w, Ab, rhs, _ = bc
    for e, (i, j) in enumerate(I['pairs']):
        idx = [i, j, I['p'] + e]; sbar = x[idx]
        if abs(sbar[2] - sbar[0] * sbar[1]) < 1e-6:
            continue
        side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
        Q, bq, cq = bilinear_quadratic(side); P = R[idx, :]
        wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))
        zk = corner_bound(Q, bq, cq, sbar, P, wpos)
        t0 = time.time(); c_old, _, F_old = best_orbit_bound(side, sbar, P, wpos, min(zk, 1e6), iters=25); t_old += time.time() - t0
        t0 = time.time(); c_new, _, F_new = FO.best_orbit(side, sbar, P, wpos, min(zk, 1e6), iters=25); t_new += time.time() - t0
        a_old = np.array([0 if not np.isfinite(t) else 1 / t for t in [step_A(F_old, side, sbar, P[:, q]) for q in range(P.shape[1])]])
        a_new = np.array([0 if not np.isfinite(t) else 1 / t for t in FO.steps_A(F_new, side, sbar, P)])
        rc = abs(c_old - c_new) / max(abs(zk), 1e-12)
        ra = np.abs(a_old - a_new).max() / max(np.abs(a_old).max(), 1e-12)
        worst_cert, worst_coef, n = max(worst_cert, rc), max(worst_coef, ra), n + 1
        print('inst %d term %d zK %.6g old %.6g new %.6g |dcoef|/|coef| %.2e' % (k, e, zk, c_old, c_new, ra), flush=True)
print('SUMMARY corners %d  max |cert diff|/zK %.3e  max rel coef diff %.3e  time old %.1fs new %.1fs'
      % (n, worst_cert, worst_coef, t_old, t_new))
