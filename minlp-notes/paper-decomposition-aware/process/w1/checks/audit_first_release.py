"""Recompute numbers quoted in computation.tex from the saved first-release results."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import json, statistics as st
from fractions import Fraction as F
from pathlib import Path
base = Path((_PUBLIC_REPO + '/research-20261002-decomposition/solver/extra-benchmarks'))
runs = json.load(open(base/'results/results.json'))
ext = json.load(open(base/'extension-results/results.json'))
ext = ext['runs'] if isinstance(ext, dict) and 'runs' in ext else ext
print('main runs', len(runs), 'ext runs', len(ext))
methods = sorted({r['method'] for r in runs})
small = [r for r in runs if not r['case'].startswith('QPLIB')]
for m in methods:
    rs = [r for r in small if r['method']==m]
    reached = sum(1 for r in rs if r['status'] in ('certified',) or (m=='scip' and r.get('gap') is not None and float(r['gap'])<=float(F(r['epsilon']))))
    print(m, 'small configs', len(rs), 'statuses', sorted({r['status'] for r in rs}))
    print('  ', [ (r['case'], r['epsilon'], r['status'], r.get('gap')) for r in rs if r['status']!='certified'])
# certificates
certs = [r for r in runs if 'certificate_check' in r]
print('main certificates', len(certs), 'valid', sum(r['certificate_check'].get('valid') is True for r in certs))
encl = [r for r in certs if r.get('exact_reference') is not None]
print('small enclosures', len(encl), sum(bool(r.get('exact_reference_enclosed')) for r in encl))
ecerts = [r for r in ext if 'certificate_check' in r]
print('ext certificates', len(ecerts), 'valid', sum(r['certificate_check'].get('valid') is True for r in ecerts))
# matched states
pr = {(r['case'], r['epsilon']): r for r in small if r['method']=='geometric_pruned'}
up = {(r['case'], r['epsilon']): r for r in small if r['method']=='geometric_unpruned'}
print('cum states pruned', sum(r['stats']['completed_table_states'] for r in pr.values()),
      'unpruned', sum(r['stats']['completed_table_states'] for r in up.values()))
for k in sorted(pr):
    print('  ', k, pr[k]['stats']['completed_table_states'], up[k]['stats']['completed_table_states'], pr[k]['status'], up[k]['status'])
for m in ('geometric_pruned','geometric_unpruned'):
    rs = [r for r in small if r['method']==m]
    print(m, 'median solve', st.median(r['solve_wall_seconds'] for r in rs),
          'median replay', st.median(r['certificate_check_seconds'] for r in rs),
          'median subprocess', st.median(r['subprocess_wall_seconds'] for r in rs),
          'max rss', max(r['peak_process_rss_kib'] for r in rs))
print('scip small statuses', sorted([r['status'] for r in small if r['method']=='scip']))
print('sum subprocess main', sum(r['subprocess_wall_seconds'] for r in runs), 'ext', sum(r.get('subprocess_wall_seconds',0) for r in ext))
for r in ext:
    print(r.get('case'), r.get('method'), r.get('status'), r.get('gap'), r.get('solve_wall_seconds'), r.get('certificate_check_seconds'), r.get('peak_process_rss_kib'), r.get('stats',{}).get('completed_table_states'))
