"""Reviewer r2: split F's logged time advantage over X into block type (XF vs F) and
selection (X vs XF), from the regenerated method tables; and recheck Section 4.5 audit numbers
and the n = 3 safe closure table from raw records.
Run from three-var-computation/: python reviews/r2-code/r2_cost_split.py
"""
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def table(kind):
    rows, inst = {}, None
    for line in open(os.path.join(ROOT, 'logs/table_%s.md' % kind)):
        c = [s.strip() for s in line.strip().strip('|').split('|')]
        if len(c) < 13 or c[2] in ('method', '---'):
            continue
        inst = c[0] or inst
        rows.setdefault(inst, {})[c[2]] = dict(solve=float(c[7]), blocks=c[9], closed=c[4])
    return rows


for kind in ('chain', 'cactus'):
    print('==', kind)
    lo = {}
    for inst, r in table(kind).items():
        if not all(m in r for m in ('F', 'X', 'XF')):
            print(inst, 'missing', sorted(r))
            continue
        F, X, XF = r['F']['solve'], r['X']['solve'], r['XF']['solve']
        share = np.log(X / XF) / np.log(X / F) if X > F else float('nan')
        print('%-22s F %7.2f XF %7.2f X %7.2f  X/F %5.2f  XF/F %5.2f  X/XF %5.2f  selection share of log(X/F) %.2f  blocks F %s XF %s X %s' % (
            inst, F, XF, X, X / F, XF / F, X / XF, share, r['F']['blocks'], r['XF']['blocks'], r['X']['blocks']))

print('== Section 4.5 final-family audits')
for name in ('chain_m300_e0.3_s1', 'chain_m1000_e0.3_s1', 'chain_m3000_e0.3_s1', 'cactus_m300_s1',
             'ht_plus_n300_k3_s1', 'ht_plus_n1000_k2_s1'):
    r = json.load(open(os.path.join(ROOT, 'logs/audit', name + '.json')))
    eps = max(0.0, -r['min_depth'])
    g = eps * (r['f_uniform'] - r['F_pobj']) / (1 + eps)
    worst = r.get('worst')
    wtv = None
    if isinstance(worst, list) and worst and isinstance(worst[0], dict):
        wtv = max(w.get('tri_viol', w.get('triangle_violation', float('nan'))) for w in worst)
    print('%-22s depth %.2e fam %.3e gain %.5f gain+margin %.5f pinf %.2e blocks %s worst-keys %s maxtv %s' % (
        name, r['min_depth'], r['family_stqp_min'], g, g + r['F_pobj'] - r['F_safe'], r['F_pinf'],
        r['F_blocks'], sorted(worst[0]) if isinstance(worst, list) and worst and isinstance(worst[0], dict) else type(worst).__name__, wtv))

print('== n = 3 safe closures')
pool = [json.loads(l) for l in open(os.path.join(ROOT, 'data/pool_hard3.jsonl'))]
print('objectives', len(pool))
for m in ('K', 'A', 'KA', 'F', 'KAF'):
    c = np.array([(p[m + '_safe'] - p['B_safe']) / (p['X_safe'] - p['B_safe']) for p in pool])
    print('%-4s mean %.4f median %.4f min %r' % (m, c.mean(), np.median(c), c.min()))
print('KA == K on all (safe, 1e-7 rel):', all(abs(p['KA_safe'] - p['K_safe']) <= 1e-7 * max(1, abs(p['K_safe'])) for p in pool))
print('max X_safe - F_primal:', max(p['X_safe'] - p['F'] for p in pool) if 'F' in pool[0] else sorted(pool[0]))
