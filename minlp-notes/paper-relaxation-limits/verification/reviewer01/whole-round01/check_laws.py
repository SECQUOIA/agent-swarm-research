from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import json

def orient(p, patterns):
 n=len(p); law={}
 for bits,weight in patterns:
  ends=sorted({Q(0),Q(1),*(p[i] if bits[i] else 1-p[i] for i in range(n))})
  for a,b in zip(ends,ends[1:]):
   u=(a+b)/2
   x=tuple(int(u<p[i]) if bits[i] else int(u>1-p[i]) for i in range(n))
   law[x]=law.get(x,Q(0))+weight*(b-a)
 assert sum(law.values())==1
 assert [sum(w*x[i] for x,w in law.items()) for i in range(n)]==list(p)
 return law

def independent(p):
 return {x:prod(p[i] if x[i] else 1-p[i] for i in range(len(p))) for x in product((0,1),repeat=len(p))}
def prod(v):
 z=Q(1)
 for x in v:z*=x
 return z

def blaw(p):
 n=len(p); law={}; ends=sorted({Q(0),Q(1),*(p[i] if p[i]<=Q(1,2) else 2*(1-p[i]) for i in range(n))})
 for a,b in zip(ends,ends[1:]):
  u=(a+b)/2
  probs=[Q(u<v) if v<=Q(1,2) else (Q(1,2) if u<2*(1-v) else Q(1)) for v in p]
  for x,w in independent(probs).items():law[x]=law.get(x,Q(0))+w*(b-a)
 assert sum(law.values())==1
 assert [sum(w*x[i] for x,w in law.items()) for i in range(n)]==list(p)
 return law

def deficiency(law,S,anchor):return sum(w*(x[anchor]-prod(x[i] for i in S)) for x,w in law.items())
grid=tuple(Q(i,4) for i in range(5)); cubic_count=0; coef_count=0
for n in (2,3):
 points=list(product(grid,repeat=n))
 if n==3:points +=[(Q(1,100),Q(9999,10000),Q(9999,10000)),(Q(51,100),Q(149,200),Q(149,200))]
 for p in points:
  laws=[orient(p,[(bits,Q(1,2**n)) for bits in product((0,1),repeat=n)]),independent(p),blaw(p)]
  anchor=min(range(n),key=lambda i:p[i]); gap=min(p[anchor],sum(1-p[i] for i in range(n) if i!=anchor))
  ds=[deficiency(law,range(n),anchor) for law in laws]
  assert 18*ds[0]+6*ds[1]+7*ds[2]>=12*gap,(p,ds,gap)
  cubic_count+=1
for n in range(2,6):
 patterns=[]
 for J in combinations(range(n),n//2):patterns.append((tuple(int(i in J) for i in range(n)),Q(1,comb(n,n//2))))
 beta=Q(n*(n-1),2*(n//2)*(n-n//2))
 for p in combinations_with_replacement(grid,n):
  laws=[orient(p,[(tuple([1]*n),Q(1))]),independent(p),orient(p,patterns)]
  for k in range(1,n+1):
   for S in combinations(range(n),k):
    s=sum(p[i] for i in S); floor=s.numerator//s.denominator; theta=s-floor
    def choose(k,j):return Q(comb(k,j)) if 0<=j<=k else Q(0)
    vals=[[sum(w*choose(sum(x[i] for i in S),j) for x,w in law.items()) for j in range(k+2)] for law in laws]
    C,P,O=vals; V=[(1-theta)*choose(floor,j)+theta*choose(floor+1,j) for j in range(k+2)]
    for j in range(k+2):
     prior=C[j-1]-P[j-1] if j else Q(0)
     assert P[j]-V[j]<=beta*(C[j]-O[j])+prior,(n,p,S,j)
     coef_count+=1
feedback_count=0
for p in product(grid,repeat=3):
 patterns=[((a,b,1),Q(1,4)) for a,b in product((0,1),repeat=2)]
 law=orient(p,patterns)
 for x in product((0,1),repeat=3):
  bound=min(p[i] if x[i] else 1-p[i] for i in range(3))
  assert law.get(x,Q(0))>=bound/4
  feedback_count+=1
res={'exact':True,'cubic_and_quadratic_mixture_cases':cubic_count,'balanced_coefficient_inequalities':coef_count,'feedback_cell_domination_cases':feedback_count,'limits':'Finite rational checks; universal guarantees require the manuscript proofs.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2));print(res)
