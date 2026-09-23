"""Independent exact-rational checks; no author/repository helpers imported."""
from itertools import product
from pathlib import Path
import json
import sympy as s
Q=s.Rational
counts={'dense_forward_reverse':0,'diagonal_resolvent':0,'binary_exactness':0,'boundary_gradient':0,'toy':0}
for n in (1,2,4):
 for rho in (Q(-3,5),Q(0),Q(7,8)):
  P,r=Q(3,2),Q(5,4)
  K=s.Matrix(n,n,lambda i,j:P*rho**abs(i-j));R=K+r*s.eye(n)
  F=s.Matrix(n,2,lambda i,j:Q((-1)**(i+j)*(i+2*j+1),i+j+2));J0=s.Matrix([[2,Q(1,3)],[Q(1,3),1]])
  for a in (r/2,r,r+P*(1-abs(rho))/(1+abs(rho))/2):
   for z in product((Q(0),Q(1,3),Q(1)),repeat=n):
    Z=s.diag(*(v/a for v in z));V=(s.eye(n)+(R-a*s.eye(n))*Z).inv()*F
    J=J0+F.T*Z*V;beta=[a*(1-v)+r*v for v in z]
    if n>=2:
     c=P*(1-rho**2);M=c*K.inv()
     U=(M+c*s.diag(*(z[i]/beta[i] for i in range(n)))).inv()*M*F
     assert V==s.diag(*(a/beta[i] for i in range(n)))*U
    pred=P;mean=s.zeros(1,2);Jf=J0.copy();hist=[]
    for i in range(n):
     e=F[i,:]-mean;q=z[i]*pred+beta[i];w=z[i]/q
     hist.append((pred,e,q,w));Jf+=w*e.T*e
     mean=rho*(mean+pred*w*e);pred=rho**2*pred*beta[i]/q+P*(1-rho**2)
    assert J==Jf
    b=s.zeros(1,2)
    for i in reversed(range(n)):
     pred,e,q,w=hist[i];assert V[i,:]==a/q*(e-rho*pred*b)
     b=w*e+rho*beta[i]/q*b
     assert a/q<=1
    counts['dense_forward_reverse']+=1
# General unequal diagonal splits including rank-deficient and zero B.
for n in (2,3):
 D=s.diag(*(Q(i+1,2) for i in range(n)));F=s.Matrix(n,2,lambda i,j:i+j+1)
 for U in (s.zeros(n,1),s.ones(n,1),s.Matrix(n,2,lambda i,j:Q((-1)**(i+j)*(i+j+1),3))):
  B=U*U.T;R=D+B;J0=s.eye(2)
  for z in product((Q(0),Q(1,2),Q(1)),repeat=n):
   Z=s.diag(*(z[i]/D[i,i] for i in range(n)));res=(s.eye(n)+B*Z).inv();V=res*F;J=J0+F.T*Z*V
   T=[i for i in range(n) if z[i]>0]
   if T:
    S=R.extract(T,T)+s.diag(*(D[i,i]*(1-z[i])/z[i] for i in T));Fs=F.extract(T,range(2));Js=J0+Fs.T*S.inv()*Fs
   else:Js=J0
   assert J==Js;counts['diagonal_resolvent']+=1
   if all(v in (0,1) for v in z):counts['binary_exactness']+=1
   for i in range(n):
    dZ=s.zeros(n);dZ[i,i]=1/D[i,i]
    dJ=F.T*(dZ*res-Z*res*B*dZ*res)*F
    assert dJ==V[i,:].T*V[i,:]/D[i,i]
    if z[i] in (0,1):counts['boundary_gradient']+=1
R=s.Matrix([[2,1],[1,2]]);F=s.Matrix([1,-1]);a=s.ones(2,1);S=R+s.eye(2);V=S.inv()*F;J=1+(F.T*V)[0]
g=s.Matrix([-V[i,0]**2/J for i in range(2)]);Y=s.Matrix([[1,-1],[-1,1]])/8
assert J==2 and g==s.Matrix([-Q(1,8),-Q(1,8)])
assert -(g.T*a)[0]-s.trace(R*Y)==0
assert 1+F[0,0]**2/R[0,0]==Q(3,2)
counts['toy']+=1
Path(__file__).with_name('results.json').write_text(json.dumps({'status':'PASS','arithmetic':'exact SymPy rationals','counts':counts},indent=2)+'\n')
print(counts)
