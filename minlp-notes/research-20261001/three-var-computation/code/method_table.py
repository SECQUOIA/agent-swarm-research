"""Markdown tables of driver.py runs: bound, gap closure, time and SDP size per method.

For each instance log (logs/<dir>/<tag>.jsonl, plus logs/chain/xf_<tag>.jsonl for the
XF runs of the first draft): reference value U = Gurobi optimum if proved, otherwise the
best feasible value from Gurobi and ub_local.py (logs/ub, logs/ub2); s_B = safe bound
of B; for each method, the final safe bound s, the closure (s - s_B)/(U - s_B), the
closure of the triple-level gap (s - s_B)/(s* - s_B) where s* is the largest final safe
bound over all methods, rounds, cumulative Clarabel solve time (for KAF, KAFc, KAX
including the KA stage), cumulative separation time, number of blocks or cuts, and model
size: variables, SOC count, PSD blocks and the total PSD dimension sum k(k+1)/2.
Usage: python method_table.py dir [tag-regex]"""
import glob
import json
import os
import re
import sys
from collections import OrderedDict

from audit_table import best_ub
from chain_table import gurobi_ref

ORDER = ['B', 'K', 'A', 'KA', 'KAF', 'KAFc', 'F', 'XF', 'X', 'KAX', 'Xc']


def load(path):
    by = OrderedDict()
    for line in open(path):
        r = json.loads(line)
        by.setdefault(r['method'], []).append(r)
    return by


def stage(rs, m):
    recs = rs if m == 'B' else rs[1:]
    return sum(r['time_solve'] for r in recs), sum(r['time_sep'] for r in rs), len(rs) - (0 if m == 'B' else 1)


def blocks(size, m):
    if m in ('F', 'KAF'):
        return '%d F' % size['F']
    if m in ('X', 'KAX', 'XF'):
        return '%d X' % size['X']
    if m in ('K', 'KA'):
        return '%d K' % size['K']
    if m == 'A':
        return '%d A' % size['A']
    if m == 'KAFc':
        return '%d cuts' % size['Fcut']
    if m == 'Xc':
        return '%d cuts' % size['Xcut']
    return ''


def reference(tag):
    g = gurobi_ref(tag)
    if g is not None and g['optimal']:
        return g['ub'], 'opt'
    u = best_ub(tag)
    return (u, 'feas') if u is not None else (None, '')


def main():
    d = sys.argv[1]
    pat = re.compile(sys.argv[2]) if len(sys.argv) > 2 else None
    paths = [p for p in glob.glob('../logs/%s/*.jsonl' % d) if not os.path.basename(p).startswith('xf_')]
    if pat:
        paths = [p for p in paths if pat.search(p)]

    def key(p):
        nums = re.findall(r'_[mn](\d+)_', p)
        return (int(nums[0]) if nums else 0, p)
    paths.sort(key=key)
    print('| instance | U | method | safe bound | closed (U) | closed (triple) | rounds | solve s | sep s | blocks/cuts | vars | SOC | PSD dim |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for path in paths:
        tag = os.path.basename(path)[:-6]
        by = load(path)
        xf = '../logs/chain/xf_%s.jsonl' % tag
        if 'XF' not in by and os.path.exists(xf):
            by['XF'] = load(xf)['XF']
        U, kind = reference(tag)
        sB = by['B'][-1]['safe']
        sstar = max(rs[-1]['safe'] for rs in by.values())
        tKA = stage(by['KA'], 'KA')[0] if 'KA' in by else 0.0
        rKA = stage(by['KA'], 'KA')[2] if 'KA' in by else 0
        first = True
        for m in ORDER:
            if m not in by:
                continue
            rs = by[m]
            last = rs[-1]
            t, tsep, rnd = stage(rs, m)
            if m in ('KAF', 'KAFc', 'KAX'):
                t += tKA
                rnd += rKA
            cu = (last['safe'] - sB) / (U - sB) if U is not None and U - sB > 1e-9 * max(1, abs(U)) else float('nan')
            ct = (last['safe'] - sB) / (sstar - sB) if sstar - sB > 1e-9 * max(1, abs(sstar)) else float('nan')
            s = last['size']
            print('| %s | %s | %s | %.6f | %.4f | %.4f | %d | %.2f | %.2f | %s | %d | %d | %d |' % (
                tag if first else '', ('%.6f (%s)' % (U, kind)) if (first and U is not None) else ('' if not first else 'n/a'),
                m, last['safe'], cu, ct, rnd, t, tsep, blocks(s, m), s['vars'], s['soc'], s.get('psd_svec', 0)))
            first = False


if __name__ == '__main__':
    main()
