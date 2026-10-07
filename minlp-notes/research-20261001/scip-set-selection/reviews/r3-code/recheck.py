"""Review r3: independent recheck of the round-2 revision numbers.

Own parser; imports nothing from the stream code or earlier review code.
Reads logs/full (archived patched batch), logs/full_stock (stock rerun, not
attempts/) and reviews/r2-logs/sameload (reviewer same-load runs).
"""
import math
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
INST = (BASE / 'logs/testset_full.txt').read_text().split()
SEEDS = (1, 2)
LIMIT = 300.0


def parse(path):
    text = path.read_text(errors='replace')

    def grab(pat):
        m = re.search(pat, text, re.M)
        return m.group(1) if m else None

    status = grab(r'^SCIP Status\s*:\s*(.*)$') or ''
    t = grab(r'^Solving Time \(sec\)\s*:\s*(\S+)')
    nodes_line = re.search(r'^Solving Nodes\s*:\s*(\d+)(?:\s*\(total of (\d+) nodes)?', text, re.M)
    last = int(nodes_line.group(1)) if nodes_line else None
    total = int(nodes_line.group(2)) if nodes_line and nodes_line.group(2) else last
    plp = re.search(r'^  primal LP\s*:\s*\S+\s+(\d+)\s+(\d+)', text, re.M)
    dlp = re.search(r'^  dual LP\s*:\s*\S+\s+(\d+)\s+(\d+)', text, re.M)
    rows = []
    for line in text.splitlines():
        m = re.match(r'^\s*[*a-zA-Z]?\s*([\d.]+)s\|(.*)$', line)
        if m:
            cols = [c.strip() for c in m.group(2).split('|')]
            rows.append((float(m.group(1)), cols))
    return dict(solved='optimal solution found' in status, time=float(t) if t else None,
                last=last, total=total,
                sig=(last, plp.groups() if plp else None, dlp.groups() if dlp else None),
                rows=rows)


R = {}
for setting in ('off', 'scip', 'corner', 'eff'):
    for i in INST:
        for s in SEEDS:
            R[setting, i, s] = parse(BASE / 'logs/full' / f'{i}.{setting}.s{s}.log')
for i in INST:
    for s in SEEDS:
        R['stock', i, s] = parse(BASE / 'logs/full_stock' / f'{i}.scip.s{s}.log')
SETTINGS = ('off', 'stock', 'scip', 'corner', 'eff')
PAIRS = [(i, s) for i in INST for s in SEEDS]
assert len(PAIRS) == 120


def cpu(setting, p):
    r = R[(setting,) + p]
    return r['time'] if r['solved'] else LIMIT


def sgm(vals, shift):
    return math.exp(math.fsum(math.log(v + shift) for v in vals) / len(vals)) - shift


def ratio(a, b, pairs):
    return math.exp(math.fsum(math.log((cpu(a, p) + 1) / (cpu(b, p) + 1)) for p in pairs) / len(pairs))


print('== Solved counts and CPU sgm (shift 1, unsolved at 300 s)')
for st in SETTINGS:
    for seeds in ((1,), (2,), (1, 2)):
        ps = [p for p in PAIRS if p[1] in seeds]
        n = sum(R[(st,) + p]['solved'] for p in ps)
        print(f'{st:7s} seeds {seeds}: solved {n}/{len(ps)} CPU sgm {sgm([cpu(st, p) for p in ps], 1):.3f}')

print('\n== Node sgm (shift 100), pairs where every setting has a node count')
node_pairs = [p for p in PAIRS if all(R[(st,) + p]['last'] is not None for st in SETTINGS)]
print('node pairs:', len(node_pairs), 'missing:', [p for p in PAIRS if p not in node_pairs])
maxdiff = (0, None)
for st in SETTINGS:
    for seeds in ((1,), (2,), (1, 2)):
        ps = [p for p in node_pairs if p[1] in seeds]
        a = sgm([R[(st,) + p]['last'] for p in ps], 100)
        b = sgm([R[(st,) + p]['total'] for p in ps], 100)
        if abs(b - a) > maxdiff[0]:
            maxdiff = (abs(b - a), (st, seeds, a, b))
        print(f'{st:7s} seeds {seeds}: n {len(ps)} last {a:.4f} ({a:.1f}) total {b:.4f} ({b:.1f}) diff {b - a:.4f}')
print('max node-sgm change (all-pair tables):', maxdiff)

print('\n== Common solved by all five settings')
common = [p for p in PAIRS if all(R[(st,) + p]['solved'] for st in SETTINGS)]
print('common pairs:', len(common), 'instances:', len({p[0] for p in common}))
for st in SETTINGS:
    ps = common
    a = sgm([cpu(st, p) for p in ps], 1)
    nl = sgm([R[(st,) + p]['last'] for p in ps], 100)
    nt = sgm([R[(st,) + p]['total'] for p in ps], 100)
    print(f'{st:7s}: CPU sgm {a:.3f} nodes last {nl:.1f} total {nt:.1f}')

print('\n== Stock vs off excluding ex5_4_2 s1')
ps = [p for p in PAIRS if p != ('ex5_4_2', 1)]
for st in ('stock', 'off'):
    print(st, sum(R[(st,) + p]['solved'] for p in ps), f'{sgm([cpu(st, p) for p in ps], 1):.3f}')
print('stock/off shifted CPU ratio', f'{ratio("stock", "off", ps):.4f}')
print('stock-only solved:', [p for p in PAIRS if R[('stock',) + p]['solved'] and not R[('off',) + p]['solved']])
print('off-only solved:', [p for p in PAIRS if R[('off',) + p]['solved'] and not R[('stock',) + p]['solved']])

