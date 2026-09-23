import numpy as np, gurobipy as gp
ENV=gp.Env(empty=True); ENV.setParam('OutputFlag',0); ENV.start()
def geg(deg,a,t):
    t=np.asarray(t,float); C=[np.ones_like(t),2*a*t]
    for k in range(2,deg+1): C.append((2*t*(k+a-1)*C[-1]-(k+2*a-2)*C[-2])/k)
    return C
def lp(n,s,deg=24,grid=3000):
    a=(n-2)/2; t=np.linspace(-1,s,grid); C=geg(deg,a,t); C1=geg(deg,a,[1.0])
    A=np.array([C[k]/C1[k][0] for k in range(1,deg+1)]).T
    m=gp.Model(env=ENV)
    f=m.addVars(deg,lb=0)
    for i in range(A.shape[0]): m.addConstr(gp.LinExpr(A[i].tolist(),[f[k] for k in range(deg)])<=-1)
    m.setObjective(f.sum()); m.optimize()
    return 1+m.ObjVal if m.Status==2 else np.inf
def smin(n,N):
    lo,hi=-0.99,0.999
    for _ in range(40):
        mid=(lo+hi)/2
        if lp(n,mid)>=N: hi=mid
        else: lo=mid
    return hi
for n,N,ld,pr in [(3,12,2.280669,1.105573),(4,24,3.676075,1.0),(5,40,4.0,0.9848552),(5,41,4,0.9688859),(5,42,4,0.9600717),(5,43,4,0.9475223),(5,44,4,0.9450841)]:
    s=smin(n,N); print(f'knp{n}-{N}: LP bound obj <= {2*(1-s):.4f}  (listed dual {ld}, listed primal {pr})',flush=True)
