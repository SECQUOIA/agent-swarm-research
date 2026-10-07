"""Markdown tables for the chain instances.

Reference value U: Gurobi's value when Gurobi proves optimality (MIPGap 1e-6);
otherwise the best feasible value found by Gurobi or ub_local.py (an upper bound
on the minimum).  'closed' = (s_M - s_B) / (U - s_B) with safe dual bounds s.
When U is only an upper bound, 'closed' is a lower estimate of the true
fraction.  Times are cumulative Clarabel solve times in seconds; for KAF and KAX
they include the KA stage they start from.
Usage: python chain_markdown.py > ../logs/chain_tables.md"""
import glob
import json
import re
from collections import OrderedDict

from chain_table import gurobi_ref

ORDER = ['B', 'K', 'A', 'KA', 'KAF', 'KAFc', 'F', 'XF', 'X', 'KAX', 'Xc']


def load(path):
    by = OrderedDict()
    for line in open(path):
        r = json.loads(line)
        by.setdefault(r['method'], []).append(r)
    return by


def ubl(tag):
    try:
        return json.loads(open('../logs/ub/%s.json' % tag).read().strip().splitlines()[-1])['ub']
    except (OSError, ValueError, IndexError, KeyError):
        return None


def stage(rs, m):
    tsolve = sum(r['time_solve'] for r in (rs if m == 'B' else rs[1:]))
    return tsolve, len(rs) - (0 if m == 'B' else 1)


def blocks(size, m):
    p = size['psd']
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


def main():
    paths = [p for p in glob.glob('../logs/chain/chain_*.jsonl')]
    paths.sort(key=lambda p: (int(re.search(r'_m(\d+)_', p).group(1)), p))
    print('| instance | n | s_B | reference U | method | safe bound | closed | rounds | solve time (s) | blocks/cuts | vars | SOC | PSD blocks (order:count) |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for path in paths:
        tag = path.split('/')[-1][:-6]
        by = load(path)
        xf = '../logs/chain/xf_%s.jsonl' % tag
        try:
            byx = load(xf)
            if 'XF' in byx:
                by['XF'] = byx['XF']
        except OSError:
            pass
        n = 3 * int(re.search(r'_m(\d+)_', tag).group(1))
        g = gurobi_ref(tag)
        u = ubl(tag)
        cands = []
        if g is not None:
            cands.append(g['ub'])
        if u is not None:
            cands.append(u)
        if g is not None and g['optimal']:
            U, us = g['ub'], '%.6f (Gurobi opt.)' % g['ub']
        elif cands:
            U = min(cands)
            us = '%.6f (feasible)' % U
        else:
            U, us = None, 'n/a'
        sB = by['B'][-1]['safe']
        tKA, rKA = stage(by['KA'], 'KA') if 'KA' in by else (0.0, 0)
        first = True
        for m in ORDER:
            if m not in by:
                continue
            rs = by[m]
            last = rs[-1]
            t, rnd = stage(rs, m)
            if m in ('KAF', 'KAFc', 'KAX'):
                t += tKA
                rnd += rKA
            closed = (last['safe'] - sB) / (U - sB) if U is not None and U != sB else float('nan')
            s = last['size']
            psd = ', '.join('%s:%d' % kv for kv in s['psd'].items())
            print('| %s | %s | %s | %s | %s | %.6f | %.4f | %d | %.2f | %s | %d | %d | %s |' % (
                tag if first else '', n if first else '', ('%.6f' % sB) if first else '', us if first else '',
                m, last['safe'], closed, rnd, t, blocks(s, m), s['vars'], s['soc'], psd))
            first = False


if __name__ == '__main__':
    main()
