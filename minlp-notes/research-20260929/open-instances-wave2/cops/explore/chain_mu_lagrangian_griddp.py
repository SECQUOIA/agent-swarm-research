import numpy as np, sys
sys.path.insert(0,'..')
import chain_model as cm
import mpmath as mp
N=int(sys.argv[1]); delta=float(sys.argv[2])
z,mu,_=cm.solve(N)
fstar=float(cm.lag_grad_hess(z,mu,N,mp.mpf(1)/N,mp.mpf,mp.sqrt)[0]-mu*4)
mu=float(mu); h=1.0/N
zs=np.array([float(v) for v in z])
A=np.array([0,1.]); B=np.array([1,3.])
def ell_range(t):
    # y range with |P-A|+|P-B|<=4 at abscissa t
    ys=np.linspace(-1,5,600001)
    s=np.hypot(t-A[0],ys-A[1])+np.hypot(t-B[0],ys-B[1])
    ok=ys[s<=4]; return ok.min(), ok.max()
def run(mu):
    V=None; grids=[]
    for i in range(1,N+1):
        t=(i-0.5)*h; lo,hi=ell_range(t)
        g=np.arange(lo,hi,delta); grids.append(g)
    g=grids[0]; V=0.5*np.hypot(h,2*g-2)*(1+mu)
    for i in range(1,N):
        g2=grids[i]
        best=np.full(g2.shape,np.inf)
        for k0 in range(0,len(g),500):
            gz=g[k0:k0+500,None]; 
            c=V[k0:k0+500,None]+np.hypot(h,g2[None,:]-gz)*((gz+g2[None,:])/2+mu)
            best=np.minimum(best,c.min(axis=0))
        V=best; g=g2
    tot=V+0.5*np.hypot(h,6-2*g)*(3+mu)
    k=np.argmin(tot)
    return tot[k]-4*mu, g[k]
print('fstar',fstar,'mu*',mu,'ellipse lo at t=0.3', ell_range(0.3))
mus=[float(v) for v in sys.argv[3:]] or [mu, mu*0.5, mu*1.5, mu*2, mu*3, 0.0, 0.05]
for m in mus:
    d,zN=run(m); print('mu=%.5f d=%.6f  (d-f*=%.2e) zN=%.4f zN*=%.4f'%(m,d,d-fstar,zN,zs[-1]))
