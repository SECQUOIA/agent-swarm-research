"""Independent review02 checks; exact except labeled numerical harmonic probes.
No author/repository checker is imported. Run with the minlp-notes environment.
"""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb, log
from pathlib import Path
import hashlib, json
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq

out={}
a,b,c,t,m=s.symbols('a b c t m')
F=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a*a
ell=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
p=s.expand((F-ell).subs({a:1,b:s.Rational(13,24)-3*c*c/4}))
station=s.solve([s.diff(F-ell,a),s.diff(F-ell,b)],[a,b])
r=s.expand((F-ell).subs(station))
rows=[(p,0,s.Rational(1,5),60000,[63125,39125,20975,9395,4133]),(p,s.Rational(1,5),s.Rational(3,10),240000,[16532,6008,1802,3788,11597]),(r,s.Rational(3,10),s.Rational(1,2),7440000,[215357,1285415,1434125,1250375,1008125]),(r,s.Rational(1,2),s.Rational(3,4),190464,[25808,18056,7964,9230,15869]),(r,s.Rational(3,4),1,190464,[15869,22508,34520,45920,31040])]
for f,l,u,D,nums in rows:
 assert s.expand(f.subs(c,l+(u-l)*t)-sum(s.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(nums)))==0
slack=min(Q(v,D) for _,_,_,D,nums in rows for v in nums)
assert slack==Q(901,120000)
assert Q(161,4)/(Q(223,12)-slack)==Q(1610000,743033)
assert s.expand(a*c*c+s.Rational(5,4)*a*a-(s.Rational(11,6)*a+s.Rational(20,27)*c-s.Rational(95,108))-s.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert s.expand(a*c*c+s.Rational(24,25)*a*a-(s.Rational(41,25)*a+s.Rational(4,5)*c-s.Rational(68,75))-s.Rational(24,25)*(a-(41-25*c*c)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480)==0
out['symbolic_cubic']={'bernstein_identities':5,'minimum_coefficient':str(slack),'limiting_bound':str(Q(1610000,743033)),'two_level_identities':2}

cases=[(6,[2,3,9,10,7,7],13,[962,778,842,-4816],[(1,4,4),(2,1,6),(6,2,1)],[Q(17,26),Q(4,13),Q(1,26)]),(8,[2,3,13,12,8,7],7,[793,770,798,-5882],[(1,2,8),(1,5,6),(8,4,2)],[Q(2,7),Q(4,7),Q(1,7)]),(64,[2,3,120,105,70,63],105,[871710,900446,899046,-51743768],[(4,19,64),(5,19,64),(16,40,43),(64,31,17)],[Q(241,735),Q(12,735),Q(419,735),Q(63,735)])]
out['finite_cubic']=[]
for n,co,D,du,states,weights in cases:
 def value(A,B,C): return sum(x*y for x,y in zip(co,[comb(C,3),B*comb(C,2),comb(B,2),A*C,A*B,comb(A,2)]))
 residuals=[D*value(A,B,C)-sum(x*y for x,y in zip(du,[A,B,C,1])) for A,B,C in product(range(n+1),repeat=3)]
 assert min(residuals)==0 and sum(weights)==1
 means=[sum(w*state[i] for state,w in zip(states,weights)) for i in range(3)]
 assert means==[Q(n,4),Q(n,2),Q(3*n,4)]
 v=sum(w*value(*state) for state,w in zip(states,weights));assert v==sum(Q(x,D)*y for x,y in zip(du,means+[1]))
 sizes=[comb(n,3),n*comb(n,2),comb(n,2),n*n,n*n,comb(n,2)]
 upper=sum(co[i]*sizes[i]*[Q(3,4),Q(1,2),Q(1,2),Q(1,4),Q(1,4),Q(1,4)][i] for i in range(6))
 lower=Q(co[0]*sizes[0],4)
 out['finite_cubic'].append({'m':n,'states':len(residuals),'vex':str(v),'cav':str(upper),'term_lower':str(lower),'ratio':str((upper-lower)/(upper-v))})
assert [v['ratio'] for v in out['finite_cubic']]==['20891/10411','6601/3225','7443345/3445256']
out['two_level_finite']=[]
for n,du in [(4,(9,4,-19)),(8,(47,20,-188)),(12,(Q(231,2),48,-684)),(16,(214,Q(177,2),-1686))]:
 def value(A,C): return A*comb(C,2)+Q(5*n,4)*comb(A,2)
 assert min(value(A,C)-du[0]*A-du[1]*C-du[2] for A,C in product(range(n+1),repeat=2))==0
 v=value(n//2,3*n//4);assert v==du[0]*(n//2)+du[1]*(3*n//4)+du[2]
 upper=Q(9*n,8)*comb(n,2)
 out['two_level_finite'].append({'m':n,'vex':str(v),'ratio':str(upper/(upper-v))})
assert Q(943,1)/(Q(3225,7)+Q(46,25))==Q(165025,80947)
assert Q(2160,1)/(1072+Q(12,5))==Q(2700,1343)

# Integrate the actual three laws exactly at sorted rational means, including boundaries.
def orient(x):
 result=Q(0)
 for bits in product([0,1],repeat=len(x)):
  endpoints=sorted({Q(0),Q(1),*x,*[1-y for y in x]})
  for l,u in zip(endpoints,endpoints[1:]):
   U=(l+u)/2; vals=[int(U<y) if z==0 else int(U>1-y) for y,z in zip(x,bits)]
   result+=(u-l)*(vals[0]-int(all(vals)))/2**len(x)
 return result
def blaw(x):
 points=sorted({Q(0),Q(1),*[y for y in x if y<=Q(1,2)],*[2*(1-y) for y in x if y>Q(1,2)]})
 result=Q(0)
 for l,u in zip(points,points[1:]):
  U=(l+u)/2;probs=[Q(int(U<y)) if y<=Q(1,2) else (Q(1,2) if U<2*(1-y) else Q(1)) for y in x]
  prod=Q(1)
  for y in probs:prod*=y
  result+=(u-l)*(probs[0]-prod)
 return result
count=0
for deg in [2,3]:
 for vals in combinations_with_replacement(range(21),deg):
  x=[Q(i,20) for i in vals];gap=min(x[0],sum(1-v for v in x[1:]));prod=Q(1)
  for y in x:prod*=y
  assert 18*orient(x)+6*(x[0]-prod)+7*blaw(x)>=12*gap
  count+=1
out['exact_three_law_grid']={'vectors':count,'denominator':20,'scope':'finite falsification test; not universal proof'}

# Exact radix resource profiles: means, active lines, and supporting intercepts.
rcount=0
for radix in range(2,8):
 for L in range(2,10):
  cap=lambda q:Q((L-q)*(radix-1)+radix,radix**q)
  cut=next(q for q in range(1,L) if cap(q+1)<=1<=cap(q))
  weights=[Q(radix-1,radix**(j+1)) if j<L else Q(1,radix**L) for j in range(L+1)]
  exp=[]
  for q in [cut,cut+1]:
   R=[radix**(j-q+1) if j>=q else 0 for j in range(L+1)]
   assert sum(w*r for w,r in zip(weights,R))==cap(q)
   for j,r in enumerate(R):assert sum(min(radix**h,r) for h in range(1,j+1))==cut*r+sum(radix**h for h in range(1,j-cut+1))
  assert sum(weights[j]*sum(radix**h for h in range(1,j-cut+1)) for j in range(L+1))==Q(L-cut,radix**cut)
  rcount+=1
out['exact_radix_profiles']={'parameter_pairs':rcount}

# Numerical probes of finite Lambert certificate, retaining the applicability condition.
num=[]
for deg in [2,3,10,1000,10**6,10**12]:
 N=1+log(deg-1)
 for M in [deg-1,(deg-1)*N,10*(deg-1)]:
  Lam=1+log(M);eta=(deg-1)/M
  fun=lambda z:quad(lambda v:-__import__('math').expm1(-(1/v-eta)/Lam),z,1,epsabs=1e-11)[0]
  z=brentq(lambda z:fun(z)-z,1e-10,1-1e-10)
  w=brentq(lambda w:w+log(w)-log(Lam)+eta,1e-10,Lam+1)
  lower=(w-1/(2*w))/Lam if w>=1 else None
  if lower is not None: assert lower<=z+1e-10
  num.append({'d':deg,'M':M,'root':z,'Lambert_lower':lower})
out['numerical_harmonic']=num

root=Path(__file__).resolve().parents[3]/'process/snapshots/stage06-round01'
out['frozen_pdf_sha256']=hashlib.sha256((root/'main.pdf').read_bytes()).hexdigest()
out['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='numerical_harmonic'},indent=2))
