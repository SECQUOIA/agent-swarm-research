"""Recompute numbers quoted in completion.tex from saved phase-two results."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import json
from fractions import Fraction as F
from pathlib import Path
base = Path((_PUBLIC_REPO + '/research-20261002-decomposition/completion/benchmarks'))
lanes = ['baseline','completed_grid','completed_exact','completed_recourse','completed_constraints','completed_sets']
allruns = []
for lane in lanes:
    runs = json.load(open(base/f'results/{lane}.json'))
    allruns += runs
    tot = sum(r.get('solve_subprocess_seconds', 0) + r.get('check_subprocess_seconds', 0) for r in runs)
    st = {}
    for r in runs: st[r['status']] = st.get(r['status'], 0) + 1
    valid = sum(1 for r in runs if (r.get('certificate_check') or {}).get('valid') is True)
    print(f"{lane}: runs={len(runs)} valid={valid} statuses={st} subprocess_sum={tot:.3f}")
print('total runs', len(allruns))
def show(case, method=None, lane=None, keys=()):
    for r in allruns:
        if r['case']==case and (method is None or r['method']==method) and (lane is None or r['lane']==lane):
            print(' ', r['lane'], r['case'], r['method'], r['status'], 'gap', r.get('gap'), 'solve', r.get('solve_seconds'), 'check', r.get('check_seconds'),
                  {k: (r.get('stats') or {}).get(k) for k in keys}, {k: r.get(k) for k in keys if k in r})
show('affine_star_17_shuffled', 'recourse')
show('dense_mincut_33', 'recourse')
for c in ('piecewise_convex_1','piecewise_convex_100'):
    for r in allruns:
        if r['case']==c:
            print(' ', c, r['status'], r.get('gap'), json.dumps(r.get('stats'))[:600])
for r in allruns:
    if r['lane']=='completed_constraints' and r['case'] in ('disconnected_tu_optima','large_equality_energy_full','large_equality_energy_projected'):
        print(' ', r['case'], r['method'], r['status'], r.get('gap'), json.dumps(r.get('stats'))[:500])
