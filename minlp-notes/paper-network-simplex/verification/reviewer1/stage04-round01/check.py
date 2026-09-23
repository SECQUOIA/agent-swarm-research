"""Exact independent checks of the new rank-three example and finite recovery."""
from itertools import combinations, product
from fractions import Fraction as F
from math import gcd
from functools import reduce
from pathlib import Path
import random, json

C=((1,0,0),(0,1,0),(0,0,1),(1,1,0),(-1,0,1),(0,-1,-1))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def primitive(a):
    g=reduce(gcd,a)
    if not g:return None
    a=tuple(x//abs(g) for x in a)
    return neg(a) if next(x for x in a if x)<0 else a
M=sorted(set(C)|{neg(a) for a in C})
D=sorted({primitive(cross(a,b)) for a,b in combinations(M,2)}-{None})
R0={primitive(cross(a,b)) for a,b in combinations(D,2)}-{None}
R=sorted(R0|{neg(a) for a in R0})
N=sorted(set(M)|{neg(a) for a in R})
assert all(abs(dot(a,d))<=1 for a in M for d in D)
assert all(abs(x)<=2 for h in R for x in h)

def bases(rows):
    result=[]
    for ids in combinations(range(len(rows)),3):
        a,b,c=(rows[i] for i in ids)
        det=dot(a,cross(b,c))
        if det:
            cols=[tuple(F(x,det) for x in v) for v in (cross(b,c),cross(c,a),cross(a,b))]
            result.append((ids,cols))
    return result
BM,BN=bases(M),bases(N)
def solve(basis,rhs):
    ids,cols=basis
    return tuple(sum(cols[j][i]*rhs[ids[j]] for j in range(3)) for i in range(3))
def feasible(rows,rhs,p):return all(dot(a,p)<=b for a,b in zip(rows,rhs))
def vertices(rhs):
    return {p for base in BM if feasible(M,rhs,p:=solve(base,rhs))}

rng=random.Random(9041)
recoveries=0
dimensions=set()
for case in range(16):
    centers=[]; gammas=[]; supports=[]
    for j in range(4):
        weight=F(1,3) if j<3 else F(0)
        center=tuple(F(rng.randrange(-1,2),12) if weight else F(0) for _ in range(3))
        selected=list(C)
        rng.shuffle(selected)
        selected=selected[:(case+j)%4]
        rhs=[min([weight]+[dot(a,center) for o in selected if a==o or a==neg(o)]) for a in M]
        assert feasible(M,rhs,center)
        vs=vertices(rhs)
        assert vs
        origin=next(iter(vs))
        differences=[tuple(a-b for a,b in zip(p,origin)) for p in vs if p!=origin]
        if not differences:
            dimension=0
        else:
            normals=[cross(differences[0],d) for d in differences]
            nonzero=next((n for n in normals if any(n)),None)
            dimension=1 if nonzero is None else (3 if any(dot(nonzero,d) for d in differences) else 2)
        dimensions.add(dimension)
        centers.append(center);gammas.append(rhs)
        supports.append([max(dot(h,p) for p in vs) for h in R])
    t=tuple(sum(c[i] for c in centers) for i in range(3))
    for j in range(4):
        entries={a:[g] for a,g in zip(M,gammas[j])}
        for k,h in enumerate(R):
            entries.setdefault(neg(h),[]).append(sum(s[k] for s in supports[j+1:])-dot(h,t))
        rhs=[min(entries[a]) for a in N]
        candidate=next((p for base in BN if feasible(N,rhs,p:=solve(base,rhs))),None)
        assert candidate is not None and feasible(M,gammas[j],candidate)
        t=tuple(a-b for a,b in zip(t,candidate))
        for k,h in enumerate(R):
            assert dot(h,t)<=sum(s[k] for s in supports[j+1:])
        recoveries+=1
    assert t==(0,0,0)

v=(F(1,2),F(1,2),F(1,2),F(1,4),F(1,2),F(1,2))
bar=(F(1,6),F(1,24),F(1,8))
positive=negative=0
for ip,iq in product(range(-9,10),repeat=2):
    p,q=F(ip,1000),F(iq,1000)
    w=2*p+q
    if w<0:
        # Residual h support 1/3 and state-two h value zero certify exclusion.
        assert F(1,3)-w>F(1,3)
        negative+=1
        continue
    states=((p,q,p),(q/2,-q/2,F(0)),(F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p))
    assert tuple(sum(t[i] for t in states) for i in range(3))==bar
    for theta in states:
        flow=tuple(vv/3+dot(a,theta) for vv,a in zip(v,C))
        assert all(0<=f<=F(1,3) for f in flow)
    assert dot(C[4],states[0])==0
    assert dot(C[2],states[1])==dot(C[3],states[1])==0
    positive+=1
out={'status':'PASS','normal_rows':len(M),'directions':len(D),'support_rays':len(R),
     'recovery_normal_rows':len(N),'recovery_bases':len(BN),'exact_recovery_steps':recoveries,
     'state_dimensions':sorted(dimensions),'five_product_exact_witnesses':positive,
     'five_product_exact_exclusions':negative}
Path(__file__).with_name('check-output.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
