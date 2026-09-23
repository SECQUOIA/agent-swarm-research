"""Independent exact circuit and per-product branch checks for small chains."""
from itertools import combinations, product
from math import gcd, lcm
from functools import reduce
from pathlib import Path
import json
import sympy as s

def circuits(normals,m):
    out=[]
    for size in range(2,m+2):
        for ix in combinations(range(len(normals)),size):
            A=s.Matrix([normals[i] for i in ix]).T
            kernel=A.nullspace()
            if len(kernel)!=1:
                continue
            q=kernel[0]
            if all(x<0 for x in q):
                q=-q
            if not all(x>0 for x in q):
                continue
            scale=reduce(lcm,(int(x.q) for x in q),1)
            w=[int(x*scale) for x in q]
            common=reduce(gcd,w)
            out.append(tuple((normals[i],a//common) for i,a in zip(ix,w)))
    return out

counts={}
for m in range(1,4):
    subsets=[tuple(v) for v in product([0,1],repeat=m) if any(v)]
    singletons=[tuple(int(i==j) for i in range(m)) for j in range(m)]
    full=tuple([1]*m)
    normals=sorted(set(subsets+[tuple(-v for v in e) for e in singletons]+[tuple([-1]*m)]))
    cs=circuits(normals,m)
    assert len(cs)==[1,5,16][m-1]
    assert max(w for c in cs for n,w in c)==[1,1,2][m-1]
    checks=0
    for pattern in product('ABTU',repeat=m):
        rows=[]
        R=[0]*(2*m)
        for j,typ in enumerate(pattern):
            unit=singletons[j]
            if typ in 'AT':R[2*j]-=1
            if typ=='B':R[2*j+1]+=1
            if typ in 'AB':
                v=[0]*(2*m);v[2*j+int(typ=='B')]=-1
                rows.append((tuple(-x for x in unit),v))
            if typ=='T':
                v=[0]*(2*m);v[2*j]=v[2*j+1]=1
                rows.append((unit,v))
                rows.append((tuple(-x for x in unit),[-x for x in v]))
        rows.append((tuple(int(t=='B') for t in pattern),R))
        rows.append((tuple(int(t in 'AT') for t in pattern),[-x for x in R]))
        for c in cs:
            for k in range(2*m):
                # A branch chooses exactly one row from each normal group.
                # Zero also permits a row belonging to another gadget/domain.
                choices={n:[0]+[v[k] for a,v in rows if a==n] for n,w in c}
                lo=sum(w*min(choices[n]) for n,w in c)
                hi=sum(w*max(choices[n]) for n,w in c)
                assert -1<=lo<=hi<=1,(m,pattern,c,k,lo,hi)
                checks+=1
    signed=sorted(set(subsets+[tuple(-x for x in v) for v in subsets]))
    old=circuits(signed,m)
    assert len(old)==[1,5,41][m-1]
    counts[str(m)]={'reduced_normals':len(normals),'reduced_circuits':len(cs),
                    'unreduced_circuits':len(old),'product_branch_bounds':checks}
    if m==3:
        actual={frozenset(c) for c in cs}
        # Check the stated list without relying on the numerical count alone.
        expected=[]
        for S in subsets:
            expected.append(frozenset([(S,1)]+[(tuple(-x for x in singletons[j]),1)
                                             for j in range(m) if S[j]]))
        for size in range(1,4):
            for partition in combinations(subsets,size):
                if all(sum(p[j] for p in partition)==1 for j in range(3)):
                    expected.append(frozenset([(tuple([-1]*3),1)]+[(p,1) for p in partition]))
        for i in range(3):
            pairs=[tuple(int(k==i or k==j) for k in range(3)) for j in range(3) if j!=i]
            expected.append(frozenset([(tuple([-1]*3),1),(tuple(-x for x in singletons[i]),1)]+[(p,1) for p in pairs]))
        expected.append(frozenset([(tuple([-1]*3),2)]+[(p,1) for p in subsets if sum(p)==2]))
        assert actual==set(expected)
repair_checks=0
for state in range(4):
    y=[int(state==j) for j in range(1,4)]
    paths=[(1,(0,0,0),(0,0,0))]+[(0,bits,tuple(1-b for b in bits)) for bits in product([0,1],repeat=3)]
    for h,a,b in paths:
        z_a=[a[i]*y[i] for i in range(3)]
        first=3-2*h-sum(a)+sum(z_a)-sum(y)
        first_fixed=first+a[0]+b[0]+h-1
        pairs=[(0,1),(0,2),(1,2)]
        z_b_sum=sum(b[i]*y[j] for i,js in enumerate(pairs) for j in js)
        second=sum(a)+z_b_sum+2*h-2*sum(y)
        second_fixed=second-a[0]-b[0]-h+1
        assert first==first_fixed>=0
        assert second==second_fixed>=0
        repair_checks+=2
counts['repair_vertex_checks']=repair_checks
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n')
print(counts)
