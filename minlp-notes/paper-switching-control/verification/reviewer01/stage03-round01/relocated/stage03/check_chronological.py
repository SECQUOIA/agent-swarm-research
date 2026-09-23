"""Exact audit of the old witness and one strengthened chronological chamber."""
from pathlib import Path
from fractions import Fraction as Q
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'reference'))
from general_reach_research import weighted_triple_relaxation, verify_relaxation_witness

def check():
 if not __debug__:raise RuntimeError('Run without -O')
 print(verify_relaxation_witness())
 old=[Q(v) for v in json.loads((HERE.parent/'reference'/'general_reach_relaxation_witness.json').read_text())['variables']]
 cert=json.loads((HERE/'chronological_chamber_certificate.json').read_text())
 order=sorted(range(64),key=lambda j:(old[6+7*j],j))
 assert cert['order']==order
 violations=[(a,b,i,old[7+7*a+i]-old[7+7*b+i]) for ai,a in enumerate(order) for b in order[ai+1:] for i in range(6) if old[7+7*a+i]>old[7+7*b+i]]
 size,ub,eq,obj=weighted_triple_relaxation()
 for a,b in zip(order,order[1:]):
  for i in range(6): ub.append(({7+7*a+i:1,7+7*b+i:-1},0))
 y=[Q(v) for v in cert['inequality_dual']]; z=[Q(v) for v in cert['equality_dual']]
 assert len(y)==len(ub)==4038 and len(z)==len(eq)==64
 assert max(y)<=0
 residual=[Q(obj.get(i,0)) for i in range(size)]
 for values,(row,rhs) in zip(y,ub):
  for i,a in row.items(): residual[i]-=values*a
 for values,(row,rhs) in zip(z,eq):
  for i,a in row.items(): residual[i]-=values*a
 assert min(residual)>=0
 bound=sum(v*rhs for v,(_,rhs) in zip(y,ub))+sum(v*rhs for v,(_,rhs) in zip(z,eq))
 assert bound==Q(13104,125)
 x=[Q(v) for v in cert['primal']]
 assert len(x)==size and min(x)>=0
 for row,rhs in ub: assert sum(a*x[i] for i,a in row.items())<=rhs
 for row,rhs in eq: assert sum(a*x[i] for i,a in row.items())==rhs
 assert sum(a*x[i] for i,a in obj.items())==bound
 # The saved primal is uniform at all event allocations, a real trajectory.
 assert all(x[7+7*j+i]==x[6+7*j]/6 for j in range(64) for i in range(6))
 assert x[:6]==[Q(6,5)]*6
 assert {x[6+7*j] for j in range(42)}=={Q(66,25)}
 assert {x[6+7*j] for j in range(42,64)}=={Q(546,125)}
 print({'chronological_decreases':len(violations),'maximum_decrease':str(max(v[-1] for v in violations)), 'new_chamber_constraints':378,'exact_chamber_minimum':str(bound),'nonzero_dual_rows':sum(v!=0 for v in y)+sum(v!=0 for v in z),'uniform_primal':'passed'})
 return bound
if __name__=='__main__': check()
