"""Review r2: independent recomputation of the full-solve tables (logs/full, logs/full_stock).

Own parser; imports nothing from the stream code. Usage (from the stream dir):
  python3 reviews/r2-code/recompute_stock.py [total|last]
'total' uses total nodes over restarts (default), 'last' the first number of 'Solving Nodes'.
"""
import math, re, sys, statistics
from pathlib import Path
from scipy.stats import wilcoxon

BASE = Path(__file__).resolve().parents[2]
NODEMODE = sys.argv[1] if len(sys.argv) > 1 else 'total'
TL = 300.0
INST = (BASE / 'logs/testset_full.txt').read_text().split()
assert len(INST) == 60


def num(pat, txt, cast=float):
    m = re.search(pat, txt, re.M)
    return cast(m.group(1)) if m else None


def parse(path):
    t = path.read_text(errors='replace')
    r = {}
    r['rc'] = num(r'^@@ wallclock \S+ returncode (\S+)', t, str)
    r['wall'] = num(r'^@@ wallclock (\S+)', t)
    r['status'] = num(r'^SCIP Status\s*: (.*)$', t, str)
    r['time'] = num(r'^Solving Time \(sec\)\s*: (\S+)', t)
    m = re.search(r'^Solving Nodes\s*: (\d+)(?: \(total of (\d+) nodes)?', t, re.M)
    r['nodes'] = None if not m else float(m.group(2) if (NODEMODE == 'total' and m.group(2)) else m.group(1))
    r['primal'] = num(r'^Primal Bound\s*: (\S+)', t)
    r['dual'] = num(r'^Dual Bound\s*: (\S+)', t)
    r['firstlp'] = num(r'^  First LP value\s*: (\S+)', t)
    r['rootdual'] = num(r'^  Final Dual Bound\s*: (\S+)', t)
    m = re.search(r'^  dual LP\s*:\s*\S+\s+(\d+)\s+(\d+)', t, re.M)
    r['duallp'] = (int(m.group(1)), int(m.group(2))) if m else None
    m = re.search(r'^  primal LP\s*:\s*\S+\s+(\d+)\s+(\d+)', t, re.M)
    r['primallp'] = (int(m.group(1)), int(m.group(2))) if m else None
    r['error'] = bool(re.search(r'^\s*\[.*\] ERROR|^ERROR', t, re.M)) or 'ERROR' in t
    r['solved'] = bool(r['status'] and 'optimal solution found' in r['status'])
    return r


SET = {'off': ('full', 'off'), 'scip': ('full', 'scip'), 'corner': ('full', 'corner'),
       'eff': ('full', 'eff'), 'stock': ('full_stock', 'scip')}
D = {}
for s, (d, name) in SET.items():
    for i in INST:
        for sd in (1, 2):
            p = BASE / 'logs' / d / f'{i}.{name}.s{sd}.log'
            D[s, i, sd] = parse(p)

# reference values
solu = {}
for l in (BASE / 'sources/minlplib.solu').read_text().splitlines():
    f = l.split()
    if len(f) >= 3 and f[0] in ('=opt=', '=best='):
        solu[f[1]] = (f[0], float(f[2]))


def sgm(vals, shift):
    return math.exp(math.fsum(math.log(v + shift) for v in vals) / len(vals)) - shift


def cpu(r):
    return r['time'] if r['solved'] else TL


out = []
P = out.append
P('# Review r2 recomputation of full-solve tables (own parser, node mode %s)\n' % NODEMODE)
for s in SET:
    rs = [D[s, i, sd] for i in INST for sd in (1, 2)]
    rcs = {}
    for r in rs:
        rcs[r['rc']] = rcs.get(r['rc'], 0) + 1
    P(f'{s}: runs {len(rs)} solved {sum(r["solved"] for r in rs)} timelimit '
      f'{sum(bool(r["status"]) and "time limit" in r["status"] for r in rs)} rc {rcs} '
      f'missing-status {sum(r["status"] is None for r in rs)}')
P('')

ALL = list(SET)
nodepairs = [(i, sd) for i in INST for sd in (1, 2) if all(D[s, i, sd]['nodes'] is not None for s in ALL)]
P(f'node pairs with nodes in all settings: {len(nodepairs)}; missing: '
  f'{[(i, sd) for i in INST for sd in (1, 2) if (i, sd) not in nodepairs]}\n')

