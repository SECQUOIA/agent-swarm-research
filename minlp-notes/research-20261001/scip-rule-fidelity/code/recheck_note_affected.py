"""Recompute the earlier note's Section 9.2 quantities on the corners whose stored z_K was wrong
(core.two_ray antiparallel-ray cancellation; see recheck_note_zK.py), with z_K from zk_fast.

For each record trial: corrected zK, SCIP's set (scout ms_set) bound, best orbit bound (LMI
bisection with the corrected zK as target scale), the corner-optimal cut and the LP re-solves.
Then the summary rows of Section 9.2 are recomputed with the corrected values substituted.
Usage: python3 recheck_note_affected.py SEED NTRIALS RECORDS.json OUT.json [p npairs nlin]"""
import os, sys, json
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)
import exp_mccormick as E
from core import qval, best_orbit_bound, bilinear_quadratic
from bilinear import step_A
from scout_sfree import ms_set, ic_bound
import zk_fast as Z

seed, T, recf, outf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
SIZE = tuple(int(a) for a in sys.argv[5:8]) if len(sys.argv) > 7 else (4, 4, 3)
data = json.load(open(recf)); recs = {r['trial']: r for r in data['records']}
E.rng = np.random.default_rng(seed)
new = {}
for trial in range(T):
    I = E.make_instance(*SIZE)
    if trial not in recs:
        continue
    r = recs[trial]
    h, A, bb = E.solve_lp(I)
    x, R, w, Ab, rhs, zlp = E.basis_cone(I, h, A, bb)
    p = I['p']
    viol = [(abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
    vmax, e = max(viol)
    i, j = I['pairs'][e]; idx = [i, j, p + e]
    sbar = x[idx]; side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
    Q, bq, cq = bilinear_quadratic(side); P = R[idx, :]
    wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))
    Qr, br, cr, sr, Pr, rho, _ = Z.reduce_space(Q, bq, cq, sbar, P)
    zk, _ = Z.zK_upto2(Qr, br, cr, sr, Pr, wpos)
    if abs(zk - r['zK']) <= 1e-6 * zk:
        continue
    G, cs = ms_set(Q, bq, cq, sbar)
    zms, al_ms = ic_bound(G, sbar, P, w)
    zorb, zorb_hi, F = best_orbit_bound(side, sbar, P, wpos, min(zk, 1e6), iters=30)
    al_orb = np.array([step_A(F, side, sbar, P[:, jj]) for jj in range(P.shape[1])])
    gap = r['gap']
    fr = lambda v: None if v is None else float(min(max(v, 0.0), gap) / gap)
    inv = lambda al: np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al])
    lp_ms = E.lp_with_cut(I, Ab, rhs, inv(al_ms)); lp_orb = E.lp_with_cut(I, Ab, rhs, inv(al_orb))
    lp_cor = E.lp_with_cut(I, Ab, rhs, wpos / zk)
    rec = dict(trial=trial, zK_stored=r['zK'], zK=zk, ms_over_zK_stored=r['ms_over_zK'],
               orbit_over_zK_stored=r['orbit_over_zK'], ms_over_zK=float(min(zms, zk) / zk),
               orbit_over_zK=float(min(zorb, zk) / zk), orbit_bisect_hi_over_zK=float(zorb_hi / zk),
               ms_incr=fr(min(zms, zk)), orbit_incr=fr(min(zorb, zk)), corner_incr=fr(zk),
               ms_lp=fr(None if lp_ms is None else lp_ms - zlp), orbit_lp=fr(None if lp_orb is None else lp_orb - zlp),
               corner_lp=fr(None if lp_cor is None else lp_cor - zlp))
    for k in ('ms_incr', 'orbit_incr', 'corner_incr', 'ms_lp', 'orbit_lp', 'corner_lp'):
        rec[k + '_stored'] = r[k]
    new[trial] = rec
    print(json.dumps(rec), flush=True)
keys = ['ms_incr', 'orbit_incr', 'corner_incr', 'ms_lp', 'orbit_lp', 'corner_lp', 'ms_over_zK', 'orbit_over_zK']
summ = {'n': len(recs), 'n_corrected': len(new)}
for k in keys:
    old = np.array([r[k] for r in recs.values() if r[k] is not None], float)
    cur = np.array([(new[t][k] if t in new else r[k]) for t, r in recs.items() if r[k] is not None], float)
    summ[k] = dict(stored_mean=float(old.mean()), stored_median=float(np.median(old)),
                   corrected_mean=float(cur.mean()), corrected_median=float(np.median(cur)))
ms = np.array([(new[t]['ms_over_zK'] if t in new else r['ms_over_zK']) for t, r in recs.items()])
orb = np.array([(new[t]['orbit_over_zK'] if t in new else r['orbit_over_zK']) for t, r in recs.items()])
summ['ms_below_0.9'] = int(np.sum(ms < 0.9)); summ['ms_below_0.5'] = int(np.sum(ms < 0.5))
summ['orbit_below_0.9999'] = int(np.sum(orb < 0.9999)); summ['orbit_min'] = float(orb.min())
print('SUMMARY', json.dumps(summ))
json.dump(dict(summary=summ, corrected=new), open(outf, 'w'), indent=1)
