from fractions import Fraction as Q
from itertools import product,permutations
from collections import Counter
from random import Random

# Floor histories from coordinate increment constraints; optimization uses
# actual count vectors, not the manuscript's three-node offset recursion.
def histories(N,previous=(0,0,0),history=()):
 if not history:
  yield from histories(N,(0,0,0),((0,0,0),));return
 if len(history)==N:yield history;return
 j=len(history)+1
 for inc in product((0,1),repeat=3):
  f=tuple(a+b for a,b in zip(previous,inc))
  if j-sum(f) in (1,2):yield from histories(N,f,history+(f,))

def optimize_floor(history):
 states={((0,0,0),-1):0}
 for f in history:
  nxt={}
  for (c,last),cost in states.items():
   for active in range(3):
    cc=tuple(c[i]+(i==active) for i in range(3))
    if all(f[i]<=cc[i]<=f[i]+1 for i in range(3)):
     key=(cc,active);value=cost+(last>=0 and last!=active)
     nxt[key]=min(nxt.get(key,100),value)
  assert nxt
  states=nxt
 return min(states.values())
canonical=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
expected={5:{0:3,1:138,2:255},6:{0:3,1:255,2:1377,3:237},7:{0:3,1:414,2:4542,3:3891,4:6}}
for N in (5,6,7):
 dist=Counter();bad=set()
 for h in histories(N):
  opt=optimize_floor(h);dist[opt]+=1
  if opt==4:bad.add(h)
 assert dist==expected[N]
 if N==7:
  orbit={tuple(tuple(f[p[i]] for i in range(3)) for f in canonical) for p in permutations(range(3))}
  assert bad==orbit
 print('PASS independent count-vector DP:',N,dict(dist))

# Check the repair property directly from integer prefix occupations.
for i,word in enumerate(('1200022','0021122','0011220')):
 c=[0,0,0];fail=[]
 for j,p in enumerate(word,1):
  c[int(p)]+=1
  fail.extend((j,h,c[h]) for h in range(3) if not canonical[j-1][h]<=c[h]<=canonical[j-1][h]+1)
 assert fail==[(i+2,i,0)]
 assert sum(p!=q for p,q in zip(word,word[1:]))==3
print('PASS all three repair properties')

# Independently assembled full-control LPs retain all mode coordinates.
# Every feasible optimum is accepted only after exact rational primal/dual
# verification; infeasibility statuses remain numerical corroboration.
import numpy as np
from scipy.optimize import linprog

def formula(n,t):
 T=t[-1];N=len(t)-1;c=next(j for j in range(1,N+1) if t[j]>=T/3)
 best=min((T+t[c])/4,(T-t[c-1])/2)
 for a in range(1,N+1):
  for b in range(a,N+1):
   A,B,P,R=t[a],t[b],t[a-1],t[b-1]
   low=max(T/3,Q(n-1,n)*T-B,((n-1)*T-A-(n-1)*B)/n)
   high=min(A,((n-2)*A+B)/n,Q(n-1,n)*T-P,((n-1)*T-P-(n-1)*R)/n,(T-P+(n-2)*A)/n)
   if (n-2)*(T-A)<=(n-1)*B and low<=high:best=max(best,high)
 return best

certified=infeasible=0
rng=Random(49277)
for n,N in ((3,1),(3,3),(3,6),(4,5),(6,4),(9,4)):
 for trial in range(2):
  t=[Q(0)]
  for j in range(N):t.append(t[-1]+(Q(1) if trial==0 else Q(rng.randrange(1,12),rng.randrange(1,8))))
  T=t[-1];dim=3*n+1;E=3*n
  candidates=[]
  for a in range(1,N+1):
   for b in range(a,N+1):
    for family in (0,1):
     ub=[];rhs=[];eq=[];erhs=[]
     def row(terms,target):
      r=[Q(0)]*dim
      for i,v in terms:r[i]+=v
      ub.append(r);rhs.append(Q(target))
     for i in range(n):
      row(((i,1),(n+i,-1)),0);row(((n+i,1),(2*n+i,-1)),0)
     for i in range(n-1):row(((2*n+i+1,1),(2*n+i,-1)),0)
     row(((E,-1),),-T/3)
     for mode,cut in ((0,a),(1,b)):
      row(((E,1),(2*n+mode,1)),T-t[cut-1])
      row(((E,-1),(2*n+mode,-1)),-T+t[cut])
     row(((1,1),(E,1)),t[a]);row(((n,1),(E,1)),t[b])
     if family==0:
      for i in range(2,n):row(((i,1),(E,1)),t[a])
     else:row(((E,1),(2*n+1,-1)),0)
     for block,target in ((0,t[a]),(1,t[b]),(2,T)):
      r=[Q(0)]*dim
      for i in range(n):r[block*n+i]=Q(1)
      eq.append(r);erhs.append(target)
     c=[Q(0)]*dim;c[E]=-1
     result=linprog(list(map(float,c)),A_ub=np.array(ub,dtype=float),b_ub=np.array(rhs,dtype=float),A_eq=np.array(eq,dtype=float),b_eq=np.array(erhs,dtype=float),bounds=(0,None),method='highs')
     if result.status==2:infeasible+=1;continue
     assert result.success,result.message
     rat=lambda z:Q(float(z)).limit_denominator(10**8)
     x=list(map(rat,result.x));y=list(map(rat,result.ineqlin.marginals));z=list(map(rat,result.eqlin.marginals))
     dot=lambda a,b:sum(v*w for v,w in zip(a,b))
     assert min(x)>=0 and max(y)<=0
     assert all(dot(r,x)<=v for r,v in zip(ub,rhs))
     assert all(dot(r,x)==v for r,v in zip(eq,erhs))
     residual=[c[j]-sum(y[i]*ub[i][j] for i in range(len(ub)))-sum(z[i]*eq[i][j] for i in range(len(eq))) for j in range(dim)]
     assert min(residual)>=0
     assert dot(c,x)==dot(y,rhs)+dot(z,erhs)
     certified+=1;candidates.append(x[E])
  assert max(candidates)==formula(n,t),(n,t,max(candidates),formula(n,t))
print('PASS 12 independent full-control LP-family versus formula comparisons')
print('Exact rational optimality certificates:',certified,'; numerical infeasibility cases:',infeasible)
