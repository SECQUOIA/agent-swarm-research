from itertools import combinations
import json
from pathlib import Path
import sympy as s
R=s.Rational
counts={}
def subs(n):
 return [list(c) for k in range(n+1) for c in combinations(range(n),k)]
def schur(M,d):
 return M[:d,:d]-M[:d,d:]*M[d:,d:].inv()*M[d:,:d] if M.rows>d else M

def model(K,F,J,r,A,T):
 n=K.rows; p=F.cols
 if A:
  Ka=K.extract(A,A); H=K[:,A]*Ka.inv(); D=K-H*K[A,:]
  base=s.diag(J,Ka.inv())
 else:
  H=s.zeros(n,0); D=K; base=J
 D=D+r*s.eye(n)
 Q=F.row_join(H)
 return base+(Q[T,:].T*D.extract(T,T).inv()*Q[T,:] if T else s.zeros(p+len(A))), H,D

# Direct rational proof checks independent of the paper's code.
K=s.Matrix([[3,1,-1],[1,2,R(1,3)],[-1,R(1,3),4]])
F=s.Matrix([[1,2],[-2,1],[3,-1]]); J=s.Matrix([[2,R(1,3)],[R(1,3),1]])
allS=subs(3)
for B in allS:
 for A in subs(3):
  if not set(A)<=set(B): continue
  C=[x for x in B if x not in A]
  for T in allS:
   MA,_,_=model(K,F,J,R(2,3),A,T)
   MB,_,_=model(K,F,J,R(2,3),A+C,T)
   assert schur(MB,2+len(A))==MA
   assert schur(MA,2)==J+(F[T,:].T*(K+R(2,3)*s.eye(3)).extract(T,T).inv()*F[T,:] if T else s.zeros(2))
   counts['cross_representation']=counts.get('cross_representation',0)+1
  # Same mixture over complete cardinality-one schedules, exact PSD orders.
  Ts=[[0],[1],[2]]; alpha=[R(1,7),R(2,7),R(4,7)]
  avgA=sum((a*model(K,F,J,R(2,3),A,T)[0] for a,T in zip(alpha,Ts)),s.zeros(2+len(A)))
  avgB=sum((a*model(K,F,J,R(2,3),A+C,T)[0] for a,T in zip(alpha,Ts)),s.zeros(2+len(B)))
  dif=schur(avgB,2+len(A))-avgA
  assert dif.is_positive_semidefinite
  assert (schur(avgB,2)-schur(avgA,2)).is_positive_semidefinite
  counts['mixture_orders']=counts.get('mixture_orders',0)+1

# All boundary/signed stationary bridge loadings and covariances, including rho=0.
n=5
for rho in [R(-2,3),R(0),R(3,5)]:
 K=s.Matrix(n,n,lambda i,j:R(7,5)*rho**abs(i-j)); P=R(7,5); r=R(4,7)
 F=s.Matrix(n,2,lambda i,j:(i+1)**(j+1)-2*j); J=s.eye(2)
 for A in subs(n):
  _,H,D=model(K,F,J,r,A,[])
  for i in range(n):
   if i in A:
    expected=s.zeros(1,len(A)); expected[A.index(i)]=1
   else:
    expected=s.zeros(1,len(A)); left=[a for a in A if a<i]; right=[a for a in A if a>i]
    a=max(left) if left else None; c=min(right) if right else None
    if a is not None: expected[A.index(a)]=rho**(i-a)*(1-rho**(2*(c-i)))/(1-rho**(2*(c-a))) if c is not None else rho**(i-a)
    if c is not None: expected[A.index(c)]=rho**(c-i)*(1-rho**(2*(i-a)))/(1-rho**(2*(c-a))) if a is not None else rho**(c-i)
   assert H[i,:]==expected
   for j in range(i,n):
    if i in A or j in A or any(i<a<j for a in A): val=0
    else:
     left=[a for a in A if a<i]; right=[a for a in A if a>j]
     a=max(left) if left else None; c=min(right) if right else None
     val=P*rho**(j-i)
     if a is not None: val*=1-rho**(2*(i-a))
     if c is not None: val*=1-rho**(2*(c-j))
     if a is not None and c is not None: val/=1-rho**(2*(c-a))
    assert D[i,j]==val+(r if i==j else 0)
    counts['bridge_entries']=counts.get('bridge_entries',0)+1
  if A:
   G=s.Matrix(len(A),2,lambda i,j:(i+1)*(-1)**j+j); W=s.Matrix([[2,R(1,3)],[R(1,3),1]])
   val=(G[0,:]*W*G[0,:].T)[0]/P
   for j in range(1,len(A)):
    c=rho**(A[j]-A[j-1]); u=G[j,:]-c*G[j-1,:]
    val+=(u*W*u.T)[0]/(P*(1-c*c))
   assert val==s.trace(W*G.T*K.extract(A,A).inv()*G)
   counts['anchor_prior']=counts.get('anchor_prior',0)+1

