"""Summarize r1-logs/indep_check_*.jsonl and compare with the stream's analysis (logs/an_*).
Usage: python3 summarize_indep.py"""
import os, json, glob, collections, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, '../../logs')
R = []
for f in sorted(glob.glob(os.path.join(HERE, '../r1-logs/indep_check_*.jsonl'))):
    R += [json.loads(l) for l in open(f)]
S = {}
for f in [os.path.join(LOGS, 'an_mc11.jsonl'), os.path.join(LOGS, 'an_mc12.jsonl')] + glob.glob(os.path.join(LOGS, 'an_minlplib*', '*.jsonl')):
    for l in open(f):
        r = json.loads(l)
        if 'k' in r and 'inst' in r:
            S[(r['inst'], r['k'])] = r
G = {}
for l in open(os.path.join(LOGS, 'gurobi_zk.jsonl')):
    g = json.loads(l); G[(g['inst'], g['k'])] = g

print('records', len(R), 'by set', dict(collections.Counter(r['set'] for r in R)), 'status', dict(collections.Counter(r['status'] for r in R)))
ok = [r for r in R if r['status'] in ('ok', 'allzero')]
print('in stream sample:', sum((r['inst'], r['k']) in S for r in R))
# identity of records (same lp/cons/node as stream)
bad_id = [(r['inst'], r['k']) for r in R if (r['inst'], r['k']) in S and (S[(r['inst'], r['k'])].get('lp'), S[(r['inst'], r['k'])].get('cons')) != (r['lp'], r['cons'])]
print('records whose lp/cons differ from the stream record with the same (inst,k):', bad_id[:5], len(bad_id))
print('q(sbar) vs SCIP violation: max rel diff %.2e' % max(abs(r['q_sbar'] - r['viol']) / max(abs(r['viol']), 1e-12) for r in ok))
print('G(sbar) < 0 in', sum(r['G0'] < 0 for r in ok), 'of', len(ok))
print('negative rates on corner rays (records):', sum(r['wneg'] > 0 for r in ok))
print('case agreement (tolerance rule vs SCIP):', sum(r['case_mine'] == r['case_scip'] for r in ok), 'of', len(ok),
      ' cases', dict(collections.Counter((r['case_scip'], r['kappa_scip'] != 0) for r in ok)))
print('kappa: max |k_mine - k_scip| / max(1,|k_scip|): %.2e' % max(abs(r['kappa_mine'] - r['kappa_scip']) / max(1, abs(r['kappa_scip'])) for r in ok))
# steps
tot = collections.Counter()
bycase = collections.defaultdict(collections.Counter)
for r in ok:
    tot.update(r['cmp']); bycase[r['case_scip']].update(r['cmp'])
print('step comparison (SCIP dumped t vs reviewer):', dict(tot), ' rays compared', sum(tot.values()))
for c in sorted(bycase):
    print('   case', c, dict(bycase[c]))
print('max rel diff over matching finite rays: %.2e' % max(r['maxrel_match'] for r in ok))
mm = [(r['inst'], r['k'], j, a, m) for r in ok for j, a, m in r['mismatch']]
print('mismatching rays (first 40):')
for x in mm[:40]:
    print('   ', x)
# compare with stream classification of the same rays where available
print('mismatch magnitude: min finite step among mismatches',
      min([min(a, m) for _, _, _, a, m in mm if min(a, m) > 0] or [math.nan]))
# validity along rays
v = [r['min_q_on_segments_rel'] for r in ok if 'min_q_on_segments_rel' in r]
print('validity: min over records of min q on (sbar, sbar + t_scip p) / q(sbar): %.3e; records with value < -1e-9: %d of %d'
      % (min(v), sum(x < -1e-9 for x in v), len(v)))
