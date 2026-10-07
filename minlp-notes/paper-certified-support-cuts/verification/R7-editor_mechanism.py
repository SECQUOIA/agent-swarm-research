"""R7-editor: check path-family root bounds against the analytic pair-hull bound (0).

For interleaving copies, Theorem 6.2(ii) gives value 0 for the glued pair
relaxation R in each copy, so an exact-pair-hull relaxation has root bound 0.
Compare SCIP's per-copy root bound and the fraction of the root gap that the
pair-hull bound would close with the fractions reported for the cuts.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, collections, statistics
base = (_PUBLIC_REPO + '/paper-certified-support-cuts/experiments/')
recs = []
for path in [base + 'v3/runs/partC/records.jsonl', base + 'v3d/runs/partC-rowdir/records.jsonl']:
    for line in open(path):
        r = json.loads(line)
        r['_src'] = path.split('/')[-2]
        recs.append(r)
keys = collections.Counter((r['_src'], r['mode'], r.get('phase')) for r in recs)
print(keys)
print(sorted(recs[0].keys()))

opt = {}
for r in recs:
    if r['name'] not in opt:
        c = json.load(open(base + 'v3/runs/partC/cases/' + r['name'] + '.json'))
        opt[r['name']] = c['known_optimum']
def n_of(name):
    return int(name.split('_n')[1].split('_')[0])
rows = collections.defaultdict(dict)
for r in recs:
    if r.get('phase') != 'root':
        continue
    rows[r['name']][(r['_src'], r['mode'])] = r['root_dual'] if r['root_dual'] is not None else r['dual']
print('name  opt  base_root  per_copy  frac_pair(0)  frac_frozen  frac_rowdir  frac_wide')
per_copy = []
pair_fr = collections.defaultdict(list)
for name in sorted(rows, key=lambda s: (n_of(s), s)):
    d = rows[name]; n = n_of(name); o = opt[name]
    b = d[('partC', 'baseline')]
    per_copy.append(b / n)
    fr = lambda v: (v - b) / (o - b)
    fp = fr(0.0)
    pair_fr[n].append(fp)
    print(name, round(o, 5), round(b, 3), round(b / n, 4), round(fp, 2),
          round(fr(d[('partC', 'all-diag-mech')]), 2),
          round(fr(d[('partC-rowdir', 'all-diag-mech')]), 2),
          round(fr(d[('partC-rowdir', 'all-diag-mech-wide')]), 2))
print('per-copy baseline root: min %.4f max %.4f' % (min(per_copy), max(per_copy)))
for n in sorted(pair_fr):
    vals = [rows[nm][('partC', 'baseline')] / n for nm in rows if n_of(nm) == n]
    print(n, 'median pair-hull closure %.2f' % statistics.median(pair_fr[n]), 'mean per-copy root %.4f' % statistics.mean(vals))

print('--- rerun baseline (partC-rowdir) and medians')
for src in ['partC', 'partC-rowdir']:
    allpc = []
    for n in [10, 20, 40, 80]:
        vals = [rows[nm][(src, 'baseline')] / n for nm in rows if n_of(nm) == n]
        allpc += vals
        print(src, n, 'median per-copy %.4f mean %.4f min %.4f max %.4f' % (statistics.median(vals), statistics.mean(vals), min(vals), max(vals)))
    print(src, 'overall per-copy min %.4f max %.4f' % (min(allpc), max(allpc)))
