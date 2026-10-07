import numpy as np, sys
from scipy.optimize import minimize, minimize_scalar
E=np.array([[1.0,0],[0,0]])
def M(s): return np.array([[s[2],s[0]],[s[1],1.0]])
def sym(A): return 0.5*(A+A.T)
def lmin(A):
    a,b,c=A[0,0],A[0,1],A[1,1]
    return 0.5*(a+c)-np.sqrt(0.25*(a-c)**2+b*b)
def Xof(u):
    ph,al,b=u
    a=np.exp(al)
    R=np.array([[np.cos(ph),-np.sin(ph)],[np.sin(ph),np.cos(ph)]])
    return R@np.array([[a,b],[0,1/a]])
def maxconc(f,lo,hi):
    # maximize concave f on [lo,hi] by golden section
    gr=(np.sqrt(5)-1)/2
    a,b=lo,hi
    for _ in range(80):
        m1,m2=b-gr*(b-a),a+gr*(b-a)
        if f(m1)>=f(m2): b=m2
        else: a=m1
    return max(f(lo),f(hi),f(0.5*(a+b)))
def mB(X,s):
    A=sym(X@M(s)); Z=sym(X@E); qs=s[2]-s[0]*s[1]
    f=lambda t: lmin(A-t*Z)
    return maxconc(f,0.0,max(qs,0.0))
def mLine(X,rho):
    A0=sym(X@M((rho,rho,0.0))); Z=sym(X@E)
    f=lambda h: lmin(A0+h*Z)
    return maxconc(f,rho*rho,rho*rho+1e7)
def slacks(X,rho,H,k=2.0):
    nX=np.abs(X).max()
    out=[]
    pts=[(0,0,1.0),(rho,-rho,1.0),(rho,-k*rho,1.0)]
    if H is not None: pts.append((rho,rho,1.0+H))
    for s in pts:
        out.append(mB(X,s)/(nX*(1+abs(s[0])+abs(s[1])+abs(s[2]))))
    if H is None:
        out.append(mLine(X,rho)/(nX*(1+2*rho)))
    return np.array(out)
def best(rho,H,nstart=40,seed=0,X0s=()):
    rng=np.random.default_rng(seed)
    bv=-np.inf;bu=None
    f=lambda u: -slacks(Xof(u),rho,H).min()
    starts=[np.array([rng.uniform(-np.pi,np.pi),rng.normal()*3,rng.normal()*5]) for i in range(nstart)]
    for u0 in starts:
        r=minimize(f,u0,method='Nelder-Mead',options=dict(maxiter=3000,xatol=1e-12,fatol=1e-15))
        if -r.fun>bv: bv=-r.fun;bu=r.x
    return bv,bu
if __name__=='__main__':
    H=None if sys.argv[1]=='inf' else float(sys.argv[1])
    for rho in [float(a) for a in sys.argv[2:]]:
        v,u=best(rho,H)
        print('H',H,'rho',rho,'max min slack %.3e'%v,'X',np.round(Xof(u),6).tolist(),flush=True)
