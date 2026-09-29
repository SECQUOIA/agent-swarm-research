import json, collections, numpy as np, sys
d=collections.defaultdict(list)
for fn in sys.argv[1:]:
  for l in open(fn):
    r=json.loads(l)
    c=r['rho']/np.log(r['N'])
    lab=('rho=%g'%r['rho']) if r['rho'] in (1,2,4,8,16) else ('%.0flogN'%c)
    d[(lab,r['N'])].append(r)
labs=sorted(set(k[0] for k in d), key=lambda s:(s.endswith('logN'), float(s.split('=')[1]) if '=' in s else float(s[:-4])))
Ns=sorted(set(k[1] for k in d))
print("geomean nodes (done/total) [max]; cols N=",Ns)
for lab in labs:
    row=[]
    for N in Ns:
        v=d.get((lab,N),[])
        if not v: row.append("%16s"%"-"); continue
        nd=[r['nodes'] for r in v]
        row.append("%6.0f(%d/%d)[%d]"%(np.exp(np.mean(np.log(nd))),sum(r['done'] for r in v),len(v),max(nd)))
    print("%-8s"%lab," ".join(row))
