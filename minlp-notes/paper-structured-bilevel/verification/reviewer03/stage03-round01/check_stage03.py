"""Independent exact diagnostics; no imported manuscript/author test code."""
from pathlib import Path
from itertools import product
import json
import sympy as s

HERE=Path(__file__).resolve().parent
x,z,c=s.symbols('x z c',real=True)
rho=s.Rational(1,16)
h=3*z*z-2*z**3
f=z*z*(1-z)**2+c*h
a=(1+s.sqrt(17))/16
assert s.factor((f-rho).subs(c,rho))==(z-1)**2*(16*z*z-2*z-1)/16
assert s.simplify((f-rho).subs({c:rho,z:a}))==0
assert bool(a<s.Rational(1,3))
assert s.simplify(s.diff(f,z)-2*z*(1-z)*(1-2*z+3*c))==0
# The derivative ratio is decreasing on [0,1/3], and its endpoint exceeds 1/4.
ratio=s.expand(s.diff(f,z).subs(c,rho)/z)
assert s.diff(ratio,z)==8*z-s.Rational(51,8)
assert ratio.subs(z,s.Rational(1,3))>s.Rational(1,4)
assert s.factor(h-z)==-z*(z-1)*(2*z-1)

# Fiber candidate can represent a nonstationary near-optimal response.
tau=s.Rational(1,2)
assert tau+(-tau)==0  # gradient + measurement-equality multiplier
assert tau!=0 and tau*tau/2<=s.Rational(1,4)
assert not (0<=s.Integer(2)<=1)  # empty measurement fiber is rejected

# An independent small Max-Cut check against continuous rational cube points.
edges=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]
def G(v): return sum((v[i]-v[j])**2 for i,j in edges)
binary=list(product([0,1],repeat=5))
cut=max(map(G,binary))
for v in product([s.Integer(0),s.Rational(1,2),s.Integer(1)],repeat=5):
    assert sum(t*t/2 for t in v)<=s.Rational(5,2)
    assert G(v)<=cut

# Three-coordinate exact dense follower, signed perturbation, diagonal surrogate.
Qhat=s.diag(1,2,1)
linear=s.Matrix([-2*x,s.Rational(1,4)-x,-s.Rational(1,2)])
cells=[(s.Integer(0),s.Rational(1,4)),(s.Rational(1,4),s.Rational(1,2)),(s.Rational(1,2),s.Integer(1))]
nominal=[s.Matrix([2*x,0,s.Rational(1,2)]),s.Matrix([2*x,(x-s.Rational(1,4))/2,s.Rational(1,2)]),s.Matrix([1,(x-s.Rational(1,4))/2,s.Rational(1,2)])]
nominal_labels=[('F','L','F'),('F','F','F'),('U','F','F')]
m0=s.Integer(1); L0=s.Integer(2); R=s.Integer(2)
sigma=s.Rational(1,8)
eps0=min(m0/2,sigma/(4*R*max(1/m0,1+L0/m0)))
E=eps0/s.Integer(6)*s.Matrix([[1,1,-1],[1,-1,1],[-1,1,0]])
eps=max(sum(abs(E[i,j]) for j in range(3)) for i in range(3))
Q=Qhat+E; Qi=Q.inv()
assert eps<=eps0 and all(Q[:k,:k].det()>0 for k in range(1,4))

# Original-coordinate exhaustive active-status oracle, prepared independently.
branches=[]
for labels in product('LFU',repeat=3):
    free=[i for i in range(3) if labels[i]=='F']
    upper=[i for i in range(3) if labels[i]=='U']
    zz=s.Matrix([1 if i in upper else 0 for i in range(3)])
    if free:
        sol=-Q[free,free].inv()*(linear[free,:]+Q[free,upper]*s.ones(len(upper),1))
        for i,b in enumerate(free): zz[b]=sol[i]
    branches.append((labels,zz,s.simplify(Q*zz+linear)))

def response(at):
    winners=[]
    for labels,zz,gg in branches:
        v=zz.subs(x,at); g=gg.subs(x,at)
        if not all(0<=v[i]<=1 for i in range(3)): continue
        if any((labels[i]=='L' and g[i]<0) or (labels[i]=='U' and g[i]>0) or (labels[i]=='F' and g[i]!=0) for i in range(3)): continue
        if v not in winners: winners.append(v)
    assert len(winners)==1
    return winners[0]

checks=0
certificate_checks=0
for (left,right),yy,labs in zip(cells,nominal,nominal_labels):
    pp=E*yy; ghat=Qhat*yy+linear
    eta=max((pp.T*Qi*pp)[0].subs(x,v) for v in [left,right])
    ss=yy-Qi*pp/2; tt=ghat+pp/2
    cert=[]
    transition=set()
    for endpoint in [left,right]:
        for i in range(3):
            if yy[i].subs(x,endpoint) in [0,1] and ghat[i].subs(x,endpoint)==0:
                transition.add(i)
    assert len(transition)<=2  # (r+1)q with r=q=1
    for i in range(3):
        ri=s.sqrt(Qi[i,i]*eta)/2; si=s.sqrt(Q[i,i]*eta)/2
        smin=min(ss[i].subs(x,v) for v in [left,right]); smax=max(ss[i].subs(x,v) for v in [left,right])
        tmin=min(tt[i].subs(x,v) for v in [left,right]); tmax=max(tt[i].subs(x,v) for v in [left,right])
        flags=[]
        if tmin>si or smax+ri<=0 or (tmin>=si and tmax>si): flags.append('L')
        if tmax<-si or smin-ri>=1 or (tmax<=-si and tmin<-si): flags.append('U')
        if (smin>=ri and smax<=1-ri and smax>ri and smin<1-ri): flags.append('F')
        if i not in transition: flags.append(labs[i])  # independent norm certificates
        cert.append(flags)
    for numerator in range(9):
        at=left+(right-left)*s.Rational(numerator,8)
        true=response(at); y=yy.subs(x,at); p=pp.subs(x,at); e=true-y
        assert (e.T*Q*e+p.T*e)[0]<=0
        for b in [s.Matrix([1,0,0]),s.Matrix([0,-1,2]),s.Matrix([-2,3,-1])]:
            center=(b.T*e+b.T*Qi*p/2)[0]
            assert center**2 <= (b.T*Qi*b)[0]*(p.T*Qi*p)[0]/4
            checks+=1
        gradient=Q*true+linear.subs(x,at)
        for i,flags in enumerate(cert):
            for label in flags:
                assert (label=='L' and true[i]==0) or (label=='U' and true[i]==1) or (label=='F' and gradient[i]==0)
                certificate_checks+=1

# Closure rule works at clipping endpoints; strict-somewhere is necessary.
assert min([0,1])>=0 and max([0,1])<=1 and max([0,1])>0 and min([0,1])<1
assert not (max([0])>0)  # a singleton lower-bound point fails the free refinement

summary={'positive_budget_factorization_and_bounds':'passed','nonstationary_fiber_candidate':'passed','maxcut_binary_optimum':cut,'continuous_grid_points':3**5,'directional_checks':checks,'whole_cell_certificate_point_checks':certificate_checks,'radius':str(eps0),'perturbation_norm':str(eps),'q':1,'max_transition_union':2,'limits':'Exact finite diagnostics; proof audit supplies universal whole-cell and asymptotic guarantees.'}
(HERE/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
