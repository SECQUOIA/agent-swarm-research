"""Independent bounded-rank audit. Imports no manuscript/author implementation."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm
from functools import reduce
from pathlib import Path
import json
import random

def dot(a, b):
    return sum((x*y for x,y in zip(a,b)), F(0))

def det(a):
    if not a: return 1
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))

def inv(a):
    d = det(a)
    if not d: return None
    n = len(a)
    return tuple(tuple(F((-1)**(i+j)*det([[a[k][l] for l in range(n) if l != i]
                                       for k in range(n) if k != j]), d)
                       for j in range(n)) for i in range(n))

def primitive(v):
    den = lcm(*(x.denominator if isinstance(x,F) else 1 for x in v))
    v = tuple(int(x*den) for x in v)
    g = reduce(gcd, (abs(x) for x in v))
    if not g: return None
    v = tuple(x//g for x in v)
    return v if next(x for x in v if x) > 0 else tuple(-x for x in v)

def orthogonal(rows, s):
    return primitive(tuple((-1)**j*det([list(r[:j]+r[j+1:]) for r in rows]) for j in range(s)))

def make_library(c):
    s = len(c[0])
    m = sorted(set(c) | {tuple(-x for x in r) for r in c})
    bases = []
    for ix in combinations(range(len(m)),s):
        b = [list(m[i]) for i in ix]
        bi = inv(b)
        if bi is not None:
            assert abs(det(b)) == 1
            bases.append((ix,bi))
    directions = {orthogonal(rows,s) for rows in combinations(m,s-1)} - {None}
    assert all(all(abs(x)<=1 for x in d) and all(abs(dot(a,d))<=1 for a in m) for d in directions)
    rays = {orthogonal(rows,s) for rows in combinations(sorted(directions),s-1)} - {None}
    rays |= {tuple(-x for x in h) for h in rays}
    rays = sorted(rays)
    H = (1,1,2,5)[s-1]
    duals = []
    for h in rays:
        assert all(abs(x)<=H for x in h)
        entries = []
        for ix,bi in bases:
            q = tuple(dot(col,h) for col in zip(*bi))
            if min(q)>=0:
                assert all(x.denominator==1 and x<=H for x in q)
                entries.append((ix,q))
        assert entries
        duals.append(entries)
    circuits = []
    for k in range(2,s+2):
        for ix in combinations(range(len(m)),k):
            a = [m[i] for i in ix]
            q = None
            for cols in combinations(range(s),k-1):
                q = primitive(tuple((-1)**i*det([[a[j][l] for l in cols] for j in range(k) if j!=i])
                                    for i in range(k)))
                if q is not None: break
            if q and min(q)>0 and all(dot(q,[a[i][j] for i in range(k)])==0 for j in range(s)):
                assert set(q)=={1}
                circuits.append(ix)
    return m,bases,rays,duals,circuits,len(directions)

def vertices(m,bases,gamma):
    result = set()
    for ix,bi in bases:
        v = tuple(dot(row,[gamma[i] for i in ix]) for row in bi)
        if all(dot(a,v)<=b for a,b in zip(m,gamma)): result.add(v)
    return sorted(result)

def recover(m,rays,domains,all_vertices,target):
    normals = sorted(set(m)|{tuple(-x for x in h) for h in rays})
    s = len(m[0]); bases = []
    for ix in combinations(range(len(normals)),s):
        bi = inv([list(normals[i]) for i in ix])
        if bi is not None: bases.append((ix,bi))
    remaining = target; result=[]; attempts=0
    supports = [[max(dot(h,v) for v in vv) for h in rays] for vv in all_vertices]
    for j,gamma in enumerate(domains):
        rhs = dict(zip(m,gamma))
        for hi,h in enumerate(rays):
            normal = tuple(-x for x in h)
            value = sum((ss[hi] for ss in supports[j+1:]),F(0))-dot(h,remaining)
            rhs[normal] = min(rhs.get(normal,value),value)
        for ix,bi in bases:
            attempts+=1
            v = tuple(dot(row,[rhs[normals[i]] for i in ix]) for row in bi)
            if all(dot(n,v)<=rhs[n] for n in normals): break
        else: raise AssertionError('No recovery basis')
        assert all(dot(a,v)<=b for a,b in zip(m,gamma))
        remaining=tuple(a-b for a,b in zip(remaining,v))
        assert all(dot(h,remaining)<=sum((ss[hi] for ss in supports[j+1:]),F(0)) for hi,h in enumerate(rays))
        result.append(v)
    assert not any(remaining)
    return len(result), attempts, max(max(x.numerator.bit_length(),x.denominator.bit_length()) for v in result for x in v)

rng = random.Random(9032)
summary = {}
configs = {
    'theta': ((1,0),(0,1),(1,1)),
    'K4': ((1,0,0),(0,1,0),(0,0,1),(1,1,0),(-1,0,1),(0,-1,-1)),
    'rank4': ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(-1,0,1,1),(0,-1,-1,0),(0,0,0,-1)),
}
for name,c in configs.items():
    m,bases,rays,duals,circuits,nd=make_library(c)
    s=len(c[0]); out=dict(normals=len(m),bases=len(bases),directions=nd,rays=len(rays),circuits=len(circuits))
    out.update(support_checks=0,feasibility_checks=0,recovered_states=0,recovery_attempts=0,max_output_bits=0)
    for case in range(15 if s<4 else 4):
        gamma=[F(rng.randint(-2,3),rng.randint(1,5)) for _ in m]
        vv=vertices(m,bases,gamma)
        assert bool(vv)==all(sum(gamma[i] for i in ix)>=0 for ix in circuits)
        out['feasibility_checks']+=1
    for case in range(7 if s<4 else 2):
        domains=[]; vs=[]; target=[F(0)]*s
        for state in range(1+(case%5)):
            center=tuple(F(rng.randint(-3,3),rng.randint(2,7)) for _ in range(s))
            gamma=[dot(a,center)+F(rng.randrange(4),rng.randint(2,7)) for a in m]
            # Force points and lower-dimensional slices by paired coordinate rows.
            for d in range(s if (case+state)%4==0 else (case+state)%s):
                for sign in (-1,1):
                    a=tuple(sign*(i==d) for i in range(s));gamma[m.index(a)]=dot(a,center)
            vv=vertices(m,bases,gamma); assert vv
            for h,dd in zip(rays,duals):
                assert max(dot(h,v) for v in vv)==min(dot(q,[gamma[i] for i in ix]) for ix,q in dd)
                out['support_checks']+=1
            witness=tuple((vv[0][i]+vv[-1][i])/2 for i in range(s))
            target=[a+b for a,b in zip(target,witness)]
            domains.append(gamma);vs.append(vv)
        if s<4:
            n,a,b=recover(m,rays,domains,vs,tuple(target))
            out['recovered_states']+=n;out['recovery_attempts']+=a;out['max_output_bits']=max(out['max_output_bits'],b)
    if s<4:
        # Long degenerate sum: zero state plus 24 parallel segments.
        domains=[];vs=[]
        for j in range(25):
            width=F(j,7*(j+1))
            gamma=[abs(a[0])*width for a in m]
            vv=vertices(m,bases,gamma)
            assert len(vv)==(1 if j==0 else 2)
            domains.append(gamma);vs.append(vv)
        n,a,b=recover(m,rays,domains,vs,(F(0),)*s)
        out['recovered_states']+=n;out['recovery_attempts']+=a;out['max_output_bits']=max(out['max_output_bits'],b)
        out['long_degenerate_state_sequence']=25
    summary[name]=out
    print(name,out,flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps(summary,indent=2)+'\n')
