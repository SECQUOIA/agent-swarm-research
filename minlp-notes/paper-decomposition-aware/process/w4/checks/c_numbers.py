"""Independent re-derivation of Section 11 numbers from the CSV files."""
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import median

R = Path(__file__).resolve().parents[3] / 'experiments' / 'results'
rd = lambda name: list(csv.DictReader(open(R / name)))

# planted: indefiniteness and kappa bracket
nus, klb, kub, ratio = [], [], [], []
for f in ('E1_runs.csv', 'E2_runs.csv', 'E3_runs.csv', 'E5_grid_runs.csv'):
    for r in rd(f):
        nus.append(float(r['nu']))
        if int(r['kappa_target']) == 4:
            klb.append(float(r['kappa_lb'])); kub.append(float(r['kappa_ub']))
        ratio.append(float(r['kappa_ub']) / float(r['kappa_lb']))
print('min nu (=-lambda_min H):', min(nus))
print('kappa_target=4 bracket:', min(klb), max(kub), ' max ub/lb', max(ratio))

# E6 per-instance
rows = rd('E6_random_growth.csv')
inst = defaultdict(dict)
meta = {}
for r in rows:
    inst[r['name']][int(r['q'])] = r
    meta[r['name']] = (r['growth_status'], r['kind'], r['n'], r['optimality_proof'])
cert50 = [int(v[50]['max_nodes']) for k, v in inst.items() if meta[k][0] == 'certified']
oth50 = [int(v[50]['max_nodes']) for k, v in inst.items() if meta[k][0] != 'certified']
print('E6 q50 max nodes: certified', min(cert50), max(cert50), ' others', min(oth50), max(oth50), len(oth50))
changed_after_30 = [k for k, v in inst.items() if len({int(v[q]['max_nodes']) for q in (30, 40, 50)}) > 1]
print('E6 instances whose largest grid changes between q=30 and q=50:', changed_after_30)
# time column: is the max over q attained at q=50?
for (kind, n) in sorted({(m[1], m[2]) for m in meta.values()}):
    sel = [v for k, v in inst.items() if meta[k][1] == kind and meta[k][2] == n]
    allmax = max(float(x['solve_s']) for v in sel for x in v.values())
    q50max = max(float(v[50]['solve_s']) for v in sel)
    st50 = sorted({int(v[50]['stages']) for v in sel})
    st10 = sorted({int(v[10]['stages']) for v in sel})
    print(f'E6 {kind}{n}: max time all q {allmax:.3f}, at q50 {q50max:.3f}; stages q10 {st10} q50 {st50}')
# E6 largest grid range over all stages and instances
print('E6 trials>1:', sum(int(x['trials']) > 1 for v in inst.values() for x in v.values()))

# E3 separable formula at all runs and last four stages
st = rd('E3_stages.csv')
runs = {r['key']: r for r in rd('E3_runs.csv')}
by = defaultdict(list)
for r in st:
    by[r['key']].append((int(r['stage']), int(r['max_nodes_free'])))
bad = []
for k, v in by.items():
    r = runs[k]
    if r['method'] == 'unif' and int(r['kappa_target']) == 2:
        n = int(r['n'])
        f = 4 * (math.isqrt(n // 4) + 1) + 1 if n % 4 == 0 else None
        last4 = [x for _, x in sorted(v)[-4:]]
        if any(x != f for x in last4):
            bad.append((k, last4, f))
print('E3 separable uniform runs violating exact formula in last 4 stages:', bad)
# E1 path medians
st1 = rd('E1_stages.csv')
per = defaultdict(lambda: defaultdict(list))
for r in st1:
    if r['kind'] == 'path':
        per[r['method']][int(r['stage'])].append(int(r['table_states']))
for m, d in per.items():
    full = [j for j in sorted(d) if len(d[j]) == 3]
    print('E1 path', m, 'stages with 3 runs:', full[-1], 'median at last:', median(d[full[-1]]),
          ' stage4..15 range:', (min(median(d[j]) for j in full if j >= 4), max(median(d[j]) for j in full if j >= 4)) if full[-1] >= 15 else '')
