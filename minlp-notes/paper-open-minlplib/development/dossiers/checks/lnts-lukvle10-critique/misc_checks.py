"""Critic's small exact checks (Fractions only) on saved data."""
import json
from fractions import Fraction as Fr
# 1. stored 60-digit h enclosures of the independently proved primal points vs Theorem 3 optimum (critic's iv enclosure)
res = json.load(open('thm3_iv.json'))
for r in res:
    N = r['N']
    pt = json.load(open(f'lnts{N}_point.json'))
    hkey = [k for k in pt['unknowns_box'] if k not in ('x1', 'x%d' % (N + 1))][0]
    enc = {e[0]: (Fr(e[1]), Fr(e[2])) for e in pt['enclosures']}
    lo, hi = enc[hkey]
    olo, ohi = Fr(r['opt_lo']), Fr(r['opt_hi'])
    print(f'N={N}: N*h_enc in [opt_lo {float(N*lo-olo):+.2e}, opt_lo {float(N*hi-olo):+.2e}]; contains optimum: {N*lo <= ohi and olo <= N*hi}')
# 2. author lnts_bound.py float duals vs the author's own N*h2 (binary64 h2), and the report's 15-digit decimals
for N, h2, db, rep in [(50, 0.011093375297664241, 0.554668764883212, '0.554668764883212'),
                       (100, 0.005545954011114516, 0.5545954011114516, '0.554595401111452'),
                       (200, 0.00277288508023813, 0.554577016047626, '0.554577016047626'),
                       (400, 0.0013864310341130746, 0.5545724136452298, '0.554572413645230')]:
    ex = N * Fr(h2)
    print(f'N={N}: author float dual - N*h2 = {float(Fr(db)-ex):+.2e}; report decimal - N*h2 = {float(Fr(rep)-ex):+.2e}')
# 3. lnts50 listed relative gap
for p in ['0.55466876', '0.5546687649386789']:
    print('lnts50 listed rel gap with primal', p, float((Fr(p) - Fr('0.55464755')) / Fr(p)))
# 4. COPS lnts50 six-digit display of our optimum
o = Fr('0.5546687649386788986220922339726517468015')
print('six digits: nearest', round(float(o), 6), ' truncated', int(o * 10**6) / 10**6)
# 5. B&B leaves: binary bisection, leaves = (boxes+1)/2 per problem
d = json.load(open('lukvle10_bnb.json'))
nb = sum(g['boxes'] for g in d['groups']) + d['tail']['boxes']
nl = sum((g['boxes'] + 1) // 2 for g in d['groups']) + (d['tail']['boxes'] + 1) // 2
print('boxes evaluated', nb, ' leaves (pruned+open)', nl)
