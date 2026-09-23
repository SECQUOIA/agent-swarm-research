from itertools import combinations
import json
from pathlib import Path
import sympy as s
Q=s.Rational

def psd(M):
    assert M==M.T
    M=M.copy()
    while M.rows:
        if M[0,0]<0:return False
        if M[0,0]==0:
            if any(M[0,j]!=0 for j in range(1,M.cols)):return False
            M=M[1:,1:]
        else:M=M[1:,1:]-M[1:,0]*M[0,1:]/M[0,0]
    return True

def T(n):return Q(2,5)**(n+1)/(1-Q(2,5))
def near(n):
    x=Q(2,5)
    return sum(x**(h+2*d) for h in range(1,n+1) for d in range(n+1-h,n+1))

# Singular rank-two latent covariance with a changing nonorthogonal ambient
# coordinate system, noncommuting transitions, varying packet sizes, and
# nondiagonal observation noise. Covariance is built directly from transitions.
n=6; rho=Q(2,5); Pbase=s.diag(1,1,0)
Ts=[s.Matrix([[1,Q(t+1,7),0],[0,1,Q(t-2,8)],[Q(1,9),0,1]]) for t in range(n)]
Us=[s.Matrix([[0,-1,0],[1,0,0],[0,0,1]]) if t%2 else s.diag(1,-1,1) for t in range(n)]
Ps=[M*Pbase*M.T for M in Ts]
As=[None]+[rho*Ts[t]*Us[t]*Ts[t-1].inv() for t in range(1,n)]
Hs=[s.Matrix([[1,Q(t-2,5),Q(1,3)]]) if t%2==0 else s.Matrix([[1,Q(1,2),0],[Q(t,8),-1,Q(2,3)]]) for t in range(n)]
Vs=[H*P*H.T+s.eye(H.rows) for H,P in zip(Hs,Ps)]
assert all(P.rank()==2 for P in Ps)
assert all(psd(Ps[t]-As[t]*Ps[t-1]*As[t].T-(1-rho**2)*Ps[t]) for t in range(1,n))
Ks={}
for t in range(n):
    Ks[t,t]=Ps[t]
    for j in range(t):Ks[t,j]=As[t]*Ks[t-1,j];Ks[j,t]=Ks[t,j].T
Rb={(t,j):Hs[t]*Ks[t,j]*Hs[j].T+(Vs[t] if t==j else s.zeros(Hs[t].rows,Hs[j].rows)) for t in range(n) for j in range(n)}

def blockmat(S):return s.BlockMatrix([[Rb[t,j] for j in S] for t in S]).as_explicit()
count=far=0; max_delta=Q(0)
for k in range(1,n+1):
 for S in combinations(range(n),k):
    R=blockmat(S); dims=[Hs[t].rows for t in S];off=[sum(dims[:i]) for i in range(k+1)]
    for L in range(n):
      A=s.eye(R.rows); Ds=[]
      for i,t in enumerate(S):
        hist=[j for j in range(i) if S[j]>=t-L]
        idx=[u for j in hist for u in range(off[j],off[j+1])]
        tar=list(range(off[i],off[i+1])); D=R.extract(tar,tar)
        if idx:
          b=R.extract(tar,idx)*R.extract(idx,idx).inv();D-=b*R.extract(idx,tar)
          for a,u in enumerate(tar):
            for bidx,v in enumerate(idx):A[u,v]=-b[a,bidx]
        Ds.append(D)
      E=A*R*A.T;D=s.diag(*Ds);delta=0 if L==n-1 else 2*Q(1,2)*(T(L)+Q(71,100)*near(L))
      assert psd((1+delta)*D-E) and psd(E-(1-delta)*D),(S,L)
      count+=1
      for i,t in enumerate(S):
       for j,u in enumerate(S[:i]):
        if t-u>L:
          C=E[off[i]:off[i+1],off[j]:off[j+1]]; c=Q(1,2)*rho**(t-u)
          M=s.BlockMatrix([[c*Ds[i],C],[C.T,c*Ds[j]]]).as_explicit()
          assert psd(M),(S,L,t,u)
          far+=1
out={'model':'singular rank-two latent state, changing nonorthogonal coordinates, varying 1/2-dimensional complete packets','exact_sandwich_checks':count,'exact_far_endpoint_checks':far,'status':'PASS'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
