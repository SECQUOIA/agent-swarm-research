import sympy as s
from itertools import product
import json
F=[0,1,1]
for i in range(3,15):F.append(F[-1]+F[-2])
witnesses=obstructions=0
for q in range(3,13):
 N=2*q-1
 cols=[{q,0},{q,1}]
 for i in range(3,q+1):cols += [{q+i-2,i-1},{q+i-2,i-2,i-3}]
 cols += [{q-1,q-2}]
 D=s.Matrix(N,N,lambda i,j:int(i in cols[j]))
 gamma=F[q+1];alpha=s.Matrix([F[i] for i in range(1,q+1)]+[gamma-1]+[gamma-F[i] for i in range(3,q+1)])
 K=s.ones(N)-D
 assert sum(D)==5*q-4 and D.det()!=0 and K.det()!=0
 assert D.T*alpha==gamma*s.ones(N,1)
 assert K.T*alpha==(sum(alpha)-gamma)*s.ones(N,1)
 assert sum(alpha)==(q-1)*gamma+1
 inv=K.inv();norm=max(sum(abs(inv[i,j]) for j in range(N)) for i in range(N))
 a=s.Rational(1,2*N);c=a/4;ratio=F[q]
 eps=a/(16*(1+ratio)*(1+norm))
 r=q-1;rr=0
 xa=[sum(K[i,j] for j in range(N))*a+sum(D[i,j] for j in range(N))*c for i in range(N)]
 for dr,ds in product([-eps/2,0,eps/2],repeat=2):
  delta=s.zeros(N,1);delta[r]=dr;delta[rr]=ds
  value=(alpha.T*delta)[0]
  if value<0:
   assert ratio*dr+ds<0
   obstructions+=1
   continue
  tau=s.zeros(N,1);tau[rr]=ratio*dr+ds
  w=a*s.ones(N,1)+inv*(-delta+tau)
  assert sum(w)==s.Rational(1,2) and all(0<z<2*a for z in w)
  fa=s.zeros(N,N)
  for i in range(N):
   for j in range(N):
    fa[i,j]=w[j] if K[i,j] else c
  fa[r,N-1]+=dr;fa[rr,0]+=ds
  reducecol=next(j for j in range(N) if K[rr,j])
  fa[rr,reducecol]-=tau[rr]
  for i in range(N):
   assert sum(fa[i,j] for j in range(N))==xa[i]
   assert all(0<=fa[i,j]<=w[j] for j in range(N))
   fb=[w[j]-fa[i,j] for j in range(N)]
   assert sum(fb)==s.Rational(1,2)-xa[i]
   for j in range(N):
    if D[i,j]:assert fa[i,j]==c+(dr if (i,j)==(r,N-1) else ds if (i,j)==(rr,0) else 0)
  fh=[2*a-z for z in w]
  assert sum(fh)==s.Rational(1,2) and all(0<=z<=2*a for z in fh)
  witnesses+=1
 # Independently count/check the split and subdivided simple graph.
 source=('s',);sink=('t',)
 def left(i):return source if i==0 else ('out',i)
 def right(i):return sink if i==N else ('in',i)
 edges=[(source,sink)]
 for i in range(1,N+1):
  edges += [(left(i-1),right(i)),(left(i-1),('mid',i)),(('mid',i),right(i))]
 for i in range(1,N):edges += [(('in',i),('out',i))]
 vertices=set(v for e in edges for v in e)
 assert len(vertices)==3*N and len(edges)==4*N and len(set(edges))==len(edges)
 assert max(sum(v in e for e in edges) for v in vertices)==3
 assert len(edges)-len(vertices)+1==2*q
print(json.dumps({'q_range':[3,12],'largest_fibonacci_ratio':F[12],'exact_feasible_witnesses':witnesses,'exact_support_obstructions':obstructions,'simple_degree3_graphs_checked':10,'status':'PASS'},indent=2))
