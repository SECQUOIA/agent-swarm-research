"""Box QP (max 0.5 x'Qx + c'x on [0,1]^n): declare variables with Q_ii >= 0 binary (mode bin), optionally add
pairwise second-order cuts (mode bin2).  Usage: boxqp_binarize.py <spar file> <orig|bin|bin2> <time limit> <threads>
Instances: https://github.com/sburer/BoxQP_instances"""
import sys, time, numpy as np, gurobipy as gp
def load(fn):
    tok=open(fn).read().split(); n=int(tok[0]); v=np.array(tok[1:],float)
    return n, v[:n], v[n:n+n*n].reshape(n,n)
fn=sys.argv[1]; mode=sys.argv[2]; TL=float(sys.argv[3]); thr=int(sys.argv[4])
n,c,Q=load(fn)
m=gp.Model(); m.Params.OutputFlag=0; m.Params.TimeLimit=TL; m.Params.Threads=thr; m.Params.NonConvex=2; m.Params.MIPGap=1e-4
nb=0
if mode=="orig":
    x=m.addMVar(n,lb=0,ub=1)
else:
    vt=["B" if Q[i,i]>=0 else "C" for i in range(n)]; nb=vt.count("B")
    x=m.addMVar(n,lb=0,ub=1,vtype=vt)
m.setObjective(0.5*(x@Q@x)+c@x, gp.GRB.MAXIMIZE)
if mode=="bin2":
    # pairwise second-order cuts on free indicators for Q_ii<0 vars
    neg=[i for i in range(n) if Q[i,i]<0]
    pairs=[(i,j) for a,i in enumerate(neg) for j in neg[a+1:] if Q[i,i]*Q[j,j]<Q[i,j]**2]
    inv=sorted({i for p in pairs for i in p})
    t={i:m.addVar(vtype="B") for i in inv}; u={i:m.addVar(vtype="B") for i in inv}
    for i in inv:
        m.addConstr(x[i]>=u[i]); m.addConstr(x[i]<=u[i]+t[i]); m.addConstr(u[i]+t[i]<=1)
    for i,j in pairs: m.addConstr(t[i]+t[j]<=1)
t0=time.time(); m.optimize()
import json
print(json.dumps(dict(instance=fn.split('/')[-1], mode=mode, nbin=nb, status=m.Status, obj=m.ObjVal, bound=m.ObjBound, nodes=m.NodeCount, time=time.time()-t0)))
#print(f"{fn.split('/')[-1]} {mode} nbin={nb} status={m.Status} obj={m.ObjVal:.3f} bound={m.ObjBound:.3f} nodes={m.NodeCount:.0f} t={time.time()-t0:.1f}",flush=True)
