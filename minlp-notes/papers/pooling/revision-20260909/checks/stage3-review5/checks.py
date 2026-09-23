"""Independent exact checks for frozen Sections 4--5 (not a proof)."""
from itertools import product
from random import Random
from fractions import Fraction as F
import json
import sympy as s
rng=Random(500909)
# Exhaustively compare binary dynamic programming and clamp value for small paths.
path_count=0
for n in range(1,9):
 for trial in range(100):
  U=[(rng.randrange(-4,5),rng.randrange(-4,5)) for _ in range(n)]
  a=[rng.randrange(5) for _ in range(n-1)]
  b=[rng.randrange(5) for _ in range(n-1)]
  actual=min(sum(U[i][x[i]] for i in range(n))+sum(a[i] if (x[i],x[i+1])==(0,1) else b[i] if (x[i],x[i+1])==(1,0) else 0 for i in range(n-1)) for x in product(range(2),repeat=n))
  E0=U[0][0]; D=U[0][1]-U[0][0]; P=D; Z=0
  for i in range(1,n):
   ui=U[i][1]-U[i][0]
   E0+=U[i][0]+min(0,D+b[i-1])
   Z=max(-b[i-1]-P,min(Z,a[i-1]-P))
   P+=ui; D=P+Z
  assert actual==E0+min(0,D)
  path_count+=1
# Exact signed-box rank / connected-cut / greedy support comparisons.
# Integral circulation polyhedra permit complete enumeration of integer flows here.
box_count=0; infeasible_count=0
for n in range(1,7):
 for trial in range(40):
  edges=[(i,i+1) for i in range(n-1)]
  if n>=3 and trial%2: edges.append((n-1,0))
  edges=[(v,u) if rng.randrange(2) else (u,v) for u,v in edges]
  lo=[rng.randrange(-2,1) for _ in edges]
  hi=[x+rng.randrange(3) for x in lo]
  al=[rng.randrange(-3,1) for _ in range(n)]
  be=[x+rng.randrange(6) for x in al]
  masks=list(range(1<<n)); full=(1<<n)-1
  def sm(vals,S):return sum(vals[i] for i in range(n) if S>>i&1)
  def rank(S):
   return sum(hi[e] if S>>u&1 and not S>>v&1 else -lo[e] if S>>v&1 and not S>>u&1 else 0 for e,(u,v) in enumerate(edges))
  divs=[]
  for w in product(*(range(l,h+1) for l,h in zip(lo,hi))):
   d=[0]*n
   for x,(u,v) in zip(w,edges):d[u]+=x;d[v]-=x
   if all(l<=x<=h for l,x,h in zip(al,d,be)):divs.append(d)
  cuts=all(sm(al,S)<=rank(S) and sm(be,S)>=-rank(full^S) for S in masks)
  assert cuts==bool(divs)
  if not divs:infeasible_count+=1;continue
  g={S:min(rank(T)+sm(be,S&~T)-sm(al,T&~S) for T in masks) for S in masks}
  assert g[0]==g[full]==0
  for S in masks:assert g[S]==max(sm(d,S) for d in divs)
  c=[rng.randrange(-5,6) for _ in range(n)]
  order=sorted(range(n),key=lambda i:-c[i]);S=0;dstar=[0]*n
  for i in order:
   old=S; S|=1<<i; dstar[i]=g[S]-g[old]
  assert dstar in divs
  assert sum(c[i]*dstar[i] for i in range(n))==max(sum(c[i]*d[i] for i in range(n)) for d in divs)
  box_count+=1
# Symbolic physical outlet identity, vector residual, and QP midpoint identity.
q,C1,C2,z1,z2,b,B,v=s.symbols('q C1 C2 z1 z2 b B v')
g1=C1-q;g2=C2-q;R=b*(B-q)
w1=g1*(R-g2*(z1+z2))/(C1-C2)
assert s.simplify(w1-g1*z1-g1*(R-g1*z1-g2*z2)/(C1-C2))==0
W0=-q*z1;W1=(1-q)*z2
# impose v=b-z1-z2 and quality equality z2+q*v=b*B via substitution B.
assert s.simplify((W0-q*b*(B-1)-q*(1-q)*v).subs(B,(z2+q*v)/b).subs(v,b-z1-z2))==0
x,y,rx,ry=s.symbols('x y rx ry')
assert s.expand(((x+y)/2)**2-(rx+ry)/2-(x*x-rx+y*y-ry)/2+(x-y)**2/4)==0
# Exact numerical boundary residual equation with arbitrary vector qualities.
residual_count=0
for _ in range(100):
 K=5; beta=[1,2,4,8,16]
 c1=[F(rng.randrange(-4,5)) for _ in range(K)]
 c2=[F(rng.randrange(-4,5)) for _ in range(K)]
 qq=[F(rng.randrange(-4,5),3) for _ in range(K)]
 z1=F(rng.randrange(5),3);z2=F(rng.randrange(5),3);v=F(rng.randrange(1,5),3);b=z1+z2+v
 BB=[(c1[h]*z1+c2[h]*z2+qq[h]*v)/b for h in range(K)]
 ga1=sum(beta[h]*(c1[h]-qq[h]) for h in range(K));ga2=sum(beta[h]*(c2[h]-qq[h]) for h in range(K))
 RR=b*sum(beta[h]*(BB[h]-qq[h]) for h in range(K))
 for h in range(K):
  aa=(c1[h]-qq[h])*ga2-(c2[h]-qq[h])*ga1
  ff=ga1*(b*(BB[h]-qq[h])*ga2-(c2[h]-qq[h])*RR)
  assert aa*ga1*z1==ff
 residual_count+=1
print(json.dumps({'seed':500909,'clamp_paths_passed':path_count,'box_rank_greedy_feasible_cases_passed':box_count,'cut_infeasible_cases_passed':infeasible_count,'full_vector_residual_cases_passed':residual_count,'symbolic_identities_passed':3},indent=2))
