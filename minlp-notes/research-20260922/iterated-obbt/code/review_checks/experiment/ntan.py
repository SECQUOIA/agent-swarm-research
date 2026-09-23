import sys, math, numpy as np, pandas as pd
sys.path.insert(0,'/home/sgusev/repo/minlp-notes/research-20260922/iterated-obbt/code')
from qcqp import QCQP
import relax, gurobipy as gp
RES='/home/sgusev/repo/minlp-notes/research-20260922/iterated-obbt/results'
inst=pd.read_csv(RES+'/instances.csv').set_index('name')
env=gp.Env(params={'OutputFlag':0})
for name in sys.argv[1:]:
    P=QCQP(name); f=np.load(RES+'/fbbt/%s.npz'%name); lb,ub=f['lb'],f['ub']
    fs=inst.loc[name,'fstar_min']; U=fs+1e-6*max(1,abs(fs)); nl=np.array(P.nlvars)
    res=[]
    for nt in (5,65):
        relax.NTAN=nt
        R=relax.Relaxation(P,lb,ub,env,U); LB0,_=R.bound()
        out=relax.iterate(R,max_rounds=50,time_cap=60)
        LB=out['hist'][-1]['LB']; g=fs-LB0
        res.append((nt,LB0,LB,(R.ub-R.lb)[nl].sum()/(ub-lb)[nl].sum(),len(out['hist'])))
    print(name,'nsq',sum(1 for t in P.terms if t[0]==t[1]),res)
