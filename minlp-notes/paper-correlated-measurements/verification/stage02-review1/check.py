"""Independent exact checks of Stage 2; does not import manuscript producer code."""
import itertools
import json
from pathlib import Path
import sympy as s

q = s.Rational
I = s.eye(2)
As = [s.Matrix([[q(1,3), q(1,4)], [0,q(1,5)]]),
      s.Matrix([[q(1,5),0], [-q(1,4), q(1,3)]]),
      s.diag(q(1,3),0),
      s.Matrix([[0,q(1,3)],[-q(1,4),0]])]
n = 5
def psd2(M):
    assert M == M.T and M[0,0] >= 0 and M[1,1] >= 0 and M.det() >= 0
for A in As:
    psd2(I/4-A*A.T)
assert As[0]*As[1] != As[1]*As[0]
def phi(t,j):
    out=I
    for u in range(j,t): out=As[u]*out
    return out
R=s.zeros(2*n)
for t in range(n):
    for j in range(n):
        R[2*t:2*t+2,2*j:2*j+2] = (2*I if t==j else phi(t,j) if t>j else phi(j,t).T)
def inds(H): return [a for j in H for a in (2*j,2*j+1)]
def residual(S,t,L):
    H=[j for j in S if t-L <= j < t]
    E=s.zeros(2,2*n); E[:,2*t:2*t+2]=I
    if H:
        b=R.extract(inds([t]),inds(H))*R.extract(inds(H),inds(H)).inv()
        for pos,j in enumerate(H): E[:,2*j:2*j+2]=-b[:,2*pos:2*pos+2]
    return E,H
counts={'far_identity':0,'far_bound':0,'markov_paths':0,'forward_reverse':0}
for bits in itertools.product((False,True),repeat=n):
    S=[i for i,v in enumerate(bits) if v]
    for L in range(4):
        cache={t:residual(S,t,L) for t in S}
        for t in S:
            Et,Ht=cache[t]
            for j in S:
                if j>=t-L: continue
                Ej,Hj=cache[j]
                cov=Et*R*Ej.T
                # Direct prediction covariance at j from its local selected past.
                D=Ej*R*Ej.T
                predj=D-I
                # Fresh t-local filter, started at j with unconditional covariance I.
                P=I; T=I
                for u in range(j,t):
                    if u in Ht:
                        gain=P*(P+I).inv()
                        T=(I-gain)*T
                        P=P-P*(P+I).inv()*P
                    T=As[u]*T
                    P=As[u]*P*As[u].T+I-As[u]*As[u].T
                assert cov==T*predj
                counts['far_identity']+=1
                bound=q(1,2)**(t-j)
                psd2(bound**2*I-cov*cov.T)
                counts['far_bound']+=1

# Noiseless complete-state exact path identities, including a singular A.
K=R-s.eye(2*n)
F=s.Matrix([[q((i+1)*(j+2)%7-3,5) for j in range(3)] for i in range(2*n)])
for bits in itertools.product((False,True),repeat=n):
    S=[i for i,v in enumerate(bits) if v]
    if not S: continue
    Fs=F.extract(inds(S),range(3))
    direct=Fs.T*K.extract(inds(S),inds(S)).inv()*Fs
    first=F[2*S[0]:2*S[0]+2,:]
    total=first.T*first
    for i,j in zip(S,S[1:]):
        Fi=F[2*i:2*i+2,:]; Fj=F[2*j:2*j+2,:]
        A=phi(j,i); Omega=I-A*A.T
        plus=(Fj-A*Fi).T*Omega.inv()*(Fj-A*Fi)
        minus=(Fi-A.T*Fj).T*(I-A.T*A).inv()*(Fi-A.T*Fj)
        assert Fi.T*Fi+plus==minus+Fj.T*Fj
        counts['forward_reverse']+=1
        total+=plus
    assert direct==total
    counts['markov_paths']+=1

# Scalar nonstationary near-pair boundary and finite-window random intercept.
Rs=s.Matrix([[2,q(1,2),q(1,4)],[q(1,2),q(5,4),q(1,8)],[q(1,4),q(1,8),q(17,16)]])
assert (s.Matrix([[0,-q(1,10),1]])*Rs*s.Matrix([-q(1,4),1,0]))[0]==-q(1,20)
for nn in range(1,10):
    for L in range(nn+1):
        calc=sum(q(1,(min(t,L)+1)*(min(t,L)+2)) for t in range(nn))
        if nn>=L: assert calc==q(L,L+1)+q(nn-L,(L+1)*(L+2))
counts['exact_scalar_boundary']=1
counts['random_intercept_formulas']=sum(nn+1 for nn in range(1,10))
out=Path(__file__).with_name('results.json')
out.write_text(json.dumps({'passed':True,'checks':counts},indent=2)+'\n')
print(out.read_text())
