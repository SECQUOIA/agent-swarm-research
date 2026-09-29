import json, collections, numpy as np
d=collections.defaultdict(list)
for l in open('sparse_single.jsonl'):
    r=json.loads(l)
    if not r['done']: d[(r['k'],'notdone')].append(r); continue
    d[(r['k'],round(r['alpha'],1))].append(r)
for key in sorted(d,key=str):
    v=[r for r in d[key] if r.get('done')]
    if not v: print(key,'not done',len(d[key]), [r['n'] for r in d[key]]); continue
    print(key, "n=%d"%v[0]['n'], "N=%d"%len(v), "C1 holds %d"%sum(r['c1'] for r in v), "recov %d"%sum(r['recov'] for r in v),
          "nodes med %.0f max %d"%(np.median([r['nodes'] for r in v]),max(r['nodes'] for r in v)),
          "bad0 med %.1f bad1 med %.1f"%(np.median([r['bad0'] for r in v]),np.median([r['bad1'] for r in v])))
