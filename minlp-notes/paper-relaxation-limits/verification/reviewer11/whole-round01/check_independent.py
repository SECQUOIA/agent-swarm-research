from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json,re,hashlib,subprocess
out={}
# All finite binary orderings of the two relevant primitive contractors.
trials=0
for n in range(1,5):
 b=Q(1,2**(2**n)); c=1-b
 states={(Q(0),Q(0),0)}
 for depth in range(13):
  nxt=set()
  for z,w,k in states:
   assert 0<=w<=c*z<=c
   assert z<=1-c**k<=k*b
   # Exact simultaneous interval-hull lower endpoints; upper z=1.
   zz,ww=max(z,w/c),max(w,c*z)
   assert ww<=c*zz
   nxt.add((zz,ww,k))
   zz,ww=max(z,b+w),max(w,z-b)
   assert ww<=c*zz
   nxt.add((zz,ww,k+1)); trials+=2
  states=nxt
out['primitive_schedule_transitions']=trials
# Detector and amplifier with every boundary c=0,1/2,1 included.
cases=0
for M in range(1,33):
 b=Q(1,16*M*M)
 for U,V in product(range(M+1),repeat=2):
  c=Q(1,2)+Q(U-V,2*M); d=1-c
  a=Q(1) if c<=Q(1,2) else d/c
  assert a==d+c*a*a
  z=b/(1-(1-b)*a)
  assert (z==1) if U<=V else (0<=z<=b*M<=Q(1,8))
  if U>V: assert 1-a>=Q(1,M)
  for root in ({Q(1)} if c==0 else {Q(1),d/c}):
   if 0<=root<=1: assert (c*root<=Q(1,2))==(root==a)
  cases+=1
out['rational_detector_cases']=cases
# Exact short Kleene runs, not a numerical asymptotic proof.
for n in range(1,5):
 x=[Q(0)]*(n+1)
 for k in range(9):
  err=[1-v for v in x]
  assert err[0]>=Q(1,k+1)
  assert all(err[i]**2>=err[i-1] for i in range(1,n+1))
  x=[(x[0]**2+1)/2]+[(x[i]**2+x[i-1])/2 for i in range(1,n+1)]
out['kleene_checks']='four chain lengths, nine exact iterates each'
# Execute the complete proof programs printed in the frozen manuscript.
for name in ['appendix-finite-signings','appendix-cubic-certificates']:
 s=(Path('build/sections')/(name+'.tex')).read_text()
 code='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',s,re.S))
 assert code.strip()
 cp=subprocess.run(['python','-c',code],text=True,capture_output=True,check=True)
 out[name]={'stdout':cp.stdout,'printed_code_sha256':hashlib.sha256(code.encode()).hexdigest()}
Path('independent-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
