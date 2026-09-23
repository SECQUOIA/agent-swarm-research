import numpy as np, gurobipy as gp
from numpy.polynomial import legendre as L
env=gp.Env(empty=True); env.setParam('OutputFlag',0); env.start()
def f(t): return 1/np.sqrt(2-2*t)
def bound(N,K=40,grid=4000):
    t=np.concatenate([np.linspace(-1,0.999,grid), 1-np.logspace(-3,-12,50)])
    P=np.array([L.legval(t,np.eye(K+1)[k]) for k in range(K+1)]).T  # P_k(t), P_k(1)=1
    m=gp.Model(env=env); h=m.addVars(K+1,lb=[-gp.GRB.INFINITY]+[0]*K)
    for i in range(len(t)): m.addConstr(gp.quicksum(P[i,k]*h[k] for k in range(K+1))<=f(t[i]))
    m.setObjective((N*N*h[0]-N*gp.quicksum(h[k] for k in range(K+1)))/2, gp.GRB.MAXIMIZE); m.optimize()
    hv=np.array([h[k].X for k in range(K+1)])
    # certification-style check on a very fine grid with Lipschitz margin
    tt=np.linspace(-1,1-1e-9,2_000_001); hv_t=L.legval(tt,hv)
    Lip=sum(hv[k]*k*(k+1)/2 for k in range(K+1)); dt=tt[1]-tt[0]
    # on [tt_i, tt_{i+1}]: h <= h(tt_i)+Lip*dt, f >= f(tt_i) (f increasing)
    viol=max(0.0,np.max(hv_t[:-1]+Lip*dt-f(tt[:-1])))
    # last cell near 1: f huge, h bounded by sum hv
    h0c=hv[0]-viol
    val=(N*N*h0c-N*(hv.sum()-viol))/2
    return m.ObjVal,val,viol
for N,pr,du in [(25,243.8127603,90.22758027),(50,1055.182315,359.0296983),(100,4448.350634,1429.500306),(200,18438.87685,5744.71434)]:
    for K in (20,40,60):
        lp,val,viol=bound(N,K)
        print(N,K,'LP',round(lp,3),'safe',round(val,3),'viol',f'{viol:.1e}','primal',pr,'listed dual',du,'new gap %.2f%%'%(100*(pr-val)/val),flush=True)
