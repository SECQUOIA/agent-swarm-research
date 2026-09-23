import sympy as s
from itertools import combinations
q=s.Rational

def psd(X):
    return all(X.extract(T,T).det()>=0 for k in range(1,X.rows+1) for T in combinations(range(X.rows),k))

checks=0
for n in (2,3,4,5):
    V=s.Matrix(n,2,lambda i,j: q((i+2)*(j+1)%5-2,3))
    R=s.eye(n)+V*V.T
    F=s.Matrix(n,3,lambda i,j: q((i+1)*(j+2)%7-3,2))
    J0=s.diag(0,0,q(1,7))
    m=s.Integer(1); M=1+s.trace(V*V.T)
    alpha=(M+m)**2/(4*M*m)
    for k in range(n+1):
      for T in combinations(range(n),k):
        C=tuple(i for i in range(n) if i not in T)
        f=F.extract(T,range(3)); A=R.extract(T,T)
        J=J0+f.T*A.inv()*f if k else J0
        G=J0+f.T*R.inv().extract(T,T)*f if k else J0
        assert psd(G-J) and psd(alpha*J-G)
        assert J.nullspace()==G.nullspace()
        D=s.diag(*[i+1 for i in range(n)])
        RR=D*R*D; FF=D*F; ff=FF.extract(T,range(3))
        JJ=J0+ff.T*RR.extract(T,T).inv()*ff if k else J0
        GG=J0+ff.T*RR.inv().extract(T,T)*ff if k else J0
        assert JJ==J and GG==G
        if k and k<n:
            B=R.extract(T,C); CC=R.extract(C,C)
            gap=f.T*A.inv()*B*(CC-B.T*A.inv()*B).inv()*B.T*A.inv()*f
            assert G-J==gap
            fc=F.extract(C,range(3))
            cond=f-B*CC.inv()*fc
            assert cond.T*(A-B*CC.inv()*B.T).inv()*cond+fc.T*CC.inv()*fc==F.T*R.inv()*F
            assert (G-J).rank()<=B.rank()
        checks+=1
print('Exact subset/Schur/sandwich/kernel/scaling cases:',checks)
R=s.Matrix([[1,q(3,4)],[q(3,4),1]]); f=s.ones(2,1)
assert R.inv()[0,0]==q(16,7)
assert (f.T*R.inv()*f)[0]==q(8,7)
assert (1-q(3,4))**2/(1-q(3,4)**2)==q(1,7)
C=s.Matrix([[1,q(1,10),q(1,10)],[q(1,10),4,q(1,2)],[q(1,10),q(1,2),8]])
assert [C[:i,:i].det() for i in range(1,4)]==[1,q(399,100),q(791,25)]
R6=s.kronecker_product(s.Matrix([[1,q(1,2)],[q(1,2),1]]),C)
assert R6.inv()[:3,:3]==q(4,3)*C.inv()
a,k1,k2,t=s.symbols('a k1 k2 t',positive=True)
B=a*k1/(k2-k1)*(s.exp(-k1*t)-s.exp(-k2*t))
assert s.simplify(B-B.subs({a:a*k1/k2,k1:k2,k2:k1}, simultaneous=True))==0
F=s.Matrix([[s.diff(B,v).subs({a:1,k1:1,k2:2,t:j*s.log(2)}).simplify() for v in (a,k1,k2)] for j in (1,2,3)])
det=s.factor(F.det())
assert det!=0
print('Rate-swap preserved and local 3-time sensitivity determinant:',det)
print('All exact checks passed')
