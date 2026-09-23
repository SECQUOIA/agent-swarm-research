"""Independent exact rank-three library construction and suffix recovery."""
import itertools
import json
import math
import random
from pathlib import Path
import sympy as s
rng=random.Random(49127)
C=s.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
rows=sorted(set(tuple(sign*t for t in C[i,:]) for i in range(6) for sign in [-1,1]))
M=s.Matrix(rows)
def primitive(v):
    vals=[int(t) for t in v]
    gcd=math.gcd(*vals)
    vals=[t//gcd for t in vals]
    if next(t for t in vals if t)!=abs(next(t for t in vals if t)): vals=[-t for t in vals]
    return tuple(vals)
D=set()
for a,b in itertools.combinations(rows,2):
    v=s.Matrix(a).cross(s.Matrix(b))
    if v!=s.zeros(3,1): D.add(primitive(v))
assert all(t in [-1,0,1] for d in D for t in list(d)+list(M*s.Matrix(d)))
R=set()
for a,b in itertools.combinations(D,2):
    v=s.Matrix(a).cross(s.Matrix(b))
    if v!=s.zeros(3,1):
        p=primitive(v); R.add(p); R.add(tuple(-t for t in p))
R=sorted(R)
assert max(abs(t) for h in R for t in h)<=2
basis=[]
for indices in itertools.combinations(range(M.rows),3):
    B=M[list(indices),:]
    if B.det():
        assert abs(B.det())==1
        basis.append((indices,B.inv()))
dual={}
maxq=0
for h in R:
    options=[]
    for indices,inv in basis:
        q=inv.T*s.Matrix(h)
        if min(q)>=0:
            assert all(t.q==1 and 0<=t<=2 for t in q)
            maxq=max(maxq,max(q)); options.append((indices,q))
    assert options
    dual[h]=options
N=s.Matrix(sorted(set(rows+R)))
recovery_bases=[]
for indices in itertools.combinations(range(N.rows),3):
    B=N[list(indices),:]
    if B.det(): recovery_bases.append((indices,B.inv()))
recoveries=0
for case in range(12):
    domains=[]; known=[]
    for j in range(3):
        center=s.Matrix([s.Rational(rng.randrange(-3,4),7) for i in range(3)])
        slack=s.Matrix([0 if case%4==0 else s.Rational(rng.randrange(3),5) for a in rows])
        gamma=M*center+slack
        domains.append(gamma); known.append(center)
    support=[]
    for gamma in domains:
        sh={}
        for h,options in dual.items():
            sh[h]=min((q.T*gamma[list(indices),0])[0] for indices,q in options)
        support.append(sh)
    remaining=sum(known,s.zeros(3,1))
    for j,gamma in enumerate(domains):
        rhs=[]
        for normal in map(tuple,N.tolist()):
            candidates=[]
            if normal in rows: candidates.append(gamma[rows.index(normal)])
            # -h.theta <= suffix(h)-h.remaining, normal=-h
            h=tuple(-t for t in normal)
            if h in R: candidates.append(sum(sh[h] for sh in support[j+1:])-(s.Matrix(h).T*remaining)[0])
            rhs.append(min(candidates))
        rhs=s.Matrix(rhs)
        for indices,inv in recovery_bases:
            candidate=inv*rhs[list(indices),0]
            if all(t<=0 for t in N*candidate-rhs): break
        else: raise AssertionError('No recovery vertex')
        assert all(t<=0 for t in M*candidate-gamma)
        remaining-=candidate
        recoveries+=1
    assert remaining==s.zeros(3,1)
record={'status':'PASS','signed_normals':len(rows),'primitive_edge_directions':len(D),'support_rays':len(R),'max_nonnegative_dual_multiplier':int(maxq),'recovery_normal_rows':N.rows,'recovery_bases':len(recovery_bases),'exact_state_recoveries':recoveries,'degenerate_cases':'Every fourth case consists of singleton states, with all bound rows tight.'}
Path(__file__).with_name('rank-result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
