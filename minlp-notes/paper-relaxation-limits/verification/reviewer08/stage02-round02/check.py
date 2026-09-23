from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, log, exp
import json, re, subprocess, sys
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import lambertw
ROOT=Path(__file__).resolve().parents[3]
SNAP=ROOT/'process/snapshots/stage02-round02'
OUT=Path(__file__).resolve().parent
report={}
# Replay exactly the frozen printed certificates, including both blocks.
tex=(SNAP/'sections/appendix-cubic-certificates.tex').read_text()
blocks=re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}',tex,re.S)
assert len(blocks)==2
printed=''.join(blocks)
assert printed==(SNAP/'verification/check_stage02_finite.py').read_text()
(OUT/'printed.py').write_text(printed)
r=subprocess.run([sys.executable,str(OUT/'printed.py')],text=True,capture_output=True,check=True)
report['printed_replay']=r.stdout.splitlines()
# Independent exact dyadic resource profile check, including every cutoff tie.
ties=[]
for L in range(2,201):
 B=lambda q:Q(L-q+2,2**q)
 ss=[q for q in range(1,L) if B(q+1)<=1<=B(q)]
 vals=[]
 for cutoff in ss:
  theta=(1-B(cutoff+1))/(B(cutoff)-B(cutoff+1))
  ER=Q(0);obj=Q(0);means=[Q(0)]*L
  for ell in range(L+1):
   wt=Q(1,2**(ell+1 if ell<L else L))
   for q,prob in [(cutoff,theta),(cutoff+1,1-theta)]:
    R=0 if ell<q else 2**(ell-q+1)
    assert 0<=R<=2**L
    cap=0 if ell<=cutoff else 2**(ell-cutoff+1)-2
    payoff=sum(min(2**j,R) for j in range(1,ell+1))
    assert payoff==cutoff*R+cap
    ER+=wt*prob*R;obj+=wt*prob*payoff
    for j in range(ell):means[j]+=wt*prob
  assert ER==1 and means==[Q(1,2**j) for j in range(1,L+1)]
  assert obj==cutoff+Q(L-cutoff,2**cutoff)
  vals.append(obj)
 assert len(set(vals))==1
 if len(ss)>1:ties.append(L)
report['dyadic']={'L_range':[2,200],'tie_L':ties}
# Re-derive the quartics, then reconstruct all printed Bernstein rows.
a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h=F-ell
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c**2/4}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],[a,b])
r=s.expand(h.subs(stationary))
rows=[(p,0,s.Rational(1,5),60000,[63125,39125,20975,9395,4133]),(p,s.Rational(1,5),s.Rational(3,10),240000,[16532,6008,1802,3788,11597]),(r,s.Rational(3,10),s.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),(r,s.Rational(1,2),s.Rational(3,4),190464,[25808,18056,7964,9230,15869]),(r,s.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for poly,lo,hi,D,vs in rows:
 rhs=sum(s.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vs))
 assert s.expand(poly.subs(c,lo+(hi-lo)*t)-rhs)==0
slack=min(s.Rational(v,D) for _,_,_,D,vs in rows for v in vs)
assert slack==s.Rational(901,120000)
assert s.Rational(161,4)/(s.Rational(223,12)-slack)==s.Rational(1610000,743033)
for k,ell2,rhs in [(s.Rational(5,4),11*a/6+20*c/27-s.Rational(95,108),s.Rational(5,4)*(a-(11-6*c**2)/15)**2+(1-c)*(3*c-2)**2*(3*c+7)/135),(s.Rational(24,25),41*a/25+4*c/5-s.Rational(68,75),s.Rational(24,25)*(a-(41-25*c**2)/48)**2+(1-c)*(5*c-3)**2*(5*c+11)/480)]:
 assert s.expand(a*c**2+k*a**2-ell2-rhs)==0
report['symbolic']={'bernstein_slack':str(slack),'limiting_lower':'1610000/743033','two_level_identities':2}
# Integrate actual O and B laws directly at a rational grid, not their deficiency formulas.
def actual_O(xs):
 out=Q(0)
 for orient in product([0,1],repeat=len(xs)):
  lo=max([Q(0)]+[1-x for x,o in zip(xs,orient) if o])
  hi=min([Q(1)]+[x for x,o in zip(xs,orient) if not o])
  out+=max(Q(0),hi-lo)/2**len(xs)
 return out
def actual_B(xs):
 endpoints=sorted(set([Q(0),Q(1)]+[x if x<=Q(1,2) else 2*(1-x) for x in xs]))
 out=Q(0)
 for lo,hi in zip(endpoints,endpoints[1:]):
  t=(lo+hi)/2;p=Q(1)
  for x in xs:p*=int(t<=x) if x<=Q(1,2) else (Q(1,2) if t<=2*(1-x) else 1)
  out+=(hi-lo)*p
 return out
count=0
for degree in [2,3]:
 for xs in combinations_with_replacement([Q(i,16) for i in range(17)],degree):
  u=min(xs);term=min(u,sum(1-x for x in xs)-1+u)
  # Equivalent term expression removes anchor failure.
  assert term==u-max(Q(0),sum(xs)-degree+1)
  ip=Q(1)
  for x in xs:ip*=x
  expectation=(18*actual_O(xs)+6*ip+7*actual_B(xs))/31
  assert u-expectation>=Q(12,31)*term
  count+=1
report['rational_actual_couplings']={'tuples':count,'denominator':16}
# Equal-mean finite formula: positivity, upper bound and optimizer comparisons.
count=0
for n in range(2,33):
 for ud in range(2,14):
  for un in range(1,ud):
   u=Q(un,ud);b=(n*u).__floor__();theta=n*u-b
   rr=u/(1-u);ks={max(1,rr.__floor__()),max(1,rr.__ceil__())}
   candidate=lambda k:min(Q(1),k*(1-u)/u)/(1-u**k)
   best=max(candidate(k) for k in ks)
   assert best==max(candidate(k) for k in range(1,30)) and best<=2
   for d in range(2,n+1):
    q=((1-theta)*comb(b,d)+theta*comb(b+1,d))/comb(n,d)
    assert 0<=q<=u**d<u
    assert min(u,(d-1)*(1-u))/(u-q)<=best
    count+=1
report['equal_means_rational_cases']=count
# Numerical supplementary checks of integral endpoint/root and finite Lambert bound.
cases=[]
for d in [2,3,16,1000,1000000]:
 for multiplier in [1,1.5,1+log(d-1),10]:
  M=(d-1)*multiplier;Lam=1+log(M);eta=(d-1)/M
  F=lambda v:1 if v==0 else -__import__('math').expm1(-(1-eta*v)/(Lam*v))
  J=lambda z:quad(F,z,1,epsabs=1e-12,epsrel=1e-12)[0]
  z=brentq(lambda z:J(z)-z,0,1,xtol=1e-14)
  assert 0<z<1 and abs(J(z)-z)<1e-10
  w=float(lambertw(Lam*exp(-eta)).real)
  if w>=1:assert z>=(w-1/(2*w))/Lam-1e-10
  cases.append([d,M,Lam,eta,z,w])
report['harmonic_numerical_cases']=cases
(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='harmonic_numerical_cases'},indent=2))
print('All checks passed; harmonic numerical cases:',len(cases))
