"""Reviewer13 independent finite checks; run from repository root."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import contextlib, io, re, json, hashlib
root=Path('paper-relaxation-limits')
snap=root/'process/snapshots/stage06-round01'
out=root/'verification/reviewer13/stage06-round01'
result={'frozen_pdf_sha256':hashlib.sha256((snap/'main.pdf').read_bytes()).hexdigest()}
# Execute only the displayed, self-contained standard-library certificates.
for name in ['appendix-cubic-certificates','appendix-finite-signings']:
    code='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',(snap/'sections'/f'{name}.tex').read_text(),re.S))
    capture=io.StringIO()
    with contextlib.redirect_stdout(capture): exec(compile(code,name,'exec'),{})
    result[name]=capture.getvalue().splitlines()
# Recreate the four point-packing constructions, including all repeated-index RLT constraints.
packing=0
for n in range(2,25):
 for sym in [False, True]:
  if sym and n<5: continue
  k=(n+3)//4 if sym else n
  nx=(n+1)//2
  lo=[[F(1,2) if sym and i<(nx if c==0 else k) else F(0) for i in range(n)] for c in range(2)]
  means=[[(l+1)/2 for l in ls] for ls in lo]
  for sdp in [False,True]:
   moments=[]
   for c in range(2):
    ls=lo[c]; mu=means[c]; M=[]
    for i in range(n):
     row=[]
     for j in range(n):
      if not sdp:
       v=(ls[i]+1)*mu[i]-ls[i] if i==j else max(ls[i]*mu[j]+ls[j]*mu[i]-ls[i]*ls[j],mu[i]+mu[j]-1)
      else:
       cov=(1-ls[i])**2/4 if i==j else (-F(1,16*(k-1)) if sym and i<k and j<k else (-F(1,4*(n-1)) if not sym else F(0)))
       v=mu[i]*mu[j]+cov
      assert v>=ls[i]*mu[j]+ls[j]*mu[i]-ls[i]*ls[j]
      assert v>=mu[i]+mu[j]-1
      assert v<=mu[j]+ls[j]*mu[i]-ls[j]
      assert v<=ls[i]*mu[j]+mu[i]-ls[i]
      row.append(v)
     M.append(row)
    moments.append(M)
   distance=min(sum(M[i][i]-2*M[i][j]+M[j][j] for M in moments) for i in range(n) for j in range(i+1,n))
   target=(F(k,4*(k-1)) if sym else F(n,n-1)) if sdp else (F(1,2) if sym else F(2))
   assert distance==target,(n,sym,sdp,distance,target)
   packing+=1
result['packing_exact_cases']=packing
# Rational grid generators: round and repair explicitly, then test actual distance,
# exposure, and the sharper generator inequality. This is finite falsification only.
count=0
for m in [1,2]:
 vectors=list(product([F(0),F(1,2),F(1)],repeat=2*m))
 for r in vectors:
  S=sum(r)
  if not S: continue
  for c in vectors:
   if sum(c)!=S: continue
   W=[[a*b/S for b in c] for a in r]
   D=1-sum(W[i][i] for i in range(2*m));B=sum(W[i][m+i] for i in range(m))
   g=m-S+(2*m+1)*B+(4*m+1)*D
   assert g>=B+D>=0
   b=[int(a>=F(1,2)) for a in r]
   for i in range(m):
    if b[i]==b[m+i]: b[m+i]=1-b[i]
   distance=sum(abs(W[i][j]-F(b[i]*b[j],m)) for i in range(2*m) for j in range(2*m))
   assert distance<=4*S*B+58*S*D+5*abs(S-m)
   assert distance<=(136*m+10)*g
   count+=1
result['rank_one_grid_generators']=count
tex=(snap/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in (snap/'sections').glob('*.tex'))
labels=set(re.findall(r'\\label\{([^}]+)\}',tex))
ledger=(snap/'process/claim-coverage.md').read_text()
ledger_labels=set(re.findall(r'`((?:thm|lem|prop|cor|eq|app|sec|tab):[^` ]+)`',ledger))
missing=sorted(ledger_labels-labels)
assert not missing,missing
result['coverage_labels_checked']=len(ledger_labels)
result['limits']=['Packing PSD feasibility follows analytically from the displayed projection/diagonal covariance blocks; no numerical eigenvalue claim.', 'Rational rank-one grid checks are finite, not universal proofs.', 'Displayed finite certificates were independently executed, not independently rediscovered.', 'Label resolution checks do not establish semantic coverage.']
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
