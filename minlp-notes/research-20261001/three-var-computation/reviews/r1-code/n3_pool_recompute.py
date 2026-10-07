"""Reviewer r1: recompute the Section 4.4 hard-objective table from data/pool_hard3.jsonl."""
import json
import numpy as np
P = [json.loads(l) for l in open('data/pool_hard3.jsonl')]
print('objectives', len(P), 'all three positive diagonals:', all((np.diag(np.array(p['H'])) > 0).all() for p in P))
gap = np.array([p['X'] - p['B'] for p in P])
print('B gap (X - B, primal): min %.4f median %.4f max %.4f' % (gap.min(), np.median(gap), gap.max()))
for m in ('K', 'A', 'KA', 'F', 'KAF'):
    cp_ = np.array([(p[m] - p['B']) / (p['X'] - p['B']) for p in P])
    cs = np.array([(p[m + '_safe'] - p['B_safe']) / (p['X'] - p['B_safe']) for p in P])
    print('%-3s primal closure mean %.4f median %.4f min %.4f | safe closure mean %.4f min %.6f' % (m, cp_.mean(), np.median(cp_), cp_.min(), cs.mean(), cs.min()))
print('max X_safe - F (primal) %.2e' % max(p['X_safe'] - p['F'] for p in P))
print('KA == K on all (|KA-K| < 1e-7):', all(abs(p['KA'] - p['K']) < 1e-7 for p in P))
