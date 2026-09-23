"""Reviewer 2 independent exact checks; no author implementation imports."""
import itertools as it
import json, math, random
from pathlib import Path
import sympy as S
import numpy as np
from scipy.optimize import linprog

OUT=Path(__file__).parent
rng=random.Random(80802)
counts={}

def primitive(v):
    den=S.ilcm(*[x.q for x in v]) if len(v)>1 else v[0].q
    a=[int(x*den) for x in v]
    g=math.gcd(*a)
    a=tuple(x//g for x in a)
    return a if next(x for x in a if x)>0 else tuple(-x for x in a)

def bases(M):
    ans=[]
    for ix in it.combinations(range(M.rows),M.cols):
        B=M[list(ix),:]
        if B.det(): ans.append((ix,B.inv()))
    return ans

def vertices(M,b,bs):
    ans=set()
    for ix,inv in bs:
        v=inv*b[list(ix),:]
        if all(x<=y for x,y in zip(M*v,b)): ans.add(tuple(v))
    return [S.Matrix(v) for v in ans]

def circuits(M):
    ans=[]
    for k in range(2,M.cols+2):
        for ix in it.combinations(range(M.rows),k):
            ns=M[list(ix),:].T.nullspace()
            if len(ns)==1 and all(x!=0 for x in ns[0]):
                q=primitive(ns[0])
                if min(q)>0: ans.append((ix,q))
    return ans

for name,C in [('cycle',S.Matrix([[1]])),('theta',S.Matrix([[1,0],[0,1],[1,1]])),
               ('k4',S.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]]))]:
    s=C.cols
    M=S.Matrix(sorted(set(tuple(sign*x for x in C.row(i)) for i in range(C.rows) for sign in (-1,1))))
    bs=bases(M); cs=circuits(M)
    assert all(all(q==1 for q in weights) for _,weights in cs)
    directions={(1,)} if s==1 else {primitive(M[list(ix),:].nullspace()[0]) for ix in it.combinations(range(M.rows),s-1) if M[list(ix),:].rank()==s-1}
    assert all(abs(x)<=1 for d in directions for x in d)
    assert all(abs(x)<=1 for d in directions for x in M*S.Matrix(d))
    D=S.Matrix(sorted(directions))
    ray0={(1,)} if s==1 else {primitive(D[list(ix),:].nullspace()[0]) for ix in it.combinations(range(D.rows),s-1) if D[list(ix),:].rank()==s-1}
    rays=sorted(ray0|{tuple(-x for x in h) for h in ray0})
    H=1 if s<=2 else math.floor((s-1)**((s-1)/2))
    duals={}
    for h in rays:
        duals[h]=[]
        assert max(map(abs,h))<=H
        for ix,inv in bs:
            q=inv.T*S.Matrix(h)
            if min(q)>=0:
                assert all(v.q==1 and v<=H for v in q)
                duals[h].append((ix,q))
        assert duals[h]
    N=S.Matrix(list(map(tuple,M.tolist()))+[tuple(-x for x in h) for h in rays])
    nb=bases(N)
    supports_checked=0; recovered=0; local_tests=0
    for trial in range(12):
        gammas=[]; witnesses=[]; supports=[]
        for j in range(3):
            v=S.Matrix([S.Rational(rng.randrange(-3,4),7) for _ in range(s)])
            b=M*v+S.Matrix([S.Rational(rng.randrange(0,5),5) for _ in range(M.rows)])
            # Include point states and exact coordinate faces.
            if trial%4==0 and j==0: b=M*v
            gammas.append(b); witnesses.append(v)
            vs=vertices(M,b,bs)
            assert vs
            sj={}
            for h in rays:
                primal=max(S.Matrix(h).dot(z) for z in vs)
                dual=min(q.dot(b[list(ix),:]) for ix,q in duals[h])
                assert primal==dual
                sj[h]=dual; supports_checked+=1
            supports.append(sj)
        t=sum(witnesses,S.zeros(s,1))
        for j,b in enumerate(gammas):
            rhs=b.col_join(S.Matrix([sum(sup[h] for sup in supports[j+1:])-S.Matrix(h).dot(t) for h in rays]))
            found=None
            for ix,inv in nb:
                z=inv*rhs[list(ix),:]
                if all(x<=y for x,y in zip(N*z,rhs)):
                    found=z; break
            assert found is not None
            assert all(x<=y for x,y in zip(M*found,b))
            t-=found; recovered+=1
        assert t==S.zeros(s,1)
    for trial in range(80):
        b=S.Matrix([S.Rational(rng.randrange(-4,6),3) for _ in range(M.rows)])
        exact=all(sum(q*b[i] for i,q in zip(ix,qs))>=0 for ix,qs in cs)
        numerical=linprog(np.zeros(s),A_ub=np.array(M,float),b_ub=np.array(b,float).ravel(),bounds=[(None,None)]*s,method='highs')
        assert numerical.status in (0,2)
        assert exact==(numerical.status==0)
        assert exact==bool(vertices(M,b,bs))
        local_tests+=1
    counts[name]=dict(normals=M.rows,directions=len(directions),rays=len(rays),circuits=len(cs),bases=len(bs),recovery_bases=len(nb),exact_support_checks=supports_checked,recovered_states=recovered,local_feasibility_checks=local_tests)
    print(name,counts[name],flush=True)

