"""Table of chain-instance results (logs/chain/*.jsonl) with Gurobi reference values.

For each instance: n, eta, reference value (Gurobi incumbent if Gurobi reports
optimality within its tolerance, otherwise the incumbent with its bound), and
for each method the gap closed  (safe_M - safe_B) / (ref - safe_B)  using the
safe dual bounds, the final model size, and cumulative solve time.
Usage: python chain_table.py [pattern]"""
import glob
import json
import re
import sys
from collections import OrderedDict

METHODS = ['B', 'K', 'A', 'KA', 'KAF', 'KAFc', 'F', 'X', 'KAX', 'Xc']


def gurobi_ref(tag):
    refs = []
    for directory in ('gurobi', 'gurobi2'):
        try:
            txt = open('../logs/%s/%s.log' % (directory, tag)).read()
        except OSError:
            continue
        m = re.findall(r'Best objective ([-+0-9.e]+), best bound ([-+0-9.e]+), gap ([-+0-9.e]+)%', txt)
        if m:
            ub, lb, gap = map(float, m[-1])
            refs.append({'ub': ub, 'lb': lb, 'gap_pct': gap, 'optimal': 'Optimal solution found' in txt})
    if not refs:
        return None
    ub = min(r['ub'] for r in refs)
    lb = max(r['lb'] for r in refs)
    return {'ub': ub, 'lb': lb, 'gap_pct': 100 * (ub - lb) / abs(ub) if ub else 0.0,
            'optimal': any(r['optimal'] for r in refs)}


def load(path):
    by = OrderedDict()
    for line in open(path):
        r = json.loads(line)
        by.setdefault(r['method'], []).append(r)
    return by


def main():
    pat = sys.argv[1] if len(sys.argv) > 1 else '../logs/chain/chain_*.jsonl'
    for path in sorted(glob.glob(pat), key=lambda p: (int(re.search(r'_m(\d+)_', p).group(1)), p)):
        tag = path.split('/')[-1][:-6]
        by = load(path)
        if 'B' not in by:
            continue
        g = gurobi_ref(tag)
        sB = by['B'][-1]['safe']
        best_safe = max(v[-1]['safe'] for v in by.values())
        if g is not None:
            ref = g['ub']
            refs = 'Gurobi UB %.6f (LB %.6f, %s)' % (g['ub'], g['lb'], 'optimal' if g['optimal'] else 'gap %.4g%%' % g['gap_pct'])
        else:
            ref = best_safe
            refs = 'no Gurobi value; reference = best safe bound %.6f' % ref
        print('%s  B safe %.6f  %s  best safe %.6f' % (tag, sB, refs, best_safe))
        for m in METHODS:
            if m not in by:
                continue
            rs = by[m]
            last = rs[-1]
            tsolve = sum(r['time_solve'] for r in (rs if m == 'B' else rs[1:]))
            tsep = sum(r['time_sep'] for r in rs)
            s = last['size']
            closed = (last['safe'] - sB) / (ref - sB) if ref != sB else float('nan')
            print('   %-5s safe %14.6f closed %7.4f  rounds %2d  t_solve %8.2f t_sep %7.2f t_last %7.2f  vars %6d soc %6d psd %s  %s' % (
                m, last['safe'], closed, len(rs) - (0 if m == 'B' else 1), tsolve, tsep, last['time_solve'],
                s['vars'], s['soc'], s['psd'], last['status']))


if __name__ == '__main__':
    main()
