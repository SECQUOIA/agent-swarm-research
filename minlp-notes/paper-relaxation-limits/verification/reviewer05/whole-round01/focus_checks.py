from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
import json,random
out={}
def rank(rows):
 basis={}
 for a in rows:
  while a:
   j=a.bit_length()-1
   if j in basis:a^=basis[j]
   else:basis[j]=a;break
 return len(basis)
# All subsets of nonzero rows in F_2^4, checking support/rank and all attainable RHS fibre sizes.
rows=list(range(1,16)); tests=0
for mask in range(1<<15):
 rr=[a for j,a in enumerate(rows) if mask>>j&1]
 q=rank(rr); union=0
 for a in rr:union|=a
 D=max([a.bit_count() for a in rr],default=0)
 assert union.bit_count()<=D*q
 buckets={}
 for w in range(16):
  rhs=tuple((a&w).bit_count()%2 for a in rr)
  buckets[rhs]=buckets.get(rhs,0)+1
 assert len(buckets)==2**q and set(buckets.values())=={2**(4-q)}
 tests+=1
out['binary_rank_exact']={'families':tests,'dimension':4,'all_consistent_rhs':True}
# The full-box quadratic certificate is multiaffine; enumerate its corners at rational grids.
checks=0
for M in [1,2,3,7]:
 h=Q(2,M)
 for cell in product(range(M),repeat=3):
  a=[-1+j*h for j in cell]
  for endpoints in product([0,1],repeat=3):
   x=[a[j]+h*endpoints[j] for j in range(3)]
   for u,v,b in product([-1,1],repeat=3):
    q=3*h/2-Q(b,2)*(u*(x[2]-a[2])+a[2]*(x[0]*x[1]-a[0]*a[1]))
    assert q>=0
    lhs=Q(1-b*v,2)-Q(1,2)*(1-b*a[0]*a[1]*a[2])+3*h/2
    rhs=q-Q(b,2)*((v-u*x[2])+a[2]*(u-x[0]*x[1]))
    assert lhs==rhs
    checks+=1
out['order_one_quadratic_exact']={'corners_with_signs':checks,'grid_counts':[1,2,3,7]}
# Signed Gram law: construct signed orthogonal classes, enumerate independent class signs,
# and compare every prescribed first and second moment in rational arithmetic.
rng=random.Random(5); cases=0
for N in range(1,15):
 for trial in range(30):
  classes=[0]+[rng.randrange(5) for _ in range(N)]
  signs=[1]+[rng.choice([-1,1]) for _ in range(N)]
  used=sorted(set(classes)-{0}); denom=2**len(used)
  sums=[[0]*(N+1) for _ in range(N+1)]
  for bits in product([-1,1],repeat=len(used)):
   vals={0:1,**dict(zip(used,bits))}; z=[signs[j]*vals[classes[j]] for j in range(N+1)]
   for i,j in product(range(N+1),repeat=2):sums[i][j]+=z[i]*z[j]
  for i,j in product(range(N+1),repeat=2):
   assert Q(sums[i][j],denom)==(signs[i]*signs[j] if classes[i]==classes[j] else 0)
  cases+=1
out['signed_gram_law_exact']={'deterministic_seed':5,'class_patterns':cases,'coordinate_counts':[1,14]}
assert 384*3**24 < 2**64
out['deletion_arithmetic_exact']={'384_times_3pow24':384*3**24,'2pow64':2**64}
Path('focus-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
