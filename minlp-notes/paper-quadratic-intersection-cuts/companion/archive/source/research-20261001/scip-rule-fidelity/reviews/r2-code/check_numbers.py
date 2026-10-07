"""Review r2: independent checks of the numbers changed in the round-1 revision (m1-m4, m8, m9).

No stream code is imported. Usage: python3 -B check_numbers.py
"""
import gzip
import json
import math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / 'logs'


def rows(p):
    return [json.loads(l) for l in open(p)]


# ---- m1/m2: Gurobi files
for name in ('gurobi_zk', 'gurobi_zk_validate', 'gurobi_zk_lowratio'):
    R = rows(LOGS / (name + '.jsonl'))
    print(name, len(R), dict(Counter(r['status'] for r in R)))
    if name == 'gurobi_zk':
        continue
    opt = [r for r in R if r['status'] == 'optimal']
    rel = [(r['obj'] - r['zK_analysis']) / r['zK_analysis'] for r in opt]
    i = int(np.argmax(np.abs(rel)))
    print('  optimal: median |rel| %.3e, max |rel| %.3e at %s k=%d (signed %.3e)'
          % (np.median(np.abs(rel)), abs(rel[i]), opt[i]['inst'], opt[i]['k'], rel[i]))
    for r in R:
        if r['status'] != 'optimal':
            d = None if r['obj'] is None else (r['obj'] - r['zK_analysis']) / r['zK_analysis']
            print('  non-optimal', r['inst'], r['k'], r['status'], r['zK_kind'], 'obj', r['obj'], 'rel', d)
    if name.endswith('lowratio'):
        print('  kinds of optimal records', Counter(r['zK_kind'] for r in opt))

# ---- ratio table, own implementation of the definition
GUR = {(g['inst'], g['k']): g for g in rows(LOGS / 'gurobi_zk.jsonl')}
allrows, norays = [], Counter()
for d in ('an_minlplib', 'an_minlplib2'):
    for p in sorted((LOGS / d).glob('*.jsonl')):
        for r in rows(p):
            if 'k' not in r:
                continue
            allrows.append(r)
            if r['status'] == 'norays':
                norays[(d, r['inst'])] += 1
print('\nm4: analysed records', len(allrows), 'status', dict(Counter(r['status'] for r in allrows)))
print('  no-ray records by sample/instance', dict(norays))

table = []
for r in allrows:
    if r['status'] != 'ok' or r['wmax'] <= 0 or r.get('zeroface_meets_S'):
        continue
    zc = r['zC_scip'] if r['zC_scip'] is not None else r['zC_fixed']
    zk, lo, kind, gst = r['zK'], None, r['zK_kind'], None
    if kind == 'upper' and (r['inst'], r['k']) in GUR:
        g = GUR[(r['inst'], r['k'])]
        gst = g['status']
        if g['obj'] is not None:
            zk = min(zk, g['obj'])
        if g['bound'] is not None and g['bound'] > 0:
            lo = min(g['bound'], zk)
            kind = 'gurobi' if zk - lo <= 1e-4 * zk else 'bracket'
    if zc is None or zk is None or not math.isfinite(zk) or zk <= 0:
        continue
    table.append(dict(inst=r['inst'], k=r['k'], r=zc / zk, hi=zc / lo if lo else None, kind=kind, gst=gst))
print('\nm1: table records', len(table), 'kinds', dict(Counter(t['kind'] for t in table)))
print('  Gurobi status among upper-kind table records', dict(Counter(t['gst'] for t in table if t['gst'])))
br = [t for t in table if t['kind'] == 'bracket']
print('  bracket records', len(br), 'max ratio (lower) %.4g, max upper estimate %r'
      % (max(t['r'] for t in br), max(t['hi'] for t in br)))
inf = [t for t in table if t['gst'] == 'infeasible']
print('  infeasible-reported records in table', len(inf), 'ratios', sorted(round(t['r'], 4) for t in inf))
print('  infeasible kinds', Counter(t['kind'] for t in inf))
lo_arr = np.array([t['r'] for t in table])
hi_arr = np.array([t['hi'] if t['kind'] == 'bracket' else t['r'] for t in table])
print('  mean shift %.6f; quartile shift' % (hi_arr.mean() - lo_arr.mean()),
      np.quantile(hi_arr, [.25, .5, .75]) - np.quantile(lo_arr, [.25, .5, .75]))
print('  below 0.5', int((lo_arr < .5).sum()), '; below 0.9', int((lo_arr < .9).sum()),
      '; 10/1067 = %.2f pp' % (100 * len(inf) / len(table)))
print('  infeasible records below 0.5: %d, below 0.9: %d' % (sum(t['r'] < .5 for t in inf), sum(t['r'] < .9 for t in inf)))
upper_left = [t for t in table if t['kind'] == 'upper']
print('  upper-kind records without any Gurobi bound in table', len(upper_left))

