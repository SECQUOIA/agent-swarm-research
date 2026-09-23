"""Stage 6 reviewer 03: independent source parsing and cell-count-state optimization.
No manuscript solver is imported. Exact integers/rationals only.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from math import lcm
from statistics import median
import hashlib,json
P=Path(__file__).resolve().parent
S=P.parents[2]/'process/snapshots/stage06-round01'
D=json.loads((S/'verification/stage06/results.json').read_text())
raw=(P/'source.csv').read_bytes()
assert hashlib.sha256(raw).hexdigest()==D['provenance']['sha256']
lines=[line.split() for line in raw.decode().splitlines()]
assert lines[0]==['t','x1','x2','w1','w2','w3']
source=[[Q(x) for x in line] for line in lines[1:]]
assert len(source)==12001
rows=[];normalization=Q(0);quantization=Q(0);deltas=[Q(0)]*3;cumulative=Q(0)
for j,line in enumerate(source[:-1]):
 assert line[0]==Q(j,1000) and source[j+1][0]-line[0]==Q(1,1000)
 weights=line[3:];norm=[w/sum(weights) for w in weights]
 ints=[];rem=[]
 for i,x in enumerate(norm):
  a,b=divmod(x.numerator*10**6,x.denominator);ints.append(a);rem.append((Q(b,x.denominator),-i))
 for _,minus_i in sorted(rem,reverse=True)[:10**6-sum(ints)]:ints[-minus_i]+=1
 assert sum(ints)==10**6 and min(ints)>=0
 normalization=max(normalization,*[abs(w-x) for w,x in zip(weights,norm)])
 quantization=max(quantization,*[abs(Q(a,10**6)-x) for a,x in zip(ints,norm)])
 for i in range(3):deltas[i]+=(norm[i]-Q(ints[i],10**6))/1000
 cumulative=max(cumulative,*map(abs,deltas));rows.append(ints)
assert normalization==Q(D['provenance']['normalization_max'])
assert quantization==Q(D['provenance']['quantization_max'])
assert cumulative==Q(D['provenance']['cumulative_quantization_max'])
# All source cell masses are now integer units of 10^-9 time.
scale=10**9; fine_width=10**6; N=len(rows);T=N*fine_width
prefix=[[0]*3]
for row in rows:prefix.append([a+b for a,b in zip(prefix[-1],row)])
totals=prefix[-1]
# Direct all-pair endpoint errors on every boundary, including constants.
def endpoint_score(p,q,t,A):
 service=[t if i==p else 0 for i in range(3)]
 final=[(t if i==p else T-t if i==q else 0) for i in range(3)]
 return max(*(abs(A[i]-service[i]) for i in range(3)),*(abs(totals[i]-final[i]) for i in range(3)))
best=T;pairs={}
for p in range(3):
 for q in range(3):
  if p==q:continue
  scores=[endpoint_score(p,q,j*fine_width,prefix[j]) for j in range(N+1)]
  pairs[p,q]=min(scores);best=min(best,min(scores))
assert Q(best,scale)==Q(D['public_fine']['error'])
# Independently solve 2-variable affine max problems: all intersections between
# every signed endpoint affine form within each input cell, plus cell edges.
# Unlike the manuscript crossing implementation, do not select just two terms.
continuous_pairs={}
for p in range(3):
 for q in range(3):
  if p==q:continue
  candidates=[]
  for j,row in enumerate(rows):
   a=j*fine_width;b=a+fine_width
   forms=[]
   for i in range(3):
    slope=Q(row[i],fine_width)-int(i==p)
    intercept=prefix[j][i]-Q(row[i],fine_width)*a
    forms.extend([(slope,intercept),(-slope,-intercept)])
    final_slope=-(int(i==p)-int(i==q));final_intercept=totals[i]-T*int(i==q)
    forms.extend([(Q(final_slope),Q(final_intercept)),(Q(-final_slope),Q(-final_intercept))])
   points={Q(a),Q(b)}
   for x,(m,c) in enumerate(forms):
    for mm,cc in forms[:x]:
     if m!=mm:
      t=(cc-c)/(m-mm)
      if a<=t<=b:points.add(t)
   value=min(max(m*t+c for m,c in forms) for t in points)
   candidates.append(value)
  continuous_pairs[p,q]=min(candidates)
  archived=next(x for x in D['public_continuous_one']['all_pairs'] if (x['p'],x['q'])==(p,q))
  assert continuous_pairs[p,q]/scale==Q(archived['error'])
print('Public source and six independent piecewise-affine envelope minima passed',flush=True)
# Integer state DP: state=(total cells used by first modes,last label,changes).
# Its value is the least maximum endpoint error, so histories with this same
# state have identical future error possibilities. No block subset is used.
def cell_state_opt(rows,width,budget):
 n=len(rows[0]);A=[0]*n; states={(tuple([0]*n),-1,0):0};visited=0
 for row in rows:
  A=[a+b for a,b in zip(A,row)];nxt={}
  for (counts,last,s),value in states.items():
   for mode in range(n):
    ss=s+int(last!=-1 and last!=mode)
    if ss>budget:continue
    c=list(counts);c[mode]+=1;c=tuple(c)
    e=max(value,*(abs(A[i]-c[i]*width) for i in range(n)))
    key=(c,mode,ss)
    if key not in nxt or e<nxt[key]:nxt[key]=e
  states=nxt;visited+=len(states)
 return [min(e for (_,_,s),e in states.items() if s<=b) for b in range(budget+1)],visited
public=[];visited=0
for M in (12,24,48):
 block=N//M
 coarse=[[sum(rows[j][i] for j in range(a,a+block)) for i in range(3)] for a in range(0,N,block)]
 derived=next(g for g in json.loads((S/'verification/stage06/derived_public.json').read_text())['grids'] if g['N']==M)
 assert [[Q(x,scale) for x in row] for row in coarse]==[list(map(Q,row)) for row in derived['masses']]
 vals,count=cell_state_opt(coarse,block*fine_width,3);visited+=count
 for s,v in enumerate(vals):
  archived=next(r for r in D['public'] if (r['N'],r['budget'])==(M,s))
  assert Q(v,scale)==Q(archived['error'])
  h=Q(12,M);assert Q(archived['general_lower'])==max(0,Q(v,scale)-h)
  assert archived['lower_strict']==(Q(v,scale)>=h)
 public.append({'N':M,'values':[str(Q(v,scale)) for v in vals],'states':count})
 print('Independent cell-state DP public',M,public[-1],flush=True)
# Controlled cases: exhaustive raw cell words, no padded block enumeration.
controlled=[]
for r in D['controlled']:
 n,N,s=r['n'],r['N'],r['budget'];masses=[]
 for j in range(N):
  w=[1+((j+2)*(i+3)+i*i)%11 for i in range(n)]
  masses.append([Q(x,N*sum(w)) for x in w])
 denominator=lcm(N,*[x.denominator for row in masses for x in row]);width=denominator//N
 A=[[0]*n]
 for row in masses:A.append([a+int(x*denominator) for a,x in zip(A[-1],row)])
 best=denominator;eligible=0
 for word in product(range(n),repeat=N):
  if sum(a!=b for a,b in zip(word,word[1:]))>s:continue
  counts=[0]*n;e=0;eligible+=1
  for j,p in enumerate(word,1):
   counts[p]+=1;e=max(e,*(abs(A[j][i]-counts[i]*width) for i in range(n)))
  best=min(best,e)
 assert Q(best,denominator)==Q(r['error'])
 controlled.append({'n':n,'N':N,'s':s,'eligible_words':eligible,'optimum':str(Q(best,denominator))})
# Uniform convergence uses independent cell-state recurrence too.
convergence=[]
for r in D['uniform_convergence']:
 M=r['N'];values,count=cell_state_opt([[1]*3 for _ in range(M)],3,2)
 val=Q(values[2],3*M);assert val==Q(r['error']) and Q(r['lower'])<=Q(1,6)<=val
 convergence.append([M,str(val)])
# Exact formula transition regimes and comparison threshold.
thresholds=[]
for s in (1,2,3):
 first=next(n for n in range(s+2,50) if 1/(Q(n)*(Q(n,n-1)**(s+1)-1))>Q(1,s+2));thresholds.append(first)
assert thresholds==[5,8,12]
for n in range(2,30):
 for k in range(1,80):assert (Q(2*n-3,2*n-2)/k<Q(1,k+1))==(k>2*n-3)
# Timing records: medians, repetition counts and nonnegative observations.
records=[D['public_fine']]+D['public']+D['scaling']+[r[m] for r in D['controlled'] for m in ('subset_dp','word_enumeration')]
for r in records:
 for kind in ('cpu','wall'):
  samples=r[kind+'_samples_s'];assert len(samples)==3 and min(samples)>=0
  assert median(samples)==r[kind+'_median_s']
result={'source_sha256':hashlib.sha256(raw).hexdigest(),'normalization_max':str(normalization),'quantization_max':str(quantization),'cumulative_quantization_max':str(cumulative),'fine_grid_value':str(Q(best if False else min(pairs.values()),scale)),'continuous_pair_values':{str(k):str(v/scale) for k,v in continuous_pairs.items()},'public_state_DP':public,'public_states_visited':visited,'controlled_full_cell_words':controlled,'uniform_convergence':convergence,'minimax_transitions':thresholds,'timing_records_checked':len(records)}
(P/'independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('All independent checks passed',flush=True)
