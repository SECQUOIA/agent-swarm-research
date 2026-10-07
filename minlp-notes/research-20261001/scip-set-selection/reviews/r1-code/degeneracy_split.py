"""Review r1: recompute the Section 8.2 split (criterion at a zero-cost ray in < 50% / >= 50% of corners) from
logs/degeneracy_root.jsonl and the raw root logs (review parser)."""
import json, os, sys
from collections import defaultdict
import numpy as np
from scipy.stats import wilcoxon, spearmanr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute import parse, load_ref, LOGS
ref, tag, sense = load_ref()
deg = {d['inst']: d for d in map(json.loads, open(os.path.join(LOGS, 'degeneracy_root.jsonl')))}
R = defaultdict(dict)
for d in ('root', 'rootseeds'):
    for f in os.listdir(os.path.join(LOGS, d)):
        if f.endswith('.log'):
            r = parse(os.path.join(LOGS, d, f)); R[(r['inst'], r['seed'])][r['setting']] = r
def ok(r): return r is not None and r['status'] and 'time limit' not in r['status'] and r['rc'] == '0'
def rgc(r, i):
    sg = -1 if sense[i] == 'max' else 1
    if r['rootdb'] is None or r['firstlp'] is None: return None
    den = sg * (ref[i] - r['firstlp'])
    return None if abs(den) <= 1e-6 * max(1, abs(ref[i])) else sg * (r['rootdb'] - r['firstlp']) / den
D = {}
for i in sorted({k[0] for k in R}):
    if i not in ref or i not in deg: continue
    vals = []
    for sd in (0, 1, 2):
        sets = ['off', 'scip', 'corner', 'eff'] + (['scipS', 'cornerS', 'effS'] if sd == 0 else [])
        rs = R.get((i, sd), {})
        if not all(ok(rs.get(s)) for s in sets): break
        v = {s: rgc(rs[s], i) for s in sets}
        if None in v.values(): break
        vals.append(v)
    if len(vals) == 3:
        D[i] = {k: np.mean([v[a] - v[b] for v in vals]) for k, (a, b) in
                {'corner': ('corner', 'scip'), 'eff': ('eff', 'scip'), 'scipoff': ('scip', 'off')}.items()}
print('instances:', len(D))
for name, sel in [('<50%', lambda i: deg[i]['crit_at_zero'] < 0.5), ('>=50%', lambda i: deg[i]['crit_at_zero'] >= 0.5),
                  ('all', lambda i: True)]:
    I = [i for i in D if sel(i)]
    out = [name, len(I)]
    for k in ('corner', 'eff'):
        d = np.array([D[i][k] for i in I])
        out += ['%+.4f' % d.mean(), '%d/%d' % ((d > 0.01).sum(), (d < -0.01).sum()), '%.3g' % wilcoxon(d[np.abs(d) > 1e-9]).pvalue]
    print(*out)
I = list(D)
for k in ('corner', 'eff', 'scipoff'):
    rho, p = spearmanr([deg[i]['crit_at_zero'] for i in I], [D[i][k] for i in I])
    print('spearman crit_at_zero vs D(%s): %+.3f (p %.2g)' % (k, rho, p))
c = sum(d['corners'] for d in deg.values())
print('corners %d, criterion at zero-cost ray %.3f, all-zero %.3f, per-instance median zero_share %.2f, crit_at_zero %.2f' % (
    c, sum(d['corners'] * d['crit_at_zero'] for d in deg.values()) / c,
    sum(d['corners'] * d['allzero_share'] for d in deg.values()) / c,
    np.median([d['zero_share'] for d in deg.values()]), np.median([d['crit_at_zero'] for d in deg.values()])))