# Singleton split, exact zero and one marginals, including empty/full anchors.
for n in [1,3]:
 K=s.Matrix(n,n,lambda i,j:R(1,2)**abs(i-j)); F=s.Matrix(n,2,lambda i,j:(i+1)**(j+1)); J=s.eye(2); r=R(2,3)
 for A in [[],list(range(n)),list(range(n-1))]:
  base,H,D=model(K,F,J,r,A,[])
  if not D.is_diagonal(): continue
  for zs in [[R(0)]*n,[R(1)]*n,[R(i,n+1) for i in range(1,n+1)]]:
   Z=s.diag(*[zs[i]/D[i,i] for i in range(n)])
   M=base+F.row_join(H).T*Z*F.row_join(H)
   expected=J+F.T*Z*(s.eye(n)+(K+r*s.eye(n)-D)*Z).inv()*F
   assert schur(M,2)==expected
   counts['singleton_splits']=counts.get('singleton_splits',0)+1

# Strict hierarchy example exact values.
K=s.Matrix([[1,R(1,2)],[R(1,2),1]]); F=s.Matrix([1,-1]); J=s.eye(1)
for A,val in [([],R(3,2)),([0],R(75,44)),([0,1],R(9,5))]:
 M=(model(K,F,J,1,A,[0])[0]+model(K,F,J,1,A,[1])[0])/2
 assert schur(M,1)[0]==val
counts['strict_hierarchy']=3
print(json.dumps(counts,indent=2))
Path(__file__).with_name('results.json').write_text(json.dumps(counts,indent=2)+'\n')
# Stationary conditional bridge filtering, with anchors assigned on either side.
for rho in [R(-2,3),R(0),R(3,5)]:
 n=5; P=R(7,5); r=R(4,7)
 K=s.Matrix(n,n,lambda i,j:P*rho**abs(i-j)); F=s.Matrix(n,2,lambda i,j:(i+1)**(j+1)-j)
 A=[1,3]; G=s.Matrix([[R(1,3),-1],[R(2,5),R(4,3)]]); W=s.Matrix([[2,R(1,3)],[R(1,3),1]])
 base,H,D=model(K,F,s.eye(2),r,A,[]); rows=F+H*G
 for blocks in [[[0,1],[2,3],[4]],[[0],[1,2],[3,4]]]:
  for T in subs(n):
   score=s.zeros(2)
   for block in blocks:
    previous=None; estimate=s.zeros(1,2); post=0
    for t in [i for i in block if i in T]:
     if t in A:
      score+=rows[t,:].T*rows[t,:]/r
      previous=None; estimate=s.zeros(1,2); post=0
      continue
     Vt=D[t,t]-r
     if previous is None:
      pred=Vt; estimate=s.zeros(1,2)
     else:
      right=[a for a in A if a>t]; c=min(right) if right else None
      tr=rho**(t-previous)
      if c is not None: tr*= (1-rho**(2*(c-t)))/(1-rho**(2*(c-previous)))
      Vs=D[previous,previous]-r
      pred=Vt-tr*tr*Vs+tr*tr*post
      estimate=tr*estimate
     innovation=rows[t,:]-estimate
     score+=innovation.T*innovation/(pred+r)
     gain=pred/(pred+r); estimate+=gain*innovation; post=(1-gain)*pred; previous=t
   exact=rows[T,:].T*D.extract(T,T).inv()*rows[T,:] if T else s.zeros(2)
   assert score==exact
   M=model(K,F,s.eye(2),r,A,T)[0]
   E=s.eye(2).col_join(G)
   assert (E.T*M*E-schur(M,2)).is_positive_semidefinite
   Jsch=schur(M,2); Gstar=-M[2:,2:].inv()*M[2:,:2]; Estar=s.eye(2).col_join(Gstar)
   grad=Estar*Jsch.inv()*Estar.T
   assert grad.rank()==2 and s.trace(grad*M)==2
   counts['filter_and_arbitrary_witness']=counts.get('filter_and_arbitrary_witness',0)+1
print(json.dumps(counts,indent=2))
Path(__file__).with_name('results.json').write_text(json.dumps(counts,indent=2)+'\n')
