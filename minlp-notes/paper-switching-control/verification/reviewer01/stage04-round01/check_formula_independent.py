from fractions import Fraction as Q
from itertools import product
from random import Random
from scipy.optimize import linprog

def formula(n,g):
 T=g[-1];c=next(j for j in range(1,len(g)) if g[j]>=T/3)
 H=min((T+g[c])/4,(T-g[c-1])/2)
 C=g[c];xx=max(Q(0),(C-T+2*H)/2)
 winner=(H,[(Q(0),[Q(0)]*n),(C,[xx,xx]+[min(C,T-2*H)/(n-2)]*(n-2)),(T,[H,H]+[(T-2*H)/(n-2)]*(n-2))])
 for a in range(1,len(g)):
  for b in range(a,len(g)):
   A,B,P,R=g[a],g[b],g[a-1],g[b-1]
   lo=max(T/3,Q(n-1,n)*T-B,((n-1)*T-A-(n-1)*B)/n)
   hi=min(A,((n-2)*A+B)/n,Q(n-1,n)*T-P,((n-1)*T-P-(n-1)*R)/n,(T-P+(n-2)*A)/n)
   if (n-2)*(T-A)>(n-1)*B or lo>hi:continue
   E=hi
   M=max(T/n,T-A-E,(n-1)*(E+R)-(n-2)*T,(n-1)*E-(n-2)*A)
   assert M<=min(T-P-E,(n-1)*(E+B)-(n-2)*T)
   x=max(Q(0),(n-1)*E-(n-2)*A,A-T+M);y=max(x,B-T+M)
   points=[(Q(0),[Q(0)]*n),(A,[x]+[(A-x)/(n-1)]*(n-1)),(B,[y]+[(B-y)/(n-1)]*(n-1)),(T,[M]+[(T-M)/(n-1)]*(n-1))]
   if E>winner[0]:winner=(E,points)
 return winner

def direct(g,points):
 unique=[]
 for t,z in points:
  if unique and unique[-1][0]==t:assert unique[-1][1]==z
  else:unique.append((t,z))
 n=len(points[0][1]);A=[]
 for t in g:
  left,right=next((l,r) for l,r in zip(unique,unique[1:]) if l[0]<=t<=r[0])
  A.append([a+(t-left[0])*(b-a)/(right[0]-left[0]) for a,b in zip(left[1],right[1])])
 for j,z in enumerate(A):
  assert sum(z)==g[j]
  if j:assert all(a>=b for a,b in zip(z,A[j-1]))
 best=g[-1]
 for p,q,s in product(range(n),range(n),range(len(g))):
  value=max(abs(z[i]-(min(t,g[s]) if i==p else 0)-(max(Q(0),t-g[s]) if i==q else 0)) for t,z in zip(g,A) for i in range(n))
  best=min(best,value)
 return best

def full_LP(n,g):
 # All n modes and N cell allocations retained, without component averaging.
 N=len(g)-1;num=n*N+1;eid=num-1
 def cumulative(i,j):return {i*N+h:Q(1) for h in range(j)}
 def addrow(*terms):
  r=[Q(0)]*num
  for dic,factor in terms:
   for j,c in dic.items():r[j]+=factor*c
  return r
 er={eid:Q(1)};eq=[];erhs=[]
 for j in range(N):
  eq.append(addrow(({i*N+j:1 for i in range(n)},1)));erhs.append(g[j+1]-g[j])
 optimum=0;cases=0
 for a in range(1,N+1):
  for b in range(a,N+1):
   for family in ('all','two'):
    rows=[];rhs=[]
    def row(r,bound):rows.append(r);rhs.append(bound)
    for i in range(n-1):row(addrow((cumulative(i+1,N),1),(cumulative(i,N),-1)),0)
    row(addrow((er,-1)),-g[-1]/3)
    for mode,j in ((0,a),(1,b)):
     row(addrow((er,1),(cumulative(mode,N),1)),g[-1]-g[j-1])
     row(addrow((er,-1),(cumulative(mode,N),-1)),-g[-1]+g[j])
    row(addrow((er,1),(cumulative(1,a),1)),g[a])
    row(addrow((er,1),(cumulative(0,b),1)),g[b])
    if family=='all':
     for i in range(2,n):row(addrow((er,1),(cumulative(i,a),1)),g[a])
    else:row(addrow((er,1),(cumulative(1,N),-1)),0)
    obj=[0]*num;obj[eid]=-1
    r=linprog(obj,A_ub=rows,b_ub=rhs,A_eq=eq,b_eq=erhs,bounds=[(0,None)]*num,method='highs')
    assert r.status in (0,2)
    if r.success:optimum=max(optimum,-r.fun)
    cases+=1
 return optimum,cases

rng=Random(4441);count=programs=0
grids=[(n,[Q(j) for j in range(N+1)]) for n in (3,4,5,8) for N in range(1,7)]
grids += [(5,list(map(Q,range(10)))),(9,list(map(Q,['0','19/2','61/6','265/24','481/24','2669/120'])))]
for _ in range(45):
 n=rng.randrange(3,8);N=rng.randrange(1,7);g=[Q(0)]
 for j in range(N):g.append(g[-1]+Q(rng.randrange(1,19),rng.randrange(1,15)))
 grids.append((n,g))
for n,g in grids:
 E,points=formula(n,g)
 assert direct(g,points)==E
 numerical,cases=full_LP(n,g)
 assert abs(numerical-float(E))<1e-8*max(1,float(E)),(n,g,E,numerical)
 count+=1;programs+=cases
print('PASS independently implemented rational formula/witness and full-cell LP families:',count,'grids,',programs,'LPs')
