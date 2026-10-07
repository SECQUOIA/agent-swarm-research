"""Markdown table of the check_dump.py results (logs/dumps/*.check.json)."""
import json, glob, sys, os
D = sys.argv[1] if len(sys.argv) > 1 else '.'
print('| dump | corners | decomposition error | max rel. diff alpha (SCIP lambda / chosen / final cut) | C steps longer than exact | S-freeness violations (samples / rays) | z_K checked (spurious) | z_C > z_K | changed | median gain | mean z_C/z_K SCIP / chosen | reach z_K SCIP / chosen | final-cut rays < 0.9 exact step |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
tot = dict(c=0, sv=0, rv=0, zv=0, ov=0, short=0, rays=0)
for f in sorted(glob.glob(os.path.join(D, '*.check.json'))):
    d = json.load(open(f))
    g = d['rel_gain']['median']
    zs, zl = d['zC_over_zK_scip']['mean'], d['zC_over_zK_sel']['mean']
    print('| %s | %d | %.0e | %.0e / %.0e / %.0e | %d | %d / %d | %d (%d) | %d | %d | %s | %s | %s | %d / %d |' % (
        os.path.basename(f).replace('.check.json', ''), d['corners'], d['decomp_max'], d['alpha0_maxrel'],
        d['alpha_maxrel'], d['final_maxrel'], d['overshoot'], d['sfree_viol'], d['ray_viol'], d['zk_checked'],
        d.get('zk_spurious', 0), d['zk_viol'], d['changed'], '%.3f' % g if g else '-',
        '%.3f / %.3f' % (zs, zl) if zs is not None else '-',
        '%s / %s' % (d.get('reach_zK_scip'), d.get('reach_zK_sel')) if zs is not None else '-',
        d.get('rays_short10', 0), d.get('rays_compared', 0)))
    tot['c'] += d['corners']; tot['sv'] += d['sfree_viol']; tot['rv'] += d['ray_viol']; tot['zv'] += d['zk_viol']
    tot['ov'] += d['overshoot']; tot['short'] += d.get('rays_short10', 0); tot['rays'] += d.get('rays_compared', 0)
print('\nTotals: %(c)d corners, %(sv)d sampled S-freeness violations, %(rv)d ray violations, %(zv)d z_C > z_K, '
      '%(ov)d C steps longer than the exact step, %(short)d of %(rays)d final-cut rays shorter than 0.9 x exact.' % tot)
