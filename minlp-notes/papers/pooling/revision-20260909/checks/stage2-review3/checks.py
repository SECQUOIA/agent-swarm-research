"""Independent bounded checks; these supplement, not replace, proof review."""
from fractions import Fraction as F
from itertools import product, combinations
import json
from pathlib import Path
import sympy as sp
from scipy.optimize import linprog

results={}
def perfect(v):
    if not v:
        yield (); return
    a=v[0]
    for b in v[1:]:
        for rest in perfect([x for x in v if x not in (a,b)]):
            yield ((a,b),)+rest

def alpha(n,edges):
    best=0
    for mask in range(1<<n):
        if mask.bit_count()>best and all(not(mask>>a&1 and mask>>b&1) for a,b in edges):
            best=mask.bit_count()
    return best

def colored_check(n,colors):
    edges=sum(colors,())
    orig=alpha(n,edges)
    h_edges=list(colors[0]+colors[1])
    for a,b in colors[2]:
        h_edges += [(a,n+a),(n+a,n+b),(n+b,b)]
    assert alpha(2*n,h_edges)==n//2+orig
    best=0
    for modes in product(range(3),repeat=n): # inactive, clean, dirty
        if any(modes[a]==modes[b]==1 for a,b in colors[0]+colors[1]):continue
        if any(modes[a]==modes[b]==2 for a,b in colors[2]):continue
        best=max(best,sum(t!=0 for t in modes))
    assert best==n//2+orig
    # For all fixed modes, the resource LP attains integral value.
    for modes in product([1,2],repeat=n):
        rows=[]
        for c,color in enumerate(colors):
            for a,b in color:
                row=[0]*n
                for v in [a,b]:row[v]=int(modes[v]==(2 if c==2 else 1))
                rows.append(row)
        lp=linprog([-1]*n,A_ub=rows,b_ub=[1]*len(rows),bounds=[(0,1)]*n,method='highs')
        assert lp.success and abs(-lp.fun-round(-lp.fun))<1e-8
    return orig,best

count=0
for n in [4,6]:
    ps=list(perfect(list(range(n))))
    for colors in combinations(ps,3):
        if len(set(sum(colors,())))!=3*n//2:continue
        colored_check(n,colors);count+=1
results['all_colored_graphs_n4_n6']=count

# Positive-tolerance K4 point: verify mass, pool/source/output capacities and mass qualities exactly.
colors=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
for delta in [F(1,100),F(1,7),F(1,2)]:
    a=[1-delta,0,0,1-delta]; d=[delta,1,0,delta]; ss=[1,0,0,1]; b=[0,1,0,0]
    q=[delta,F(1),0,delta]
    assert all(a[v]+d[v]==ss[v]+b[v]<=1 for v in range(4))
    assert all(q[v]*(a[v]+d[v])==d[v] for v in range(4))
    assert all(a[u]+a[v]<=1 for u,v in colors[0])
    assert all(d[u]+d[v]<=1 and b[u]+b[v]<=1 for u,v in colors[2])
    assert all(ss[u]+ss[v]<=1 and q[u]*ss[u]+q[v]*ss[v]<=delta*(ss[u]+ss[v]) for u,v in colors[1])
    assert sum(ss)+sum(d)==3+2*delta
results['positive_tolerance_K4']='3 exact rational cases passed'

