"""Reviewer 2: integrity and constructive rational fractional-arc perturbation."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, random
import sympy as sp
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
manifest=json.loads((root/'paper-network-simplex/verification/stage07-validation.json').read_text())['sha256']
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
snap=root/'paper-network-simplex/process/snapshots/stage07-round01'
sm=json.loads((snap/'manifest.json').read_text())
assert all(hashlib.sha256((snap/p).read_bytes()).hexdigest()==h for p,h in sm.items())
rng=random.Random(777922)
leaves=0
maxterms=0
for case in range(24):
    arcs=[(0,1),(1,0),(1,2),(2,1),(2,0),(0,2),(0,0),(2,2)]
    generators=[(1,1,0,0,0,0,0,0),(0,0,1,1,0,0,0,0),(0,0,0,0,1,1,0,0),(1,0,1,0,1,0,0,0),(0,1,0,1,0,1,0,0),(0,0,0,0,0,0,1,0),(0,0,0,0,0,0,0,1)]
    ref=[rng.randrange(2) for e in arcs]
    points=[]
    for j in range(4):
        point=ref[:]
        for g in rng.sample(generators,3): point=[a+b for a,b in zip(point,g)]
        points.append(point)
    u=[max(p[e] for p in points)+rng.randrange(2) for e in range(len(arcs))]
    for e,(a,b) in enumerate(arcs):
        if rng.randrange(2):
            arcs[e]=(b,a)
            for p in points:p[e]=u[e]-p[e]
    A=sp.zeros(4,len(arcs)) # Includes isolated vertex.
    for e,(a,b) in enumerate(arcs):A[a,e]-=1;A[b,e]+=1
    balance=A*sp.Matrix(points[0])
    assert all(A*sp.Matrix(p)==balance for p in points)
    x=tuple(sum(F(j+1,10)*p[e] for j,p in enumerate(points)) for e in range(len(arcs)))
    def refine(x):
        frac=[e for e,a in enumerate(x) if a.denominator!=1]
        if not frac:return [(F(1),x)]
        d=A[:,frac].nullspace()[0]
        direction=[F(0)]*len(arcs)
        for e,a in zip(frac,d):direction[e]=F(a)
        stepplus=[];stepminus=[]
        for e in frac:
            a=direction[e]
            if a:
                lower=x[e].numerator//x[e].denominator
                if a>0:stepplus.append((lower+1-x[e])/a);stepminus.append((x[e]-lower)/a)
                else:stepplus.append((x[e]-lower)/(-a));stepminus.append((lower+1-x[e])/(-a))
        t,s=min(stepplus),min(stepminus)
        xp=tuple(a+t*d for a,d in zip(x,direction));xm=tuple(a-s*d for a,d in zip(x,direction))
        assert sum(a.denominator!=1 for a in xp)<len(frac)
        assert sum(a.denominator!=1 for a in xm)<len(frac)
        return [(s/(s+t)*w,p) for w,p in refine(xp)]+[(t/(s+t)*w,p) for w,p in refine(xm)]
    terms=refine(x)
    assert sum(w for w,p in terms)==1
    assert all(sum(w*p[e] for w,p in terms)==x[e] for e in range(len(arcs)))
    for w,p in terms:
        assert all(a.denominator==1 and 0<=a<=u[e] for e,a in enumerate(p))
        assert A*sp.Matrix(p)==balance
    leaves+=len(terms);maxterms=max(maxterms,len(terms))
result={'status':'PASS','validation_hashes':len(manifest),'snapshot_hashes':len(sm),'rational_cycle_refinement_cases':24,'integer_decomposition_terms':leaves,'max_terms':maxterms,'method':'Exact rational nullspace perturbations between consecutive integer bounds; not LP.'}
(out/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
