"""Recheck of the one-cut experiment of the sfree note (Section 9.2, exp_mccormick.py) with
the corrected corner bound.  core.corner_bound returns infeasible two-ray points when two
projected rays are collinear (check_zk.py, check_zk_scip.py); exp_mccormick.py used it for
z_K, for the cap of the orbit bisection and for the corner-optimal cut.
For each corner of the JSON records (same generator and seed), recompute z_K with zk_vec,
the orbit set with the corrected cap (fastorbit) and the corner cut, and the LP re-solve.
The single-constraint gap z1 - z_LP is taken from the records (SCIP values).
Usage: python3 recheck_mccormick.py SEED NTRIALS P NPAIRS NLIN RECORDS.json"""
import sys, json
import numpy as np
import mrcore as M
import exp_mccormick as E
from core import corner_bound, bilinear_quadratic

seed, T, p, npairs, nlin = [int(a) for a in sys.argv[1:6]]
recs = {r['trial']: r for r in json.load(open(sys.argv[6]))['records']}
E.rng = np.random.default_rng(seed)
out = []
for trial in range(T):
    I = E.make_instance(p, npairs, nlin)
    o = E.solve_lp(I)
    if o is None:
        continue
    h, A, bb = o
    bc = E.basis_cone(I, h, A, bb)
    if bc is None:
        continue
    x, R, w, Ab, rhs, zlp = bc
    viol = [(abs(x[I['p'] + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
    vmax, e = max(viol)
    if vmax < 1e-4 or trial not in recs:
        continue
    rec = recs[trial]
    i, j = I['pairs'][e]; idx = [i, j, I['p'] + e]; sbar = x[idx]
    side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
    Q, bq, cq = bilinear_quadratic(side); P = R[idx, :]
    wpos = M.floor_pos(w)
    zc, lc = corner_bound(Q, bq, cq, sbar, P, wpos, return_point=True)
    g0 = float(sbar @ Q @ sbar + bq @ sbar + cq)
    s_ = sbar + P @ lc
    core_feas = float(s_ @ Q @ s_ + bq @ s_ + cq) <= 1e-7 * g0
    zv = M.zk_vec(side, sbar, P, wpos)
    gap = rec['gap']
    _, _, F = M.FO.best_orbit(side, sbar, P, wpos, min(zv, 1e6), iters=30)
    al = M.FO.steps_A(F, side, sbar, P)
    zorb = min([wpos[q] * al[q] for q in range(len(al)) if np.isfinite(al[q])], default=np.inf)
    lp_orb = E.lp_with_cut(I, Ab, rhs, M.inv(al))
    a_ms = M.scip_alpha(side, sbar, P)
    zms = min([w[q] * a_ms[q] for q in range(len(a_ms)) if np.isfinite(a_ms[q])], default=np.inf)
    lp_cor = E.lp_with_cut(I, Ab, rhs, wpos / zv) if np.isfinite(zv) and zv > 0 else None
    fr = lambda v: None if v is None else float(min(max(v, 0.0), gap) / gap)
    r = dict(trial=trial, zK_core=zc, zK=zv, core_point_feasible=bool(core_feas),
             rel_err=float(abs(zc - zv) / zv) if np.isfinite(zv) else None,
             orbit_over_zK=float(min(zorb, zv) / zv), corner_incr=fr(zv), ms_incr=fr(min(zms, zv)),
             ms_over_zK=float(min(zms, zv) / zv), orbit_incr=fr(min(zorb, zv)),
             orbit_lp=fr(None if lp_orb is None else lp_orb - zlp), corner_lp=fr(None if lp_cor is None else lp_cor - zlp),
             old=dict((k, rec[k]) for k in ('zK', 'orbit_over_zK', 'corner_incr', 'orbit_incr', 'orbit_lp', 'corner_lp', 'ms_incr', 'ms_lp')))
    out.append(r)
    print(json.dumps(r), flush=True)

bad = [r for r in out if r['rel_err'] is not None and r['rel_err'] > 1e-6]
print('SUMMARY corners %d; core z_K wrong (rel err > 1e-6) in %d (core minimizer infeasible in %d)' % (
    len(out), len(bad), sum(not r['core_point_feasible'] for r in out)))
for k in ('ms_incr', 'corner_incr', 'orbit_incr', 'orbit_lp', 'corner_lp'):
    old = np.array([r['old'][k] for r in out if r['old'][k] is not None and r[k] is not None], float)
    new = np.array([r[k] for r in out if r['old'][k] is not None and r[k] is not None], float)
    print('  %-12s old mean %.3f median %.3f | corrected mean %.3f median %.3f' % (k, old.mean(), np.median(old), new.mean(), np.median(new)))
ms = np.array([r['old']['ms_incr'] for r in out]); ml = np.array([r['old']['ms_lp'] for r in out])
print('  SCIP set LP re-solve (unchanged): mean %.3f median %.3f' % (ml.mean(), np.median(ml)))
mz = np.array([r['ms_over_zK'] for r in out])
print('  SCIP set / corrected z_K: below 0.9 in %d, below 0.5 in %d' % (int(np.sum(mz < 0.9)), int(np.sum(mz < 0.5))))
ratio = np.array([r['orbit_over_zK'] for r in out])
print('  orbit / corrected z_K: min %.6f, corners below 0.999: %d' % (ratio.min(), int(np.sum(ratio < 0.999))))
on = np.array([r['orbit_lp'] for r in out]); sl = ml
print('  LP re-solve, orbit vs SCIP set: orbit better by > 0.01 in %d, worse by > 0.01 in %d' % (
    int(np.sum(on > sl + 0.01)), int(np.sum(on < sl - 0.01))))
