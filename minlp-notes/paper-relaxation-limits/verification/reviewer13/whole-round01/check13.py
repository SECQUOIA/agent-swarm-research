from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import json, re, hashlib
root=Path('/home/sgusev/repo/minlp-notes/paper-relaxation-limits')
snapshot=root/'process/snapshots/whole-round01'
result={}
# Direct interval integration of count moments, independent of the finite-spreading induction.
def binom(k,j):
 return comb(k,j) if 0<=j<=k else 0

def moments(p,coins):
 out=[Q(0)]*(len(p)+2)
 cuts=sorted({Q(0),Q(1),*p,*(1-x for x in p)})
 for left,right in zip(cuts,cuts[1:]):
  t=(left+right)/2
  k=sum(t<x if bit else t>1-x for x,bit in zip(p,coins))
  for j in range(len(out)):
   out[j]+=(right-left)*binom(k,j)
 return out

cases=0; coeffs=0
for N in range(2,8):
 beta=Q(N*(N-1),2*(N//2)*(N-N//2))
 for d in range(1,N+1):
  weights={}
  for J in combinations(range(N),N//2):
   coin=tuple(i in J for i in range(d)); weights[coin]=weights.get(coin,0)+1
  den=comb(N,N//2)
  for p in combinations_with_replacement([Q(i,4) for i in range(5)],d):
   s=sum(p); k=s.numerator//s.denominator; theta=s-k
   V=[(1-theta)*binom(k,j)+theta*binom(k+1,j) for j in range(d+2)]
   C=moments(p,(1,)*d)
   P=[Q(1)]
   for x in p:
    P=[P[j] if j<len(P) else Q(0) for j in range(len(P)+1)]
    for j in range(len(P)-1,0,-1): P[j]+=x*P[j-1]
   P.append(Q(0))
   O=[Q(0)]*(d+2)
   for coin,w in weights.items():
    vals=moments(p,coin)
    for j in range(d+2): O[j]+=Q(w,den)*vals[j]
   for j in range(d+2):
    f=beta*(C[j]-O[j])+V[j]-P[j]+(C[j-1]-P[j-1] if j else 0)
    assert f>=0,(N,p,j,f)
    coeffs+=1
   cases+=1
result['balanced_coefficients']={'sorted_grid_support_cases':cases,'coefficients':coeffs,'ambient_N':'2..7','grid':'0,1/4,1/2,3/4,1','arithmetic':'exact fractions; interval count integration','minimum_slack':'0'}
# Exhaustive rational proof of profile equality at every stratum, all tested radices and levels.
radix=0
for b in range(2,13):
 for L in range(2,41):
  M=lambda q:Q((L-q)*(b-1)+b,b**q)
  choices=[s for s in range(1,L) if M(s+1)<=1<=M(s)]
  assert choices
  for s in choices:
   total=Q(0); mean=Q(0)
   mix=(1-M(s+1))/(M(s)-M(s+1))
   for l in range(L+1):
    wt=Q(b-1,b**(l+1)) if l<L else Q(1,b**L)
    for q,prob in [(s,mix),(s+1,1-mix)]:
     R=b**(l-q+1) if l>=q else 0
     actual=sum(min(b**j,R) for j in range(1,l+1))
     affine=s*R+sum(b**j for j in range(1,l-s+1))
     assert actual==affine
     total+=wt*prob*actual; mean+=wt*prob*R
   assert mean==1 and total==s+Q(L-s,b**s)
   radix+=1
result['radix_profiles']={'exact_cases':radix,'radices':'2..12','levels':'2..40'}
# Repository ledger checks examine concrete paths and labels, not PASS words.
text='\n'.join(p.read_text() for p in [snapshot/'main.tex',*(snapshot/'sections').glob('*.tex')])
labels=re.findall(r'\\label\{([^}]+)\}',text)
assert len(labels)==len(set(labels))
ledger=(snapshot/'process/claim-coverage.md').read_text()
cited=set(re.findall(r'`((?:eq|thm|lem|prop|cor|ex|sec|subsec|app|tab):[^`]+)`',ledger))
assert cited<=set(labels), cited-set(labels)
paths=set(re.findall(r'`((?:results|notes|code)/[^`]+\.(?:md|py))`',ledger))
assert all((root.parent/p).is_file() for p in paths)
result['coverage']={'distinct_ledger_labels':len(cited),'manuscript_labels':len(labels),'referenced_repo_files_present':len(paths),'all_required_labels_present':True}
result['pdf_sha256']=hashlib.sha256((snapshot/'main.pdf').read_bytes()).hexdigest()
print(json.dumps(result,indent=2))
(root/'verification/reviewer13/whole-round01/check13.json').write_text(json.dumps(result,indent=2)+'\n')
