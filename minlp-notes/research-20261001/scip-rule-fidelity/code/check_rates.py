"""End-to-end check of the objective rates w and steps t used for z_C.

If SCIP adds a cut at LP number L of node n and the cut is in a later LP of the same node, that LP
is a subset of the basis cone of LP L intersected with the cut (as long as no row of LP L was
removed and no bound relaxed), so its value is at least lpobj_L + z_cut, where
z_cut = min_{a_j > 0} w_j / a_j is the single-cut bound of the actual cut coefficients (analysis
field 'zcut').  A wrong sign or scale of w would show up as lpobj_later < lpobj_L + z_cut.
SCIPaddRow only puts the cut into the separation storage, so the later LP is taken from the next
attempt record of the same expression at the same node whose 'lpcuts' list contains this cut.

Reports: number of checked cuts, number with lpobj_next - lpobj_L >= z_cut (1 - 1e-6) - 1e-7 max(1, |lpobj_L|),
the distribution of (lpobj_next - lpobj_L) / z_cut, and the violations.
Usage: python3 check_rates.py SET ANALYSIS.jsonl [...]   (SET = mc11 | mc12 | minlplib)
"""
import sys, os, json, glob, collections
import numpy as np

st = sys.argv[1]
idxdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/index')
an = collections.defaultdict(dict)
for f in sys.argv[2:]:
    for l in open(f):
        r = json.loads(l)
        if r.get('status') == 'ok' and r.get('added') == 1 and r.get('zcut') is not None:
            an[r['inst']][r['k']] = r
checked = ok = 0; ratios = []; bad = []; nontriv = []
for inst, recs in an.items():
    X = [json.loads(l) for l in open(os.path.join(idxdir, '%s__%s.jsonl' % (st, inst)))]
    X = [x for x in X if 'outcome' in x and 'lp' in x]
    for k, r in recs.items():
        x = X[k]
        assert x['lp'] == r['lp'] and x['cons'] == r['cons'], (inst, k)
        nxt = None
        for y in X[k + 1:]:
            if y['node'] != x['node']:
                break
            if y['expr'] == x['expr'] and y['lp'] > x['lp'] and [x['over'], x['lp']] in (y.get('lpcuts') or []):
                nxt = y; break
        if nxt is None or not np.isfinite(r['zcut']) or r['zcut'] <= 0:
            continue
        gain = nxt['lpobj'] - x['lpobj']; z = r['zcut']
        checked += 1
        tol = 1e-6 * z + 1e-7 * max(1.0, abs(x['lpobj']))
        if gain >= z - tol:
            ok += 1
        else:
            bad.append(dict(inst=inst, k=k, lp=x['lp'], next_lp=nxt['lp'], gain=gain, zcut=z, mono=r.get('nmono', 0)))
        ratios.append(gain / z)
        if z > 1e-6 * max(1.0, abs(x['lpobj'])):
            nontriv.append(gain / z)
ratios = np.array(ratios)
print(st, 'cuts checked', checked, 'satisfied', ok, 'violated', len(bad))
if checked:
    print('  (lpobj_next - lpobj)/z_cut: min %.6g, quantiles 1/10/50%%: %s' % (ratios.min(), np.round(np.quantile(ratios, [0.01, 0.1, 0.5]), 4)))
nt = np.array(nontriv)
print('  nontrivial (z_cut > 1e-6 max(1, |lpobj|)):', nt.size, ('min ratio %.6g' % nt.min()) if nt.size else '')
for b in bad[:20]:
    print('  VIOLATION', json.dumps(b))