# ---- m3: kappa
ok = [r for r in allrows if r['status'] == 'ok']
sc = max(ok, key=lambda r: abs(r['kappa_py'] - r['kappa']) / max(1, abs(r['kappa'])))
nz = [r for r in ok if r['kappa'] != 0]
rl = max(nz, key=lambda r: abs(r['kappa_py'] - r['kappa']) / abs(r['kappa']))
print('\nm3: |dk|/max(1,|k|) max %.3e (%s k=%d kappa %r); relative max %.3e (%s k=%d kappa %r)'
      % (abs(sc['kappa_py'] - sc['kappa']) / max(1, abs(sc['kappa'])), sc['inst'], sc['k'], sc['kappa'],
         abs(rl['kappa_py'] - rl['kappa']) / abs(rl['kappa']), rl['inst'], rl['k'], rl['kappa']))

# ---- m1: waterund25 k=410 exact single-ray check with exact constant
k = -1
with gzip.open(LOGS / 'runs_minlplib/waterund25.jsonl.gz', 'rt') as f:
    for line in f:
        if line.startswith('{"v":'):
            k += 1
            if k == 410:
                rec = json.loads(line)
                break
sf = -1 if rec['over'] else 1
nq, nl = rec['nquad'], rec['nlin']
aux = rec['auxvar'] is not None
nv = nq + nl + (1 if aux else 0)
Q = {}
for i, a in enumerate(rec['qsqr']):
    if a:
        Q[(i, i)] = Q.get((i, i), F(0)) + sf * F(a)
for i, j, a in rec['bilin']:
    for key in ((i, j), (j, i)):
        Q[key] = Q.get(key, F(0)) + sf * F(a) / 2
b = [F(0)] * nv
for i, v in enumerate(rec['qlin']):
    b[i] = sf * F(v)
for i, v in enumerate(rec['lincoefs']):
    b[nq + i] = sf * F(v)
if aux:
    b[-1] = F(-sf)
    c = sf * F(rec['constant'])
else:
    c = (F(rec['constant']) - F(rec['rhs'])) if sf > 0 else (F(rec['lhs']) - F(rec['constant']))
w = [(-rt if st == 2 else rt) for st, rt in zip(rec['raystat'], rec['rayrate'])]
keep = [j for j in range(rec['nrays']) if rec['raywidth'][j] > 1e-9]
wmax = max(w[j] for j in keep)
j = keep[62]
p = {i: F(v) for i, v in rec['rays'][j]}
s = [F(x) for x in rec['zlp']]
q0 = sum(s[a] * v * s[m] for (a, m), v in Q.items()) + sum(x * y for x, y in zip(b, s)) + c
L = sum(2 * s[a] * v * p.get(m, 0) for (a, m), v in Q.items()) + sum(b[i] * x for i, x in p.items())
M = sum(p.get(a, 0) * v * p.get(m, 0) for (a, m), v in Q.items())
print('\nwaterund25 k=410: ray', j, rec['rayname'][j], 'rate', w[j], 'floor', 1e-9 * wmax, 'q0', float(q0),
      'L', float(L), 'M', float(M))
# exact smallest root bracket by bisection on rationals
assert M != 0 or L < 0
lo_t, hi_t = F(0), F(1)
qf = lambda t: q0 + L * t + M * t * t
while qf(hi_t) > 0:
    hi_t *= 2
for _ in range(80):
    mid = (lo_t + hi_t) / 2
    if qf(mid) > 0:
        lo_t = mid
    else:
        hi_t = mid
wj = F(max(w[j], 1e-9 * wmax))
print('  exact root in [%r, %r]; cost in [%.17g, %.17g]; q(hi) <= 0: %s'
      % (float(lo_t), float(hi_t), float(wj * lo_t), float(wj * hi_t), qf(hi_t) <= 0))
print('  float c vs exact c differ by', float(c - F((rec['constant'] - rec['rhs']) if sf > 0 else (rec['lhs'] - rec['constant']))) if not aux else 'aux')

# ---- m8 / m9
st, rs = Counter(), []
for pth in sorted((LOGS / 'runs_minlplib').glob('*.log')):
    t = pth.read_text()
    st['time limit' if 'time limit reached' in t else ('optimal' if 'optimal solution found' in t else 'other')] += 1
    if 'restarting after' in t:
        rs.append(pth.stem)
print('\nm8/m9: run statuses', dict(st), 'restarted', rs)
tot = sum(p.stat().st_size for p in (LOGS / 'runs_minlplib').glob('*.jsonl.gz'))
print('  gzipped dump size %.2f GB (%.2f GiB)' % (tot / 1e9, tot / 2 ** 30))
ex = [r for r in rows(LOGS / 'index/minlplib__ex1264.jsonl') if 'outcome' in r]
lps = sorted({r['lp'] for r in ex})
print('  ex1264 LPs with attempts', lps[:12], '...', lps[-3:])
before = [r for r in ex if r['lp'] <= 77]
after = [r for r in ex if r['lp'] >= 113]
print('  before: max LP', max(r['lp'] for r in before), 'max counter', max(r['exprncuts'] for r in before),
      'exprs', len({r['expr'] for r in before}))
print('  first LP after restart', min(r['lp'] for r in after), [(r['cons'], r['exprncuts'], r['expr'] in {x['expr'] for x in before})
                                                              for r in after if r['lp'] == 113])
