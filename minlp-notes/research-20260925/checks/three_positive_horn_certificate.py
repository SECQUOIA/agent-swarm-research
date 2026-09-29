from fractions import Fraction as F
from itertools import product
import sympy as s
N=5
EPS=F(1,1000000)
def mom(p):
 deg=sum(p);twos=[i for i,a in enumerate(p) if a==2]
 if twos:
  assert len(twos)==1 and max(p)<=2
  return EPS**deg*(40 if deg>2 else 1)
 support=[i for i,a in enumerate(p) if a]
 if deg==0:return F(1)
 if deg==1:return EPS/10
 if deg==2:
  i,j=support
  return EPS**2*(F(13,20) if (i-j)%5 in [1,4] else F(1,10))
 return EPS**deg

def entry(a,b,fixed):
 p=tuple(x+y for x,y in zip(a,b));terms={p:1}
 for k,v in fixed.items():
  new={}
  for p,coeff in terms.items():
   r=list(p);r[k]+=1;r=tuple(r)
   new[r]=new.get(r,0)+(coeff if v else -coeff)
   if not v:new[p]=new.get(p,0)+coeff
  terms=new
 return sum(coeff*mom(p) for p,coeff in terms.items())
mins={};count=0
for status in product((-1,0,1),repeat=N):
 free=[i for i,z in enumerate(status) if z==-1];fixed={i:z for i,z in enumerate(status) if z!=-1}
 powers=[(0,)*N]+[tuple(int(j==i) for j in range(N)) for i in free]
 # congruence scaling diag(1,eps^-1,...) and divide by eps^number_of_fixed_ones
 scale=[F(1)]+[1/EPS]*len(free); k=list(fixed.values()).count(1)
 M=s.Matrix([[entry(a,b,fixed)*scale[i]*scale[j]/EPS**k for j,b in enumerate(powers)] for i,a in enumerate(powers)])
 for j in range(1,len(powers)+1):
  d=M[:j,:j].det()
  if d<=0:raise AssertionError((status,j,d))
  if j not in mins or d<mins[j]:mins[j]=d
 count+=1
print('Exact Sylvester checks passed:',count,'localizing matrices, epsilon=',EPS)
print('Minimum leading principal minor by order:',{k:str(v) for k,v in mins.items()})
print('Horn objective:',-EPS**2/F(2))
