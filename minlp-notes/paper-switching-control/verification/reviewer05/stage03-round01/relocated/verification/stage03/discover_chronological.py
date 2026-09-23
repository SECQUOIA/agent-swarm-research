"""Optional SciPy discovery for one chronological chamber; no global claim.

Creates a rational dual candidate. check_chronological.py verifies it without
SciPy. The chamber fixes the weak event order of the old nonphysical witness.
"""
from pathlib import Path
import sys, json
from fractions import Fraction as Q
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'reference'))
from general_reach_research import weighted_triple_relaxation
HERE=Path(__file__).resolve().parent
ref=HERE.parent/'reference'
x=[Q(v) for v in json.loads((ref/'general_reach_relaxation_witness.json').read_text())['variables']]
size,ub,eq,obj=weighted_triple_relaxation()
order=sorted(range(64),key=lambda j:(x[6+7*j],j))
for a,b in zip(order,order[1:]):
 for i in range(6): ub.append(({7+7*a+i:1,7+7*b+i:-1},0))
def dense(rows):
 a=np.zeros((len(rows),size)); b=[]
 for row,(values,rhs) in enumerate(rows):
  for col,v in values.items(): a[row,col]=v
  b.append(rhs)
 return a,np.array(b)
a,b=dense(ub); ae,be=dense(eq)
c=np.zeros(size)
for i,v in obj.items(): c[i]=v
sol=linprog(c,A_ub=a,b_ub=b,A_eq=ae,b_eq=be,bounds=(0,None),method='highs')
print(sol.message,sol.fun, 'target',float(Q(13104,125)))
assert sol.success
cert={'order':order,'inequality_dual':[str(Q(float(v)).limit_denominator(10**6)) for v in sol.ineqlin.marginals], 'equality_dual':[str(Q(float(v)).limit_denominator(10**6)) for v in sol.eqlin.marginals], 'primal':[str(Q(float(v)).limit_denominator(10**6)) for v in sol.x]}
# Use the explicit uniform-control primal, including its genuine first reaches.
cert['primal']=[str(Q(6,5))]*6
for j in range(64):
 t=Q(66,25) if j<42 else Q(546,125)
 cert['primal'] += [str(t)]+[str(t/6)]*6
(HERE/'chronological_chamber_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
