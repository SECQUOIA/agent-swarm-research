import json, sys, collections, numpy as np
d = collections.defaultdict(list)
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l); d[(r['p'], r['k'], r['rule'], r['n'])].append(r)
print("p k lam n alpha N | PWE root-cert | witness | C1 exact (capped) | mean tau^2 | 2log p | 2log(p lam/n) | mean gap | max time")
for key in sorted(d):
    v = d[key]; p, k, rule, n = key
    lam = v[0]['lam']
    c1 = sum(r['c1'] is True for r in v); cap = sum(r['c1'] == 'capped' for r in v)
    print("%5d %3d %6s %4d %.2f %2d | %d | %d | %d (%d) | %.2f | %.2f | %.2f | %.3f | %.0f" % (
        p, k, rule, n, n / (k * np.log(p)), len(v), sum(r['pwe'] for r in v), sum(r['wit'] for r in v), c1, cap,
        np.mean([r['tau'] ** 2 for r in v]), 2 * np.log(p), 2 * np.log(p * lam / n), np.mean([r['gap'] for r in v]), max(r['time'] for r in v)))
