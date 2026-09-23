"""Independent exact moment feasibility and distances. PSD is analytic, not numerically certified."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from pathlib import Path
import json, hashlib, subprocess
checks=0
cases=[]
for n in list(range(2,34))+[40,51,64,81,100]:
 for sym in (False,True):
  if sym and n<5: continue
  nx=(n+1)//2;k=(n+3)//4
  for sdp in (False,True):
   M=[]
   for coord in range(2):
    lows=[Q(1,2) if sym and i<(nx if coord==0 else k) else Q(0) for i in range(n)]
    means=[(a+1)/2 for a in lows]
    z=[]
    for i in range(n):
     row=[]
     for j in range(n):
      if not sdp:
       v=(lows[i]+1)*means[i]-lows[i] if i==j else max(lows[i]*means[j]+lows[j]*means[i]-lows[i]*lows[j],means[i]+means[j]-1)
      else:
       if not sym: cov=Q(1,4) if i==j else -Q(1,4*(n-1))
       elif i<k and j<k: cov=Q(1,16) if i==j else -Q(1,16*(k-1))
       elif i==j: cov=(1-lows[i])**2/4
       else: cov=Q(0)
       v=means[i]*means[j]+cov
      row.append(v)
     z.append(row)
    for i,j in combinations_with_replacement(range(n),2):
     a,b=lows[i],lows[j];u,v=means[i],means[j];w=z[i][j]
     slacks=(w-a*v-b*u+a*b,u-w-a+a*v,v-w-b+b*u,1-u-v+w)
     assert min(slacks)>=0,(n,sym,sdp,coord,i,j,slacks)
     checks+=4
    for i in range(n): assert z[i][i]==(lows[i]+1)*means[i]-lows[i]
    M.append(z)
   distances=[sum(z[i][i]+z[j][j]-2*z[i][j] for z in M) for i in range(n) for j in range(i+1,n)]
   expected=Q(k,4*(k-1)) if sym and sdp else Q(1,2) if sym else Q(n,n-1) if sdp else Q(2)
   assert min(distances)==expected,(n,sym,sdp,min(distances),expected)
   cases.append({'n':n,'sym':sym,'sdp':sdp,'minimum_distance':str(expected)})
# Execute the two frozen printed finite proof programs without modifying their files.
snapshot=Path('paper-relaxation-limits/process/snapshots/stage06-round01')
import re
finite=[]
for name in ('appendix-finite-signings.tex','appendix-cubic-certificates.tex'):
 text=(snapshot/'sections'/name).read_text()
 code='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',text,re.S))
 result=subprocess.run(['python','-c',code],text=True,capture_output=True,check=True)
 finite.append({'file':name,'stdout':result.stdout})
result={'exact_rlt_inequalities':checks,'constructions':len(cases),'n_values':sorted(set(c['n'] for c in cases)),'cases':cases,'finite_programs':finite,'scope':'Exact rational pair inequalities, diagonal secants and distances. PSD relies separately on positive projection/diagonal blocks; no numerical eigenvalue test used. Finite cases do not prove all n.','pdf_sha256':hashlib.sha256((snapshot/'main.pdf').read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
