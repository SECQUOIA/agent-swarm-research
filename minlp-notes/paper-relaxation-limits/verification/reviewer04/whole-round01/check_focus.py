from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
import json, pathlib, re, contextlib, io
out=pathlib.Path(__file__).parent
frozen=pathlib.Path('process/snapshots/whole-round01')
def fall(t,k):
    a=Q(1)
    for i in range(k): a*=t-i
    return a
def mom(s,t,k):return fall(t,k)/fall(s,k)
counts={'gram_entries':0,'cardinality_identities':0,'indicator_identities':0,'conditioned_parameters':0}
for r in range(1,4):
 for s in range(max(2*r,4*r-2),13):
  for ti in range(2*(2*r-1),2*(s-2*r+1)+1):
   t=Q(ti,2)
   for d in range(1,r+1):
    co=[fall(t,2*d-j)*fall(s-t,j)/fall(s,2*d) for j in range(d+1)]
    assert min(co)>=0
    for ell in range(d+1):
     assert mom(s,t,2*d-ell)==sum(comb(ell,j)*co[j] for j in range(ell+1))
     counts['gram_entries']+=1
   for k in range(2*r):
    assert k*mom(s,t,k)+(s-k)*mom(s,t,k+1)==t*mom(s,t,k)
    counts['cardinality_identities']+=1
   for a in range(2*r+1):
    for b in range(2*r-a+1):
     weight=fall(t,a)*fall(s-t,b)/fall(s,a+b)
     assert weight>=0
     for c in range(min(s-a-b,2*r-a-b)+1):
      direct=sum((-1)**j*comb(b,j)*mom(s,t,a+c+j) for j in range(b+1))
      assert direct==fall(t,a+c)*fall(s-t,b)/fall(s,a+b+c)
      if a+b<s:
       assert direct==weight*mom(s-a-b,t-a,c)
      counts['indicator_identities']+=1
     for d in range(1,(2*r-a-b)//2+1):
      assert s-a-b>=2*d and t-a>=2*d-1 and s-t-b>=2*d-1
      counts['conditioned_parameters']+=1
# All-slack obstruction, even though a weaker moment range can hold.
assert mom(6,Q(5,2),4)<0
# Exact tensor-localizer matrix and PSD via a rational elimination.
def psd(M):
 M=[row[:] for row in M]
 while M:
  if M[0][0]<0:return False
  if M[0][0]==0:
   assert all(v==0 for v in M[0]);M=[row[1:] for row in M[1:]];continue
  d=M[0][0];v=M[0][1:]
  M=[[M[i+1][j+1]-v[i]*v[j]/d for j in range(len(v))]for i in range(len(v))]
 return True
# Two seven-variable blocks at fractional total 7/2; g=u_0(1-u_7).
# Both blocks satisfy t,s-t >= 2r-1, including full-preordering feasibility.
s=7;t=Q(7,2);r=2
assert min(t,s-t)>=2*r-1
basis=[frozenset()]+[frozenset([i]) for i in range(2*s)]
def E(S):return mom(s,t,len(S&set(range(s))))*mom(s,t,len(S&set(range(s,2*s))))
M=[[E(A|B|{0})-E(A|B|{0,s}) for B in basis]for A in basis]
assert psd(M)
counts['global_tensor_matrix_order']=len(M)
# Endpoint graph substitution for a polynomial penalty and high-degree auxiliary.
# Every Boolean assignment evaluates actual endpoint tuples, no degree explosion.
for w in product([Q(0),Q(1)],repeat=4):
 y=[v*(1-v) for v in w];z=[v**17+2*v for v in w]
 assert sum(y)==sum(v*(1-v) for v in w)
 assert all(y[i]==0 and z[i]==3*w[i] for i in range(4))
counts['graph_endpoint_assignments']=16
# Re-execute the exact code printed in the frozen manuscript, not its result logs.
for source in ['appendix-finite-signings.tex','appendix-cubic-certificates.tex']:
 body=(frozen/'sections'/source).read_text()
 code='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',body,re.S))
 stdout=io.StringIO()
 with contextlib.redirect_stdout(stdout):exec(compile(code,source,'exec'),{})
 (out/(source+'.replay.txt')).write_text(stdout.getvalue())
counts['printed_integer_checkers_executed']=2
(out/'checks.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
