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
n=6;d=2;rho=Q(2,5)
Ts=[s.Matrix([[1,Q(t-2,7)],[Q(1,5),1]]) for t in range(n)]
U=[s.Matrix([[0,-1],[1,0]]) if t%2 else s.diag(1,-1) for t in range(n)]
V=[T*T.T for T in Ts];A=[None]+[rho*Ts[t]*U[t]*Ts[t-1].inv() for t in range(1,n)]
assert all(psd(rho**2*V[t]-A[t]*V[t-1]*A[t].T) for t in range(1,n))
assert A[1]*A[2]!=A[2]*A[1]
K={}
for t in range(n):
 K[t,t]=V[t]
 for j in range(t):K[t,j]=A[t]*K[t-1,j];K[j,t]=K[t,j].T
R={(t,j):K[t,j]+(V[t] if t==j else s.zeros(d)) for t in range(n) for j in range(n)}
count=far=0
for k in range(1,n+1):
 for S in combinations(range(n),k):
  M=s.BlockMatrix([[R[t,j] for j in S] for t in S]).as_explicit()
  for L in range(n):
   C=s.eye(d*k);D=[]
   for i,t in enumerate(S):
    idx=[d*j+a for j,u in enumerate(S[:i]) if u>=t-L for a in range(d)];tar=list(range(d*i,d*(i+1)))
    D0=M.extract(tar,tar)
    if idx:
     b=M.extract(tar,idx)*M.extract(idx,idx).inv();D0-=b*M.extract(idx,tar)
     for a,u in enumerate(tar):
      for j,v in enumerate(idx):C[u,v]=-b[a,j]
    D.append(D0)
   E=C*M*C.T;DD=s.diag(*D)
   delta=0 if L==n-1 else 2*(rho**(L+1)/(1-rho)+Q(1,2)*sum(rho**(h+2*l) for h in range(1,L+1) for l in range(L+1-h,L+1)))
   assert psd((1+delta)*DD-E) and psd(E-(1-delta)*DD)
   count+=1
   for i,t in enumerate(S):
    for j,u in enumerate(S[:i]):
     if t-u>L:
      Cross=E[d*i:d*(i+1),d*j:d*(j+1)];b=rho**(t-u)
      assert psd(s.BlockMatrix([[b*V[t],Cross],[Cross.T,b*V[u]]]).as_explicit())
      far+=1
out={'model':'noncommuting full blocks in changing nondiagonal observation-noise metrics','exact_sandwich_checks':count,'exact_far_pair_checks':far,'status':'PASS'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
