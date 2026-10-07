import numpy as np, sys
sys.path.insert(0,'..')
import chain_model as cm
import mpmath as mp
N=int(sys.argv[1]); delta=float(sys.argv[2])
z,mu,_=cm.solve(N)
fstar=float(cm.lag_grad_hess(z,mu,N,mp.mpf(1)/N,mp.mpf,mp.sqrt)[0]-mu*4)
mu=float(mu); h=1.0/N
y=np.array([1.0]+[float(v) for v in z]+[3.0])
dt=np.array([h/2]+[h]*(N-1)+[h/2])
dy=np.diff(y); lam=np.hypot(dt,dy); sig=np.concatenate([[0],np.cumsum(lam)])
a=np.array([1.0]+[0.5]*(N-1)+[0.0])
eta=np.concatenate([[1.0],(y[1:N]+y[2:N+1])/2,[3.0]])
Tmag=eta+mu
V=Tmag*dy/lam; H=Tmag*dt/lam
Vb=V[0]-sig[0]-a[0]*lam[0]
print('Vb',Vb,'check V recursion', np.max(np.abs(V-(Vb+sig[:-1]+a*lam))))
print('H range',H.min(),H.max(),'H[0],H[N]',H[0],H[-1])
rhs=12+2*Vb+np.sum(H*dt-lam*np.hypot(H,V))
print('RHS(lam*)',rhs,'f*',fstar)
def dp(Hk,Vb):
    g=np.arange(0,4+delta/2,delta)
    val=np.full(g.shape,np.inf); val[0]=0.0
    for k in range(N+1):
        new=np.full(g.shape,np.inf)
        for i0 in range(0,len(g),400):
            s=g[i0:i0+400,None]; v=val[i0:i0+400,None]
            L=g[None,:]-s
            ok=L>=dt[k]-1e-15
            c=Hk[k]*dt[k]-L*np.hypot(Hk[k],Vb+s+a[k]*L)
            c=np.where(ok,v+c,np.inf)
            new=np.minimum(new,c.min(axis=0))
        val=new
    return 12+2*Vb+val[-1]
print('DP bound with KKT H_k:',dp(H,Vb))
Hc=np.full(N+1,np.median(H))
print('DP bound with const H:',dp(Hc,Vb))
