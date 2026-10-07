import glob, json, collections, numpy as np
BUCK=[(0,0),(1,2),(3,5),(6,10),(11,19)]
T=collections.defaultdict(lambda:[[] for _ in BUCK])
for f in glob.glob('/tmp/rv/mr/logs/diag/diag_6x8_*.jsonl'):
    for line in open(f):
        r=json.loads(line)
        for c in r.get('cuts',[]):
            if 'a' not in c or 'w' not in c: continue
            b=[i for i,(a,z) in enumerate(BUCK) if a<=c['r']<=z][0]
            w=np.array(c['w']); a=np.array(c['a']); m=(a>0)&(w>=1e-4)
            if not m.any(): continue
            v=w[m]/a[m]; z=v.min()
            T[r['rule']+':'+c['set']][b].append((int(np.sum(v<=(1+1e-3)*z)), c['zC']/c['zk'] if c['zk'] and np.isfinite(c['zk']) and c['zk']>0 else np.nan))
for k,B in sorted(T.items()):
    print(k, ' '.join('r%d-%d n=%d tie2=%.3f zC/zK=%.3f'%(BUCK[i]+(len(L),np.mean([x[0]>=2 for x in L]),np.nanmean([x[1] for x in L]))) for i,L in enumerate(B) if L))
