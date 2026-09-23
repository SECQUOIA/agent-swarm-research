"""Independent brute objectives and support-rounding existence checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
from random import Random
import sys,json,hashlib
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;SNAP=OUT.parents[2]/'process/snapshots/stage05-round01'
sys.path.insert(0,str(SNAP/'verification/reference'))
import rounding
manifest=json.loads((SNAP/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((SNAP/p).read_bytes()).hexdigest()==v for p,v in manifest.items())
rng=Random(880713)
def changes(w):return sum(a!=b for a,b in zip(w,w[1:]))
def direct(rows,dt,word):
 A=[F(0)]*len(rows[0]);W=A.copy();e=F(0)
 for col,h,p in zip(rows,dt,word):
  W[p]+=h
  for i,a in enumerate(col):A[i]+=a;e=max(e,abs(A[i]-W[i]))
 return e

def dwell_ok(word,dt,d):
 last=word[0];length=F(0)
 for p,h in zip(word,dt):
  if p!=last:
   if length<d[last]:return False
   last=p;length=F(0)
  length+=h
 return length>=d[last]
cases=completion=negative=onecases=0
for trial in range(55):
 n=rng.randint(2,4);N=rng.randint(1,6)
 dt=tuple(F(rng.randint(1,7),rng.randint(1,5)) for _ in range(N))
 rows=[]
 for h in dt:
  weights=[rng.randrange(5) for i in range(n)];weights[0]+=1
  rows.append(tuple(h*w/sum(weights) for w in weights))
 words=list(product(range(n),repeat=N));obj={w:direct(rows,dt,w) for w in words}
 for s in (0,1,2,N+1):
  for dwell in ((F(0),)*n,tuple(F(rng.randrange(15),3) for i in range(n))):
   feasible=[v for w,v in obj.items() if changes(w)<=s and dwell_ok(w,dt,dwell)]
   sol=rounding.optimal_few_switches(rows,dt,s,minimum_dwell=dwell)
   assert (sol is None)==(not feasible)
   if sol is not None:assert sol.error==min(feasible)==direct(rows,dt,sol.schedule()) and dwell_ok(sol.schedule(),dt,dwell)
   cases+=1
 allowed=tuple(j for j in range(1,N) if rng.randrange(2))
 for p in [None]+list(range(n)):
  feasible=[v for w,v in obj.items() if changes(w)<=1 and (p is None or w[0]==p) and all(j in allowed for j in range(1,N) if w[j]!=w[j-1])]
  sol=rounding.optimal_one_switch(rows,dt,switch_indices=allowed,initial_mode=p)
  assert sol.error==min(feasible)==direct(rows,dt,sol.schedule());onecases+=1
 for length in range(N):
  pre=tuple(rng.randrange(n) for _ in range(length))
  totals=[sum(row[i] for row in rows) for i in range(n)]
  service=[sum(h for h,p in zip(dt,pre) if p==i) for i in range(n)]
  negative+=any(a-b<0 for a,b in zip(totals,service))
  for required in (False,True):
   eligible=[i for i in range(n) if not(required and pre and i==pre[-1])]
   val,j=rounding.complete_with_one_block(rows,dt,pre,require_switch=required)
   assert j in eligible and val==min(direct(rows,dt,pre+(i,)*(N-length)) for i in eligible)
   completion+=1
# Abstract candidate-set exchange checked by complete injective assignment.
rolecases=0
for d,n in ((1,5),(2,9),(3,13)):
 for trial in range(12):
  masses=[F(rng.randrange(10),3) for i in range(n)]
  costs=[[F(rng.randrange(10),3) for i in range(n)] for r in range(d)]
  top=sorted(range(n),key=lambda i:(-masses[i],i))[:d]
  union=set(top)
  for r in range(d):union.update(sorted(range(n),key=lambda i:(costs[r][i],i))[:d])
  def objective(labels):return max([costs[r][i] for r,i in enumerate(labels)]+[masses[i] for i in range(n) if i not in labels])
  assert min(objective(q) for q in permutations(range(n),d))==min(objective(q) for q in permutations(sorted(union),d))
  rolecases+=1
# Exhaust support/floor-ceiling assignments for schedules with multiple switches per cell.
transfercases=assignments=0
for n in (2,3,4):
 for N in (1,2,3,4,5):
  for trial in range(4):
   sub=3;original=tuple(rng.randrange(n) for _ in range(N*sub));h=F(1,sub)
   W=[[F(0)]*n]
   for p in original:
    v=W[-1].copy();v[p]+=h;W.append(v)
   support=[set(original[sub*j:sub*(j+1)]) for j in range(N)]
   accepted=0
   for word in product(*[sorted(s) for s in support]):
    counts=[0]*n;good=True
    for j,p in enumerate(word,1):
     counts[p]+=1
     for i in range(n):
      a=W[sub*j][i];lo=a.numerator//a.denominator;hi=-((-a.numerator)//a.denominator)
      if not lo<=counts[i]<=hi:good=False
    if not good:continue
    assert changes(word)<=changes(original)
    # Original and replacement evaluated at all fine boundaries, not only mesh endpoints.
    V=[F(0)]*n;error=F(0)
    for z in range(N*sub):
     V[word[z//sub]]+=h
     error=max(error,max(abs(a-b) for a,b in zip(V,W[z+1])))
    assert error<1
    accepted+=1;assignments+=1
   assert accepted;transfercases+=1
# Binary nonuniform bound via independent supported-word enumeration.
binary=0
for trial in range(45):
 N=rng.randint(1,6);dt=[F(rng.randint(1,9),rng.randint(1,7)) for _ in range(N)]
 original=tuple(rng.randrange(2) for _ in range(3*N));fine=[h/3 for h in dt for _ in range(3)]
 source=[tuple(h*int(i==p) for i in range(2)) for p,h in zip(original,fine)]
 supports=[set(original[3*j:3*j+3]) for j in range(N)]
 minimum=sum(dt)
 for word in product(*[sorted(s) for s in supports]):
  assert changes(word)<=changes(original)
  expanded=tuple(p for p in word for _ in range(3))
  minimum=min(minimum,direct(source,fine,expanded))
 assert minimum<=max(dt)/2;binary+=1
result={'snapshot_hashes':len(manifest),'fixed_budget_dwell_brute_cases':cases,'one_switch_restricted_cases':onecases,'prefix_completion_comparisons':completion,'prefixes_with_negative_residual':negative,'candidate_set_brute_cases':rolecases,'uniform_transfer_inputs':transfercases,'all_supported_prefix_roundings_checked':assignments,'binary_nonuniform_transfer_cases':binary}
(OUT/'grid-transfer-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
