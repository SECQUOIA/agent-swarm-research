from itertools import combinations, product
from fractions import Fraction as F
from math import gcd,lcm
from functools import reduce
import sympy as sp
import json

def neg(a):return tuple(-x for x in a)
def universe(m,full=False):
 positive={v for v in product((0,1),repeat=m) if any(v)}
 negative={neg(v) for v in positive} if full else {tuple(-int(i==j) for i in range(m)) for j in range(m)}|{(-1,)*m}
 return sorted(positive|negative)
def circuits(rows):
 m=len(rows[0]); out=[]
 for k in range(2,m+2):
  for ids in combinations(range(len(rows)),k):
   A=sp.Matrix([rows[i] for i in ids]).T
   ns=A.nullspace()
   if len(ns)!=1:continue
   q=ns[0]
   if not (all(x>0 for x in q) or all(x<0 for x in q)):continue
   den=lcm(*[int(x.q) for x in q]); nums=[int(x*den) for x in q]
   if nums[0]<0:nums=[-x for x in nums]
   g=reduce(gcd,nums);nums=[x//g for x in nums]
   out.append([(rows[i],v) for i,v in zip(ids,nums)])
 return out
counts={}; product_checks=0
for m in (1,2,3):
 rows=universe(m);cs=circuits(rows)
 counts[str(m)]={'normals':len(rows),'circuits':len(cs),'largest_weight':max(q for c in cs for a,q in c),'unreduced_signed_circuits':len(circuits(universe(m,True)))}
 if m==1:continue
 def ei(j):return tuple(int(i==j) for i in range(m))
 for pattern in product(range(4),repeat=m): # neither, a only, b only, both
  A={j for j,s in enumerate(pattern) if s==1};B={j for j,s in enumerate(pattern) if s==2};T={j for j,s in enumerate(pattern) if s==3}
  rhs_rows=[]
  def row(n,coef):rhs_rows.append((n,coef))
  R={'xa':1}
  for j in A|T:R['a'+str(j)]=-1
  for j in B:R['b'+str(j)]=1
  row(tuple(int(j in B) for j in range(m)),R)
  upper={k:-v for k,v in R.items()};upper['xh']=-1
  row(tuple(int(j in A|T) for j in range(m)),upper)
  for j in A:row(neg(ei(j)),{'a'+str(j):-1})
  for j in B:row(neg(ei(j)),{'b'+str(j):-1})
  for j in T:
   row(ei(j),{'a'+str(j):1,'b'+str(j):1})
   row(neg(ei(j)),{'a'+str(j):-1,'b'+str(j):-1})
  symbols={v for n,c in rhs_rows for v in c if v!='xh'}
  for sym in symbols:
   # Any original row can be selected per normal; zero contributions from
   # other gadgets only enlarge this interval, so this is a safe universal bound.
   for circ in cs:
    low=high=0
    for n,weight in circ:
     choices=[0]+[c.get(sym,0) for nn,c in rhs_rows if nn==n]
     low+=weight*min(choices);high+=weight*max(choices)
    assert low>=-1 and high<=1,(m,pattern,sym,circ,low,high)
    product_checks+=1
 for j in range(m):
  for circ in cs:
   coeff=sum(weight*(-1 if n==ei(j) else 1 if n==neg(ei(j)) else 0) for n,weight in circ)
   assert abs(coeff)<=1
 # Enumerate bypass coefficients on all positive-normal row choices.
 for circ in cs:
  opts=[[-1,0] if all(x>=0 for x in n) else [1] if n==(-1,)*m else [0] for n,q in circ]
  for choice in product(*opts):
   h=sum(w*c for (n,w),c in zip(circ,choice))
   if m==2:assert abs(h)<=1
   elif abs(h)>1:
    assert h in (-2,2)
    positives=[n for (n,w),c in zip(circ,choice) if all(x>=0 for x in n)]
    if h==-2:assert len(positives)==3 and all(sum(n)==1 for n in positives)
    else:assert len(positives)==3 and all(sum(n)==2 for n in positives)
# Exact numerical values and separate McCormick checks of both repair examples.
for ya,xa,xb,z in [(F(1,3),F(2,5),F(1,10),F(0)),(F(1,4),F(1,20),F(9,20),F(1,20))]:
 flow=xa if ya==F(1,3) else xb
 assert 0<=z<=ya and z<=flow and z>=flow+ya-1
 assert xa+xb+F(1,2)==1
assert 2*F(1,2)-3*F(2,5)==-F(1,5)
assert 3*F(3,20)+2*(F(1,4)-F(1,2))==-F(1,20)
print(json.dumps({'normal_and_circuit_counts':counts,'local_coefficient_bounds_checked':product_checks,'repair_examples':'PASS','status':'PASS'},indent=2))