P('| seed | setting | solved/runs | CPU sgm | nodes sgm | common-solved (5 settings) | CPU sgm there | nodes sgm there |')
P('|---|---|---|---|---|---|---|---|')
for seeds in ((1,), (2,), (1, 2)):
    pairs = [(i, sd) for i in INST for sd in seeds]
    common = [p for p in pairs if all(D[s, p[0], p[1]]['solved'] for s in ALL)]
    for s in ('off', 'stock', 'scip', 'corner', 'eff'):
        rs = [D[s, i, sd] for i, sd in pairs]
        np_ = [p for p in pairs if p in nodepairs]
        P(f'| {"+".join(map(str, seeds))} | {s} | {sum(r["solved"] for r in rs)}/{len(rs)} | '
          f'{sgm([cpu(r) for r in rs], 1):.3f} | {sgm([D[s, i, sd]["nodes"] for i, sd in np_], 100):.1f} | '
          f'{len(common)} | {sgm([D[s, i, sd]["time"] for i, sd in common], 1):.3f} | '
          f'{sgm([D[s, i, sd]["nodes"] for i, sd in common], 100):.1f} |')
P('')

# excluding ex5_4_2 s1
pairs = [(i, sd) for i in INST for sd in (1, 2) if (i, sd) != ('ex5_4_2', 1)]
for s in ('off', 'stock', 'scip'):
    rs = [D[s, i, sd] for i, sd in pairs]
    P(f'excl ex5_4_2 s1: {s} solved {sum(r["solved"] for r in rs)}/{len(rs)} CPU sgm {sgm([cpu(r) for r in rs], 1):.3f}')
P('')

# solved-set differences
for a, b in (('stock', 'off'), ('stock', 'scip')):
    pa = [(i, sd) for i in INST for sd in (1, 2) if D[a, i, sd]['solved'] and not D[b, i, sd]['solved']]
    pb = [(i, sd) for i in INST for sd in (1, 2) if D[b, i, sd]['solved'] and not D[a, i, sd]['solved']]
    P(f'{a} only vs {b}: ' + ', '.join(f'{i} s{sd} ({D[a, i, sd]["time"]} s, {D[a, i, sd]["nodes"]:.0f} nodes)' for i, sd in pa))
    P(f'{b} only vs {a}: ' + ', '.join(f'{i} s{sd} ({D[b, i, sd]["time"]} s, {D[b, i, sd]["nodes"]} nodes; {a} status {D[a, i, sd]["status"]}, {D[a, i, sd]["nodes"]} nodes)' for i, sd in pb))
P('')


def ratio_test(x, y, subset, key, shift):
    pairs = [(i, sd) for i, sd in subset]
    vals = []
    for i, sd in pairs:
        vx = cpu(D[x, i, sd]) if key == 'cpu' else D[x, i, sd]['nodes']
        vy = cpu(D[y, i, sd]) if key == 'cpu' else D[y, i, sd]['nodes']
        vals.append((i, math.log((vx + shift) / (vy + shift))))
    ratio = math.exp(math.fsum(v for _, v in vals) / len(vals))
    per = {}
    for i, v in vals:
        per.setdefault(i, []).append(v)
    avg = [sum(v) / len(v) for v in per.values()]
    nz = [a for a in avg if a != 0]
    p = wilcoxon(nz).pvalue if len(nz) >= 10 else None
    return ratio, len(per), len(nz), p


allp = [(i, sd) for i in INST for sd in (1, 2)]
common = [p for p in allp if all(D[s, p[0], p[1]]['solved'] for s in ALL)]
for x, y in (('stock', 'off'), ('scip', 'stock'), ('scip', 'off')):
    r1 = ratio_test(x, y, allp, 'cpu', 1)
    r2 = ratio_test(x, y, common, 'cpu', 1)
    r3 = ratio_test(x, y, common, 'nodes', 100)
    both = [p for p in allp if D[x, p[0], p[1]]['solved'] and D[y, p[0], p[1]]['solved']]
    r4 = ratio_test(x, y, both, 'cpu', 1)
    r5 = ratio_test(x, y, both, 'nodes', 100)
    P(f'{x} vs {y}: all-pair CPU ratio {r1[0]:.4f} p {r1[3]} (n inst {r1[1]}, nonzero {r1[2]}); '
      f'common CPU {r2[0]:.4f} p {r2[3]}; common nodes {r3[0]:.4f} p {r3[3]} (nonzero {r3[2]}); '
      f'pair-solved n {len(both)} CPU {r4[0]:.4f} p {r4[3]} nodes {r5[0]:.4f} p {r5[3]} (nonzero {r5[2]})')
