"""Independent symbolic identities and direct rational all-light constructions."""
import sympy as s
from fractions import Fraction as F
from pathlib import Path
from random import Random
import json
n,k,c,x,j=s.symbols('n k c x j',positive=True)
f=((n-1)**2*c+1)/(n*(n-1)*(1+c))
C=(n*(n-1)+(n-k)*(n-k-1))/(n*k*(2*n-k-1))
assert s.factor(f-1/n)==s.factor((n-2)*((n-1)*c-1)/(n*(n-1)*(1+c)))
assert s.factor((n*f-1)/(n*f+1)-(n-2)/n*((n-1)*c-1)/((n-1)*c+1))==0
assert s.factor(C-1/(k+1)-2*(n-k-1)*(n-k*(k+1)/2)/(n*k*(k+1)*(2*n-k-1)))==0
assert s.factor(1/k-C-(k+1)*(n-k)/(n*k*(2*n-k-1)))==0
assert s.factor(s.diff(f,c)-(n-2)/((n-1)*(1+c)**2))==0
oldseries=s.series(C.subs(n,1/x),x,0,3).removeO().expand()
assert s.simplify(oldseries-(1/k-(k+1)*x/(2*k)+(k*k-1)*x*x/(4*k)))==0
L=1/(n*((n/(n-1))**k-1))
lowseries=s.series(L.subs(n,1/x),x,0,3).removeO().expand()
assert s.simplify(lowseries-(1/k-(k+1)*x/(2*k)+(k*k-1)*x*x/(12*k)))==0
for ell in range(1,5):
 m=n-k+ell
 theta=m*(m-1)/(n*(n-1))*(2*((m-1)/m)**ell-1)
 seeded=(1+theta)/(n*(1-theta))
 series=s.series(seeded.subs(n,1/x),x,0,3).removeO()
 expected=1/k-(k+1)*x/(2*k)+(3*k**3-3*k-2*ell**3+2*ell)*x*x/(12*k*k)
 assert s.simplify(series-expected)==0
assert s.factor(C.subs(k,4)-L.subs(k,4)-(10*n*n-5*n+1)/(2*(2*n-5)*(2*n-1)*(2*n*n-2*n+1)))==0
U=(n**4-7*n**3+21*n*n-29*n+15)/(n*(2*n-3)*(2*n*n-6*n+5))
assert s.factor(f.subs(c,L.subs({n:n-1,k:3},simultaneous=True))-U)==0
assert s.factor(U-L.subs(k,4)-(6*n**4-20*n**3+21*n*n-7*n+1)/((2*n-3)*(2*n-1)*(2*n*n-6*n+5)*(2*n*n-2*n+1)))==0
assert s.factor((n-j)*j*(n-j+1)/(n-j)-(n-j+1)*(j-1)*(n-j+2)/(n-j+1)-(n-2*j+2))==0
# General exclusion aggregate: use Bprev=n*(E+Bolder)/(n-1).
e,b=s.symbols('e b');bp=n*(e+b)/(n-1)
aggregate=(n-k+1-(k-1)/(n-2))*bp+((k-1)*n*e+(k-1)*n*b)/(n-2)
assert s.factor(aggregate-n*bp)==0

rng=Random(15016);cases=bandcases=0
for N in range(2,19):
 for trial in range(4):
  nums=[rng.randrange(12) for _ in range(N)];nums[0]+=1
  cols=[[F(nums[(i+t)%N],sum(nums)) for i in range(N)] for t in range(N)]
  prefix=[[F(0)]*N]
  for col in cols:prefix.append([a+b for a,b in zip(prefix[-1],col)])
  assert prefix[-1]==[F(1)]*N
  def A(t):
   cell=min(int(t),N-1)
   return [prefix[cell][i]+(t-cell)*cols[cell][i] for i in range(N)]
  for K in range(1,N):
   prev=F(0);blocks=[];unused=set(range(N))
   for J in range(1,K+1):
    t=min(F(N),F(J*(N-J+1),N-J))
    alloc=A(t);i=max(unused,key=lambda p:alloc[p]);unused.remove(i)
    blocks.append((prev,t,i));prev=t
    if t==N:break
   times=sorted({F(0),prev}|{F(t) for t in range(N+1) if t<=prev}|{t for a,t,i in blocks})
   error=F(0)
   for t in times:
    W=[F(0)]*N
    for left,right,i in blocks:W[i]+=max(F(0),min(t,right)-left)
    error=max(error,max(abs(a-w) for a,w in zip(A(t),W)))
   assert error<=1
   if (N-K)**2<=K:
    assert prev==N and error==1
    bandcases+=1
   cases+=1
out={'symbolic_transfer_plateau_seed_asymptotic_exclusion_identities':'passed','all_light_rational_profiles_and_budgets':cases,'equal_mass_exact_instance_band_cases':bandcases}
Path(__file__).with_name('formulas-light-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
