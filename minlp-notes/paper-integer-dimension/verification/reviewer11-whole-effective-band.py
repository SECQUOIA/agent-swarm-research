"""Exact arithmetic checks of the effective-image band with ill-scaled coordinates.
This tests the set-containment certificate, not a general GLS implementation.
"""
from itertools import product
import random
import sympy as s
Q=s.Rational
rng=random.Random(110401)
cases=0
for r in range(1,5):
 for bits in (0,1,8,31,80):
  A=s.eye(r)
  for i in range(r):
   A[i,i]=Q(2)**(bits if i%2 else -bits)
   for j in range(i+1,r): A[i,j]=Q(rng.randrange(-3,4),7)
  Ai=A.inv(); B=A/3; Bi=B.inv()
  # First r ambient box constraints make C exactly A[-1,1]^r.
  scales=[Q(2)**(bits*(i-1)) for i in range(r)]
  V=s.diag(*scales)*Ai
  widths=scales[:]
  for k in range(2):
   row=s.Matrix([[Q(rng.randrange(-5,6),11) for _ in range(r)]])
   V=V.col_join(row*Ai)
   widths.append(1+sum(abs(x) for x in row))
  J=(V.T*V).inv()*V.T
  assert J*V==s.eye(r)
  LB=1+sum(abs(x) for x in Bi)
  delta=1/(16*r*LB)
  def gauge_P(z): return r*max(abs(x) for x in Bi*z)
  def gauge_K(e): return max(abs(e[i])/widths[i] for i in range(r+2))
  for signs in product((-1,1), repeat=r):
   t=s.Matrix(signs)
   gap=Q(13,192*r)*A*t
   assert gauge_K(V*gap)<=Q(13,192*r)
   assert gauge_P(gap)<=Q(13,64)
   for theta in (Q(0),Q(1,7),Q(1,2),Q(1)):
    r0=s.Matrix([delta*rng.choice((-1,0,1)) for _ in range(r)])
    r1=s.Matrix([delta*rng.choice((-1,0,1)) for _ in range(r)])
    err=(1-theta)*r0+theta*r1
    assert gauge_P(err)<=Q(1,16)
    center=gap+err
    assert gauge_P(center)<=Q(17,64)<Q(1,2)
    # Entire band is certified by its vertices, and includes exact graph.
    for sigma in product((-1,1), repeat=r):
     admitted=center+B*s.Matrix(sigma)/(2*r)
     assert gauge_P(admitted)<=Q(49,64)
     assert gauge_K(V*admitted)<=Q(49,64)
     assert V*J*(V*admitted)==V*admitted
    exact_band=-2*r*Bi*center
    assert max(abs(x) for x in exact_band)<=1
    cases+=1
print(f'PASS: {cases} exact effective-coordinate rounding/band cases; ranks 1--4; scaling through 2^80; endpoint and interior interpolation weights')