# z_C
zc = [(r['zC_scip'], r['zC_mine']) for r in ok if r.get('zC_scip') is not None and r.get('zC_mine') is not None and np.isfinite(r['zC_scip'])]
print('z_C (SCIP steps) vs z_C (reviewer steps): records %d, max rel diff %.2e' % (len(zc), max(abs(a - b) / max(abs(a), 1e-300) for a, b in zc)))
# z_K and classes vs stream
rows = []
for r in ok:
    s = S.get((r['inst'], r['k']))
    if s is None or s.get('status') != 'ok' or r['status'] != 'ok' or 'zK_pairs' not in r:
        continue
    scls = 'allzero' if s['wmax'] <= 0 else ('zeroface' if s.get('zeroface_meets_S') else 'ratio')
    rows.append((r, s, scls))
print('\nz_K check (n_+ <= 1, rho <= 2): records', len(rows))
print('  degeneracy class agreement:', sum((r['degenerate'] == (c == 'zeroface')) for r, s, c in rows), 'of', len(rows),
      '  disagreements:', [(r['inst'], r['k'], c, r['degenerate']) for r, s, c in rows if r['degenerate'] != (c == 'zeroface')][:10])
rat = [(r, s) for r, s, c in rows if c == 'ratio']
d = []
for r, s in rat:
    zk_s = s['zK']
    g = G.get((r['inst'], r['k']))
    if s['zK_kind'] == 'upper' and g and g.get('obj') is not None:
        zk_s = min(zk_s, g['obj'])
    zk_m = r['zK_pairs']
    d.append((abs(zk_m - zk_s) / zk_s if np.isfinite(zk_m) else math.inf, (zk_m - zk_s) / zk_s, r['inst'], r['k'], s['zK_kind'], zk_s, zk_m))
d.sort(key=lambda x: -x[0])
print('  ratio records:', len(d), ' |zK_reviewer - zK_stream|/zK_stream: median %.2e, max %.2e'
      % (np.median([x[0] for x in d]), d[0][0]))
print('  largest differences:', d[:8])
print('  reviewer z_K lower than stream (by >1e-6 rel):', sum(x[1] < -1e-6 for x in d), ' higher (>1e-6):', sum(x[1] > 1e-6 for x in d))
# ratios
rr = []
for r, s in rat:
    zc = s['zC_scip'] if s['zC_scip'] is not None else s['zC_fixed']
    zcm = r.get('zC_scip') if r.get('zC_scip') is not None else r.get('zC_mine')
    rr.append((zc / s['zK'], zcm / r['zK_pairs'] if r['zK_pairs'] and np.isfinite(r['zK_pairs']) else math.nan, r['inst'], r['k']))
dr = [abs(a - b) for a, b, _, _ in rr if np.isfinite(b)]
print('  ratio z_C/z_K: stream vs reviewer, max abs diff %.2e; reviewer ratios > 1 + 1e-6: %d' % (max(dr), sum(b > 1 + 1e-6 for _, b, _, _ in rr)))
print('  reviewer ratio stats on these records: n %d, median %.3f, <0.9 %.3f, <0.5 %.3f, =1 %.3f' % (
    len(rr), np.nanmedian([b for _, b, _, _ in rr]), np.nanmean([b < 0.9 for _, b, _, _ in rr]),
    np.nanmean([b < 0.5 for _, b, _, _ in rr]), np.nanmean([b >= 1 - 1e-6 for _, b, _, _ in rr])))
# records not in stream sample: classes
ns = [r for r in ok if (r['inst'], r['k']) not in S and r['set'] == 'minlplib']
print('\nrandom MINLPLib records outside the stream sample:', len(ns), ' degenerate (rho<=2):',
      sum(bool(r.get('degenerate')) for r in ns), ' non-degenerate:', sum(r.get('degenerate') is False for r in ns),
      ' allzero:', sum(r['status'] == 'allzero' for r in ns), ' rho>=3 unchecked:', sum(r['status'] == 'ok' and 'degenerate' not in r for r in ns))
