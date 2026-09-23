from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
import json
import numpy as np
from scipy.optimize import linprog
from network_simplex_benchmarks.baselines import Instance
from network_simplex_benchmarks.strong_baselines import optimize_ef

rng=np.random.default_rng(650502)
counts=dict(networks=0,fixed_cases=0,free_cases=0,joint_results=0,infeasible_results=0,state_blocks_checked=0)
max_error=0.
for graph in range(6):
 arcs=[(0,1,1+graph%2),(1,2,2),(0,2,2),(1,0,1),(2,2,1+graph%3)]
 arcs=[(v,u,cap) if rng.integers(2) else (u,v,cap) for u,v,cap in arcs]
 E=len(arcs);A=np.zeros((3,E));caps=np.array([c for u,v,c in arcs],float)
 for e,(u,v,c) in enumerate(arcs):A[u,e]+=1;A[v,e]-=1
 reference=caps/2;b=A@reference;rank=np.linalg.matrix_rank(A)
 verts=[]
 for inds in combinations(range(E),rank):
  M=A[:,inds]
  if np.linalg.matrix_rank(M)!=rank:continue
  fixed=[e for e in range(E) if e not in inds]
  for bits in product((0,1),repeat=len(fixed)):
   flow=np.zeros(E);flow[fixed]=caps[fixed]*bits
   flow[list(inds)]=np.linalg.lstsq(M,b-A@flow,rcond=None)[0]
   if np.max(np.abs(A@flow-b))<1e-9 and min(flow)>-1e-9 and np.max(flow-caps)<1e-9:
    if not any(np.max(np.abs(flow-v))<1e-9 for v in verts):verts.append(flow)
 assert len(verts)>0
 counts['networks']+=1
 for m in range(6):
  obs=[(e,j) for e in range(E) for j in range(m) if rng.random() < (0 if graph==0 else .45)]
  instance=Instance(arcs,b,m,obs,reference)
  original=[]
  for state in range(m+1):
   y=np.eye(m+1)[state,:m]
   for flow in verts:original.append(np.r_[flow,y,[flow[e]*y[j] for e,j in obs]])
  V=np.array(original).T;n=V.shape[0];c=rng.normal(size=n)
  for mode in ('interior','boundary','free'):
   integers=rng.integers(0,4,size=m+1)
   if mode=='boundary' and m:integers[-1]=0
   if not integers.any():integers[0]=1
   w=tuple(F(int(k),int(sum(integers))) for k in integers)
   yf=np.array(w[:m],float)
   p=np.r_[reference,yf,[reference[e]*yf[j] for e,j in obs]]
   rows=rng.normal(size=(3,n));rhs=rows@p+np.array([0.,.01,.1])
   # Some pure-y contradictions, including the m=0 constant contradiction.
   infeasible=(graph+m)%4==0 and mode!='free'
   if infeasible:
    extra=np.zeros(n)
    if m:extra[E+m-1]=1
    rows=np.vstack((rows,extra));rhs=np.r_[rhs,extra@p-.1]
   eq=np.ones((1,V.shape[1]));eqrhs=[1.]
   if mode!='free':eq=np.vstack((eq,V[E:E+m]));eqrhs=np.r_[1.,yf]
   oracle=linprog(c@V,A_eq=eq,b_eq=eqrhs,A_ub=rows@V,b_ub=rhs,bounds=(0,None),method='highs')
   assert oracle.status in (0,2)
   counts['free_cases' if mode=='free' else 'fixed_cases']+=1
   for merge in (False,True):
    result=optimize_ef(instance,c,None if mode=='free' else w[:m],merge=merge,extra_rows=list(zip(rows,rhs)))
    assert result.status==oracle.status,(graph,m,mode,merge,result.status,oracle.status)
    counts['joint_results']+=1
    if result.status==2:counts['infeasible_results']+=1;continue
    p=result.original_point
    error=max(abs(result.fun-oracle.fun),abs(c@p-result.fun),max(0,np.max(rows@p-rhs)))
    max_error=max(max_error,error);assert error<1e-7
    assert np.max(np.abs(A@p[:E]-b))<1e-8
    if mode!='free':
     assert np.max(np.abs(p[E:E+m]-yf),initial=0)<1e-9
     labels=sorted({j for e,j in obs}) if merge else list(range(m))
     weights=[w[j] for j in labels]+[1-sum(w[j] for j in labels)]
     positive=np.array([k for k in weights if k>0],float)
     assert result.model_stats['variables']==E*len(positive)
     assert result.model_stats['rows']==3*len(positive)+len(rhs)
     flows=result.x.reshape(-1,E)
     assert np.min(flows)>-1e-8 and np.max(flows-positive[:,None]*caps)<1e-8
     for f,weight in zip(flows,positive):
      assert np.max(np.abs(A@f-weight*b))<1e-8;counts['state_blocks_checked']+=1
print(json.dumps(dict(status='PASS',counts=counts,max_error=max_error),indent=2))