# Algebraic identities and Matsui counterexample.
Y,X,p,n,T,S=sp.symbols('Y X p n T S')
A=sp.symbols('A')
assert sp.expand((2*A-p+Y+2*sp.sqrt(A)*X)*(2*A-p+Y-2*sp.sqrt(A)*X)-4*A*A-((Y-p)**2+4*A*(Y-X*X-p)))==0
nn=5;pp=2
xx=sum(F(pp**i,2) for i in range(1,nn+1))
yy=sum(F(pp**(2*i),2) for i in range(1,nn+1))
assert yy-xx*xx==-279
assert F(pp**2,8)-pp*nn**2==F(-99,2)
results['Matsui_counterexample']={'D':str(yy-xx*xx),'printed_bound':str(F(-99,2))}
for nn in [5,6,8]:
    pp=nn**(nn**4); s=nn+nn**2; P4=pp**(4*nn);u0=2*P4-pp;D0=1<<((u0//2).bit_length()-1);K=4*pp**(8*nn)
    assert 2*D0<=u0<4*D0 and D0>F(P4,4)
    generators=[(u0,u0)]
    generators += [(u0+2*s*pp**(2*nn+i),u0-2*s*pp**(2*nn+i)) for i in range(1,nn+1)]
    generators += [(u0+s*pp**(i+j),u0+s*pp**(i+j)) for i in range(1,nn+1) for j in range(1,nn+1)]
    for U,V in generators:
        assert 2<=F(U,D0)<20 and K-D0*V>0
        rho=F(U-2*D0,32*D0)
        assert 0<=rho<1 and rho.denominator&(rho.denominator-1)==0
results['finite_data_generator_bounds']='n=5,6,8 passed using exact big integers'

# Binary multiplier all dyadic numerators up to 8 bits and three rational signals.
count=0
for L in range(1,9):
    for c in range(2**L):
        for x in [F(0),F(7,11),F(2)]:
            t=F(0)
            for k in range(L):
                t=(t+((c>>k)&1)*x)/2
                assert 0<=t<=2
            assert t==F(c,2**L)*x;count+=1
results['binary_multiplier_exact_cases']=count

# Full/half closed cycles directly as independent LP constraints, without port identities imposed.
def cycle_lp(half,r):
    # Every gadget has [uA,vA,mA,uB,vB,mB].
    eq=[];rhs=[];ub=[];urhs=[]
    D=3 if half else 4; gamma=F(1) if half else F(3,2)
    for g in range(r):
        for o in [0,3]:
            z=[0]*(6*r)
            for k in [0,1,2]:z[6*g+o+k]=1
            eq.append(z);rhs.append(D)
            z=[0]*(6*r);z[6*g+o+1]=3;z[6*g+o+2]=float(gamma)
            ub.append(z);urhs.append(float(gamma*D))
        z=[0]*(6*r);z[6*g+2]=z[6*g+5]=1;eq.append(z);rhs.append(D)
        z=[0]*(6*r);z[6*g+3]=z[6*((g+1)%r)]=1;eq.append(z);rhs.append(2)
    bounds=[v for _ in range(r) for v in [(0,2),(0,1 if half else 2),(0,D),(0,2),(0,1 if half else 2),(0,D)]]
    for g in range(r):
        for o in [0,3]:
            c=[0]*(6*r);c[6*g+o]=1;c[6*g+o+1]=-2 if half else -1
            for sign in [-1,1]:
                rr=linprog([sign*x for x in c],A_ub=ub,b_ub=urhs,A_eq=eq,b_eq=rhs,bounds=bounds,method='highs')
                assert rr.success and abs(rr.fun)<1e-8
for half in [False,True]:
    for r in [1,2,5]:cycle_lp(half,r)
results['cycle_LP_projection']='full and half cycles of length 1,2,5 force exact endpoint ratios'

# Radial repair and two-feed mass over exact rational grids.
count=0
for a in [F(1),F(3,2),F(19),F(100)]:
    for t in [F(k,10) for k in range(21)]:
        mass=a*t; defect=mass*(t-1)-t
        if defect>0:
            repaired=1+1/a
            assert repaired<t and a*repaired*(repaired-1)-repaired==0
            assert t-repaired==defect/mass
        else:
            y1=max(F(0),t-1);y2=t-y1;anchor=(a-1)*y1
            assert y2<=1 and 0<=anchor<=1 and y1+anchor<=1 and a*y1<=y1+anchor
        count+=1
results['radial_repair_cases']=count
Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
