"""Independent exact checks written directly from Stage4 formulas."""
import itertools, json
from pathlib import Path
import sympy as s
Q=s.Rational
counts={'dense_queries':0,'cross_schur':0,'mixture_order':0}

def schur(M,p):
    return M[:p,:p] if M.rows==p else M[:p,:p]-M[:p,p:]*M[p:,p:].inv()*M[p:,:p]

def psd(M):
    for k in range(1,M.rows+1):
        for I in itertools.combinations(range(M.rows),k):
            assert M.extract(I,I).det()>=0, M

for rho in (Q(-2,3),Q(0),Q(2,3)):
    n=4; P=Q(3,2); r=Q(1); a=Q(6,5)
    K=s.Matrix(n,n,lambda i,j:P*rho**abs(i-j)); R=K+r*s.eye(n)
    psd(R-a*s.eye(n))
    F=s.Matrix([[1,-2],[3,0],[-1,4],[2,3]])/3
    J0=s.Matrix([[2,1],[1,3]])/5
    for zs in itertools.product((Q(0),Q(1,3),Q(1)),repeat=n):
        Z=s.diag(*[z/a for z in zs]); Vr=(s.eye(n)+(R-a*s.eye(n))*Z).inv()*F
        Jr=J0+F.T*Z*Vr
        pred=P; mean=s.zeros(1,2); Ji=J0; cache=[]
        for i,z in enumerate(zs):
            beta=a*(1-z)+r*z; e=F[i,:]-mean; q=z*pred+beta; w=z/q
            assert a/q<=1
            Ji+=w*e.T*e
            cache.append((pred,e,q,beta,w))
            mean=rho*(mean+pred*w*e)
            pred=rho*rho*pred*beta/q+P*(1-rho*rho)
        adj=s.zeros(1,2); Vi=s.zeros(n,2)
        for i in reversed(range(n)):
            pred,e,q,beta,w=cache[i]
            Vi[i,:]=(a/q)*(e-rho*pred*adj)
            adj=w*e+rho*beta/q*adj
        assert Ji==Jr and Vi==Vr
        counts['dense_queries']+=1

# Nonstationary, signed transitions: all selected sets and all nested anchor pairs.
n=4; p=2; trans=[Q(-1,2),Q(2,3),Q(-3,4)]; proc=[Q(1),Q(1,3),Q(2,5),Q(1,2)]
T=s.eye(n)
for i in range(1,n):
    for j in range(i): T[i,j]=trans[i-1]*T[i-1,j]
K=T*s.diag(*proc)*T.T; R=K+Q(2,3)*s.eye(n)
F=s.Matrix([[1,0],[1,1],[2,-1],[-1,3]]); J0=s.eye(p)
sets=[tuple(i for i in range(n) if mask>>i&1) for mask in range(1<<n)]

def augmented(A,S):
    if A:
        KA=K.extract(A,A); H=K[:,list(A)]*KA.inv(); D=R-H*K[list(A),:]
        base=s.diag(J0,KA.inv()); load=F.row_join(H)
    else: D=R; base=J0; load=F
    if not S:return base
    L=load.extract(S,range(load.cols))
    return base+L.T*D.extract(S,S).inv()*L

cache={(A,S):augmented(A,S) for A in sets for S in sets}
for A in sets:
    for B in sets:
        if not set(A)<=set(B):continue
        order=list(range(p))+[p+B.index(i) for i in A]+[p+B.index(i) for i in B if i not in A]
        for S in sets:
            MB=cache[B,S].extract(order,order)
            assert schur(MB,p+len(A))==cache[A,S]
            counts['cross_schur']+=1
        SA=(0,2); SB=(1,3)
        MA=(cache[A,SA]+2*cache[A,SB])/3
        MB=(cache[B,SA]+2*cache[B,SB])/3
        psd(schur(MB,p)-schur(MA,p))
        counts['mixture_order']+=1

Path(__file__).with_name('result.json').write_text(json.dumps(counts,indent=2)+'\n')
print(counts)