excl = [p for p in allp if p != ('ex5_4_2', 1)]
r = ratio_test('stock', 'off', excl, 'cpu', 1)
P(f'stock vs off excl ex5_4_2 s1: CPU ratio {r[0]:.4f} p {r[3]}')
# per-seed stock vs off
for sd in (1, 2):
    sub = [(i, sd) for i in INST]
    r = ratio_test('stock', 'off', sub, 'cpu', 1)
    P(f'stock vs off seed {sd}: all-pair CPU ratio {r[0]:.4f} p {r[3]}')
P('')

# mean of common-solved CPU and nodes, arithmetic (note Summary says "CPU mean 1.926 s")
# signatures stock vs patched scip
diff_solved, diff_all = [], []
for i, sd in allp:
    a, b = D['stock', i, sd], D['scip', i, sd]
    sa = (a['nodes'], a['duallp'], a['primallp'], a['primal'], a['dual'])
    sb = (b['nodes'], b['duallp'], b['primallp'], b['primal'], b['dual'])
    if sa != sb:
        diff_all.append((i, sd))
        if a['solved'] and b['solved']:
            diff_solved.append((i, sd, a['nodes'], b['nodes'], a['duallp'], b['duallp']))
both = [p for p in allp if D['stock', p[0], p[1]]['solved'] and D['scip', p[0], p[1]]['solved']]
P(f'stock vs patched scip: both solved {len(both)}; signature differs on {len(diff_all)} / 120; on both-solved: {len(diff_solved)}')
for x in diff_solved:
    P(f'  {x}')
fl = [(i, sd) for i, sd in allp if D['stock', i, sd]['firstlp'] is not None and D['scip', i, sd]['firstlp'] is not None
      and D['stock', i, sd]['rootdual'] is not None and D['scip', i, sd]['rootdual'] is not None]
P(f'pairs with first LP and root dual in both: {len(fl)}; first LP differs: '
  f'{sum(D["stock", i, sd]["firstlp"] != D["scip", i, sd]["firstlp"] for i, sd in fl)}; root dual differs: '
  f'{sum(D["stock", i, sd]["rootdual"] != D["scip", i, sd]["rootdual"] for i, sd in fl)}')
P('')

# wall/CPU ratios
for s in SET:
    rat = [D[s, i, sd]['wall'] / D[s, i, sd]['time'] for i, sd in allp
           if D[s, i, sd]['time'] and D[s, i, sd]['time'] > 5 and D[s, i, sd]['wall']]
    P(f'median wall/CPU (> 5 CPU s) {s}: {statistics.median(rat):.4f} (n {len(rat)}), max {max(rat):.3f}')
P('')

# reference check for stock
sense = {}
for l in (BASE / 'sources/instancedata.csv').read_text().splitlines()[1:]:
    pass
flags = []
for i, sd in allp:
    r = D['stock', i, sd]
    if i not in solu or r['dual'] is None:
        continue
    kind, z = solu[i]
    tol = 1e-6 * max(1, abs(z))
    # sense from primal/dual ordering: minimization if primal >= dual
    minim = r['primal'] >= r['dual'] if r['primal'] is not None and abs(r['primal']) < 1e19 else None
    if minim is None:
        continue
    bad = (r['dual'] > z + tol) if minim else (r['dual'] < z - tol)
    optbad = r['solved'] and kind == '=opt=' and abs(r['primal'] - z) > tol
    if bad or optbad:
        flags.append((i, sd, kind, z, r['primal'], r['dual'], 'dual-excludes' if bad else 'opt-mismatch'))
P(f'stock reference flags: {flags}')
print('\n'.join(out))
