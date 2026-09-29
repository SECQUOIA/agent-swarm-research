"""Exact finite certificate for a failed PSD-center extension of SDP exactness."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
Q=sp.Matrix([[11,-5,-sp.Rational(7,2),0],[-5,6,0,-5],[ -sp.Rational(7,2),0,-5,0],[0,-5,0,-6]])
b=sp.Matrix([9,-1,23,27])
H=Q[:2,:2]
assert H.det()==41 and H[0,0]>0

def box_value(z):
 z=sp.Matrix(z);lin=b[:2,0]+2*Q[:2,2:]*z
 candidates=[]
 for st in product(range(3),repeat=2):
  free=[i for i in range(2) if st[i]==2];fixed=[i for i in range(2) if st[i]!=2]
  x=sp.Matrix([st[i] if st[i]!=2 else 0 for i in range(2)])
  if free:
   rhs=-lin.extract(free,[0])/2-H.extract(free,fixed)*x.extract(fixed,[0])
   sol=H.extract(free,free).inv()*rhs
   for i,v in zip(free,sol):x[i]=v
  if all(0<=v<=1 for v in x):
   v=(x.T*H*x+lin.T*x+z.T*Q[2:,2:]*z+b[2:,0].T*z)[0]
   candidates.append((v,x))
 return min(candidates,key=lambda p:p[0])
vals={z:box_value(z) for z in product(range(2),repeat=2)}
f00=vals[(0,0)][0];g2=vals[(0,1)][0]-f00;g1=vals[(1,1)][0]-vals[(0,1)][0]
bnew=b.copy();bnew[2]-=g1;bnew[3]-=g2
assert all(v[0]-f00-g1*z[0]-g2*z[1]>=0 for z,v in vals.items())
# The stored certificate is rational. Its validity does not depend on the
# numerical SDP used to discover it.
data=json.loads((HERE/'psd_center_exact_certificate.json').read_text())
mu=sp.Matrix([sp.Rational(v) for v in data['mu']])
X=sp.Matrix([[sp.Rational(v) for v in row] for row in data['X']])
assert sp.Matrix(data['Q']).applyfunc(sp.Rational)==Q
assert sp.Matrix(data['b']).applyfunc(sp.Rational)==bnew
assert sp.Rational(data['constant'])==-f00
Y=sp.Matrix.vstack(sp.Matrix.hstack(sp.ones(1,1),mu.T),sp.Matrix.hstack(mu,X))
_,diag=Y.LDLdecomposition(hermitian=False)
assert all(diag[i,i]>0 for i in range(5))
assert all(0<=v<=1 for v in mu)
assert all(X[i,j]>=0 and X[i,j]>=mu[i]+mu[j]-1 and X[i,j]<=mu[i] and X[i,j]<=mu[j] for i in range(4) for j in range(4))
value=sum(Q[i,j]*X[i,j] for i in range(4) for j in range(4))+(bnew.T*mu)[0]-f00
assert value<0
print('Principal center determinant:',H.det())
print('Binary fiber minima:',{str(z):str(v[0]) for z,v in vals.items()})
print('New b:',list(bnew),'constant:',-f00)
print('Exact relaxed objective:',value,'approximately',float(value))
print('Smallest LDL pivot:',min(diag[i,i] for i in range(5)))
print('All full RLT inequalities and positive definiteness checked exactly.')
assert sp.Rational(data['objective'])==value
