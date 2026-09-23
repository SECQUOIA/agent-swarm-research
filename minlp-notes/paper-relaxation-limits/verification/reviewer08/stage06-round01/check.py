"""Reviewer08 checks; exact finite evidence and a labeled numerical radial check."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from math import sqrt
import contextlib, io, json, hashlib, re
ROOT = Path(__file__).resolve().parents[3]
SNAP = ROOT/'process/snapshots/stage06-round01'

def solve(rows, rhs):
    n=len(rhs); a=[list(map(Q,row))+[Q(b)] for row,b in zip(rows,rhs)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:return None
        a[j],a[pivot]=a[pivot],a[j]; p=a[j][j]
        a[j]=[v/p for v in a[j]]
        for i in range(n):
            if i!=j:
                t=a[i][j]; a[i]=[x-t*y for x,y in zip(a[i],a[j])]
    return tuple(row[-1] for row in a)

# Independently enumerate the candidate auxiliary polytope's vertices and
# show every vertex belongs to one original disjunct, for finite parameters.
counts=[]
for transverse in [1,2,3]:
    n=transverse+2
    for U,R in [(Q(16),Q(1)),(Q(49,4),Q(1,4)),(Q(25),Q(4))]:
        rows=[]; rhs=[]
        for j in range(n):
            row=[Q(0)]*n; row[j]=-1; rows.append(row);rhs.append(Q(0))
        for j in [0,1]:
            row=[Q(0)]*n; row[j]=1; rows.append(row);rhs.append(U)
        rows += [[0,0]+[1]*transverse,[1]*n]; rhs += [R,U+R]
        vertices=set()
        for ids in combinations(range(len(rows)),n):
            v=solve([rows[i] for i in ids],[rhs[i] for i in ids])
            if v is not None and all(sum(a*b for a,b in zip(row,v))<=b for row,b in zip(rows,rhs)):
                vertices.add(v)
        assert vertices
        for a,b,*cs in vertices:
            assert a+sum(cs)<=R or b+sum(cs)<=R
        counts.append([transverse,str(U),str(R),len(vertices)])

# Exact rational retained-box lift and stronger endpoint-image witness.
for t,w in product([Q(i,10) for i in range(31)],[Q(i,10) for i in range(-10,11)]):
    assert t*t<=3*t and (t-3)**2<=9-3*t and w*w<=1
rotations=[]
for D in [Q(2),Q(7,3),Q(10),Q(100)]:
    v=(3*D,4*D);p=(2*D,4*D/3)
    for x,center in zip(p,v):
        assert max(x*x,(x-center)**2)<=center*center/2
        assert 2*max(x*x,(x-center)**2)<=(center+1)**2
    t=(3*p[0]+4*p[1])/5;w=(4*p[0]-3*p[1])/5
    assert t==34*D/15 and w==4*D/5
    assert t*t+w*w==sum(x*x for x in p)
    rotations.append(str(D))

# Numerical sampling corroborates, and does not prove, the radial maximizer.
radial=[]
for d,r in [(3.,1.),(10.,2.),(100.,1.)]:
    vals=[]
    for i in range(1001):
        rho=r*i/1000;e=sqrt((d/2+r)**2-rho*rho/2)-d/2
        vals.append(sqrt(e*e+rho*rho)-r)
    predicted=sqrt(r*r+(sqrt((d/2+r)**2-r*r/2)-d/2)**2)-r
    assert all(a<=b+1e-12 for a,b in zip(vals,vals[1:]))
    assert abs(max(vals)-predicted)<1e-12
    radial.append([d,r,predicted])

# Replay complete printed finite computations without writing into the snapshot.
replays={}
for name in ['appendix-cubic-certificates.tex','appendix-finite-signings.tex']:
    text=(SNAP/'sections'/name).read_text()
    code='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',text,re.S))
    output=io.StringIO()
    with contextlib.redirect_stdout(output):exec(compile(code,name,'exec'),{})
    replays[name]=output.getvalue().strip()

report={'pdf_sha256':hashlib.sha256((SNAP/'main.pdf').read_bytes()).hexdigest(),
        'exact_auxiliary_vertex_enumerations':counts,'retained_box_lift_points':31*21,
        'exact_rational_rotations':rotations,'numerical_radial_samples':radial,
        'printed_program_replays':replays,
        'limits':'Finite exact checks and numerical radial sampling supplement analytic derivations; no universal theorem or external source proof is certified.'}
(ROOT/'verification/reviewer08/stage06-round01/check-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
