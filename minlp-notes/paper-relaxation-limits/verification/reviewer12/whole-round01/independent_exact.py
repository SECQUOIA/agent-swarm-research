from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import json
import sympy as s
out={}
# Independent exact coefficient check, integrating actual orientation outcomes.
cases=0
for n in range(2,7):
 coins=list(combinations(range(n),n//2)); beta=Q(n*(n-1),2*(n//2)*((n+1)//2))
 for p in combinations_with_replacement([Q(i,4) for i in range(5)],n):
  total=sum(p); k=total.numerator//total.denominator; theta=total-k
  V=[(1-theta)*comb(k,j)+(theta*comb(k+1,j)) for j in range(n+1)]
  C=[Q(1)]+[sum(p[i]*comb(n-i-1,j-1) for i in range(n)) for j in range(1,n+1)]
  P=[sum((__import__('functools').reduce(lambda a,b:a*b,(p[i] for i in I),Q(1)) for I in combinations(range(n),j)),Q(0)) for j in range(n+1)]
  O=[Q(0)]*(n+1)
  ends=sorted(set([Q(0),Q(1),*p,*(1-x for x in p)]))
  for J in coins:
   for a,b in zip(ends,ends[1:]):
    t=(a+b)/2; count=sum(t<p[i] if i in J else t>1-p[i] for i in range(n))
    for j in range(n+1):O[j]+=(b-a)*comb(count,j)/len(coins)
  for j in range(1,n+1):assert P[j]-V[j]<=beta*(C[j]-O[j])+C[j-1]-P[j-1],(n,p,j)
  cases+=1
out['balanced_coefficient_quarter_grid_vectors']=cases
# Fractional-cardinality Gram identity as rational polynomial identity in t.
t=s.symbols('t'); count=0
for d in range(1,6):
 for n in range(2*d,2*d+4):
  ff=lambda a,b:s.prod(a-j for j in range(b))
  for ell in range(d+1):
   lhs=sum(comb(ell,j)*ff(t,2*d-j)*ff(n-t,j) for j in range(ell+1))
   rhs=ff(t,2*d-ell)*ff(n-2*d+ell,ell)
   assert s.expand(lhs-rhs)==0;count+=1
out['symbolic_gram_entries']=count
# Full assignment-localizer matrices at the nonintegral admissible endpoint example.
n=7;t=Q(7,2);r=2
ff=lambda a,b:__import__('functools').reduce(lambda x,y:x*(a-y),range(b),Q(1))
def moment(I):return ff(t,len(I))/ff(n,len(I))
count=0
for v in range(5):
 for a in range(v+1):
  A=frozenset(range(a));B=frozenset(range(a,v));remain=range(v,n);deg=(4-v)//2
  mon=[frozenset(I) for j in range(deg+1) for I in combinations(remain,j)]
  def entry(I,J):
   return sum(((-1)**len(T)*moment(A|I|J|frozenset(T)) for z in range(len(B)+1) for T in combinations(B,z)),Q(0))
  M=s.Matrix([[entry(I,J) for J in mon] for I in mon])
  assert M.is_positive_semidefinite is True,(v,a);count+=1
out['exact_psd_localizer_representatives_s7_t3_5_r2']=count
# Exhaust every basis-row support-union case in F2 for n=4,D=2.
rows=[sum(1<<i for i in I) for d in (1,2) for I in combinations(range(4),d)]
for mask in range(1<<len(rows)):
 selected=[row for i,row in enumerate(rows) if mask>>i&1];basis={};union=0
 for row in selected:
  union|=row;x=row
  while x:
   j=x.bit_length()-1
   if j in basis:x^=basis[j]
   else:basis[j]=x;break
 assert union.bit_count()<=2*len(basis)
 for rhs in range(16):
  values=[sum((w&row).bit_count()%2 != (rhs&row).bit_count()%2 for row in selected)==0 for w in range(16)]
  assert sum(values)==2**(4-len(basis))
out['parity_systems_checked']=2**len(rows)*16
# Exact PARTITION gap check on all length <=5 lists with entries 1,2,3, after doubling.
count=0
for n in range(1,6):
 for inp in product(range(1,4),repeat=n):
  a=[2*x for x in inp];A=sum(a);eps=Q(1,16*A**3)
  b=1+eps*A/2+eps**2*(Q(A*A,8)-Q(sum(x*x for x in a),4));threshold=b+eps**2/4
  vals=[];sums=[]
  for z in product((0,1),repeat=n):
   S=sum(x*y for x,y in zip(a,z)); val=__import__('functools').reduce(lambda x,y:x*y,(1+eps*x*y for x,y in zip(a,z)),Q(1))
   R=val-1-eps*S-eps**2*(S*S-sum(x*x*y for x,y in zip(a,z)))/2
   assert 0<=R<=eps**2/8
   vals.append(val);sums.append(S)
  if A//2 in sums:
   i=sums.index(A//2);assert (vals[i]+vals[-1-i])/2<threshold
  else:
   for S in sums:assert (S-A//2)**2>=1
  count+=1
out['partition_lists']=count
# Primitive lower recurrence, exact first crossing.
res=[]
for n in range(1,4):
 b=Q(1,2**(2**n));c=1-b;l=Q(0);k=0
 while l<Q(1,2):k+=1;l=b+c*l;assert l<=k*b
 assert k>=2**(2**n-1);res.append([n,k])
out['primitive_exact_crossings']=res
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
