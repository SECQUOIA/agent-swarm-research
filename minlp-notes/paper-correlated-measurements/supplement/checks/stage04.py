"""Independent exact, bounded proof diagnostics for Stage 4 (no repo imports)."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json
import sympy as sp

counts = {}
def check(name, condition):
    assert condition, name
    counts[name] = counts.get(name, 0) + 1

def sub(M, rows, cols=None):
    return M.extract(rows, rows if cols is None else cols)
def psd(M):
    return M == M.T and all(sub(M, list(I)).det() >= 0
      for r in range(1,M.rows+1) for I in combinations(range(M.rows),r))
def schur(M,p):
    return M[:p,:p] if M.rows==p else M[:p,:p]-M[:p,p:]*M[p:,p:].inv()*M[p:,:p]
def logbounds(x,m=45):
    x=Q(x);h=0
    while x>=2: x/=2;h+=1
    while x<1: x*=2;h-=1
    def part(u):
        val=2*sum((u**(2*j+1)/Q(2*j+1) for j in range(m)),Q(0))
        return val,val+2*u**(2*m+1)/((2*m+1)*(1-u*u))
    lo,hi=part((x-1)/(x+1));a,b=part(Q(1,3))
    return (lo+h*a,hi+h*b) if h>=0 else (lo+h*b,hi+h*a)

# Covariance filtering/adjoint independently versus literal resolvent inversion.
for n,rho,P in product(range(1,6),[sp.Rational(-2,3),sp.Rational(0),sp.Rational(2,3)], [sp.Rational(0),sp.Rational(1),sp.Rational(5)]):
    r=sp.Rational(1,3);a=sp.Rational(1,4)
    K=sp.Matrix(n,n,lambda i,j:P*rho**abs(i-j));R=K+r*sp.eye(n)
    F=sp.Matrix(n,2,lambda i,j:sp.Rational((-1)**(i+j)*(i+2*j+1),i+2));J0=sp.diag(sp.Rational(1,2),sp.Rational(2,3))
    for mode in range(4):
        z=[sp.Rational([0,1,sp.Rational(1,2),sp.Rational(2,3)][(i+mode)%4]) for i in range(n)]
        Z=sp.diag(*[v/a for v in z]);V=(sp.eye(n)+(R-a*sp.eye(n))*Z).inv()*F
        J=J0+F.T*Z*V
        pred=P;mean=sp.zeros(1,2);saved=[];Jf=J0.copy()
        for i in range(n):
            beta=a*(1-z[i])+r*z[i];q=z[i]*pred+beta;w=z[i]/q;e=F[i,:]-mean
            saved.append((pred,beta,q,w,e));Jf+=w*e.T*e
            mean=rho*(mean+pred*w*e);pred=rho**2*pred*beta/q+P*(1-rho**2)
        b=sp.zeros(1,2);Vr=sp.zeros(n,2)
        for i in reversed(range(n)):
            pred,beta,q,w,e=saved[i];Vr[i,:]=a/q*(e-rho*pred*b);b=w*e+rho*beta/q*b
        check('filter_information',Jf==J);check('reverse_adjoint_rows',Vr==V)
        grad=[(V[i,:]*J.inv()*V[i,:].T)[0]/a for i in range(n)]
        lo,hi=logbounds(J.det())
        for S in combinations(range(n),min(2,n)):
            S=list(S);Js=J0+sub(F,S,list(range(2))).T*sub(R,S).inv()*sub(F,S,list(range(2)))
            _,true_hi=logbounds(Js.det()/J.det());delta=sum(grad[i] for i in S)-sum(grad[i]*z[i] for i in range(n))
            # lower tangent intercept minus upper exact objective, certified rational positive.
            check('binary_log_tangent',Q(delta)>=true_hi)

# All-diagonal convex lower tangent and deliberately arbitrary dual factors.
R=sp.Matrix([[2,1],[1,2]]);F=sp.Matrix([1,-1]);z=[sp.Rational(1,2)]*2
A0=[sp.Rational(1),sp.Rational(1)];S=R+sp.diag(*A0);V=S.inv()*F;J=1+(F.T*V)[0]
g=sp.Matrix([-V[i]**2/J for i in range(2)]);Y=sp.Matrix([[1,-1],[-1,1]])/8
check('toy_information',J==2);check('toy_gradient',g==sp.Matrix([-sp.Rational(1,8)]*2))
check('toy_dual',psd(Y) and (R*Y).trace()==-(g.T*sp.Matrix(A0))[0])
for a1,a2 in product([sp.Rational(i,4) for i in range(1,8)],repeat=2):
    if not psd(R-sp.diag(a1,a2)):continue
    Ja=1+(F.T*(R+sp.diag(a1,a2)).inv()*F)[0]
    check('all_diagonal_toy_barrier',Ja>=2)
    lo,_=logbounds(Ja/J)
    check('diagonal_lower_tangent',lo>=Q((g.T*(sp.Matrix([a1,a2])-sp.Matrix(A0)))[0]))
for i in range(10):
    B=sp.Matrix([[sp.Rational(i-3,7),sp.Rational(i,9)],[sp.Rational(2-i,8),sp.Rational(i-4,5)]])
    YY=B*B.T;YY+=sp.diag(*[max(0,-g[j]-YY[j,j]) for j in range(2)])
    check('dual_repair',psd(YY) and all(YY[j,j]>=-g[j] for j in range(2)))

# Exact signed bridge and augmented Schur identities over every subset.
for rho in [sp.Rational(-3,5),sp.Rational(2,3)]:
    n=5;P=sp.Rational(3,2);r=sp.Rational(2,5)
    K=sp.Matrix(n,n,lambda i,j:P*rho**abs(i-j));R=K+r*sp.eye(n)
    F=sp.Matrix(n,2,lambda i,j:sp.Rational(i+(-1)**i*j,3));J0=sp.diag(1,2)
    for A in [[],[1],[1,3],list(range(n))]:
        KA=sub(K,A);H=K[:,A]*KA.inv() if A else sp.zeros(n,0)
        D=R-H*KA*H.T
        for k in range(n+1):
            for S0 in combinations(range(n),k):
                S0=list(S0);FS=F[S0,:];HS=H[S0,:];Z=FS.row_join(HS)
                M=sp.diag(J0,KA.inv())+Z.T*sub(D,S0).inv()*Z if S0 else sp.diag(J0,KA.inv())
                true=J0+FS.T*sub(R,S0).inv()*FS if S0 else J0
                check('separator_true_information',schur(M,2)==true)
        if A==[1,3]:
            i=2;l=i-A[0];u=A[1]-i
            expected=sp.Matrix([[rho**l*(1-rho**(2*u))/(1-rho**(2*(l+u))),rho**u*(1-rho**(2*l))/(1-rho**(2*(l+u)))]])
            check('signed_bridge_loadings',H[i,:]==expected)
            check('signed_bridge_variance',D[i,i]-r==P*(1-rho**(2*l))*(1-rho**(2*u))/(1-rho**(2*(l+u))))

# Generic normalized robust comparisons and the sharp tie construction.
a=Q(3,4);C=[(a,Q(1,10)),(Q(1,10),Q(1)),(Q(3,8),Q(3,8)),(Q(9,32),Q(3,8))]
family=C+[(Q(1,2),Q(1,2)),(Q(1),Q(1,10))]
d=[max(v[s] for v in C) for s in range(2)]
D=[max(v[s] for v in family) for s in range(2)]
for v in family:
    check('robust_simultaneous_cover',any(all(a*v[s]<=w[s]<=Q(5,4)*v[s] for s in range(2)) for w in C))
true=lambda v:min(v[s]/D[s] for s in range(2));approx=lambda v:min(v[s]/d[s] for s in range(2))
check('robust_normalized_tie',approx(C[-1])==max(map(approx,C)))
check('robust_factor_squared',true(C[-1])/max(map(true,family))==a*a)

# Signed interval scorer with independent direct rational quadratic comparison.
def mul(x,y):
    vals=[a*b for a in x for b in y];return min(vals),max(vals)
def sq(x):
    return (0 if x[0]<=0<=x[1] else min(x[0]**2,x[1]**2),max(x[0]**2,x[1]**2))
def encl(x,G):return (int(sp.floor(x*G)),int(sp.ceiling(x*G)))
for seed in range(100):
    GF=11;G=17;GS=13;d=sp.Rational(seed%7+1,9)
    H=sp.Matrix([[sp.Rational(seed%9-4,5),sp.Rational(seed%5-2,7)],[sp.Rational(seed%5-2,7),sp.Rational(seed%11-5,3)]])
    f=[sp.Rational(seed%7-3,8),sp.Rational(seed%13-6,9)];old=[sp.Rational(seed%5-2,6),sp.Rational(seed%3-1,4)];b=sp.Rational(seed%9-4,7)
    ui=[]
    for j in range(2):
        fl,fu=encl(f[j],GF);pl,pu=mul(encl(b,G),encl(old[j],GF));ui.append((G*fl-pu,G*fu-pl))
    upper=0
    for i in range(2):
        upper+=mul(encl(H[i,i],G),sq(ui[i]))[1]
    upper+=2*mul(encl(H[0,1],G),mul(ui[0],ui[1]))[1]
    dl=int(sp.floor(G*d));bound=sp.ceiling(sp.Rational(GS*max(0,upper),G*G*GF*GF*dl))/GS
    u=sp.Matrix(f)-b*sp.Matrix(old);score=(u.T*H*u)[0]/d
    check('signed_interval_score',bound>=score)

out={'status':'PASS','arithmetic':'exact rational; log inequalities use separately implemented rational enclosures; no floating tolerance','counts':counts,'assertions':sum(counts.values()),'sympy':sp.__version__}
(Path(__file__).resolve().parents[1]/'results/stage04-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
