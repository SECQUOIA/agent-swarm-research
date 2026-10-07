from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../../../..').resolve()

import json, numpy as np
RES=(str(_NOTES_ROOT) + '/research-20260922/iterated-obbt/results')
F={}
for l in open(RES+'/final.jsonl'):
    r=json.loads(l); F[r['key']]=r
def sgm(x,sh): x=np.asarray(x,float); return float(np.exp(np.mean(np.log(x+sh)))-sh)
for s in ('grb','scip'):
    rows=[]
    for k,r in F.items():
        if r['arm']!='pipe-r1' or r['solver']!=s: continue
        n=r['name']; f=np.load(RES+'/fbbt/%s.npz'%n); b=np.load(RES+'/boxes/%s__%s__r1.npz'%(n,s))
        if np.array_equal(f['lb'],b['lb']) and np.array_equal(f['ub'],b['ub']):
            c=F.get('%s/%s/pipe-none/%d'%(n,s,r['seed']))
            if c and r['status']=='optimal' and c['status']=='optimal':
                rows.append((r['time'],c['time'],r['nodes'],c['nodes'],n))
    a=np.array([x[:4] for x in rows],float)
    same=(a[:,2]==a[:,3]).mean()
    print(s,'identical-setup pairs',len(a),'time ratio pipe-r1/none %.3f'%(sgm(a[:,0],1)/sgm(a[:,1],1)),'node-identical frac %.2f'%same,
          'median |log ratio| time %.3f'%np.median(np.abs(np.log((a[:,0]+0.01)/(a[:,1]+0.01)))))
    big=a[a[:,1]>5]; print('   control>5s: n=%d ratio %.3f'%(len(big), sgm(big[:,0],1)/sgm(big[:,1],1)))