print('\n== Matching-signature pairs (nodes + primal LP calls/iters + dual LP calls/iters)')
both = [p for p in PAIRS if R[('stock',) + p]['solved'] and R[('scip',) + p]['solved']]
same = [p for p in both if R[('stock',) + p]['sig'] == R[('scip',) + p]['sig']]
print('both solved:', len(both), 'matching:', len(same), 'changed:', [p for p in both if p not in same])
print('all-120 signature differences:', sum(R[('stock',) + p]['sig'] != R[('scip',) + p]['sig'] for p in PAIRS))
print(f'patched/stock on matching: {ratio("scip", "stock", same):.4f}')
for lo, hi in ((0, 1), (1, 10), (10, 1e9)):
    sub = [p for p in same if lo <= R[('stock',) + p]['time'] < hi]
    print(f'  stock CPU [{lo},{hi}): n {len(sub)} ratio {ratio("scip", "stock", sub):.4f}')
same_off = [p for p in same if R[('off',) + p]['solved']]
print('matching and off-solved:', len(same_off))
print(f'  cross-batch stock/off {ratio("stock", "off", same_off):.4f}')
print(f'  within-batch patched/off {ratio("scip", "off", same_off):.4f}')
off_same_nodes = sum(R[('off',) + p]['sig'] == R[('scip',) + p]['sig'] for p in same_off)
print(f'  of these, off has the same signature as patched on {off_same_nodes}')
print(f'Section 7.2 check: patched scip/off on all pairs {ratio("scip", "off", PAIRS):.4f}')

print('\n== Path outcomes')
for i, s in (('blend852', 1), ('blend852', 2), ('tln7', 1), ('gabriel01', 2)):
    for st in ('stock', 'scip'):
        r = R[(st, i, s)]
        print(f'{i} s{s} {st}: solved {r["solved"]} time {r["time"]} nodes {r["last"]}')

print('\n== gabriel01 s2 shared display prefix (columns except time and mem)')
a = R['stock', 'gabriel01', 2]['rows']
b = R['scip', 'gabriel01', 2]['rows']


def key(cols):
    return tuple(c for k, c in enumerate(cols) if k != 4)  # drop mem/heur column (cols: node, left, LP iter, LP it/n, mem/heur, ...)


k = 0
while k < min(len(a), len(b)) and key(a[k][1]) == key(b[k][1]):
    k += 1
print('shared rows:', k, 'last shared node:', a[k - 1][1][0], 'stock time', a[k - 1][0], 'patched time', b[k - 1][0])
fac = b[k - 1][0] / a[k - 1][0]
print(f'speed factor {fac:.4f}; 256.83 x factor = {R["stock", "gabriel01", 2]["time"] * fac:.1f}')
k2 = 0
while k2 < min(len(a), len(b)) and a[k2][1] == b[k2][1]:
    k2 += 1
print('shared rows including mem column:', k2)

print('\n== Same-load runs (reviews/r2-logs/sameload)')
SL = BASE / 'reviews/r2-logs/sameload'
for i in ('kall_diffcircles_5b', 'nvs24', 'crudeoil_pooling_ct2', 'pointpack08'):
    L = {(c, b): parse(SL / f'{i}.{c}.s1.{b}.log') for c in ('off', 'scip') for b in ('patched', 'stock')}
    for c in ('off', 'scip'):
        arch = R[(c, i, 1)]
        stk = R[('stock', i, 1)]
        nodes_ok = all(L[c, b]['last'] == arch['last'] for b in ('patched', 'stock'))
        if c == 'scip':
            nodes_ok = nodes_ok and stk['last'] == arch['last']
        print(f'{i} {c}: patched/stock same-load {L[c, "patched"]["time"] / L[c, "stock"]["time"]:.4f}; '
              f'nodes match archived: {nodes_ok}; archived patched {arch["time"]} '
              f'same-load stock {L[c, "stock"]["time"]} archived/same-load {arch["time"] / L[c, "stock"]["time"]:.2f}'
              + (f'; stock batch {stk["time"]}' if c == 'scip' else ''))

print('\n== Section 7.4 cross-batch ratio table (unchanged numbers, spot check)')
print(f'stock/off all {ratio("stock", "off", PAIRS):.4f} common {ratio("stock", "off", common):.4f}')
print(f'patched/stock all {ratio("scip", "stock", PAIRS):.4f} common {ratio("scip", "stock", common):.4f}')
pso = [p for p in PAIRS if R[('stock',) + p]['solved'] and R[('off',) + p]['solved']]
print(f'stock/off pair-solved n {len(pso)} {ratio("stock", "off", pso):.4f}; patched/stock pair-solved n {len(both)} {ratio("scip", "stock", both):.4f}')

print('\n== Per-seed common-solved node sgm, last vs total (N2 bound)')
worst = 0.0
for st in SETTINGS:
    for sd in SEEDS:
        ps = [p for p in common if p[1] == sd]
        a = sgm([R[(st,) + p]['last'] for p in ps], 100)
        b = sgm([R[(st,) + p]['total'] for p in ps], 100)
        worst = max(worst, abs(round(b, 1) - round(a, 1)))
        print(f'{st:7s} s{sd}: n {len(ps)} last {a:.1f} total {b:.1f}')
print(f'max displayed change in per-seed common-solved columns: {worst:.1f}')

print('\n== Local links in note.md')
note = (BASE / 'note.md').read_text()
bad = [t for t in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', note)
       if not t.startswith('http') and not (BASE / t).exists()]
print('missing link targets:', bad)
