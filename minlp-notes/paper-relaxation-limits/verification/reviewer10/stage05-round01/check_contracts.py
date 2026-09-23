from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from pathlib import Path
import json
out=Path(__file__).parent
# Real-polynomial pullback of every degree <=2 monomial for one clause.
supports=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,1,1)]
monomials=[()]+[(i,) for i in range(5)]+list(combinations_with_replacement(range(5),2))
buckets={}
for mon in monomials:
 exp=tuple(sum(supports[i][j] for i in mon) for j in range(3))
 buckets.setdefault(exp,[]).append(mon)
# Nongraph law: x1=x2=0, x3=+-1/2, u=sign(x3), v independent with E[v]=1/2.
atoms=[((Q(0),Q(0),Q(s,2),Q(s),Q(v)),Q(1,2)*Q(3 if v==1 else 1,4)) for s,v in product((-1,1),repeat=2)]
def moment(mon):
 return sum(weight*prod([z[i] for i in mon]) for z,weight in atoms)
def prod(vals):
 r=Q(1)
 for v in vals:r*=v
 return r
for group in buckets.values():
 assert len(set(moment(mon) for mon in group))==1
assert len(monomials)-len(buckets)==2
assert all(z[3]!=z[0]*z[1] for z,_ in atoms)
assert (1-moment((4,)))/2==Q(1,4)
# True graph cost on the entire chosen original box is identically 1/2.
# Exact valid-cut identity and positivity at all full-box vertices on unequal/singleton boxes.
intervals=[(Q(-1),Q(-1)),(Q(-1),Q(-1,2)),(Q(-1,2),Q(1,2)),(Q(0),Q(0)),(Q(0),Q(1)),(Q(1),Q(1))]
cases=0
for box in product(intervals,repeat=3):
 a=[x[0] for x in box]; h=max(hi-lo for lo,hi in box)
 for x in product(*[sorted(set(i)) for i in box]):
  for u,v,b in product((-1,1),repeat=3):
   q=3*h/2-Q(b,2)*(u*(x[2]-a[2])+a[2]*(x[0]*x[1]-a[0]*a[1]))
   lhs=(1-b*v)/Q(2)-(1-b*prod(a))/Q(2)+3*h/2
   rhs=q-Q(b,2)*((v-u*x[2])+a[2]*(u-x[0]*x[1]))
   assert lhs==rhs and q>=0
   cases+=1
assert 384*3**24 < 2**64
assert Q(7,16*64)==Q(7,1024)
assert Q(7,16*64*3)==Q(7,3072)
assert Q(7,3072*17)==Q(7,52224)
record={'arithmetic':'exact rational/integer','nongraph_law_atoms':len(atoms),'all_degree_two_graph_identity_dimension':2,'relaxation_objective':'1/4','true_graph_objective':'1/2','quadratic_vertex_cases':cases,'limits':'Finite tests supplement the universal proofs. Vertex positivity extends for the tested multiaffine quadratic cuts only; this is not asymptotic XOR verification.'}
(out/'check_contracts.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
