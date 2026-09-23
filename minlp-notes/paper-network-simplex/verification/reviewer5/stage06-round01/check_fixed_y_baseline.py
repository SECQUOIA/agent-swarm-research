from time import perf_counter
from statistics import median
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,eye,kron
from network_simplex_benchmarks.baselines import incidence,block_chain
from network_simplex_benchmarks.paper_stage06 import local_labels_instance
from network_simplex_benchmarks.strong_baselines import optimize_ef
from network_simplex_compressed import CompressedNetworkSimplex

def fixed(instance,c,y,extra,merge=False):
 start=perf_counter();E=instance.edge_count;m=instance.simplex_size
 labels=sorted({j for e,j in instance.observations}) if merge else list(range(m))
 weights=[y[j] for j in labels]+[1-sum(y[j] for j in labels)]
 slots={j:i for i,j in enumerate(labels)};q=len(weights)
 A=incidence(instance); b=np.asarray(instance.balances,float)
 eq=kron(eye(q,format='csr'),A,format='csr');rhs=np.kron(np.asarray(weights,float),b)
 cost=np.tile(c[:E],q)
 for k,(e,j) in enumerate(instance.observations):cost[slots[j]*E+e]+=c[E+m+k]
 caps=np.kron(np.asarray(weights,float),np.asarray([a[2] for a in instance.arcs],float))
 ub=[];ubs=[]
 for row,bound in extra:
  mapped=np.tile(row[:E],q)
  for k,(e,j) in enumerate(instance.observations):mapped[slots[j]*E+e]+=row[E+m+k]
  ub.append(mapped);ubs.append(float(bound)-np.dot(row[E:E+m],np.asarray(y,float)))
 build=perf_counter()-start
 ans=linprog(cost,A_eq=eq,b_eq=rhs,A_ub=csr_matrix(np.asarray(ub)) if ub else None,b_ub=ubs if ub else None,
             bounds=np.column_stack((np.zeros(q*E),caps)),method='highs')
 total=perf_counter()-start
 assert ans.status==0
 return {'objective':float(ans.fun+np.dot(c[E:E+m],np.asarray(y,float))),'variables':q*E,'rows':eq.shape[0]+len(ub),'build_seconds':build,'total_seconds':total}

raw=json.load(open('paper-network-simplex/verification/stage06-benchmarks.json'))
out=[]
for case in raw['optimization']:
 inst=local_labels_instance() if case['name']=='all_labels_global_but_few_per_block' else block_chain(seed=33,blocks=4,paths=5,states=128)
 c=np.asarray(case['objective_vector']);y=list(map(F,case['y']));extra=[(np.asarray(r['coefficients']),F(r['rhs'])) for r in case['extra_rows']]
 def current(merge):
  start=perf_counter();r=optimize_ef(inst,c,y_fixed=y,merge=merge,extra_rows=extra)
  return {'objective':float(r.fun),'total_seconds':perf_counter()-start}
 def compact():
  start=perf_counter();m=CompressedNetworkSimplex(inst.arcs,-inst.balances,inst.simplex_size,inst.observations)
  for row,rhs in extra:m.ub.append(({i:F(str(v)) for i,v in enumerate(row) if v},rhs))
  ans=m.optimize(c,y_fixed=y)
  return {'objective':float(ans.fun),'total_seconds':perf_counter()-start}
 methods={'constant_full':lambda:fixed(inst,c,y,extra),'constant_global':lambda:fixed(inst,c,y,extra,True),'current_full':lambda:current(False),'current_global':lambda:current(True),'initial':compact}
 for f in methods.values():assert abs(f()['objective']-case['objective'])<1e-7
 runs=[]
 names=list(methods)
 for i in range(5):
  order=names[i:]+names[:i];run={}
  for name in order:
   v=methods[name]();assert abs(v['objective']-case['objective'])<1e-7;run[name]=v
  runs.append(run)
 out.append({'case':case['name'],'runs':runs,'median_ms':{name:1000*median(r[name]['total_seconds'] for r in runs) for name in methods}})
print(json.dumps(out,indent=2))
