"""Dossier check: recompute the verifier's lukvle10 dual-bound sum exactly from its logs."""
import json
from fractions import Fraction as Fr
import numpy as np

d = json.load(open('lukvle10_bnb.json'))
lam = np.load('lukvle10_lam_kkt.npy').copy()
x5 = np.load('lukvle10_x5.npy')
LC = lam[495]
assert float(LC) == d['LC']
lam[30:961] = LC
M = 994
print('lam range (dualized, after replacement):', lam[:M].min(), lam[:M].max())
q = [-2 * lam[j - 1] for j in range(1, M + 1)]
print('q range:', min(q), max(q))
# group counts
groups = {}
for i in range(497):
    w = tuple(float(lam[j]) if 0 <= j < M else 0.0 for j in (2 * i - 2, 2 * i - 1, 2 * i, 2 * i + 1))
    groups.setdefault(w, []).append(i)
print('groups', len(groups), 'largest', max(len(v) for v in groups.values()))
cnt = sum(g['count'] for g in d['groups'])
print('pairs covered', cnt)
eps = Fr(1, 10 ** 18)
tot = sum(g['count'] * (Fr(g['LB']) - eps) for g in d['groups']) + Fr(d['tail']['LB']) - eps
ub = sum(g['count'] * Fr(g['UB']) for g in d['groups']) + Fr(d['tail']['UB'])
s = sum(Fr(float(lam[j])) for j in range(M))
bound = tot + s
print('sum lam  =', float(s), ' logged', d['sum_lam'])
def dec(q, n=25):
    neg = q < 0
    q = abs(q)
    i = q.numerator * 10 ** n // q.denominator
    st = str(i).rjust(n + 1, '0')
    return ('-' if neg else '') + st[:-n] + '.' + st[-n:]
print('bound (floor 25 dp) =', dec(bound))
print('sum of UB + sum lam =', dec(ub + s))
summary = Fr('352.2380254050784')
print('summary display <= recomputed bound:', summary <= bound, ' slack', float(bound - summary))
print('verification-report display 352.2380254050785 <= bound:', Fr('352.2380254050785') <= bound)
# tolerance accounting
tol_pairs = sum(g['count'] * (Fr(g['UB']) - Fr(g['LB'])) for g in d['groups'])
print('pair UB-LB total', float(tol_pairs), ' tail UB-LB', float(Fr(d['tail']['UB']) - Fr(d['tail']['LB'])))
xstar_hi = Fr('352.2380254064956226308712710293664647979979')
print('gap to exact point (upper end) vs recomputed bound:', float(xstar_hi - bound))
print('gap to exact point vs summary display:', float(xstar_hi - summary))
# middle group
mid = [g for g in d['groups'] if g['count'] > 1]
print('middle group', mid)
print('max open boxes', max(g['open'] for g in d['groups']), 'incomplete any', any(g['incomplete'] for g in d['groups']))
# KKT stationarity check of float lam at p5 restricted (numerical)
print('x5 middle', x5[40:960].min(), x5[40:960].max())
