"""Review r1: corner/eff vs scip root RGC (seed 0..2) excluding instances where SCIP's rule used monoidal
strengthening at seed 0 (the patch disables it whenever lambda changes)."""
import os, re, sys
from collections import defaultdict
import numpy as np
from scipy.stats import wilcoxon
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute import parse, load_ref, LOGS
ref, tag, sense = load_ref()
mono = set()
for f in os.listdir(os.path.join(LOGS, 'root')):
    if f.endswith('.scip.s0.log'):
        m = re.search(r'\n  Quadratic Nlhdlr :' + r'\s+(\S+)' * 9, open(os.path.join(LOGS, 'root', f)).read())
        if m and int(m.group(9)) > 0:
            mono.add(f.split('.')[0])
print('instances with monoidal strengthening under scip, seed 0:', len(mono))
R = defaultdict(dict)
for d in ('root', 'rootseeds'):
    for f in os.listdir(os.path.join(LOGS, d)):
        if f.endswith('.log') and f.split('.')[1] in ('off', 'scip', 'corner', 'eff'):
            r = parse(os.path.join(LOGS, d, f)); R[(r['inst'], r['seed'])][r['setting']] = r
def ok(r): return r and r['status'] and 'time limit' not in r['status'] and r['rc'] == '0'
def rgc(r, i):
    sg = -1 if sense[i] == 'max' else 1
    if r['rootdb'] is None or r['firstlp'] is None: return None
    den = sg * (ref[i] - r['firstlp'])
    return None if abs(den) <= 1e-6 * max(1, abs(ref[i])) else sg * (r['rootdb'] - r['firstlp']) / den
for sd in (0, 1, 2):
    for a in ('corner', 'eff'):
        for excl in (False, True):
            d = []
            for (i, s), rs in R.items():
                if s != sd or i not in ref or (excl and i in mono): continue
                if not all(ok(rs.get(x)) for x in ('off', 'scip', 'corner', 'eff')): continue
                if sd == 0 and not all(ok(R[(i, 0)].get(x)) for x in ('scipS', 'cornerS', 'effS') if False): pass
                v = [rgc(rs[x], i) for x in ('off', 'scip', 'corner', 'eff')]
                if None in v: continue
                d.append(rgc(rs[a], i) - rgc(rs['scip'], i))
            d = np.array(d)
            print('seed %d %s vs scip %s: n %d mean %+.4f p %.3g' % (sd, a, 'excl. monoidal' if excl else 'all', len(d), d.mean(), wilcoxon(d[np.abs(d) > 1e-9]).pvalue))
