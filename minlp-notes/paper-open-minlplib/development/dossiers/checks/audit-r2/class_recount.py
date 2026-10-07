# per-(instance, solver) class counts from results.json, strongest class over flagged points
import json
from collections import defaultdict
R = json.load(open('results.json'))
rank = {'(i) gross': 0, '(i) tolerance-scale': 1, '(i-r)': 2, '(ii) proven': 3, '(ii) repair': 4, '(iii)': 5}
def cl(r):
    c = r['cls']
    if c.startswith('(i) '): return '(i) ' + r['i_group']
    if c.startswith('(i-r)'): return '(i-r)'
    if 'proven' in c: return '(ii) proven'
    if c.startswith('(ii)'): return '(ii) repair'
    return '(iii)'
best = {}
for r in R:
    k = (r['name'], r['solver']); c = cl(r)
    if k not in best or rank[c] < rank[best[k]]: best[k] = c
by = defaultdict(set); cnt = defaultdict(int)
for (n, s), c in best.items(): by[c].add(n); cnt[c] += 1
for c in rank: print(c, cnt[c], 'pairs', len(by[c]), 'instances', sorted(by[c]))
print('total', len(best))
