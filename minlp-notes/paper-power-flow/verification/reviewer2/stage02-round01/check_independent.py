"""Independent symbolic and 80-digit analytic checks, without importing author code."""
from fractions import Fraction as F
from itertools import product
import mpmath as mp
import sympy as s
mp.mp.dps=80
# Expand U_i conjugate(I_i) with unrestricted real symbols.
e,f,a,b,g,B,h,t=s.symbols('e f a b g B h t',real=True)
U=e+s.I*f; V=a+s.I*b
power=s.expand(U*s.conjugate((h+s.I*t)*U+(g+s.I*B)*(U-V)))
H=e*a+f*b; D=f*a-e*b; R=e*e+f*f
assert s.expand(s.re(power)-(h*R+g*(R-H)-B*D))==0
assert s.expand(s.im(power)-(-t*R-B*(R-H)-g*D))==0
print('PASS exact symbolic P/Q expansion, including both shunt terms.')
# Distinct rational unit directions with denominator variation, both axes included.
rays={(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))}
for p in range(-13,14):
 for q in range(1,8):
  z=F(p,q); rays.add(((1-z*z)/(1+z*z),2*z/(1+z*z)))
rays=sorted(rays)
m=lambda x:mp.mpf(x.numerator)/x.denominator
alpha=[mp.atan2(m(y),m(x))%(2*mp.pi) for x,y in rays]
count=0; long=0; axes=0
for i,j in product(range(len(rays)),repeat=2):
 ei,fi=rays[i]; ej,fj=rays[j]
 D=fi*ej-ei*fj; H=ei*ej+fi*fj
 if D==0 and H<0: continue
 k=1 if fj<0<=fi and D>0 else -1 if fi<0<=fj and D<0 else 0
 delta=mp.atan2(m(D),m(H))
 assert abs(delta-(alpha[i]-alpha[j]+2*mp.pi*k))<mp.mpf('1e-75')
 count+=1; long+=H<0; axes+=fi==0 or fj==0
print(f'PASS 80-digit angle identity on {count} direction pairs ({long} obtuse, {axes} real-axis incident), from {len(rays)} exact rational directions.')
# Connected graph with two fundamental cycles; check analytic edge deltas
# against integer winding and direct tree propagation for random assignments.
import random
rng=random.Random(92026)
edges=[(0,1),(1,2),(2,3),(3,4),(0,2),(1,4)]
cycles=[[(0,1),(1,2),(2,0)],[(1,2),(2,3),(3,4),(4,1)]]
trials=0; liftable=0
for _ in range(3000):
 ids=[rng.randrange(len(rays)) for _ in range(5)]
 deltas={}; kval={}
 for i,j in edges:
  ei,fi=rays[ids[j]]; ej,fj=rays[ids[i]]
  D=fi*ej-ei*fj; H=ei*ej+fi*fj
  if D==0 and H<0: break
  delta=mp.atan2(m(D),m(H))
  k=1 if fj<0<=fi and D>0 else -1 if fi<0<=fj and D<0 else 0
  deltas[i,j]=delta; deltas[j,i]=-delta
  kval[i,j]=k; kval[j,i]=-k
 else:
  zero=all(sum(kval[e] for e in C)==0 for C in cycles)
  theta=[alpha[ids[0]]]
  for i in range(4): theta.append(theta[-1]+deltas[i,i+1])
  realized=all(abs(theta[j]-theta[i]-deltas[i,j])<mp.mpf('1e-74') for i,j in edges)
  assert realized==zero
  trials+=1; liftable+=realized
print(f'PASS fundamental-cycle criterion versus direct analytic tree lift on {trials} non-antipodal profiles ({liftable} liftable).')
print('Analytic finite checks use high precision and are supplementary, not formal certificates.')
