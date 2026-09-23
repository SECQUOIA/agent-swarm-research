"""Distinct geometry, symbolic algebra, certificate and analytic stability audit."""
from fractions import Fraction as F
from itertools import combinations
import sympy as s
import numpy as np
# Exact straight-line incidence drawing: no crossings except common endpoints.
pos={'X':(-2,0),'Y':(0,-2),'Xp':(2,0),'Yp':(0,2),'Z':(0,0),'A':(-1,-1),'B':(-1,1),'C':(1,-1)}
edges=[(a,b) for a,bs in [('A',['X','Y','Z']),('B',['X','Yp','Z']),('C',['Xp','Y','Z'])] for b in bs]
cross=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
for (a,b),(c,d) in combinations(edges,2):
 if len({a,b,c,d})<4:continue
 A,B,C,D=[pos[z] for z in (a,b,c,d)]
 assert not (cross(A,B,C)*cross(A,B,D)<=0 and cross(C,D,A)*cross(C,D,B)<=0)
print('PASS exact straight-line crossover drawing has no unintended intersections.')
X,Y,Xp,Yp,Z=s.symbols('X Y Xp Yp Z')
g=s.groebner([X+Y-Z,X+Yp-Z,Xp+Y-Z],Xp,Yp,Z,X,Y)
g2=s.groebner([Xp-X,Yp-Y,Z-X-Y],Xp,Yp,Z,X,Y)
assert g==g2
print('PASS exact crossover ideal gives unique affine extension for all real input values.')
x,y,I,W=s.symbols('x y I W');C=s.Rational(9,2)
rCI=(1-I)+(1-(C-x))-(2-C)
rI=I*((I-W)+(I-1))+1
rD=(1-W)+2*(1-(C-x))+(1-(C-y))-(5-3*C)
assert s.groebner([rCI,rI,rD],I,W,x,y)==s.groebner([I-x,W-2*x+1-y,x*y-1],I,W,x,y)
print('PASS generalized inversion ideal, including enlarged complement constant.')
# Repeated variables cause no extra solutions in elimination ideal.
assert s.groebner([rCI.subs(y,x),rI,rD.subs(y,x)],I,W,x)==s.groebner([I-x,W-3*x+1,x*x-1],I,W,x)
print('PASS repeated-name generalized inversion.')
# Rational certificate for a genuinely irrational feasible 2-bus network:
# v0=1, v1=phi, P1=1. Round with mesh <=epsilon/(2*4*U*D), U=2,D=1.
phi=(1+s.sqrt(5))/2
for exp in range(1,101):
 eps=F(1,2**exp);mesh=F(1,2**(exp+4))
 w=F(int(s.floor(phi*2**(exp+4))),2**(exp+4))
 assert F(1,2)<=w<=2 and abs(w*(w-1)-1)<=eps/2
print('PASS 100 exact rational certificates approximating an irrational feasible voltage.')
# Check sharp-constant inequalities using independently assembled currents
# and weighted Laplacian eigenvalues on random connected graphs.
rng=np.random.default_rng(20260907)
trials=0
for n in range(2,19):
 for _ in range(30):
  E={(j,int(rng.integers(j))) for j in range(1,n)}
  E|={(i,j) for i in range(n) for j in range(i) if rng.random()<.12}
  L=np.zeros((n,n));current=np.zeros(n,dtype=complex)
  v=rng.uniform(.5,4,n)
  theta=rng.uniform(-np.pi/4,np.pi/4,n);theta-=theta.mean()
  U=v*np.exp(1j*theta); P0=np.zeros(n);gmin=np.inf
  for i,j in E:
   conductance=float(rng.uniform(.125,4));gmin=min(gmin,conductance)
   L[i,i]+=conductance;L[j,j]+=conductance;L[i,j]-=conductance;L[j,i]-=conductance
   f=conductance*(U[i]-U[j]);current[i]+=f;current[j]-=f
   P0[i]+=v[i]*conductance*(v[i]-v[j]);P0[j]+=v[j]*conductance*(v[j]-v[i])
  power=U*np.conj(current);q=power.imag;discrepancy=power.real-P0
  lam=np.linalg.eigvalsh(L)[1];ell=v.min();upper=v.max();qnorm=np.linalg.norm(q)
  assert np.linalg.norm(theta)<=np.pi*qnorm/(2*ell**2*lam)+1e-10
  assert discrepancy.min()>-1e-10
  assert discrepancy.max()<=np.pi**2*upper**2*qnorm**2/(8*ell**4*lam)+1e-10
  assert lam>=2*gmin/(n-1)**2-1e-10
  trials+=1
print(f'PASS numerical tight-constant reactive/spectral bounds on {trials} connected profiles.')
print('Finite symbolic/analytic checks supplement the mathematical audit; numerical checks are not proof certificates.')
