"""Minima of SCIP's ratio in the random samples of scip_random.py (revision after review round 1).
Reads the four compressed logs; scipB is SCIP's Case-4 set (the completion), scipA the uncompleted set.
usage: python3 scip_random_minima.py"""
import glob
import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for fn in sorted(glob.glob(os.path.join(HERE, '..', 'logs', 'scip_random_*.log.gz'))):
    with gzip.open(fn, 'rt') as f:
        rows += [json.loads(l) for l in f if l.startswith('{')]
print('corners:', len(rows))
for name, sel in (('D <= 2', lambda r: r['D'] <= 2), ('D <= 2 and cond(P~) <= 10', lambda r: r['D'] <= 2 and r['cond'] <= 10)):
    m = [r for r in rows if sel(r)]
    for key in ('scipB', 'scipA'):
        r0 = min(m, key=lambda r: r[key])
        print('%-27s %5d corners  min %s = %.4f  (D = %.3f, cond = %.1f)' % (name, len(m), key, r0[key], r0['D'], r0['cond']))
