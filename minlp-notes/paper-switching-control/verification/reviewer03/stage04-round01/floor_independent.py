"""Independent floor-history audit by intersections of complete-word bitsets.
Does not use the manuscript's nine-entry cost DP or import author code.
"""
from itertools import product,permutations
from collections import Counter,defaultdict
from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent
SNAP=OUT.parents[2]/'process/snapshots/stage04-round01'
manifest=json.loads((SNAP/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((SNAP/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
results={'snapshot_hashes':len(manifest),'histograms':{}}
canonical=((0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1),(2,1,1),(2,1,2))
for N in (5,6,7):
 words=list(product(range(3),repeat=N));compatible=[defaultdict(int) for j in range(N)]
 coordinate=[defaultdict(int) for j in range(N)];switch_masks=defaultdict(int);prefixes=[]
 for number,w in enumerate(words):
  bit=1<<number;ns=sum(a!=b for a,b in zip(w,w[1:]));switch_masks[ns]|=bit
  counts=[0,0,0];pre=[]
  for j,a in enumerate(w):
   counts[a]+=1;pre.append(tuple(counts))
   for i,c in enumerate(counts):coordinate[j][(i,c)]|=bit
   # A count vector can be in a strict floor chamber at an offset of
   # one or two binary ones. Enumerate that relation directly.
   for offset in product((0,1),repeat=3):
    if sum(offset) not in (1,2):continue
    floor=tuple(c-d for c,d in zip(counts,offset))
    if min(floor)>=0:compatible[j][floor]|=bit
  prefixes.append(pre)
 histogram=Counter();bad=[];realization_checks=0
 def visit(history,mask):
  nonlocal_dummy=None
  j=len(history)
  if j==N:
   assert mask
   # Every lower/upper bound is reached by a full word, so averaging
   # the full feasible words realizes a strictly interior input.
   for t,floor in enumerate(history):
    for i,f in enumerate(floor):
     assert mask&coordinate[t][(i,f)]
     assert mask&coordinate[t][(i,f+1)]
   minimum=next(s for s in range(N) if mask&switch_masks[s])
   histogram[minimum]+=1
   if minimum>=4:bad.append(tuple(history))
   return
  previous=history[-1]
  for increment in product((0,1),repeat=3):
   floor=tuple(a+b for a,b in zip(previous,increment))
   if (j+1)-sum(floor) not in (1,2):continue
   visit(history+[floor],mask&compatible[j][floor])
 visit([(0,0,0)],compatible[0][(0,0,0)])
 results['histograms'][str(N)]=dict(sorted(histogram.items()))
 if N==5:assert histogram=={0:3,1:138,2:255}
 if N==6:assert histogram=={0:3,1:255,2:1377,3:237}
 if N==7:
  assert histogram=={0:3,1:414,2:4542,3:3891,4:6}
  orbit={tuple(tuple(row[p[i]] for i in range(3)) for row in canonical) for p in permutations(range(3))}
  assert set(bad)==orbit and len(bad)==6
  feasible=(1<<len(words))-1
  for j,f in enumerate(canonical):feasible&=compatible[j][f]
  assert feasible.bit_count()==104
  triple=[(1,1,1),(4,1,1),(4,4,1),(4,4,4),(7,4,4),(8,5,5),(8,5,8)]
  errors=[max(abs(a-3*c) for row,pre in zip(triple,pref) for a,c in zip(row,pre)) for pref in prefixes]
  best=min(e for w,e in zip(words,errors) if sum(a!=b for a,b in zip(w,w[1:]))<=3)
  assert best==4
  repairs=[(1,2,0,0,0,2,2),(0,0,2,1,1,2,2),(0,0,1,1,2,2,0)]
  for i,w in enumerate(repairs):
   pre=prefixes[words.index(w)]
   violations=[(j,c) for j,(f,p) in enumerate(zip(canonical,pre)) for c in range(3) if not f[c]<=p[c]<=f[c]+1]
   assert violations==[(i+1,i)]
   assert sum(a!=b for a,b in zip(w,w[1:]))<=3
results['strict_histories_with_complete_word_realization']=396+1872+8856
results['seven_cell_chamber_words']=104
results['seven_cell_original_objective_optimum']='4/3'
(OUT/'floor-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
