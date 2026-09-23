"""Independent finite rational checks of the manuscript boundary constructions."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sympy as s

results = {}
def clip(t): return min(F(1), max(F(0), t))

# Check the exact weighted square gadget by differentiating its original cost.
n = 3
x = s.Symbol('x')
y = s.symbols('y:3'); p = s.symbols('p:3'); v = s.symbols('v:2')
clauses = [(y[0] + y[1] + y[2]), (1-y[0] + 1-y[1] + y[2])]
rho = s.Rational(1, 100*3**n); eta = rho**n; xi = eta/3
r = [y[i]-3**(i+1)*x+2*sum(3**(i-j)*y[j] for j in range(i))+1 for i in range(n)]
cost = sum(rho**i*r[i]**2/2 for i in range(n)) + eta/2*sum((p[i]-2*y[i]+1)**2 for i in range(n)) + xi/2*sum((v[a]-1+clauses[a])**2 for a in range(2))
coords = y+p+v
Q = s.hessian(cost, coords)
assert all(Q[:i,:i].det() > 0 for i in range(1,len(coords)+1))
grads = [s.diff(cost,z) for z in coords]
for bits in product([0,1],repeat=n):
    xd = sum(s.Rational(2*bits[i],3**(i+1)) for i in range(n))+s.Rational(1,2*3**n)
    subs = dict(zip(y,bits)); subs[x]=xd
    subs.update(zip(p,[max(0,2*d-1) for d in bits]))
    subs.update(zip(v,[max(0,1-c.subs(subs)) for c in clauses]))
    for z,g in zip(coords,grads):
        value = g.subs(subs)
        assert (subs[z] == 0 and value >= 0) or (subs[z] == 1 and value <= 0)
results['dense_original_square_KKT'] = '8 Boolean witnesses; all principal leading minors positive'

# Exact active-face oracle, independent of paper implementation.
def box_qp(Q,t):
    N=Q.rows
    for status in product([0,1,2],repeat=N):
        free=[i for i,a in enumerate(status) if a==1]
        z=s.Matrix([1 if a==2 else 0 for a in status])
        if free:
            zz=Q.extract(free,free).inv()*(-t-Q*z).extract(free,[0])
            for i,u in zip(free,zz): z[i]=u
        if any(u<0 or u>1 for u in z): continue
        g=Q*z+t
        if all(g[i]>=0 if a==0 else g[i]<=0 if a==2 else g[i]==0 for i,a in enumerate(status)):
            return z
    raise AssertionError('No KKT face')

# Near-identity network: exact scaled solutions, avoiding floating underflow.
N=6; C=18
A=s.zeros(N); b0=s.zeros(N,1); b1=s.zeros(N,1)
b0[0]=-1;b1[0]=3;b0[1]=-2;b1[1]=3
A[2,0]=-6;A[2,1]=6;b0[2]=-1;b1[2]=9
A[3,0]=-6;A[3,1]=6;b0[3]=-2;b1[3]=9
A[4,0]=2;A[4,1]=-2;b0[4]=-1
A[5,2]=2;A[5,3]=-2;b0[5]=-1
M=(1+N*C)**N; theta=s.Rational(1,100*N*C*M)
S=s.diag(*[theta**i/(4*C) for i in range(N)])
B=S*A*S.inv(); Q=(s.eye(N)-B).T*(s.eye(N)-B)
norm_inf=lambda M: max(sum(abs(M[i,j]) for j in range(M.cols)) for i in range(M.rows))
assert norm_inf(Q-s.eye(N)) < s.Rational(1,20)
checks=0
for price in [s.Rational(0),s.Rational(1,18),s.Rational(5,18),s.Rational(13,18),s.Rational(17,18),s.Rational(1)]:
    h=s.zeros(N,1)
    for i in range(N): h[i]=max(0,(A*h+b0+price*b1)[i])
    t=-(s.eye(N)-B).T*S*(b0+price*b1)
    u=box_qp(Q,t)
    error=max(abs(a-b) for a,b in zip(S.inv()*u,h))
    assert error <= 8*M*C*theta**2 <= s.Rational(1,16*N)
    checks+=1
results['near_identity_exact_relative_error']={'prices':checks,'dimension':N}

# Telescoping, distinct terminal coordinates, both exposures, and backward LP oracle.
checks=0
for n in range(1,7):
    gam=F(1,4)
    verts=[]
    for bits in product([0,1],repeat=n):
        z=[];prev=F(0)
        for bit in bits: prev=bit+(1-2*bit)*gam*prev;z.append(prev)
        verts.append((bits,z))
    assert len({z[-1] for _,z in verts})==2**n
    c=[(1-gam)*gam**(2*(n-i-1)-1) for i in range(n-1)]+[F(0)]
    chat=[gam**(3*(n-i-1)) for i in range(n-1)]+[F(0)]
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    for bits,z in verts:
        assert z[-1]-dot(c,z)-z[-1]**2==0
        lam=2*z[-1]-1
        score=dot(c,z)+lam*z[-1]
        assert all(score > dot(c,u)+lam*u[-1] for _,u in verts if u!=z)
        lamps=-sum(F(__import__('math').prod(1-2*d for d in bits[j:]))*gam**(2*(n-j)) for j in range(n))
        assert all(dot(chat,z)+lamps*z[-1]>dot(chat,u)+lamps*u[-1] for _,u in verts if u!=z)
        aa=lamps; value=max(F(0),aa)
        for i in range(n-2,-1,-1): aa=chat[i]-gam*abs(aa);value+=max(F(0),aa)
        assert value==dot(chat,z)+lamps*z[-1]
        checks+=1
results['path_vertices_exposure_and_LP_oracle']=checks

# Padding/slab equivalence for all targets on a small nonsurjective subset-sum set.
weights=[2,5,9]; W=sum(weights);r=0
while F(1,4**(r+1))>F(1,8*W):r+=1
n=len(weights);N=n+(n-1)*r;free=[i*(r+1) for i in range(n)]
values=[]
for bits in product([0,1],repeat=n):
    full=[0]*N
    for i,d in zip(free,bits):full[i]=d
    z=[];prev=F(0)
    for d in full:prev=d+(1-2*d)*F(1,4)*prev;z.append(prev)
    assert all(z[j]<=F(1,2) for j in range(N) if j not in free)
    score=sum(weights[i]*z[j] for i,j in enumerate(free))
    assert abs(score-sum(a*d for a,d in zip(weights,bits)))<=F(1,8)
    values.append(score)
for T in range(W+1):
    assert any(abs(v-T)<=F(1,4) for v in values)==any(sum(a*d for a,d in zip(weights,bits))==T for bits in product([0,1],repeat=n))
results['padding_all_targets']={'dimension':N,'targets':W+1}

# Continued-fraction recovery after the actual prescribed rational iterations.
Q=s.Matrix([[s.Rational(3,2),s.Rational(1,4)],[s.Rational(1,4),1]])
for t in [s.Matrix([-s.Rational(2,3),-s.Rational(1,3)]),s.Matrix([1,-2]),s.Matrix([-1,-s.Rational(1,9)])]:
    exact=box_qp(Q,t); LQ=norm_inf(Q); K=LQ*norm_inf(Q.inv())
    d=s.ilcm(*[a.q for a in list(Q)+list(t)])
    H=max(1,*[abs(d*a) for a in list(Q)+list(t)])
    Bden=2*H**2
    ceil_log2=lambda q: int(q).bit_length()-(1 if int(q)&(int(q)-1)==0 else 0)
    j=int(s.ceiling(K*(2*ceil_log2(Bden)+1+4)))
    z=s.zeros(2,1)
    for _ in range(j): z=(z-(Q*z+t)/LQ).applyfunc(lambda a:max(0,min(1,a)))
    assert max(abs(a-b) for a,b in zip(z,exact))<s.Rational(1,4*Bden**2)
    reconstructed=[F(int(a.p),int(a.q)).limit_denominator(int(Bden)) for a in z]
    assert all(s.Rational(a.numerator,a.denominator)==b for a,b in zip(reconstructed,exact))
results['exact_projected_gradient_rational_recovery']=3
Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
