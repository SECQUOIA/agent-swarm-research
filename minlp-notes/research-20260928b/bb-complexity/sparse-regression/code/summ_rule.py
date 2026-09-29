import json, sys, collections, numpy as np
d = collections.defaultdict(list)
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l); d[(r['p'], r['k'], r['alpha'])].append(r)
print("p k alpha n | N | S* opt | removal half holds | C1 holds | median bad1 | maxz nodes geo [max] (done) | maxfrac nodes geo [max] (done)")
for key in sorted(d):
    v = d[key]; p, k, a = key
    g = lambda br: (np.exp(np.mean(np.log([r[br]['nodes'] for r in v]))), max(r[br]['nodes'] for r in v), sum(r[br]['done'] for r in v))
    w = [r for r in v if 'bad0' in r]
    print("%4d %2d %.2f %3d | %d | %d | %d | %d | %.0f | %.0f [%d] (%d) | %.0f [%d] (%d)" % (p, k, a, v[0]['n'], len(v), sum(r.get('rec', False) for r in v),
          sum(r['bad0'] == 0 for r in w), sum(r['bad0'] + r['bad1'] == 0 for r in w), np.median([r['bad1'] for r in w]) if w else -1,
          *g('maxz'), *g('maxfrac')))
