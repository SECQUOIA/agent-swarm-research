"""Reviewer r1: recompute the Section 4.3, 4.5 and 4.6 tables from raw logs (no stream imports).

Definitions are taken from the note text, not from the stream's table code:
  U        = smallest feasible value among ub_local outputs (logs/ub, logs/ub2, last line 'ub')
             and Gurobi incumbents (logs/gurobi, logs/gurobi2, 'Best objective'); Gurobi
             'Optimal solution found' gives the '(opt.; tol.)' label.
  closed M = (final safe bound of M - final safe bound of B) / (U - final safe bound of B).
  time M   = sum of time_solve over the method's own rounds (records after round 0);
             KAF additionally includes the KA rounds.
  PSD dim  = psd_svec of the final model; blocks = size['F'] / size['X'] of the final model.
Also: Gurobi .sol files are evaluated with the instance JSON objective, and the
(triple, orientation) pair count of all F runs is summed.
Run from three-var-computation/: python reviews/r1-code/tables_recompute.py
"""
import glob
import json
import os
import re

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L = os.path.join(ROOT, 'logs')
D = os.path.join(ROOT, 'data')


def load_inst(tag):
    d = json.load(open(os.path.join(D, tag + '.json')))
    n = d['n']
    H = np.zeros((n, n))
    for i, j, v in d['H']:
        H[i, j] = H[j, i] = v
    return H, np.array(d['g'])


def gurobi(tag):
    out = []
    for dd in ('gurobi', 'gurobi2'):
        p = os.path.join(L, dd, tag + '.log')
        if os.path.exists(p):
            txt = open(p).read()
            m = re.findall(r'Best objective ([-+0-9.e]+), best bound ([-+0-9.e]+)', txt)
            if m:
                out.append((float(m[-1][0]), float(m[-1][1]), 'Optimal solution found' in txt, dd))
    return out


def U_of(tag):
    vals = []
    for dd in ('ub', 'ub2'):
        p = os.path.join(L, dd, tag + '.json')
        if os.path.exists(p):
            lines = [x for x in open(p).read().splitlines() if x.strip()]
            if lines:
                vals.append(json.loads(lines[-1])['ub'])
    gs = gurobi(tag)
    vals += [g[0] for g in gs]
    return (min(vals) if vals else None), any(g[2] for g in gs)


def load_log(path):
    by = {}
    for line in open(path):
        r = json.loads(line)
        by.setdefault(r['method'], []).append(r)
    return by


def method_rows(d):
    rows = {}
    paths = sorted(p for p in glob.glob(os.path.join(L, d, '*.jsonl')) if not os.path.basename(p).startswith('xf_'))
    for p in paths:
        tag = os.path.basename(p)[:-6]
        by = load_log(p)
        xf = os.path.join(L, 'chain', 'xf_' + tag + '.jsonl')
        if 'XF' not in by and os.path.exists(xf):
            by['XF'] = load_log(xf)['XF']
        U, opt = U_of(tag)
        sB = by['B'][-1]['safe']
        row = {'U': U, 'opt': opt, 'B_safe': sB}
        for m, rs in by.items():
            t = sum(r['time_solve'] for r in (rs if m == 'B' else rs[1:]))
            if m == 'KAF' and 'KA' in by:
                t += sum(r['time_solve'] for r in by['KA'][1:])
            last = rs[-1]
            row[m] = {'safe': last['safe'], 'pobj': last['pobj'], 'closed': (last['safe'] - sB) / (U - sB) if U else None,
                      'time': t, 'psd': last['size'].get('psd_svec'), 'F': last['size'].get('F'),
                      'X': last['size'].get('X'), 'status': last['status'], 'rounds': len(rs) - 1}
            if m == 'F':
                row['F_pairs'] = sum(r.get('violated_pairs', 0) for r in rs)
                row['F_triples'] = sum(r.get('violated_triples', 0) for r in rs)
        rows[tag] = row
    return rows


def parse_compact(path):
    out = {}
    for line in open(path).read().splitlines()[2:]:
        c = [x.strip() for x in line.split('|')[1:-1]]
        out[c[0]] = c
    return out


def fmt_row(tag, r):
    M = ['KA', 'KAF', 'F', 'XF', 'X']
    g = lambda m, k, f: (f % r[m][k]) if m in r else '-'
    U = '%.6f' % r['U'] + (' (opt.; tol.)' if r['opt'] else '')
    return [tag, U] + [g(m, 'closed', '%.4f') for m in M] + [
        '%s / %s / %s' % (g('KA', 'time', '%.2f'), g('F', 'time', '%.2f'), g('X', 'time', '%.2f')),
        '%s / %s / %s' % (g('KA', 'psd', '%d'), g('F', 'psd', '%d'), g('X', 'psd', '%d')),
        '%s / %s' % (g('F', 'F', '%d'), g('X', 'X', '%d'))]


note = open(os.path.join(ROOT, 'note.md')).read()
note_rows = {}
for line in note.splitlines():
    if line.startswith('| chain_') or line.startswith('| cactus_') or line.startswith('| ht_'):
        c = [x.strip() for x in line.split('|')[1:-1]]
        if len(c) == 10:
            note_rows[c[0]] = c

allrows = {}
for d in ('chain', 'cactus', 'ht'):
    rows = method_rows(d)
    allrows.update(rows)
    nmis = 0
    for tag, r in rows.items():
        mine = fmt_row(tag, r)
        theirs = note_rows.get(tag)
        if theirs is None:
            print('MISSING in note:', tag)
            continue
        diff = [(i, a, b) for i, (a, b) in enumerate(zip(mine, theirs)) if a != b and a.replace('-0.0000', '0.0000') != b.replace('-0.0000', '0.0000')]
        if diff:
            nmis += 1
            print('DIFF', tag, diff)
    print('%s: %d instances recomputed, %d rows differ from the note' % (d, len(rows), nmis))

