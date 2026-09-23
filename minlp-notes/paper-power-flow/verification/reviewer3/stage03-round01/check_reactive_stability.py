"""Independent numerical smoke checks against physical line injections.
The eigenvalue is the closed-form eigenvalue of a uniformly weighted path.
This is supplemental finite evidence, not a proof or exact certificate.
"""
import math
import random
rng = random.Random(37)
cases=0
for n in range(2, 22):
 for g in (0.5, 1, 2):
  lam=4*g*math.sin(math.pi/(2*n))**2
  assert lam + 1e-12 >= 2*g/(n-1)**2
  for amplitude in (1.0, 1e-5, 0.0):
   theta=[amplitude*rng.uniform(-math.pi/4,math.pi/4) for _ in range(n)]
   if n==2 and amplitude==1.0:
    theta=[-math.pi/4,math.pi/4]
   mean=sum(theta)/n
   theta=[t-mean for t in theta]
   v=[rng.uniform(0.5,4) for _ in range(n)]
   q=[0.0]*n
   correction=[0.0]*n
   for i in range(n-1):
    delta=theta[i]-theta[i+1]
    flow=-g*v[i]*v[i+1]*math.sin(delta)
    q[i]+=flow
    q[i+1]-=flow
    corr=2*g*v[i]*v[i+1]*math.sin(delta/2)**2
    correction[i]+=corr
    correction[i+1]+=corr
   q2=sum(x*x for x in q)
   norm=math.sqrt(sum(t*t for t in theta))
   assert norm <= math.pi*math.sqrt(q2)/(2*0.5**2*lam)+1e-12
   bound=math.pi**2*4**2*q2/(8*0.5**4*lam)
   assert max(correction) <= bound+1e-12
   cases+=1
print(f'PASS: {cases} path profiles, including zero and small angles and the pi/2 line boundary.')
