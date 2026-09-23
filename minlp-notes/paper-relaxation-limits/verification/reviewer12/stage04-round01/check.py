"""Independent finite Stage 4 checks: exact identities; numerical matrix PSD."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from functools import lru_cache
from math import prod, comb
import json
import numpy as np
from pathlib import Path

def fall(x,a): return prod((x-j for j in range(a)),start=Q(1))
N=27; ell=9; K=Q(7,2); r=2
w=tuple([Q(1)]*3+[Q(1,6)]*3+[Q(0)]*3)*3
eta=Q(1,32)
d=tuple(eta*Q((i+1)**2,ell*N*N) for i in range(N))
records=[]
for heavy in [False,True]:
 fixed={3:w[3],21:w[21]}
 if heavy: fixed.update({i:w[i] for i in range(9,18)})
 blocks=[]
 for b in range(3):
  U=set(range(b*ell,(b+1)*ell))-fixed.keys()
  t=K-sum((fixed[i] for i in fixed if i//ell==b),Q(0))
  blocks.append((U,t))
 @lru_cache(None)
 def L(m):
  val=prod((fixed[i] for i in m if i in fixed),start=Q(1))
  if not val:return val
  support=set(m)-fixed.keys()
  for U,t in blocks:
   a=len(support & U)
   val*=fall(t,a)/fall(len(U),a)
  return val
 def term(*ms):return L(tuple(sorted(sum((tuple(m) for m in ms),()))))
 mons=[()] + [m for degree in range(1,4) for m in combinations_with_replacement(range(N),degree)]
 eq=0
 for b in range(3):
  for m in mons:
   assert sum((term(m,(i,)) for i in range(b*ell,(b+1)*ell)),Q(0))==K*L(m)
   eq+=1
 basis=[()] + [(i,) for i in range(N)] + list(combinations_with_replacement(range(N),2))
 M=np.array([[float(term(a,b)) for b in basis] for a in basis])
 eig=float(np.linalg.eigvalsh(M)[0]); assert eig>-1e-9
 # Full linear-square spaces, factors spanning distinct blocks and repeated factors.
 linear=[()]+[(i,) for i in range(N)]
 localmins=[]
 for i,j in [(0,9),(1,18),(9,18),(0,0),(3,12)]:
  for left,right in product([0,1],repeat=2):
   # 1 means lower slack, 0 means upper slack.
   def loc(a,b):
    factors=[[(Q(1),(i,))] if left else [(Q(1),()),(Q(-1),(i,))],[(Q(1),(j,))] if right else [(Q(1),()),(Q(-1),(j,))]]
    return sum((ca*cb*term(a,b,ma,mb) for ca,ma in factors[0] for cb,mb in factors[1]),Q(0))
   A=np.array([[float(loc(a,b)) for b in linear] for a in linear])
   e=float(np.linalg.eigvalsh(A)[0]);assert e>-1e-9;localmins.append(e)
 penalty=sum((term((i,))-term((i,i)) for i in range(N)),Q(0))
 assert penalty==sum((v*(1-v) for v in fixed.values()),Q(0))
 objective=3*K+penalty+sum((d[i]*term((i,)) for i in range(N)),Q(0))
 # Endpoint penalty auxiliary maps to a deterministic witness penalty, or zero.
 y={i:fixed[i]*(1-fixed[i]) if i in fixed else Q(0) for i in range(N)}
 # Full-graph identity y_i-x_i+x_i^2 multiplied by every quadratic original monomial,
 # including multipliers crossing all pairs of blocks; lifted degree at most four.
 graph=0
 for i in range(N):
  for m in basis:
   assert y[i]*term(m)-term(m,(i,))+term(m,(i,i))==0
   graph+=1
 assert objective==3*K+sum(y.values(),Q(0))+sum((d[i]*term((i,)) for i in range(N)),Q(0))
 records.append(dict(heavy_middle_block=heavy,exact_balance_products=eq,exact_graph_identity_products=graph,moment_matrix_dimension=len(basis),numerical_moment_min_eigenvalue=eig,full_crossblock_or_repeated_localizer_matrices=len(localmins),numerical_localizer_min_eigenvalue=min(localmins),penalty=str(penalty),objective=str(objective)))
# Asymmetry check independent of sorted-difference proof: enumerate all feasible permutations
# of two length-three blocks, compare objective differences modulo balances.
from itertools import permutations
sym=0
for swap in [False,True]:
 for p,q in product(permutations(range(3)),repeat=2):
  perm=tuple((3 if swap else 0)+i for i in p)+tuple((0 if swap else 3)+i for i in q)
  delta=[(perm[i]+1)**2-(i+1)**2 for i in range(6)]
  if len(set(delta[:3]))==len(set(delta[3:]))==1 and delta[0]+delta[3]==0:
   sym+=1;assert perm==tuple(range(6))
assert sym==1
assert Q(1,4)-Q(1,32)*(Q(5,2)+Q(1,4))-eta==Q(17,128)
output=dict(status='PASS',cases=records,exact_feasible_permutations_checked=72,symmetries=sym,scope='Finite exact identities and floating-point full-matrix eigenvalues; not a proof for arbitrary dimensions, degrees, functions or localizers.')
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
