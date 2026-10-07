import numpy as np, sys
sys.path.insert(0,'..')
import chain_model as cm
import mpmath as mp
from scipy.optimize import minimize
def Gint(v,H):
    g=np.hypot(H,v); return 0.5*(v*g+H*H*np.arcsinh(v/H))
def D(p,z1,zN,L,W):
    H,V=p
    return (V+L)*zN-V*z1+H*W-(Gint(V+L,H)-Gint(V,H))
def dualmax(z1,zN,L,W,p0):
    # Newton on gradient
    H,V=p0
    for it in range(60):
        g1=np.hypot(H,V+L); g0=np.hypot(H,V)
        dV=zN-z1-(g1-g0)
        dH=W-H*(np.arcsinh((V+L)/H)-np.arcsinh(V/H))
        # Hessian
        hVV=-((V+L)/g1-V/g0)
        # d/dH of -(g1-g0) = -(H/g1-H/g0)
        hVH=-(H/g1-H/g0)
        # d/dH of W - H*(asinh(b/H)-asinh(a/H)) : -(asinh(b/H)-asinh(a/H)) - H*( -b/(H*g1) + a/(H*g0))
        hHH=-(np.arcsinh((V+L)/H)-np.arcsinh(V/H)) + ((V+L)/g1 - V/g0)
        Hm=np.array([[hHH,hVH],[hVH,hVV]]); gr=np.array([dH,dV])
        st=np.linalg.solve(Hm,-gr)
        t=1.0
        while H+t*st[0]<=0: t/=2
        H,V=H+t*st[0],V+t*st[1]
        if np.max(np.abs(st))<1e-15: break
    return D((H,V),z1,zN,L,W),(H,V)
for N in [int(a) for a in sys.argv[1:]]:
    z,mu,_=cm.solve(N)
    fstar=float(cm.lag_grad_hess(z,mu,N,mp.mpf(1)/N,mp.mpf,mp.sqrt)[0]-mu*4)
    h=1.0/N; W=1-h
    zf=[float(v) for v in z]
    state={'p':(0.16,-0.95)}
    def F(q):
        z1,zN=q
        l0=np.hypot(h/2,z1-1); lN=np.hypot(h/2,3-zN); L=4-l0-lN
        val,p=dualmax(z1,zN,L,W,state['p']); state['p']=p
        return l0+3*lN+val
    # start from discrete optimum
    q0=np.array([zf[0],zf[-1]])
    # compute p0 at q0 with a decent start: continuous catenary H ~ .164, V ~ vertical tension after piece 0
    l0=np.hypot(h/2,zf[0]-1); 
    state['p']=(0.164,-0.99+l0)
    F0=F(q0)
    res=minimize(F,q0,method='Nelder-Mead',options=dict(xatol=1e-12,fatol=1e-15,maxiter=4000))
    print(N,'f*=%.12f'%fstar,'F(q*)=%.12f'%F0,'min F=%.12f'%res.fun,'gap=%.3e'%(fstar-res.fun),'q*',q0,'qmin',res.x,'p',state['p'])
