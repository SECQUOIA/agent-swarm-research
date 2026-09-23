"""Exact author-stage checks, with explicit reuse of archived audit helpers.

Imports never execute historical main functions or write their result records.
New rational fixtures and elementary scope tests are authored for this stage.
These tiny exhaustive checks are proof tests, not a large-instance solver.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'

def load(name):
    path=ROOT/'legacy'/f'{name}.py'
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def psd(M):
    return M==M.T and all(M.extract(ix,ix).det()>=0 for q in range(1,M.rows+1) for ix in combinations(range(M.rows),q))

R=s.Rational
stats=Counter()
# Scope hardness tested for all subsets of the cubic graph K3,3.
A=s.zeros(6)
for i in range(3):
 for j in range(3,6): A[i,j]=A[j,i]=1
C=s.eye(6)+A/12
assert psd(C-3*s.eye(6)/4) and psd(5*s.eye(6)/4-C)
for k in range(7):
 for S in combinations(range(6),k):
  independent=sum(A[i,j] for i,j in combinations(S,2))==0
  value=(s.ones(1,k)*C.extract(S,S).inv()*s.ones(k,1))[0] if k else s.Integer(0)
  assert value==k if independent else value<=k-R(1,9)
  stats['hardness_subsets']+=1
# Prior local-cost counterexample and near-singular kernel necessity.
M=s.Matrix([[2,1],[1,3]])
assert M.inv()[0,0]==R(3,5) and 1/M[0,0]==R(1,2)
a=s.Matrix([1,0]);b=s.Matrix([1,R(1,2**120)])
assert not psd(b*b.T-R(1,2)*a*a.T)
# Exact scalar transfer constants across accuracy and promise values.
for eps in (R(1,10000),R(1,7),R(999,1000)):
 eta,delta=eps/4,eps/8
 assert (1-eta)*(1-delta)/(1+delta)>=1-eps
 assert (1+eta)*(1+delta)/(1-delta)<=1+eps
 for rho in (R(0),R(1,3),R(9,10)):
  for B in (R(0),R(1),R(7)):
   zeta=eps*(1-rho)**2/16
   D=4+16*B+4*zeta/(1-rho**2)
   alpha=eps/(4*(D+1))
   assert (1-alpha*D)/(1+alpha)>=1-eps/4
   stats['scalar_prior_ratio_checks']+=1
# All-basis exact DAG tests on new oblique and variable-length fixtures.
dag=load('review_psd_approximation_set')
counts=Counter();cases=[]
v=s.Matrix([1,-2,3]);w=s.Matrix([0,R(1,2**70),R(-1,2**70)])
lift=lambda X:s.Matrix.hstack(v,w)*X*s.Matrix.hstack(v,w).T
cases.append(dag.review_case('stage3_oblique_variable_paths',4,
 [(0,3,lift(s.Matrix([[1,R(-1,10)],[R(-1,10),1]]))),
  (0,1,lift(s.diag(R(1,2),0))), (1,3,lift(s.diag(0,R(1,2)))),
  (0,2,s.zeros(3)),(2,3,s.zeros(3))],s.zeros(3),R(1,3),counts))
cases.append(dag.review_case('stage3_signed_profile_collision',3,
 [(0,2,R(1,100)*s.Matrix([[2,-1],[-1,2]])),
  (0,1,R(1,200)*s.Matrix([[2,-1],[-1,2]])),
  (1,2,R(1,201)*s.Matrix([[2,-1],[-1,2]]))],s.eye(2),R(2,5),counts))
# Existing adversarial matroid fixtures cover contraction, rank loss, aliases,
# signed profiles, input-sized q, range filtering and coefficient interpolation.
mat=load('review_represented_matroid_psd')
m_cases=[]
for fixture in mat.fixtures():m_cases.append(mat.review_case(*fixture))
mat.auxiliary_checks()
report={'status':'passed','scope':'tiny exact proof checks, not runtime benchmarks',
 'new_elementary_checks':dict(stats),'dag_cases':cases,'dag_counts':dict(counts),
 'matroid_cases':m_cases,'matroid_counts':dict(mat.STATS),
 'reuse':'archived audit helper imports; their main/output routines are not run'}
(OUT/'stage03-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'passed','new_checks':dict(stats),'dag_cases':len(cases),'matroid_cases':len(m_cases)}))
