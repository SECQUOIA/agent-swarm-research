"""Compare my exact C1 decisions (verify_*.jsonl from verify_table61.py, cg_*.jsonl from verify_cg.py)
with the author's records in ../../bb-complexity/sparse-regression/data/."""
import json, glob, collections
D = '../../bb-complexity/sparse-regression/data/'
auth = {}
for fn in sorted(glob.glob(D + 'c1_*.jsonl')):
    for l in open(fn):
        r = json.loads(l)
        key = (r['p'], r['k'], str(r['rule']), r['n'], r['seed'])
        # later full reruns (e.g. c1_gamma_half_full) override capped records
        if key not in auth or auth[key]['c1'] == 'capped':
            auth[key] = r
mine = {}
for fn in sorted(glob.glob('verify_p*.jsonl')):
    for l in open(fn):
        r = json.loads(l); mine[(r['p'], 8, '1.5', r['n'], r['seed'])] = ('C1' if r['c1'] is True else 'fail' if r['c1'] is False else 'undecided', r.get('fail'))
for fn in sorted(glob.glob('cg_*.jsonl')):
    for l in open(fn):
        r = json.loads(l); mine[(r['p'], r['k'], str(r['rule']), r['n'], r['seed'])] = (r['status'], r.get('fail'))
cells = collections.defaultdict(lambda: collections.Counter())
dis = []
for key, (st, fl) in sorted(mine.items()):
    a = auth.get(key)
    if a is None:
        dis.append((key, st, 'no author record')); continue
    ac = a['c1']; acs = 'C1' if ac is True else 'fail' if ac is False else str(ac)
    cells[key[:4]][(acs, st)] += 1
    if not ((acs == 'C1' and st == 'C1') or (acs == 'fail' and st == 'fail')):
        dis.append((key, st, acs))
print("cell (p, k, rule, n): counts of (author, mine)")
for c in sorted(cells):
    print(" ", c, dict(cells[c]))
print("\nnon-matching or upgraded records:")
for d in dis:
    print(" ", d)
