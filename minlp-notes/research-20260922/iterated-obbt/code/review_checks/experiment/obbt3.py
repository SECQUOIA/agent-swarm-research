import json, math, numpy as np, pandas as pd
from qcqp import QCQP
RES='/home/sgusev/repo/minlp-notes/research-20260922/iterated-obbt/results'
inst=pd.read_csv(RES+'/instances.csv'); inst=inst[inst.in_scope].set_index('name')
FS=inst.fstar_min.to_dict()
ob={}
for l in open(RES+'/obbt.jsonl'):
    r=json.loads(l); ob[(r['name'],r['src'])]=r
allint=[];chg=0;tint=0;ttot=0
for n in inst.index:
    P=QCQP(n)
    ai=all(P.isint[k] for k in P.nlvars)
    c=False
    for s in ('known','grb','scip'):
        if (n,s) in ob:
            r=ob[(n,s)]; t=r['trajs']['full']['snaps']['r1']['time']; ttot+=t
            if ai: tint+=t
            if ai and r['trajs']['full']['hist'][0]['nchanged']>0: c=True
    if ai: allint.append(n); chg+=c
print('allint',len(allint),'changed',chg,'time int %.0f of %.0f = %.2f'%(tint,ttot,tint/ttot))
def gc(LB,LB0,f):
    g=f-LB0
    if not(math.isfinite(LB0) and g>1e-6*max(1,abs(f))): return None
    return 1.0 if LB==math.inf else min(max((LB-LB0)/g,0),1)
a=[];b=[]
for n in inst.index:
    if (n,'grb') in ob and (n,'known') in ob:
        rg,rk=ob[(n,'grb')]['trajs']['full'],ob[(n,'known')]['trajs']['full']
        x=gc(rg['hist'][-1]['LB'],rg['LB0'],FS[n]); y=gc(rk['hist'][-1]['LB'],rk['LB0'],FS[n])
        if x is not None and y is not None: a.append(x); b.append(y)
print('both cutoffs',len(a),np.mean(a),np.mean(b))
for s in ('known','grb','scip'):
    R=[r for (n,ss),r in ob.items() if ss==s]
    t1=sum(r['trajs']['full']['snaps']['r1']['time'] for r in R); ta=sum(r['trajs']['restr']['snaps']['ad0.8']['time'] for r in R)
    t1s=np.exp(np.mean(np.log([r['trajs']['full']['snaps']['r1']['time']+1 for r in R]))); tas=np.exp(np.mean(np.log([r['trajs']['restr']['snaps']['ad0.8']['time']+1 for r in R])))
    print(s,'ad0.8/r1 sum time %.3f  sgm %.3f'%(ta/t1,tas/t1s))
