"""Group D: recount varboundrelax=b vs default from raw scan logs, own parser and own rule
(status optimal and claimed dual > witness + 1e-4), ignoring the logs' WRONG/ok labels."""
import os, re, ast, csv
from fractions import Fraction as Q
T = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scip-bug', 'logs'))
W = {'p0': Q('168.108652029808'), 'p4': Q('-6.73064369981647'), 'p5': Q('-232.172853003462'),
     'pair2236': Q('55.689908409449'), 'pumps_default': Q(153, 250), 'fm336_v1010': Q(187, 270),
     'fm318_master': Q(729, 500)}
def model_of(s):
    for k in sorted(W, key=len, reverse=True):
        if k + '.cip' in s: return k
    raise ValueError(s)
def groups(name):
    """yield (header, extra, model, [(label, seed, optimal, claim, logflag)])"""
    buf = []
    for line in open(os.path.join(T, name)):
        line = line.rstrip('\n')
        m = re.match(r'(?:(\S+) )?seed\s+(\d+) (.*)$', line)
        if m:
            rest = m.group(3)
            opt = ('status optimal' in rest) or ('optimal solution foun' in rest)
            c = re.search(r'(?:claimed|dual) (\S+)', rest)
            buf.append((m.group(1) or 'wheel', int(m.group(2)), opt, Q(c.group(1)) if c else None, rest.split()[-1]))
        elif line.startswith('# ') and 'extra=' in line:
            extra = ast.literal_eval(re.search(r'extra=(\{.*?\}):', line).group(1))
            yield line, extra, model_of(line), buf
            buf = []
def wrong(model, r):
    return r[2] and r[3] is not None and r[3] > W[model] + Q(1, 10**4)
B = {'b': [], 'def': []}
mism = 0
def note(kind, model, rows):
    global mism
    for r in rows:
        w = wrong(model, r)
        mism += (w != (r[4] == 'WRONG'))
        B[kind].append((model, r[0], r[1], w, r[2]))
# b runs
for name in ['fm_scan.log', 'master_vbr_b_p4.log', 'master_vbr_b_p5.log', 'master_vbr_b_pair2236.log',
             'master_vbr_b_pumps_default.log', 'p4_smallexcess_vbr_b.log'] + [f'seedscan_vbr_b_{m}.log' for m in ['p0', 'p4', 'p5', 'pair2236']]:
    for h, ex, model, rows in groups(name):
        if ex.get('constraints/nonlinear/varboundrelax') == 'b':
            note('b', model, rows)
nb = len(B['b']); wb = sum(x[3] for x in B['b']); nopt = sum(not x[4] for x in B['b'])
print('varboundrelax=b runs', nb, 'wrong', wb, 'non-optimal status', nopt)
# matched defaults
bkeys = {(m, l, s) for m, l, s, _, _ in B['b']}
# wheel: seeds 0-9 of p0,p4,p5 and 0-29 pair2236
for m, n in [('p0', 10), ('p4', 10), ('p5', 10), ('pair2236', 30)]:
    for h, ex, model, rows in groups(f'seedscan_{m}.log'):
        if ex == {}: note('def', model, [r for r in rows if r[1] < n])
for m in ['p4', 'p5', 'pair2236', 'pumps_default']:
    seeds = {s for (mm, l, s) in bkeys if mm == m and l == 'master'}
    for h, ex, model, rows in groups(f'master_{m}.log'):
        if ex == {}: note('def', model, [r for r in rows if r[1] in seeds])
for h, ex, model, rows in groups('fm_scan.log'):
    if ex == {} and h.startswith(('# master ', '# 10.1.0 ')):
        note('def', model, rows)
for h, ex, model, rows in groups('binary_p4.log'):
    lab = h.split()[1]
    if ex == {} and lab in ('10.0.2', '10.1.0'):
        want = 3 if lab == '10.0.2' else 4
        note('def', model, [r for r in rows if r[1] == want])
D = B['def']
print('matched default runs', len(D), 'wrong', sum(x[3] for x in D))
from collections import Counter
print('default by (model,label):', sorted(Counter((x[0], x[1], x[3]) for x in D).items()))
# each default run matched to a b run with same model/label/seed?
dkeys = Counter((m, l, s) for m, l, s, _, _ in D); bk = Counter((m, l, s) for m, l, s, _, _ in B['b'])
print('default keys == b keys:', dkeys == bk)
print('label mismatches vs own rule:', mism)
# CSV coverage
rows = list(csv.DictReader(open(os.path.join(T, 'scan_summary.csv'))))
print('CSV rows', len(rows), 'rows from p4_smallexcess_vbr_b.log:', sum('smallexcess' in r['log'] for r in rows))
print('CSV rows with varboundrelax b:', sum('varboundrelax' in r['extra'] for r in rows),
      'seeds', sum(int(r['seeds']) for r in rows if 'varboundrelax' in r['extra']))
