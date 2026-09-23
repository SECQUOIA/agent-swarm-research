"""Independent length-variable LPs, common-refinement errors, coarse brute force."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from random import Random
import numpy as np
from scipy.optimize import linprog
import json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;SNAP=OUT.parents[2]/'process/snapshots/stage05-round01'
sys.path.insert(0,str(SNAP/'verification/stage05'))
from coarsening import certified_coarsen
from continuous_exact import optimal_continuous

def knots(dt):
 t=[F(0)]
 for h in dt:t.append(t[-1]+h)
 return t

def cumulative(rows,dt,t):
 times=knots(dt);n=len(rows[0]);A=[F(0)]*n
 for j,h in enumerate(dt):
  length=max(F(0),min(t,times[j+1])-times[j])
  for i in range(n):A[i]+=length*rows[j][i]/h
 return A

def discrepancy(rows,dt,word,times,one=False):
 n=len(rows[0]);value=F(0)
 for t in sorted(set(knots(dt)+list(times))):
  A=cumulative(rows,dt,t);W=[F(0)]*n
  for p,a,b in zip(word,times,times[1:]):W[p]+=max(F(0),min(t,b)-a)
  value=max(value,max((w-a if one else abs(w-a)) for w,a in zip(W,A)))
 return value

def length_lps(rows,dt,s,one=False):
 t=knots(dt);T=t[-1];N=len(dt);n=len(rows[0]);K=s+1;best=float(T);count=0
 for cells in combinations_with_replacement(range(N),K-1):
  for word in product(range(n),repeat=K):
   A=[];b=[]
   for j,cell in enumerate(cells,1):
    r=[F(h<j) for h in range(K)]+[F(0)]
    A.extend([r,[-v for v in r]]);b.extend([t[cell+1],-t[cell]])
   for j in range(1,K+1):
    for i in range(n):
     if j<K:
      cell=cells[j-1];rate=rows[cell][i]/dt[cell];intercept=cumulative(rows,dt,t[cell])[i]-rate*t[cell]
     else:rate=F(0);intercept=cumulative(rows,dt,T)[i]
     coeff=[F(h<j)*(int(word[h]==i)-rate) for h in range(K)]
     A.append(coeff+[F(-1)]);b.append(intercept)
     if not one:A.append([-v for v in coeff]+[F(-1)]);b.append(-intercept)
   sol=linprog([0]*K+[1],A_ub=np.array(A,float),b_ub=np.array(b,float),A_eq=[[1]*K+[0]],b_eq=[float(T)],bounds=[(0,None)]*K+[(0,float(T))],method='highs')
   assert sol.success
   best=min(best,sol.fun);count+=1
 return best,count
rng=Random(973)
continuous=[]
for n in (2,3):
 for trial in range(2):
  dt=[F(2,5),F(3,5)];rows=[]
  for h in dt:
   nums=[rng.randint(1,7) for _ in range(n)];rows.append(tuple(h*v/sum(nums) for v in nums))
  continuous.append((rows,dt,1,False))
continuous.extend([([(F(1,3),)*3],[F(1)],2,False), ([(F(1,3),)*3],[F(1)],2,True), ([(F(1,3),0),(0,F(1,3)),(F(1,3),0)],[F(1,3)]*3,2,False), ([(1,0)],[F(1)],3,False)])
LPs=0;answers=[]
for rows,dt,s,one in continuous:
 ans=optimal_continuous(rows,dt,s,one_sided=one)
 numeric,count=length_lps(rows,dt,s,one);LPs+=count
 assert abs(numeric-float(ans.error))<1e-8
 assert discrepancy(rows,dt,ans.modes,ans.times,one)==ans.error
 answers.append({'n':len(rows[0]),'N':len(dt),'s':s,'one_sided':one,'error':str(ans.error),'lp_count':count})
coarse=0;clipped=0;strict=0
for trial in range(24):
 n=rng.randint(2,3);N=rng.randint(1,4);M=rng.randint(1,4);s=rng.randint(0,3)
 dt=[F(rng.randint(1,7),rng.randint(2,9)) for _ in range(N)];rows=[]
 for h in dt:
  nums=[rng.randrange(8) for _ in range(n)];nums[0]+=1;rows.append(tuple(h*v/sum(nums) for v in nums))
 T=sum(dt);times=[T*j/M for j in range(M+1)]
 ans=certified_coarsen(rows,dt,s,cells=M)
 differences=[]
 for a,b in zip(times,times[1:]):differences.append(tuple(v-u for u,v in zip(cumulative(rows,dt,a),cumulative(rows,dt,b))))
 assert tuple(differences)==ans.coarse_masses
 vals=[discrepancy(rows,dt,w,times) for w in product(range(n),repeat=M) if sum(a!=b for a,b in zip(w,w[1:]))<=s]
 assert ans.exact_error==min(vals)==discrepancy(rows,dt,ans.schedule,times)
 assert ans.upper==ans.exact_error and ans.mesh_width==T/M
 raw=ans.exact_error-T/M
 assert ans.lower==max(F(0),raw) and ans.lower_strict==(raw>=0)
 clipped+=not ans.lower_strict;strict+=ans.lower_strict
 # Continuous objective via independent length LPs, restricted to s<=2
 # to keep this corroborating optimization finite and small.
 if s<=2:
  optimum,count=length_lps(rows,dt,s);LPs+=count
  assert float(ans.lower)<=optimum+1e-8 and optimum<=float(ans.upper)+1e-8
  if ans.lower_strict:assert float(ans.lower)<optimum-1e-8
 coarse+=1
# Sharpness family: exact supplied continuous competitor and constant-grid error.
sharp=[]
for n in range(2,9):
 T=n+1;rows=[tuple([F(1,n)]*n),tuple(F(T-1)*int(i==n-1) for i in range(n))];dt=[F(1),F(T-1)]
 word=tuple(range(n));times=[F(j,n) for j in range(n)]+[F(T)]
 err=discrepancy(rows,dt,word,times)
 assert err==F(n-1,n*n)
 constant=discrepancy(rows,dt,(n-1,),(F(0),F(T)))
 assert constant==1-F(1,n)
 assert constant-err==(1-F(1,n))**2
 sharp.append(str(constant-err))
# Dwell obstruction by explicit allowed boundary intervals, independently of DP.
for M in (1,3,5,7,9,11):
 assert not [F(j,M) for j in range(1,M) if F(j,M)>=F(1,2) and 1-F(j,M)>=F(1,2)]
 source=[(F(1,2),0),(0,F(1,2))];dt=[F(1,2)]*2
 assert min(discrepancy(source,dt,(i,),(F(0),F(1))) for i in range(2))==F(1,2)
 assert discrepancy(source,dt,(0,1),(F(0),F(1,2),F(1)))==0
result={'continuous_exact_comparisons':answers,'independent_length_LPs_total':LPs,'coarse_cases':coarse,'clipped_lower_cases':clipped,'strict_lower_cases':strict,'sharpness_gaps_n2_to_n8':sharp,'odd_grid_dwell_obstructions':6}
(OUT/'continuous-coarse-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
