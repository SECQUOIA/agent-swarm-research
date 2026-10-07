"""Compare the sfree note's Section 9.2 corners (HiGHS basis of the McCormick LP, most violated product)
with SCIP's attempt for the same product at SCIP's first LP with an attempt.

For each record trial: regenerate the HiGHS corner exactly as exp_mccormick.py, find the SCIP attempt
for constraint bil<e> at the smallest LP number of that instance, and compare
  (a) the LP point on (x_i, x_j, w_e)  (max abs difference),
  (b) z_C/z_K of the point-rule set (SCIP's set) on both corners (HiGHS corner: scout ms_set, kappa = 0,
      z_K from zk_fast; SCIP corner: logs/an_*.jsonl).
Usage: python3 compare_first_lp.py SEED NTRIALS RECORDS.json SET [p npairs nlin]
"""
import os, sys, json
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)
import exp_mccormick as E
from core import bilinear_quadratic
from scout_sfree import ms_set, ic_bound
import zk_fast as Z

seed, T, recf, st = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
SIZE = tuple(int(a) for a in sys.argv[5:8]) if len(sys.argv) > 7 else (4, 4, 3)
LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
recs = {r['trial']: r for r in json.load(open(recf))['records']}
an = {}
for l in open(os.path.join(LOGS, 'an_%s.jsonl' % st)):
    r = json.loads(l)
    if r.get('status') == 'ok':
        an.setdefault(r['inst'], []).append(r)
E.rng = np.random.default_rng(seed)
rows = []
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
    Qr, br, cr, sr, Pr, rho, _ = Z.reduce_space(Q, bq, cq, sbar, P)
    zk, _ = Z.zK_upto2(Qr, br, cr, sr, Pr, wpos)
    G, _ = ms_set(Q, bq, cq, sbar)
    zms, _ = ic_bound(G, sbar, P, w)
    r_h = min(zms, zk) / zk
    inst = 'mc_s%d_t%03d' % (seed, trial)
    X = an.get(inst, [])
    lp0 = min((r['lp'] for r in X), default=None)
    cand = [r for r in X if r['lp'] == lp0 and r['cons'] == 'bil%d' % e]
    out = dict(trial=trial, ratio_highs=float(r_h), e=int(e))
    if cand:
        r = cand[0]
        out['ratio_scip'] = r['zC_scip'] / r['zK'] if r['zC_scip'] is not None else None
        out['scip_lp'] = lp0
        # SCIP orders the quadratic variables itself: compare as sorted triples of (x_i, x_j) and w
        out['sbar_highs'] = [float(v) for v in sbar]
    else:
        out['ratio_scip'] = None
    rows.append(out)
    print(json.dumps(out), flush=True)
# point comparison needs SCIP's zlp: read it from the dumps
import dumpio as D
for o in rows:
    if o['ratio_scip'] is None:
        continue
    inst = 'mc_s%d_t%03d' % (seed, o['trial'])
    for rec in D.records(os.path.join(LOGS, 'runs_' + st, inst + '.jsonl.gz')):
        if 'v' in rec and rec['lp'] == o['scip_lp'] and rec['cons'] == 'bil%d' % o['e']:
            zs = rec['zlp']; names = rec['vars']
            xs = [zs[k] for k, nm in enumerate(names) if nm.startswith('t_x')]
            ws = [zs[k] for k, nm in enumerate(names) if nm.startswith('t_w')]
            sh = o['sbar_highs']
            o['point_diff'] = float(max(abs(sorted(xs)[0] - sorted(sh[:2])[0]), abs(sorted(xs)[1] - sorted(sh[:2])[1]),
                                       abs(ws[0] - sh[2]))) if len(xs) == 2 and ws else None
            break
both = [o for o in rows if o['ratio_scip'] is not None]
same = [o for o in both if o.get('point_diff') is not None and o['point_diff'] <= 1e-7]
agree = [o for o in same if abs(o['ratio_scip'] - o['ratio_highs']) <= 1e-6]
print('SUMMARY', json.dumps(dict(records=len(rows), scip_attempt_found=len(both), same_point=len(same),
      same_point_ratio_agree=len(agree),
      highs_below_09=sum(o['ratio_highs'] < 0.9 for o in rows), highs_below_05=sum(o['ratio_highs'] < 0.5 for o in rows),
      scip_below_09=sum(o['ratio_scip'] < 0.9 for o in both), scip_below_05=sum(o['ratio_scip'] < 0.5 for o in both),
      ratio_diff_same_point=[round(o['ratio_scip'] - o['ratio_highs'], 4) for o in same if abs(o['ratio_scip'] - o['ratio_highs']) > 1e-6])))
