"""Independent constructive fractional-cycle refinement, exact arithmetic."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, random
from sympy import Matrix
rng=random.Random(7042026)
stats=dict(graphs=0,normalized_flow_refinements=0,integral_terms=0,complete_sparse_hull_mixtures=0)

def refine(arcs,A,x):
    fractional=[e for e,v in enumerate(x) if v.denominator!=1]
    if not fractional:return [(F(1),x)]
    # On the fractional support a dependence must exist. This is found by
    # exact elimination, not by consulting enumerated integral points.
    null=A[:,fractional].nullspace();assert null
    c=[F(0)]*len(x)
    for e,v in zip(fractional,null[0]):c[e]=F(v)
    assert any(c) and A*Matrix(c)==Matrix.zeros(A.rows,1)
    lo=[];hi=[]
    for e,v in enumerate(c):
        if not v:continue
        floor=x[e].numerator//x[e].denominator;ceil=floor+1
        if v>0:hi.append((ceil-x[e])/v);lo.append((x[e]-floor)/v)
        else:hi.append((x[e]-floor)/(-v));lo.append((ceil-x[e])/(-v))
    plus=min(hi);minus=min(lo);assert plus>0 and minus>0
    xp=tuple(v+plus*d for v,d in zip(x,c));xm=tuple(v-minus*d for v,d in zip(x,c))
    assert sum(v.denominator!=1 for v in xp)<len(fractional)
    assert sum(v.denominator!=1 for v in xm)<len(fractional)
    out=[(minus/(plus+minus)*a,p) for a,p in refine(arcs,A,xp)]+[(plus/(plus+minus)*a,p) for a,p in refine(arcs,A,xm)]
    assert sum(a for a,p in out)==1
    assert tuple(sum(a*p[e] for a,p in out) for e in range(len(x)))==x
    return out

for trial in range(24):
    n=4;E=6
    arcs=[(rng.randrange(n-1),rng.randrange(n-1),rng.randrange(1,3)) for _ in range(E)]
    if trial%3==0:arcs[0]=(0,0,0)
    A=Matrix.zeros(n,E)
    for e,(tail,head,u) in enumerate(arcs):A[head,e]+=1;A[tail,e]-=1
    buckets={}
    for x in product(*(range(u+1) for _,_,u in arcs)):
        b=tuple(A*Matrix(x));buckets.setdefault(b,[]).append(tuple(map(F,x)))
    b,integer=max(buckets.items(),key=lambda t:len(t[1]))
    stats['graphs']+=1
    for m in range(4):
        raw=[rng.randrange(4) for _ in range(m+1)]
        if not sum(raw):raw[-1]=1
        lam=[F(v,sum(raw)) for v in raw]
        fs=[];refinements=[]
        for j in range(m+1):
            picks=rng.choices(integer,k=3)
            f=tuple(sum(p[e]*w for p,w in zip(picks,(F(1,7),F(2,7),F(4,7)))) for e in range(E))
            terms=refine(arcs,A,f);fs.append(f);refinements.append(terms)
            for alpha,p in terms:
                assert alpha>0 and tuple(A*Matrix(p))==b
                assert all(v.denominator==1 and 0<=v<=u for v,(_,_,u) in zip(p,arcs))
            stats['normalized_flow_refinements']+=1;stats['integral_terms']+=len(terms)
        obs=[(e,j) for j in range(m) for e in range(E) if rng.random()<.5]
        point=tuple(sum(lam[j]*fs[j][e] for j in range(m+1)) for e in range(E))+tuple(lam[:m])+tuple(lam[j]*fs[j][e] for e,j in obs)
        terms=[]
        for j in range(m+1):
            if not lam[j]:continue
            y=tuple(F(j==k) for k in range(m))
            for alpha,p in refinements[j]:terms.append((lam[j]*alpha,p+y+tuple(p[e]*y[k] for e,k in obs)))
        assert sum(w for w,p in terms)==1
        assert tuple(sum(w*p[k] for w,p in terms) for k in range(len(point)))==point
        stats['complete_sparse_hull_mixtures']+=1
stats['status']='PASS'
Path(__file__).with_suffix('.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats))
