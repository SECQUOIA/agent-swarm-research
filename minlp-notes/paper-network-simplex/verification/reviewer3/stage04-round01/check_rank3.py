"""Independent exact checks of the transformed-ray bound and new K4 section."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from functools import reduce
from pathlib import Path
import json
import random
import sympy as s

C = s.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
M = s.Matrix(sorted(set(tuple(sign*x for x in C.row(i)) for sign in [-1,1] for i in range(6))))
def primitive(v):
    g = reduce(gcd, (abs(int(x)) for x in v))
    if not g:
        return None
    out = tuple(int(x)//g for x in v)
    return out if next(x for x in out if x) > 0 else tuple(-x for x in out)
D = set()
for i,j in combinations(range(M.rows),2):
    v = primitive(M.row(i).cross(M.row(j)))
    if v:
        D.add(v)
for d in D:
    assert all(x in [-1,0,1] for x in d)
    assert all(x in [-1,0,1] for x in M*s.Matrix(d))
R = set()
for d,e in combinations(D,2):
    v = primitive(s.Matrix(d).cross(s.Matrix(e)))
    if v:
        R.add(v)
        R.add(tuple(-x for x in v))
assert all(abs(x)<=2 for h in R for x in h)
checks = dict(normals=M.rows, directions=len(D), support_rays=len(R),
              transformed_vectors=0, nonnegative_support_vectors=0,
              feasible_section_witnesses=0, negative_section_certificates=0)
for rows in combinations(range(M.rows),3):
    B = M[list(rows),:]
    if not B.det():
        continue
    assert abs(B.det()) == 1
    inv = B.T.inv()
    for h in R:
        q = inv*s.Matrix(h)
        assert all(x.q==1 and abs(x)<=2 for x in q)
        assert reduce(gcd,(abs(int(x)) for x in q))==1
        checks['transformed_vectors'] += 1
        checks['nonnegative_support_vectors'] += all(x>=0 for x in q)

v = [F(1,2),F(1,2),F(1,2),F(1,4),F(1,2),F(1,2)]
aggregate = [F(1,6),F(1,24),F(1,8)]
def arcs(theta):
    return [sum(int(C[e,i])*theta[i] for i in range(3)) for e in range(6)]
for pi in range(-18,19):
    for qi in range(-18,19):
        p,q = F(pi,1920), F(qi,1920)
        w = 2*p+q
        if w < 0:
            # Residual support must be 1/3-w, above its certified upper bound.
            assert sum(aggregate)-sum([p,q,p]) > F(1,3)
            checks['negative_section_certificates'] += 1
            continue
        states = [[p,q,p],[q/2,-q/2,F(0)],
                  [F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p]]
        assert [sum(t[i] for t in states) for i in range(3)] == aggregate
        flows=[]
        for theta in states:
            flow = [v[e]/3+a for e,a in enumerate(arcs(theta))]
            assert all(0<=x<=F(1,3) for x in flow)
            flows.append(flow)
        assert flows[0][0] == p+F(1,6)
        assert flows[0][1] == q+F(1,6)
        assert flows[0][4] == F(1,6)
        assert flows[1][2] == F(1,6)
        assert flows[1][3] == F(1,12)
        checks['feasible_section_witnesses'] += 1

# Independently exercise the newly added general finite-basis recovery.
def dot(a,b):
    return sum(x*y for x,y in zip(a,b))
def bases(normals):
    out=[]
    for idx in combinations(range(len(normals)),3):
        B=s.Matrix([normals[i] for i in idx])
        if B.det():
            inv=B.inv()
            out.append((idx,[[F(int(inv[i,j].p),int(inv[i,j].q)) for j in range(3)] for i in range(3)]))
    return out
def vertices(normals,library,rhs,first=False):
    out=set()
    for idx,inv in library:
        x=tuple(dot(row,[rhs[i] for i in idx]) for row in inv)
        if all(dot(n,x)<=b for n,b in zip(normals,rhs)):
            if first:
                return x
            out.add(x)
    assert out
    return out
normals=[tuple(int(x) for x in M.row(i)) for i in range(M.rows)]
recovery_normals=sorted(set(normals)|R)
base_library=bases(normals)
recovery_library=bases(recovery_normals)
rng=random.Random(14009)
checks['recovery_models']=0
checks['recovered_states']=0
checks['zero_weight_recovered_states']=0
for trial in range(10):
    size=1+trial%5
    raw=[rng.randrange(4) for _ in range(size)]
    raw[0]=max(1,raw[0])
    weights=[F(a,sum(raw)) for a in raw]
    known=[tuple(lam*F(rng.randrange(-2,3),16) for _ in range(3)) for lam in weights]
    state_rhs=[]
    supports=[]
    for lam,theta in zip(weights,known):
        gamma={n:lam/2 for n in normals}
        for e in range(6):
            if rng.randrange(3)==0:
                row=tuple(int(x) for x in C.row(e))
                neg=tuple(-x for x in row)
                gamma[row]=min(gamma[row],dot(row,theta))
                gamma[neg]=min(gamma[neg],dot(neg,theta))
        rhs=[gamma[n] for n in normals]
        V=vertices(normals,base_library,rhs)
        state_rhs.append(rhs)
        supports.append({h:max(dot(h,x) for x in V) for h in R})
    remainder=tuple(sum(x[i] for x in known) for i in range(3))
    recovered=[]
    for i in range(size):
        rhs=dict(zip(normals,state_rhs[i]))
        for h in R:
            n=tuple(-x for x in h)
            b=sum(supports[j][h] for j in range(i+1,size))-dot(h,remainder)
            rhs[n]=min(rhs.get(n,b),b)
        x=vertices(recovery_normals,recovery_library,[rhs[n] for n in recovery_normals],first=True)
        assert all(dot(n,x)<=b for n,b in zip(normals,state_rhs[i]))
        if not weights[i]:
            assert x==(0,0,0)
            checks['zero_weight_recovered_states']+=1
        recovered.append(x)
        remainder=tuple(a-b for a,b in zip(remainder,x))
        checks['recovered_states']+=1
    assert remainder==(0,0,0)
    checks['recovery_models']+=1
Path(__file__).with_suffix('.json').write_text(json.dumps(checks,indent=2)+'\n')
print(checks)
