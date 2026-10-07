# Own minimal reader for QPLIB (.qplib) files of type LCQ/DCQ (continuous vars).
# Convention (QPLIB docs): objective 0.5 x'Q0x + b0'x + c; constraint i: cl_i <= 0.5 x'Q_i x + b_i'x <= cu_i,
# quadratic terms given as lower-triangle entries (i>=j); off-diagonal entry q means q*x_i*x_j, diagonal q means 0.5*q*x_i^2.
from fractions import Fraction as Fr
def read(path):
    L=[l.split('#')[0].strip() for l in open(path)]
    L=[l for l in L if l!='']
    it=iter(L)
    name=next(it); typ=next(it); sense=next(it)
    n=int(next(it)); m=int(next(it)) if typ[2] in 'QLB' and typ[2]!='N' else 0
    obj={}; objq=[]
    if typ[0] in 'QC':  # quadratic objective
        k=int(next(it))
        for _ in range(k):
            i,j,v=next(it).split(); objq.append((int(i),int(j),Fr(v)))
    dflt=Fr(next(it)); k=int(next(it))
    objlin={i:dflt for i in range(1,n+1)}
    for _ in range(k):
        i,v=next(it).split(); objlin[int(i)]=Fr(v)
    objc=Fr(next(it))
    cq=[]; cl=[]
    if typ[2] in 'QC':
        k=int(next(it))
        for _ in range(k):
            r,i,j,v=next(it).split(); cq.append((int(r),int(i),int(j),Fr(v)))
    k=int(next(it))
    for _ in range(k):
        r,i,v=next(it).split(); cl.append((int(r),int(i),Fr(v)))
    inf=float(next(it))
    def vec(cnt):
        d=next(it); dv=float(d); k=int(next(it)); out={i:dv for i in range(1,cnt+1)}
        for _ in range(k):
            i,v=next(it).split(); out[int(i)]=float(v) if abs(float(v))<inf else (float('inf') if float(v)>0 else -float('inf'))
        if abs(dv)>=inf:
            out={i:(v if abs(v)<inf else (float('inf') if v>0 else -float('inf'))) for i,v in out.items()}
        return out
    def vecraw(cnt):
        d=next(it); k=int(next(it)); out={i:d for i in range(1,cnt+1)}
        for _ in range(k):
            i,v=next(it).split(); out[int(i)]=v
        return out
    lhs=vecraw(m); rhs=vecraw(m); lb=vecraw(n); ub=vecraw(n)
    return dict(n=n,m=m,objlin=objlin,objq=objq,objc=objc,cq=cq,cl=cl,lhs=lhs,rhs=rhs,lb=lb,ub=ub,inf=inf)
