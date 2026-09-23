"""Exact finite checks of general-radix cutoff profiles and objective equality."""
from fractions import Fraction as Q
from pathlib import Path
import json
cases=[]
for b in range(2,10):
 for L in range(2,17):
  w=[Q(b-1,b**(l+1)) for l in range(L)]+[Q(1,b**L)]
  M=lambda q:Q((L-q)*(b-1)+b,b**q)
  cutoff=next(s for s in range(1,L) if M(s+1)<=1<=M(s))
  assert sum(w)==1
  profiles=[]
  for q in (cutoff,cutoff+1):
   R=[b**(l-q+1) if l>=q else 0 for l in range(L+1)]
   assert sum(t*r for t,r in zip(w,R))==M(q)
   for l,r in enumerate(R):
    actual=sum(min(b**j,r) for j in range(1,l+1))
    bound=cutoff*r+sum(b**j for j in range(1,l-cutoff+1))
    assert actual==bound
   profiles.append(sum(w[l]*sum(min(b**j,R[l]) for j in range(1,l+1)) for l in range(L+1)))
  p=(1-M(cutoff+1))/(M(cutoff)-M(cutoff+1))
  exact=cutoff+Q(L-cutoff,b**cutoff)
  assert p*profiles[0]+(1-p)*profiles[1]==exact
  assert sum(M(q) for q in range(cutoff+1,L+1))==Q(L-cutoff,b**cutoff)
  if b>=L:assert exact==1+Q(L-1,b)
  cases.append({'radix':b,'levels':L,'cutoff':cutoff,'hull_gap':str(exact)})
out={'status':'PASS','cases':len(cases),'checks':cases,'scope':'Exact finite profile checks; general digit-reversal attainment requires the analytic proof.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
