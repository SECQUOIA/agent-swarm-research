"""Independent Fraction checks of the new K4 section and finite-basis recovery."""
from fractions import Fraction as F
from itertools import combinations, product
from functools import reduce
from math import gcd
from pathlib import Path
import json
import random

C = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(-1,0,1),(0,-1,-1)]
dot = lambda a,b: sum(x*y for x,y in zip(a,b))
neg = lambda a: tuple(-x for x in a)
cross = lambda a,b: (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def primitive(a):
    g = reduce(gcd, a)
    return tuple(x//g for x in a) if g else None


def bases(rows):
    ans=[]
    for ids in combinations(range(len(rows)),3):
        a,b,c=(rows[i] for i in ids)
        det=dot(a,cross(b,c))
        if det:
            cof=[cross(b,c),cross(c,a),cross(a,b)]
            inv=tuple(tuple(F(cof[j][i],det) for j in range(3)) for i in range(3))
            ans.append((ids,inv))
    return ans


def feasible_vertex(rows,rhs,library):
    for ids,inv in library:
        p=tuple(dot(row,[rhs[i] for i in ids]) for row in inv)
        if all(dot(row,p)<=v for row,v in zip(rows,rhs)):
            return p
    raise AssertionError("No feasible vertex")


M=sorted(set(C+[neg(c) for c in C]))
D=set()
for a,b in combinations(M,2):
    d=primitive(cross(a,b))
    if d:
        D.add(min(d,neg(d)))
assert all(dot(a,d) in (-1,0,1) for a in M for d in D)
R=set()
for a,b in combinations(D,2):
    h=primitive(cross(a,b))
    if h:
        R.update((h,neg(h)))
R=sorted(R)
assert all(abs(x)<=2 for h in R for x in h)
mb=bases(M)
for ids,inv in mb:
    for h in R:
        q=tuple(sum(inv[j][i]*h[j] for j in range(3)) for i in range(3))
        if all(x>=0 for x in q):
            assert all(x.denominator==1 and x<=2 for x in q)
N=M+[neg(h) for h in R]
nb=bases(N)
rng=random.Random(4410)
counts={"K4_directions":len(D),"K4_rays":len(R),"K4_normal_bases":len(mb),
        "recovery_bases_with_duplicate_normals":len(nb),"recovery_states":0,
        "new_K4_grid_witnesses":0,"new_K4_grid_exclusions":0}
for trial in range(12):
    states=[]
    for j in range(1+trial%5):
        # Includes point states and various lower-dimensional slices at zero.
        rhs=[F(rng.randrange(5),7) for _ in M]
        if (trial+j)%4==0:
            rhs=[F(0) for _ in M]
        vs=set()
        for ids,inv in mb:
            p=tuple(dot(row,[rhs[i] for i in ids]) for row in inv)
            if all(dot(row,p)<=v for row,v in zip(M,rhs)):
                vs.add(p)
        assert vs
        support=[max(dot(h,p) for p in vs) for h in R]
        states.append((rhs,support,rng.choice(sorted(vs))))
    rem=tuple(sum(st[2][k] for st in states) for k in range(3))
    for j,(rhs,support,_) in enumerate(states):
        suffix=[sum(st[1][k] for st in states[j+1:]) for k in range(len(R))]
        next_rhs=rhs+[s-dot(h,rem) for h,s in zip(R,suffix)]
        p=feasible_vertex(N,next_rhs,nb)
        rem=tuple(x-y for x,y in zip(rem,p))
        assert all(dot(h,rem)<=s for h,s in zip(R,suffix))
        counts["recovery_states"]+=1
    assert rem==(0,0,0)

v=(F(1,2),F(1,2),F(1,2),F(1,4),F(1,2),F(1,2))
bar=(F(1,6),F(1,24),F(1,8))
assert tuple(v[e]+dot(C[e],bar) for e in range(6))==(F(2,3),F(13,24),F(5,8),F(11,24),F(11,24),F(1,3))
# Exact residual support certificate: C_12 - C_03 = (1,1,1).
assert tuple(C[0][k]-C[5][k] for k in range(3))==(1,1,1)
assert (1-v[0])/3+v[5]/3==F(1,3)==sum(bar)
for a,b in product(range(-15,16),repeat=2):
    p,q=F(a,1536),F(b,1536)
    w=2*p+q
    if w<0:
        # State 1 has h-value w; state 2 has zero h-value. Sum forces
        # residual h-value 1/3-w, strictly above its certified bound 1/3.
        assert sum(bar)-w>F(1,3)
        counts["new_K4_grid_exclusions"]+=1
        continue
    th=[(F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p),(p,q,p),(q/2,-q/2,F(0))]
    assert tuple(sum(t[k] for t in th) for k in range(3))==bar
    flows=[tuple(v[e]/3+dot(C[e],t) for e in range(6)) for t in th]
    assert all(0<=f<=F(1,3) for row in flows for f in row)
    assert flows[1][0]==F(1,6)+p and flows[1][1]==F(1,6)+q
    assert flows[1][4]==flows[2][2]==F(1,6) and flows[2][3]==F(1,12)
    counts["new_K4_grid_witnesses"]+=1
counts["status"]="PASS"
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts))
