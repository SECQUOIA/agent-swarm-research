import numpy as np, itertools
from scipy.optimize import linprog
rng=np.random.default_rng(0)
n=5
for trial in range(5):
    b=rng.normal(size=n); l=rng.uniform(-2,0,n); u=l+rng.uniform(.5,2,n); x=l+(u-l)*rng.uniform(size=n)
    V=np.array(list(itertools.product(*[[l[i],u[i]] for i in range(n)])))
    f=(V@b)**2
    res=linprog(-f,A_eq=np.vstack([V.T,np.ones(len(V))]),b_eq=np.append(x,1),bounds=(0,None),method='highs')
    conc=-res.fun
    # staircase with flips: coordinate "high" end = u if b>0 else l
    hi=np.where(b>0,u,l); lo=np.where(b>0,l,u); p=(x-lo)/(hi-lo)
    o=np.argsort(-p); v=lo.copy(); pk=np.concatenate([[1.],p[o],[0.]]); val=0
    for k in range(n+1):
        if k>0: v[o[k-1]]=hi[o[k-1]]
        val+=(pk[k]-pk[k+1])*(b@v)**2
    L=min((V@b)); U=max(V@b); t=b@x; secant=(L+U)*t-L*U
    print(f"LP concave env={conc:.6f} staircase={val:.6f} univariate secant={secant:.6f} (b^T x)^2={t*t:.6f}")
