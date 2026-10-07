import numpy as np, sys
sys.path.insert(0,'..')
import chain_model as cm
import mpmath as mp
N=int(sys.argv[1]); delta=float(sys.argv[2])
z,mu,_=cm.solve(N)
fstar=float(cm.lag_grad_hess(z,mu,N,mp.mpf(1)/N,mp.mpf,mp.sqrt)[0]-mu*4)
h=1.0/N
zf=np.array([1.0]+[float(v) for v in z]+[3.0])  # heights y_0..y_{N+1} of Q_0..Q_{N+1}
dt=np.array([h/2]+[h]*(N-1)+[h/2])
dy=np.diff(zf); lam=np.hypot(dt,dy); sig=np.concatenate([[0],np.cumsum(lam)])
a=np.array([1.0]+[0.5]*(N-1)+[0.0])
print('sum lam',sig[-1],'f*',fstar)
# tension from KKT: V_k parallel to dy_k: find V_b that best matches sign; print V_k/dy_k ratios
def J(Vb):
    g=np.arange(0,4+delta/2,delta)  # sigma grid
    val=np.full(g.shape,-np.inf); val[0]=0.0
    for k in range(N+1):
        new=np.full(g.shape,-np.inf)
        for i0 in range(0,len(g),400):
            s=g[i0:i0+400,None]; v=val[i0:i0+400,None]
            L=g[None,:]-s
            ok=L>=dt[k]
            r=np.sqrt(np.where(ok,L*L-dt[k]**2,0))
            rew=np.abs(Vb+s+a[k]*L)*r
            c=np.where(ok,v+rew,-np.inf)
            new=np.maximum(new,c.max(axis=0))
        val=new
    return val[-1]
# exact value of the sum at the optimal config for given Vb
def at_opt(Vb):
    V=Vb+sig[:-1]+a*lam
    return np.sum(np.abs(V)*np.abs(dy)), np.sum(-V*dy)
for Vb in np.linspace(-1.02,-0.96,7):
    Jg=J(Vb); ao=at_opt(Vb)
    print('Vb=%.4f bound(grid)=%.6f  f*=%.6f  12+2Vb-sum|V|r at opt=%.6f  12+2Vb+sum(-V dy)=%.6f'%(Vb,12+2*Vb-Jg,fstar,12+2*Vb-ao[0],12+2*Vb+ao[1]))
