"""Compare the rerun of exp_loop.py (this stream) with the JSON records of the sfree note."""
import json, sys
import numpy as np
O = '../../../research-20260928b/sfree/logs/'
for tag in ('small', 'big'):
    a = json.load(open(O + 'exp_loop_%s.json' % tag)); b = json.load(open('../logs/repro_exp_loop_%s.json' % tag))
    ra, rb = a['records'], b['records']
    assert [r['inst'] for r in ra] == [r['inst'] for r in rb]
    print('%s: n = %d instances' % (tag, len(ra)))
    for rule in ('scip', 'orbit', 'orbitB', 'corner'):
        d = max(abs(x - y) for p, q in zip(ra, rb) for x, y in zip(p[rule], q[rule]))
        m = b['summary'][rule]['mean_closed_by_round']
        print('  %-7s max |diff| %.2e   mean closed by round (rerun): %s  cuts %.1f' % (
            rule, d, ' '.join('%.3f' % v for v in m), b['summary'][rule]['mean_ncuts']))
