"""Independent exact finite checks; no numerical solver and no universal inference."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json, re

OUT=Path(__file__).resolve().parent
SNAP=OUT.parents[2]/'process/snapshots/stage06-round01'

def unique_solution(cols, rhs):
    n=len(cols)
    a=[[F(col[i]) for col in cols]+[F(rhs[i])] for i in range(len(rhs))]
    row=0
    piv=[]
    for j in range(n):
        k=next((i for i in range(row,len(a)) if a[i][j]),None)
        if k is None: continue
        a[row],a[k]=a[k],a[row]
        q=a[row][j]; a[row]=[x/q for x in a[row]]
        for i in range(len(a)):
            if i!=row:
                q=a[i][j]; a[i]=[x-q*y for x,y in zip(a[i],a[row])]
        piv.append(j); row+=1
    if any(all(not x for x in r[:n]) and r[-1] for r in a): return None
    if row<n: return None
    ans=[F(0)]*n
    for i,j in enumerate(piv): ans[j]=a[i][-1]
    return ans

def hull_cost(atoms,target):
    best=None
    for k in range(1,min(len(target)+1,len(atoms))+1):
        for ids in combinations(range(len(atoms)),k):
            weights=unique_solution([[1]+list(atoms[j][:-1]) for j in ids],[1]+list(target))
            if weights is None or min(weights)<0: continue
            cost=sum(w*atoms[j][-1] for w,j in zip(weights,ids))
            best=cost if best is None else min(best,cost)
    return best

# Convex line E can be replaced by its two endpoints at every scale.
line=[(s,s*t,t,F(s!=1)) for s in (0,1,2) for t in (0,1)]
assert hull_cost(line,(1,1,F(1,2)))==1
# Rectangular convex E, diagnostic cost, every grid point in the scale-one slice.
rectangle=[(s,s*x,t,F(s!=1)) for s in (0,1,2) for x,t in product((0,1),repeat=2)]
rect_cases=0
for x,t in product((F(i,4) for i in range(5)),repeat=2):
    assert hull_cost(rectangle,(1,x,t))==0
    rect_cases+=1
# Nonconvex extensive domain, signed operating and scale costs, including zero.
f={0:F(1),1:F(-3),3:F(1)}
c={-1:F(3),2:F(-2)}
atoms=[(s,s*x,s*c[x]+f[s]) for s,x in product(f,c)]
perspective_cases=0
for lam in (F(i,4) for i in range(13)):
    for q in (F(-1)+F(3*i,8) for i in range(9)):
        x=lam*q
        fc=1-4*lam if lam<=1 else 2*lam-5
        expected=(4*lam-5*x)/3+fc
        assert hull_cost(atoms,(lam,x))==expected
        perspective_cases+=1
# Exact symmetry covariance/RLT construction; PSD follows analytically from
# projection blocks, while this test checks diagonal and cross bounds/distances.
pairs=0
for n in range(5,26):
    k=(n+3)//4; nx=(n+1)//2
    mu=[[F(3,4) if i<nx else F(1,2) for i in range(n)],
        [F(3,4) if i<k else F(1,2) for i in range(n)]]
    mats=[]
    for coord in range(2):
        lo=[F(1,2) if i<(nx if coord==0 else k) else F(0) for i in range(n)]
        mat=[]
        for i in range(n):
            row=[]
            for j in range(n):
                cov=F(1,16) if i==j and lo[i] else F(1,4) if i==j else F(-1,16*(k-1)) if i<k and j<k else F(0)
                z=mu[coord][i]*mu[coord][j]+cov
                a,b=lo[i],lo[j]; x,y=mu[coord][i],mu[coord][j]
                assert min(z-a*y-b*x+a*b,x-z-a+a*y,y-z-b+b*x,1-x-y+z)>=0
                row.append(z); pairs+=1
            assert row[i]==(lo[i]+1)*mu[coord][i]-lo[i]
            mat.append(row)
        mats.append(mat)
    target=F(k,4*(k-1))
    distances=[sum(M[i][i]+M[j][j]-2*M[i][j] for M in mats) for i,j in combinations(range(n),2)]
    assert min(distances)==target
# Replay the *printed* finite cubic certificate to check executable evidence.
tex=(SNAP/'sections/appendix-cubic-certificates.tex').read_text()
blocks=re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}',tex,re.S)
exec('\n'.join(blocks),{})
result={'arithmetic':'exact Fraction/integer','scale_cost_counterexample':True,'rectangular_grid_cases':rect_cases,'perspective_grid_cases':perspective_cases,'point_packing_ordered_coordinate_pairs':pairs,'printed_cubic_checker':'passed','scope':'Finite exact examples and replay; not general theorem verification.'}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
