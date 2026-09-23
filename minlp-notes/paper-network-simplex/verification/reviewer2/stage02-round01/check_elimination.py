"""Independent rational tests for path and observation compression; no hull imports."""
import itertools
import json
import random
from pathlib import Path
import sympy as s
rng = random.Random(28103)

def components(n, edges):
    p = list(range(n))
    def root(v):
        while p[v] != v:
            p[v] = p[p[v]]; v = p[v]
        return v
    forest=[]
    for i,(u,v) in enumerate(edges):
        a,b = root(u),root(v)
        if a != b: p[a]=b; forest.append(i)
    return len({root(i) for i in range(n)}), forest

def incidence(n,edges):
    A=s.zeros(n,len(edges))
    for e,(u,v) in enumerate(edges): A[u,e]-=1; A[v,e]+=1
    return A

def cycle_matrix(n,edges):
    A=incidence(n,edges)
    nc,T=components(n,edges)
    assert nc==1
    Q=[i for i in range(len(edges)) if i not in T]
    C=s.zeros(len(edges),len(Q))
    if T:
        top=-A[:-1,T].inv()*A[:-1,Q]
        for i,e in enumerate(T):
            for j in range(len(Q)): C[e,j]=top[i,j]
    for j,e in enumerate(Q): C[e,j]=1
    assert A*C==s.zeros(n,len(Q))
    return A,C

cores=[(1,[(0,0)]),(2,[(0,1)]*2),(2,[(0,1)]*3),
       (4,list(itertools.combinations(range(4),2))),
       (6,[(u,v) for u in range(3) for v in range(3,6)])]
checked=0
for n,core in cores:
    for orientation in range(6):
        edges=[]; paths=[]; new_n=n
        for u,v in core:
            size=rng.randrange(1,4)
            interior=list(range(new_n,new_n+size-1)); new_n+=size-1
            route=[u]+interior+[v]; path=[]
            for a,b in zip(route,route[1:]):
                sign=rng.choice([-1,1])
                path.append((len(edges),sign))
                edges.append((a,b) if sign==1 else (b,a))
            paths.append(path)
        A,C=cycle_matrix(new_n,edges)
        r=C.cols
        assert r == len(core)-n+1
        for path in paths:
            first,sign=path[0]
            for e,epsilon in path: assert epsilon*C[e,:] == sign*C[first,:]
        if r>=2:
            degrees=[0]*n
            for u,v in core: degrees[u]+=1; degrees[v]+=1
            assert min(degrees)>=3
            assert n<=2*r-2 and len(core)<=3*r-3
        candidates = [[],list(range(len(edges)))]
        candidates += [[e for e in range(len(edges)) if rng.randrange(2)] for _ in range(25)]
        for observed in candidates:
            obs=C[observed,:]
            selected=list(obs.T.rref()[1])
            D=obs[selected,:]
            d=D.rows
            I=list(D.rref()[1]); F=[j for j in range(r) if j not in I]
            B=D[:,I]
            Binv=B.inv() if d else s.zeros(0,0)
            t=s.Matrix([s.Rational(rng.randrange(-10,11),7) for _ in range(r)])
            q=D*t
            for e in range(len(edges)):
                c=C[e,:]
                W=c[:,I]*Binv
                R=c[:,F]-W*D[:,F]
                assert all(v in [-1,0,1] for v in list(W)+list(R))
                assert (W*q+R*t[F,0])[0] == (c*t)[0]
            U=[i for i in range(len(edges)) if i not in observed]
            nc,forest=components(new_n,[edges[i] for i in U])
            rho=len(U)-new_n+nc
            assert rho==r-d
            added=[U[i] for i in range(len(U)) if i not in forest]
            assert len(added)==rho and C[observed+added,:].rank()==r
            checked+=1
# K4 worked example: independent incoming-minus-outgoing check.
edges=list(itertools.combinations(range(1,5),2))
A=incidence(5,edges)
y,q13,q14,q24=s.symbols('y q13 q14 q24')
h=s.Matrix([-q13-q14,q13,q14,-q13-q14-q24,q24,-q14-q24])
assert A*h==s.zeros(5,1)
x=s.Matrix([s.Rational(1,2),s.Rational(1,4),s.Rational(1,4),s.Rational(1,4),s.Rational(1,4),s.Rational(1,2)])
assert A*x==s.Matrix([0,-1,0,0,1])
for e in [1,2,4]:
    z=s.Rational(1,5); yy=s.Rational(1,2)
    assert max(0,x[e]+yy-1)<=z<=min(x[e],yy)
assert 3*s.Rational(1,5)>s.Rational(1,2)
record={'status':'PASS','exact_observation_patterns':checked,'subdivided_oriented_graphs':30,'features':['loops','parallel edges','theta cores','K4','K3,3','path row signs','core ranks and bounds','all observed','none observed','TU elimination coefficients','forest completion','worked K4 symbolic balances and McCormick gap']}
Path(__file__).with_name('result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
