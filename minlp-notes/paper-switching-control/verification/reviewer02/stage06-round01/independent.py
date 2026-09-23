from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations
import hashlib,json
ROOT=Path(__file__).resolve().parent
SNAP=ROOT/'relocated'
arch=json.loads((SNAP/'verification/stage06/results.json').read_text())
derived=json.loads((SNAP/'verification/stage06/derived_public.json').read_text())
raw=(ROOT/'public.csv').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883'
lines=raw.decode().splitlines();assert lines[0].split()==['t','x1','x2','w1','w2','w3']
parsed=[list(map(Q,line.split())) for line in lines[1:]]
assert len(parsed)==12001
counts=[];normbound=Q(0);quantbound=Q(0);cumerr=[Q(0)]*3;cummax=Q(0)
for j,row in enumerate(parsed[:-1]):
 assert parsed[j+1][0]-row[0]==Q(1,1000)
 weights=row[3:];normal=[w/sum(weights) for w in weights]
 floored=[int(x*10**6) for x in normal]
 # Increment largest remainder by repeated selection, rather than slicing a sorted list.
 remainders=[x*10**6-k for x,k in zip(normal,floored)]
 for _ in range(10**6-sum(floored)):
  p=max(range(3),key=lambda i:(remainders[i],-i));floored[p]+=1;remainders[p]=-1
 assert sum(floored)==10**6 and min(floored)>=0
 counts.append(floored)
 normbound=max(normbound,*[abs(x-y) for x,y in zip(weights,normal)])
 quantbound=max(quantbound,*[abs(x-Q(y,10**6)) for x,y in zip(normal,floored)])
 cumerr=[z+(x-Q(y,10**6))/1000 for z,x,y in zip(cumerr,normal,floored)]
 cummax=max(cummax,*map(abs,cumerr))
assert normbound==Q(arch['provenance']['normalization_max'])<Q(4959,10**10)
assert quantbound==Q(arch['provenance']['quantization_max'])<Q(1,10**6)
assert cummax==Q(arch['provenance']['cumulative_quantization_max'])<Q(12,10**6)
# Integrated occupations in integer units 10^-9.
P=[(0,0,0)]
for row in counts:P.append(tuple(x+y for x,y in zip(P[-1],row)))
T=12*10**9;unit=10**6
best=T;bestword=None
for j in range(12001):
 for p,q in product(range(3),repeat=2):
  e=0
  for i in range(3):
   e=max(e,abs(P[j][i]-j*unit*(i==p)),abs(P[-1][i]-j*unit*(i==p)-(12000-j)*unit*(i==q)))
  if e<best:best=e;bestword=(p,q,j)
assert Q(best,10**9)==Q(1889,1000)
print('Fine all-word endpoint optimum:',Q(best,10**9),bestword,flush=True)
# Independently minimize every piecewise-linear pair objective using all cell
# endpoints and all pairwise intersections of its three affine pieces.
records=[]
for p,q in [(p,q) for p in range(3) for q in range(3) if p!=q]:
 omitted=next(i for i in range(3) if i not in (p,q));best=Q(T);time=None
 for j in range(12000):
  lines=[(unit-counts[j][p],j*unit-P[j][p]),(-unit,T-P[-1][q]-j*unit),(0,P[-1][omitted])]
  candidates={Q(0),Q(1)}
  for (a,b),(c,d) in combinations(lines,2):
   if a!=c:
    x=Q(d-b,a-c)
    if 0<=x<=1:candidates.add(x)
  for x in candidates:
   value=max(a*x+b for a,b in lines)
   if value<best:best=value;time=(j+x)/1000
 records.append((p,q,best/10**9,time))
expected={(r['p'],r['q']):Q(r['error']) for r in arch['public_continuous_one']['all_pairs']}
assert all(e==expected[p,q] for p,q,e,t in records)
assert min(e for p,q,e,t in records)==Q(4721469,2500000)
print('All continuous pair minima:',records,flush=True)
# Independent exhaustive labeled-word enumerator, direct integer endpoint service.
def brute(prefix,dt,s):
 n=len(prefix[0]);N=len(prefix)-1;k=min(s+1,N);best=10**30;cases=0
 for inside in combinations(range(1,N),k-1):
  bounds=(0,)+inside+(N,)
  for word in product(range(n),repeat=k):
   service=[0]*n;error=0
   for h,p in enumerate(word):
    service[p]+=(bounds[h+1]-bounds[h])*dt
    error=max(error,*[abs(prefix[bounds[h+1]][i]-service[i]) for i in range(n)])
   best=min(best,error);cases+=1
 return best,cases
coarseresults=[]
for M in (12,24,48):
 g=[P[j*12000//M] for j in range(M+1)]
 saved=next(r for r in derived['grids'] if r['N']==M)
 assert [[Q(y-x,10**9) for x,y in zip(g[j],g[j+1])] for j in range(M)]==[list(map(Q,row)) for row in saved['masses']]
 for s in range(4):
  value,cases=brute(g,T//M,s);want=next(r for r in arch['public'] if r['N']==M and r['budget']==s)
  assert Q(value,10**9)==Q(want['error'])
  lower=Q(value,10**9)-Q(12,M)
  assert Q(want['general_lower'])==max(0,lower) and want['lower_strict']==(lower>=0)
  coarseresults.append((M,s,str(Q(value,10**9)),cases))
  print('Public exhaustive:',coarseresults[-1],flush=True)
for row in arch['uniform_convergence']:
 M=row['N'];prefix=[(j,j,j) for j in range(M+1)]
 value,cases=brute(prefix,3,2)
 assert Q(value,3*M)==Q(row['error'])
# Exact transition tests; classical coefficient strictly improves T/(k+1)
# precisely when k>2n-3.
for s,want in ((1,5),(2,8),(3,12)):
 transition=next(n for n in range(s+2,100) if 1/(Q(n)*(Q(n,n-1)**(s+1)-1))>Q(1,s+2))
 assert transition==want
for n in range(2,20):
 for k in range(1,40):
  assert (Q(2*n-3,(2*n-2)*k)<Q(1,k+1))==(k>2*n-3)
# Every stored timing median agrees with its three archived samples.
def timings(obj):
 if isinstance(obj,dict):
  if 'cpu_samples_s' in obj:
   for typ in ('cpu','wall'):
    samples=obj[typ+'_samples_s'];assert len(samples)==3 and min(samples)>=0
    assert sorted(samples)[1]==obj[typ+'_median_s']
  for v in obj.values():timings(v)
 elif isinstance(obj,list):
  for v in obj:timings(v)
timings(arch)
print('PASS: exact source transformation, every derived mass, all six continuous pair minima, all twelve public grid optima including M48/s3, uniform convergence, regime thresholds, classical crossover, timing medians',flush=True)
(ROOT/'independent-results.json').write_text(json.dumps({'public_exhaustive':coarseresults,'continuous_pairs':[(p,q,str(e),str(t)) for p,q,e,t in records]},indent=2)+'\n')
