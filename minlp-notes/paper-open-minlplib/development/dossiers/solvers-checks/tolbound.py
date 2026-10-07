# Worst-case objective deficit of camshape points that violate rows/bounds by at most eps (dossier check).
import sys; sys.set_int_max_str_digits(0)
exec(open('cambound.py').read().replace("if __name__=='__main__':","if False:"))
from fractions import Fraction as F
def bound_eps(path,eps):
    eqs,lo,up=parse(path)
    obj=[n for n,(mon,s,r) in eqs.items() if ('objvar',) in mon][0]
    mon,s,rhs=eqs[obj]; a=mon[('objvar',)]
    rv=sorted([k[0] for k in mon if k!=('objvar',)],key=lambda v:int(v[1:]))
    coef={v:-mon[(v,)]/a for v in rv}; const=rhs/a
    n=len(rv); idx={v:i+1 for i,v in enumerate(rv)}
    # reuse structure checks from bound()
    nn,c,val0,inb,minS,a1=bound(path)
    # slope alphas
    alpha={}
    for name,(m,s_,r) in eqs.items():
        if s_=='E' and name!=obj and len(m)==3 and all(len(k)==1 for k in m) and r==0:
            vs=[k[0] for k in m]; rs=[v for v in vs if v in idx]; sv=[v for v in vs if v not in idx]
            if len(rs)==2 and len(sv)==1:
                a1_=min(rs,key=lambda v:idx[v]); u_=up.get(sv[0])
                alpha[idx[a1_]]=None if u_ is None else u_+2*eps   # |r_{j+1}-r_j| <= alpha+eps (bound) + eps (row)
    ub=[None]+[up[v]+eps for v in rv]
    delta=eps/(1-eps)**3          # u-space residual of a row violated by eps when r >= 1-eps
    U=[F(1),c]
    for m in range(2,n): U.append(c*U[-1]-U[-2])
    W=[F(0)]*(n+1); acc=F(0)
    for j in range(2,n+1):
        acc+=U[j-2]; W[j]=acc
    S=[F(1),1/ub[1]]
    for j in range(1,n): S.append(c*S[j]-S[j-1])
    Q=10**60; B=[None]
    for j in range(1,n+1):
        L=S[j]-delta*W[j]
        if L>0:
            Rj=1/L; Rj=F(-((-Rj.numerator*Q)//Rj.denominator),Q); B.append(min(ub[j],Rj))
        else: B.append(ub[j])
    E=B[:]
    for j in range(2,n+1):
        if alpha[j-1] is not None: E[j]=min(E[j],E[j-1]+alpha[j-1])
    for j in range(n-1,0,-1):
        if alpha[j] is not None: E[j]=min(E[j],E[j+1]+alpha[j])
    val=const+sum(coef[rv[j-1]]*E[j] for j in range(1,n+1))
    return val0,val,max(U),max(W)
cases=[('camshape100.gms','1e-10','5.2581469e-7','BARON (claim)'),('camshape100.gms','7.72e-10','1.5191022e-7','SCIP'),
       ('camshape200.gms','1e-10','2.05270746e-6','BARON (claim)'),('camshape400.gms','1e-10','8.15450068e-6','BARON'),
       ('camshape400.gms','3e-10','8.15e-6','MINLPLib p2'),('camshape800.gms','3e-10','3.27e-5','MINLPLib p2'),
       ('camshape800.gms','3.32e-7','0.09365569719715','BARON'),('camshape800.gms','9.75e-7','0.02328447110410','GUROBI')]
for p,e,obs,who in cases:
    v0,v,mU,mW=bound_eps(p,F(e))
    print(f"{p} eps={e}: max admissible deficit {float(v0-v):.4e}  observed {who} {float(obs):.4e}  ratio obs/max {float(F(obs)/(v0-v)):.3f}  maxU={float(mU):.1f} maxW={float(mW):.4g}",flush=True)
