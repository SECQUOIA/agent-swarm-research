import json, sys, collections, numpy as np
d = collections.defaultdict(list)
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l); d[(r['b'], r['alpha'], r['k'])].append(r)
print("b alpha k p n | N done | nodes geo-mean [min,max] | clique median [min,max] | leaves>=clique | rec")
for key in sorted(d):
    v = d[key]; b, a, k = key
    nodes = [r['nodes'] for r in v]; done = sum(r['done'] for r in v)
    cl = [r['clique'] for r in v if 'clique' in r]
    ok = all((r['nodes'] + 1) // 2 >= r['clique'] for r in v if 'clique' in r)
    print("%.0f %.2f %2d %3d %3d | %d %d | %8.1f [%d,%d] | %s | %s | %d" % (b, a, k, v[0]['p'], v[0]['n'], len(v), done,
          np.exp(np.mean(np.log(nodes))), min(nodes), max(nodes),
          ("%.1f [%d,%d]" % (np.median(cl), min(cl), max(cl))) if cl else '-', ok, sum(r['rec'] for r in v)))