# Five-product K4: directly verify every state-flow certificate on a grid.
C=S.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
arcs=[(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
A=S.zeros(4,6)
for e,(a,b) in enumerate(arcs): A[a,e]=-1; A[b,e]=1
assert A*C==S.zeros(4,3)
v=S.Matrix([S.Rational(1,2)]*3+[S.Rational(1,4),S.Rational(1,2),S.Rational(1,2)])
agg=S.Matrix([S.Rational(1,6),S.Rational(1,24),S.Rational(1,8)])
observations=[(0,1),(1,1),(4,1),(2,2),(3,2)]
grid=0; witnesses=0
for a,b in it.product(range(-8,9),repeat=2):
    p,q=S.Rational(a,1000),S.Rational(b,1000)
    vals=[p+S.Rational(1,6),q+S.Rational(1,6),S.Rational(1,6),S.Rational(1,6),S.Rational(1,12)]
    eq=[]; rhs=[]
    for j in range(3):
        for k in range(4):
            row=[0]*18; row[6*j:6*(j+1)]=list(A.row(k)); eq.append(row); rhs.append((A*v)[k]/3)
    for e in range(6):
        row=[0]*18
        for j in range(3): row[6*j+e]=1
        eq.append(row);rhs.append((v+C*agg)[e])
    for (e,j),value in zip(observations,vals):
        row=[0]*18;row[6*j+e]=1;eq.append(row);rhs.append(value)
    res=linprog(np.zeros(18),A_eq=np.array(eq,float),b_eq=np.array(rhs,float),bounds=[(0,1/3)]*18,method='highs')
    assert res.status in (0,2) and (res.status==0)==(2*p+q>=0)
    if 2*p+q>=0:
        ts=[S.Matrix([S.Rational(1,6)-p-q/2,S.Rational(1,24)-q/2,S.Rational(1,8)-p]),S.Matrix([p,q,p]),S.Matrix([q/2,-q/2,0])]
        fs=[v/3+C*t for t in ts]
        assert sum(ts,S.zeros(3,1))==agg
        assert all(0<=x<=S.Rational(1,3) for f in fs for x in f)
        assert all(A*f==A*v/3 for f in fs)
        assert all(fs[j][e]==value for (e,j),value in zip(observations,vals))
        witnesses+=1
    grid+=1
counts['k4_section']=dict(grid=grid,exact_witnesses=witnesses)
for m,expected in [(1,1),(2,5),(3,16)]:
    rows=set(it.product((0,1),repeat=m))-{(0,)*m}
    rows|={tuple(-int(i==j) for i in range(m)) for j in range(m)}|{(-1,)*m}
    cs=circuits(S.Matrix(sorted(rows)))
    assert len(cs)==expected
    counts['chain_m'+str(m)]=dict(normals=len(rows),circuits=len(cs),maximum_weight=max(max(q) for _,q in cs))
OUT.joinpath('independent-results.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
