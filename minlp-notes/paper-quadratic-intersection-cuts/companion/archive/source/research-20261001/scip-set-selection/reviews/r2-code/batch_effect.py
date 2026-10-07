"""Review r2: is the stock-vs-patched CPU gap a capture cost or a batch (load) effect?

Compares CPU of identical search paths (same nodes and LP iteration counts) between
batches, split by whether any intersection cut was added. Own parser.
"""
import math, re, statistics
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
INST = (BASE / 'logs/testset_full.txt').read_text().split()


def parse(p):
    t = p.read_text(errors='replace')
    g = lambda pat: (re.search(pat, t, re.M) or [None, None])[1]
    m = re.search(r'^  Quadratic Nlhdlr :\s+(\d+)\s+(\d+)', t, re.M)
    lp = re.search(r'^  dual LP\s*:\s*\S+\s+(\d+)\s+(\d+)', t, re.M)
    plp = re.search(r'^  primal LP\s*:\s*\S+\s+(\d+)\s+(\d+)', t, re.M)
    st = g(r'^SCIP Status\s*: (.*)$') or ''
    return dict(solved='optimal solution found' in st, time=float(g(r'^Solving Time \(sec\)\s*: (\S+)') or 'nan'),
                nodes=g(r'^Solving Nodes\s*: (\d+)'), sig=(lp and lp.groups(), plp and plp.groups()),
                gen=int(m.group(1)) if m else None, add=int(m.group(2)) if m else None)


R = {}
for s, d, n in (('off', 'full', 'off'), ('scip', 'full', 'scip'), ('stock', 'full_stock', 'scip')):
    for i in INST:
        for sd in (1, 2):
            R[s, i, sd] = parse(BASE / 'logs' / d / f'{i}.{n}.s{sd}.log')


def gm(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def report(label, pairs, a, b):
    rat = [(R[a, i, sd]['time'] + 1) / (R[b, i, sd]['time'] + 1) for i, sd in pairs]
    if rat:
        print(f'{label}: n {len(pairs)}, geo-mean shifted CPU ratio {a}/{b} {gm(rat):.4f}, median {statistics.median(rat):.4f}')
    else:
        print(f'{label}: n 0')


pairs = [(i, sd) for i in INST for sd in (1, 2)]
same = [(i, sd) for i, sd in pairs if R['stock', i, sd]['solved'] and R['scip', i, sd]['solved']
        and R['stock', i, sd]['nodes'] == R['scip', i, sd]['nodes'] and R['stock', i, sd]['sig'] == R['scip', i, sd]['sig']]
noadd = [p for p in same if R['stock', p[0], p[1]]['add'] == 0]
add = [p for p in same if (R['stock', p[0], p[1]]['add'] or 0) > 0]
report('identical solved paths, stock vs patched', same, 'scip', 'stock')
report('  ... with zero added intersection cuts (capture cannot act)', noadd, 'scip', 'stock')
report('  ... with added cuts', add, 'scip', 'stock')
for lo, hi in ((0, 1), (1, 10), (10, 300)):
    sub = [p for p in same if lo <= R['stock', p[0], p[1]]['time'] < hi]
    report(f'  ... stock CPU in [{lo},{hi})', sub, 'scip', 'stock')
# off (same batch as patched) vs patched where no cut was added: same-batch control
ctrl = [(i, sd) for i, sd in pairs if R['off', i, sd]['solved'] and R['scip', i, sd]['solved']
        and R['scip', i, sd]['add'] == 0 and R['off', i, sd]['nodes'] == R['scip', i, sd]['nodes']]
report('same batch control: patched scip with 0 added cuts vs off, identical node count', ctrl, 'scip', 'off')
ctrl2 = [(i, sd) for i, sd in pairs if R['off', i, sd]['solved'] and R['stock', i, sd]['solved']
         and R['stock', i, sd]['add'] == 0 and R['off', i, sd]['nodes'] == R['stock', i, sd]['nodes']]
report('cross batch control: stock with 0 added cuts vs off, identical node count', ctrl2, 'stock', 'off')
for i, sd in ctrl2:
    print(f'    {i} s{sd}: off {R["off", i, sd]["time"]} stock {R["stock", i, sd]["time"]} patched {R["scip", i, sd]["time"]} gen {R["stock", i, sd]["gen"]}')

# On identical-path pairs that off also solved: cross-batch stock/off vs same-batch patched/off.
both = [p for p in same if R['off', p[0], p[1]]['solved']]
report('identical-path pairs also solved by off: cross-batch', both, 'stock', 'off')
report('identical-path pairs also solved by off: same batch', both, 'scip', 'off')
