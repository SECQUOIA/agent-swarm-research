"""Independent whole-paper review: unreduced minimax, elimination, word chambers."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,permutations
from collections import Counter
from random import Random
import json
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
O=Path(__file__).resolve().parent
rng=Random(773102)
def closed(n,t):
 T=t[-1];N=len(t)-1;c=next(j for j in range(1,N+1) if t[j]>=T/3)
 H=min((T+t[c])/4,(T-t[c-1])/2);candidates=[(H,('H',c))]
 for a in range(1,N+1):
  for b in range(a,N+1):
   A,B,P,R=t[a],t[b],t[a-1],t[b-1]
   lo=max(T/3,Q(n-1,n)*T-B,((n-1)*T-A-(n-1)*B)/n)
   hi=min(A,((n-2)*A+B)/n,Q(n-1,n)*T-P,((n-1)*T-P-(n-1)*R)/n,(T-P+(n-2)*A)/n)
   if (n-2)*(T-A)<=(n-1)*B and lo<=hi:candidates.append((hi,('F',a,b)))
 E,which=max(candidates)
 if which[0]=='H':
  C=t[which[1]];x=max(Q(0),(C-T+2*E)/2)
  knots=[Q(0),C,T];states=[[Q(0)]*n,[x,x]+[min(C,T-2*E)/(n-2)]*(n-2),[E,E]+[(T-2*E)/(n-2)]*(n-2)]
 else:
  a,b=which[1:];A,B,P,R=t[a],t[b],t[a-1],t[b-1]
  M=max(T/n,T-A-E,(n-1)*(E+R)-(n-2)*T,(n-1)*E-(n-2)*A)
  assert M<=min(T-P-E,(n-1)*(E+B)-(n-2)*T)
  x=max(Q(0),(n-1)*E-(n-2)*A,A-T+M);y=max(x,B-T+M)
  knots=[Q(0),A,B,T];states=[[Q(0)]*n,[x]+[(A-x)/(n-1)]*(n-1),[y]+[(B-y)/(n-1)]*(n-1),[M]+[(T-M)/(n-1)]*(n-1)]
 for a,b,X,Y in zip(knots,knots[1:],states,states[1:]):assert all(y>=x for x,y in zip(X,Y)) and sum(Y)-sum(X)==b-a
 def A(tau):
  for a,b,X,Y in zip(knots,knots[1:],states,states[1:]):
   if a<=tau<=b and a<b:return [x+(tau-a)*(y-x)/(b-a) for x,y in zip(X,Y)]
  return states[-1]
 best=T
 for p,q in permutations(range(n),2):
  for tau in t:
   val=0
   for tt in t:
    W=[min(tt,tau) if i==p else max(Q(0),tt-tau) if i==q else Q(0) for i in range(n)]
    val=max(val,*[abs(x-y) for x,y in zip(A(tt),W)])
   best=min(best,val)
 assert best==E,(n,t,E,best)
 return E

def families(n,t):
 T=t[-1];N=len(t)-1;best=0;programs=0
 for a in range(1,N+1):
  for b in range(a,N+1):
   for family in range(2):
    rows=[];rhs=[]
    def le(terms,v):
     row=[0]*10
     for i,c in terms:row[i]+=float(c)
     rows.append(row);rhs.append(float(v))
    for i in range(3):le([(i,1),(i+3,-1)],0);le([(i+3,1),(i+6,-1)],0)
    le([(7,1),(6,-1)],0);le([(8,1),(7,-1)],0)
    for m,A,P in [(6,t[a],t[a-1]),(7,t[b],t[b-1])]:
     le([(9,-1),(m,-1)],A-T);le([(9,1),(m,1)],T-P)
    le([(1,1),(9,1)],t[a]);le([(3,1),(9,1)],t[b])
    le([(2,1),(9,1)],t[a]) if family==0 else le([(9,1),(7,-1)],0)
    eq=[]
    for offset in (0,3,6):
     row=[0]*10
     for i,w in enumerate((1,1,n-2)):row[offset+i]=w
     eq.append(row)
    c=[0]*9+[-1];ans=linprog(c,A_ub=rows,b_ub=rhs,A_eq=eq,b_eq=list(map(float,[t[a],t[b],T])),bounds=[(0,None)]*9+[(float(T/3),None)],method='highs');programs+=1
    assert ans.status in (0,2),ans.message
    if ans.success:best=max(best,-ans.fun)
 return best,programs

cases=[];programs=0
for trial in range(36):
 n=rng.randint(3,10);N=rng.randint(1,7);t=[Q(0)]
 for j in range(N):t.append(t[-1]+Q(rng.randint(1,8),rng.randint(1,7)))
 E=closed(n,t);value,count=families(n,t);programs+=count
 assert abs(float(E)-value)<1e-7,(n,t,E,value)
 cases.append({'n':n,'N':N,'value':str(E)})
# Important endpoints and large binary-encoded mode count reconstruction.
for n in (3,4,7,10**12):
 t=[Q(0),Q(1)]
 if n<100:assert closed(n,t)==Q(n-1,n)
# Unreduced outer max-min MILP from the actual signed prefix errors.
def direct_minimax(n,t):
 N=len(t)-1;T=float(t[-1]);words=[(p,)*N for p in range(n)]
 words +=[(p,)*a+(q,)*(N-a) for p,q in permutations(range(n),2) for a in range(1,N)]
 base=n*N+1;eidx=n*N;total=base+len(words)*2*n*N
 rowidx=[];colidx=[];values=[];lb=[];ub=[]
 def row(terms,lo,hi):
  r=len(lb)
  for c,v in terms:rowidx.append(r);colidx.append(c);values.append(float(v))
  lb.append(lo);ub.append(hi)
 for j in range(N):row([(j*n+i,1) for i in range(n)],float(t[j+1]-t[j]),float(t[j+1]-t[j]))
 z=base
 for word in words:
  zs=[];service=[0.0]*n
  for j in range(N):
   service[word[j]]+=float(t[j+1]-t[j])
   for i in range(n):
    for sign in (-1,1):
     terms=[(eidx,1),(z,-2*T)]+[(h*n+i,-sign) for h in range(j+1)]
     row(terms,-np.inf,-sign*service[i]);zs.append(z);z+=1
  row([(v,1) for v in zs],-np.inf,len(zs)-1)
 assert z==total
 c=np.zeros(total);c[eidx]=-1
 lower=np.zeros(total);upper=np.ones(total);upper[:base]=T
 matrix=coo_matrix((values,(rowidx,colidx)),shape=(len(lb),total)).tocsc()
 result=milp(c,integrality=np.r_[np.zeros(base),np.ones(total-base)],bounds=Bounds(lower,upper),constraints=LinearConstraint(matrix,lb,ub),options={'time_limit':60,'mip_rel_gap':1e-9,'mip_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 assert result.success,(n,t,result.message)
 return -result.fun,len(words)
outer=[]
for n,t in [(3,[Q(0),Q(1),Q(2)]),(3,[Q(0),Q(1,3),Q(4,3),Q(2)]),(4,[Q(0),Q(2,5),Q(1)])]:
 val,count=direct_minimax(n,t);E=closed(n,t);assert abs(val-float(E))<1e-7,(n,t,E,val);outer.append([n,len(t)-1,str(E),count])
print('Grid formulas and unreduced outer models passed',flush=True)

# Explicit-word bit masks independently recover every strict chamber.
results={};bad7=[];averages=0
for N in (5,6,7):
 words=list(product(range(3),repeat=N));bucket={};counts={}
 for widx,w in enumerate(words):
  bit=1<<widx;s=sum(a!=b for a,b in zip(w,w[1:]));bucket[s]=bucket.get(s,0)|bit;c=[0]*3
  for j,p in enumerate(w,1):
   c[p]+=1
   for i,x in enumerate(c):counts[j,i,x]=counts.get((j,i,x),0)|bit
 masks={}
 def boxmask(j,f):
  if (j,f) not in masks:
   m=(1<<len(words))-1
   for i,x in enumerate(f):m&=counts.get((j,i,x),0)|counts.get((j,i,x+1),0)
   masks[j,f]=m
  return masks[j,f]
 def extend(hist,m):
  j=len(hist)
  if j==N:yield hist,m;return
  f=hist[-1]
  for d in product((0,1),repeat=3):
   g=tuple(a+b for a,b in zip(f,d));sig=j+1-sum(g)
   if sig in (1,2):yield from extend(hist+(g,),m&boxmask(j+1,g))
 dist=Counter();bad=[]
 for hist,m in extend(((0,0,0),),boxmask(1,(0,0,0))):
  assert m
  minimum=min(s for s,b in bucket.items() if m&b);dist[minimum]+=1
  if minimum>=4:bad.append(hist)
  # Construct exact interior cumulative values by averaging ALL surviving words.
  number=m.bit_count();previous=[Q(0)]*3
  for j,f in enumerate(hist,1):
   A=[]
   for i,x in enumerate(f):
    below=(m&counts.get((j,i,x),0)).bit_count();above=(m&counts.get((j,i,x+1),0)).bit_count()
    assert below>0 and above>0 and below+above==number
    A.append(Q(x*number+above,number))
   assert sum(A)==j and all(a>=b for a,b in zip(A,previous));previous=A
  averages+=1
 results[N]=dict(sorted(dist.items()))
 if N==7:bad7=bad
expected={5:{0:3,1:138,2:255},6:{0:3,1:255,2:1377,3:237},7:{0:3,1:414,2:4542,3:3891,4:6}}
assert results==expected
canonical=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
orbit={tuple(tuple(f[i] for i in p) for f in canonical) for p in permutations(range(3))}
assert set(bad7)==orbit
repairs=[(1,2,0,0,0,2,2),(0,0,2,1,1,2,2),(0,0,1,1,2,2,0)]
for i,w in enumerate(repairs):
 c=[0]*3;defects=[]
 for j,(a,f) in enumerate(zip(w,canonical),1):
  c[a]+=1
  for k,x in enumerate(c):
   if not f[k]<=x<=f[k]+1:defects.append((j,k,x))
 assert defects==[(i+2,i,0)] and sum(a!=b for a,b in zip(w,w[1:]))==3
out={'random_grid_cases':cases,'original_LP_programs':programs,'unreduced_outer_MILPs':outer,'strict_chamber_distributions':results,'exact_interior_averages_constructed':averages,'exceptional_orbit_size':len(bad7),'repair_words':3}
(O/'grid-floor-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('All exact chamber word intersections, realizations and repairs passed',out['exact_interior_averages_constructed'],flush=True)
