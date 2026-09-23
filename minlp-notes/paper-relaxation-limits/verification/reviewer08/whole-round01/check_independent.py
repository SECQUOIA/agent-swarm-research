"""Independent finite/symbolic review checks; no universal claims from grids."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json, math, re
import sympy as sp

ROOT = Path(__file__).resolve().parent
SNAP = ROOT.parents[2] / 'process/snapshots/whole-round01'
out = {}

def solve(A, b):
    A = [list(map(Q, row)) + [Q(v)] for row, v in zip(A,b)]
    n = len(A)
    for j in range(n):
        pivot = next((i for i in range(j,n) if A[i][j]), None)
        if pivot is None: return None
        A[j], A[pivot] = A[pivot], A[j]
        v = A[j][j]; A[j] = [x/v for x in A[j]]
        for i in range(n):
            if i != j:
                v = A[i][j]
                A[i] = [x-v*y for x,y in zip(A[i],A[j])]
    return tuple(row[-1] for row in A)

# Independently enumerate all vertices of the proposed auxiliary polyhedron.
# Membership in one original disjunct at each vertex verifies equality for
# each finite rational case, without any convex-hull solver.
aux_cases=[]
for transverse in (1,2,3):
  for r,d in ((Q(1),Q(3)),(Q(2),Q(5)),(Q(1,2),Q(7,4))):
    n=transverse+2; U=(d+r)**2; r2=r*r
    rows=[]; bounds=[]
    for j in range(n):
        row=[0]*n; row[j]=-1; rows.append(row); bounds.append(0)
    for j in (0,1):
        row=[0]*n; row[j]=1; rows.append(row); bounds.append(U)
    rows += [[0,0]+[1]*transverse,[1]*n]; bounds += [r2,U+r2]
    vertices=set()
    for inds in combinations(range(len(rows)),n):
        v=solve([rows[i] for i in inds],[bounds[i] for i in inds])
        if v is not None and all(sum(a*x for a,x in zip(row,v))<=b for row,b in zip(rows,bounds)):
            vertices.add(v)
    assert vertices
    assert all(v[0]+sum(v[2:])<=r2 or v[1]+sum(v[2:])<=r2 for v in vertices)
    aux_cases.append([transverse,str(r),str(d),len(vertices)])
out['exact_auxiliary_vertex_cases']=aux_cases

t,d,r,z=sp.symbols('t d r z', real=True)
assert sp.expand(t*t+(t-d)**2+z-((d+r)**2+r*r) - (2*(t-d/2)**2+z-2*(d/2+r)**2))==0
e=sp.sqrt((d/2+r)**2-z/2)-d/2
assert sp.simplify(sp.diff(e*e+z,z)-(sp.Rational(1,2)+d/(4*sp.sqrt((d/2+r)**2-z/2))))==0
M=sp.Matrix([[3,4],[4,-3]])/5
assert M.T*M==sp.eye(2) and M.det()==-1
assert M*sp.Matrix([2*d,4*d/3])==sp.Matrix([34*d/15,4*d/5])
out['symbolic_psplit_identities']=True

# Numerical falsification attempt along the complete radial boundary.
errors=[]
for ratio in (2.00001,2.1,3,5,10,100,1000):
    r0=1.; d0=ratio
    predicted=math.hypot(r0,math.sqrt((d0/2+r0)**2-r0*r0/2)-d0/2)-r0
    maximum=0.
    for j in range(10001):
        rho=r0*j/10000
        t0=d0/2-math.sqrt((d0/2+r0)**2-rho*rho/2)
        val=max(0.,math.hypot(t0,rho)-r0)
        maximum=max(maximum,val)
        assert val<=predicted+1e-11
    errors.append([ratio,predicted,maximum])
out['numerical_radial_maxima']=errors

# Replay the actual printed finite proofs, from frozen source text, separately
# from the new checks above.  Standard integer/rational arithmetic only.
for name in ('appendix-finite-signings.tex','appendix-cubic-certificates.tex'):
    source=(SNAP/'sections'/name).read_text()
    code='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',source,re.S))
    (ROOT/(name+'.printed.py')).write_text(code)
    exec(compile(code,name,'exec'),{})
out['printed_finite_proofs_replayed']=True
(ROOT/'checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
