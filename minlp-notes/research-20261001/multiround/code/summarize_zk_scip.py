"""Tabulate logs/check_zk_scip.log: corners where core.corner_bound has an infeasible minimizer,
by round, and the ratio core / zk_vec there.  Usage: python3 summarize_zk_scip.py"""
import re, collections
import numpy as np
L = [l for l in open('../logs/check_zk_scip.log') if l.startswith('size')]
C = collections.Counter(); T = collections.Counter(); rat = []; low = 0
for l in L:
    m = re.search(r'round (\d+).*scip (\S+)\s+vec (\S+)\s+ref (\S+) \(ref point feasible: (\w+)', l)
    r = int(m.group(1)); s, v, rf, f = float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5)
    T[r] += 1
    if f == 'False':
        C[r] += 1; rat.append(rf / v)
print('corners %d; core minimizer infeasible by round %s of %s' % (len(L), dict(C), dict(T)))
rat = np.array(rat)
print('ratio core / zk_vec at those corners: median %.3g, min %.3g, max %.3g' % (np.median(rat), rat.min(), rat.max()))
