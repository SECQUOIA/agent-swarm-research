"""Fresh exact checks; no manuscript verification or production imports.
Finite checks complement the proofs and do not certify arbitrary rank/size.
"""
from fractions import Fraction as F
from itertools import combinations, product
from collections import defaultdict
from pathlib import Path
import json, math
import sympy as sp

def cross(o,a,b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])

def hull(points):
    points=sorted(set(points))
    if len(points)<2: return tuple(points)
    lo=[]; hi=[]
    for chain,seq in [(lo,points),(hi,list(reversed(points)))]:
        for p in seq:
            while len(chain)>1 and cross(chain[-2],chain[-1],p)<=0: chain.pop()
            chain.append(p)
    return tuple(lo[:-1]+hi[:-1])

def vertices(bounds):
    l,u=bounds
    rows=[(1,0,u[0]),(-1,0,-l[0]),(0,1,u[1]),(0,-1,-l[1]),(1,1,u[2]),(-1,-1,-l[2])]
    out=[]
    for (a,b,c),(d,e,f) in combinations(rows,2):
        det=a*e-b*d
        if det:
            p=(F(c*e-b*f,det),F(a*f-c*d,det))
            if all(a*p[0]+b*p[1]<=c for a,b,c in rows): out.append(p)
    return hull(out)

def supports(bounds):
    l,u=bounds
    return ((max(l[0],l[2]-u[1]),max(l[1],l[2]-u[0]),max(l[2],l[0]+l[1])),
            (min(u[0],u[2]-l[1]),min(u[1],u[2]-l[0]),min(u[2],u[0]+u[1])))

def theta():
    unique={}; queries=0
    for intervals in product(list(product(range(-1,2),repeat=2)),repeat=3):
        l,u=tuple(zip(*intervals)); vv=vertices((l,u))
        pred=all(a<=b for a,b in zip(l,u)) and l[0]+l[1]<=u[2] and l[2]<=u[0]+u[1]
        assert bool(vv)==pred
        if vv:
            a,b=supports((l,u))
            assert a==tuple(min((p[0],p[1],sum(p))[k] for p in vv) for k in range(3))
            assert b==tuple(max((p[0],p[1],sum(p))[k] for p in vv) for k in range(3))
            unique[vv]=(a,b)
        queries+=1
    recoveries=0; pairs=0
    for va,vb in product(unique,repeat=2):
        ba,bb=unique[va],unique[vb]
        total=tuple(tuple(x+y for x,y in zip(a,b)) for a,b in zip(ba,bb))
        expected=hull((a[0]+b[0],a[1]+b[1]) for a,b in product(va,vb))
        assert vertices(total)==expected
        candidates=list(expected)+[(sum(p[0] for p in expected)/len(expected),sum(p[1] for p in expected)/len(expected))]
        for p in candidates:
            r=(p[0],p[1],sum(p))
            ll=tuple(max(ba[0][k],r[k]-bb[1][k]) for k in range(3))
            uu=tuple(min(ba[1][k],r[k]-bb[0][k]) for k in range(3))
            s=max(ll[0],ll[2]-uu[1]); t=max(ll[1],ll[2]-s)
            for q,bound in [((s,t,s+t),ba),((p[0]-s,p[1]-t,sum(p)-s-t),bb)]:
                assert all(a<=v<=b for a,v,b in zip(bound[0],q,bound[1]))
            recoveries+=1
        pairs+=1
    return dict(interval_triples=queries,distinct_nonempty_polygons=len(unique),exact_minkowski_pairs=pairs,recoveries=recoveries)

