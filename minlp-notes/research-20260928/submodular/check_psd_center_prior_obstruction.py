"""Exact check of a PSD-center obstruction derived from Burer et al. v3."""
from itertools import product
import sympy as s
R=s.Rational
Q0=s.Matrix([[8,-14,0,0],[-14,25,-25,0],[0,-25,25,-14],[0,0,-14,8]])
c0=s.Matrix([12,29,0,0])
# Exhaustive face-stationary candidates suffice for a box quadratic. For this
# matrix every singular stationary system is inconsistent.
values=[];singular=0
for state in product(range(3),repeat=4):
 free=[i for i,t in enumerate(state) if t==2];fixed=[i for i,t in enumerate(state) if t!=2]
 x=s.Matrix([t if t<2 else 0 for t in state])
 if free:
  H=Q0.extract(free,free);rhs=-c0.extract(free,[0])/2-Q0.extract(free,fixed)*x.extract(fixed,[0])
  if H.det()==0:
   assert H.rank()<H.row_join(rhs).rank();singular+=1;continue
  y=H.inv()*rhs
  for i,v in zip(free,y):x[i]=v
 if all(0<=v<=1 for v in x):values.append((x.T*Q0*x+c0.T*x)[0])
assert min(values)==0 and singular==4
Q=Q0.copy();Q[0,0]-=8;Q[3,3]-=8;Q[1,1]+=R(1,16);Q[2,2]+=R(1,16)
c=c0+s.Matrix([8,0,0,8])
H=Q.extract([1,2],[1,2]);assert H.eigenvals()=={R(1,16):1,R(801,16):1}
mu=s.Matrix([R(3,32),R(3,16),R(9,16),R(3,4)])
X=s.Matrix([[R(3,32),R(3,32),R(3,32),R(61,1024)],[R(3,32),R(125,1024),R(3,16),R(3,16)],[R(3,32),R(3,16),R(231,512),R(9,16)],[R(61,1024),R(3,16),R(9,16),R(3,4)]])
Y=s.Matrix.vstack(s.Matrix.hstack(s.ones(1,1),mu.T),s.Matrix.hstack(mu,X))
assert all(Y[:i,:i].det()>0 for i in range(1,6))
assert all(0<=X[i,j] and mu[i]+mu[j]-1<=X[i,j]<=min(mu[i],mu[j]) for i in range(4) for j in range(4))
objective=sum(Q[i,j]*X[i,j] for i in range(4) for j in range(4))+(c.T*mu)[0]
assert objective==R(-1157,16384)
print('81 original face patterns checked; 4 singular systems inconsistent; minimum 0.')
print('PSD-center eigenvalues:',list(H.eigenvals()))
print('Full RLT and five positive leading moment minors checked exactly.')
print('Modified relaxed objective:',objective)
