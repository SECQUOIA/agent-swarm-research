"""Independent finite enumeration check of signed incidence, box-base support, and path/cycle minimization.
Integral incidence systems make enumeration of integer flows sufficient for
linear extrema with these integral arc/node bounds. No manuscript code used.
"""
from itertools import product
from fractions import Fraction
from random import Random
import json
from pathlib import Path
rng=Random(902605)

def div(n,edges,w):
 d=[0]*n
 for (v,u),x in zip(edges,w): d[v]+=x; d[u]-=x
 return tuple(d)

def solve_case(n,edges):
 lower=[rng.randint(-2,0) for _ in edges]
 upper=[l+rng.randint(0,2) for l in lower]
 seed=[rng.randint(l,u) for l,u in zip(lower,upper)]
 d0=div(n,edges,seed)
 alpha=[x-rng.randint(0,2) for x in d0]
 beta=[x+rng.randint(0,2) for x in d0]
 flows=[(w,div(n,edges,w)) for w in product(*(range(l,u+1) for l,u in zip(lower,upper)))]
 feasible=[(w,d) for w,d in flows if all(a<=x<=b for a,x,b in zip(alpha,d,beta))]
 assert feasible
 sets=[set(i for i in range(n) if mask>>i&1) for mask in range(1<<n)]
 def f(T):
  return sum(u for (v,w),u in zip(edges,upper) if v in T and w not in T)-sum(l for (v,w),l in zip(edges,lower) if v not in T and w in T)
 def rank(S):
  return min(f(T)+sum(beta[i] for i in S-T)-sum(alpha[i] for i in T-S) for T in sets)
 ranks=[rank(S) for S in sets]
 for S,g in zip(sets,ranks): assert g==max(sum(d[i] for i in S) for _,d in feasible)
 costs=[Fraction(rng.randint(-4,4),rng.randint(1,3)) for _ in range(n)]
 order=sorted(range(n),key=lambda i:-costs[i]); pref=set(); prev=0; greedy=[0]*n
 for i in order:
  pref.add(i); new=rank(pref); greedy[i]=new-prev; prev=new
 assert tuple(greedy) in {d for _,d in feasible}
 greedy_obj=sum(c*d for c,d in zip(costs,greedy))
 assert greedy_obj==max(sum(c*x for c,x in zip(costs,d)) for _,d in feasible)
 # Independent binary DP for each rank: permits signed unary costs,
 # directed edges in either orientation, and closure edge on cycles.
 for S,g in zip(sets,ranks):
  shift=div(n,edges,lower)
  unary=[[(beta[v] if v in S else 0), shift[v]-(alpha[v] if v not in S else 0)] for v in range(n)]
  def pair(e,x,y):
   v,w=edges[e]; return (upper[e]-lower[e])*(x*(1-y) if (v,w)==(e,e+1) else y*(1-x))
  opts=[]
  for first in [0,1]:
   dp={first:unary[0][first]}
   for v in range(1,n):
    dp={y:unary[v][y]+min(val+pair(v-1,x,y) for x,val in dp.items()) for y in [0,1]}
   if len(edges)==n:
    tail,head=edges[-1]
    vals=[val+(upper[-1]-lower[-1])*(x*(1-first) if (tail,head)==(n-1,0) else first*(1-x)) for x,val in dp.items()]
   else: vals=list(dp.values())
   opts.append(min(vals))
  assert min(opts)==g
 return len(feasible)
results=[]
for n,cyclic in [(2,False),(4,False),(5,False),(4,True),(5,True)]:
 for trial in range(12):
  edges=[(i,i+1) for i in range(n-1)]+([(n-1,0)] if cyclic else [])
  edges=[e if rng.randrange(2) else e[::-1] for e in edges]
  results.append({'n':n,'cycle':cyclic,'feasible_integer_flows':solve_case(n,edges)})
result={'status':'pass','cases':len(results),'scope':'Exact signed incidence support, full subset box ranks, greedy attainment, independent binary path/cycle DP','detail':results}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='detail'}))
