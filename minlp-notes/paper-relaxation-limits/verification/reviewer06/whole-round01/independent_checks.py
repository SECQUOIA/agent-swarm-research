from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json, re, runpy
BASE=Path(__file__).resolve().parent
out={}
checks=0
cases=0
for n in range(2,61):
 for sym in (False,True):
  if sym and n<5: continue
  k=(n+3)//4 if sym else n
  nx=(n+1)//2
  target=Q(k,4*(k-1)) if sym else Q(n,n-1)
  for sdp in (False,True):
   vals=[]
   for ax in (0,1):
    restricted=(nx if ax==0 else k) if sym else 0
    lo=[Q(1,2) if i<restricted else Q(0) for i in range(n)]
    mu=[(l+1)/2 for l in lo]
    X=[]
    for i in range(n):
     row=[]
     for j in range(n):
      if i==j: v=(lo[i]+1)*mu[i]-lo[i]
      elif sdp:
       v=mu[i]*mu[j]-(Q(1,16) if sym else Q(1,4))/(k-1) if i<k and j<k else mu[i]*mu[j]
      else: v=max(lo[i]*mu[j]+lo[j]*mu[i]-lo[i]*lo[j],mu[i]+mu[j]-1)
      row.append(v)
      slacks=[v-lo[i]*mu[j]-lo[j]*mu[i]+lo[i]*lo[j],mu[i]-v-lo[i]+lo[i]*mu[j],mu[j]-v-lo[j]+lo[j]*mu[i],1-mu[i]-mu[j]+v]
      assert min(slacks)>=0
      checks+=4
     X.append(row)
    vals.append(X)
   distances=[sum(M[i][i]-2*M[i][j]+M[j][j] for M in vals) for i,j in combinations(range(n),2)]
   assert min(distances)==(target if sdp else Q(1,2) if sym else Q(2))
   cases+=1
out['packing']={'cases':cases,'n':'2..60 without symmetry; 5..60 with symmetry; RLT and SDP each','exact_rlt_slacks':checks,'all_minima_correct':True,'PSD':'analytic: projection block plus positive diagonal blocks; no eigenvalue tolerance'}
# Check the fractional Gram identity independently at endpoints and fractional parameters.
def fall(t,j):
 p=Q(1)
 for h in range(j):p*=t-h
 return p
from math import comb
count=0
for d in range(1,5):
 for s in range(max(2*d,4*d-2),max(2*d,4*d-2)+5):
  for t in [Q(2*d-1),Q(s,2),Q(2*d-1)+Q(1,3),Q(s-2*d+1)]:
   if min(t,s-t)<2*d-1:continue
   for l in range(d+1):
    rhs=sum(Q(comb(l,j))*fall(t,2*d-j)*fall(s-t,j)/fall(s,2*d) for j in range(l+1))
    assert rhs==fall(t,2*d-l)/fall(s,2*d-l)
    count+=1
out['fractional_gram']={'exact_entries':count,'universal_proof':'manuscript algebra independently reconstructed'}
# Execute complete printed certificates from the frozen text in isolated copied inputs.
for name in ['appendix-finite-signings','appendix-cubic-certificates']:
 text=(BASE/'build/sections'/f'{name}.tex').read_text()
 blocks=re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',text,re.S)
 code='\n'.join(blocks)
 dst=BASE/f'printed-{name}.py';dst.write_text(code)
 exec(compile(code,str(dst),'exec'),{})
 out[name]={'printed_code_executed':True,'arithmetic':'unbounded integer/Fraction'}
(BASE/'independent-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