def circuits(m):
    pos={x for x in product((0,1),repeat=m) if any(x)}
    ns=sorted(pos|{tuple(-x for x in row) for row in pos if sum(row)==1 or sum(row)==m})
    out=[]
    for k in range(2,m+2):
        for ix in combinations(range(len(ns)),k):
            ker=sp.Matrix([ns[i] for i in ix]).T.nullspace()
            if len(ker)!=1: continue
            z=ker[0]
            if all(v<0 for v in z): z=-z
            if not all(v>0 for v in z): continue
            den=sp.ilcm(*[v.q for v in z]); weights=[int(v*den) for v in z]
            g=math.gcd(*weights); weights=[v//g for v in weights]
            out.append(dict(zip((ns[i] for i in ix),weights)))
    return ns,out

def chain():
    ns,cs=circuits(3); assert len(cs)==16
    # Check equality with the four symbolic families, not just their count.
    one=(1,1,1); negone=(-1,-1,-1)
    unit=lambda j: tuple(int(k==j) for k in range(3))
    neg=lambda a: tuple(-x for x in a)
    fam=[]
    for row in ns:
        if all(x>=0 for x in row): fam.append({row:1,**{neg(unit(j)):1 for j in range(3) if row[j]}})
    positives=[a for a in ns if min(a)>=0]
    for size in range(1,4):
        for sets in combinations(positives,size):
            if tuple(map(sum,zip(*sets)))==one: fam.append({negone:1,**{a:1 for a in sets}})
    for i in range(3):
        pairs=[tuple(int(k in (i,j)) for k in range(3)) for j in range(3) if j!=i]
        fam.append({negone:1,neg(unit(i)):1,**{a:1 for a in pairs}})
    fam.append({negone:2,**{a:1 for a in positives if sum(a)==2}})
    canonical=lambda coll:{tuple(sorted(c.items())) for c in coll}
    assert canonical(fam)==canonical(cs)
    checks=0
    for pattern in product('ABTU',repeat=3):
        rows=[]
        for a in ns: rows.append((a,{})) # zero contribution from any other gadget
        for j,kind in enumerate(pattern):
            if kind in 'AB': rows.append((neg(unit(j)),{('u' if kind=='A' else 'v')+str(j):-1}))
            if kind=='T':
                for sign in (-1,1): rows.append((tuple(sign*x for x in unit(j)),{f'u{j}':sign,f'v{j}':sign}))
        R={'xa':1}; up={'xa':-1,'xh':-1}
        for j,kind in enumerate(pattern):
            if kind in 'AT': R[f'u{j}']=-1; up[f'u{j}']=1
            if kind=='B': R[f'v{j}']=1; up[f'v{j}']=-1
        rows.extend([(tuple(int(k=='B') for k in pattern),R),(tuple(int(k in 'AT') for k in pattern),up)])
        groups=defaultdict(list)
        for n,r in rows:
            if any(n): groups[n].append(r)
            else: assert all(abs(v)<=1 for v in r.values())
        for c in cs:
            for variable in ['xa']+[a+str(j) for a in 'uv' for j in range(3)]:
                lo=sum(w*min(r.get(variable,0) for r in groups[n]) for n,w in c.items())
                hi=sum(w*max(r.get(variable,0) for r in groups[n]) for n,w in c.items())
                assert -1<=lo<=hi<=1,(pattern,c,variable,lo,hi)
                checks+=1
    repairs=defaultdict(int)
    for c in cs:
        pos=[n for n in c if min(n)>=0]
        for bits in product((0,-1),repeat=len(pos)):
            coefficient=c.get(negone,0)+sum(c[n]*b for n,b in zip(pos,bits))
            if abs(coefficient)>1:
                if coefficient==-2:
                    assert len(pos)==3 and all(sum(n)==1 for n in pos) and bits==(-1,-1,-1) and c[negone]==1
                    assert (coefficient+1,-1+1,1)==(-1,0,1)
                else:
                    assert coefficient==2 and len(pos)==3 and all(sum(n)==2 for n in pos) and bits==(0,0,0) and c[negone]==2
                    assert (coefficient-1,1-1,-1)==(1,0,-1)
                repairs[str(coefficient)]+=1
    assert dict(repairs)=={'-2':1,'2':1}
    return dict(normals=len(ns),circuits=len(cs),observation_patterns=64,coefficient_ranges=checks,bypass_exceptions=dict(repairs))

def fibonacci():
    count=0
    for q in range(3,11):
        N=2*q-1; fib=[0,1,1]
        for i in range(3,q+2): fib.append(fib[-1]+fib[-2])
        names=[('P',i) for i in range(1,q+1)]+[('H',0)]+[('H',i) for i in range(3,q+1)]
        cols=[[('H',0),('P',1)],[('H',0),('P',2)]]
        for i in range(3,q+1): cols.extend([[('H',i),('P',i)],[('H',i),('P',i-1),('P',i-2)]])
        cols.append([('P',q),('P',q-1)])
        D=sp.Matrix([[int(name in col) for col in cols] for name in names]); K=sp.ones(N)-D
        alpha=sp.Matrix([fib[i] if kind=='P' else fib[q+1]-(1 if i==0 else fib[i]) for kind,i in names])
        assert sum(D)==5*q-4 and D.det()!=0 and K.det()!=0
        assert D.T*alpha==sp.ones(N,1)*fib[q+1]
        assert K.T*alpha==sp.ones(N,1)*(sum(alpha)-fib[q+1])
        inv=K.inv(); norm=max(sum(abs(v) for v in inv.row(i)) for i in range(N))
        a=sp.Rational(1,2*N); c=a/4; R=fib[q]; eps=a/(16*(1+R)*(1+norm))
        r=q-1; s=0
        for dr,ds in [(eps/2,0),(-eps/(2*R),eps/2),(0,eps/2),(eps/4,-R*eps/4)]:
            if max(abs(dr),abs(ds))>=eps: continue
            delta=sp.zeros(N,1); delta[r]=dr; delta[s]=ds
            tau=sp.zeros(N,1); tau[s]=R*dr+ds
            assert tau[s]>=0
            w=sp.ones(N,1)*a+inv*(-delta+tau)
            assert sum(w)==sp.Rational(1,2)
            for i in range(N):
                vals=[w[j] if K[i,j] else c for j in range(N)]
                if i==r: vals[N-1]+=dr
                if i==s: vals[0]+=ds
                if i==s:
                    j=next(j for j in range(N) if K[i,j]); vals[j]-=tau[s]
                assert all(0<=v<=w[j]<=2*a for j,v in enumerate(vals))
                assert sum(vals)==sum(K.row(i))*a+(N-sum(K.row(i)))*c
            count+=1
    return dict(q_range=[3,10],exact_local_witnesses=count)

if __name__=='__main__':
    out={'theta':theta(),'chain':chain(),'fibonacci':fibonacci()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
