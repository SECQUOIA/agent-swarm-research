"""Review r1: rebuild the root and full test sets from the raw screening logs with the review parser."""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute import parse, LOGS  # review code, not stream code
recs = [parse(os.path.join(LOGS, 'screen', f)) for f in sorted(os.listdir(os.path.join(LOGS, 'screen'))) if f.endswith('.log')]
cands = [l.strip() for l in open(os.path.join(LOGS, 'candidates.txt')) if l.strip()]
print('candidates', len(cands), 'screen logs', len(recs))
root = sorted(r['inst'] for r in recs if (r.get('rootappl') or 0) > 0)
print('rootappl>0:', len(root), 'matches testset_root:', root == sorted(l.strip() for l in open(os.path.join(LOGS, 'testset_root.txt')) if l.strip()))
pool = sorted(r['inst'] for r in recs if (r.get('rootappl') or 0) > 0 and 'optimal' not in (r['status'] or '') and r['time'] < 30)
sel = sorted(random.Random(20261001).sample(pool, 60))
print('pool', len(pool), 'sample matches testset_full:', sel == sorted(l.strip() for l in open(os.path.join(LOGS, 'testset_full.txt')) if l.strip()))
print('generated>0:', sum((r['gencuts'] or 0) > 0 for r in recs), 'detected rows (Quadratic SetSel present):', sum(r.get('selcalls') is not None for r in recs))
