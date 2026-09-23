"""Independent reviewer checks; imports no manuscript implementation."""
import itertools, json
from pathlib import Path
import sympy as s
R=s.Rational
counts={}
def hit(k): counts[k]=counts.get(k,0)+1
def psd(M):
    assert M==M.T
    for k in range(1,M.rows+1):
        for ix in itertools.combinations(range(M.rows),k):
            assert M.extract(ix,ix).det()>=0, M
def schur(M,q):
    if M.rows==q:return M
    return M[:q,:q]-M[:q,q:]*M[q:,q:].inv()*M[q:,:q]
def aug(K,F,J0,a,S):
    n=K.rows;p=F.cols
    H=K[:,a]*K.extract(a,a).inv() if a else s.zeros(n,0)
    D=K-H*K[a,:]+s.eye(n)
    prior=s.diag(J0,K.extract(a,a).inv()) if a else J0
    X=F.row_join(H).extract(S,range(p+len(a)))
    return prior+X.T*D.extract(S,S).inv()*X if S else prior
T=s.Matrix([[1,0,0,0],[R(-2,3),1,0,0],[R(1,4),R(2,5),1,0],[R(3,7),R(-1,3),R(1,2),1]])
K=T*s.diag(R(1,2),R(3,4),R(2,3),R(4,5))*T.T
F=s.Matrix([[1,R(-2,3)],[R(-1,2),2],[R(2,3),R(1,5)],[R(-3,4),R(-2,5)]])
J0=s.Matrix([[1,R(1,4)],[R(1,4),R(2,3)]])
sets=[list(c) for k in range(5) for c in itertools.combinations(range(4),k)]
anchors=[[],[2],[0,2],[0,1,2,3]]
M={}
for a in anchors:
    M[tuple(a)]=[aug(K,F,J0,a,S) for S in sets]
    for S,X in zip(sets,M[tuple(a)]):
        J=J0+F[S,:].T*(K+s.eye(4)).extract(S,S).inv()*F[S,:] if S else J0
        assert schur(X,2)==J;hit('selected_schur')
        G=s.Matrix(len(a),2,lambda i,j:R((3*i+2*j)%5-2,3))
        E=s.eye(2).col_join(G)
        C=X[2:,2:];Gs=-C.inv()*X[2:,:2] if a else s.zeros(0,2)
        assert E.T*X*E-J==(G-Gs).T*C*(G-Gs)
        psd(E.T*X*E-J);hit('arbitrary_nuisance_quadratic')
for a,b in zip(anchors,anchors[1:]):
    order=list(range(2))+[2+b.index(i) for i in a]+[2+b.index(i) for i in b if i not in a]
    for i in range(len(sets)):
        assert M[tuple(a)][i]==schur(M[tuple(b)][i].extract(order,order),2+len(a));hit('cross_anchor')
    for j in range(0,len(sets),2):
        Ma=(M[tuple(a)][j]+2*M[tuple(a)][j+1])/3
        Mb=(M[tuple(b)][j]+2*M[tuple(b)][j+1])/3
        small=schur(Mb.extract(order,order),2+len(a))
        psd(small-Ma);psd(schur(Mb,2)-schur(Ma,2));hit('nested_mixture_order')
# Resolvent and exact derivatives at the cube boundary, including rank-deficient B.
B=s.Matrix([[1,-1,2],[0,1,-1],[1,0,1],[2,-1,3]])
B=B*B.T
a=[R(1,3),R(2,3),R(3,4),R(4,5)]
D=s.diag(*a);Cov=B+D
for z in itertools.product([0,R(1,2),1],repeat=4):
    Z=s.diag(*[zi/ai for zi,ai in zip(z,a)])
    V=(s.eye(4)+B*Z).inv()*F
    J=J0+F.T*Z*V
    ix=[i for i in range(4) if z[i]>0]
    direct=J0+F[ix,:].T*(Cov.extract(ix,ix)+s.diag(*[a[i]*(1-z[i])/z[i] for i in ix])).inv()*F[ix,:] if ix else J0
    assert J==direct;hit('vn_zero_boundary')
    for i in range(4):
        Ei=s.zeros(4);Ei[i,i]=1/a[i]
        derivative=F.T*(s.eye(4)+Z*B).inv()*Ei*(s.eye(4)+B*Z).inv()*F
        assert derivative==V[i,:].T*V[i,:]/a[i];psd(derivative);hit('vn_matrix_gradient')
# Independent reverse derivative with signed rho, zero visits and split above nugget.
for rho in [R(-3,5),R(2,5)]:
  n=4;P=R(3,4);r=R(1,3);a=r+R(1,20)
  K=s.Matrix(n,n,lambda i,j:P*rho**abs(i-j));Cov=K+r*s.eye(n);psd(Cov-a*s.eye(n))
  for z in itertools.product([0,R(1,2),1],repeat=n):
    priorvar=P;mean=s.zeros(1,2);records=[];J=J0
    for i in range(n):
      beta=a*(1-z[i])+r*z[i];q=z[i]*priorvar+beta;w=z[i]/q;e=F[i,:]-mean
      records.append((priorvar,beta,q,w,e));J+=w*e.T*e
      mean=rho*(mean+priorvar*w*e);priorvar=rho**2*priorvar*beta/q+P*(1-rho**2)
    back=s.zeros(1,2);rows=[]
    for i in reversed(range(n)):
      v,beta,q,w,e=records[i];rows.append(a/q*(e-rho*v*back));back=w*e+rho*beta/q*back
      assert a/q<=1
    V=s.Matrix.vstack(*rows[::-1]);Z=s.diag(*[zi/a for zi in z])
    assert V==(s.eye(n)+(Cov-a*s.eye(n))*Z).inv()*F
    assert J==J0+F.T*Z*V;hit('signed_dense_adjoint')
Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'PASS','counts':counts},indent=2)+'\n')
print(json.dumps(counts))
