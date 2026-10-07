"""Review r1: share of searched cuts whose lambda changed, and median per-instance mean criterion gain (root, seed 0),
from the 'Quadratic SetSel' statistics line (Section 6, finding 5)."""
import os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute import LOGS
for s in ('corner', 'eff'):
    calls = changed = 0; gains = []; evals = 0; seltime = 0.0
    for f in os.listdir(os.path.join(LOGS, 'root')):
        if not f.endswith('.%s.s0.log' % s):
            continue
        m = re.search(r'\n  Quadratic SetSel :' + r'\s+(\S+)' * 11, open(os.path.join(LOGS, 'root', f)).read())
        if not m:
            continue
        g = m.groups()
        calls += int(g[1]); changed += int(g[2]); evals += int(g[4]); seltime += float(g[7])
        if int(g[2]) > 0:
            gains.append(float(g[5]))
    print('%s: searches %d, changed %d (%.1f%%), evals/search %.1f, median per-instance mean gain %.3f over %d instances, select time %.1f s' % (
        s, calls, changed, 100.0 * changed / calls, evals / calls, np.median(gains), len(gains), seltime))