# --- derived claims for Section 4.5
cc = {k: v for k, v in allrows.items() if not k.startswith('ht_')}
gainKA = []
for tag, r in cc.items():
    best = max(r['F']['closed'], r['KAF']['closed'])
    gainKA.append((100 * (best - r['KA']['closed']), tag))
pos = sorted(x for x in gainKA if x[0] > 0.05)
print('\nF-or-KAF closure minus KA closure (pp), chains+cacti, >0.05pp:', ['%.2f %s' % x for x in pos])
print('instances with KA within 0.05pp of the family bound:', [t for g, t in gainKA if g <= 0.05])
rat = sorted((r['X']['time'] / r['F']['time'], t) for t, r in cc.items())
print('X/F solve-time ratio chains+cacti: min %.2f (%s) max %.2f (%s)' % (rat[0] + rat[-1]))
ratc = sorted((r['X']['time'] / r['F']['time'], t) for t, r in cc.items() if t.startswith('chain'))
print('X/F ratio chains: min %.2f (%s) max %.2f (%s)' % (ratc[0] + ratc[-1]))
xfF = sorted((r['XF']['time'] / r['F']['time'], t) for t, r in cc.items())
print('XF/F time ratio: chains', ['%.2f' % x for x, t in xfF if t.startswith('chain')], 'cacti', ['%.2f' % x for x, t in xfF if t.startswith('cactus')])
dev = max((abs(r['F']['pobj'] - r['X']['pobj']) / abs(r['X']['pobj']), t) for t, r in cc.items())
print('largest relative |F - X| primal difference:', dev)
fx = sorted((r['F']['closed'] - r['X']['closed'], t) for t, r in cc.items())
print('F closure - X closure, min/max:', fx[0], fx[-1])
kafF = max((r['KAF']['safe'] - r['F']['safe'], t) for t, r in cc.items())
print('max (KAF safe - F safe):', kafF)
pairs = sum(r.get('F_pairs', 0) for r in allrows.values())
trip = sum(r.get('F_triples', 0) for r in allrows.values())
print('F runs: violated pairs %d, violated triples %d, ratio %.4f' % (pairs, trip, pairs / trip))
ht = max((max(r[m]['closed'] for m in ('KA', 'KAF', 'F', 'XF', 'X', 'K', 'A', 'KAFc', 'Xc', 'KAX') if m in r), t)
         for t, r in allrows.items() if t.startswith('ht_'))
print('max closure over all methods on ht:', ht)
rem = sorted((1 - max(r['F']['closed'], r['KAF']['closed']), t) for t, r in cc.items() if '_e0_' not in t)
print('remaining fraction (1 - family closure), eta>0 chains and cacti: min %.4f %s, max %.4f %s' % (rem[0] + rem[-1]))

# --- Gurobi .sol files against the JSON objective
print('\nGurobi solutions evaluated on the JSON objective:')
for p in sorted(glob.glob(os.path.join(D, '*.lp.sol'))):
    tag = os.path.basename(p)[:-7]
    H, g = load_inst(tag)
    x = np.zeros(len(g))
    obj = None
    for line in open(p):
        if line.startswith('# Objective value'):
            obj = float(line.split('=')[1])
        elif line.strip() and not line.startswith('#'):
            k, v = line.split()
            x[int(k[1:])] = float(v)
    inbox = bool(((x >= 0) & (x <= 1)).all())
    print('  %-24s sol objective %.10f  JSON f(x) %.10f  diff %.1e  in box %s' % (tag, obj, x @ H @ x + g @ x, obj - (x @ H @ x + g @ x), inbox))

# --- late Gurobi table
print('\nLate Gurobi references:')
for p in sorted(glob.glob(os.path.join(L, 'gurobi2', '*.log'))):
    tag = os.path.basename(p)[:-4]
    for ub, lb, opt, dd in gurobi(tag):
        print('  %-20s ub %.11f lb %.11f gap %.4f%% diff %.6e optimal %s' % (tag, ub, lb, 100 * (ub - lb) / abs(ub), ub - lb, opt))

# --- Section 4.3 sparse table
print('\nSection 4.3:')
for p in sorted(glob.glob(os.path.join(L, 'sparse_audit', 'plus_*.json')), key=lambda p: (json.load(open(p))['n'], p)):
    tag = os.path.basename(p)[:-5]
    r = json.load(open(p))
    U, _ = U_of(tag)
    gap = U - r['B_safe']
    H, g = load_inst(tag)
    fc = np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2
    eps = max(0.0, -r['min_depth'])
    gain = eps * (fc - r['B']) / (1 + eps)
    print('  %-26s n %4d triples %5d Bsafe %.4f U %.4f U-B %.4f rel %.1e mindepth %.1e gain %.1e (stored %.1e) gain/gap %s pinf %.1e' % (
        tag, r['n'], r['triples'], r['B_safe'], U, gap, gap / abs(U), r['min_depth'], gain, r['max_triple_level_improvement'],
        ('%.4f' % (gain / gap)) if gap / abs(U) > 1e-8 else '-', r.get('pinf', float('nan'))))

# --- SCS table (Section 4.6)
print('\nSCS logs:')
for p in sorted(glob.glob(os.path.join(L, 'scs', '*.jsonl'))):
    by = load_log(p)
    print(' ', os.path.basename(p), {m: ('%.6f' % rs[-1]['safe'], round(sum(r['time_solve'] for r in (rs if m == 'B' else rs[1:])), 1),
                                       rs[-1]['status'], len(rs)) for m, rs in by.items()})
